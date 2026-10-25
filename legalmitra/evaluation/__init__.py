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
from legalmitra.evaluation.independent_evaluator import (
    IndependentClaimEvaluator,
    IndependentClaimEvaluationReport,
    PropositionEvaluation,
    PropositionVerdict,
    OverstatementSeverity,
)
from legalmitra.evaluation.completeness_auditor import (
    AnswerCompletenessAuditor,
    CompletenessAuditReport,
    CompletenessDimensionScore,
    CalibrationVerdict,
)
from legalmitra.evaluation.error_attribution import (
    ErrorTaxonomyCategory,
    PipelineStage,
    ErrorAttributionRecord,
    FailureAttributionReport,
    RootCauseAttributor,
    CATEGORY_STAGE_MAPPING,
)
from legalmitra.evaluation.differential_evaluator import (
    DifferentialEvaluator,
    DifferentialEvaluationReport,
    CaseComparison,
    RegressionSeverity,
)
from legalmitra.evaluation.release_gates import (
    ReleaseGateEvaluator,
    ReleaseGate,
    ReleaseEvaluationSummary,
    GateStatus,
)

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
    "IndependentClaimEvaluator",
    "IndependentClaimEvaluationReport",
    "PropositionEvaluation",
    "PropositionVerdict",
    "OverstatementSeverity",
    "AnswerCompletenessAuditor",
    "CompletenessAuditReport",
    "CompletenessDimensionScore",
    "CalibrationVerdict",
    "ErrorTaxonomyCategory",
    "PipelineStage",
    "ErrorAttributionRecord",
    "FailureAttributionReport",
    "RootCauseAttributor",
    "CATEGORY_STAGE_MAPPING",
    "DifferentialEvaluator",
    "DifferentialEvaluationReport",
    "CaseComparison",
    "RegressionSeverity",
    "ReleaseGateEvaluator",
    "ReleaseGate",
    "ReleaseEvaluationSummary",
    "GateStatus",
]
