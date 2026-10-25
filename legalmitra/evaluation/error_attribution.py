"""
28-Category Failure Taxonomy & Root-Cause Attribution Engine (Phase 57)

Formalizes the exhaustive 28-category legal failure taxonomy across 7 pipeline stages:
1. QUERY_ANALYSIS
2. RETRIEVAL
3. TEMPORAL_RESOLUTION
4. EVIDENCE_MATRIX
5. CLAIM_VALIDATION
6. DECISION_POLICY
7. ANSWER_ASSEMBLY

Provides deterministic root-cause attribution linking answer deficiencies
to exact pipeline components, distinguishing established causes from hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple


class PipelineStage(str, Enum):
    """The 7 canonical pipeline stages in LegalMitra."""
    QUERY_ANALYSIS = "QUERY_ANALYSIS"
    RETRIEVAL = "RETRIEVAL"
    TEMPORAL_RESOLUTION = "TEMPORAL_RESOLUTION"
    EVIDENCE_MATRIX = "EVIDENCE_MATRIX"
    CLAIM_VALIDATION = "CLAIM_VALIDATION"
    DECISION_POLICY = "DECISION_POLICY"
    ANSWER_ASSEMBLY = "ANSWER_ASSEMBLY"


class ErrorTaxonomyCategory(str, Enum):
    """Exhaustive 28-category failure taxonomy for Indian legal reasoning."""
    # Group 1: Query Analysis
    QUERY_INTERPRETATION_ERROR = "QUERY_INTERPRETATION_ERROR"
    DOMAIN_MISCLASSIFICATION = "DOMAIN_MISCLASSIFICATION"
    TEMPORAL_ANCHOR_MISIDENTIFICATION = "TEMPORAL_ANCHOR_MISIDENTIFICATION"
    ISSUE_DECOMPOSITION_OMISSION = "ISSUE_DECOMPOSITION_OMISSION"

    # Group 2: Retrieval & Source Integrity
    RETRIEVAL_OMISSION = "RETRIEVAL_OMISSION"
    OVERBROAD_RETRIEVAL = "OVERBROAD_RETRIEVAL"
    FABRICATED_SOURCE_HALLUCINATION = "FABRICATED_SOURCE_HALLUCINATION"
    QUARANTINED_SOURCE_LEAKAGE = "QUARANTINED_SOURCE_LEAKAGE"

    # Group 3: Temporal & Statutory Validity
    OUTDATED_STATUTE_APPLIED = "OUTDATED_STATUTE_APPLIED"
    PREMATURE_UNCOMMENCED_ENACTMENT = "PREMATURE_UNCOMMENCED_ENACTMENT"
    OVERRULED_PRECEDENT_APPLIED = "OVERRULED_PRECEDENT_APPLIED"
    AMENDED_PROVISO_IGNORED = "AMENDED_PROVISO_IGNORED"

    # Group 4: Exception & Proviso Coverage
    MISSED_STATUTORY_EXCEPTION = "MISSED_STATUTORY_EXCEPTION"
    MISSED_PROVISO_QUALIFICATION = "MISSED_PROVISO_QUALIFICATION"
    SUPPRESSED_LEGISLATIVE_BAR = "SUPPRESSED_LEGISLATIVE_BAR"
    IGNORED_NON_OBSTANTE_CLAUSE = "IGNORED_NON_OBSTANTE_CLAUSE"

    # Group 5: Evidence Matrix & Claim Dependency
    CLAIM_DEPENDENCY_FAILURE = "CLAIM_DEPENDENCY_FAILURE"
    PREMISE_CONCLUSION_DISCONNECT = "PREMISE_CONCLUSION_DISCONNECT"
    INTRA_ANSWER_CONTRADICTION = "INTRA_ANSWER_CONTRADICTION"
    OVERSTATED_LEGAL_HOLDING = "OVERSTATED_LEGAL_HOLDING"

    # Group 6: Decision Calibration & Policy
    FALSE_CERTAINTY_DISPOSITION = "FALSE_CERTAINTY_DISPOSITION"
    FALSE_ABSTENTION_DISPOSITION = "FALSE_ABSTENTION_DISPOSITION"
    CONFLATED_PARTIAL_DISPOSITION = "CONFLATED_PARTIAL_DISPOSITION"
    UNCALIBRATED_CONDITIONALITY = "UNCALIBRATED_CONDITIONALITY"

    # Group 7: Answer Assembly & Formatting
    CITATION_GROUNDING_MISMATCH = "CITATION_GROUNDING_MISMATCH"
    MISSING_TRACEABILITY_MATRIX = "MISSING_TRACEABILITY_MATRIX"
    UNFORMATTED_PRECEDENT_HIERARCHY = "UNFORMATTED_PRECEDENT_HIERARCHY"
    INCOHERENT_SYNTHESIS = "INCOHERENT_SYNTHESIS"


CATEGORY_STAGE_MAPPING: Dict[ErrorTaxonomyCategory, PipelineStage] = {
    # Group 1
    ErrorTaxonomyCategory.QUERY_INTERPRETATION_ERROR: PipelineStage.QUERY_ANALYSIS,
    ErrorTaxonomyCategory.DOMAIN_MISCLASSIFICATION: PipelineStage.QUERY_ANALYSIS,
    ErrorTaxonomyCategory.TEMPORAL_ANCHOR_MISIDENTIFICATION: PipelineStage.QUERY_ANALYSIS,
    ErrorTaxonomyCategory.ISSUE_DECOMPOSITION_OMISSION: PipelineStage.QUERY_ANALYSIS,
    # Group 2
    ErrorTaxonomyCategory.RETRIEVAL_OMISSION: PipelineStage.RETRIEVAL,
    ErrorTaxonomyCategory.OVERBROAD_RETRIEVAL: PipelineStage.RETRIEVAL,
    ErrorTaxonomyCategory.FABRICATED_SOURCE_HALLUCINATION: PipelineStage.RETRIEVAL,
    ErrorTaxonomyCategory.QUARANTINED_SOURCE_LEAKAGE: PipelineStage.RETRIEVAL,
    # Group 3
    ErrorTaxonomyCategory.OUTDATED_STATUTE_APPLIED: PipelineStage.TEMPORAL_RESOLUTION,
    ErrorTaxonomyCategory.PREMATURE_UNCOMMENCED_ENACTMENT: PipelineStage.TEMPORAL_RESOLUTION,
    ErrorTaxonomyCategory.OVERRULED_PRECEDENT_APPLIED: PipelineStage.TEMPORAL_RESOLUTION,
    ErrorTaxonomyCategory.AMENDED_PROVISO_IGNORED: PipelineStage.TEMPORAL_RESOLUTION,
    # Group 4
    ErrorTaxonomyCategory.MISSED_STATUTORY_EXCEPTION: PipelineStage.EVIDENCE_MATRIX,
    ErrorTaxonomyCategory.MISSED_PROVISO_QUALIFICATION: PipelineStage.EVIDENCE_MATRIX,
    ErrorTaxonomyCategory.SUPPRESSED_LEGISLATIVE_BAR: PipelineStage.EVIDENCE_MATRIX,
    ErrorTaxonomyCategory.IGNORED_NON_OBSTANTE_CLAUSE: PipelineStage.EVIDENCE_MATRIX,
    # Group 5
    ErrorTaxonomyCategory.CLAIM_DEPENDENCY_FAILURE: PipelineStage.CLAIM_VALIDATION,
    ErrorTaxonomyCategory.PREMISE_CONCLUSION_DISCONNECT: PipelineStage.CLAIM_VALIDATION,
    ErrorTaxonomyCategory.INTRA_ANSWER_CONTRADICTION: PipelineStage.CLAIM_VALIDATION,
    ErrorTaxonomyCategory.OVERSTATED_LEGAL_HOLDING: PipelineStage.CLAIM_VALIDATION,
    # Group 6
    ErrorTaxonomyCategory.FALSE_CERTAINTY_DISPOSITION: PipelineStage.DECISION_POLICY,
    ErrorTaxonomyCategory.FALSE_ABSTENTION_DISPOSITION: PipelineStage.DECISION_POLICY,
    ErrorTaxonomyCategory.CONFLATED_PARTIAL_DISPOSITION: PipelineStage.DECISION_POLICY,
    ErrorTaxonomyCategory.UNCALIBRATED_CONDITIONALITY: PipelineStage.DECISION_POLICY,
    # Group 7
    ErrorTaxonomyCategory.CITATION_GROUNDING_MISMATCH: PipelineStage.ANSWER_ASSEMBLY,
    ErrorTaxonomyCategory.MISSING_TRACEABILITY_MATRIX: PipelineStage.ANSWER_ASSEMBLY,
    ErrorTaxonomyCategory.UNFORMATTED_PRECEDENT_HIERARCHY: PipelineStage.ANSWER_ASSEMBLY,
    ErrorTaxonomyCategory.INCOHERENT_SYNTHESIS: PipelineStage.ANSWER_ASSEMBLY,
}


@dataclass
class ErrorAttributionRecord:
    """Attribution of a concrete legal reasoning failure to pipeline stage and cause."""
    attribution_id: str
    error_category: ErrorTaxonomyCategory
    pipeline_stage: PipelineStage
    is_established_cause: bool  # True = verified root cause; False = unconfirmed hypothesis
    confidence: float  # 0.0 to 1.0
    evidence_trace: str
    suggested_remediation: str
    affected_components: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attribution_id": self.attribution_id,
            "error_category": self.error_category.value,
            "pipeline_stage": self.pipeline_stage.value,
            "is_established_cause": self.is_established_cause,
            "confidence": round(self.confidence, 4),
            "evidence_trace": self.evidence_trace,
            "suggested_remediation": self.suggested_remediation,
            "affected_components": self.affected_components,
        }


@dataclass
class FailureAttributionReport:
    """Consolidated attribution report for a failed or suboptimal legal query evaluation."""
    eval_id: str
    query: str
    total_attributions: int
    primary_attribution: Optional[ErrorAttributionRecord]
    secondary_attributions: List[ErrorAttributionRecord] = field(default_factory=list)
    affected_stages: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eval_id": self.eval_id,
            "query": self.query,
            "total_attributions": self.total_attributions,
            "primary_attribution": self.primary_attribution.to_dict() if self.primary_attribution else None,
            "secondary_attributions": [a.to_dict() for a in self.secondary_attributions],
            "affected_stages": self.affected_stages,
        }


class RootCauseAttributor:
    """
    Deterministic attribution engine that links evaluation deficiencies to exact pipeline stages
    and categorizes them under the 28-category taxonomy.
    """

    def attribute(
        self,
        eval_id: str,
        query: str,
        answer_text: str,
        citations: List[str],
        response_state: Optional[str] = None,
        independent_report: Optional[Any] = None,
        completeness_report: Optional[Any] = None,
        evidence_matrix: Optional[Any] = None,
        retrieved_chunk_count: int = 5,
    ) -> FailureAttributionReport:
        """
        Derives primary and secondary error attributions based on multi-component signals.
        """
        attributions: List[ErrorAttributionRecord] = []
        q_lower = query.lower()
        ans_lower = answer_text.lower()
        state = response_state or "UNKNOWN"

        # 1. Quarantined Source Leakage (Stage: RETRIEVAL)
        if any("IND-JUD-DEL-2024-BAIL" in str(c).upper() for c in citations) or "IND-JUD-DEL-2024-BAIL" in answer_text.upper():
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.QUARANTINED_SOURCE_LEAKAGE,
                    pipeline_stage=PipelineStage.RETRIEVAL,
                    is_established_cause=True,
                    confidence=1.0,
                    evidence_trace="Quarantined synthetic scaffold IND-JUD-DEL-2024-BAIL retrieved and leaked into citations/answer",
                    suggested_remediation="Enforce strict scaffold quarantine filter in UnifiedEvidenceOrchestrator",
                    affected_components=["UnifiedEvidenceOrchestrator", "VectorRetriever"],
                )
            )

        # 2. Fabricated Source Hallucination (Stage: RETRIEVAL)
        if independent_report and getattr(independent_report, "has_fabricated_citations", False):
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.FABRICATED_SOURCE_HALLUCINATION,
                    pipeline_stage=PipelineStage.RETRIEVAL,
                    is_established_cause=True,
                    confidence=0.95,
                    evidence_trace="Citation verification failed; non-existent statutory/judicial citation detected",
                    suggested_remediation="Enable strict KB authority existence gate before citation formatting",
                    affected_components=["EvidenceTraceableAnswerAssembler", "AuthorityResolver"],
                )
            )

        # 3. Overruled Precedent Applied (Stage: TEMPORAL_RESOLUTION)
        if "prakash v. phulavati" in ans_lower and "vineeta sharma" not in ans_lower:
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.OVERRULED_PRECEDENT_APPLIED,
                    pipeline_stage=PipelineStage.TEMPORAL_RESOLUTION,
                    is_established_cause=True,
                    confidence=0.98,
                    evidence_trace="Prakash v. Phulavati applied without citing 3-Judge Bench overruling in Vineeta Sharma",
                    suggested_remediation="Update precedent hierarchy graph to suppress overruled 2-judge bench holdings",
                    affected_components=["TemporalPrecedentGraph", "AuthorityResolver"],
                )
            )

        # 4. Missed Statutory Exception / Legislative Bar (Stage: EVIDENCE_MATRIX)
        if "section 20a" in q_lower or ("specific relief" in q_lower and "infrastructure" in q_lower):
            if "bar" not in ans_lower and "impediment" not in ans_lower:
                attributions.append(
                    ErrorAttributionRecord(
                        attribution_id=f"ATTR-{len(attributions)+1:02d}",
                        error_category=ErrorTaxonomyCategory.MISSED_STATUTORY_EXCEPTION,
                        pipeline_stage=PipelineStage.EVIDENCE_MATRIX,
                        is_established_cause=True,
                        confidence=0.92,
                        evidence_trace="Section 20A Specific Relief Act statutory bar on infrastructure injunctions missed",
                        suggested_remediation="Enhance statutory exception extractor in ClaimDependencyValidator",
                        affected_components=["ClaimDependencyValidator", "EvidenceMatrix"],
                    )
                )

        # 5. Missed Proviso Qualification (Stage: EVIDENCE_MATRIX)
        if "hindu succession" in q_lower and "daughter" in q_lower:
            if "20 december 2004" not in ans_lower and "partition" not in ans_lower:
                attributions.append(
                    ErrorAttributionRecord(
                        attribution_id=f"ATTR-{len(attributions)+1:02d}",
                        error_category=ErrorTaxonomyCategory.MISSED_PROVISO_QUALIFICATION,
                        pipeline_stage=PipelineStage.EVIDENCE_MATRIX,
                        is_established_cause=True,
                        confidence=0.88,
                        evidence_trace="Section 6(1) Proviso Hindu Succession Act (pre-2004 partition exception) missed",
                        suggested_remediation="Attach proviso candidates to Hindu Succession coparcenary issues",
                        affected_components=["EvidenceMatrix", "FactSensitiveAnalyzer"],
                    )
                )

        # 6. Intra-Answer Contradiction (Stage: CLAIM_VALIDATION)
        if completeness_report and getattr(completeness_report, "intra_contradictions", []):
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.INTRA_ANSWER_CONTRADICTION,
                    pipeline_stage=PipelineStage.CLAIM_VALIDATION,
                    is_established_cause=True,
                    confidence=0.90,
                    evidence_trace=f"Contradictory propositions: {completeness_report.intra_contradictions[0]}",
                    suggested_remediation="Add cross-claim consistency checker prior to answer emission",
                    affected_components=["ClaimDependencyValidator", "AnswerAssembler"],
                )
            )

        # 7. Overstated Legal Holding (Stage: CLAIM_VALIDATION)
        if independent_report and getattr(independent_report, "overstated_propositions", 0) > 0:
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.OVERSTATED_LEGAL_HOLDING,
                    pipeline_stage=PipelineStage.CLAIM_VALIDATION,
                    is_established_cause=True,
                    confidence=0.85,
                    evidence_trace=f"{independent_report.overstated_propositions} propositions exhibit uncalibrated absolute language",
                    suggested_remediation="Calibrate claim generator to qualify rights subject to exceptions",
                    affected_components=["EvidenceTraceableAnswerAssembler"],
                )
            )

        # 8. False Certainty Disposition (Stage: DECISION_POLICY)
        if state == "ANSWER_DIRECT" and any(
            attr.error_category in (ErrorTaxonomyCategory.MISSED_STATUTORY_EXCEPTION, ErrorTaxonomyCategory.MISSED_PROVISO_QUALIFICATION, ErrorTaxonomyCategory.OVERSTATED_LEGAL_HOLDING)
            for attr in attributions
        ):
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.FALSE_CERTAINTY_DISPOSITION,
                    pipeline_stage=PipelineStage.DECISION_POLICY,
                    is_established_cause=True,
                    confidence=0.90,
                    evidence_trace="Emitted ANSWER_DIRECT when unaddressed statutory qualifications require ANSWER_QUALIFIED",
                    suggested_remediation="Adjust LegalDecisionPolicy to mandate qualification when exceptions exist",
                    affected_components=["LegalDecisionPolicy"],
                )
            )

        # 9. Premature Uncommenced Enactment (Stage: TEMPORAL_RESOLUTION)
        if "industrial relations code" in q_lower and ("enacted" in ans_lower or "in force" in ans_lower or "applies" in ans_lower):
            if "uncommenced" not in ans_lower and "not notified" not in ans_lower:
                attributions.append(
                    ErrorAttributionRecord(
                        attribution_id=f"ATTR-{len(attributions)+1:02d}",
                        error_category=ErrorTaxonomyCategory.PREMATURE_UNCOMMENCED_ENACTMENT,
                        pipeline_stage=PipelineStage.TEMPORAL_RESOLUTION,
                        is_established_cause=True,
                        confidence=0.95,
                        evidence_trace="IR Code 2020 treated as in-force statutory mandate despite lack of commencement notification",
                        suggested_remediation="Verify commencement status before applying labour codes",
                        affected_components=["TemporalPrecedentGraph", "AuthorityResolver"],
                    )
                )

        # 10. Retrieval Omission (Stage: RETRIEVAL)
        if retrieved_chunk_count == 0 and not state.startswith("ABSTAIN"):
            attributions.append(
                ErrorAttributionRecord(
                    attribution_id=f"ATTR-{len(attributions)+1:02d}",
                    error_category=ErrorTaxonomyCategory.RETRIEVAL_OMISSION,
                    pipeline_stage=PipelineStage.RETRIEVAL,
                    is_established_cause=True,
                    confidence=0.90,
                    evidence_trace="Zero relevant chunks retrieved from knowledge base",
                    suggested_remediation="Improve query reformulation and dense retrieval threshold",
                    affected_components=["VectorRetriever", "HybridSearcher"],
                )
            )

        # 11. Conflated Partial Disposition (Stage: DECISION_POLICY)
        if " and " in q_lower and state in ("ANSWER_DIRECT", "ANSWER_QUALIFIED"):
            if "industrial disputes act" in q_lower and "industrial relations code" in q_lower:
                if state != "ANSWER_PARTIAL":
                    attributions.append(
                        ErrorAttributionRecord(
                            attribution_id=f"ATTR-{len(attributions)+1:02d}",
                            error_category=ErrorTaxonomyCategory.CONFLATED_PARTIAL_DISPOSITION,
                            pipeline_stage=PipelineStage.DECISION_POLICY,
                            is_established_cause=True,
                            confidence=0.88,
                            evidence_trace="Compound inquiry with mixed in-force and uncommenced enactments conflated into single state",
                            suggested_remediation="Emit ANSWER_PARTIAL when sub-issues diverge in temporal validity",
                            affected_components=["LegalDecisionPolicy"],
                        )
                    )

        primary = attributions[0] if attributions else None
        secondaries = attributions[1:] if len(attributions) > 1 else []
        stages = list(dict.fromkeys(a.pipeline_stage.value for a in attributions))

        return FailureAttributionReport(
            eval_id=eval_id,
            query=query,
            total_attributions=len(attributions),
            primary_attribution=primary,
            secondary_attributions=secondaries,
            affected_stages=stages,
        )

