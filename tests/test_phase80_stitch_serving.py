"""Phase 80 Test Suite: Stitch Web Application Packaging & Static Asset Serving.

Validates that:
1. Root '/' endpoint returns 200 OK and serves Stitch Landing Page HTML.
2. '/chat' endpoint returns 200 OK and serves Stitch Consultation UI HTML.
3. '/assets' static directory correctly serves CSS/PNG image mockups.
"""

from fastapi.testclient import TestClient
import pytest

from legalmitra.server.api import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


class TestPhase80StitchServing:
    def test_serve_stitch_landing_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "LegalMitra" in response.text
        assert "Indian Legal Intelligence" in response.text
        assert "/chat" in response.text

    def test_serve_stitch_chat_consultation(self, client):
        response = client.get("/chat")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "LegalMitra" in response.text
        assert "BNSS" in response.text

    def test_serve_stitch_static_assets(self, client):
        response = client.get("/assets/chat_active.png")
        assert response.status_code == 200
        assert "image/png" in response.headers.get("content-type", "")

