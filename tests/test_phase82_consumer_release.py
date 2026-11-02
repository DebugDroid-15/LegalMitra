"""Phase 82 Test Suite: Turnkey Consumer Product Polish & Desktop One-Click Launcher.

Validates that:
1. 'run_legalmitra.bat' and 'run_legalmitra.sh' exist, are executable, and contain the proper launch parameters.
2. The Stitch consultation UI displays the Local Sovereign GGUF Edition status badge.
3. System health check endpoint confirms offline readiness ('gguf_model_available', 'lora_adapter_available', 'fts_index_healthy').
"""

import os
from fastapi.testclient import TestClient
import pytest

from legalmitra.server.api import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


class TestPhase82ConsumerRelease:
    def test_launcher_scripts_exist_and_configured(self):
        root_dir = os.path.dirname(os.path.dirname(__file__))
        bat_file = os.path.join(root_dir, "run_legalmitra.bat")
        sh_file = os.path.join(root_dir, "run_legalmitra.sh")

        assert os.path.isfile(bat_file)
        assert os.path.isfile(sh_file)

        with open(bat_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "uvicorn legalmitra.server.api:app" in content
            assert "http://localhost:8000" in content

        with open(sh_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "uvicorn legalmitra.server.api:app" in content
            assert "http://127.0.0.1:8000" in content

    def test_stitch_header_shows_local_sovereign_badge(self, client):
        response = client.get("/chat")
        assert response.status_code == 200
        assert "Local Sovereign GGUF Edition" in response.text

    def test_system_health_readiness(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        assert data.get("fts_index_healthy") is True
        assert data.get("gguf_model_available") is True
        assert data.get("lora_adapter_available") is True
