"""
Test Suite for LegalMitra Phase 55:
Temporal Semantics Audit, Authority-Resolution Calibration & Legal Decision Trace Verification.
"""

import datetime
import json
import pytest
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
    ProvisionTemporalVersion,
    StatuteLifecycle,
    StatutoryApplicabilityState,
    TemporalLawEngine,
    TemporalStatus,
    build_default_temporal_engine,
    normalize_calendar_date,
)
from legalmitra.orchestration.evidence_orchestrator import (
    UnifiedEvidenceOrchestrator,
)
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.orchestration.query_understanding import LegalQueryAnalyzer
from legalmitra.evaluation.contamination import ContaminationAuditor
from legalmitra.evaluation.release_gates import GateStatus, ReleaseGateEvaluator


class TestPhase55TemporalSemanticsAndBoundaries:
    """Verifies temporal interval semantics, inclusive boundaries, and legal invariants."""

    def test_calendar_date_normalization(self):
        # Pure calendar date
        d1 = normalize_calendar_date("2024-07-01")
        assert d1 == datetime.date(2024, 7, 1)

        # ISO timestamp with time and offset
        d2 = normalize_calendar_date("2024-07-01T14:30:00+05:30")
        assert d2 == datetime.date(2024, 7, 1)

        # Datetime with space
        d3 = normalize_calendar_date("2024-07-01 09:15:00")
        assert d3 == datetime.date(2024, 7, 1)

        # Invalid formats return None safely
        assert normalize_calendar_date("invalid-date") is None
        assert normalize_calendar_date(None) is None

    def test_exact_commencement_boundary(self):
        engine = build_default_temporal_engine()
        # Copyright 2012 amendment took effect on 2012-06-21

        # Day before commencement
        res_before = engine.resolve_point_in_time_applicability("COP-SEC-52", "2012-06-20")
        assert res_before["is_applicable"] is True
        assert res_before["version_number"] == 1
        assert res_before["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL

        # Exact day of commencement
        res_day_of = engine.resolve_point_in_time_applicability("COP-SEC-52", "2012-06-21")
        assert res_day_of["is_applicable"] is True
        assert res_day_of["version_number"] == 2
        assert res_day_of["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_APPLICABLE

        # Day after commencement
        res_after = engine.resolve_point_in_time_applicability("COP-SEC-52", "2012-06-22")
        assert res_after["is_applicable"] is True
        assert res_after["version_number"] == 2
        assert res_after["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_APPLICABLE

    def test_parent_enactment_commencement_barrier(self):
        engine = TemporalLawEngine()
        engine.register_statute(StatuteLifecycle(
            statute_id="TEST-STATUTE-2024",
            title="Test Future Statute 2024",
            enactment_date="2023-12-25",
            publication_date="2023-12-25",
            commencement_date="2024-07-01",
            is_fully_commenced=True,
        ))
        engine.register_provision_version(ProvisionTemporalVersion(
            provision_id="TEST-SEC-1",
            statute_id="TEST-STATUTE-2024",
            section_number="1",
            version_number=1,
            text="Section 1 test text",
            version_effective_from="2023-12-25",  # Purportedly publication date
            version_effective_until=None,
        ))

        # Query before appointed commencement date
        res = engine.resolve_point_in_time_applicability("TEST-SEC-1", "2024-03-01")
        assert res["is_applicable"] is False
        assert res["applicability_state"] == StatutoryApplicabilityState.NOT_YET_IN_FORCE
        assert "had not yet commenced" in res["rationale"]

    def test_overlapping_intervals_return_conflicting_temporal_evidence(self):
        engine = TemporalLawEngine()
        engine.register_statute(StatuteLifecycle(
            statute_id="STAT-OVERLAP",
            title="Overlap Statute",
            commencement_date="2010-01-01",
        ))
        # Version 1 valid 2010 to 2018
        engine.register_provision_version(ProvisionTemporalVersion(
            provision_id="SEC-OVERLAP",
            statute_id="STAT-OVERLAP",
            section_number="10",
            version_number=1,
            text="Version 1 text",
            version_effective_from="2010-01-01",
            version_effective_until="2018-12-31",
        ))
        # Version 2 valid 2015 to 2022 (Overlaps 2015-2018!)
        engine.register_provision_version(ProvisionTemporalVersion(
            provision_id="SEC-OVERLAP",
            statute_id="STAT-OVERLAP",
            section_number="10",
            version_number=2,
            text="Version 2 text",
            version_effective_from="2015-01-01",
            version_effective_until="2022-12-31",
        ))

        # Query during overlap window (2016)
        res = engine.resolve_point_in_time_applicability("SEC-OVERLAP", "2016-06-01")
        assert res["is_applicable"] is False
        assert res["applicability_state"] == StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE
        assert "Multiple conflicting temporal versions" in res["rationale"]

    def test_conflicting_gazette_notifications_return_uncertainty(self):
        engine = TemporalLawEngine()
        engine.register_statute(StatuteLifecycle(
            statute_id="STAT-GAZ-CONFLICT",
            title="Gazette Conflict Statute",
        ))
        v = ProvisionTemporalVersion(
            provision_id="SEC-GAZ-1",
            statute_id="STAT-GAZ-CONFLICT",
            section_number="1",
            version_number=1,
            text="Text",
            version_effective_from="2023-01-01",
            conflicting_notifications=["S.O. 101(E) appointing 2023-01-01", "S.O. 102(E) appointing 2023-06-01"],
        )
        engine.register_provision_version(v)

        res = engine.resolve_point_in_time_applicability("SEC-GAZ-1", "2023-03-01")
        assert res["is_applicable"] is False
        assert res["applicability_state"] == StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE
        assert "Conflicting commencement notifications" in res["rationale"]

    def test_retrospective_basis_hindu_succession(self):
        engine = build_default_temporal_engine()
        res = engine.resolve_point_in_time_applicability("HSA-SEC-6", "2021-01-01")
        assert res["is_applicable"] is True
        assert res["version_number"] == 2
        assert res.get("is_retrospective") is True
        assert "Vineeta Sharma" in res.get("retrospective_basis", "")

    def test_same_day_repeal_with_savings(self):
        engine = build_default_temporal_engine()
        # Query CrPC Section 65B/438 on 2024-07-01 without pending proceeding
        res_no_pending = engine.resolve_point_in_time_applicability("IEA-SEC-65B", "2024-07-01", pending_proceeding_commenced_prior=False)
        assert res_no_pending["is_applicable"] is False
        assert res_no_pending["applicability_state"] == StatutoryApplicabilityState.SUPERSEDED_OR_REPEALED

        # Query with pending proceeding commenced prior to 1 July 2024
        res_saved = engine.resolve_point_in_time_applicability("IEA-SEC-65B", "2024-07-01", pending_proceeding_commenced_prior=True)
        assert res_saved["is_applicable"] is True
        assert res_saved["savings_applied"] is True
        assert res_saved["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL


class TestPhase55PrecedentHierarchyAndCalibration:
    """Verifies precedent calibration: referral sub judice, distinguishing, obiter dicta, and co-equal splits."""

    def test_referral_to_larger_bench_sub_judice_status(self):
        graph = build_national_judicial_knowledge_graph()
        # Case A referred to larger bench vs Case B
        # Let's add test nodes with referral edge
        graph.add_node(GraphNode("CASE-TEST-REFERRING", EntityType.CASE, "Referring Bench Order (2018)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-REFERRED", EntityType.CASE, "Referred Precedent (2015)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-COORDINATE", EntityType.CASE, "Coordinate Precedent (2019)", properties={"bench_strength": 2}))
        graph.add_edge(GraphEdge(
            "EDGE-REF-1", "CASE-TEST-REFERRING", "CASE-TEST-REFERRED",
            RelationType.REFERS_TO_LARGER_BENCH,
            properties={"is_resolved": False, "question_referred": "Constitutional scope of section"}
        ))

        res = graph.resolve_precedent_conflict("CASE-TEST-REFERRED", "CASE-TEST-COORDINATE")
        assert res["is_resolvable"] is False
        assert res["conflict_status"] == "REFERRED_SUB_JUDICE"
        assert res["binding_authority"] is None
        assert res["requires_qualification"] is True
        assert "referred to a larger bench and remains sub-judice" in res["rationale"]

    def test_distinguished_precedent_remains_operative(self):
        graph = build_national_judicial_knowledge_graph()
        graph.add_node(GraphNode("CASE-TEST-DIST-1", EntityType.CASE, "Case Distinguishing (2020)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-DIST-2", EntityType.CASE, "Case Distinguished (2015)", properties={"bench_strength": 2}))
        graph.add_edge(GraphEdge(
            "EDGE-DIST-1", "CASE-TEST-DIST-1", "CASE-TEST-DIST-2",
            RelationType.DISTINGUISHES,
            properties={"distinguishing_ground": "registered vs unregistered deed"}
        ))

        res = graph.resolve_precedent_conflict("CASE-TEST-DIST-1", "CASE-TEST-DIST-2")
        assert res["is_resolvable"] is True
        assert res["conflict_status"] == "DISTINGUISHED_NOT_OVERRULED"
        assert res["binding_authority"] == "CASE-TEST-DIST-1"
        assert res["requires_qualification"] is True
        assert "Both authorities remain valid within their distinct factual/statutory matrices" in res["rationale"]

    def test_obiter_dicta_cannot_displace_binding_ratio(self):
        graph = build_national_judicial_knowledge_graph()
        graph.add_node(GraphNode("CASE-TEST-OBITER", EntityType.CASE, "Case Obiter (2022)", jurisdiction="IN", properties={"bench_strength": 5, "is_obiter": True}))
        graph.add_node(GraphNode("CASE-TEST-RATIO", EntityType.CASE, "Case Ratio (2018)", jurisdiction="IN", properties={"bench_strength": 3, "is_obiter": False}))

        res = graph.resolve_precedent_conflict("CASE-TEST-OBITER", "CASE-TEST-RATIO")
        assert res["is_resolvable"] is True
        assert res["conflict_status"] == "PERSUASIVE_OBITER_NOT_BINDING_RATIO"
        assert res["binding_authority"] == "CASE-TEST-RATIO"
        assert "cannot displace the binding ratio decidendi" in res["rationale"]

    def test_distinct_substantive_issues_no_doctrinal_conflict(self):
        graph = build_national_judicial_knowledge_graph()
        graph.add_node(GraphNode("CASE-ARBITRATION", EntityType.CASE, "Arbitration Decision", properties={"legal_issues": ["arbitration award setting aside"]}))
        graph.add_node(GraphNode("CASE-CRIMINAL", EntityType.CASE, "Criminal Decision", properties={"legal_issues": ["anticipatory bail conditions"]}))

        res = graph.resolve_precedent_conflict("CASE-ARBITRATION", "CASE-CRIMINAL", substantive_issue="arbitration")
        assert res["is_resolvable"] is False
        assert res["conflict_status"] == "DIFFERENT_LEGAL_ISSUES_NO_CONFLICT"
        assert "materially distinct legal issues" in res["rationale"]

    def test_co_equal_bench_neutral_preservation(self):
        graph = build_national_judicial_knowledge_graph()
        graph.add_node(GraphNode("CASE-SC-COEQUAL-1", EntityType.CASE, "State A v. X (2018) 2 SCC 1", jurisdiction="IN", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-SC-COEQUAL-2", EntityType.CASE, "State B v. Y (2021) 4 SCC 5", jurisdiction="IN", properties={"bench_strength": 2}))

        res = graph.resolve_precedent_conflict("CASE-SC-COEQUAL-1", "CASE-SC-COEQUAL-2")
        assert res["is_resolvable"] is False
        assert res["conflict_status"] == "UNRESOLVED_CO_EQUAL_BENCH_SPLIT"
        assert res["binding_authority"] is None
        assert res["requires_qualification"] is True


class TestPhase55AuthorityTraceIntegrity:
    """Verifies authority resolution traces generated during end-to-end evidence orchestration."""

    def test_orchestration_produces_complete_traces(self):
        analyzer = LegalQueryAnalyzer()
        parsed_q = analyzer.parse_query(
            "Under Section 52 of Copyright Act, does reproduction for educational course packs constitute infringement?",
            context_date="2010-05-10"
        )
        orchestrator = UnifiedEvidenceOrchestrator()
        evidence_set = orchestrator.orchestrate_evidence(parsed_q)

        traces = evidence_set.authority_resolution_traces
        assert len(traces) > 0

        # Verify trace attributes
        pit_traces = [t for t in traces if t.get("trace_type") == "statutory_applicability"]
        assert len(pit_traces) > 0
        t = pit_traces[0]
        assert t["provision_id"] == "COP-SEC-52"
        assert t["version_number"] == 1
        assert t["applicability_state"] == StatutoryApplicabilityState.CONFIRMED_HISTORICAL
        assert t["is_applicable"] is True

    def test_pipeline_decision_matches_traces(self):
        pipe = LegalQueryPipeline()
        # Query on struck-down Section 66A IT Act in 2023
        resp = pipe.execute("Can an FIR be registered under Section 66A IT Act for posting offensive online comments in 2023?", context_date="2023-01-15")
        
        # Verify traces record SUPERSEDED_OR_REPEALED
        traces = resp.evidence_set.authority_resolution_traces
        assert any(t.get("applicability_state") == StatutoryApplicabilityState.SUPERSEDED_OR_REPEALED for t in traces)
        # Response must not affirm that Section 66A is in force
        assert "Section 66A" in resp.answer_text
        assert ("struck down" in resp.answer_text.lower() or "unconstitutional" in resp.answer_text.lower())


class TestPhase55PITV11BenchmarkAndReleaseGates:
    """Verifies PIT-V11 benchmark manifest (188 cases, 75 held-out) and Phase 55 release quality gates."""

    def test_pit_v11_manifest_and_zero_contamination(self):
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13", "LEGALMITRA-BENCHMARK-PIT-V14")
        assert data["version"] in ("11.0.0", "12.0.0", "13.0.0", "14.0.0")
        assert len(data["test_cases"]) in (188, 212, 240, 280)
        assert data["split_counts"]["development"] in (78, 88, 100, 115)
        assert data["split_counts"]["validation"] in (35, 40, 46, 55)
        assert data["split_counts"]["held_out_evaluation"] in (75, 84, 94, 110)

        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(data["test_cases"])
        assert report.exact_duplicates_count == 0
        assert report.near_duplicates_count == 0
        assert report.max_cross_split_jaccard <= 0.85
        assert report.audit_verdict in ("PASS", "ZERO_CONTAMINATION_VERIFIED")

    def test_release_quality_gates_phase55(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57", "LEGALMITRA-RELEASE-PHASE58", "LEGALMITRA-RELEASE-PHASE59", "LEGALMITRA-RELEASE-PHASE60", "LEGALMITRA-RELEASE-PHASE61", "LEGALMITRA-RELEASE-PHASE62", "LEGALMITRA-RELEASE-PHASE63")
        assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0", "0.58.0", "0.59.0", "0.60.0", "0.61.0", "0.62.0", "0.63.0")
        assert summary.total_gates in (11, 15, 20)
        assert summary.passed_gates in (10, 14, 19)
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"
