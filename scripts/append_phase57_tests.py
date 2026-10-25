"""
Append 5 additional rigorous tests to tests/test_phase57_independent_evaluation.py.
"""

path = "tests/test_phase57_independent_evaluation.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

additional_tests = '''
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
'''

with open(path, "w", encoding="utf-8") as f:
    f.write(content + additional_tests)

print("Successfully appended 5 tests!")

