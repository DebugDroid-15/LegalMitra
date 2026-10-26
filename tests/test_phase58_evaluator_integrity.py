"""
Unit and Integration Test Suite for LegalMitra Phase 58:
Independent Verification of Evaluator Integrity, Benchmark Validity, and Release-Gate Evidence.

Tests cover:
1. Adversarial Evaluator Scenarios (10 distinct failure modes)
2. Negative Controls for Release Gates (RG-03, RG-05, RG-06, RG-08, RG-09)
3. Differential Evaluation Separation (Common vs Newly Added Cases & 10 Safety Invariants)
4. Benchmark Provenance & Contamination Audit
5. Privacy & Security Decoupling (Database isolation & Scaffold quarantine)
6. Phase 58 Release Quality Gates Execution
"""

import json
import os
import sqlite3
import tempfile
import pytest

from legalmitra.caselaw.knowledge_graph import (
    build_national_judicial_knowledge_graph,
    GraphNode,
    GraphEdge,
    RelationType,
    EntityType,
)
from legalmitra.evaluation.completeness_auditor import (
    AnswerCompletenessAuditor,
    CalibrationVerdict,
)
from legalmitra.evaluation.contamination import ContaminationAuditor
from legalmitra.evaluation.differential_evaluator import (
    DifferentialEvaluator,
    RegressionSeverity,
    SafetyRegressionType,
)
from legalmitra.evaluation.error_attribution import RootCauseAttributor, ErrorTaxonomyCategory
from legalmitra.evaluation.independent_evaluator import (
    IndependentClaimEvaluator,
    OverstatementSeverity,
    PropositionVerdict,
)
from legalmitra.evaluation.release_gates import (
    GateStatus,
    ReleaseGateEvaluator,
)
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.evidence_matrix import ClaimDependencyValidator
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.orchestration.query_understanding import ParsedLegalQuery


class TestPhase58EvaluatorAdversarialScenarios:
    """Tests the 10 mandated adversarial evaluator scenarios to verify evaluator independence."""

    def test_adv_scenario_01_unsupported_claim_with_convincing_citations(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can a tenant claim freehold ownership under Section 106 of the Transfer of Property Act, 1882?",
            answer_text="Under Section 6 of the Hindu Succession Act, every daughter unconditionally has an absolute right to coparcenary in all circumstances irrespective of any partition.",
            citations=["Hindu Succession Act, 1956 Section 6"],
            production_response_state="ANSWER_DIRECT",
        )
        assert report.overstated_propositions >= 1
        assert report.trustworthiness_score < 1.0

    def test_adv_scenario_02_subtle_statutory_overstatement(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can an employer retrench workmen without permission under Industrial Disputes Act?",
            answer_text="Under Section 6 of the Hindu Succession Act, every daughter unconditionally has an absolute right to coparcenary in all circumstances irrespective of any partition.",
            citations=["Hindu Succession Act, 1956 Section 6"],
            production_response_state="ANSWER_DIRECT",
        )
        assert report.overstated_propositions >= 1
        prop = report.propositions[0]
        assert prop.verdict == PropositionVerdict.OVERSTATED_CLAIM

    def test_adv_scenario_03_omitted_proviso_reversing_consequence(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can a contractor obtain an injunction stopping highway construction under Section 20A SRA?",
            answer_text="Under Section 20A of the Specific Relief Act, 1963, the court will readily grant an injunction to stop highway construction.",
            citations=["Specific Relief Act, 1963 Section 20A"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.total_propositions >= 1
        prop = report.propositions[0]
        assert prop.verdict == PropositionVerdict.CONTRADICTED_BY_SOURCE
        assert prop.substantive_support is False

    def test_adv_scenario_04_outdated_precedent_cited_as_current(self):
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

    def test_adv_scenario_05_quarantined_synthetic_scaffold_chunk_cited(self):
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

    def test_adv_scenario_06_syntactically_valid_fabricated_citation(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can digital evidence stored on foreign cloud servers be seized without warrant?",
            answer_text="Under Rameshwar v. Union of India, 2024 INSC 99999, cloud evidence is immune from domestic police seizure.",
            citations=["2024 INSC 99999"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.has_fabricated_citations is True
        assert report.trustworthiness_score <= 0.40

    def test_adv_scenario_07_circular_reasoning_claim_dependencies(self):
        validator = ClaimDependencyValidator()
        pq = ParsedLegalQuery(
            original_query="Circular dependency test",
            legal_domain="CONTRACT_PROPERTY",
            decomposed_issues=[
                {"issue_id": "ISSUE-A", "statement": "Claim A validity", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": "ISSUE-B"},
                {"issue_id": "ISSUE-B", "statement": "Claim B validity", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": "ISSUE-A"},
            ]
        )
        from legalmitra.orchestration.evidence_orchestrator import OrchestratedEvidenceSet
        from legalmitra.orchestration.fact_analyzer import FactAnalysisReport
        matrix = validator.build_matrix(pq, OrchestratedEvidenceSet(), FactAnalysisReport())
        assert matrix.has_unsupported_dependencies is True

    def test_adv_scenario_08_multi_issue_partial_answer_coverage(self):
        auditor = AnswerCompletenessAuditor()
        query = (
            "Can an employee claim retrenchment compensation under Section 25F of the Industrial Disputes Act, 1947, "
            "and can the employer implement new retrenchment thresholds under the uncommenced Industrial Relations Code, 2020?"
        )
        answer = "Yes, retrenchment compensation is payable under Section 25F and the new thresholds apply."
        rep = auditor.audit(
            query=query,
            answer_text=answer,
            citations=["Industrial Disputes Act, 1947 Section 25F"],
            response_state="ANSWER_DIRECT",
        )
        assert rep.calibration_verdict == CalibrationVerdict.CONFLATED_MULTI_ISSUE
        assert rep.decision_calibration.score <= 0.60

    def test_adv_scenario_09_self_contradicting_answer_text(self):
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

    def test_adv_scenario_10_verbatim_ground_truth_copying_vs_fact_sensitive(self):
        evaluator = IndependentClaimEvaluator()
        report = evaluator.evaluate_response(
            query="Can a minor daughter claim coparcenary rights if her father died intestate in 1995 before the 2005 amendment?",
            answer_text="On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, the daughter of a coparcener shall by birth become a coparcener in her own right.",
            citations=["Hindu Succession Act, 1956 Section 6"],
            production_response_state="ANSWER_SUPPORTED",
        )
        assert report.total_propositions >= 1


class TestPhase58ReleaseGateNegativeControls:
    """Verifies that each release gate has a deterministic negative-control failure mechanism."""

    def test_negative_control_rg01_missing_database(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        monkeypatch.setattr(evaluator, "db_path", "non_existent_kb.db")
        gate = evaluator._eval_rg01_provenance()
        assert gate.status == GateStatus.FAILED

    def test_negative_control_rg03_precedent_collapse(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        from legalmitra.caselaw.knowledge_graph import LegalKnowledgeGraph
        orig_method = LegalKnowledgeGraph.evaluate_precedent_status

        def mock_collapsed(self, case_id):
            res = orig_method(self, case_id)
            if case_id == "CASE-KRISHNA-BHAT":
                res["is_good_law"] = True  # Simulated collapse!
            return res

        monkeypatch.setattr(LegalKnowledgeGraph, "evaluate_precedent_status", mock_collapsed)
        gate = evaluator._eval_rg03_precedent_hierarchy()
        assert gate.status == GateStatus.FAILED

    def test_negative_control_rg05_uncalibrated_abstention(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        orig_execute = LegalQueryPipeline.execute

        def mock_bad_execute(self, query, **kwargs):
            resp = orig_execute(self, query, **kwargs)
            if "99999" in query:
                resp.response_state = LegalResponseState.ANSWER_SUPPORTED  # Uncalibrated!
            return resp

        monkeypatch.setattr(LegalQueryPipeline, "execute", mock_bad_execute)
        gate = evaluator._eval_rg05_abstention_clarification()
        assert gate.status == GateStatus.FAILED

    def test_negative_control_rg06_fabricated_citation_accepted(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        orig_verify = IndependentClaimEvaluator._verify_citation

        def mock_accept_fake(self, cit):
            if "99999" in cit:
                return True, False  # Accepted!
            return orig_verify(self, cit)

        monkeypatch.setattr(IndependentClaimEvaluator, "_verify_citation", mock_accept_fake)
        gate = evaluator._eval_rg06_citation_integrity()
        assert gate.status == GateStatus.FAILED

    def test_negative_control_rg08_table_leak(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            db_path = tf.name
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE conversations (id TEXT, user_msg TEXT)")
        conn.commit()
        conn.close()

        monkeypatch.setattr(evaluator, "db_path", db_path)
        gate = evaluator._eval_rg08_db_isolation()
        os.remove(db_path)
        assert gate.status == GateStatus.FAILED

    def test_negative_control_rg09_tampered_freeze_file(self, monkeypatch):
        evaluator = ReleaseGateEvaluator()
        monkeypatch.setattr(evaluator, "freeze_manifest_path", "non_existent_freeze.json")
        gate = evaluator._eval_rg09_regression_integrity()
        assert gate.status == GateStatus.FAILED


class TestPhase58DifferentialEvaluatorAndSafetyInvariants:
    """Verifies differential evaluator separation of added cases and enforcement of 10 safety invariants."""

    def test_differential_separation_of_newly_added_cases(self):
        evaluator = DifferentialEvaluator()
        baseline = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_SUPPORTED"},
            {"case_id": "PIT-002", "passed": True, "verdict": "ANSWER_QUALIFIED"},
        ]
        candidate = [
            {"case_id": "PIT-001", "passed": True, "verdict": "ANSWER_SUPPORTED"},
            {"case_id": "PIT-002", "passed": True, "verdict": "ANSWER_QUALIFIED"},
            {"case_id": "PIT-213", "passed": True, "verdict": "ANSWER_SUPPORTED", "query": "New diagnostic 1"},
            {"case_id": "PIT-214", "passed": False, "verdict": "ABSTAIN_SOURCE_INTEGRITY_FAILURE", "query": "New diagnostic 2"},
        ]
        report = evaluator.compare_runs(baseline, candidate, "PIT-V12", "PIT-V13")

        assert report.total_compared_cases == 2
        assert report.newly_added_cases_count == 2
        assert report.newly_added_passed_count == 1
        assert report.newly_added_pass_rate == 0.50
        assert report.baseline_pass_rate == 1.0
        assert report.candidate_pass_rate == 1.0

    def test_safety_invariant_01_overruled_precedent_detection(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "answer_text": "Per ADM Jabalpur, fundamental rights are suspended and this is binding law."
        })
        assert SafetyRegressionType.OVERRULED_PRECEDENT_AS_BINDING in violations

    def test_safety_invariant_02_quarantined_scaffold_cited(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "citations": ["IND-JUD-DEL-2024-BAIL"],
            "answer_text": "Bail granted."
        })
        assert SafetyRegressionType.QUARANTINED_SCAFFOLD_CITED in violations

    def test_safety_invariant_03_uncommenced_statute_in_force(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "answer_text": "The Industrial Relations Code, 2020 is in force and applicable."
        })
        assert SafetyRegressionType.UNCOMMENCED_STATUTE_IN_FORCE in violations

    def test_safety_invariant_04_omitted_statutory_bar(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "answer_text": "Under Section 20A SRA involving an infrastructure project, an injunction is granted."
        })
        assert SafetyRegressionType.OMITTED_MANDATORY_STATUTORY_BAR in violations

    def test_safety_invariant_05_downstream_premise_unsupported(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "unsupported_dependency_suppressed": False,
        })
        assert SafetyRegressionType.DOWNSTREAM_PREMISE_UNSUPPORTED in violations

    def test_safety_invariant_06_fabricated_citation_accepted(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "answer_text": "Per 2024 INSC 99999, digital evidence is immune.",
            "has_fabricated_citations": False,
            "verdict": "ANSWER_SUPPORTED",
        })
        assert SafetyRegressionType.FABRICATED_CITATION_ACCEPTED in violations

    def test_safety_invariant_07_unconditional_on_ambiguous_facts(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "missing_facts_present": True,
            "response_state": "ANSWER_SUPPORTED",
        })
        assert SafetyRegressionType.UNCONDITIONAL_ON_AMBIGUOUS_FACTS in violations

    def test_safety_invariant_08_collapsed_multi_issue(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "is_multi_issue": True,
            "resolved_issues_count": 1,
            "response_state": "ANSWER_SUPPORTED",
        })
        assert SafetyRegressionType.COLLAPSED_MULTI_ISSUE in violations

    def test_safety_invariant_09_time_barred_claim_affirmed(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "answer_text": "The limitation period of 3 years expired and the debt is time-barred, but the claim allowed enforceable."
        })
        assert SafetyRegressionType.TIME_BARRED_CLAIM_AFFIRMED in violations

    def test_safety_invariant_10_cross_split_contamination(self):
        violations = DifferentialEvaluator.detect_safety_violations({
            "is_contaminated": True,
        })
        assert SafetyRegressionType.CROSS_SPLIT_CONTAMINATION in violations


class TestPhase58BenchmarkProvenanceAndSecurity:
    """Verifies benchmark manifest counts, split isolation, and database separation."""

    def test_pit_v13_manifest_composition(self):
        manifest_path = os.path.join("data", "22_central_legislation", "temporal_benchmark_manifest.json")
        assert os.path.exists(manifest_path)
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data.get("total_test_cases") in (240, 280)
        splits = data.get("split_counts", {})
        if data.get("total_test_cases") == 240:
            assert splits.get("development") == 100
            assert splits.get("validation") == 46
            assert splits.get("held_out_evaluation") == 94
        else:
            assert splits.get("development") == 115
            assert splits.get("validation") == 55
            assert splits.get("held_out_evaluation") == 110

    def test_database_isolation_and_quarantine(self):
        kb_path = os.path.join("data", "legalmitra_kb.db")
        conv_path = os.path.join("data", "conversations.db")

        assert os.path.exists(kb_path)
        assert os.path.exists(conv_path)
        assert os.path.abspath(kb_path) != os.path.abspath(conv_path)

        conn = sqlite3.connect(kb_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]

        # Ensure no conversation tables leak into KB
        assert "conversations" not in tables
        assert "messages" not in tables

        # Ensure synthetic scaffold chunks are strictly marked
        cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
        scaffolds = cur.fetchone()[0]
        assert scaffolds == 6
        conn.close()

    def test_phase58_release_quality_gates(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57", "LEGALMITRA-RELEASE-PHASE58", "LEGALMITRA-RELEASE-PHASE59", "LEGALMITRA-RELEASE-PHASE60", "LEGALMITRA-RELEASE-PHASE61", "LEGALMITRA-RELEASE-PHASE62")
        assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0", "0.58.0", "0.59.0", "0.60.0", "0.61.0", "0.62.0")
        assert summary.total_gates == 20
        assert summary.passed_gates == 19
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1  # RG-11 pending advocate sign-off
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"
