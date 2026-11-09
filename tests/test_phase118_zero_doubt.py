"""
Unit tests for Phase 118: Edge Case Hallucination & Zero-Doubt Verification Engine.
"""

import pytest
from legalmitra.orchestration.zero_doubt_engine import (
    ZeroDoubtVerificationEngine,
    VerificationStatus,
)


class TestPhase118ZeroDoubtEngine:
    def test_struck_down_section_66a_flagged(self):
        text = "You can be jailed under Section 66A of Information Technology Act for offensive messages."
        report = ZeroDoubtVerificationEngine.audit_response(text, query="offensive messages")
        assert report.is_valid is False
        assert report.verification_status == VerificationStatus.UNCONSTITUTIONAL_STRUCK_DOWN
        assert any("Shreya Singhal" in f for f in report.flagged_hallucinations)
        assert report.grounding_score < 1.0

    def test_struck_down_section_66a_properly_sanitized(self):
        text = "You can be jailed under Section 66A of Information Technology Act for offensive messages."
        sanitized = ZeroDoubtVerificationEngine.guard_and_sanitize(text, query="offensive messages")
        assert "> [!CAUTION]" in sanitized
        assert "Constitutional Compliance Warning" in sanitized
        assert "Shreya Singhal" in sanitized

    def test_fake_citation_reporter_flagged(self):
        text = "In XYZ v. ABC, 2024 SCC 99999, the Supreme Court held that..."
        report = ZeroDoubtVerificationEngine.audit_response(text, query="arbitrary query")
        assert report.is_valid is False
        assert any("Fabricated" in f for f in report.flagged_hallucinations)

    def test_temporal_cutoff_boundary_post_july_2024(self):
        text = "The accused committed theft punishable under Indian Penal Code, 1860 Section 379."
        report = ZeroDoubtVerificationEngine.audit_response(text, query="theft", incident_date="2024-09-15")
        assert report.verification_status == VerificationStatus.TEMPORAL_MISMATCH
        assert "Bharatiya Nyaya Sanhita" in report.temporal_compliance_notes

    def test_valid_bns_response_passes(self):
        text = "### ⚖️ Direct Position\nUnder **Section 318(4)** of **The Bharatiya Nyaya Sanhita, 2023**, cheating is punishable up to 7 years."
        report = ZeroDoubtVerificationEngine.audit_response(text, query="cheating", incident_date="2024-10-01")
        assert report.is_valid is True
        assert report.grounding_score == 1.0
        assert "Section 318(4)" in report.detected_citations
