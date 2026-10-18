"""LegalMitra Judicial Knowledge Infrastructure — Procedural History Graph.

Traces litigation pathways across District Courts, High Courts, Tribunals, and Supreme Court:
- Original trials, appeals, revisions, remands, and curative stages
- Multi-branch procedural lifecycles (interlocutory orders, cross-appeals, retrials)
- Primary-source evidence anchoring for every procedural transition
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProceduralStage(str, Enum):
    TRIAL_ORIGINAL_FILING = "TRIAL_ORIGINAL_FILING"
    TRIAL_INTERLOCUTORY_ORDER = "TRIAL_INTERLOCUTORY_ORDER"
    TRIAL_FINAL_JUDGMENT = "TRIAL_FINAL_JUDGMENT"
    FIRST_APPEAL = "FIRST_APPEAL"
    REVISION_PETITION = "REVISION_PETITION"
    SECTION_482_QUASHING = "SECTION_482_QUASHING"
    HIGH_COURT_DIVISION_BENCH = "HIGH_COURT_DIVISION_BENCH"
    SPECIAL_LEAVE_PETITION = "SPECIAL_LEAVE_PETITION"
    SUPREME_COURT_REGULAR_APPEAL = "SUPREME_COURT_REGULAR_APPEAL"
    REVIEW_PETITION = "REVIEW_PETITION"
    CURATIVE_PETITION = "CURATIVE_PETITION"
    REMAND_TO_LOWER_COURT = "REMAND_TO_LOWER_COURT"
    EXECUTION_PROCEEDING = "EXECUTION_PROCEEDING"


class DisposalNature(str, Enum):
    ALLOWED_DECREED = "ALLOWED_DECREED"
    DISMISSED = "DISMISSED"
    PARTLY_ALLOWED = "PARTLY_ALLOWED"
    REMANDED = "REMANDED"
    SET_ASIDE_REVERSED = "SET_ASIDE_REVERSED"
    SETTLED_COMPROMISE = "SETTLED_COMPROMISE"
    WITHDRAWN = "WITHDRAWN"
    PENDING_ADJUDICATION = "PENDING_ADJUDICATION"


@dataclass
class ProceduralEvent:
    event_id: str
    case_chain_id: str
    court_id: str
    court_name: str
    stage: ProceduralStage
    filing_number: str
    order_date: str
    coram_judge_names: List[str]
    disposal_nature: DisposalNature
    summary_of_order: str
    supporting_document_id: Optional[str] = None
    preceding_event_id: Optional[str] = None
    is_verified: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "case_chain_id": self.case_chain_id,
            "court_id": self.court_id,
            "court_name": self.court_name,
            "stage": self.stage.value,
            "filing_number": self.filing_number,
            "order_date": self.order_date,
            "coram_judge_names": self.coram_judge_names,
            "disposal_nature": self.disposal_nature.value,
            "summary_of_order": self.summary_of_order,
            "supporting_document_id": self.supporting_document_id,
            "preceding_event_id": self.preceding_event_id,
            "is_verified": self.is_verified,
        }


class ProceduralHistoryGraph:
    """Manages the procedural trajectory of litigations through trial, appellate, and apex courts."""

    def __init__(self) -> None:
        self._events: Dict[str, ProceduralEvent] = {}
        self._chains: Dict[str, List[str]] = {}  # case_chain_id -> list of event_ids in sequence

    def record_event(self, event: ProceduralEvent) -> None:
        self._events[event.event_id] = event
        if event.case_chain_id not in self._chains:
            self._chains[event.case_chain_id] = []
        self._chains[event.case_chain_id].append(event.event_id)

    def get_event(self, event_id: str) -> Optional[ProceduralEvent]:
        return self._events.get(event_id)

    def get_trajectory(self, case_chain_id: str) -> List[ProceduralEvent]:
        event_ids = self._chains.get(case_chain_id, [])
        return [self._events[eid] for eid in event_ids if eid in self._events]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_chains": len(self._chains),
            "total_events": len(self._events),
            "chains": {
                chain_id: [self._events[eid].to_dict() for eid in eids if eid in self._events]
                for chain_id, eids in self._chains.items()
            },
        }
