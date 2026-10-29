"""
Tests for LegalMitra CLI Module (legalmitra.cli).
Verifies single-query mode, formatting, JSON serialization, and argument parsing.
"""

import json
from unittest.mock import patch
import pytest

from legalmitra.cli import (
    DEMO_CASES,
    format_response_terminal,
    response_to_dict,
)
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.pipeline import LegalQueryPipeline


class TestLegalMitraCLI:
    """Verifies CLI formatting, JSON serialization, and pipeline execution."""

    @pytest.fixture
    def pipeline(self):
        return LegalQueryPipeline()

    def test_single_query_formatting(self, pipeline):
        """Test terminal formatting output on a standard legal query."""
        resp = pipeline.execute("Under Section 29A of IBC, who is disqualified from submitting a resolution plan?")
        output = format_response_terminal(resp, verbose=True)

        assert "QUERY:" in output
        assert "DECISION POLICY STATE:" in output
        assert "GOVERNING PROVISIONS & AUTHORITIES" in output
        assert "FORMAL CITATIONS" in output
        assert "PROPOSITION-LEVEL CLAIMS" in output
        assert "Execution Telemetry:" in output

    def test_response_to_dict_serialization(self, pipeline):
        """Test conversion of OrchestratedLegalResponse into clean JSON dictionary."""
        resp = pipeline.execute("Can interim injunction be granted under Specific Relief Act Section 20A?")
        data = response_to_dict(resp)

        assert isinstance(data, dict)
        assert data["query"] == "Can interim injunction be granted under Specific Relief Act Section 20A?"
        assert data["response_state"] in [s.value for s in LegalResponseState]
        assert isinstance(data["citations"], list)
        assert isinstance(data["governing_provisions"], list)
        assert isinstance(data["claims"], list)
        assert "telemetry" in data
        assert "duration_ms" in data["telemetry"]

        # Ensure json.dumps works without serialization error
        serialized = json.dumps(data)
        assert len(serialized) > 0

    def test_clarification_formatting(self, pipeline):
        """Test clarification response formatting in CLI."""
        resp = pipeline.execute("Can a landlord evict a tenant for personal requirement under rent control law?")
        output = format_response_terminal(resp, verbose=False)

        assert "[ CLARIFICATION_REQUIRED ]" in output
        assert "CLARIFICATION REQUIRED FROM USER:" in output

    def test_demo_cases_catalog(self):
        """Verify that demo cases catalog is properly populated."""
        assert len(DEMO_CASES) >= 5
        for case in DEMO_CASES:
            assert "id" in case
            assert "title" in case
            assert "query" in case
            assert "expected" in case
