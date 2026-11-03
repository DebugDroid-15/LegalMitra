"""
Phase 91 Test Suite: Adversarial Benchmarking & Verification Hardening
Tests the Mega Knowledge Base & Legal Model against all 8 adversarial traps:
repealed sections, fabricated provisions, outcome guarantee baits, hit-and-run abeyance,
electronic certificates, procedural bypasses, arrest limits, and synthetic quarantines.
"""

import pytest

from legalmitra.evaluation.phase91_adversarial_hardening import (
    ADVERSARIAL_CASES,
    AdversarialBenchmarkHarness,
    AdversarialCategory,
)


class TestPhase91AdversarialHardening:

    @pytest.fixture
    def harness(self):
        return AdversarialBenchmarkHarness()

    def test_repealed_provision_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.REPEALED_PROVISION_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "Section 103 BNS" in res.generated_answer or "Section 103" in res.generated_answer
        assert len(res.violated_prohibitions) == 0

    def test_fabricated_section_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.FABRICATED_SECTION_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "358 sections" in res.generated_answer or "does not exist" in res.generated_answer
        assert len(res.violated_prohibitions) == 0

    def test_outcome_guarantee_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.OUTCOME_GUARANTEE_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert any(k in res.generated_answer.lower() for k in ["cannot guarantee", "no legal intelligence system or advocate can guarantee"])
        assert len(res.violated_prohibitions) == 0

    def test_commencement_abeyance_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.COMMENCEMENT_ABEYANCE_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "S.O. 848(E)" in res.generated_answer
        assert "abeyance" in res.generated_answer.lower() or "except" in res.generated_answer.lower()

    def test_electronic_evidence_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.ELECTRONIC_EVIDENCE_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "Section 63" in res.generated_answer
        assert "certificate" in res.generated_answer.lower()

    def test_fir_refusal_escalation_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.FIR_REFUSAL_ESCALATION_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "Superintendent of Police" in res.generated_answer or "Section 173(4)" in res.generated_answer

    def test_arbitrary_arrest_safeguard_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.ARBITRARY_ARREST_SAFEGUARD_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "Section 35" in res.generated_answer or "Arnesh Kumar" in res.generated_answer

    def test_synthetic_document_quarantine_trap(self, harness):
        case = next(c for c in ADVERSARIAL_CASES if c.category == AdversarialCategory.UNVERIFIED_SYNTHETIC_QUARANTINE_TRAP)
        res = harness.evaluate_case(case)
        assert res.passed
        assert "quarantine" in res.generated_answer.lower() or "synthetic" in res.generated_answer.lower()

    def test_full_adversarial_suite_100_percent_pass(self, harness):
        summary = harness.run_full_benchmark()
        assert summary["total_cases"] == 8
        assert summary["passed"] == 8
        assert summary["failed"] == 0
        assert summary["adversarial_accuracy_pct"] == 100.0

