"""Pytest fixtures. Use mock LLM to avoid API calls."""
import os

# Set before any app imports so config loads mock provider
os.environ.setdefault("LLM_PROVIDER", "mock")
os.environ.setdefault("LLM_MODEL", "gemini-flash-latest")
