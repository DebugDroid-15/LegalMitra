"""
LegalMitra LLM Provider Interface
Defines the interchangeable abstract contract for Large Language Model backends.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    """Message object for conversational LLM prompting."""
    role: str = Field(..., description="'system', 'user', or 'assistant'")
    content: str = Field(...)


class LLMResponse(BaseModel):
    """Normalized response payload from an LLM invocation."""
    content: str
    model_name: str
    usage: Dict[str, Any] = Field(default_factory=dict)
    finish_reason: Optional[str] = "stop"
    raw_response: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM backends (NVIDIA Nemotron, local NIM, vLLM, mock).
    """

    @abstractmethod
    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.1,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Executes text generation request.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if the provider is properly configured with credentials."""
        pass

