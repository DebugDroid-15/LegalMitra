"""
LegalMitra National Legal Universe Models & Inventory Schemas (Phase 18)
Defines structured classes for cataloging all legal materials across India:
- Document family and legal authority level
- Temporal validity and bitemporal timestamps
- Jurisdiction, court, and issuing authority
- Ingestion lifecycle state: EXPECTED -> LOCATED -> ACCESSIBLE -> ACQUIRED -> PARSED -> INDEXED -> REVIEWED
"""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentFamily(str, Enum):
    CONSTITUTION = "constitution"
    CENTRAL_ACT = "central_act"
    STATE_ACT = "state_act"
    CONSTITUTIONAL_AMENDMENT = "constitutional_amendment"
    CENTRAL_AMENDMENT = "central_amendment"
    STATE_AMENDMENT = "state_amendment"
    SUBORDINATE_RULE = "subordinate_rule"
    REGULATION = "regulation"
    GAZETTE_NOTIFICATION = "gazette_notification"
    COMMENCEMENT_ORDER = "commencement_order"
    CIRCULAR = "circular"
    PRACTICE_DIRECTION = "practice_direction"
    COURT_RULE = "court_rule"
    JUDGMENT_SUPREME_COURT = "judgment_supreme_court"
    JUDGMENT_HIGH_COURT = "judgment_high_court"
    JUDGMENT_SUBORDINATE = "judgment_subordinate"
    TRIBUNAL_ORDER = "tribunal_order"
    CAUSE_LIST = "cause_list"
    HEARING_RECORD = "hearing_record"


class LegalAuthorityLevel(str, Enum):
    SUPREME_CONSTITUTIONAL = "supreme_constitutional"
    BINDING_CENTRAL_STATUTE = "binding_central_statute"
    BINDING_STATE_STATUTE = "binding_state_statute"
    BINDING_DELEGATED_LEGISLATION = "binding_delegated_legislation"
    BINDING_SUPREME_COURT_ART141 = "binding_supreme_court_art141"
    TERRITORIALLY_BINDING_HIGH_COURT = "territorially_binding_high_court"
    PERSUASIVE_PRECEDENT = "persuasive_precedent"
    STATUTORY_EXECUTIVE_ORDER = "statutory_executive_order"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    UNVERIFIED_SCAFFOLD = "unverified_scaffold"


class IngestionLifecycleState(str, Enum):
    # Discovery and locating
    DISCOVERED = "discovered"
    EXPECTED = "expected_to_exist"
    LOCATED = "located"
    ACCESSIBLE = "accessible"
    ACCESS_RESTRICTED = "access_restricted"
    AWAITING_ACQUISITION = "awaiting_acquisition"
    
    # Acquisition and extraction
    ACQUIRED = "acquired"
    INTEGRITY_CHECKED = "integrity_checked"
    PARSED = "parsed"
    EXTRACTION_FAILED = "extraction_failed"
    METADATA_VALIDATED = "metadata_validated"
    
    # Indexing and verification
    INDEXED = "indexed"
    SOURCE_VERIFIED = "source_verified"
    CURRENTNESS_CHECKED = "currentness_checked"
    PENDING_LEGAL_REVIEW = "pending_legal_review"
    LEGALLY_REVIEWED = "legally_reviewed"
    
    # Terminal and exceptional states
    QUARANTINED = "quarantined"
    SUPERSEDED = "superseded"
    REPEALED = "repealed"
    INACCESSIBLE = "inaccessible"
    RETRY_REQUIRED = "retry_required"


class LegalUniverseItem(BaseModel):
    """
    Standard record representing a single identifiable legal source or instrument
    in India's National Legal Universe Inventory.
    """
    record_id: str = Field(..., description="Unique persistent identifier, e.g. 'UNIV-CONST-1950' or 'UNIV-ACT-BNSS-2023'")
    official_title: str = Field(..., description="Official short title or case title")
    alternate_title: Optional[str] = Field(default=None, description="Popular or Hindi title, e.g. 'BNS 2023'")
    document_family: DocumentFamily
    authority_level: LegalAuthorityLevel
    jurisdiction: str = Field(..., description="'IN', 'IN-DL', 'IN-MH', etc.")
    issuing_authority_or_court: str = Field(..., description="e.g. 'Parliament of India', 'Supreme Court of India', 'High Court of Delhi'")
    parent_instrument_id: Optional[str] = Field(default=None, description="Parent statute ID if subordinate legislation")
    enactment_or_decision_date: Optional[date] = None
    commencement_date: Optional[date] = None
    repeal_date: Optional[date] = None
    source_url: str = Field(..., description="Authoritative portal or gazette URL")
    access_method: str = Field(default="direct_http", description="'direct_http', 'portal_search', 'egazette_pull'")
    retrieval_limitations: Optional[str] = None
    lifecycle_state: IngestionLifecycleState = Field(default=IngestionLifecycleState.EXPECTED)
    checksum_sha256: Optional[str] = None
    chunks_indexed: int = Field(default=0)
    is_synthetic_scaffold: bool = Field(default=False)
    legal_domain: str = Field(..., description="e.g. 'Criminal Law', 'Constitutional Law', 'Civil Procedure'")
    known_coverage_gap: Optional[str] = None
    evidence_reference: str = Field(..., description="Citation, Gazette notification, or Act number supporting existence")
    last_checked_date: str = Field(default="2026-10-17")

