"""Environment-based configuration."""
import os
from pathlib import Path

# Load .env from project root or backend/ if present
try:
    from dotenv import load_dotenv
    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / ".env")
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

# Server
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# Retries
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "2"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Workers
WORKER_IDLE_TIMEOUT = int(os.getenv("WORKER_IDLE_TIMEOUT", "30"))
WORKER_COUNT = min(
    int(os.getenv("WORKER_COUNT", str(os.cpu_count() or 4))),
    os.cpu_count() or 4,
)

# Logging
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "chat.log")

# API Keys (loaded when provider needs them, stripped of whitespace)
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
