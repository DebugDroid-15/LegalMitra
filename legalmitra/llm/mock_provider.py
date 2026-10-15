"""
LegalMitra Mock LLM Provider
Deterministic mock backend for offline testing, CI/CD, and pipeline verification.
"""

from typing import Any, List
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage, LLMResponse


class MockLLMProvider(BaseLLMProvider):
    """
    Simulates LLM completions using source-grounded canned responses for testing.
    """

    def __init__(self, fixed_response: str = "Source-grounded simulated response under Indian law."):
        self.fixed_response = fixed_response
        self.calls: List[List[LLMMessage]] = []

    def is_available(self) -> bool:
        return True

    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.1,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> LLMResponse:
        self.calls.append(messages)
        return LLMResponse(
            content=self.fixed_response,
            model_name="mock-nemotron-offline",
            usage={"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
            finish_reason="stop",
            raw_response={"mock": True},
        )

