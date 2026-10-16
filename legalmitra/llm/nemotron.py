"""
LegalMitra NVIDIA Nemotron Provider
Connects to NVIDIA Nemotron models hosted via NVIDIA NIM, NGC API, or private inference endpoints.
API credentials and endpoints are resolved dynamically from environment variables.
"""

import os
import time
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import requests

load_dotenv()

from legalmitra.core.errors import LLMProviderError
from legalmitra.core.logging import get_logger
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage, LLMResponse

logger = get_logger("nemotron_provider")


class NemotronLLMProvider(BaseLLMProvider):
    """
    LLM provider interface for NVIDIA Nemotron models (e.g. Nemotron-4-340B, Llama-3.1-Nemotron-70B).
    Credentials and endpoint URLs are loaded from environment variables:
      - NEMOTRON_API_KEY: Secret Bearer token
      - NEMOTRON_BASE_URL: Base API endpoint (e.g. https://integrate.api.nvidia.com/v1)
      - NEMOTRON_MODEL_NAME: Target model identifier
      - NEMOTRON_API_FORMAT: 'openai_compatible' or custom
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        api_format: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
    ):
        self.api_key = api_key or os.environ.get("NEMOTRON_API_KEY")
        self.base_url = (base_url or os.environ.get("NEMOTRON_BASE_URL", "https://integrate.api.nvidia.com/v1")).rstrip("/")
        self.model_name = model_name or os.environ.get("NEMOTRON_MODEL_NAME", "nvidia/llama-3.1-nemotron-70b-instruct")
        self.api_format = api_format or os.environ.get("NEMOTRON_API_FORMAT", "openai_compatible")
        self.timeout = float(timeout_seconds or os.environ.get("NEMOTRON_TIMEOUT_SECONDS", "60.0"))

    def is_available(self) -> bool:
        """Returns True if the required API key and base URL are configured."""
        return bool(self.api_key and self.base_url)

    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.1,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> LLMResponse:
        if not self.is_available():
            raise LLMProviderError(
                "NVIDIA Nemotron credentials not configured. Please set the 'NEMOTRON_API_KEY' "
                "environment variable or pass an api_key to NemotronLLMProvider."
            )

        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "LegalMitra-DataEngine/1.0",
        }

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        payload.update(kwargs)

        max_retries = 3
        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Dispatching generation request to endpoint ({self.model_name}), attempt {attempt}/{max_retries}...")
                response = requests.post(endpoint, json=payload, headers=headers, timeout=self.timeout)

                if response.status_code == 401:
                    raise LLMProviderError(f"NVIDIA API Authentication failed (401 Unauthorized): {response.text}")
                elif response.status_code == 404:
                    raise LLMProviderError(f"Endpoint or model not found (404 Not Found) at {endpoint}: {response.text}")
                elif response.status_code >= 500:
                    logger.warning(f"NVIDIA API returned HTTP {response.status_code}. Retrying in 2s...")
                    time.sleep(2.0)
                    continue
                elif response.status_code != 200:
                    raise LLMProviderError(f"NVIDIA API returned error status {response.status_code}: {response.text}")

                res_json = response.json()
                choices = res_json.get("choices", [])
                if not choices:
                    raise LLMProviderError("Empty choices returned from API.")

                msg = choices[0].get("message", {})
                content = msg.get("content", "")
                finish_reason = choices[0].get("finish_reason", "stop")
                usage = res_json.get("usage", {})

                return LLMResponse(
                    content=content,
                    model_name=self.model_name,
                    usage=usage,
                    finish_reason=finish_reason,
                    raw_response=res_json,
                )

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as te:
                last_error = te
                logger.warning(f"Inference request attempt {attempt} failed ({te}). Retrying...")
                time.sleep(2.0)
            except requests.exceptions.RequestException as re:
                raise LLMProviderError(f"Network error communicating with API: {re}") from re

        raise LLMProviderError(f"API request timed out after {max_retries} attempts: {last_error}")

