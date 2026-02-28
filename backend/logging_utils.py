"""Async-safe shared log writer for chat interactions."""
import asyncio
from datetime import datetime

from config import LOG_FILE_PATH

_lock = asyncio.Lock()


async def append_log_entry(
    worker_id: str,
    message_id: str,
    question: str,
    response_or_error: str,
    is_error: bool = False,
) -> None:
    """
    Append a log entry to the shared log file.
    Uses asyncio.Lock for safe concurrent writes.
    """
    timestamp = datetime.utcnow().isoformat()
    kind = "error" if is_error else "response"
    line = f"{timestamp} | worker={worker_id} | messageId={message_id} | question={repr(question)} | {kind}={repr(response_or_error)}\n"

    async with _lock:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(line)
