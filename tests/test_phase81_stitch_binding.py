"""Phase 81 Test Suite: Stitch Dynamic API Binding & Real-Time SSE Token Streaming.

Validates that:
1. '/assets/stitch_stream.js' is served with JavaScript MIME type and contains SSE stream handlers.
2. '/chat' HTML includes the interactive DOM anchors ('stitch-query-input', 'stitch-send-btn', 'stitch-conversation-container', 'stitch-export-pdf-btn').
3. End-to-end integration: Calling the SSE stream endpoint yields tokens compatible with the frontend reader.
4. Calling the PDF memo export endpoint produces a valid PDF binary matching frontend download logic.
"""

from fastapi.testclient import TestClient
import pytest

from legalmitra.server.api import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


class TestPhase81StitchBinding:
    def test_serve_stitch_stream_js(self, client):
        response = client.get("/assets/stitch_stream.js")
        assert response.status_code == 200
        assert "application/javascript" in response.headers.get("content-type", "") or "text/javascript" in response.headers.get("content-type", "")
        assert "initStitchStreamClient" in response.text
        assert "/api/v1/query/stream" in response.text
        assert "event: token" in response.text

    def test_chat_html_contains_dom_anchors(self, client):
        response = client.get("/chat")
        assert response.status_code == 200
        html = response.text
        assert 'id="stitch-query-input"' in html
        assert 'id="stitch-send-btn"' in html
        assert 'id="stitch-conversation-container"' in html
        assert 'id="stitch-export-pdf-btn"' in html
        assert 'stitch_stream.js' in html

    def test_e2e_stream_endpoint_contract_for_stitch(self, client):
        payload = {
            "query": "What are the essential ingredients of Section 138 NI Act?",
            "mock_mode": True
        }
        response = client.post("/api/v1/query/stream", json=payload)
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")
        body = response.text
        assert "event: metadata" in body
        assert "event: token" in body
        assert "event: done" in body

    def test_e2e_pdf_export_contract_for_stitch(self, client):
        payload = {
            "notice_type": "ni138",
            "sender": {"name": "Senior Counsel", "address": "Delhi", "advocate_name": "Advocate-on-Record"},
            "recipient": {"name": "Respondent Entity", "address": "Mumbai"},
            "facts": {
                "cheque_number": "482019",
                "cheque_amount": "500000",
                "memo_date": "2024-10-15",
                "dishonour_reason": "Funds Insufficient"
            }
        }
        response = client.post("/api/v1/draft/export/pdf", json=payload)
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/pdf"
        assert response.content.startswith(b"%PDF")
