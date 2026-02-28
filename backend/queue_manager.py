"""asyncio.Queue for pending message IDs. Single process, single event loop."""
import asyncio

_queue: asyncio.Queue[str] | None = None


def get_queue() -> asyncio.Queue[str]:
    """Get or create the global asyncio.Queue."""
    global _queue
    if _queue is None:
        _queue = asyncio.Queue()
    return _queue


def queue_size() -> int:
    """Current number of items in the queue."""
    if _queue is None:
        return 0
    return _queue.qsize()
