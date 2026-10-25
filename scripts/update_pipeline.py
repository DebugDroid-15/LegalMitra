"""
Update pipeline.py for Phase 56:
- Add has_partial_support, is_conditional, and issue_matrix_records_count to PipelineExecutionTelemetry.
- Add evidence_matrix field to OrchestratedLegalResponse.
- Add formatting for ANSWER_PARTIAL and ANSWER_CONDITIONAL response states.
"""

from pathlib import Path

file_path = Path("legalmitra/orchestration/pipeline.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

# 1. Update PipelineExecutionTelemetry
old_telem = """@dataclass
class PipelineExecutionTelemetry:
    \"\"\"Detailed audit telemetry for pipeline execution.\"\"\"
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
    abstention_triggered: bool = False"""

new_telem = """@dataclass
class PipelineExecutionTelemetry:
    \"\"\"Detailed audit telemetry for pipeline execution.\"\"\"
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
    issue_matrix_records_count: int = 0"""

assert old_telem in content, "Could not find old_telem"
content = content.replace(old_telem, new_telem, 1)

# 2. Update OrchestratedLegalResponse
old_resp = """@dataclass
class OrchestratedLegalResponse:
    \"\"\"Final output object returned by the orchestration pipeline.\"\"\"
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
    timestamp: str"""

new_resp = """@dataclass
class OrchestratedLegalResponse:
    \"\"\"Final output object returned by the orchestration pipeline.\"\"\"
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
    evidence_matrix: Optional[Any] = None"""

assert old_resp in content, "Could not find old_resp"
content = content.replace(old_resp, new_resp, 1)

# 3. Add formatting for ANSWER_PARTIAL and ANSWER_CONDITIONAL
old_format = """        elif policy_result.state == LegalResponseState.CLARIFICATION_REQUIRED:
            final_text = (
                "CLARIFICATION REQUIRED BEFORE DEFINITIVE DETERMINATION:\\n"
                f"{policy_result.clarifying_question}\\n\\n"
                "Preliminary Statutory Context:\\n"
                + final_text
            )"""

new_format = """        elif policy_result.state == LegalResponseState.CLARIFICATION_REQUIRED:
            final_text = (
                "CLARIFICATION REQUIRED BEFORE DEFINITIVE DETERMINATION:\\n"
                f"{policy_result.clarifying_question}\\n\\n"
                "Preliminary Statutory Context:\\n"
                + final_text
            )
        elif policy_result.state == LegalResponseState.ANSWER_PARTIAL:
            final_text = (
                "PARTIAL LEGAL DETERMINATION (MULTI-ISSUE CALIBRATED SYNTHESIS):\\n"
                f"{policy_result.policy_rationale}\\n\\n"
                + final_text
            )
        elif policy_result.state == LegalResponseState.ANSWER_CONDITIONAL:
            final_text = (
                "CONDITIONAL LEGAL DETERMINATION (ALTERNATIVE FACTUAL BRANCHES):\\n"
                f"{policy_result.policy_rationale}\\n\\n"
                + final_text
            )"""

assert old_format in content, "Could not find old_format"
content = content.replace(old_format, new_format, 1)

# 4. Update telemetry and return in execute()
old_telem_inst = """        telemetry = PipelineExecutionTelemetry(
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
        )"""

new_telem_inst = """        matrix = getattr(assembled_ans, "evidence_matrix", None)
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
        )"""

assert old_telem_inst in content, "Could not find old_telem_inst"
content = content.replace(old_telem_inst, new_telem_inst, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
