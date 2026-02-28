"""FastAPI app: HTTP API, lifespan, CORS."""
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import SERVER_PORT, WORKER_COUNT
from models import (
    ChatQuestionRequest,
    ChatSubmitResponse,
    ChatStatusResponse,
    StatisticsResponse,
)
from storage import create_message, get_message
from queue_manager import get_queue, queue_size
from worker import start_workers, stop_workers, get_active_worker_count
import metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start workers on startup, stop on shutdown."""
    await start_workers()
    yield
    await stop_workers()


app = FastAPI(
    title="Medical Expert AI Chat",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatSubmitResponse)
async def submit_chat(request: ChatQuestionRequest):
    """Submit a medical question. Returns messageId for polling."""
    message_id = str(uuid.uuid4())
    create_message(request.question, message_id)
    queue = get_queue()
    await queue.put(message_id)
    return ChatSubmitResponse(messageId=message_id)


@app.get("/chat/{message_id}", response_model=ChatStatusResponse)
async def get_chat_status(message_id: str):
    """Get status and response for a previously submitted question."""
    rec = get_message(message_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Message not found")

    if rec.status == "completed":
        return ChatStatusResponse(status="completed", answer=rec.answer)
    if rec.status == "failed":
        return ChatStatusResponse(status="failed", error=rec.error or "Unknown error")
    return ChatStatusResponse(status="processing")


@app.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """Get system metrics."""
    active = get_active_worker_count()
    idle = WORKER_COUNT - active
    stats = metrics.get_stats(
        current_queue_length=queue_size(),
        active_workers=active,
        idle_workers=idle,
    )
    return StatisticsResponse(**stats)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, reload=True)
