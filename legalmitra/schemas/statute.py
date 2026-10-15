"""
LegalMitra Statute Schema
Preserves exact statutory hierarchy, numbering, provisos, explanations, and citations
peculiar to the Indian legislative drafting tradition.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus


class StatuteSubClause(BaseModel):
    """Sub-clause such as (i), (ii) within a clause."""
    sub_clause_number: str = Field(..., description="e.g. '(i)' or '(ii)'")
    text: str = Field(..., description="Verbatim text of the sub-clause")


class StatuteClause(BaseModel):
    """Clause such as (a), (b), (c) within a subsection."""
    clause_number: str = Field(..., description="e.g. '(a)' or '(b)'")
    text: str = Field(..., description="Verbatim text of the clause")
    sub_clauses: List[StatuteSubClause] = Field(default_factory=list)


class StatuteSubSection(BaseModel):
    """Sub-section such as (1), (2), (3) within a section."""
    sub_section_number: str = Field(..., description="e.g. '(1)', '(2)'")
    text: str = Field(..., description="Verbatim text of the subsection")
    clauses: List[StatuteClause] = Field(default_factory=list)


class StatuteProviso(BaseModel):
    """Statutory proviso ('Provided that...', 'Provided further that...')."""
    proviso_index: int = Field(default=1, description="Index of proviso within section")
    text: str = Field(..., description="Verbatim text of proviso starting with 'Provided that...'")


class StatuteExplanation(BaseModel):
    """Statutory explanation ('Explanation.—' or 'Explanation 1.—')."""
    explanation_identifier: str = Field(default="Explanation", description="e.g. 'Explanation' or 'Explanation 1'")
    text: str = Field(..., description="Verbatim text of the explanation")


class StatuteIllustration(BaseModel):
    """Statutory illustration provided by Parliament to elucidate meaning."""
    illustration_identifier: str = Field(..., description="e.g. 'Illustration (a)'")
    text: str = Field(..., description="Verbatim text of the illustration")


class StatuteSection(BaseModel):
    """
    Normalized representation of a single statutory section.
    Maintains exact wording, section numbering, and internal subdivisions.
    """
    section_id: str = Field(..., description="Unique section key, e.g. 'BSA-2023-SEC-61'")
    source_id: str = Field(..., description="Foreign key to SourceRegistryRecord.document_id")
    act_title: str = Field(..., description="Short title of the Act (e.g. 'Bharatiya Sakshya Adhiniyam, 2023')")
    act_number: Optional[str] = Field(default=None, description="e.g. 'Act No. 47 of 2023'")
    chapter_number: Optional[str] = Field(default=None, description="e.g. 'Chapter V'")
    chapter_title: Optional[str] = Field(default=None, description="e.g. 'Of Documentary Evidence'")
    section_number: str = Field(..., description="e.g. '61' or '437A'")
    section_title: str = Field(..., description="Marginal heading / section title (e.g. 'Admissibility of electronic records')")
    full_verbatim_text: str = Field(..., description="Exact verbatim full text of the section")
    subsections: List[StatuteSubSection] = Field(default_factory=list)
    provisos: List[StatuteProviso] = Field(default_factory=list)
    explanations: List[StatuteExplanation] = Field(default_factory=list)
    illustrations: List[StatuteIllustration] = Field(default_factory=list)
    source_page_start: Optional[int] = Field(default=None, ge=1)
    source_page_end: Optional[int] = Field(default=None, ge=1)
    legal_review_status: LegalReviewStatus = Field(
        default=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        description="Explicit review status. Never assumed legally correct without human verification."
    )


class StatuteDocument(BaseModel):
    """
    Top-level normalized statute containing metadata and parsed sections.
    """
    source_id: str = Field(..., description="Foreign key to SourceRegistryRecord")
    act_title: str = Field(...)
    act_number: Optional[str] = None
    jurisdiction: Jurisdiction = Jurisdiction.INDIA_CENTRAL
    enactment_date: date
    effective_date: Optional[date] = None
    preamble: Optional[str] = None
    sections: List[StatuteSection] = Field(default_factory=list)
    legal_review_status: LegalReviewStatus = LegalReviewStatus.UNVERIFIED_AUTOMATED

