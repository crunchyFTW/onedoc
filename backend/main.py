"""FastAPI app: HTTP API, lifespan, CORS."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import SERVER_PORT, LOG_FILE_PATH
from models import (
    ChatQuestionRequest,
    ChatSubmitResponse,
    ChatStatusResponse,
    StatisticsResponse,
)
from worker import start_workers, stop_workers
from controller import (
    submit_chat_controller,
    get_chat_status_controller,
    get_statistics_controller,
)
import metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start workers on startup, stop on shutdown."""
    metrics.bootstrap_from_log(LOG_FILE_PATH)
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
    """Submit a medical question and return a message ID."""
    return await submit_chat_controller(request)


@app.get("/chat/{message_id}", response_model=ChatStatusResponse)
async def get_chat_status(message_id: str):
    """Get status and response for a submitted question."""
    return await get_chat_status_controller(message_id)


@app.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """Get system metrics."""
    stats = await get_statistics_controller()
    return StatisticsResponse(**stats)


if __name__ == "__main__":
    import uvicorn

    # Keep reload off by default because in-memory storage is cleared on restart.
    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, reload=False)
