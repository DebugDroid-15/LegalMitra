"""
Independent Legal Quality Assurance & Adversarial Evaluation Models.
Enforces strict schemas for benchmark cases, categories, expected answer types,
audit results, and release gate decision thresholds.
"""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EvaluationCategory(str, Enum):
    STATUTORY_PINPOINT = "statutory_pinpoint"
    TEMPORAL_APPLICABILITY = "temporal_applicability"
    PRECEDENT_AUTHORITY = "precedent_authority"
    PROCEDURAL_TIMELINE = "procedural_timeline"
    ADVERSARIAL_PREMISE = "adversarial_premise"
    MISSING_EVIDENCE = "missing_evidence"
    CONFLICTING_SOURCE = "conflicting_source"
    PROMPT_INJECTION = "prompt_injection"
    PRIVACY_PROTECTED = "privacy_protected"


class AnswerExpectedType(str, Enum):
    AFFIRMATIVE_STATUTE = "affirmative_statute"
    AFFIRMATIVE_JUDGMENT = "affirmative_judgment"
    AFFIRMATIVE_PROCEDURAL = "affirmative_procedural"
    ABSTENTION_INSUFFICIENT = "abstention_insufficient"
    ABSTENTION_TEMPORAL_FACT_REQUIRED = "abstention_temporal_fact_required"
    REFUTATION_FALSE_PREMISE = "refutation_false_premise"
    REFUSAL_INJECTION = "refusal_injection"
    REDACTION_PRIVACY = "redaction_privacy"


class SeverityLevel(str, Enum):
    CRITICAL = "critical"      # Block release immediately
    HIGH = "high"              # Requires fix or legal review
    MEDIUM = "medium"          # Procedural or format anomaly
    LOW = "low"                # Informational / minor phrasing


class EvaluationCase(BaseModel):
    eval_id: str = Field(..., description="Unique deterministic evaluation identifier, e.g. EVAL-STAT-001")
    category: EvaluationCategory = Field(..., description="Primary legal evaluation category")
    question: str = Field(..., description="Query / benchmark prompt presented to the retrieval & answering system")
    expected_type: AnswerExpectedType = Field(..., description="Expected behavior or response structure")
    target_act_or_case: str = Field(..., description="Target statutory act, case title, or legal topic")
    target_sections_or_paras: List[str] = Field(default_factory=list, description="Expected pinpoint references")
    as_of_date: Optional[str] = Field(None, description="Temporal anchor date YYYY-MM-DD if applicable")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter if applicable (e.g. IN, IN-DL)")
    court: Optional[str] = Field(None, description="Court filter if applicable (e.g. supreme_court, delhi_high_court)")
    golden_citations: List[str] = Field(default_factory=list, description="Required citation tokens that must appear")
    forbidden_terms: List[str] = Field(default_factory=list, description="Hallucinated or conflated terms that must NOT appear")
    should_abstain: bool = Field(False, description="Whether the system must report insufficient evidence or abstain")
    rationale: str = Field(..., description="Legal rationale explaining the benchmark ground truth")


class CitationAudit(BaseModel):
    total_citations_extracted: int = 0
    supported_citations_count: int = 0
    hallucinated_citations_count: int = 0
    citation_support_rate: float = 0.0
    citations_verified: List[str] = Field(default_factory=list)
    citations_unverified: List[str] = Field(default_factory=list)


class TemporalAudit(BaseModel):
    temporal_anchor: Optional[str] = None
    correctly_identified_regime: bool = True
    anachronistic_statute_invoked: bool = False
    details: Optional[str] = None


class AdversarialAudit(BaseModel):
    injected_override_detected: bool = False
    refusal_successful: bool = True
    privacy_violation_detected: bool = False
    notes: Optional[str] = None


class ClaimAudit(BaseModel):
    total_claims: int = 0
    grounded_claims: int = 0
    unsupported_claims: int = 0
    overstated_claims: int = 0
    outdated_claims: int = 0
    wrong_authority_claims: int = 0
    claim_support_rate: float = 1.0
    audit_notes: List[str] = Field(default_factory=list)


class CaseEvaluationResult(BaseModel):
    eval_id: str
    category: EvaluationCategory
    question: str
    passed: bool
    severity: Optional[SeverityLevel] = None
    retrieval_success: bool
    retrieved_chunk_ids: List[str] = Field(default_factory=list)
    top_k_count: int = 0
    answer_text: str
    sufficiency_verdict: str
    citation_audit: CitationAudit
    temporal_audit: TemporalAudit
    adversarial_audit: AdversarialAudit
    claim_audit: Optional[ClaimAudit] = None
    latency_seconds: float
    failure_reasons: List[str] = Field(default_factory=list)


class EvaluationSummaryReport(BaseModel):
    suite_version: str = "v1.0"
    total_cases: int
    passed_cases: int
    failed_cases: int
    overall_pass_rate: float
    retrieval_recall_at_k: float
    mean_reciprocal_rank: float
    citation_support_rate: float
    claim_support_rate: float = 1.0
    hallucination_rate: float
    abstention_precision: float
    temporal_correctness_rate: float
    precedent_validity_rate: float
    adversarial_robustness_rate: float
    privacy_compliance_rate: float
    release_gate_status: str  # GO, NO-GO, CONDITIONAL
    blocking_defects_count: int
    category_breakdown: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    case_results: List[CaseEvaluationResult] = Field(default_factory=list)

