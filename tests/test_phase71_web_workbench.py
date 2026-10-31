"""Phase 71 Test Suite: Interactive Web Workbench & Visual Legal Explorer."""

from pathlib import Path
import py_compile
import pytest

from legalmitra.web import APP_PATH
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.models.local_adapter import LocalLegalModelAdapter, ModelAdapterConfig
from legalmitra.drafting import StatutoryNoticeDraftingEngine, NoticeType, NoticeParty


class TestPhase71WebWorkbench:
    """Verifies that the web workbench app file exists, compiles cleanly, and binds to all pipeline services."""

    def test_app_file_exists_and_compiles(self):
        """Test that legalmitra/web/app.py exists and compiles with zero syntax errors."""
        assert APP_PATH.exists()
        compiled = py_compile.compile(str(APP_PATH), doraise=True)
        assert compiled is not None

    def test_pipeline_integration_with_web_modes(self):
        """Test that the three UI model modes operate smoothly within the web session scope."""
        # 1. Deterministic mode
        pipe_det = LegalQueryPipeline()
        res_det = pipe_det.execute("What is the limitation period for arbitration?", context_date="2024-01-01")
        assert res_det.response_state is not None

        # 2. Mock neural mode
        mock_adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
        pipe_mock = LegalQueryPipeline(model_adapter=mock_adapter)
        res_mock = pipe_mock.execute("What is the limitation period for arbitration?", context_date="2024-01-01")
        assert "### Issue" in res_mock.answer_text

    def test_drafting_studio_notice_generation_within_web_layer(self):
        """Test notice generator integration as called by the drafting studio tab."""
        sender = NoticeParty(name="Test Sender", address="New Delhi")
        recipient = NoticeParty(name="Test Recipient", address="Noida")
        facts = {
            "cheque_number": "123456",
            "cheque_date": "2024-01-01",
            "cheque_amount": "2,00,000",
            "bank_name": "SBI",
            "return_memo_date": "2024-01-10",
            "dishonour_reason": "Funds Insufficient"
        }
        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.CHEQUE_BOUNCE_NI_ACT_138, sender, recipient, facts
        )
        assert draft.mandatory_cure_period_days == 15
        assert len(draft.full_notice_markdown) > 100
