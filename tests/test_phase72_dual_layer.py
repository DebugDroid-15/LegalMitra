"""Phase 72 Test Suite: Dual-Layer Citizen & Lawyer Natural Synthesis Engine."""

import pytest
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.orchestration.query_understanding import LegalQueryAnalyzer


class TestPhase72DualLayerSynthesis:
    """Verifies plain English layperson summarization, colloquial legal synonym expansion, and dual-layer formatting."""

    def test_layperson_synonym_expansion(self):
        """Test colloquial layperson phrases expand into formal statutory candidates."""
        analyzer = LegalQueryAnalyzer()
        parsed = analyzer.parse_query("What happens in case of minor theft?")
        assert any("petty theft" in issue or "Juvenile Justice" in issue for issue in parsed.candidate_issues)

        parsed_chk = analyzer.parse_query("My cheque bounce what should I do")
        assert any("Section 138" in issue for issue in parsed_chk.candidate_issues)

    def test_plain_english_summary_generation_minor_theft(self):
        """Test query regarding minor theft produces plain English explanation covering value and juvenile aspects."""
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("What happens in case of Minor theft")

        assert "### Plain-English Summary (For Quick Understanding)" in resp.answer_text
        assert "community service" in resp.answer_text or "petty theft" in resp.answer_text
        assert "Juvenile Justice" in resp.answer_text
        assert "Direct Position:" in resp.answer_text

    def test_plain_english_summary_generation_cheque_bounce(self):
        """Test query regarding cheque bounce produces citizen guidance on notice timeline."""
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("My cheque bounce what are the steps?")

        assert "### Plain-English Summary (For Quick Understanding)" in resp.answer_text
        assert "30 days" in resp.answer_text
        assert "15 mandatory days" in resp.answer_text or "15" in resp.answer_text

    def test_plain_english_summary_generation_tenancy_eviction(self):
        """Test query regarding tenant eviction produces landlord/tenant plain guidance."""
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("Can a landlord evict a tenant immediately?")

        assert "### Plain-English Summary (For Quick Understanding)" in resp.answer_text
        assert "due legal process" in resp.answer_text or "notice to quit" in resp.answer_text

