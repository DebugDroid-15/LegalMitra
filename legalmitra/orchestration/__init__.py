"""
LegalMitra Orchestration Package (Phase 50)
Exposes the complete query orchestration pipeline, issue spotting,
fact analysis, evidence orchestration, claim validation, and decision policies.
"""

from legalmitra.orchestration.query_understanding import (
    LegalQueryAnalyzer,
    ParsedLegalQuery,
)
from legalmitra.orchestration.evidence_orchestrator import (
    EvidenceItem,
    OrchestratedEvidenceSet,
    UnifiedEvidenceOrchestrator,
)
from legalmitra.orchestration.fact_analyzer import (
    FactAnalysisReport,
    FactClassification,
    FactNode,
    FactSensitiveAnalyzer,
    IRACUnit,
)
from legalmitra.orchestration.answer_assembler import (
    AssembledAnswer,
    AssembledClaim,
    EvidenceTraceableAnswerAssembler,
)
from legalmitra.orchestration.decision_policy import (
    LegalDecisionPolicy,
    LegalResponseState,
    PolicyEvaluationResult,
)
from legalmitra.orchestration.pipeline import (
    LegalQueryPipeline,
    OrchestratedLegalResponse,
    PipelineExecutionTelemetry,
)

__all__ = [
    "LegalQueryAnalyzer",
    "ParsedLegalQuery",
    "EvidenceItem",
    "OrchestratedEvidenceSet",
    "UnifiedEvidenceOrchestrator",
    "FactAnalysisReport",
    "FactClassification",
    "FactNode",
    "FactSensitiveAnalyzer",
    "IRACUnit",
    "AssembledAnswer",
    "AssembledClaim",
    "EvidenceTraceableAnswerAssembler",
    "LegalDecisionPolicy",
    "LegalResponseState",
    "PolicyEvaluationResult",
    "LegalQueryPipeline",
    "OrchestratedLegalResponse",
    "PipelineExecutionTelemetry",
]

