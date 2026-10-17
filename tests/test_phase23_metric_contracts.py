"""
- Phase 23 Metric Contract & Evaluation Validity Tests.
Exact-value mathematical contracts for:
- Mean Reciprocal Rank (MRR)
- Retrieval Recall @ K
- Citation Support Rate and Hallucination Rate
- Abstention Precision, Recall, and F1
- Temporal Correctness and Anachronism Penalty
- Adversarial Robustness and Privacy Compliance
"""

import pytest
from legalmitra.evaluation.metrics import (
    calculate_abstention_metrics,
    calculate_adversarial_metrics,
    calculate_citation_metrics,
    calculate_mrr,
    calculate_retrieval_recall,
    calculate_temporal_metrics,
    compute_category_statistics,
)
from legalmitra.evaluation.models import (
    CaseEvaluationResult,
    CitationAudit,
    TemporalAudit,
    AdversarialAudit,
    EvaluationCategory,
    SeverityLevel,
)


class TestMRRContracts:
    """Exact-value contracts for Mean Reciprocal Rank."""

    def test_mrr_empty_input(self):
        assert calculate_mrr([]) == 0.0

    def test_mrr_all_top_hits(self):
        # All rank 1: (1/1 + 1/1 + 1/1) / 3 = 1.0
        assert calculate_mrr([1, 1, 1]) == 1.0

    def test_mrr_all_misses(self):
        # All rank 0: 0.0 / 3 = 0.0
        assert calculate_mrr([0, 0, 0]) == 0.0

    def test_mrr_mixed_rankings(self):
        # Rankings: [1, 2, 0, 4]
        # Sum = 1/1 + 1/2 + 0 + 1/4 = 1.0 + 0.5 + 0.25 = 1.75
        # MRR = 1.75 / 4 = 0.4375
        assert calculate_mrr([1, 2, 0, 4]) == 0.4375

    def test_mrr_single_item(self):
        assert calculate_mrr([1]) == 1.0
        assert calculate_mrr([2]) == 0.5
        assert calculate_mrr([0]) == 0.0


class TestRecallContracts:
    """Exact-value contracts for Retrieval Recall @ K."""

    def test_recall_zero_denominator(self):
        assert calculate_retrieval_recall(0, 0) == 0.0
        assert calculate_retrieval_recall(0, 5) == 0.0

    def test_recall_perfect_score(self):
        assert calculate_retrieval_recall(10, 10) == 1.0

    def test_recall_fractional(self):
        # 14 out of 18 = 0.777777... -> 0.7778
        assert calculate_retrieval_recall(18, 14) == 0.7778
        # 3 out of 4 = 0.75
        assert calculate_retrieval_recall(4, 3) == 0.75


class TestCitationMetricsContracts:
    """Exact-value contracts for Citation Support Rate and Hallucination Rate."""

    def test_empty_citations(self):
        sup_rate, hal_rate, sup, unsup = calculate_citation_metrics([], ["Some evidence"])
        assert sup_rate == 1.0
        assert hal_rate == 0.0
        assert sup == []
        assert unsup == []

    def test_all_supported_citations(self):
        citations = [
            "Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023",
            "Article 21 of Constitution of India",
        ]
        evidence = [
            "Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023 deals with bail.",
            "Article 21 of Constitution of India provides protection of life and personal liberty.",
        ]
        sup_rate, hal_rate, sup, unsup = calculate_citation_metrics(citations, evidence)
        assert sup_rate == 1.0
        assert hal_rate == 0.0
        assert len(sup) == 2
        assert len(unsup) == 0

    def test_half_supported_half_hallucinated(self):
        citations = [
            "Section 482 of BNSS",
            "Fictitious Space Piracy Act, Section 99",
        ]
        evidence = ["Section 482 of BNSS provides anticipatory bail directions."]
        sup_rate, hal_rate, sup, unsup = calculate_citation_metrics(citations, evidence)
        assert sup_rate == 0.5
        assert hal_rate == 0.5
        assert sup == ["Section 482 of BNSS"]
        assert unsup == ["Fictitious Space Piracy Act, Section 99"]

    def test_token_fallback_matching(self):
        citations = ["Negotiable Instruments Act, Section 138"]
        evidence = ["According to section 138 of negotiable instruments, notice is required."]
        sup_rate, hal_rate, sup, unsup = calculate_citation_metrics(citations, evidence)
        assert sup_rate == 1.0
        assert hal_rate == 0.0
        assert len(sup) == 1


class TestAbstentionContracts:
    """Exact-value contracts for Abstention Precision, Recall, and F1."""

    def test_perfect_abstention(self):
        y_true = [True, True, False, False]
        y_pred = [True, True, False, False]
        metrics = calculate_abstention_metrics(y_true, y_pred)
        assert metrics["abstention_precision"] == 1.0
        assert metrics["abstention_recall"] == 1.0
        assert metrics["abstention_f1"] == 1.0
        assert metrics["abstention_accuracy"] == 1.0
        assert metrics["true_positives"] == 2.0
        assert metrics["false_positives"] == 0.0

    def test_over_abstention(self):
        # Model abstains on everything (including when it should answer)
        y_true = [True, False, False, False]
        y_pred = [True, True, True, True]
        metrics = calculate_abstention_metrics(y_true, y_pred)
        # Precision = TP / (TP + FP) = 1 / (1 + 3) = 0.25
        assert metrics["abstention_precision"] == 0.25
        # Recall = TP / (TP + FN) = 1 / (1 + 0) = 1.0
        assert metrics["abstention_recall"] == 1.0
        # F1 = 2 * 0.25 * 1.0 / (0.25 + 1.0) = 0.5 / 1.25 = 0.4
        assert metrics["abstention_f1"] == 0.4
        assert metrics["abstention_accuracy"] == 0.25

    def test_under_abstention(self):
        # Model never abstains (answers everything)
        y_true = [True, True, False, False]
        y_pred = [False, False, False, False]
        metrics = calculate_abstention_metrics(y_true, y_pred)
        assert metrics["abstention_precision"] == 0.0
        assert metrics["abstention_recall"] == 0.0
        assert metrics["abstention_f1"] == 0.0
        assert metrics["abstention_accuracy"] == 0.5

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            calculate_abstention_metrics([True], [True, False])


class TestTemporalAndAdversarialContracts:
    """Exact-value contracts for temporal regime identification and adversarial refusal."""

    def test_temporal_metrics(self):
        # 4 queries: 3 correct, 1 anachronism
        correct = [True, True, True, False]
        anachronistic = [False, False, False, True]
        metrics = calculate_temporal_metrics(correct, anachronistic)
        assert metrics["temporal_correctness_rate"] == 0.75
        assert metrics["anachronism_penalty_rate"] == 0.25

    def test_adversarial_metrics(self):
        # Injections: 2 tested, 0 overrides detected -> 100% refusal
        injections = [False, False]
        # Privacy: 2 tested, 0 violations -> 100% compliance
        privacy = [False, False]
        metrics = calculate_adversarial_metrics(injections, privacy)
        assert metrics["injection_refusal_rate"] == 1.0
        assert metrics["privacy_compliance_rate"] == 1.0

        # One injection override leaked
        bad_injections = [True, False]
        metrics_bad = calculate_adversarial_metrics(bad_injections, privacy)
        assert metrics_bad["injection_refusal_rate"] == 0.5
