"""
LegalMitra Failure Attribution & Traceability Module (Phase 31)
Implements reproducible failure taxonomy, structured evaluation tracing,
and diagnostic attribution across custom, unseen Indian legal inquiries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class FailureCategory(str, Enum):
    """Exhaustive failure taxonomy for Indian legal reasoning and RAG diagnosis."""
    QUESTION_UNDERSTANDING_FAILURE = "QUESTION_UNDERSTANDING_FAILURE"
    MISSING_FACTS_NOT_CLARIFIED = "MISSING_FACTS_NOT_CLARIFIED"
    JURISDICTION_SELECTION_FAILURE = "JURISDICTION_SELECTION_FAILURE"
    TEMPORAL_LAW_FAILURE = "TEMPORAL_LAW_FAILURE"
    RETRIEVAL_MISS = "RETRIEVAL_MISS"
    RETRIEVAL_RANKING_FAILURE = "RETRIEVAL_RANKING_FAILURE"
    SOURCE_QUALITY_FAILURE = "SOURCE_QUALITY_FAILURE"
    PROMPT_CONSTRUCTION_FAILURE = "PROMPT_CONSTRUCTION_FAILURE"
    MODEL_REASONING_FAILURE = "MODEL_REASONING_FAILURE"
    ANSWER_FORMAT_FAILURE = "ANSWER_FORMAT_FAILURE"
    UNSUPPORTED_CLAIM = "UNSUPPORTED_CLAIM"
    CITATION_ENTAILMENT_FAILURE = "CITATION_ENTAILMENT_FAILURE"
    ABSTENTION_FAILURE = "ABSTENTION_FAILURE"
    PRIVACY_OR_SECURITY_FAILURE = "PRIVACY_OR_SECURITY_FAILURE"
    EVALUATION_ORACLE_UNCERTAIN = "EVALUATION_ORACLE_UNCERTAIN"


@dataclass
class EvaluationTrace:
    """Detailed structured trace for a single evaluated legal question."""
    eval_id: str
    turn_id: str = "turn_1"
    original_query: str = ""
    normalized_query: str = ""
    detected_legal_issues: List[str] = field(default_factory=list)
    detected_missing_facts: Optional[str] = None
    selected_jurisdiction: Optional[str] = None
    effective_date: Optional[str] = None
    retrieved_chunk_ids: List[str] = field(default_factory=list)
    retrieved_sources_provenance: List[Dict[str, Any]] = field(default_factory=list)
    retrieval_scores: List[float] = field(default_factory=list)
    constructed_prompt_redacted: str = ""
    provider_model_id: str = "mock-nemotron-offline"
    generated_response: str = ""
    extracted_claims: List[Dict[str, Any]] = field(default_factory=list)
    citation_to_claim_relationships: List[Dict[str, Any]] = field(default_factory=list)
    verification_decisions: Dict[str, Any] = field(default_factory=dict)
    abstention_outcome: str = "not_abstained"
    latency_seconds: float = 0.0
    primary_failure_cause: Optional[FailureCategory] = None
    secondary_failure_causes: List[FailureCategory] = field(default_factory=list)
    passed: bool = True
    audit_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eval_id": self.eval_id,
            "turn_id": self.turn_id,
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "detected_legal_issues": self.detected_legal_issues,
            "detected_missing_facts": self.detected_missing_facts,
            "selected_jurisdiction": self.selected_jurisdiction,
            "effective_date": self.effective_date,
            "retrieved_chunk_ids": self.retrieved_chunk_ids,
            "retrieved_sources_provenance": self.retrieved_sources_provenance,
            "retrieval_scores": self.retrieval_scores,
            "constructed_prompt_redacted": self.constructed_prompt_redacted,
            "provider_model_id": self.provider_model_id,
            "generated_response": self.generated_response,
            "extracted_claims": self.extracted_claims,
            "citation_to_claim_relationships": self.citation_to_claim_relationships,
            "verification_decisions": self.verification_decisions,
            "abstention_outcome": self.abstention_outcome,
            "latency_seconds": self.latency_seconds,
            "primary_failure_cause": self.primary_failure_cause.value if self.primary_failure_cause else None,
            "secondary_failure_causes": [c.value for c in self.secondary_failure_causes],
            "passed": self.passed,
            "audit_notes": self.audit_notes,
        }


def attribute_failure(
    retrieval_success: bool,
    top_k_chunks: List[Any],
    answer_text: str,
    sufficiency_verdict: str,
    should_abstain: bool,
    missing_facts_prompt: Optional[str],
    unsupported_citations: List[str],
    unsupported_claims_count: int,
    forbidden_terms_found: List[str],
    privacy_violation: bool,
    prompt_injection_success: bool,
    is_multi_turn_miss: bool = False,
) -> tuple[Optional[FailureCategory], List[FailureCategory]]:
    """
    Deterministic rule-based classifier attributing failures to exact pipeline stages.
    """
    primary: Optional[FailureCategory] = None
    secondary: List[FailureCategory] = []

    # 1. Security / Privacy failures (Highest priority)
    if privacy_violation or prompt_injection_success:
        primary = FailureCategory.PRIVACY_OR_SECURITY_FAILURE
        return primary, secondary

    # 2. Temporal law failure (anachronisms)
    if forbidden_terms_found:
        primary = FailureCategory.TEMPORAL_LAW_FAILURE
        if not retrieval_success:
            secondary.append(FailureCategory.RETRIEVAL_MISS)
        return primary, secondary

    # 3. Missing facts that were not clarified
    if should_abstain and "temporal_fact_required" in sufficiency_verdict:
        if not missing_facts_prompt:
            primary = FailureCategory.MISSING_FACTS_NOT_CLARIFIED
            return primary, secondary

    # 4. Abstention failure
    if should_abstain and sufficiency_verdict == "sufficient":
        primary = FailureCategory.ABSTENTION_FAILURE
        if not retrieval_success:
            secondary.append(FailureCategory.RETRIEVAL_MISS)
        return primary, secondary

    # 5. Multi-turn anaphora / question understanding
    if is_multi_turn_miss:
        primary = FailureCategory.QUESTION_UNDERSTANDING_FAILURE
        secondary.append(FailureCategory.RETRIEVAL_MISS)
        return primary, secondary

    # 6. Retrieval miss
    if not retrieval_success and not should_abstain:
        if len(top_k_chunks) == 0:
            primary = FailureCategory.RETRIEVAL_MISS
        else:
            primary = FailureCategory.RETRIEVAL_RANKING_FAILURE
        return primary, secondary

    # 7. Unsupported claims & citation entailment
    if unsupported_citations:
        primary = FailureCategory.CITATION_ENTAILMENT_FAILURE
        if unsupported_claims_count > 0:
            secondary.append(FailureCategory.UNSUPPORTED_CLAIM)
        return primary, secondary

    if unsupported_claims_count > 0:
        primary = FailureCategory.UNSUPPORTED_CLAIM
        secondary.append(FailureCategory.MODEL_REASONING_FAILURE)
        return primary, secondary

    return primary, secondary
