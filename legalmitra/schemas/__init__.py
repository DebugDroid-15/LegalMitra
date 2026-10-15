"""
LegalMitra Schemas Package
Exports all standard schemas for the Indian legal dataset pipeline.
"""

from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.drafting_example import DraftingClause, DraftingExampleDocument
from legalmitra.schemas.evaluation import EvaluationQuestionDocument, EvaluationRubric
from legalmitra.schemas.judgment import (
    CaseHolding,
    JudgmentCitation,
    JudgmentDocument,
    JudgmentParagraph,
)
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument, ProceduralStep
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import (
    StatuteClause,
    StatuteDocument,
    StatuteExplanation,
    StatuteIllustration,
    StatuteProviso,
    StatuteSection,
    StatuteSubClause,
    StatuteSubSection,
)

__all__ = [
    "SourceRegistryRecord",
    "StatuteDocument",
    "StatuteSection",
    "StatuteSubSection",
    "StatuteClause",
    "StatuteSubClause",
    "StatuteProviso",
    "StatuteExplanation",
    "StatuteIllustration",
    "JudgmentDocument",
    "JudgmentParagraph",
    "JudgmentCitation",
    "CaseHolding",
    "EvidencePassage",
    "LegalQADocument",
    "CaseAnalysisDocument",
    "ProceduralGuidanceDocument",
    "ProceduralStep",
    "DraftingExampleDocument",
    "DraftingClause",
    "EvaluationQuestionDocument",
    "EvaluationRubric",
]

