"""Phase 70 Test Suite: Production REST API Server & OpenAPI Contract."""

import pytest
from fastapi.testclient import TestClient

from legalmitra.server.api import app


@pytest.fixture
def client():
    """Provides a fresh FastAPI test client."""
    return TestClient(app)


class TestPhase70RestApiEndpoints:
    """Verifies REST endpoints for query evaluation, multi-turn chat, statutory notice drafting, and health checks."""

    def test_health_endpoint(self, client):
        """Test GET /api/v1/health returns 200 with FTS and LoRA adapter statuses."""
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["fts_index_healthy"] is True
        assert data["lora_adapter_available"] is True
        assert "version" in data

    def test_query_endpoint_deterministic(self, client):
        """Test POST /api/v1/query returns full 15-stage structured response under deterministic mode."""
        payload = {
            "query": "Can an interim injunction be granted in infrastructure project contracts under Section 20A Specific Relief Act?",
            "context_date": "2024-06-01",
            "jurisdiction": "IN",
            "model_mode": "deterministic"
        }
        resp = client.post("/api/v1/query", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["response_state"] in ("ANSWER_QUALIFIED", "ANSWER_SUPPORTED")
        assert "Direct Position:" in data["answer_text"]
        assert len(data["claims"]) > 0
        assert len(data["citations"]) > 0
        assert data["duration_ms"] > 0

    def test_query_endpoint_mock_neural(self, client):
        """Test POST /api/v1/query with mock neural mode returns IRAC synthesis."""
        payload = {
            "query": "What is the procedure for digital evidence search?",
            "context_date": "2024-09-01",
            "model_mode": "mock"
        }
        resp = client.post("/api/v1/query", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["response_state"] is not None
        assert "### Issue" in data["answer_text"]
        assert "### Conclusion" in data["answer_text"]

    def test_chat_multi_turn_endpoint_and_clarification(self, client):
        """Test POST /api/v1/chat across two turns resolves clarification loop."""
        sid = "api_session_test_99"

        # Turn 1: Rent control query missing state jurisdiction
        payload_1 = {
            "session_id": sid,
            "message": "Can a landlord evict a tenant for personal bona fide requirement under rent control law?",
            "context_date": "2024-01-01"
        }
        resp1 = client.post("/api/v1/chat", json=payload_1)
        assert resp1.status_code == 200
        d1 = resp1.json()
        assert d1["turn_index"] == 1
        assert d1["response_state"] == "CLARIFICATION_REQUIRED"
        assert d1["clarification_requested"] is not None

        # Turn 2: Provide clarifying jurisdiction
        payload_2 = {
            "session_id": sid,
            "message": "The property is in Delhi under Delhi Rent Control Act."
        }
        resp2 = client.post("/api/v1/chat", json=payload_2)
        assert resp2.status_code == 200
        d2 = resp2.json()
        assert d2["turn_index"] == 2
        assert d2["response_state"] in ("ANSWER_SUPPORTED", "ANSWER_QUALIFIED")
        assert d2["persisted_jurisdiction"] == "IN-DL"

    def test_draft_statutory_notice_endpoint(self, client):
        """Test POST /api/v1/draft generates Section 138 NI Act statutory demand notice."""
        payload = {
            "notice_type": "ni138",
            "sender": {
                "name": "Alpha Corp",
                "address": "Connaught Place, New Delhi",
                "advocate_name": "Advocate R. Sharma",
                "advocate_enrollment": "D/123/2014"
            },
            "recipient": {
                "name": "Beta Enterprises",
                "address": "Sector 18, Noida"
            },
            "facts": {
                "cheque_number": "887766",
                "cheque_date": "2024-05-01",
                "cheque_amount": "12,00,000",
                "bank_name": "ICICI Bank",
                "return_memo_date": "2024-05-10",
                "dishonour_reason": "Funds Insufficient"
            },
            "as_of_date": "2024-05-15"
        }
        resp = client.post("/api/v1/draft", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["notice_type"] == "NI_ACT_138"
        assert data["mandatory_cure_period_days"] == 15
        assert "fifteen (15) days" in data["full_notice_markdown"]
        assert "Section 138" in data["full_notice_markdown"]
        assert "Advocate R. Sharma" in data["full_notice_markdown"]

    def test_openapi_schema_generation(self, client):
        """Verify OpenAPI JSON schema endpoint is valid and describes endpoints."""
        resp = client.get("/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        assert schema["info"]["title"] == "LegalMitra Intelligence API"
        assert "/api/v1/query" in schema["paths"]
        assert "/api/v1/chat" in schema["paths"]
        assert "/api/v1/draft" in schema["paths"]
        assert "/api/v1/health" in schema["paths"]
