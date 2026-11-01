from fastapi.testclient import TestClient
from legalmitra.server.api import app


def test_contract_audit_endpoint_risky_success():
    client = TestClient(app)
    contract_text = """
    1. Employee agrees not to engage in competing business for 2 years following termination.
    2. Any claim must be brought within 90 days or be barred.
    3. Sole arbitrator shall be appointed unilaterally by the Company.
    """
    response = client.post("/api/v1/contract/audit", json={
        "contract_text": contract_text,
        "contract_title": "Employment Agreement"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["composite_risk_score"] >= 70
    assert data["critical_risks_count"] >= 2
    assert "NON-COMPLIANT" in data["overall_compliance_verdict"]
    assert len(data["findings"]) >= 3


def test_contract_audit_endpoint_empty_error():
    client = TestClient(app)
    response = client.post("/api/v1/contract/audit", json={"contract_text": "  "})
    assert response.status_code == 400

