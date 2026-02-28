"""In-memory message store. Single event loop - no thread safety needed."""
from typing import Dict, Optional

from models import MessageRecord


# In-memory dict: messageId -> MessageRecord
_messages: Dict[str, MessageRecord] = {}


def create_message(question: str, message_id: str) -> MessageRecord:
    """Create and store a new message with status 'pending'."""
    record = MessageRecord(messageId=message_id, question=question, status="pending")
    _messages[message_id] = record
    return record


def get_message(message_id: str) -> Optional[MessageRecord]:
    """Get a message by ID. Returns None if not found."""
    return _messages.get(message_id)


def update_status(message_id: str, status: str) -> None:
    """Update message status."""
    if message_id in _messages:
        _messages[message_id].status = status


def update_result(
    message_id: str,
    answer: Optional[str] = None,
    error: Optional[str] = None,
    tokens_used: int = 0,
    processing_time_ms: Optional[float] = None,
    retry_count: int = 0,
) -> None:
    """Update message with result, tokens, and timing."""
    if message_id not in _messages:
        return
    rec = _messages[message_id]
    if answer is not None:
        rec.answer = answer
    if error is not None:
        rec.error = error
    rec.tokensUsed = tokens_used
    if processing_time_ms is not None:
        rec.processingTimeMs = processing_time_ms
    rec.retryCount = retry_count


def update_completed_at(message_id: str) -> None:
    """Set completedAt timestamp."""
    from datetime import datetime

    if message_id in _messages:
        _messages[message_id].completedAt = datetime.utcnow()
