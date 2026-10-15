"""
LegalMitra Drafting Example Schema
Provides verified legal drafting templates (pleadings, affidavits, applications, notices)
with explicit statutory compliance notes under Indian law.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus
from legalmitra.schemas.legal_qa import EvidencePassage


class DraftingClause(BaseModel):
    """A specific clause in a legal draft with statutory rationale."""
    clause_heading: str = Field(...)
    clause_text: str = Field(...)
    is_mandatory: bool = Field(default=True)
    statutory_rationale: str = Field(..., description="Why this exact wording is required under Indian law")


class DraftingExampleDocument(BaseModel):
    """
    Standardized legal draft template with statutory grounding.
    """
    template_id: str = Field(..., description="e.g. 'DRAFT-BSA-SEC63-ELEC-CERT'")
    template_title: str = Field(...)
    category: str = Field(..., description="e.g. 'Affidavit', 'Statutory Certificate', 'Bail Application', 'Notice'")
    court_or_authority: str = Field(...)
    statutory_basis: str = Field(..., description="Statute and section mandating or enabling this draft")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    clauses: List[DraftingClause] = Field(..., min_length=1)
    full_draft_template: str = Field(..., min_length=50, description="Full draft text with placeholders like [DEPONENT NAME]")
    placeholders: List[str] = Field(default_factory=list, description="Variables to be filled in (e.g. ['[CASE NUMBER]', '[DEPONENT NAME]'])")
    drafting_pitfalls_to_avoid: List[str] = Field(default_factory=list)
    supporting_source_ids: List[str] = Field(..., min_length=1)
    evidence_passages: List[EvidencePassage] = Field(..., min_length=1)
    legal_review_status: LegalReviewStatus = Field(default=LegalReviewStatus.UNVERIFIED_AUTOMATED)

