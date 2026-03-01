"""Async-safe shared log writer for chat interactions."""
import asyncio
from datetime import datetime
from typing import Optional

from config import LOG_FILE_PATH

_lock = asyncio.Lock()


async def append_log_entry(
    worker_id: str,
    message_id: str,
    question: str,
    response_or_error: str,
    is_error: bool = False,
    retries: int = 0,
    tokens_used: int = 0,
    processing_time_ms: Optional[float] = None,
) -> None:
    """
    Append a log entry to the shared log file.
    Uses asyncio.Lock for safe concurrent writes.
    """
    timestamp = datetime.utcnow().isoformat()
    kind = "error" if is_error else "response"
    status = "failed" if is_error else "completed"
    processing_ms_str = (
        f"{processing_time_ms:.2f}" if isinstance(processing_time_ms, (float, int)) else "0.00"
    )
    line = (
        f"{timestamp} | worker={worker_id} | messageId={message_id} "
        f"| status={status} | retries={retries} | tokens={tokens_used} "
        f"| processingMs={processing_ms_str} | question={repr(question)} "
        f"| {kind}={repr(response_or_error)}\n"
    )

    async with _lock:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(line)
