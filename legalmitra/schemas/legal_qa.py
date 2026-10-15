"""
LegalMitra Legal Q&A Schema
Enforces strict source grounding: every question-answer pair must link to an identified
source document ID and contain verifiable verbatim evidence passages.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus


class EvidencePassage(BaseModel):
    """
    Verbatim passage extracted from an authoritative source document.
    Serves as strict evidential anchor for any generated answer.
    """
    source_id: str = Field(..., description="Document ID in SourceRegistryRecord")
    section_or_para_ref: str = Field(..., description="e.g. 'Section 61(1)' or 'Paragraph 24'")
    verbatim_text: str = Field(..., description="Exact textual excerpt from the source document")
    page_number: Optional[int] = Field(default=None, ge=1)


class LegalQADocument(BaseModel):
    """
    Structured Legal Q&A instance for RAG evaluation and supervised instruction tuning.
    Never allows ungrounded legal assertions.
    """
    qa_id: str = Field(..., description="Unique QA identifier (e.g. 'QA-BSA-ELEC-REC-001')")
    question: str = Field(..., min_length=10, description="The legal query or user prompt")
    answer: str = Field(..., min_length=15, description="Source-grounded legal answer")
    supporting_source_ids: List[str] = Field(
        ...,
        min_length=1,
        description="List of SourceRegistryRecord document_ids grounding this answer"
    )
    evidence_passages: List[EvidencePassage] = Field(
        ...,
        min_length=1,
        description="Direct verbatim passages supporting all legal propositions in the answer"
    )
    legal_domain: str = Field(..., description="e.g. 'Criminal Law - Evidence', 'Constitutional Law - Fundamental Rights'")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    statutory_citations: List[str] = Field(default_factory=list, description="Statutory sections cited in answer")
    case_citations: List[str] = Field(default_factory=list, description="Court case citations cited in answer")
    flagged_unsupported: bool = Field(
        default=False,
        description="True if any claim in the answer lacks verified ground truth in evidence passages"
    )
    legal_disclaimer: str = Field(
        default="This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
        description="Mandatory Indian legal information disclaimer"
    )
    legal_review_status: LegalReviewStatus = Field(
        default=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        description="Explicit review status. Automated validation never establishes legal correctness."
    )

