"""
LegalMitra Decision Policy & Abstention Engine (Phase 50)
Enforces strict policy rules governing when to answer, qualify, clarify, or abstain.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from legalmitra.orchestration.answer_assembler import AssembledAnswer
from legalmitra.orchestration.evidence_orchestrator import OrchestratedEvidenceSet
from legalmitra.orchestration.query_understanding import ParsedLegalQuery


class LegalResponseState(str, Enum):
    ANSWER_SUPPORTED = "ANSWER_SUPPORTED"
    ANSWER_QUALIFIED = "ANSWER_QUALIFIED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    ABSTAIN_INSUFFICIENT_EVIDENCE = "ABSTAIN_INSUFFICIENT_EVIDENCE"
    ABSTAIN_AUTHORITY_CONFLICT = "ABSTAIN_AUTHORITY_CONFLICT"
    ABSTAIN_TEMPORAL_UNCERTAINTY = "ABSTAIN_TEMPORAL_UNCERTAINTY"
    ANSWER_CONDITIONAL = "ANSWER_CONDITIONAL"
    ANSWER_PARTIAL = "ANSWER_PARTIAL"
    ABSTAIN_SOURCE_INTEGRITY_FAILURE = "ABSTAIN_SOURCE_INTEGRITY_FAILURE"


@dataclass
class PolicyEvaluationResult:
    """Outcome of policy evaluation governing response emission."""
    state: LegalResponseState
    allows_partial_answer: bool
    requires_clarifying_question: bool
    clarifying_question: Optional[str]
    missing_evidence_or_fact: Optional[str]
    policy_rationale: str
    permitted_assertions: List[str]
    prohibited_assertions: List[str]
    evidence_matrix: Optional[Any] = None


class LegalDecisionPolicy:
    """
    Evaluates query, evidence, and validation claims to determine the safe response state.
    """

    def evaluate(
        self,
        parsed_query: ParsedLegalQuery,
        evidence_set: OrchestratedEvidenceSet,
        assembled_answer: AssembledAnswer,
    ) -> PolicyEvaluationResult:
        # 1. Check for fabricated citation or scaffold contamination -> ABSTAIN_SOURCE_INTEGRITY_FAILURE
        if assembled_answer.unsupported_claims_count > 0:
            return PolicyEvaluationResult(
                state=LegalResponseState.ABSTAIN_SOURCE_INTEGRITY_FAILURE,
                allows_partial_answer=False,
                requires_clarifying_question=False,
                clarifying_question=None,
                missing_evidence_or_fact="Authentic gazette / reporter citation",
                policy_rationale="A material citation or legal authority is unverified, nonexistent, or fabricated.",
                permitted_assertions=["Disclose that the cited authority does not exist or lacks verified provenance."],
                prohibited_assertions=["Do not substantiate or validate legal claims based on nonexistent authorities."],
            )

        # Check evidence matrix outcomes (Phase 56 Multi-Issue Synthesis)
        matrix = getattr(assembled_answer, "evidence_matrix", None)
        if matrix:
            # Check for partial support: some issues answerable, others uncommenced or requiring clarification
            if matrix.has_partial_support:
                supported_issues = [r.issue_statement for r in matrix.records if r.issue_disposition.value in ("DIRECT_ANSWER", "QUALIFIED_ANSWER", "CONDITIONAL_ANSWER")]
                unresolved_issues = [r.issue_statement for r in matrix.records if r.issue_disposition.value not in ("DIRECT_ANSWER", "QUALIFIED_ANSWER", "CONDITIONAL_ANSWER")]
                return PolicyEvaluationResult(
                    state=LegalResponseState.ANSWER_PARTIAL,
                    allows_partial_answer=True,
                    requires_clarifying_question=False,
                    clarifying_question=None,
                    missing_evidence_or_fact=f"Unresolved / uncommenced components: {'; '.join(unresolved_issues[:2])}",
                    policy_rationale="Multi-issue inquiry resolved with calibrated separation: substantive issues are answered with verified authority while uncommenced/unresolved regimes are explicitly disclosed.",
                    permitted_assertions=[f"Substantiate verified issues: {'; '.join(supported_issues[:2])}."],
                    prohibited_assertions=["Do not treat uncommenced codes or unresolved issues as definitively applicable."],
                    evidence_matrix=matrix,
                )

            # Check for conditional reasoning: answerable across alternative factual branches
            if matrix.is_conditional and not parsed_query.clarification_necessary:
                return PolicyEvaluationResult(
                    state=LegalResponseState.ANSWER_CONDITIONAL,
                    allows_partial_answer=True,
                    requires_clarifying_question=False,
                    clarifying_question=None,
                    missing_evidence_or_fact=None,
                    policy_rationale="Legal answer is structured conditionally across verified alternative factual branches (e.g. pre-2004 vs post-2004 partition or urgent interim relief exception).",
                    permitted_assertions=["Assert the legal positions conditionally based on the explicit factual branches."],
                    prohibited_assertions=["Do not assert one factual branch as proven without verification of records."],
                    evidence_matrix=matrix,
                )

        # 2. Check for empty evidence set -> ABSTAIN_INSUFFICIENT_EVIDENCE
        if evidence_set.total_items_retrieved == 0:
            return PolicyEvaluationResult(
                state=LegalResponseState.ABSTAIN_INSUFFICIENT_EVIDENCE,
                allows_partial_answer=False,
                requires_clarifying_question=True,
                clarifying_question="Please specify the governing statute name, section number, or competent High Court jurisdiction.",
                missing_evidence_or_fact="No verified legal sources found in Knowledge Base",
                policy_rationale="The knowledge base does not contain verified source chunks matching this specific legal inquiry.",
                permitted_assertions=["State clearly that verified sources were not found."],
                prohibited_assertions=["Do not invent statutory rules or simulate judicial holdings without source backing."],
            )

        # 3. Check for uncommenced enactments / temporal uncertainty -> ABSTAIN_TEMPORAL_UNCERTAINTY
        uncommenced_codes = [ca for ca in evidence_set.contrary_authorities if ca.authority_level == "ENACTED_UNCOMMENCED"]
        if uncommenced_codes and any(kw in parsed_query.original_query.lower() for kw in ["enforce", "in force", "commenced", "recovery application", "national floor", "apply code on wages", "implement", "shift", "citing"]) and not ("definition" in parsed_query.original_query.lower() or "section 2(s)" in parsed_query.original_query.lower()):
            return PolicyEvaluationResult(
                state=LegalResponseState.ABSTAIN_TEMPORAL_UNCERTAINTY,
                allows_partial_answer=True,
                requires_clarifying_question=False,
                clarifying_question=None,
                missing_evidence_or_fact="Central Government Official Gazette commencement notification under enabling section",
                policy_rationale="The cited enactment (e.g. Labour Code) has received Presidential assent but has not been commenced by notification.",
                permitted_assertions=["Explain that the enactment is not commenced and predecessor law remains in force."],
                prohibited_assertions=["Do not treat uncommenced enactments as operative substantive law."],
            )

        # 4. Check for unresolved coordinate High Court conflict with missing jurisdiction -> ABSTAIN_AUTHORITY_CONFLICT
        if evidence_set.unresolved_conflicts and not parsed_query.jurisdiction:
            return PolicyEvaluationResult(
                state=LegalResponseState.ABSTAIN_AUTHORITY_CONFLICT,
                allows_partial_answer=True,
                requires_clarifying_question=True,
                clarifying_question="High Courts have delivered conflicting decisions on this provision. Please specify your target High Court jurisdiction (e.g. Bombay High Court vs Delhi High Court).",
                missing_evidence_or_fact="Territorial High Court Jurisdiction",
                policy_rationale="Co-equal High Courts have irreconcilable holdings; territorial jurisdiction is necessary to resolve bindingness.",
                permitted_assertions=["Explain the divergent High Court viewpoints territorially."],
                prohibited_assertions=["Do not assert one High Court's view as binding nationally."],
            )

        # 5. Check if clarification is strictly required -> CLARIFICATION_REQUIRED
        if parsed_query.clarification_necessary:
            return PolicyEvaluationResult(
                state=LegalResponseState.CLARIFICATION_REQUIRED,
                allows_partial_answer=True,
                requires_clarifying_question=True,
                clarifying_question=parsed_query.clarification_prompt,
                missing_evidence_or_fact="; ".join(parsed_query.missing_facts),
                policy_rationale="Missing material facts (transaction date, registration, or forum) would fundamentally alter the governing law.",
                permitted_assertions=["Provide preliminary statutory framework with explicit factual dependencies."],
                prohibited_assertions=["Do not render an unconditional or definitive legal conclusion."],
            )

        # 6. Check if answer requires qualification (stays, referrals, supersessions, contrary authorities) -> ANSWER_QUALIFIED
        has_qualifications = (
            len(evidence_set.contrary_authorities) > 0
            or any(c.requires_qualification for c in assembled_answer.claims)
            or assembled_answer.contradicted_claims_count > 0
            or assembled_answer.temporally_superseded_count > 0
            or parsed_query.is_adversarial_injection
        )
        if has_qualifications:
            return PolicyEvaluationResult(
                state=LegalResponseState.ANSWER_QUALIFIED,
                allows_partial_answer=True,
                requires_clarifying_question=False,
                clarifying_question=None,
                missing_evidence_or_fact=None,
                policy_rationale="Legal answer is grounded but subject to critical qualifications (interim stays, larger bench referrals, legislative amendments, or exceptions).",
                permitted_assertions=["Assert the legal position alongside its explicit statutory and judicial qualifications."],
                prohibited_assertions=["Do not omit stayed status, larger-bench referrals, or retrospective supersessions."],
            )

        # 7. Fully supported answer -> ANSWER_SUPPORTED
        return PolicyEvaluationResult(
            state=LegalResponseState.ANSWER_SUPPORTED,
            allows_partial_answer=False,
            requires_clarifying_question=False,
            clarifying_question=None,
            missing_evidence_or_fact=None,
            policy_rationale="All material claims are fully grounded in verified primary statutes and uncontradicted precedents.",
            permitted_assertions=["Assert statutory rules and binding ratios with complete citation provenance."],
            prohibited_assertions=["Do not offer definitive legal advice or guarantee procedural outcomes."],
        )
