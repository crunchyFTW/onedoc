"""Statistics and metrics for GET /statistics."""
from typing import List

# Counters (single event loop - no atomics needed for asyncio)
_messages_processed: int = 0
_messages_succeeded: int = 0
_messages_failed: int = 0
_total_retries: int = 0
_total_tokens: int = 0
_processing_times_ms: List[float] = []

# Worker tracking
_active_workers: int = 0
_idle_workers: int = 0


def increment_processed() -> None:
    global _messages_processed
    _messages_processed += 1


def increment_succeeded() -> None:
    global _messages_succeeded
    _messages_succeeded += 1


def increment_failed() -> None:
    global _messages_failed
    _messages_failed += 1


def add_retries(count: int) -> None:
    global _total_retries
    _total_retries += count


def add_tokens(tokens: int) -> None:
    global _total_tokens
    _total_tokens += tokens


def add_processing_time_ms(ms: float) -> None:
    _processing_times_ms.append(ms)


def set_worker_counts(active: int, idle: int) -> None:
    global _active_workers, _idle_workers
    _active_workers = active
    _idle_workers = idle


def get_average_processing_time_ms() -> float:
    if not _processing_times_ms:
        return 0.0
    return sum(_processing_times_ms) / len(_processing_times_ms)


def get_average_tokens_per_message() -> float:
    completed = _messages_succeeded
    if completed == 0:
        return 0.0
    return _total_tokens / completed


def get_stats(
    current_queue_length: int,
    active_workers: int,
    idle_workers: int,
) -> dict:
    """Build the full statistics dict for GET /statistics."""
    set_worker_counts(active_workers, idle_workers)
    return {
        "messagesProcessed": _messages_processed,
        "messagesSucceeded": _messages_succeeded,
        "messagesFailed": _messages_failed,
        "totalRetries": _total_retries,
        "averageProcessingTimeMs": round(get_average_processing_time_ms(), 2),
        "averageTokensPerMessage": round(get_average_tokens_per_message(), 2),
        "totalTokensUsed": _total_tokens,
        "currentQueueLength": current_queue_length,
        "idleWorkers": idle_workers,
        "activeWorkers": active_workers,
    }
