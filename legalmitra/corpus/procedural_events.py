"""
LegalMitra Court Hearing & Procedural Event Model
Models Indian litigation lifecycles, court cause lists, hearing events, interim orders,
final decrees, and procedural state transitions across civil and criminal proceedings.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class HearingType(str, Enum):
    FIRST_LISTING_ADMISSION = "first_listing_admission"
    NOTICE_RETURNABLE = "notice_returnable"
    INTERLOCUTORY_APPLICATION = "interlocutory_application"
    FRAMING_OF_ISSUES = "framing_of_issues"
    FRAMING_OF_CHARGES = "framing_of_charges"
    PROSECUTION_EVIDENCE = "prosecution_evidence"
    PLAINTIFF_EVIDENCE = "plaintiff_evidence"
    DEFENCE_EVIDENCE = "defence_evidence"
    STATEMENT_ACCUSED_313 = "statement_under_313"
    FINAL_ARGUMENTS = "final_arguments"
    PRONOUNCEMENT_OF_ORDER = "pronouncement_of_order"
    PRONOUNCEMENT_OF_JUDGMENT = "pronouncement_of_judgment"
    COMPLIANCE_REPORT = "compliance_report"
    MISCELLANEOUS = "miscellaneous"


class OrderDispositionType(str, Enum):
    INTERIM_STAY_GRANTED = "interim_stay_granted"
    NOTICE_ISSUED = "notice_issued"
    STATUS_QUO_ORDERED = "status_quo_ordered"
    ADJOURNED = "adjourned"
    BAIL_GRANTED = "bail_granted"
    BAIL_REJECTED = "bail_rejected"
    ANTICIPATORY_BAIL_GRANTED = "anticipatory_bail_granted"
    ANTICIPATORY_BAIL_REJECTED = "anticipatory_bail_rejected"
    DISMISSED_AS_WITHDRAWN = "dismissed_as_withdrawn"
    DISMISSED_DEFAULT = "dismissed_for_default"
    DISPOSED_OF_WITH_DIRECTIONS = "disposed_of_with_directions"
    ALLOWED = "allowed"
    DISMISSED_ON_MERITS = "dismissed_on_merits"
    REFERRED_TO_MEDIATION = "referred_to_mediation"
    TRANSFERRED = "transferred"
    DECREED = "decreed"


class ProceduralStage(str, Enum):
    PRE_FILING_LEGAL_NOTICE = "pre_filing_legal_notice"
    FILING_AND_DEFECT_SCRUTINY = "filing_and_defect_scrutiny"
    REGISTRATION_AND_NUMBERING = "registration_and_numbering"
    FIRST_LISTING_ADMISSION = "first_listing_admission"
    SERVICE_OF_SUMMONS_OR_NOTICE = "service_of_summons_or_notice"
    PLEADINGS_COMPLETION = "pleadings_completion"
    SETTLEMENT_OR_MEDIATION = "settlement_or_mediation"
    FRAMING_OF_ISSUES_OR_CHARGES = "framing_of_issues_or_charges"
    EVIDENCE_OR_TRIAL = "evidence_or_trial"
    FINAL_HEARING = "final_hearing"
    RESERVED_FOR_JUDGMENT = "reserved_for_judgment"
    JUDGMENT_PRONOUNCED = "judgment_pronounced"
    DECREE_DRAWN_UP = "decree_drawn_up"
    EXECUTION_OR_COMPLIANCE = "execution_or_compliance"
    APPELLATE_REVIEW = "appellate_review"


@dataclass
class CauseListEntry:
    entry_id: str
    court_name: str
    bench_name: str                      # e.g., "Court No. 3 - Hon'ble Justice X & Hon'ble Justice Y"
    cause_list_date: str                 # YYYY-MM-DD
    item_number: int
    case_type: str                       # e.g., "W.P.(C)", "CRL.M.C.", "SLP(Crl)"
    case_number: str                     # e.g., "1234/2026"
    party_petitioner_or_appellant: str
    party_respondent: str
    advocate_petitioner: str
    advocate_respondent: str
    listing_stage: str                   # e.g., "For Admission", "For Orders", "Final Disposal"
    is_supplementary: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HearingRecord:
    hearing_id: str
    case_id: str
    hearing_date: str                    # YYYY-MM-DD
    court_name: str
    bench: str
    hearing_type: HearingType
    proceedings_summary: str
    disposition: OrderDispositionType
    next_date_of_hearing: Optional[str] = None
    next_stage_purpose: Optional[str] = None
    order_document_url: Optional[str] = None
    recorded_at: str = ""

    def __post_init__(self):
        if not self.recorded_at:
            self.recorded_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["hearing_type"] = self.hearing_type.value
        d["disposition"] = self.disposition.value
        return d


@dataclass
class LitigationCaseLifecycle:
    case_id: str
    case_number: str
    court_name: str
    current_stage: ProceduralStage
    filing_date: str
    petitioner_or_plaintiff: str
    respondent_or_defendant: str
    acts_involved: List[str] = field(default_factory=list)
    provisions_involved: List[str] = field(default_factory=list)
    hearings: List[HearingRecord] = field(default_factory=list)
    is_disposed: bool = False
    disposal_date: Optional[str] = None
    final_disposition: Optional[str] = None

    def add_hearing(self, hearing: HearingRecord) -> None:
        self.hearings.append(hearing)
        if hearing.next_date_of_hearing:
            # Lifecycle remains active
            self.is_disposed = False
        if hearing.disposition in [
            OrderDispositionType.ALLOWED,
            OrderDispositionType.DISMISSED_ON_MERITS,
            OrderDispositionType.DISPOSED_OF_WITH_DIRECTIONS,
            OrderDispositionType.DECREED,
            OrderDispositionType.DISMISSED_AS_WITHDRAWN,
            OrderDispositionType.DISMISSED_DEFAULT
        ]:
            self.is_disposed = True
            self.disposal_date = hearing.hearing_date
            self.final_disposition = hearing.disposition.value

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["current_stage"] = self.current_stage.value
        d["hearings"] = [h.to_dict() for h in self.hearings]
        return d

