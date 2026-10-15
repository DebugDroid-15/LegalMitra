"""
LegalMitra Evaluation Schema
Defines evaluation benchmarks for testing legal RAG and legal language models,
including negative constraints (hallucination traps, repealed laws) and golden citation rubrics.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus
from legalmitra.schemas.legal_qa import EvidencePassage


class EvaluationRubric(BaseModel):
    """Grading rubric for model output evaluation."""
    accuracy_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    statutory_citation_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    grounding_faithfulness_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    negative_constraint_penalty: float = Field(
        default=1.0,
        description="Penalty deducted if model hallucinates or cites repealed provisions"
    )


class EvaluationQuestionDocument(BaseModel):
    """
    Gold standard evaluation case for Indian legal reasoning.
    """
    eval_id: str = Field(..., description="Unique evaluation identifier, e.g. 'EVAL-BSA-S61-001'")
    question: str = Field(..., min_length=10)
    expected_answer: str = Field(..., min_length=20)
    target_statute_or_case: str = Field(..., description="Target Indian statute or case holding tested")
    golden_citations: List[str] = Field(..., min_length=1, description="Citations the model MUST provide")
    forbidden_terms_or_repealed_citations: List[str] = Field(
        default_factory=list,
        description="Repealed statutes (e.g. 'Indian Evidence Act 1872 s.65B') that must NOT be cited as current law"
    )
    rubric: EvaluationRubric = Field(default_factory=EvaluationRubric)
    supporting_source_ids: List[str] = Field(..., min_length=1)
    evidence_passages: List[EvidencePassage] = Field(..., min_length=1)
    legal_domain: str = Field(...)
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    legal_review_status: LegalReviewStatus = Field(default=LegalReviewStatus.UNVERIFIED_AUTOMATED)

