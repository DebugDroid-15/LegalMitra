"""
Phase 57 Test Suite: Independent Legal Answer Evaluation, Error Attribution,
4-Dimensional Completeness Auditing, PIT-V13 Benchmark, and Release Quality Gates RG-01 to RG-20.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import pytest

from legalmitra.evaluation.independent_evaluator import (
    IndependentClaimEvaluator,
    IndependentClaimEvaluationReport,
    PropositionVerdict,
    OverstatementSeverity,
)
from legalmitra.evaluation.completeness_auditor import (
    AnswerCompletenessAuditor,
    CompletenessAuditReport,
    CalibrationVerdict,
)
from legalmitra.evaluation.error_attribution import (
    ErrorTaxonomyCategory,
    PipelineStage,
    RootCauseAttributor,
    CATEGORY_STAGE_MAPPING,
)
from legalmitra.evaluation.differential_evaluator import (
    DifferentialEvaluator,
    DifferentialEvaluationReport,
    RegressionSeverity,
)
from legalmitra.evaluation.contamination import ContaminationAuditor
from legalmitra.evaluation.release_gates import (
    ReleaseGateEvaluator,
    GateStatus,
)
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.orchestration.decision_policy import LegalResponseState


class TestPhase57IndependentClaimEvaluation:
    """Tests independent claim-level evaluation separating citations from substantive support."""

    def test_independent_evaluator_substantive_support_separation(self):
        evaluator = IndependentClaimEvaluator()
        # Citation exists (Section 20A SRA), but claim states injunction can be granted to stop highway
        report = evaluator.evaluate_response(
            query="Can a contractor obtain an injunction stopping highway construction under Section 20A SRA?",
            answer_text="Under Section 20A of the Specific Relief Act, 1963, the court will readily grant an injunction to stop highway construction.",
            citations=["Specific Relief Act, 1963 Section 20A"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.total_propositions >= 1
        assert report.has_contradictions is False
        # The proposition directly contradicts the statutory bar of Section 20A
        prop = report.propositions[0]
        assert prop.verdict == PropositionVerdict.CONTRADICTED_BY_SOURCE
        assert prop.citation_valid is True
        assert prop.substantive_support is False
        assert prop.overstatement_severity == OverstatementSeverity.CRITICAL_ABSOLUTE_DISTORTION
        assert report.substantive_support_rate == 0.0

    def test_independent_evaluator_overstatement_detection(self):
        evaluator = IndependentClaimEvaluator()
        # Overstated claim with uncalibrated absolute terms
        report = evaluator.evaluate_response(
            query="Can a daughter claim coparcenary rights under Hindu Succession Act?",
            answer_text="Under Section 6 of the Hindu Succession Act, every daughter unconditionally has an absolute right to coparcenary in all circumstances irrespective of any partition.",
            citations=["Hindu Succession Act, 1956 Section 6"],
            production_response_state="ANSWER_DIRECT",
        )
        assert report.overstated_propositions >= 1
        prop = report.propositions[0]
        assert prop.verdict == PropositionVerdict.OVERSTATED_CLAIM
        assert prop.overstatement_severity in (OverstatementSeverity.MILD_QUALIFICATION_LAPSE, OverstatementSeverity.MODERATE_EXCEPTION_OMISSION)
        assert report.independent_verdict == "ANSWER_QUALIFIED"

    def test_independent_evaluator_omitted_proviso_detection(self):
        evaluator = IndependentClaimEvaluator()
        # Omits pre-2004 registered partition proviso
        report = evaluator.evaluate_response(
            query="Can a daughter claim partition under Hindu Succession Act Section 6?",
            answer_text="Under Section 6 of the Hindu Succession Act, daughters have equal rights in coparcenary property as sons.",
            citations=["Hindu Succession Act, 1956 Section 6"],
            production_response_state="ANSWER_DIRECT",
        )
        assert report.omitted_qualification_count >= 1
        assert any("Section 6(1) Proviso" in p.omitted_provisos[0] for p in report.propositions if p.omitted_provisos)

    def test_independent_evaluator_fabricated_citation_immunity(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Is Section 138 NI Act unconstitutional?",
            answer_text="In 2099 SCC 999 FAKE CITATION, the Supreme Court struck down Section 138 of the NI Act.",
            citations=["2099 SCC 999 FAKE CITATION"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.has_fabricated_citations is True
        assert report.independent_verdict == "ABSTENTION_FABRICATED_OR_QUARANTINED"
        assert report.trustworthiness_score < 0.30

    def test_independent_evaluator_quarantined_scaffold_rejection(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="What are bail principles under Section 438 CrPC?",
            answer_text="Under IND-JUD-DEL-2024-BAIL, anticipatory bail cannot be granted in economic offences.",
            citations=["IND-JUD-DEL-2024-BAIL Section 438"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.has_quarantined_sources is True
        assert report.independent_verdict == "ABSTENTION_FABRICATED_OR_QUARANTINED"
        assert report.trustworthiness_score < 0.20

    def test_independent_evaluator_overruled_precedent_detection(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Does a daughter's father have to be alive in 2005 under Hindu Succession Act?",
            answer_text="The Supreme Court held that Prakash v. Phulavati governs and is binding, requiring father to be alive on 9 September 2005.",
            citations=["Prakash v. Phulavati (2016) 2 SCC 36"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.has_temporal_anachronisms is True
        prop = report.propositions[0]
        assert prop.verdict == PropositionVerdict.TEMPORALLY_SUPERSEDED
        assert prop.temporal_validity is False

    def test_independent_evaluator_intra_answer_contradictions(self):
        evaluator = IndependentClaimEvaluator()
        answer = (
            "Under Section 20A of the Specific Relief Act, an injunction is barred for infrastructure projects. "
            "However, in practical terms, the contractor may seek an interim injunction and an injunction may be granted."
        )
        report = evaluator.evaluate_response(
            query="Can an injunction be granted against highway expansion?",
            answer_text=answer,
            citations=["Specific Relief Act, 1963 Section 20A"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.has_contradictions is True
        assert report.independent_verdict == "ANSWER_CONTRADICTED_INTERNAL"
        assert report.trustworthiness_score <= 0.50

    def test_independent_evaluator_verdict_reconciliation(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can a contractor get an injunction against a national highway project under Section 20A SRA?",
            answer_text="Under Section 20A of the Specific Relief Act, 1963, no injunction shall be granted by any court in a suit under this Act involving an infrastructure project.",
            citations=["Specific Relief Act, 1963 Section 20A"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.production_verdict == "ANSWER_SUPPORTED"
        assert report.independent_verdict == "ANSWER_SUPPORTED"
        assert report.verdict_concordance is True
        assert report.trustworthiness_score >= 0.85


class TestPhase57AnswerCompletenessAuditing:
    """Tests 4-dimensional answer completeness and qualification auditing."""

    def test_completeness_auditor_all_4_dimensions_scored(self):
        auditor = AnswerCompletenessAuditor()
        query = "Can pre-institution mediation be dispensed with under Section 12A Commercial Courts Act when urgent relief is sought?"
        answer = (
            "Under Section 12A of the Commercial Courts Act, 2015, pre-institution mediation is mandatory per Patil Automation. "
            "However, an exception applies where urgent interim relief is contemplated as reaffirmed in Yamini Manohar."
        )
        citations = ["Commercial Courts Act, 2015 Section 12A", "Patil Automation v. Rakheja Engineers (2022) 10 SCC 1"]
        rep = auditor.audit(query=query, answer_text=answer, citations=citations, response_state="ANSWER_QUALIFIED")

        assert rep.factual_and_legal_support.score >= 0.80
        assert rep.material_completeness.score >= 0.75
        assert rep.decision_calibration.score >= 0.85
        assert rep.internal_consistency.score == 1.0
        assert rep.overall_completeness_score >= 0.80
        assert rep.is_audit_passed is True
        assert rep.calibration_verdict == CalibrationVerdict.WELL_CALIBRATED

    def test_completeness_auditor_false_certainty_penalty(self):
        auditor = AnswerCompletenessAuditor()
        query = "Can an injunction be granted for specific performance of a contract on an infrastructure project?"
        # Emits direct answer while omitting the mandatory Section 20A statutory bar
        answer = "Yes, an injunction can unconditionally be granted in all circumstances for breach of contract."
        rep = auditor.audit(query=query, answer_text=answer, citations=[], response_state="ANSWER_DIRECT")

        assert rep.calibration_verdict == CalibrationVerdict.FALSE_CERTAINTY
        assert rep.decision_calibration.score <= 0.50
        assert rep.is_audit_passed is False
        assert len(rep.omitted_statutory_bars) >= 1

    def test_completeness_auditor_false_abstention_penalty(self):
        auditor = AnswerCompletenessAuditor()
        query = "Is pre-institution mediation mandatory under Section 12A of the Commercial Courts Act?"
        answer = "LegalMitra cannot answer this question due to conflicting authorities."
        rep = auditor.audit(query=query, answer_text=answer, citations=[], response_state="ABSTAIN_CONFLICTING_AUTHORITY")

        assert rep.calibration_verdict == CalibrationVerdict.FALSE_ABSTENTION
        assert rep.decision_calibration.score <= 0.50

    def test_completeness_auditor_omitted_statutory_bar(self):
        auditor = AnswerCompletenessAuditor()
        query = "Can a contractor file for specific performance and an injunction on a national highway project?"
        answer = "Specific performance of contract may be granted under Section 10 of the Specific Relief Act."
        rep = auditor.audit(query=query, answer_text=answer, citations=["Specific Relief Act Section 10"], response_state="ANSWER_SUPPORTED")

        assert len(rep.omitted_statutory_bars) >= 1
        assert "Section 20A" in rep.omitted_statutory_bars[0]
        assert rep.material_completeness.passed is False


class TestPhase57ErrorTaxonomyAndAttribution:
    """Tests the 28-category failure taxonomy and deterministic root-cause attribution."""

    def test_error_taxonomy_28_categories_and_7_stages(self):
        assert len(ErrorTaxonomyCategory) == 28
        assert len(PipelineStage) == 7
        assert len(CATEGORY_STAGE_MAPPING) == 28

        stages = {s.value for s in PipelineStage}
        expected_stages = {
            "QUERY_ANALYSIS",
            "RETRIEVAL",
            "TEMPORAL_RESOLUTION",
            "EVIDENCE_MATRIX",
            "CLAIM_VALIDATION",
            "DECISION_POLICY",
            "ANSWER_ASSEMBLY",
        }
        assert stages == expected_stages

    def test_error_attribution_deterministic_root_cause(self):
        attributor = RootCauseAttributor()
        # Query where Section 20A statutory bar is missed
        report = attributor.attribute(
            eval_id="ATTR-TEST-01",
            query="Can a contractor get an injunction against an expressway under Section 20A SRA?",
            answer_text="The court will grant an injunction to halt construction.",
            citations=["Specific Relief Act, 1963 Section 20A"],
            response_state="ANSWER_DIRECT",
        )
        assert report.total_attributions >= 1
        assert report.primary_attribution is not None
        assert report.primary_attribution.error_category == ErrorTaxonomyCategory.MISSED_STATUTORY_EXCEPTION
        assert report.primary_attribution.pipeline_stage == PipelineStage.EVIDENCE_MATRIX
        assert report.primary_attribution.is_established_cause is True
        assert report.primary_attribution.confidence >= 0.90
        assert "ClaimDependencyValidator" in report.primary_attribution.affected_components


class TestPhase57DifferentialEvaluationAndBenchmark:
    """Tests differential evaluation, regression detection, and PIT-V13 benchmark expansion."""

    def test_pit_v13_manifest_structure_and_zero_contamination(self):
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        assert manifest_path.exists()
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V13", "LEGALMITRA-BENCHMARK-PIT-V14")
        assert data["version"] in ("13.0.0", "14.0.0")
        assert len(data["test_cases"]) in (240, 280)
        assert data["total_test_cases"] in (240, 280)
        assert data["split_counts"]["development"] in (100, 115)
        assert data["split_counts"]["validation"] in (46, 55)
        assert data["split_counts"]["held_out_evaluation"] in (94, 110)

        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(data["test_cases"])
        assert report.exact_duplicates_count == 0
        assert report.max_cross_split_jaccard <= 0.85
        assert report.is_split_isolated is True
        assert report.audit_verdict == "PASS"

    def test_pit_v13_held_out_case_invariants(self):
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        held_out = [c for c in data["test_cases"] if c.get("split") == "held_out_evaluation"]
        assert len(held_out) in (94, 110)
        for case in held_out[-5:]:
            assert "case_id" in case
            assert "query_description" in case
            assert "expected_governing_regime" in case
            assert "temporal_validation_status" in case

    def test_differential_evaluator_runs_comparison(self):
        diff_eval = DifferentialEvaluator()
        baseline_cases = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_SUPPORTED"},
            {"case_id": "PIT-002", "passed": False, "verdict": "ABSTAIN_INSUFFICIENT_FACTS"},
            {"case_id": "PIT-003", "passed": True, "verdict": "ANSWER_QUALIFIED"},
        ]
        candidate_cases = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_SUPPORTED"},
            {"case_id": "PIT-002", "passed": True, "verdict": "ANSWER_SUPPORTED"},  # Improved!
            {"case_id": "PIT-003", "passed": True, "verdict": "ANSWER_QUALIFIED"},
        ]
        rep = diff_eval.compare_runs(baseline_cases, candidate_cases, "PIT-V12", "PIT-V13")

        assert rep.total_compared_cases == 3
        assert rep.both_passed_count == 2
        assert rep.improvements_count == 1
        assert rep.regressions_count == 0
        assert rep.critical_safety_regressions == 0
        assert rep.is_regression_free is True
        assert rep.pass_rate_delta > 0.0

    def test_differential_evaluator_critical_safety_regression_detection(self):
        diff_eval = DifferentialEvaluator()
        baseline_cases = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_SUPPORTED"},
        ]
        candidate_cases = [
            {"case_id": "PIT-001", "passed": False, "verdict": "ANSWER_SUPPORTED", "query": "scaffold IND-JUD-DEL-2024-BAIL injected"},
        ]
        rep = diff_eval.compare_runs(baseline_cases, candidate_cases, "PIT-V12", "PIT-V13")

        assert rep.regressions_count == 1
        assert rep.critical_safety_regressions == 1
        assert rep.is_regression_free is False
        assert rep.case_comparisons[0].regression_severity == RegressionSeverity.CRITICAL_SAFETY_REGRESSION

    def test_release_quality_gates_phase57(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57", "LEGALMITRA-RELEASE-PHASE58", "LEGALMITRA-RELEASE-PHASE59", "LEGALMITRA-RELEASE-PHASE60")
        assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0", "0.58.0", "0.59.0", "0.60.0")
        assert summary.total_gates == 20
        assert summary.passed_gates == 19
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1  # RG-11 pending advocate review
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"

        gate_map = {g.gate_id: g for g in summary.gates}
        assert gate_map["RG-16-INDEPENDENT-CLAIM-EVALUATION"].status == GateStatus.PASSED
        assert gate_map["RG-17-ANSWER-COMPLETENESS-4D"].status == GateStatus.PASSED
        assert gate_map["RG-18-ERROR-TAXONOMY-ATTRIBUTION"].status == GateStatus.PASSED
        assert (gate_map.get("RG-19-PIT-V14-BENCHMARK-INTEGRITY") or gate_map.get("RG-19-PIT-V13-BENCHMARK-INTEGRITY")).status == GateStatus.PASSED
        assert gate_map["RG-20-DIFFERENTIAL-REGRESSION-GUARD"].status == GateStatus.PASSED

    def test_end_to_end_orchestrated_response_evaluation(self):
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("A contractor files a suit seeking specific performance of a contract for a national highway expansion and requests an injunction under Section 20A SRA.")

        evaluator = IndependentClaimEvaluator()
        eval_report = evaluator.evaluate_response(
            query=resp.query,
            answer_text=resp.answer_text,
            citations=resp.citations,
            production_response_state=resp.response_state.value,
        )
        assert eval_report.total_propositions >= 1
        assert eval_report.trustworthiness_score >= 0.70
        assert not eval_report.has_fabricated_citations
        assert not eval_report.has_quarantined_sources

        auditor = AnswerCompletenessAuditor()
        audit_report = auditor.audit(
            query=resp.query,
            answer_text=resp.answer_text,
            citations=resp.citations,
            response_state=resp.response_state.value,
            decomposed_issues=resp.parsed_query.decomposed_issues,
        )
        assert audit_report.factual_and_legal_support.passed is True
        assert audit_report.internal_consistency.passed is True
        assert audit_report.calibration_verdict == CalibrationVerdict.WELL_CALIBRATED

class TestPhase57AdditionalEvaluationAndAttribution:
    """Additional edge-case and robustness tests for Phase 57."""

    def test_independent_evaluator_clean_slate_and_promoter_guarantor(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Does an approved resolution plan extinguish promoter personal guarantees under IBC?",
            answer_text="Under Section 31 of the Insolvency and Bankruptcy Code, 2016, the corporate debtor receives a clean slate, but the promoter remains personally liable on their independent personal guarantee.",
            citations=["Insolvency and Bankruptcy Code, 2016 Section 31", "Lalit Kumar Jain v. Union of India (2021) 9 SCC 321"],
            production_response_state="ANSWER_QUALIFIED",
        )
        assert report.total_propositions >= 1
        assert report.substantive_support_rate >= 0.80
        assert report.trustworthiness_score >= 0.80
        assert not report.has_contradictions

    def test_independent_evaluator_uncommenced_statute_warning(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can an employer retrench 50 workers under Industrial Relations Code 2020?",
            answer_text="The Industrial Relations Code, 2020 has been enacted by Parliament, but has not yet been notified for commencement.",
            citations=["Industrial Relations Code, 2020"],
            production_response_state="ANSWER_QUALIFIED",
        )
        assert report.total_propositions >= 1
        assert report.has_temporal_anachronisms is False

    def test_completeness_auditor_conflated_multi_issue(self):
        auditor = AnswerCompletenessAuditor()
        query = "Can an employee claim retrenchment compensation under Section 25F of the Industrial Disputes Act, 1947, and can the employer implement new retrenchment thresholds under the uncommenced Industrial Relations Code, 2020?"
        answer = "Yes, retrenchment compensation is payable under Section 25F and the new thresholds apply."
        rep = auditor.audit(query=query, answer_text=answer, citations=["Industrial Disputes Act, 1947 Section 25F"], response_state="ANSWER_DIRECT")
        assert rep.calibration_verdict == CalibrationVerdict.CONFLATED_MULTI_ISSUE
        assert rep.decision_calibration.score <= 0.60

    def test_error_attribution_stage_mapping_integrity(self):
        from legalmitra.evaluation.error_attribution import ErrorTaxonomyCategory, PipelineStage, CATEGORY_STAGE_MAPPING
        for cat in ErrorTaxonomyCategory:
            assert cat in CATEGORY_STAGE_MAPPING
            stage = CATEGORY_STAGE_MAPPING[cat]
            assert isinstance(stage, PipelineStage)

    def test_differential_evaluator_state_transition_matrix(self):
        diff_eval = DifferentialEvaluator()
        baseline_cases = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_DIRECT"},
            {"case_id": "PIT-002", "passed": True, "verdict": "ANSWER_DIRECT"},
            {"case_id": "PIT-003", "passed": True, "verdict": "ABSTAIN"},
        ]
        candidate_cases = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_QUALIFIED"},  # Calibrated transition
            {"case_id": "PIT-002", "passed": True, "verdict": "ANSWER_DIRECT"},     # Stable
            {"case_id": "PIT-003", "passed": True, "verdict": "ANSWER_SUPPORTED"},  # Resolved abstention
        ]
        rep = diff_eval.compare_runs(baseline_cases, candidate_cases, "PIT-V12", "PIT-V13")
        assert rep.state_transitions["ANSWER_DIRECT -> ANSWER_QUALIFIED"] == 1
        assert rep.state_transitions["ANSWER_DIRECT -> ANSWER_DIRECT"] == 1
        assert rep.state_transitions["ABSTAIN -> ANSWER_SUPPORTED"] == 1
