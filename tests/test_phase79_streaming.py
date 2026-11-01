"""Tests for Phase 79: Real-time SSE token streaming for local GGUF engine."""

import json
from fastapi.testclient import TestClient
import pytest

from legalmitra.models.gguf_adapter import GGUFAdapterConfig, LocalGGUFModelAdapter
from legalmitra.server.api import app


class TestPhase79TokenStreaming:
    """Test suite certifying real-time token streaming."""

    def test_mock_stream_generator_tokens(self):
        """Verify that stream_natural_answer yields sequential chunks."""
        config = GGUFAdapterConfig(enable_mock_for_testing=True)
        adapter = LocalGGUFModelAdapter(config)

        stream = list(adapter.stream_natural_answer(
            query="Test query",
            provisions=[],
            precedents=[]
        ))
        assert len(stream) > 1
        full_text = "".join(stream)
        assert "### Issue" in full_text
        assert "Bharatiya Nyaya Sanhita" in full_text

    def test_rest_api_stream_endpoint_sse(self):
        """Verify REST API SSE streaming protocol."""
        client = TestClient(app)
        payload = {
            "query": "What is minor theft under BNS?",
            "mock_mode": True
        }
        response = client.post("/api/v1/query/stream", json=payload)
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        body = response.text
        assert "event: metadata" in body
        assert "event: token" in body
        assert "event: done" in body
        assert "completed" in body

    def test_rest_api_stream_endpoint_empty_error(self):
        """Verify validation error on empty query."""
        client = TestClient(app)
        response = client.post("/api/v1/query/stream", json={"query": "   "})
        assert response.status_code == 400
