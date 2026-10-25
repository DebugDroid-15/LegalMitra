"""
Update answer_assembler.py for Phase 56:
- Add evidence_matrix field to AssembledAnswer dataclass.
- Instantiate ClaimDependencyValidator in EvidenceTraceableAnswerAssembler.
- Synthesize statutory exceptions, provisos, conditional reasoning, and partial response prose.
"""

from pathlib import Path

file_path = Path("legalmitra/orchestration/answer_assembler.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

# 1. Add import for evidence_matrix
old_imports = """from legalmitra.orchestration.evidence_orchestrator import EvidenceItem, OrchestratedEvidenceSet
from legalmitra.orchestration.fact_analyzer import FactAnalysisReport
from legalmitra.orchestration.query_understanding import ParsedLegalQuery
from legalmitra.temporal.engine import TemporalLawEngine"""

new_imports = """from legalmitra.orchestration.evidence_matrix import ClaimDependencyValidator, IssueEvidenceMatrix
from legalmitra.orchestration.evidence_orchestrator import EvidenceItem, OrchestratedEvidenceSet
from legalmitra.orchestration.fact_analyzer import FactAnalysisReport
from legalmitra.orchestration.query_understanding import ParsedLegalQuery
from legalmitra.temporal.engine import TemporalLawEngine"""

assert old_imports in content, "Could not find old_imports"
content = content.replace(old_imports, new_imports, 1)

# 2. Add evidence_matrix to AssembledAnswer dataclass
old_assembled_answer = """@dataclass
class AssembledAnswer:
    \"\"\"Traceable, evidence-grounded legal answer payload.\"\"\"
    answer_text: str
    citations: List[str]
    claims: List[AssembledClaim]
    governing_provisions: List[str]
    competing_authorities: List[str]
    missing_facts_notes: Optional[str]
    overall_validation_status: str  # FULLY_VALIDATED, QUALIFIED, CONTRADICTED_DETECTED, UNSUPPORTED_DETECTED
    unsupported_claims_count: int
    contradicted_claims_count: int
    temporally_superseded_count: int
    practical_next_steps: List[str]
    disclaimer: str"""

new_assembled_answer = """@dataclass
class AssembledAnswer:
    \"\"\"Traceable, evidence-grounded legal answer payload.\"\"\"
    answer_text: str
    citations: List[str]
    claims: List[AssembledClaim]
    governing_provisions: List[str]
    competing_authorities: List[str]
    missing_facts_notes: Optional[str]
    overall_validation_status: str  # FULLY_VALIDATED, QUALIFIED, CONTRADICTED_DETECTED, UNSUPPORTED_DETECTED
    unsupported_claims_count: int
    contradicted_claims_count: int
    temporally_superseded_count: int
    practical_next_steps: List[str]
    disclaimer: str
    evidence_matrix: Optional[IssueEvidenceMatrix] = None"""

assert old_assembled_answer in content, "Could not find old_assembled_answer"
content = content.replace(old_assembled_answer, new_assembled_answer, 1)

# 3. Add ClaimDependencyValidator to EvidenceTraceableAnswerAssembler.__init__
old_init = """    def __init__(self, temporal_engine: TemporalLawEngine):
        self.temporal_engine = temporal_engine"""

new_init = """    def __init__(self, temporal_engine: TemporalLawEngine):
        self.temporal_engine = temporal_engine
        self.dependency_validator = ClaimDependencyValidator()"""

assert old_init in content, "Could not find old_init"
content = content.replace(old_init, new_init, 1)

# 4. Build matrix at start of assemble_answer and incorporate into prose
matrix_build_anchor = """        claims: List[AssembledClaim] = []
        governing_provisions: List[str] = []
        competing_authorities: List[str] = []
        citations: List[str] = []

        # 1. Synthesize candidate claims from IRAC units and retrieved evidence"""

matrix_build_code = """        claims: List[AssembledClaim] = []
        governing_provisions: List[str] = []
        competing_authorities: List[str] = []
        citations: List[str] = []

        # Build Phase 56 Issue-Level Evidence Matrix
        matrix = self.dependency_validator.build_matrix(
            parsed_query=parsed_query,
            evidence_set=evidence_set,
            fact_report=fact_report,
        )

        # 1. Synthesize candidate claims from IRAC units and retrieved evidence"""

assert matrix_build_anchor in content, "Could not find matrix_build_anchor"
content = content.replace(matrix_build_anchor, matrix_build_code, 1)

# 5. Add statutory exceptions & provisos synthesis to claims
claims_loop_anchor = """        # Synthesize claims from primary statutes"""

claims_loop_enhancement = """        # Synthesize claims for statutory exceptions & provisos identified in evidence matrix
        for rec in matrix.records:
            for exc in rec.applicable_exceptions:
                if exc not in competing_authorities:
                    competing_authorities.append(f"Statutory Exception: {exc}")
                exc_claim = AssembledClaim(
                    claim_id=f"CLAIM-{claim_idx}",
                    claim_text=f"Material Exception / Proviso ({rec.issue_id}): {exc}",
                    supporting_evidence_ids=rec.selected_evidence_ids,
                    verbatim_passage=exc[:200],
                    statutory_version=rec.temporal_status,
                    jurisdiction=parsed_query.jurisdiction or "IN",
                    authority_status="STATUTORY_EXCEPTION_PROVISO",
                    validation_verdict="PARTIALLY_SUPPORTED" if rec.issue_disposition.value == "QUALIFIED_ANSWER" else "SUPPORTED",
                    validation_rationale=rec.disposition_rationale or "Material statutory qualification/exception verified.",
                    is_supported=True,
                    requires_qualification=True,
                )
                claims.append(exc_claim)
                claim_idx += 1

        # Synthesize claims from primary statutes"""

assert claims_loop_anchor in content, "Could not find claims_loop_anchor"
content = content.replace(claims_loop_anchor, claims_loop_enhancement, 1)

# 6. Enhance prose generation for conditional reasoning & partial support
prose_body_anchor = """        elif raw_draft_answer and len(raw_draft_answer.strip()) > 30:
            prose_sections.append(f"Direct Position:\\n{raw_draft_answer.strip()}")
        elif claims:"""

new_prose_body = """        elif matrix.has_partial_support:
            # Multi-issue calibrated partial answer
            part_a_items = []
            part_b_items = []
            for r in matrix.records:
                if r.issue_disposition.value in ("DIRECT_ANSWER", "QUALIFIED_ANSWER", "CONDITIONAL_ANSWER"):
                    part_a_items.append(f"- Issue {r.issue_id} ({r.issue_statement}): {r.disposition_rationale} Rules: {', '.join(r.candidate_rules)}")
                else:
                    part_b_items.append(f"- Issue {r.issue_id} ({r.issue_statement}): {r.disposition_rationale} Status: {r.temporal_status}")
            
            prose_sections.append(
                "Direct Position (Multi-Issue Calibrated Determination):\\n"
                "This inquiry involves multiple distinct legal issues with differing operational statuses.\\n\\n"
                "1. Substantively Resolved Issues:\\n" + "\\n".join(part_a_items) + "\\n\\n"
                "2. Unresolved / Contingent Issues:\\n" + "\\n".join(part_b_items)
            )
        elif matrix.is_conditional:
            cond_lines = [r.conditional_reasoning for r in matrix.records if r.conditional_reasoning]
            prose_sections.append(
                "Direct Position (Conditional Legal Determination):\\n"
                "The applicable legal rule is contingent upon specific factual conditions:\\n"
                + "\\n\\n".join(cond_lines)
            )
        elif raw_draft_answer and len(raw_draft_answer.strip()) > 30:
            prose_sections.append(f"Direct Position:\\n{raw_draft_answer.strip()}")
        elif claims:"""

assert prose_body_anchor in content, "Could not find prose_body_anchor"
content = content.replace(prose_body_anchor, new_prose_body, 1)

# 7. Add evidence_matrix to AssembledAnswer return
old_return = """        return AssembledAnswer(
            answer_text=final_prose,
            citations=list(dict.fromkeys(citations)),
            claims=claims,
            governing_provisions=list(dict.fromkeys(governing_provisions)),
            competing_authorities=list(dict.fromkeys(competing_authorities)),
            missing_facts_notes=missing_notes,
            overall_validation_status=overall_status,
            unsupported_claims_count=unsupported_count,
            contradicted_claims_count=contradicted_count,
            temporally_superseded_count=temporally_superseded_count,
            practical_next_steps=practical_steps,
            disclaimer=disclaimer,
        )"""

new_return = """        return AssembledAnswer(
            answer_text=final_prose,
            citations=list(dict.fromkeys(citations)),
            claims=claims,
            governing_provisions=list(dict.fromkeys(governing_provisions)),
            competing_authorities=list(dict.fromkeys(competing_authorities)),
            missing_facts_notes=missing_notes,
            overall_validation_status=overall_status,
            unsupported_claims_count=unsupported_count,
            contradicted_claims_count=contradicted_count,
            temporally_superseded_count=temporally_superseded_count,
            practical_next_steps=practical_steps,
            disclaimer=disclaimer,
            evidence_matrix=matrix,
        )"""

assert old_return in content, "Could not find old_return"
content = content.replace(old_return, new_return, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
