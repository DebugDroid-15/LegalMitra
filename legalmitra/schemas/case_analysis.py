"""
LegalMitra Case Analysis Schema
Captures structured doctrinal legal analysis of Indian court decisions.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus
from legalmitra.schemas.legal_qa import EvidencePassage


class CaseAnalysisDocument(BaseModel):
    """
    Doctrinal case brief and analysis grounded in verified judgment text.
    """
    analysis_id: str = Field(..., description="Unique analysis identifier")
    case_id: str = Field(..., description="Case identifier or citation key")
    case_title: str = Field(..., description="Full cause title")
    court: CourtType = Field(default=CourtType.SUPREME_COURT)
    judgment_date: date
    bench_coram: List[str] = Field(default_factory=list)
    factual_matrix_summary: str = Field(..., min_length=20, description="Concise summary of material facts")
    issues_raised: List[str] = Field(..., min_length=1, description="Legal questions framed")
    appellant_arguments: List[str] = Field(default_factory=list)
    respondent_arguments: List[str] = Field(default_factory=list)
    ratio_decidendi: str = Field(..., min_length=20, description="Core legal rule established")
    obiter_dicta: Optional[str] = Field(default=None, description="Persuasive side remarks")
    precedential_value: str = Field(
        ...,
        description="e.g. 'Binding under Article 141 of Constitution', 'Division Bench Precedent'"
    )
    supporting_source_ids: List[str] = Field(..., min_length=1)
    evidence_passages: List[EvidencePassage] = Field(..., min_length=1)
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    legal_review_status: LegalReviewStatus = Field(
        default=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        description="Explicit review status."
    )

