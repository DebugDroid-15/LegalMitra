# PHASE 56: ISSUE-LEVEL EVIDENCE MATRIX REPORT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  
**Module:** `legalmitra.orchestration.evidence_matrix`  

---

## 1. Executive Summary

Phase 56 introduces the `IssueEvidenceMatrix`, a structured data artifact that links every decomposed legal question to its evidentiary foundation, candidate statutory provisions, temporal status, precedent hierarchy, claim validation outcome, and disposition.

---

## 2. IssueEvidenceRecord Schema

Every decomposed issue is tracked via `IssueEvidenceRecord`:
- `issue_id`: Unique string (`ISSUE-1`, `ISSUE-2`).
- `issue_statement`: Concise statement of the legal question.
- `material_facts`: User-supplied facts relevant to the issue.
- `unresolved_assumptions`: Implicit assumptions requiring verification.
- `candidate_rules`: Applicable statutory provisions and judicial ratios.
- `applicable_exceptions`: Provisos, statutory bars, and exceptions.
- `selected_evidence_ids`: Chunk IDs of verified knowledge base sources.
- `temporal_status`: `IN_FORCE`, `ENACTED_UNCOMMENCED`, `REPEALED_WITH_SAVINGS`, `OVERRULED`.
- `precedent_status`: `BINDING_RATIO`, `DISTINGUISHED`, `REFERRED_TO_LARGER_BENCH`, `CO_EQUAL_CONFLICT`.
- `claim_validation_outcome`: `FULLY_SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`, `TEMPORALLY_UNCERTAIN`, `INSUFFICIENT_EVIDENCE`.
- `missing_evidence`: Specific missing gazette entries or records.
- `issue_disposition`: `DIRECT_ANSWER`, `QUALIFIED_ANSWER`, `CONDITIONAL_ANSWER`, `CLARIFICATION_REQUIRED`, `ABSTAIN_*`.
- `prerequisite_issue_id`: Parent issue on which this issue depends.
- `dependency_satisfied`: Boolean indicating whether prerequisite passed.
- `conditional_reasoning`: Explicit IF-THEN branching text.
- `disposition_rationale`: Audit rationale justifying the disposition.

---

## 3. Sample Rendered Matrix

| Issue ID | Legal Issue | Candidate Rules | Temporal / Authority Status | Validation Outcome | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ISSUE-1` | Specific performance of concession agreement | SRA 1963 Section 10 | IN_FORCE / BINDING_RATIO | `FULLY_SUPPORTED` | `DIRECT_ANSWER` |
| `ISSUE-2` | Statutory bar on infrastructure injunctions | SRA 1963 Section 20A | IN_FORCE / BINDING_RATIO | `FULLY_SUPPORTED` | `QUALIFIED_ANSWER` |

Matrix markdown generation is implemented via `IssueEvidenceMatrix.format_markdown_table()` and verified in Phase 56 test suite.
