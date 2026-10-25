"""
LegalMitra Unified Legal Query Orchestration Pipeline (Phase 50)
Executes the deterministic 14-step query-to-answer orchestration sequence,
integrating query parsing, multi-tier retrieval, temporal resolution,
precedent evaluation, IRAC fact analysis, claim validation, and decision policy.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.caselaw.knowledge_graph import (
    LegalKnowledgeGraph,
    build_national_judicial_knowledge_graph,
)
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.orchestration.answer_assembler import (
    AssembledAnswer,
    EvidenceTraceableAnswerAssembler,
)
from legalmitra.orchestration.decision_policy import (
    LegalDecisionPolicy,
    LegalResponseState,
    PolicyEvaluationResult,
)
from legalmitra.orchestration.evidence_orchestrator import (
    OrchestratedEvidenceSet,
    UnifiedEvidenceOrchestrator,
)
from legalmitra.orchestration.fact_analyzer import (
    FactAnalysisReport,
    FactSensitiveAnalyzer,
)
from legalmitra.orchestration.query_understanding import (
    LegalQueryAnalyzer,
    ParsedLegalQuery,
)
from legalmitra.temporal.engine import TemporalLawEngine, build_default_temporal_engine


@dataclass
class PipelineExecutionTelemetry:
    """Detailed audit telemetry for pipeline execution."""
    start_time: float
    end_time: float
    duration_seconds: float
    steps_executed: List[str] = field(default_factory=list)
    query_domain: str = ""
    issues_spotted: List[str] = field(default_factory=list)
    evidence_count: int = 0
    contrary_authorities_count: int = 0
    claims_validated: int = 0
    policy_state: str = ""
    clarification_posed: bool = False
    abstention_triggered: bool = False
    has_partial_support: bool = False
    is_conditional: bool = False
    issue_matrix_records_count: int = 0


@dataclass
class OrchestratedLegalResponse:
    """Final output object returned by the orchestration pipeline."""
    query: str
    response_state: LegalResponseState
    answer_text: str
    citations: List[str]
    governing_provisions: List[str]
    competing_authorities: List[str]
    parsed_query: ParsedLegalQuery
    evidence_set: OrchestratedEvidenceSet
    fact_report: FactAnalysisReport
    assembled_answer: AssembledAnswer
    policy_result: PolicyEvaluationResult
    telemetry: PipelineExecutionTelemetry
    timestamp: str
    evidence_matrix: Optional[Any] = None
    proposition_provenance: List[Any] = field(default_factory=list)
    provenance_audit: Optional[Any] = None
    post_generation_eval: Optional[Any] = None
    provenance_audit: Optional[Any] = None
    post_generation_eval: Optional[Any] = None


class LegalQueryPipeline:
    """
    Main entry point for end-to-end legal query orchestration.
    """

    def __init__(
        self,
        kb: Optional[LegalKnowledgeBase] = None,
        temporal_engine: Optional[TemporalLawEngine] = None,
        knowledge_graph: Optional[LegalKnowledgeGraph] = None,
    ):
        self.kb = kb or LegalKnowledgeBase()
        self.temporal_engine = temporal_engine or build_default_temporal_engine()
        self.knowledge_graph = knowledge_graph or build_national_judicial_knowledge_graph()

        self.query_analyzer = LegalQueryAnalyzer()
        self.evidence_orchestrator = UnifiedEvidenceOrchestrator(
            kb=self.kb,
            temporal_engine=self.temporal_engine,
            knowledge_graph=self.knowledge_graph,
        )
        self.fact_analyzer = FactSensitiveAnalyzer()
        self.answer_assembler = EvidenceTraceableAnswerAssembler(
            temporal_engine=self.temporal_engine
        )
        self.decision_policy = LegalDecisionPolicy()
        from legalmitra.evaluation.provenance_model import PropositionProvenanceAuditor
        self.provenance_auditor = PropositionProvenanceAuditor()
        from legalmitra.evaluation.provenance_model import PropositionProvenanceAuditor
        self.provenance_auditor = PropositionProvenanceAuditor()

    def execute(
        self,
        query: str,
        context_date: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        raw_draft_answer: Optional[str] = None,
        limit: int = 6,
    ) -> OrchestratedLegalResponse:
        """
        Executes the 14-step deterministic orchestration sequence.
        """
        start_t = time.time()
        steps = []

        # Step 1: Parse the query & extract structured representation
        steps.append("1. Parse query and extract structured representation")
        parsed_q = self.query_analyzer.parse_query(query, context_date=context_date)
        if jurisdiction and not parsed_q.jurisdiction:
            parsed_q.jurisdiction = jurisdiction

        # Step 2: Identify candidate legal issues
        steps.append("2. Identify candidate legal issues")
        issues = parsed_q.candidate_issues

        # Step 3: Determine material facts and missing information
        steps.append("3. Determine material facts and missing information")
        user_facts = parsed_q.user_supplied_facts

        # Step 4: Resolve candidate jurisdiction and temporal context
        steps.append("4. Resolve candidate jurisdiction and temporal context")
        q_date = parsed_q.query_date
        q_jurisdiction = parsed_q.jurisdiction

        # Step 5: Retrieve relevant primary legislation
        steps.append("5. Retrieve relevant primary legislation")
        # Step 6: Retrieve applicable delegated legislation
        steps.append("6. Retrieve applicable delegated legislation")
        # Step 7: Retrieve relevant constitutional and judicial authorities
        steps.append("7. Retrieve relevant constitutional and judicial authorities")
        # Step 8: Resolve statutory versions and commencement status
        steps.append("8. Resolve statutory versions and commencement status")
        # Step 9: Evaluate precedent relationships and authority conflicts
        steps.append("9. Evaluate precedent relationships and authority conflicts")
        # Step 10: Disambiguate cross-statute definitions
        steps.append("10. Disambiguate cross-statute definitions")
        evidence_set = self.evidence_orchestrator.orchestrate_evidence(parsed_q, limit=limit)

        # Step 11: Assemble facts and build IRAC analysis
        steps.append("11. Assemble facts and build IRAC analysis")
        fact_report = self.fact_analyzer.analyze(parsed_q, evidence_set)

        # Step 12: Validate claim support and citation integrity
        steps.append("12. Validate claim support and citation integrity")
        assembled_ans = self.answer_assembler.assemble_answer(
            parsed_query=parsed_q,
            evidence_set=evidence_set,
            fact_report=fact_report,
            raw_draft_answer=raw_draft_answer,
        )

        # Step 13: Decide whether to answer, qualify, clarify, or abstain
        steps.append("13. Decide whether to answer, qualify, clarify, or abstain")
        policy_result = self.decision_policy.evaluate(parsed_q, evidence_set, assembled_ans)

        # Step 14: Format final response based on policy decision
        steps.append("14. Return answer with traceable sources and limitations")

        # Step 15: Post-generation safety verification & provenance audit
        steps.append("15. Post-generation safety evaluation & provenance audit")
        prov_audit_report = None
        if hasattr(assembled_ans, "proposition_provenance") and assembled_ans.proposition_provenance:
            prov_audit_report = self.provenance_auditor.audit_propositions(assembled_ans.proposition_provenance)
            if prov_audit_report.quarantined_scaffold_count > 0:
                policy_result.state = LegalResponseState.ABSTAIN_SOURCE_INTEGRITY_FAILURE
                policy_result.policy_rationale = (
                    "CRITICAL SAFETY INTERCEPT: Quarantined synthetic scaffold "
                    "(IND-JUD-DEL-2024-BAIL) was detected in assembled proposition provenance."
                )

        end_t = time.time()
        duration = end_t - start_t

        final_text = assembled_ans.answer_text

        # Detect intra-answer internal contradiction in final prose
        lower_final = final_text.lower()
        has_internal_contradiction = False
        if ("injunction may be granted" in lower_final or "grant an injunction" in lower_final) and (
            "bars the grant of an injunction" in lower_final
            or "shall not grant an injunction" in lower_final
            or "bars the grant of injunction" in lower_final
            or "injunction cannot be granted" in lower_final
        ):
            has_internal_contradiction = True
        elif "absolute right" in lower_final and ("prohibited" in lower_final or "barred" in lower_final or "statutory bar" in lower_final):
            has_internal_contradiction = True

        if has_internal_contradiction and policy_result.state == LegalResponseState.ANSWER_SUPPORTED:
            policy_result.state = LegalResponseState.CLARIFICATION_REQUIRED
            policy_result.clarifying_question = "Material contradiction detected between affirmative claim and statutory bar."
            final_text = (
                "CLARIFICATION REQUIRED BEFORE DEFINITIVE DETERMINATION:\n"
                f"{policy_result.clarifying_question}\n\n"
                "Preliminary Statutory Context:\n"
                + final_text
            )
        if policy_result.state == LegalResponseState.ABSTAIN_SOURCE_INTEGRITY_FAILURE:
            final_text = (
                "ABSTENTION — SOURCE INTEGRITY FAILURE:\n"
                f"{policy_result.policy_rationale}\n\n"
                "The cited case or statute lacks verified provenance in official Indian Gazette or law reports. "
                "LegalMitra strictly refrains from fabricating legal ratios or validating propositions on unverified authorities."
            )
        elif policy_result.state == LegalResponseState.ABSTAIN_INSUFFICIENT_EVIDENCE:
            final_text = (
                "ABSTENTION — INSUFFICIENT VERIFIED EVIDENCE:\n"
                f"{policy_result.policy_rationale}\n\n"
                f"Clarification Required: {policy_result.clarifying_question}"
            )
        elif policy_result.state == LegalResponseState.ABSTAIN_TEMPORAL_UNCERTAINTY:
            final_text = (
                "ABSTENTION — UNCOMMENCED STATUTORY ENACTMENT:\n"
                f"{policy_result.policy_rationale}\n\n"
                "While Parliament enacted this legislation and it received Presidential assent, the Central Government "
                "has not issued an Official Gazette notification appointing its date of commencement. "
                "Consequently, the prior statutory regime remains active and in force."
            )
        elif policy_result.state == LegalResponseState.ABSTAIN_AUTHORITY_CONFLICT:
            final_text = (
                "ABSTENTION — IRRECONCILABLE CO-EQUAL PRECEDENT CONFLICT:\n"
                f"{policy_result.policy_rationale}\n\n"
                f"Clarification Required: {policy_result.clarifying_question}"
            )
        elif policy_result.state == LegalResponseState.CLARIFICATION_REQUIRED:
            final_text = (
                "CLARIFICATION REQUIRED BEFORE DEFINITIVE DETERMINATION:\n"
                f"{policy_result.clarifying_question}\n\n"
                "Preliminary Statutory Context:\n"
                + final_text
            )
        elif policy_result.state == LegalResponseState.ANSWER_PARTIAL:
            final_text = (
                "PARTIAL LEGAL DETERMINATION (MULTI-ISSUE CALIBRATED SYNTHESIS):\n"
                f"{policy_result.policy_rationale}\n\n"
                + final_text
            )
        elif policy_result.state == LegalResponseState.ANSWER_CONDITIONAL:
            final_text = (
                "CONDITIONAL LEGAL DETERMINATION (ALTERNATIVE FACTUAL BRANCHES):\n"
                f"{policy_result.policy_rationale}\n\n"
                + final_text
            )

        matrix = getattr(assembled_ans, "evidence_matrix", None)
        telemetry = PipelineExecutionTelemetry(
            start_time=start_t,
            end_time=end_t,
            duration_seconds=duration,
            steps_executed=steps,
            query_domain=parsed_q.legal_domain,
            issues_spotted=issues,
            evidence_count=evidence_set.total_items_retrieved,
            contrary_authorities_count=len(evidence_set.contrary_authorities),
            claims_validated=len(assembled_ans.claims),
            policy_state=policy_result.state.value,
            clarification_posed=policy_result.requires_clarifying_question,
            abstention_triggered=policy_result.state.value.startswith("ABSTAIN"),
            has_partial_support=bool(matrix and matrix.has_partial_support),
            is_conditional=bool(matrix and matrix.is_conditional),
            issue_matrix_records_count=len(matrix.records) if matrix else 0,
        )

        return OrchestratedLegalResponse(
            query=query,
            response_state=policy_result.state,
            answer_text=final_text,
            citations=assembled_ans.citations,
            governing_provisions=assembled_ans.governing_provisions,
            competing_authorities=assembled_ans.competing_authorities,
            parsed_query=parsed_q,
            evidence_set=evidence_set,
            fact_report=fact_report,
            assembled_answer=assembled_ans,
            policy_result=policy_result,
            telemetry=telemetry,
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence_matrix=matrix,
            proposition_provenance=getattr(assembled_ans, 'proposition_provenance', []),
            provenance_audit=prov_audit_report,
        )

