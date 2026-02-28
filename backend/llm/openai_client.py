"""OpenAI LLM client."""
from llm.base import BaseLLMClient
from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    OPENAI_API_KEY,
)


class OpenAILLMClient(BaseLLMClient):
    """OpenAI API client."""

    async def complete(self, question: str) -> tuple[str, int]:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            messages=[
                {"role": "system", "content": self.MEDICAL_SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        content = response.choices[0].message.content or ""
        usage = response.usage
        tokens = usage.total_tokens if usage else len(content.split())
        return content, tokens
