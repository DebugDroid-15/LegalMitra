"""
LegalMitra Judgment Schema
Models Indian case law from the Supreme Court, High Courts, and Tribunals with
numbered paragraph fidelity, bench coram, ratio decidendi, and privacy redaction compliance.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus


class JudgmentParagraph(BaseModel):
    """
    Exact verbatim paragraph from an Indian court judgment with paragraph number and page.
    """
    paragraph_number: int = Field(..., ge=1, description="Sequential paragraph number as numbered by court")
    verbatim_text: str = Field(..., description="Unmodified paragraph text")
    page_number: Optional[int] = Field(default=None, ge=1)
    is_heading_or_transition: bool = Field(default=False)


class JudgmentCitation(BaseModel):
    """
    Law report or neutral citation referenced in or belonging to this judgment.
    """
    citation_text: str = Field(..., description="e.g. '(2017) 10 SCC 1' or '2023 INSC 582'")
    reporter: Optional[str] = Field(default=None, description="e.g. 'SCC', 'AIR', 'SCR', 'INSC'")
    year: Optional[int] = Field(default=None)


class CaseHolding(BaseModel):
    """
    Formal holding of the court on a specific issue.
    """
    issue_number: int = Field(default=1)
    issue_text: str = Field(..., description="The question of law framed by the court")
    holding_summary: str = Field(..., description="The definitive determination on that question")
    supporting_paragraph_numbers: List[int] = Field(default_factory=list)


class JudgmentDocument(BaseModel):
    """
    Normalized representation of an Indian Court Judgment.
    """
    judgment_id: str = Field(..., description="Unique judgment identifier, e.g. 'IND-SC-2017-PUTTASWAMY'")
    source_id: str = Field(..., description="Foreign key to SourceRegistryRecord")
    case_title: str = Field(..., description="e.g. 'Justice K.S. Puttaswamy (Retd.) and Another v. Union of India and Others'")
    case_number: Optional[str] = Field(default=None, description="e.g. 'Writ Petition (Civil) No. 494 of 2012'")
    court: CourtType = Field(default=CourtType.SUPREME_COURT)
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    bench_coram: List[str] = Field(..., description="Names of the presiding Judges on the Bench")
    judgment_date: date = Field(...)
    citations: List[JudgmentCitation] = Field(default_factory=list)
    paragraphs: List[JudgmentParagraph] = Field(default_factory=list)
    issues_framed: List[str] = Field(default_factory=list)
    holdings: List[CaseHolding] = Field(default_factory=list)
    ratio_decidendi: Optional[str] = Field(
        default=None,
        description="The binding principle of law upon which the decision is founded"
    )
    obiter_dicta: Optional[str] = Field(
        default=None,
        description="Incidental legal observations made by the court not essential to the disposition"
    )
    final_disposition: Optional[str] = Field(
        default=None,
        description="e.g. 'Petition allowed', 'Appeals dismissed', 'Referred to a 9-Judge Constitution Bench'"
    )
    is_victim_identity_redacted: bool = Field(
        default=True,
        description="Flag certifying compliance with Section 33(7) POCSO, Section 74 JJ Act, and Section 72 BNS"
    )
    legal_review_status: LegalReviewStatus = Field(
        default=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        description="Explicit review status. Automated validation never establishes legal correctness."
    )

