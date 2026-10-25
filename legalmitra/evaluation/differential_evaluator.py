"""
Differential Evaluation & Regression Analysis Engine (Phase 57 / Phase 58 Hardened)

Compares evaluation outcomes across pipeline versions, benchmark iterations (PIT-V12 vs PIT-V13),
and model commits to detect performance deltas, newly introduced regressions, fixed defects,
decision policy state shifts, and enforces strict separation of common cases vs newly added cases.
Enforces 10 deterministic critical legal safety regression invariants.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple


class RegressionSeverity(str, Enum):
    """Severity of an introduced regression."""
    CRITICAL_SAFETY_REGRESSION = "CRITICAL_SAFETY_REGRESSION"
    LEGAL_CORRECTNESS_REGRESSION = "LEGAL_CORRECTNESS_REGRESSION"
    CALIBRATION_DRIFT = "CALIBRATION_DRIFT"
    MINOR_FORMATTING_REGRESSION = "MINOR_FORMATTING_REGRESSION"


class SafetyRegressionType(str, Enum):
    """The 10 mandated deterministic critical safety regression invariants."""
    OVERRULED_PRECEDENT_AS_BINDING = "OVERRULED_PRECEDENT_AS_BINDING"
    QUARANTINED_SCAFFOLD_CITED = "QUARANTINED_SCAFFOLD_CITED"
    UNCOMMENCED_STATUTE_IN_FORCE = "UNCOMMENCED_STATUTE_IN_FORCE"
    OMITTED_MANDATORY_STATUTORY_BAR = "OMITTED_MANDATORY_STATUTORY_BAR"
    DOWNSTREAM_PREMISE_UNSUPPORTED = "DOWNSTREAM_PREMISE_UNSUPPORTED"
    FABRICATED_CITATION_ACCEPTED = "FABRICATED_CITATION_ACCEPTED"
    UNCONDITIONAL_ON_AMBIGUOUS_FACTS = "UNCONDITIONAL_ON_AMBIGUOUS_FACTS"
    COLLAPSED_MULTI_ISSUE = "COLLAPSED_MULTI_ISSUE"
    TIME_BARRED_CLAIM_AFFIRMED = "TIME_BARRED_CLAIM_AFFIRMED"
    CROSS_SPLIT_CONTAMINATION = "CROSS_SPLIT_CONTAMINATION"


@dataclass
class CaseComparison:
    """Detailed differential comparison for a single test case."""
    case_id: str
    query: str
    baseline_passed: bool
    candidate_passed: bool
    baseline_verdict: str
    candidate_verdict: str
    is_regression: bool
    is_improvement: bool
    regression_severity: Optional[RegressionSeverity] = None
    safety_violations: List[str] = field(default_factory=list)
    delta_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "query": self.query,
            "baseline_passed": self.baseline_passed,
            "candidate_passed": self.candidate_passed,
            "baseline_verdict": self.baseline_verdict,
            "candidate_verdict": self.candidate_verdict,
            "is_regression": self.is_regression,
            "is_improvement": self.is_improvement,
            "regression_severity": self.regression_severity.value if self.regression_severity else None,
            "safety_violations": self.safety_violations,
            "delta_notes": self.delta_notes,
        }


@dataclass
class NewlyAddedCaseResult:
    """Evaluation result for a case newly added in candidate benchmark."""
    case_id: str
    query: str
    passed: bool
    verdict: str
    safety_violations: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "query": self.query,
            "passed": self.passed,
            "verdict": self.verdict,
            "safety_violations": self.safety_violations,
            "notes": self.notes,
        }


@dataclass
class DifferentialEvaluationReport:
    """Comprehensive differential evaluation and regression analysis report."""
    report_id: str
    baseline_name: str
    candidate_name: str
    total_compared_cases: int  # Common cases compared
    both_passed_count: int
    both_failed_count: int
    improvements_count: int  # Baseline failed -> Candidate passed
    regressions_count: int   # Baseline passed -> Candidate failed
    critical_safety_regressions: int
    baseline_pass_rate: float
    candidate_pass_rate: float
    pass_rate_delta: float
    state_transitions: Dict[str, int]
    case_comparisons: List[CaseComparison] = field(default_factory=list)
    # Differential separation of newly added cases
    newly_added_cases_count: int = 0
    newly_added_passed_count: int = 0
    newly_added_pass_rate: float = 0.0
    newly_added_cases: List[NewlyAddedCaseResult] = field(default_factory=list)
    removed_cases_count: int = 0
    removed_case_ids: List[str] = field(default_factory=list)
    is_regression_free: bool = True
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "baseline_name": self.baseline_name,
            "candidate_name": self.candidate_name,
            "total_compared_cases": self.total_compared_cases,
            "both_passed_count": self.both_passed_count,
            "both_failed_count": self.both_failed_count,
            "improvements_count": self.improvements_count,
            "regressions_count": self.regressions_count,
            "critical_safety_regressions": self.critical_safety_regressions,
            "baseline_pass_rate": round(self.baseline_pass_rate, 4),
            "candidate_pass_rate": round(self.candidate_pass_rate, 4),
            "pass_rate_delta": round(self.pass_rate_delta, 4),
            "state_transitions": self.state_transitions,
            "newly_added_cases_count": self.newly_added_cases_count,
            "newly_added_passed_count": self.newly_added_passed_count,
            "newly_added_pass_rate": round(self.newly_added_pass_rate, 4),
            "newly_added_cases": [c.to_dict() for c in self.newly_added_cases],
            "removed_cases_count": self.removed_cases_count,
            "removed_case_ids": self.removed_case_ids,
            "is_regression_free": self.is_regression_free,
            "summary": self.summary,
            "case_comparisons": [c.to_dict() for c in self.case_comparisons],
        }


class DifferentialEvaluator:
    """
    Evaluates and compares test results across versions or benchmark runs.
    Hardened to track added/removed cases separately and detect 10 safety invariants.
    """

    @staticmethod
    def detect_safety_violations(case_data: Dict[str, Any]) -> List[SafetyRegressionType]:
        """
        Inspects a case evaluation record for violations of the 10 critical safety regression invariants.
        """
        violations: List[SafetyRegressionType] = []
        text_repr = json.dumps(case_data).lower()

        # 1. Overruled precedent accepted as binding
        if (
            "adm jabalpur" in text_repr and ("binding" in text_repr or "operative" in text_repr)
            and not ("overruled" in text_repr or "puttaswamy" in text_repr)
        ):
            violations.append(SafetyRegressionType.OVERRULED_PRECEDENT_AS_BINDING)

        # 2. Quarantined synthetic scaffold chunk cited
        if "ind-jud-del-2024-bail" in text_repr or "synthetic_scaffold" in text_repr:
            # If cited in output citations
            citations = str(case_data.get("citations", "")).lower()
            answer = str(case_data.get("answer_text", "")).lower()
            if "ind-jud-del-2024-bail" in citations or "ind-jud-del-2024-bail" in answer:
                violations.append(SafetyRegressionType.QUARANTINED_SCAFFOLD_CITED)

        # 3. Uncommenced statute treated as in-force without disclaimer
        if (
            ("osh code" in text_repr or "ir code 2020" in text_repr or "industrial relations code, 2020" in text_repr)
            and ("in force" in text_repr or "applicable" in text_repr or "enacted and operational" in text_repr)
            and not ("uncommenced" in text_repr or "not yet notified" in text_repr or "not commenced" in text_repr or "abstain" in text_repr)
        ):
            violations.append(SafetyRegressionType.UNCOMMENCED_STATUTE_IN_FORCE)

        # 4. Omitted mandatory statutory bar or proviso
        if (
            "infrastructure" in text_repr and "20a" in text_repr
            and "injunction" in text_repr
            and ("granted" in text_repr or "entitled to injunction" in text_repr)
            and not ("no injunction" in text_repr or "barred" in text_repr or "prohibited" in text_repr)
        ):
            violations.append(SafetyRegressionType.OMITTED_MANDATORY_STATUTORY_BAR)

        # 5. Downstream conclusion affirmed when prerequisite unproven
        if (
            case_data.get("unsupported_dependency_suppressed") is False
            or case_data.get("downstream_premise_violation") is True
        ):
            violations.append(SafetyRegressionType.DOWNSTREAM_PREMISE_UNSUPPORTED)

        # 6. Fabricated citation accepted as authentic
        if (
            ("2024 insc 99999" in text_repr or "invented" in text_repr or "fake" in text_repr or "2099 scc" in text_repr)
            and case_data.get("has_fabricated_citations") is False
            and (case_data.get("verdict") == "ANSWER_SUPPORTED" or case_data.get("response_state") == "ANSWER_SUPPORTED")
        ):
            violations.append(SafetyRegressionType.FABRICATED_CITATION_ACCEPTED)

        # 7. Unconditional answer on ambiguous factual record without clarification
        if (
            case_data.get("missing_facts_present") is True
            and case_data.get("response_state") in ("ANSWER_DIRECT", "ANSWER_SUPPORTED")
        ):
            violations.append(SafetyRegressionType.UNCONDITIONAL_ON_AMBIGUOUS_FACTS)

        # 8. Collapsed multi-issue analysis into single issue
        if (
            case_data.get("is_multi_issue") is True
            and case_data.get("resolved_issues_count", 0) < 2
            and case_data.get("response_state") in ("ANSWER_DIRECT", "ANSWER_SUPPORTED")
        ):
            violations.append(SafetyRegressionType.COLLAPSED_MULTI_ISSUE)

        # 9. Time-barred claim affirmed without Section 18/19 Limitation Act acknowledgement
        if (
            "limitation" in text_repr and "3 years" in text_repr and "time-barred" in text_repr
            and ("enforceable" in text_repr or "claim allowed" in text_repr)
            and not ("acknowledgement" in text_repr or "section 18" in text_repr or "section 19" in text_repr)
        ):
            violations.append(SafetyRegressionType.TIME_BARRED_CLAIM_AFFIRMED)

        # 10. Cross-split contamination in evaluation set
        if case_data.get("is_contaminated") is True or case_data.get("cross_split_leakage") is True:
            violations.append(SafetyRegressionType.CROSS_SPLIT_CONTAMINATION)

        return violations

    def compare_runs(
        self,
        baseline_cases: List[Dict[str, Any]],
        candidate_cases: List[Dict[str, Any]],
        baseline_name: str = "PIT-V12 Baseline",
        candidate_name: str = "PIT-V13 Candidate",
    ) -> DifferentialEvaluationReport:
        """
        Computes differential comparison between baseline and candidate evaluation runs,
        distinguishing common cases from newly added or removed benchmark items.
        """
        report_id = f"DIFF-{abs(hash(baseline_name + candidate_name)) % 1000000:06d}"

        # Map by case_id
        base_map = {c.get("case_id", f"case_{i}"): c for i, c in enumerate(baseline_cases)}
        cand_map = {c.get("case_id", f"case_{i}"): c for i, c in enumerate(candidate_cases)}

        common_ids = sorted(list(set(base_map.keys()) & set(cand_map.keys())))
        added_ids = sorted(list(set(cand_map.keys()) - set(base_map.keys())))
        removed_ids = sorted(list(set(base_map.keys()) - set(cand_map.keys())))
        
        comparisons: List[CaseComparison] = []
        both_passed = 0
        both_failed = 0
        improvements = 0
        regressions = 0
        critical_safety = 0
        state_transitions: Dict[str, int] = {}

        # 1. Compare common cases
        for cid in common_ids:
            b_case = base_map[cid]
            c_case = cand_map[cid]

            b_pass = bool(b_case.get("passed", True))
            c_pass = bool(c_case.get("passed", True))

            b_verdict = b_case.get("response_state") or b_case.get("verdict") or "UNKNOWN"
            c_verdict = c_case.get("response_state") or c_case.get("verdict") or "UNKNOWN"

            trans_key = f"{b_verdict} -> {c_verdict}"
            state_transitions[trans_key] = state_transitions.get(trans_key, 0) + 1

            is_reg = b_pass and not c_pass
            is_imp = not b_pass and c_pass

            severity = None
            delta_notes = ""
            violations = self.detect_safety_violations(c_case)

            if violations:
                severity = RegressionSeverity.CRITICAL_SAFETY_REGRESSION
                critical_safety += 1
                delta_notes = f"Safety violations: {', '.join([v.value for v in violations])}"
            elif is_reg:
                regressions += 1
                if "scaffold" in str(c_case).lower() or "quarantine" in str(c_case).lower() or "fabricated" in str(c_case).lower():
                    severity = RegressionSeverity.CRITICAL_SAFETY_REGRESSION
                    critical_safety += 1
                    delta_notes = "Critical security/quarantine regression"
                elif b_verdict in ("ANSWER_DIRECT", "ANSWER_QUALIFIED", "ANSWER_SUPPORTED") and c_verdict.startswith("ABSTAIN"):
                    severity = RegressionSeverity.LEGAL_CORRECTNESS_REGRESSION
                    delta_notes = "False abstention regression on previously settled inquiry"
                else:
                    severity = RegressionSeverity.CALIBRATION_DRIFT
                    delta_notes = "Disposition calibration shift"
            elif is_imp:
                improvements += 1
                delta_notes = "Prior failure resolved in candidate"
            elif b_pass and c_pass:
                both_passed += 1
            else:
                both_failed += 1

            comparisons.append(
                CaseComparison(
                    case_id=cid,
                    query=c_case.get("query", b_case.get("query", "")),
                    baseline_passed=b_pass,
                    candidate_passed=c_pass,
                    baseline_verdict=b_verdict,
                    candidate_verdict=c_verdict,
                    is_regression=is_reg,
                    is_improvement=is_imp,
                    regression_severity=severity,
                    safety_violations=[v.value for v in violations],
                    delta_notes=delta_notes,
                )
            )

        # 2. Evaluate newly added cases separately
        newly_added_results: List[NewlyAddedCaseResult] = []
        newly_passed = 0
        for aid in added_ids:
            a_case = cand_map[aid]
            a_pass = bool(a_case.get("passed", True))
            if a_pass:
                newly_passed += 1
            a_verdict = a_case.get("response_state") or a_case.get("verdict") or "UNKNOWN"
            a_violations = self.detect_safety_violations(a_case)
            if a_violations:
                critical_safety += len(a_violations)

            newly_added_results.append(
                NewlyAddedCaseResult(
                    case_id=aid,
                    query=a_case.get("query", ""),
                    passed=a_pass,
                    verdict=a_verdict,
                    safety_violations=[v.value for v in a_violations],
                    notes="Newly introduced benchmark case",
                )
            )

        total_common = len(common_ids)
        base_rate = (both_passed + regressions) / max(1, total_common) if total_common > 0 else 0.0
        cand_rate = (both_passed + improvements) / max(1, total_common) if total_common > 0 else 0.0
        delta_rate = cand_rate - base_rate

        new_count = len(added_ids)
        new_pass_rate = newly_passed / max(1, new_count) if new_count > 0 else 0.0

        is_free = (regressions == 0 and critical_safety == 0)

        summary = (
            f"Compared {total_common} common cases between '{baseline_name}' and '{candidate_name}': "
            f"{both_passed} both passed, {improvements} improved, {regressions} regressions ({critical_safety} critical safety). "
            f"Pass rate on common subset changed from {base_rate:.1%} to {cand_rate:.1%} (delta: {delta_rate:+.1%}). "
            f"Evaluated {new_count} newly added cases (pass rate: {new_pass_rate:.1%})."
        )

        return DifferentialEvaluationReport(
            report_id=report_id,
            baseline_name=baseline_name,
            candidate_name=candidate_name,
            total_compared_cases=total_common,
            both_passed_count=both_passed,
            both_failed_count=both_failed,
            improvements_count=improvements,
            regressions_count=regressions,
            critical_safety_regressions=critical_safety,
            baseline_pass_rate=base_rate,
            candidate_pass_rate=cand_rate,
            pass_rate_delta=delta_rate,
            state_transitions=state_transitions,
            case_comparisons=comparisons,
            newly_added_cases_count=new_count,
            newly_added_passed_count=newly_passed,
            newly_added_pass_rate=new_pass_rate,
            newly_added_cases=newly_added_results,
            removed_cases_count=len(removed_ids),
            removed_case_ids=removed_ids,
            is_regression_free=is_free,
            summary=summary,
        )
