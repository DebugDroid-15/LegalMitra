from fastapi.testclient import TestClient
from legalmitra.server.api import app


def test_brief_summarize_endpoint_success():
    client = TestClient(app)
    judgment_sample = """
    IN THE SUPREME COURT OF INDIA
    CRIMINAL APPEAL NO. 1420 OF 2023
    Vikram Singh & Anr. v. State of Punjab
    CORAM: HON'BLE MR. JUSTICE ABHAY S. OKA
    JUDGMENT:
    We hold that compliance with Section 41A of the CrPC is mandatory.
    The appeal is allowed.
    """
    response = client.post("/api/v1/brief/summarize", json={"judgment_text": judgment_sample})
    assert response.status_code == 200
    data = response.json()
    assert data["court"] == "Supreme Court of India"
    assert "Appeal Allowed" in data["disposition"]
    assert len(data["statutory_transitions"]) > 0
    assert "full_brief_markdown" in data


def test_brief_summarize_endpoint_empty_error():
    client = TestClient(app)
    response = client.post("/api/v1/brief/summarize", json={"judgment_text": "   "})
    assert response.status_code == 400

