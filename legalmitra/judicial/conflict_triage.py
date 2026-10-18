"""LegalMitra Judicial Knowledge Infrastructure — Precedent Conflict Triage Engine.

Structured, human-in-the-loop workflow for identifying, categorizing, and triaging
potentially conflicting judicial propositions, especially across co-equal High Court benches:
- Rigorous distinction between genuine doctrinal conflict, factual distinction, and statutory divergence
- Court hierarchy & Article 141 preservation
- Authorization gating: only verified legal reviewers can resolve conflicts; automated algorithms cannot declare winners
- Full immutable audit trails and prioritized review queuing
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ConflictCategory(str, Enum):
    CO_EQUAL_HIGH_COURT_CONFLICT = "CO_EQUAL_HIGH_COURT_CONFLICT"
    INTRA_COURT_CO_EQUAL_BENCH_DIVERGENCE = "INTRA_COURT_CO_EQUAL_BENCH_DIVERGENCE"
    FACTUALLY_DISTINGUISHABLE = "FACTUALLY_DISTINGUISHABLE"
    STATUTORY_VERSION_DIVERGENCE = "STATUTORY_VERSION_DIVERGENCE"
    RATIO_VS_OBITER_AMBIGUITY = "RATIO_VS_OBITER_AMBIGUITY"
    RESOLVED_BY_SUBSEQUENT_APEX_DECISION = "RESOLVED_BY_SUBSEQUENT_APEX_DECISION"


class TriageStatus(str, Enum):
    PENDING_TRIAGE = "PENDING_TRIAGE"
    ROUTED_FOR_ADVOCATE_REVIEW = "ROUTED_FOR_ADVOCATE_REVIEW"
    CONFIRMED_GENUINE_CONFLICT = "CONFIRMED_GENUINE_CONFLICT"
    RESOLVED_FACTUALLY_DISTINGUISHED = "RESOLVED_FACTUALLY_DISTINGUISHED"
    RESOLVED_REFERRED_TO_LARGER_BENCH = "RESOLVED_REFERRED_TO_LARGER_BENCH"
    RESOLVED_BY_APEX_COURT = "RESOLVED_BY_APEX_COURT"


@dataclass
class PrecedentConflictRecord:
    conflict_id: str
    case_a_id: str
    case_a_title: str
    case_a_court_id: str
    case_a_bench_count: int
    case_a_passage_anchor: str
    case_a_proposition: str

    case_b_id: str
    case_b_title: str
    case_b_court_id: str
    case_b_bench_count: int
    case_b_passage_anchor: str
    case_b_proposition: str

    governing_statute_section: str
    category: ConflictCategory
    status: TriageStatus = TriageStatus.PENDING_TRIAGE
    priority_score: float = 1.0  # 1.0 (standard) to 5.0 (critical national conflict)
    priority_rationale: str = ""
    assigned_reviewer: Optional[str] = None
    reviewer_authorized: bool = False
    reviewer_decision_rationale: Optional[str] = None
    audit_trail: List[Tuple[str, str, str]] = field(default_factory=list)

    def transition(self, new_status: TriageStatus, note: str = "") -> None:
        self.status = new_status
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.audit_trail.append((ts, new_status.value, note))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "case_a": {
                "case_id": self.case_a_id,
                "title": self.case_a_title,
                "court_id": self.case_a_court_id,
                "bench_count": self.case_a_bench_count,
                "passage_anchor": self.case_a_passage_anchor,
                "proposition": self.case_a_proposition,
            },
            "case_b": {
                "case_id": self.case_b_id,
                "title": self.case_b_title,
                "court_id": self.case_b_court_id,
                "bench_count": self.case_b_bench_count,
                "passage_anchor": self.case_b_passage_anchor,
                "proposition": self.case_b_proposition,
            },
            "governing_statute_section": self.governing_statute_section,
            "category": self.category.value,
            "status": self.status.value,
            "priority_score": self.priority_score,
            "priority_rationale": self.priority_rationale,
            "assigned_reviewer": self.assigned_reviewer,
            "reviewer_authorized": self.reviewer_authorized,
            "reviewer_decision_rationale": self.reviewer_decision_rationale,
            "audit_trail": self.audit_trail,
        }


class PrecedentConflictTriageManager:
    """Manages the lifecycle of candidate judicial conflicts with strict human-in-the-loop review."""

    def __init__(self) -> None:
        self._conflicts: Dict[str, PrecedentConflictRecord] = {}
        self._authorized_reviewers: Set[str] = {"ADV-SHATRUJEET-01", "ADV-REGULATORY-LEAD"}

    def register_conflict(self, record: PrecedentConflictRecord) -> None:
        # Validate that paragraph anchors are present and not empty
        if not record.case_a_passage_anchor or not record.case_b_passage_anchor:
            raise ValueError(f"Conflict {record.conflict_id} violates evidentiary requirement: Both cases must have exact paragraph anchors.")

        self._conflicts[record.conflict_id] = record

    def get_conflict(self, conflict_id: str) -> Optional[PrecedentConflictRecord]:
        return self._conflicts.get(conflict_id)

    def list_all_conflicts(self) -> List[PrecedentConflictRecord]:
        return list(self._conflicts.values())

    def get_prioritized_queue(self) -> List[PrecedentConflictRecord]:
        """Return pending review queue ordered by priority score descending."""
        pending = [c for c in self._conflicts.values() if c.status in (TriageStatus.PENDING_TRIAGE, TriageStatus.ROUTED_FOR_ADVOCATE_REVIEW)]
        return sorted(pending, key=lambda c: c.priority_score, reverse=True)

    def resolve_conflict(
        self,
        conflict_id: str,
        reviewer_id: str,
        resolution_status: TriageStatus,
        rationale: str,
    ) -> PrecedentConflictRecord:
        """Resolve or classify a conflict. Enforces reviewer authorization invariant."""
        conflict = self.get_conflict(conflict_id)
        if not conflict:
            raise KeyError(f"Conflict ID {conflict_id} not found in triage register.")

        if reviewer_id not in self._authorized_reviewers:
            raise PermissionError(
                f"Unauthorized reviewer '{reviewer_id}'. Conflict resolution requires certified advocate authorization."
            )

        if resolution_status in (TriageStatus.PENDING_TRIAGE, TriageStatus.ROUTED_FOR_ADVOCATE_REVIEW):
            raise ValueError("Resolution status must be an affirmative resolution (CONFIRMED_GENUINE, RESOLVED_FACTUALLY, etc.).")

        if not rationale or len(rationale.strip()) < 15:
            raise ValueError("Reviewer rationale must be detailed and legally justified (min. 15 characters).")

        conflict.assigned_reviewer = reviewer_id
        conflict.reviewer_authorized = True
        conflict.reviewer_decision_rationale = rationale
        conflict.transition(resolution_status, f"Resolved by {reviewer_id}: {rationale}")

        return conflict

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_conflicts": len(self._conflicts),
            "pending_review_count": sum(1 for c in self._conflicts.values() if c.status in (TriageStatus.PENDING_TRIAGE, TriageStatus.ROUTED_FOR_ADVOCATE_REVIEW)),
            "conflicts": {cid: c.to_dict() for cid, c in self._conflicts.items()},
        }
