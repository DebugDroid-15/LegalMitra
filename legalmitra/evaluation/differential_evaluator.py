"""
Differential Evaluation & Regression Analysis Engine (Phase 57)

Compares evaluation outcomes across pipeline versions, benchmark iterations (PIT-V12 vs PIT-V13),
and model commits to detect performance deltas, newly introduced regressions, fixed defects,
and decision policy state shifts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
import os
from typing import Any, Dict, List, Optional, Tuple


class RegressionSeverity(str, Enum):
    """Severity of an introduced regression."""
    CRITICAL_SAFETY_REGRESSION = "CRITICAL_SAFETY_REGRESSION"
    LEGAL_CORRECTNESS_REGRESSION = "LEGAL_CORRECTNESS_REGRESSION"
    CALIBRATION_DRIFT = "CALIBRATION_DRIFT"
    MINOR_FORMATTING_REGRESSION = "MINOR_FORMATTING_REGRESSION"


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
            "delta_notes": self.delta_notes,
        }


@dataclass
class DifferentialEvaluationReport:
    """Comprehensive differential evaluation and regression analysis report."""
    report_id: str
    baseline_name: str
    candidate_name: str
    total_compared_cases: int
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
            "is_regression_free": self.is_regression_free,
            "summary": self.summary,
            "case_comparisons": [c.to_dict() for c in self.case_comparisons],
        }


class DifferentialEvaluator:
    """
    Evaluates and compares test results across versions or benchmark runs.
    """

    def compare_runs(
        self,
        baseline_cases: List[Dict[str, Any]],
        candidate_cases: List[Dict[str, Any]],
        baseline_name: str = "PIT-V12 Baseline",
        candidate_name: str = "PIT-V13 Candidate",
    ) -> DifferentialEvaluationReport:
        """
        Computes differential comparison between baseline and candidate evaluation runs.
        """
        report_id = f"DIFF-{abs(hash(baseline_name + candidate_name)) % 1000000:06d}"

        # Map by case_id
        base_map = {c.get("case_id", f"case_{i}"): c for i, c in enumerate(baseline_cases)}
        cand_map = {c.get("case_id", f"case_{i}"): c for i, c in enumerate(candidate_cases)}

        common_ids = sorted(list(set(base_map.keys()) & set(cand_map.keys())))
        
        comparisons: List[CaseComparison] = []
        both_passed = 0
        both_failed = 0
        improvements = 0
        regressions = 0
        critical_safety = 0
        state_transitions: Dict[str, int] = {}

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

            if is_reg:
                regressions += 1
                # Check for critical safety regressions
                if "scaffold" in str(c_case).lower() or "quarantine" in str(c_case).lower() or "fabricated" in str(c_case).lower():
                    severity = RegressionSeverity.CRITICAL_SAFETY_REGRESSION
                    critical_safety += 1
                    delta_notes = "Critical security/quarantine regression"
                elif b_verdict in ("ANSWER_DIRECT", "ANSWER_QUALIFIED") and c_verdict.startswith("ABSTAIN"):
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
                    delta_notes=delta_notes,
                )
            )

        total_common = len(common_ids)
        base_rate = (both_passed + regressions) / max(1, total_common)
        cand_rate = (both_passed + improvements) / max(1, total_common)
        delta_rate = cand_rate - base_rate

        is_free = (regressions == 0 and critical_safety == 0)

        summary = (
            f"Compared {total_common} cases between '{baseline_name}' and '{candidate_name}': "
            f"{both_passed} both passed, {improvements} improved, {regressions} regressions ({critical_safety} critical safety). "
            f"Pass rate changed from {base_rate:.1%} to {cand_rate:.1%} (delta: {delta_rate:+.1%})."
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
            is_regression_free=is_free,
            summary=summary,
        )
