"""
Update decision_policy.py for Phase 56:
- Add ANSWER_CONDITIONAL and ANSWER_PARTIAL to LegalResponseState enum.
- Add evidence_matrix field to PolicyEvaluationResult.
- Implement multi-issue partial answer and conditional reasoning evaluation in LegalDecisionPolicy.
"""

from pathlib import Path

file_path = Path("legalmitra/orchestration/decision_policy.py")
content = file_path.read_text(encoding="utf-8")

# 1. Update LegalResponseState
old_enum = """class LegalResponseState(str, Enum):
    ANSWER_SUPPORTED = "ANSWER_SUPPORTED"
    ANSWER_QUALIFIED = "ANSWER_QUALIFIED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    ABSTAIN_INSUFFICIENT_EVIDENCE = "ABSTAIN_INSUFFICIENT_EVIDENCE"
    ABSTAIN_AUTHORITY_CONFLICT = "ABSTAIN_AUTHORITY_CONFLICT"
    ABSTAIN_TEMPORAL_UNCERTAINTY = "ABSTAIN_TEMPORAL_UNCERTAINTY"
    ABSTAIN_SOURCE_INTEGRITY_FAILURE = "ABSTAIN_SOURCE_INTEGRITY_FAILURE" """

new_enum = """class LegalResponseState(str, Enum):
    ANSWER_SUPPORTED = "ANSWER_SUPPORTED"
    ANSWER_QUALIFIED = "ANSWER_QUALIFIED"
    ANSWER_CONDITIONAL = "ANSWER_CONDITIONAL"
    ANSWER_PARTIAL = "ANSWER_PARTIAL"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    ABSTAIN_INSUFFICIENT_EVIDENCE = "ABSTAIN_INSUFFICIENT_EVIDENCE"
    ABSTAIN_AUTHORITY_CONFLICT = "ABSTAIN_AUTHORITY_CONFLICT"
    ABSTAIN_TEMPORAL_UNCERTAINTY = "ABSTAIN_TEMPORAL_UNCERTAINTY"
    ABSTAIN_SOURCE_INTEGRITY_FAILURE = "ABSTAIN_SOURCE_INTEGRITY_FAILURE" """

# Ensure clean matching
if "ABSTAIN_SOURCE_INTEGRITY_FAILURE = \"ABSTAIN_SOURCE_INTEGRITY_FAILURE\"" in content:
    content = content.replace(
        "    ABSTAIN_SOURCE_INTEGRITY_FAILURE = \"ABSTAIN_SOURCE_INTEGRITY_FAILURE\"",
        "    ANSWER_CONDITIONAL = \"ANSWER_CONDITIONAL\"\n    ANSWER_PARTIAL = \"ANSWER_PARTIAL\"\n    ABSTAIN_SOURCE_INTEGRITY_FAILURE = \"ABSTAIN_SOURCE_INTEGRITY_FAILURE\""
    )

# 2. Add evidence_matrix field to PolicyEvaluationResult
old_dataclass = """@dataclass
class PolicyEvaluationResult:
    \"\"\"Outcome of policy evaluation governing response emission.\"\"\"
    state: LegalResponseState
    allows_partial_answer: bool
    requires_clarifying_question: bool
    clarifying_question: Optional[str]
    missing_evidence_or_fact: Optional[str]
    policy_rationale: str
    permitted_assertions: List[str]
    prohibited_assertions: List[str]"""

new_dataclass = """@dataclass
class PolicyEvaluationResult:
    \"\"\"Outcome of policy evaluation governing response emission.\"\"\"
    state: LegalResponseState
    allows_partial_answer: bool
    requires_clarifying_question: bool
    clarifying_question: Optional[str]
    missing_evidence_or_fact: Optional[str]
    policy_rationale: str
    permitted_assertions: List[str]
    prohibited_assertions: List[str]
    evidence_matrix: Optional[Any] = None"""

assert old_dataclass in content, "Could not find old_dataclass"
content = content.replace(old_dataclass, new_dataclass, 1)

# 3. Add matrix inspection to LegalDecisionPolicy.evaluate
policy_eval_anchor = """        # 2. Check for empty evidence set -> ABSTAIN_INSUFFICIENT_EVIDENCE"""

matrix_eval_code = """        # Check evidence matrix outcomes (Phase 56 Multi-Issue Synthesis)
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

        # 2. Check for empty evidence set -> ABSTAIN_INSUFFICIENT_EVIDENCE"""

assert policy_eval_anchor in content, "Could not find policy_eval_anchor"
content = content.replace(policy_eval_anchor, matrix_eval_code, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
