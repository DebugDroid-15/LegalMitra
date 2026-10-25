"""
Test Suite for LegalMitra Phase 54:
Temporal Authority Graph, Precedent Conflict Resolution & Point-in-Time Legal Reasoning.
"""

import pytest
import datetime
from pathlib import Path

from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    GraphEdge,
    GraphNode,
    LegalKnowledgeGraph,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.temporal.engine import (
    StatutoryApplicabilityState,
    TemporalLawEngine,
    build_default_temporal_engine,
)
from legalmitra.orchestration.evidence_orchestrator import (
    UnifiedEvidenceOrchestrator,
)
from legalmitra.orchestration.query_understanding import LegalQueryAnalyzer
from legalmitra.evaluation.release_gates import GateStatus, ReleaseGateEvaluator
from legalmitra.evaluation.contamination import ContaminationAuditor
import json


class TestPhase54TemporalAuthorityGraph:
    """Tests the canonical legal-authority graph integrity, endpoints, and conflict resolution."""

    def test_canonical_graph_endpoints_and_integrity(self):
        graph = build_national_judicial_knowledge_graph()
        report = graph.validate_graph_integrity()
        assert report["is_valid"] is True
        assert report["orphan_endpoints_count"] == 0
        assert report["duplicate_edges_count"] == 0
        assert report["invalid_temporal_edges_count"] == 0
        assert report["total_nodes"] >= 99
        assert report["total_edges"] >= 62

    def test_graph_detects_orphan_endpoints(self):
        graph = LegalKnowledgeGraph()
        graph.add_node(GraphNode("NODE-1", EntityType.CASE, "Case 1"))
        # Add edge to nonexistent target
        with pytest.raises(ValueError) as exc:
            graph.add_edge(GraphEdge("E-1", "NODE-1", "NODE-NONEXISTENT", RelationType.CITES))
        assert "must exist in graph" in str(exc.value)

    def test_graph_detects_invalid_temporal_interval(self):
        graph = LegalKnowledgeGraph()
        graph.add_node(GraphNode("N-1", EntityType.CASE, "Case 1"))
        graph.add_node(GraphNode("N-2", EntityType.SECTION, "Section 1"))
        graph.add_edge(GraphEdge(
            "E-INVALID-DATES", "N-1", "N-2", RelationType.INTERPRETS,
            valid_from="2024-01-01", valid_to="2020-01-01"  # Invalid!
        ))
        res = graph.validate_graph_integrity()
        assert res["is_valid"] is False
        assert res["invalid_temporal_edges_count"] == 1
        assert "valid_from is later than valid_to" in res["invalid_temporal_edges"][0]["error"]

    def test_precedent_conflict_hierarchy_resolution(self):
        graph = build_national_judicial_knowledge_graph()
        # Supreme Court (Vodafone SC 2012) vs High Court (Vodafone Bom HC 2010)
        res = graph.resolve_precedent_conflict("CASE-SC-VODAFONE-2012", "CASE-HC-BOM-VODAFONE-2010")
        assert res["is_resolvable"] is True
        assert res["conflict_status"] == "RESOLVED_BY_HIERARCHY"
        assert res["binding_authority"] == "CASE-SC-VODAFONE-2012"
        assert "Article 141" in res["rationale"]

    def test_precedent_conflict_bench_strength_resolution(self):
        graph = build_national_judicial_knowledge_graph()
        # 3-Judge Bench (Rangappa 2010) vs 2-Judge Bench (Krishna Janardhan Bhat 2008)
        # Note: Rangappa also explicitly overrules Krishna Janardhan Bhat
        res = graph.resolve_precedent_conflict("CASE-RANGAPPA", "CASE-KRISHNA-BHAT")
        assert res["is_resolvable"] is True
        assert res["conflict_status"] in ("RESOLVED_BY_OVERRULING", "RESOLVED_BY_BENCH_STRENGTH")
        assert res["binding_authority"] == "CASE-RANGAPPA"

    def test_precedent_conflict_territorial_forum_resolution(self):
        graph = build_national_judicial_knowledge_graph()
        # Inter-High Court: Bombay HC vs Delhi HC on Section 29A Arbitration
        # In Delhi forum (IN-DL)
        res_dl = graph.resolve_precedent_conflict(
            "CASE-HC-BOM-ARBITRATION-2021", "CASE-HC-DEL-ARBITRATION-2021", target_jurisdiction="IN-DL"
        )
        assert res_dl["is_resolvable"] is True
        assert res_dl["conflict_status"] == "RESOLVED_BY_TERRITORIAL_JURISDICTION"
        assert res_dl["binding_authority"] == "CASE-HC-DEL-ARBITRATION-2021"

        # In national forum (IN): must remain unresolved with qualified output
        res_in = graph.resolve_precedent_conflict(
            "CASE-HC-BOM-ARBITRATION-2021", "CASE-HC-DEL-ARBITRATION-2021", target_jurisdiction="IN"
        )
        assert res_in["is_resolvable"] is False
        assert res_in["conflict_status"] == "UNRESOLVED_INTER_HIGH_COURT_SPLIT"
        assert res_in["binding_authority"] is None
        assert res_in["requires_qualification"] is True


class TestPhase54PointInTimeStatutoryApplicability:
    """Tests deterministic point-in-time statutory applicability and interval boundaries."""

    def test_copyright_section52_boundary_dates(self):
        engine = build_default_temporal_engine()
        # Day before 2012 amendment takes effect
        res_before = engine.resolve_point_in_time_applicability("COP-SEC-52", "2012-06-20")
        assert res_before["is_applicable"] is True
        assert res_before["version_number"] == 1
        assert res_before["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL

        # Effective date of 2012 amendment
        res_on = engine.resolve_point_in_time_applicability("COP-SEC-52", "2012-06-21")
        assert res_on["is_applicable"] is True
        assert res_on["version_number"] == 2
        assert res_on["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_APPLICABLE

        # Prior to enactment of Copyright Act 1957
        res_pre_enact = engine.resolve_point_in_time_applicability("COP-SEC-52", "1950-01-01")
        assert res_pre_enact["is_applicable"] is False
        assert res_pre_enact["applicability_state"] == StatutoryApplicabilityState.NOT_YET_IN_FORCE

    def test_uncommenced_statute_handling_dpdp(self):
        engine = build_default_temporal_engine()
        res = engine.resolve_point_in_time_applicability("DPDP-SEC-1", "2024-05-01")
        assert res["is_applicable"] is False
        assert res["applicability_state"] == StatutoryApplicabilityState.PARTIALLY_COMMENCED
        assert "uncommenced or subject to phased notification" in res["rationale"]

    def test_it_act_66a_unconstitutional_repeal(self):
        engine = build_default_temporal_engine()
        # While Section 66A was operative
        res_valid = engine.resolve_point_in_time_applicability("IT-SEC-66A", "2013-01-01")
        assert res_valid["is_applicable"] is True
        assert res_valid["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL

        # After Shreya Singhal struck it down on 2015-03-24
        res_struck = engine.resolve_point_in_time_applicability("IT-SEC-66A", "2020-01-01")
        assert res_struck["is_applicable"] is False
        assert res_struck["applicability_state"] == StatutoryApplicabilityState.SUPERSEDED_OR_REPEALED

    def test_missing_query_date_returns_insufficient_evidence(self):
        engine = build_default_temporal_engine()
        res = engine.resolve_point_in_time_applicability("COP-SEC-52", query_date_str=None)
        assert res["is_applicable"] is False
        assert res["applicability_state"] == StatutoryApplicabilityState.INSUFFICIENT_EVIDENCE
        assert "No query date provided" in res["rationale"]


class TestPhase54AuthorityAwareOrchestration:
    """Tests production path integration in UnifiedEvidenceOrchestrator."""

    def test_orchestration_produces_authority_resolution_traces(self):
        analyzer = LegalQueryAnalyzer()
        parsed_q = analyzer.parse_query("Under Section 52 of Copyright Act, does course pack photocopying violate copyright?", context_date="2010-05-10")
        orchestrator = UnifiedEvidenceOrchestrator()
        evidence_set = orchestrator.orchestrate_evidence(parsed_q)

        # Must contain point-in-time trace
        assert len(evidence_set.authority_resolution_traces) > 0
        pit_traces = [t for t in evidence_set.authority_resolution_traces if "applicability_state" in t]
        assert len(pit_traces) > 0
        assert pit_traces[0]["provision_id"] == "COP-SEC-52"
        assert pit_traces[0]["version_number"] == 1
        assert pit_traces[0]["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL


class TestPhase54PITV10BenchmarkAndReleaseGates:
    """Verifies PIT-V10 benchmark expansion, contamination isolation, and release gates."""

    def test_pit_v10_manifest_counts_and_zero_contamination(self):
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13")
        assert data["version"] in ("10.0.0", "11.0.0", "12.0.0", "13.0.0")
        assert len(data["test_cases"]) >= 160
        assert data["split_counts"]["held_out_evaluation"] >= 55

        # Contamination audit
        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(data["test_cases"])
        assert report.exact_duplicates_count == 0
        assert report.near_duplicates_count == 0
        assert report.max_cross_split_jaccard <= 0.85
        assert report.audit_verdict in ("PASS", "ZERO_CONTAMINATION_VERIFIED")

    def test_release_quality_gates_phase54(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")
        assert summary.target_version in ("0.54.0", "0.55.0", "0.56.0", "0.57.0")
        assert summary.total_gates in (11, 15, 20)
        assert summary.passed_gates in (10, 14, 19)
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"
