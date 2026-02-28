"""Async LLM workers. Consume from queue, call LLM, update storage and metrics."""
import asyncio
import time

from config import MAX_RETRIES, RETRY_DELAY, WORKER_COUNT
from queue_manager import get_queue
from storage import (
    get_message,
    update_status,
    update_result,
    update_completed_at,
)
from llm import get_llm_client
from logging_utils import append_log_entry
import metrics

_worker_tasks: list[asyncio.Task] = []
_worker_active_count = 0
_worker_lock = asyncio.Lock()


async def _run_worker(worker_id: str) -> None:
    """Single worker loop: dequeue message_id, process with LLM, update store."""
    global _worker_active_count

    queue = get_queue()
    llm = get_llm_client()

    while True:
        try:
            # Wait for next job (with timeout for graceful shutdown)
            message_id = await asyncio.wait_for(
                queue.get(),
                timeout=30.0,  # Check periodically for shutdown
            )
        except asyncio.TimeoutError:
            continue  # No job, loop again

        async with _worker_lock:
            _worker_active_count += 1

        retries = 0
        last_error = ""
        start_time = time.perf_counter()

        try:
            update_status(message_id, "processing")
            rec = get_message(message_id)
            question = rec.question if rec else ""

            while retries <= MAX_RETRIES:
                try:
                    answer, tokens = await llm.complete(question)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000
                    update_result(
                        message_id,
                        answer=answer,
                        tokens_used=tokens,
                        processing_time_ms=elapsed_ms,
                        retry_count=retries,
                    )
                    update_status(message_id, "completed")
                    update_completed_at(message_id)

                    metrics.increment_processed()
                    metrics.increment_succeeded()
                    metrics.add_tokens(tokens)
                    metrics.add_processing_time_ms(elapsed_ms)
                    if retries > 0:
                        metrics.add_retries(retries)

                    await append_log_entry(
                        worker_id=worker_id,
                        message_id=message_id,
                        question=question,
                        response_or_error=answer,
                        is_error=False,
                    )
                    break
                except Exception as e:
                    last_error = str(e)
                    # Surface rate limit clearly for user
                    if "429" in last_error or "rate limit" in last_error.lower():
                        last_error = "Gemini API rate limit exceeded. Free tier has strict limits. Wait a few minutes or use mock mode."
                    retries += 1
                    if retries <= MAX_RETRIES:
                        metrics.add_retries(1)
                        await asyncio.sleep(RETRY_DELAY)
                    else:
                        metrics.increment_processed()
                        metrics.increment_failed()
                        update_result(message_id, error=last_error, retry_count=retries)
                        update_status(message_id, "failed")
                        update_completed_at(message_id)
                        await append_log_entry(
                            worker_id=worker_id,
                            message_id=message_id,
                            question=question,
                            response_or_error=f"LLM request failed after retries: {last_error}",
                            is_error=True,
                        )
        finally:
            async with _worker_lock:
                _worker_active_count -= 1
            queue.task_done()


def get_active_worker_count() -> int:
    return _worker_active_count


async def start_workers() -> None:
    """Start worker tasks. Call from FastAPI lifespan."""
    global _worker_tasks
    for i in range(WORKER_COUNT):
        t = asyncio.create_task(_run_worker(f"worker-{i}"))
        _worker_tasks.append(t)


async def stop_workers() -> None:
    """Cancel worker tasks gracefully."""
    global _worker_tasks
    for t in _worker_tasks:
        t.cancel()
    await asyncio.gather(*_worker_tasks, return_exceptions=True)
    _worker_tasks = []
