"""
Hardened Unit and Integration Tests for LegalMitra Web API & Endpoints
Verifies session isolation, rate limiting, request validation, deletion, and failure modes.
Uses deterministic mocking for standard offline runs to avoid external network dependencies.
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from legalmitra.llm.interface import BaseLLMProvider, LLMResponse
from legalmitra.web.app import app, check_rate_limit, _rate_limit_cache
from legalmitra.web.schemas import ChatResponse, HealthStatus


class FastMockLLM(BaseLLMProvider):
    """Deterministic mock provider for offline Web API integration tests."""
    def is_available(self) -> bool:
        return True

    def generate(self, messages, **kwargs) -> LLMResponse:
        user_msg = messages[-1].content
        if "extraterrestrial" in user_msg.lower() or "moon" in user_msg.lower():
            return LLMResponse(
                content="The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law.",
                model_name="FastMockLLM"
            )
        return LLMResponse(
            content=(
                "Under Section 438 of the Code of Criminal Procedure, 1973, when any person has reason "
                "to believe that he may be arrested on an accusation of having committed a non-bailable offence, "
                "he may apply to the High Court or the Court of Session for a direction that in the event of such arrest, "
                "he shall be released on bail. [Code of Criminal Procedure, 1973, Section 438]"
            ),
            model_name="FastMockLLM"
        )


@pytest.fixture
def mock_rag_engine(monkeypatch):
    """Ensure tests run offline against deterministic mock without consuming tokens."""
    from legalmitra.web.app import rag_engine
    orig_provider = rag_engine.llm_provider
    rag_engine.llm_provider = FastMockLLM()
    yield rag_engine
    rag_engine.llm_provider = orig_provider


@pytest.fixture
def client(mock_rag_engine):
    # Reset rate limit cache before tests
    _rate_limit_cache.clear()
    return TestClient(app)


def test_health_check_endpoint(client):
    """Verify system health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "LegalMitra AI Chatbot"
    assert data["knowledge_base_chunks"] > 0
    assert data["active_sources"] > 0


def test_readiness_probe_endpoint(client):
    """Verify readiness probe confirms knowledge base availability."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["kb_status"] == "connected"
    assert data["chunks_indexed"] > 0


def test_landing_page_endpoint(client):
    """Verify landing page HTML delivery and CTA links."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "LegalMitra" in response.text
    assert "/chat" in response.text


def test_chat_page_endpoint(client):
    """Verify chat application interface delivery."""
    response = client.get("/chat")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "LegalMitra" in response.text
    assert "New Legal Consultation" in response.text


def test_chat_api_submission(client):
    """Verify API chat submission, citation extraction, and cookie generation."""
    payload = {
        "query": "What does Section 438 of the CrPC deal with regarding anticipatory bail?",
        "limit": 3
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    assert "legalmitra_session" in response.cookies
    data = response.json()
    assert "conversation_id" in data
    assert data["query"] == payload["query"]
    assert len(data["answer"]) > 0
    assert "citations" in data
    assert "evidence" in data
    assert len(data["evidence"]) > 0
    assert "legal_disclaimer" in data


def test_chat_api_insufficient_evidence(client):
    """Verify API handles query with insufficient evidence gracefully without failure."""
    payload = {
        "query": "What are the rules regarding extraterrestrial mineral rights on the Moon under Indian law?",
        "limit": 3
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["evidence_sufficiency"] == "insufficient"
    ans_lower = data["answer"].lower()
    assert "not provide sufficient evidence" in ans_lower or "insufficient" in ans_lower


def test_session_isolation_and_cross_session_protection(client):
    """
    Verify that Client A cannot access or list Client B's conversations.
    """
    # Client A creates conversation
    client_a_session = "session_alice_1234567890123456"
    headers_a = {"X-Session-ID": client_a_session}
    resp_a = client.post(
        "/api/v1/chat",
        json={"query": "Explain anticipatory bail under CrPC 438"},
        headers=headers_a
    )
    assert resp_a.status_code == 200
    conv_id_a = resp_a.json()["conversation_id"]

    # Client A can list and retrieve it
    list_a = client.get("/api/v1/conversations", headers=headers_a)
    assert list_a.status_code == 200
    assert any(c["conversation_id"] == conv_id_a for c in list_a.json())

    msgs_a = client.get(f"/api/v1/conversations/{conv_id_a}/messages", headers=headers_a)
    assert msgs_a.status_code == 200
    assert len(msgs_a.json()) >= 2

    # Client B (different session) tries to list conversations
    client_b_session = "session_bob_9876543210987654"
    headers_b = {"X-Session-ID": client_b_session}
    list_b = client.get("/api/v1/conversations", headers=headers_b)
    assert list_b.status_code == 200
    # Client B MUST NOT see Client A's conversation
    assert not any(c["conversation_id"] == conv_id_a for c in list_b.json())

    # Client B tries to read Client A's conversation directly by ID
    msgs_b = client.get(f"/api/v1/conversations/{conv_id_a}/messages", headers=headers_b)
    assert msgs_b.status_code == 404  # Access denied / not found

    # Client B tries to delete Client A's conversation
    del_b = client.delete(f"/api/v1/conversations/{conv_id_a}", headers=headers_b)
    assert del_b.status_code == 404

    # Client A deletes their own conversation
    del_a = client.delete(f"/api/v1/conversations/{conv_id_a}", headers=headers_a)
    assert del_a.status_code == 200
    assert del_a.json()["status"] == "deleted"


def test_rate_limiting_enforcement(client):
    """Verify that exceeding rate limit triggers HTTP 429."""
    headers = {"X-Session-ID": "test_rate_limited_session_123456"}
    payload = {"query": "Tell me about Section 138 of the NI Act."}

    # Simulate hitting rate limit threshold
    for _ in range(30):
        assert check_rate_limit("test_rate_limited_session_123456:testclient") is True

    # 31st request should be rejected by rate limiter
    assert check_rate_limit("test_rate_limited_session_123456:testclient") is False

    resp = client.post("/api/v1/chat", json=payload, headers=headers)
    assert resp.status_code == 429
    assert "Rate limit exceeded" in resp.json()["detail"]


def test_payload_size_enforcement(client):
    """Verify that payloads exceeding 64KB are rejected with HTTP 413."""
    huge_query = "A" * (70 * 1024)
    resp = client.post("/api/v1/chat", json={"query": huge_query})
    # Will fail either at content-length middleware (413) or Pydantic validation (422)
    assert resp.status_code in (413, 422)


def test_feedback_submission(client):
    """Verify recording of user evaluation feedback."""
    payload = {
        "conversation_id": "conv_test_123",
        "query": "Is Section 438 applicable?",
        "is_helpful": True,
        "feedback_text": "Very accurate citation."
    }
    resp = client.post("/api/v1/feedback", json=payload)
    assert resp.status_code == 200
    assert resp.json()["status"] == "recorded"
