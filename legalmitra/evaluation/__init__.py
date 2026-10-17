"""
Evaluation module exports for LegalMitra.
"""

from legalmitra.evaluation.dataset import DatasetManifest, EvaluationDataset
from legalmitra.evaluation.metrics import (
    calculate_citation_metrics,
    calculate_mrr,
    calculate_retrieval_recall,
    compute_category_statistics,
)
from legalmitra.evaluation.models import (
    AdversarialAudit,
    AnswerExpectedType,
    CaseEvaluationResult,
    CitationAudit,
    EvaluationCase,
    EvaluationCategory,
    EvaluationSummaryReport,
    SeverityLevel,
    TemporalAudit,
)
from legalmitra.evaluation.runner import LegalEvaluationRunner

__all__ = [
    "EvaluationCategory",
    "AnswerExpectedType",
    "SeverityLevel",
    "EvaluationCase",
    "CitationAudit",
    "TemporalAudit",
    "AdversarialAudit",
    "CaseEvaluationResult",
    "EvaluationSummaryReport",
    "DatasetManifest",
    "EvaluationDataset",
    "LegalEvaluationRunner",
    "calculate_mrr",
    "calculate_retrieval_recall",
    "calculate_citation_metrics",
    "compute_category_statistics",
]

