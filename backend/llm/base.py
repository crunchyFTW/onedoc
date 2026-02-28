"""Abstract base class for LLM clients."""
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Base class for LLM providers."""

    MEDICAL_SYSTEM_PROMPT = """You are a medical expert assistant. Provide accurate, 
concise, and helpful information about health topics. Always recommend users consult 
a healthcare professional for personal medical advice. Be clear and avoid overly 
technical jargon when possible."""

    @abstractmethod
    async def complete(self, question: str) -> tuple[str, int]:
        """
        Send question to LLM and return (response_text, tokens_used).
        Raises Exception on failure.
        """
        pass
