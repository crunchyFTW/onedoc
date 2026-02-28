"""LLM client factory and providers."""
from llm.base import BaseLLMClient
from llm.mock_client import MockLLMClient
from llm.openai_client import OpenAILLMClient
from llm.anthropic_client import AnthropicLLMClient
from llm.gemini_client import GeminiLLMClient

from config import LLM_PROVIDER


def get_llm_client() -> BaseLLMClient:
    """Return the configured LLM client based on LLM_PROVIDER."""
    providers = {
        "openai": OpenAILLMClient,
        "anthropic": AnthropicLLMClient,
        "gemini": GeminiLLMClient,
        "mock": MockLLMClient,
    }
    cls = providers.get(LLM_PROVIDER, MockLLMClient)
    return cls()
