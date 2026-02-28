"""Pydantic models for API and internal use."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Request models ---


class ChatQuestionRequest(BaseModel):
    """Request body for POST /chat."""

    question: str = Field(..., min_length=1)


# --- Response models ---


class ChatSubmitResponse(BaseModel):
    """Response for POST /chat."""

    messageId: str


class ChatStatusResponse(BaseModel):
    """Response for GET /chat/{messageId}."""

    status: str  # "processing" | "completed" | "failed"
    answer: Optional[str] = None
    error: Optional[str] = None


class StatisticsResponse(BaseModel):
    """Response for GET /statistics."""

    messagesProcessed: int
    messagesSucceeded: int
    messagesFailed: int
    totalRetries: int
    averageProcessingTimeMs: float
    averageTokensPerMessage: float
    totalTokensUsed: int
    currentQueueLength: int
    idleWorkers: int
    activeWorkers: int


# --- Internal storage model ---


class MessageRecord(BaseModel):
    """Internal representation of a chat message."""

    messageId: str
    question: str
    status: str = "pending"  # pending | processing | completed | failed
    answer: Optional[str] = None
    error: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    completedAt: Optional[datetime] = None
    tokensUsed: int = 0
    processingTimeMs: Optional[float] = None
    retryCount: int = 0
