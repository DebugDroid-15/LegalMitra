"""
Answer Completeness & Qualification Auditor Module (Phase 57)

Evaluates final legal answers across 4 orthogonal dimensions:
1. Factual and Legal Support: Verification of citations and evidentiary grounding.
2. Material Completeness: Preservation of decomposed issues, exceptions, and provisos.
3. Decision Calibration: Appropriateness of disposition state (avoiding false certainty and false abstention).
4. Internal Consistency: Absence of intra-answer contradictions across sections.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Tuple


class CalibrationVerdict(str, Enum):
    """Decision calibration assessment."""
    WELL_CALIBRATED = "WELL_CALIBRATED"
    FALSE_CERTAINTY = "FALSE_CERTAINTY"
    FALSE_ABSTENTION = "FALSE_ABSTENTION"
    UNNECESSARY_QUALIFICATION = "UNNECESSARY_QUALIFICATION"
    CONFLATED_MULTI_ISSUE = "CONFLATED_MULTI_ISSUE"


@dataclass
class CompletenessDimensionScore:
    """Score and diagnostic assessment for a single completeness dimension."""
    dimension_name: str
    score: float  # 0.0 to 1.0
    weight: float
    passed: bool
    diagnostic_notes: List[str] = field(default_factory=list)
    identified_gaps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension_name": self.dimension_name,
            "score": round(self.score, 4),
            "weight": self.weight,
            "passed": self.passed,
            "diagnostic_notes": self.diagnostic_notes,
            "identified_gaps": self.identified_gaps,
        }


@dataclass
class CompletenessAuditReport:
    """Full 4-dimensional completeness and qualification audit report."""
    audit_id: str
    query: str
    answer_text: str
    factual_and_legal_support: CompletenessDimensionScore
    material_completeness: CompletenessDimensionScore
    decision_calibration: CompletenessDimensionScore
    internal_consistency: CompletenessDimensionScore
    overall_completeness_score: float  # 0.0 to 1.0
    calibration_verdict: CalibrationVerdict
    is_audit_passed: bool
    omitted_statutory_bars: List[str] = field(default_factory=list)
    omitted_provisos: List[str] = field(default_factory=list)
    intra_contradictions: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "query": self.query,
            "answer_text": self.answer_text,
            "dimensions": {
                "factual_and_legal_support": self.factual_and_legal_support.to_dict(),
                "material_completeness": self.material_completeness.to_dict(),
                "decision_calibration": self.decision_calibration.to_dict(),
                "internal_consistency": self.internal_consistency.to_dict(),
            },
            "overall_completeness_score": round(self.overall_completeness_score, 4),
            "calibration_verdict": self.calibration_verdict.value,
            "is_audit_passed": self.is_audit_passed,
            "omitted_statutory_bars": self.omitted_statutory_bars,
            "omitted_provisos": self.omitted_provisos,
            "intra_contradictions": self.intra_contradictions,
            "remediation_recommendations": self.remediation_recommendations,
        }


class AnswerCompletenessAuditor:
    """
    Independent completeness and qualification auditor for LegalMitra responses.
    """

    DIMENSION_WEIGHTS = {
        "factual_and_legal_support": 0.30,
        "material_completeness": 0.30,
        "decision_calibration": 0.20,
        "internal_consistency": 0.20,
    }

    KNOWN_MANDATORY_EXCEPTIONS = {
        "sra_infrastructure": {
            "query_terms": ["specific performance", "infrastructure", "highway", "port", "power"],
            "must_contain": ["section 20a", "bar", "prohibit", "impediment", "delay"],
            "description": "Section 20A Specific Relief Act statutory bar on injunctions for infrastructure projects",
        },
        "hsa_pre_2004_partition": {
            "query_terms": ["hindu succession", "daughter", "coparcener", "coparcenary"],
            "must_contain": ["20 december 2004", "partition", "proviso", "registered"],
            "description": "Section 6(1) Proviso Hindu Succession Act preserving pre-20 Dec 2004 registered partitions",
        },
        "commercial_courts_urgent_relief": {
            "query_terms": ["commercial courts", "section 12a", "mediation"],
            "must_contain": ["urgent interim relief", "urgency", "exception", "patil automation"],
            "description": "Urgent interim relief exception to Section 12A mandatory pre-institution mediation",
        },
        "ni_act_notice_timelines": {
            "query_terms": ["cheque bounce", "section 138", "dishonour"],
            "must_contain": ["30 days", "15 days", "notice", "cause of action"],
            "description": "Statutory notice requirement (30 days) and 15-day cure window under Section 138 NI Act",
        },
    }

    def audit(
        self,
        query: str,
        answer_text: str,
        citations: List[str],
        response_state: Optional[str] = None,
        decomposed_issues: Optional[List[Dict[str, Any]]] = None,
    ) -> CompletenessAuditReport:
        """
        Executes a 4-dimensional completeness audit.
        """
        audit_id = f"ACA-{abs(hash(query + answer_text)) % 1000000:06d}"

        # 1. Factual and Legal Support Audit
        support_score, support_notes, support_gaps = self._audit_support(answer_text, citations)
        support_dim = CompletenessDimensionScore(
            dimension_name="factual_and_legal_support",
            score=support_score,
            weight=self.DIMENSION_WEIGHTS["factual_and_legal_support"],
            passed=support_score >= 0.70,
            diagnostic_notes=support_notes,
            identified_gaps=support_gaps,
        )

        # 2. Material Completeness Audit
        comp_score, comp_notes, comp_gaps, omitted_bars, omitted_provisos = self._audit_completeness(
            query, answer_text, decomposed_issues
        )
        comp_dim = CompletenessDimensionScore(
            dimension_name="material_completeness",
            score=comp_score,
            weight=self.DIMENSION_WEIGHTS["material_completeness"],
            passed=comp_score >= 0.70 and len(omitted_bars) == 0,
            diagnostic_notes=comp_notes,
            identified_gaps=comp_gaps,
        )

        # 3. Decision Calibration Audit
        calib_score, calib_verdict, calib_notes, calib_gaps = self._audit_calibration(
            query, answer_text, response_state, omitted_bars + omitted_provisos
        )
        calib_dim = CompletenessDimensionScore(
            dimension_name="decision_calibration",
            score=calib_score,
            weight=self.DIMENSION_WEIGHTS["decision_calibration"],
            passed=calib_score >= 0.70,
            diagnostic_notes=calib_notes,
            identified_gaps=calib_gaps,
        )

        # 4. Internal Consistency Audit
        cons_score, contradictions, cons_notes = self._audit_consistency(answer_text)
        cons_dim = CompletenessDimensionScore(
            dimension_name="internal_consistency",
            score=cons_score,
            weight=self.DIMENSION_WEIGHTS["internal_consistency"],
            passed=cons_score >= 0.80,
            diagnostic_notes=cons_notes,
            identified_gaps=contradictions,
        )

        # Overall weighted completeness score
        overall_score = (
            support_dim.score * support_dim.weight
            + comp_dim.score * comp_dim.weight
            + calib_dim.score * calib_dim.weight
            + cons_dim.score * cons_dim.weight
        )

        # Recommendations
        recommendations = []
        if omitted_bars:
            recommendations.append(f"Incorporate statutory bars: {', '.join(omitted_bars)}")
        if omitted_provisos:
            recommendations.append(f"Incorporate missing provisos: {', '.join(omitted_provisos)}")
        if calib_verdict == CalibrationVerdict.FALSE_CERTAINTY:
            recommendations.append("Calibrate absolute disposition to qualified or conditional answer")
        if contradictions:
            recommendations.append(f"Resolve {len(contradictions)} internal text contradictions")

        is_passed = (
            support_dim.passed
            and comp_dim.passed
            and calib_dim.passed
            and cons_dim.passed
            and overall_score >= 0.75
        )

        return CompletenessAuditReport(
            audit_id=audit_id,
            query=query,
            answer_text=answer_text,
            factual_and_legal_support=support_dim,
            material_completeness=comp_dim,
            decision_calibration=calib_dim,
            internal_consistency=cons_dim,
            overall_completeness_score=overall_score,
            calibration_verdict=calib_verdict,
            is_audit_passed=is_passed,
            omitted_statutory_bars=omitted_bars,
            omitted_provisos=omitted_provisos,
            intra_contradictions=contradictions,
            remediation_recommendations=recommendations,
        )

    def _audit_support(
        self, answer_text: str, citations: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        notes = []
        gaps = []
        if not citations:
            if "abstain" in answer_text.lower() or "insufficient" in answer_text.lower():
                notes.append("No citations provided; appropriate for abstention response.")
                return 0.90, notes, gaps
            else:
                gaps.append("Substantive legal propositions made without cited authority.")
                return 0.30, notes, gaps

        # Check for citation anchoring in text
        cited_in_text = 0
        for cit in citations:
            # Check if citation appears or key words from citation appear in text
            cit_words = [w for w in re.split(r"[\s,()]+", cit) if len(w) > 3 and not w.isdigit()]
            if any(w.lower() in answer_text.lower() for w in cit_words):
                cited_in_text += 1
            else:
                gaps.append(f"Citation '{cit}' listed in metadata but unreferenced in text body.")

        score = cited_in_text / max(1, len(citations))
        notes.append(f"Citation text grounding: {cited_in_text}/{len(citations)} citations anchored in text.")
        return score, notes, gaps

    def _audit_completeness(
        self, query: str, answer_text: str, decomposed_issues: Optional[List[Dict[str, Any]]]
    ) -> Tuple[float, List[str], List[str], List[str], List[str]]:
        notes = []
        gaps = []
        omitted_bars = []
        omitted_provisos = []
        score = 1.0

        q_lower = query.lower()
        ans_lower = answer_text.lower()

        # Check mandatory exceptions
        for exc_id, info in self.KNOWN_MANDATORY_EXCEPTIONS.items():
            matched_terms = [t for t in info["query_terms"] if t in q_lower]
            if len(matched_terms) >= 2:
                has_contain = any(t in ans_lower for t in info["must_contain"])
                if not has_contain:
                    if "bar" in info["description"].lower():
                        score -= 0.35
                        omitted_bars.append(info["description"])
                    else:
                        score -= 0.25
                        omitted_provisos.append(info["description"])
                    gaps.append(f"Omitted mandatory legal qualification: {info['description']}")

        # Check decomposed issues coverage
        if decomposed_issues:
            addressed_count = 0
            for issue in decomposed_issues:
                stmt = issue.get("statement", "")
                stmt_words = [w for w in re.split(r"\W+", stmt.lower()) if len(w) > 4]
                if any(w in ans_lower for w in stmt_words):
                    addressed_count += 1
                else:
                    gaps.append(f"Decomposed issue not addressed in answer: '{stmt}'")
            issue_ratio = addressed_count / max(1, len(decomposed_issues))
            notes.append(f"Issue decomposition coverage: {addressed_count}/{len(decomposed_issues)}")
            score = (score + issue_ratio) / 2.0

        score = max(0.0, min(1.0, score))
        return score, notes, gaps, omitted_bars, omitted_provisos

    def _audit_calibration(
        self,
        query: str,
        answer_text: str,
        response_state: Optional[str],
        omitted_exceptions: List[str],
    ) -> Tuple[float, CalibrationVerdict, List[str], List[str]]:
        notes = []
        gaps = []
        state = response_state or "UNKNOWN"
        ans_lower = answer_text.lower()

        # Check for false certainty
        if omitted_exceptions and state in ("ANSWER_DIRECT", "ANSWER_SUPPORTED"):
            gaps.append("Direct answer emitted despite active statutory exceptions/provisos.")
            return 0.40, CalibrationVerdict.FALSE_CERTAINTY, notes, gaps

        if any(w in ans_lower for w in ["unconditionally", "in all circumstances", "absolute right"]) and state == "ANSWER_DIRECT":
            gaps.append("Uncalibrated absolute assertion emitted in direct answer.")
            return 0.50, CalibrationVerdict.FALSE_CERTAINTY, notes, gaps

        # Check for false abstention
        if state.startswith("ABSTAIN") and any(
            t in query.lower() for t in ["hindu succession act", "specific relief act", "commercial courts act"]
        ):
            # If well-known statutory rule exists and user asked a straightforward statutory question
            if "limitation" in query.lower() or "pre-institution" in query.lower() or ("mediation" in query.lower() and "mandatory" in query.lower()):
                gaps.append("Abstention emitted on clearly settled statutory question.")
                return 0.40, CalibrationVerdict.FALSE_ABSTENTION, notes, gaps

        # Multi-issue conflation check
        if " and " in query.lower() and state in ("ANSWER_DIRECT", "ANSWER_QUALIFIED"):
            if "Resolved Issues" not in answer_text and "Section 25F" in query and "Industrial Relations Code" in query:
                gaps.append("Multi-issue inquiry with divergent temporal status conflated into single disposition.")
                return 0.50, CalibrationVerdict.CONFLATED_MULTI_ISSUE, notes, gaps

        notes.append(f"Decision disposition '{state}' is well-calibrated against inquiry facts and law.")
        return 0.95, CalibrationVerdict.WELL_CALIBRATED, notes, gaps

    def _audit_consistency(self, answer_text: str) -> Tuple[float, List[str], List[str]]:
        notes = []
        contradictions = []
        ans_lower = answer_text.lower()

        contradiction_pairs = [
            ("injunction is barred", "injunction may be granted"),
            ("cannot grant an injunction", "seek an interim injunction"),
            ("mediation is mandatory", "mediation is purely discretionary"),
            ("not entitled to coparcenary", "entitled to an equal coparcenary share"),
            ("debt is extinguished", "promoter remains personally liable under section 31"),
        ]

        for s1, s2 in contradiction_pairs:
            if s1 in ans_lower and s2 in ans_lower:
                contradictions.append(f"Intra-answer contradiction between '{s1}' and '{s2}'")

        if contradictions:
            return 0.30, contradictions, notes

        notes.append("No internal contradictions detected across answer sections.")
        return 1.0, contradictions, notes
