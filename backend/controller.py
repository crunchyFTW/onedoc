"""Application controller functions used by API routes."""
import uuid

from fastapi import HTTPException

import metrics
from models import ChatQuestionRequest, ChatStatusResponse, ChatSubmitResponse
from queue_manager import get_queue, queue_size
from storage import create_message, get_message
from worker import get_active_worker_count, get_worker_pool_size, ensure_workers_for_load


async def submit_chat_controller(request: ChatQuestionRequest) -> ChatSubmitResponse:
    """Create a new message, enqueue it, and ensure workers are available."""
    message_id = str(uuid.uuid4())
    create_message(request.question, message_id)
    queue = get_queue()
    await queue.put(message_id)
    await ensure_workers_for_load()
    return ChatSubmitResponse(messageId=message_id)


async def get_chat_status_controller(message_id: str) -> ChatStatusResponse:
    """Return current processing status for a submitted message."""
    rec = get_message(message_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Message not found")

    if rec.status == "completed":
        return ChatStatusResponse(status="completed", answer=rec.answer)
    if rec.status == "failed":
        return ChatStatusResponse(status="failed", error=rec.error or "Unknown error")
    return ChatStatusResponse(status="processing")


async def get_statistics_controller() -> dict:
    """Compute and return the current statistics payload."""
    active = get_active_worker_count()
    pool_size = get_worker_pool_size()
    idle = max(0, pool_size - active)
    return metrics.get_stats(
        current_queue_length=queue_size(),
        active_workers=active,
        idle_workers=idle,
    )
