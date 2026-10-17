"""
Tests for LegalMitra Phase 23 Source Change Impact Analyzer.
Covers:
- Mapping amendments to affected chunks in database
- Mapping statutory modifications to affected evaluation benchmark cases
- Severity calculation (CRITICAL, HIGH, LOW)
- Recommended regression test suite outputs
"""

import pytest
from pathlib import Path

from legalmitra.corpus.impact_analyzer import (
    ChangeType,
    ImpactSeverity,
    SourceChangeImpactAnalyzer,
)


@pytest.fixture
def analyzer():
    return SourceChangeImpactAnalyzer(
        db_path="data/legalmitra_kb.db",
        eval_cases_path="data/13_evaluation/evaluation_cases_v2.json",
    )


def test_bnss_section_482_amendment_impact(analyzer):
    """
    Test impact of an amendment to BNSS Section 482 (Anticipatory Bail).
    Must map to EVAL-STAT-001 and have CRITICAL severity.
    """
    report = analyzer.analyze_change(
        act_title="Bharatiya Nagarik Suraksha Sanhita",
        sections_affected=["Section 482"],
        change_type=ChangeType.AMENDMENT,
        effective_date="2026-11-01",
    )
    assert report.affected_chunk_count > 0
    assert "EVAL-STAT-001" in report.affected_eval_cases
    assert report.severity == ImpactSeverity.CRITICAL
    assert len(report.recommended_regression_tests) >= 2


def test_delhi_rent_control_section_14_impact(analyzer):
    """
    Test impact of an amendment to Delhi Rent Control Act Section 14.
    Must map to EVAL-STAT-002.
    """
    report = analyzer.analyze_change(
        act_title="Delhi Rent Control Act",
        sections_affected=["Section 14"],
        change_type=ChangeType.AMENDMENT,
    )
    assert "EVAL-STAT-002" in report.affected_eval_cases
    assert report.severity == ImpactSeverity.CRITICAL


def test_unindexed_statute_impact(analyzer):
    """
    Test impact of an amendment to an unindexed hypothetical law.
    Must yield LOW severity and 0 affected chunks.
    """
    report = analyzer.analyze_change(
        act_title="Goa Fisheries Preservation Act 1970",
        sections_affected=["Section 9"],
        change_type=ChangeType.AMENDMENT,
    )
    assert report.affected_chunk_count == 0
    assert report.affected_eval_count == 0
    assert report.severity == ImpactSeverity.LOW

