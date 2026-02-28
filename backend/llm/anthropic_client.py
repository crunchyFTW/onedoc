"""Anthropic LLM client."""
from llm.base import BaseLLMClient
from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    ANTHROPIC_API_KEY,
)


class AnthropicLLMClient(BaseLLMClient):
    """Anthropic API client."""

    async def complete(self, question: str) -> tuple[str, int]:
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set")

        from anthropic import AsyncAnthropic

        client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            system=self.MEDICAL_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}],
        )
        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        return content, tokens
