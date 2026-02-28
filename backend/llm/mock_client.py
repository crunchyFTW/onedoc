"""Mock LLM client for testing without API keys."""
import asyncio
import random

from llm.base import BaseLLMClient


# Simple keyword-based simulated responses (mock only - not real medical advice)
_MOCK_RESPONSES = {
    "head": "Headaches can have many causes: tension, dehydration, lack of sleep, or eye strain. Try rest, hydration, and over-the-counter pain relief if appropriate. If severe, sudden, or persistent, see a doctor.",
    "blue": "Blue discoloration on skin can indicate bruising, circulation issues, or other conditions. If new, spreading, or concerning, have it checked by a healthcare provider.",
    "blur": "Blurred vision or blurs on skin could indicate various conditions. Blue spots on skin might be bruising. For vision changes or unexplained skin changes, a healthcare provider should evaluate you.",
    "hand": "Hand symptoms depend on the cause. Swelling, color changes, or pain could be circulation, injury, or other issues. A doctor can perform a proper examination.",
    "hurt": "Pain can stem from many sources. Rest, gentle movement, and OTC pain relievers may help mild cases. Persistent or severe pain warrants medical evaluation.",
    "pain": "Pain management depends on the type and cause. Over-the-counter options may help mild pain. Always consult a doctor for persistent or severe symptoms.",
    "fever": "Fever often indicates infection. Rest and fluids help. If fever is high, prolonged, or in infants, seek medical care.",
    "default": "As a medical expert, I'd consider your symptoms in context. Common steps include rest, hydration, and monitoring. For personalized advice, consult a healthcare professional.",
}


class MockLLMClient(BaseLLMClient):
    """Simulates LLM responses with random delay and contextual mock answers."""

    async def complete(self, question: str) -> tuple[str, int]:
        delay = random.uniform(1.0, 3.0)
        await asyncio.sleep(delay)
        tokens = len(question.split()) * 3 + 80

        q_lower = question.lower()
        response = _MOCK_RESPONSES["default"]
        for keyword, text in _MOCK_RESPONSES.items():
            if keyword != "default" and keyword in q_lower:
                response = text
                break

        response += "\n\n[Note: This is a mock response. Set LLM_PROVIDER=gemini in .env with GEMINI_API_KEY for real AI answers.]"
        return response, tokens
