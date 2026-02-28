"""Google Gemini LLM client. Uses REST API with X-goog-api-key header (AI Studio format).
Model: gemini-flash-latest (per AI Studio examples)."""
import asyncio
import re

import httpx

from llm.base import BaseLLMClient
from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    GEMINI_API_KEY,
)

RATE_LIMIT_RETRIES = 1
RATE_LIMIT_DEFAULT_WAIT = 35
FALLBACK_MODEL = "gemini-flash-latest"


class GeminiLLMClient(BaseLLMClient):
    """Google Gemini API via REST. Key in X-goog-api-key header (matches AI Studio curl)."""

    def _parse_retry_seconds(self, resp: httpx.Response) -> int:
        try:
            data = resp.json()
            for d in data.get("error", {}).get("details", []) or []:
                if d.get("@type", "").endswith("RetryInfo"):
                    delay = d.get("retryDelay", "")
                    if isinstance(delay, str) and (m := re.search(r"(\d+)", delay)):
                        return max(int(m.group(1)), 30)
        except Exception:
            pass
        return RATE_LIMIT_DEFAULT_WAIT

    async def _call_api(self, model: str, payload: dict) -> httpx.Response:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY,
        }
        async with httpx.AsyncClient(timeout=90.0) as client:
            return await client.post(url, headers=headers, json=payload)

    def _extract_text(self, cand: dict) -> str:
        """Extract text from candidate (ignores thoughtSignature, etc.)."""
        parts = cand.get("content", {}).get("parts", [])
        return "".join(p.get("text", "") for p in parts if isinstance(p.get("text"), str))

    async def complete(self, question: str) -> tuple[str, int]:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")

        payload = {
            "contents": [{"parts": [{"text": question}]}],
            "systemInstruction": {"parts": [{"text": self.MEDICAL_SYSTEM_PROMPT}]},
            "generationConfig": {
                "temperature": LLM_TEMPERATURE,
                "maxOutputTokens": LLM_MAX_TOKENS,
            },
        }

        models_to_try = [LLM_MODEL, FALLBACK_MODEL] if LLM_MODEL != FALLBACK_MODEL else [LLM_MODEL]
        last_resp = None

        for model in models_to_try:
            for attempt in range(RATE_LIMIT_RETRIES + 1):
                resp = await self._call_api(model, payload)
                last_resp = resp
                if resp.status_code == 200:
                    break
                if resp.status_code == 429 and attempt < RATE_LIMIT_RETRIES:
                    await asyncio.sleep(self._parse_retry_seconds(resp))
                    continue
                if resp.status_code == 429 and model != models_to_try[-1]:
                    break
                if resp.status_code == 429:
                    raise RuntimeError(
                        "Gemini API rate limit exceeded. Try again in a few minutes."
                    )
                resp.raise_for_status()
            if last_resp and last_resp.status_code == 200:
                break

        if not last_resp or last_resp.status_code != 200:
            raise RuntimeError("Gemini API request failed.")

        data = last_resp.json()
        text = ""
        tokens = 0

        if "candidates" in data and data["candidates"]:
            text = self._extract_text(data["candidates"][0])
        if "usageMetadata" in data:
            meta = data["usageMetadata"]
            tokens = meta.get("totalTokenCount") or (
                meta.get("promptTokenCount", 0)
                + meta.get("candidatesTokenCount", 0)
            )
        if not tokens:
            tokens = len(text.split()) + len(question.split())

        return text, tokens
