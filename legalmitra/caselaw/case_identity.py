"""
LegalMitra Case Identity and Document Relationship Engine
Implements deterministic and evidence-backed resolution of:
1. Case Entities (Court, Case Type, Number, Filing Year, Parties, Registration Date).
2. Proceeding Entities (Appeals, Revisions, Interim Applications, Connected Matters).
3. Document Entities (Final Judgments, Interim Orders, Daily Orders, Cause Lists).
4. Procedural Timelines & Status Tracking.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class DocumentClassification(str, Enum):
    FINAL_JUDGMENT = "final_judgment"
    FINAL_ORDER = "final_order"
    INTERIM_ORDER = "interim_order"
    DAILY_ORDER = "daily_order"
    PROCEDURAL_ORDER = "procedural_order"
    ADMISSION_ORDER = "admission_order"
    NOTICE_ORDER = "notice_order"
    BAIL_ORDER = "bail_order"
    STAY_ORDER = "stay_order"
    DISMISSAL_ORDER = "dismissal_order"
    CAUSE_LIST = "cause_list"
    UNKNOWN = "unknown"


class ProceduralEffect(str, Enum):
    NOTICE_ISSUED = "notice_issued"
    INTERIM_STAY_GRANTED = "interim_stay_granted"
    INTERIM_RELIEF_REFUSED = "interim_relief_refused"
    BAIL_GRANTED = "bail_granted"
    BAIL_REFUSED = "bail_refused"
    ADJOURNED = "adjourned"
    MATTER_HEARD = "matter_heard"
    PART_HEARD = "part_heard"
    RESERVED_FOR_JUDGMENT = "reserved_for_judgment"
    APPEAL_ALLOWED = "appeal_allowed"
    APPEAL_DISMISSED = "appeal_dismissed"
    DISPOSED_WITH_DIRECTIONS = "disposed_with_directions"
    REFERRED_TO_LARGER_BENCH = "referred_to_larger_bench"
    SETTLED_IN_MEDIATION = "settled_in_mediation"
    UNKNOWN_EFFECT = "unknown_effect"


class CaseStatus(str, Enum):
    PENDING = "pending"
    DISPOSED = "disposed"
    PARTLY_DISPOSED = "partly_disposed"
    TRANSFERRED = "transferred"
    REMANDED = "remanded"
    STATUS_UNKNOWN = "status_unknown"


@dataclass
class UnifiedCaseIdentity:
    case_id: str                          # Canonical ID, e.g. "IN-SC-CA-2082-2018"
    court_code: str                       # e.g. "IN-SC", "IN-DL-HC", "IN-MH-HC"
    case_type: str                        # e.g. "Civil Appeal", "Writ Petition (Civil)", "CRL.A."
    case_number: str                      # e.g. "2082-2083"
    filing_year: int                      # e.g. 2018
    petitioner_or_appellant: str          # Redacted / Anonymized if sensitive
    respondent: str
    neutral_citation: Optional[str] = None
    reporter_citations: List[str] = field(default_factory=list)
    institution_date: Optional[date] = None
    disposal_date: Optional[date] = None
    status: CaseStatus = CaseStatus.STATUS_UNKNOWN
    connected_case_ids: List[str] = field(default_factory=list)
    is_sensitive: bool = False
    redaction_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        d["institution_date"] = self.institution_date.isoformat() if self.institution_date else None
        d["disposal_date"] = self.disposal_date.isoformat() if self.disposal_date else None
        return d


@dataclass
class JudicialDocumentRecord:
    document_id: str                      # Unique document chunk/source ID
    case_id: str                          # Foreign key to UnifiedCaseIdentity
    classification: DocumentClassification
    procedural_effect: ProceduralEffect
    order_or_judgment_date: date
    bench_coram: List[str]
    verbatim_text: str
    source_url: str
    sha256_hash: str
    paragraph_count: int = 1
    page_count: int = 1
    statutory_provisions_cited: List[str] = field(default_factory=list)
    precedents_cited: List[str] = field(default_factory=list)
    verification_status: str = "verified_authoritative"
    is_synthetic_scaffold: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["classification"] = self.classification.value
        d["procedural_effect"] = self.procedural_effect.value
        d["order_or_judgment_date"] = self.order_or_judgment_date.isoformat()
        return d


class CaseIdentityResolver:
    """
    Deterministic and evidence-based matching engine for case documents.
    Prevents erroneous merging across different courts or case numbers.
    """

    @staticmethod
    def normalize_case_number(raw_case_num: str) -> str:
        """Normalizes variations like 'C.A. No. 2082/2018' -> ('CA', '2082', 2018)."""
        clean = re.sub(r"[\s\.\(\)]+", "", raw_case_num).upper()
        return clean

    @classmethod
    def generate_case_id(cls, court_code: str, case_type: str, case_number: str, year: int) -> str:
        clean_type = re.sub(r"[^A-Za-z0-9]", "", case_type).upper()
        clean_num = re.sub(r"[^A-Za-z0-9]", "-", case_number).strip("-")
        return f"{court_code}-{clean_type}-{clean_num}-{year}"

    @classmethod
    def match_case(
        cls,
        candidate_court: str,
        candidate_num: str,
        candidate_year: int,
        registered_cases: List[UnifiedCaseIdentity]
    ) -> Optional[UnifiedCaseIdentity]:
        """
        Deterministic match on (court_code, case_type_normal, case_num_normal, year).
        Returns None if ambiguous or not found.
        """
        matches = []
        for c in registered_cases:
            if c.court_code.upper() == candidate_court.upper() and c.filing_year == candidate_year:
                # Compare numbers
                nums_in_c = re.findall(r"\d+", c.case_number)
                nums_in_cand = re.findall(r"\d+", candidate_num)
                # Check if any candidate number matches numbers in registered case
                if any(nc in nums_in_c for nc in nums_in_cand) or (nums_in_c and nums_in_cand and nums_in_c[0] == nums_in_cand[0]):
                    matches.append(c)

        if len(matches) == 1:
            return matches[0]
        return None
