"""
Tests for LegalMitra LLM Provider Interface and NVIDIA Nemotron Adapter.
"""

import os
from unittest.mock import MagicMock, patch
import pytest

from legalmitra.core.errors import LLMProviderError
from legalmitra.llm.interface import LLMMessage
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.llm.nemotron import NemotronLLMProvider


def test_nemotron_unconfigured_error(monkeypatch):
    monkeypatch.delenv("NEMOTRON_API_KEY", raising=False)
    provider = NemotronLLMProvider(api_key=None)
    assert not provider.is_available()

    with pytest.raises(LLMProviderError, match="credentials not configured"):
        provider.generate([LLMMessage(role="user", content="Hello")])


def test_nemotron_env_configuration(monkeypatch):
    monkeypatch.setenv("NEMOTRON_API_KEY", "nvapi-test-secret-key")
    monkeypatch.setenv("NEMOTRON_BASE_URL", "https://custom.nim.endpoint/v1")
    monkeypatch.setenv("NEMOTRON_MODEL_NAME", "nvidia/nemotron-4-340b-instruct")

    provider = NemotronLLMProvider()
    assert provider.is_available()
    assert provider.api_key == "nvapi-test-secret-key"
    assert provider.base_url == "https://custom.nim.endpoint/v1"
    assert provider.model_name == "nvidia/nemotron-4-340b-instruct"


def test_nemotron_mock_request(monkeypatch):
    monkeypatch.setenv("NEMOTRON_API_KEY", "nvapi-test-secret-key")
    provider = NemotronLLMProvider(base_url="https://api.nvidia.com/v1")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {"role": "assistant", "content": "Under Section 61 of BSA 2023..."},
                "finish_reason": "stop",
            }
        ],
        "usage": {"total_tokens": 42},
    }

    with patch("requests.post", return_value=mock_resp) as mock_post:
        messages = [
            LLMMessage(role="system", content="You are a legal data assistant."),
            LLMMessage(role="user", content="State Section 61 BSA."),
        ]
        res = provider.generate(messages, temperature=0.1)

        assert mock_post.called
        call_args, call_kwargs = mock_post.call_args
        assert call_args[0] == "https://api.nvidia.com/v1/chat/completions"
        assert "Bearer nvapi-test-secret-key" in call_kwargs["headers"]["Authorization"]
        assert call_kwargs["json"]["model"] == provider.model_name

        assert res.content == "Under Section 61 of BSA 2023..."
        assert res.finish_reason == "stop"


def test_mock_llm_provider():
    mock = MockLLMProvider("Deterministic test legal answer.")
    assert mock.is_available()

    res = mock.generate([LLMMessage(role="user", content="Explain privacy.")])
    assert res.content == "Deterministic test legal answer."
    assert len(mock.calls) == 1

