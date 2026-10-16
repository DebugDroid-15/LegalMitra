"""
Live Integration Tests for NVIDIA Nemotron LLM Provider.
These tests make genuine API calls to the configured NVIDIA endpoint and are
separately marked with @pytest.mark.live so standard offline CI runs skip them.
"""

import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from legalmitra.llm.nemotron import NemotronLLMProvider
from legalmitra.llm.interface import LLMMessage
from legalmitra.generation.validator import extract_json_from_response


@pytest.mark.live
def test_live_nemotron_inference():
    """Verify live inference against NVIDIA endpoint with genuine API key."""
    api_key = os.environ.get("NEMOTRON_API_KEY")
    if not api_key:
        pytest.skip("NEMOTRON_API_KEY not set. Skipping live inference test.")

    provider = NemotronLLMProvider(timeout_seconds=60.0)
    assert provider.is_available()

    messages = [
        LLMMessage(
            role="system",
            content="You are an Indian legal assistant. Respond only with valid JSON.",
        ),
        LLMMessage(
            role="user",
            content="Provide the title of Section 61 of the Bharatiya Sakshya Adhiniyam, 2023. Format: {\"section\": 61, \"title\": \"...\"}",
        ),
    ]

    response = provider.generate(messages, temperature=0.1, max_tokens=256)

    assert response is not None
    assert response.content
    assert response.model_name == provider.model_name

    # Token accounting
    assert "prompt_tokens" in response.usage
    assert "completion_tokens" in response.usage
    assert response.usage["total_tokens"] > 0

    # JSON extractability
    json_str = extract_json_from_response(response.content)
    assert json_str.startswith("{") or json_str.startswith("[")


@pytest.mark.live
def test_live_nemotron_error_handling():
    """Verify error handling on invalid credentials."""
    invalid_provider = NemotronLLMProvider(api_key="nvapi-invalid-key-for-testing")
    with pytest.raises(Exception):
        invalid_provider.generate([LLMMessage(role="user", content="Hello")])

