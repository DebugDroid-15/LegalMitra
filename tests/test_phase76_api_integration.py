from fastapi.testclient import TestClient
from legalmitra.server.api import app


def test_api_health_includes_gguf_status():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "gguf_model_available" in data
    assert data["gguf_model_available"] is True
    assert data["status"] == "healthy"


def test_api_query_with_mock_model():
    client = TestClient(app)
    payload = {
        "query": "What is the punishment for theft under BNS?",
        "model_mode": "mock",
        "language": "en"
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Bharatiya Nyaya Sanhita" in data["answer_text"] or len(data["governing_provisions"]) > 0


def test_api_chat_turn_deterministic():
    client = TestClient(app)
    payload = {
        "session_id": "test_sess_gguf_integration",
        "message": "Explain cheque bounce under NI Act",
        "model_mode": "deterministic"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test_sess_gguf_integration"
    assert "Section 138" in data["answer_text"] or "138" in str(data["citations"])
