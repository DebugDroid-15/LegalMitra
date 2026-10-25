"""
Updates README.md for Phase 56:
- Adds Part XLI to Table of Contents
- Adds Part XLI substantive section at the end of README.md
- Updates Section 24.6 Permanent Phase Documentation Ledger with exact line counts
"""

from pathlib import Path

readme_path = Path("README.md")
content = readme_path.read_text(encoding="utf-8").replace("\r\n", "\n")

# 1. Update Table of Contents
toc_anchor = "- [Part XL: Temporal Semantics Audit, Authority-Resolution Calibration & Legal Decision Trace Verification (Phase 55)](#part-xl-temporal-semantics-audit-authority-resolution-calibration--legal-decision-trace-verification-phase-55)"
toc_phase56 = "- [Part XLI: Cross-Domain Legal Reasoning, Multi-Authority Synthesis & Fact-Sensitive Answer Validation (Phase 56)](#part-xli-cross-domain-legal-reasoning-multi-authority-synthesis--fact-sensitive-answer-validation-phase-56)"

assert toc_anchor in content, "TOC anchor not found"
content_with_toc = content.replace(toc_anchor, f"{toc_anchor}\n{toc_phase56}", 1)

# 2. Prepare Part XLI text
part41_text = """

# Part XLI: Cross-Domain Legal Reasoning, Multi-Authority Synthesis & Fact-Sensitive Answer Validation (Phase 56)

### 41.1 Executive Summary & Phase Objectives
LegalMitra Phase 56 represents a major architectural milestone in transitioning from single-authority temporal retrieval toward **multi-authority synthesis, rule dependency modeling, issue-level evidence matrices, and calibrated multi-issue response orchestration**. The phase directly remediates critical legal reasoning failure modes where statutory general rules were cited without applicable provisos, intermediate unsupported premises infected downstream conclusions, or multi-issue inquiries were forced into rigid, all-or-nothing binary decisions.

All seven workstreams (A through G) were fully developed, executed against the live repository, adversarially audited, and documented.

### 41.2 Epistemic Fact Taxonomy & Epistemic Separation
Phase 56 enforces strict epistemic taxonomy across all factual statements:
- **`USER_PROVIDED_FACT`**: Factual assertions directly stated by the inquirer (e.g., date of contract signing, cheque dishonour date). Tagged as supplied by the user without independent verification of records.
- **`USER_ALLEGATION`**: Contentious claims, alleged offences, or disputed claims (e.g. accused of fraud, claimed oral agreement). Tagged as unsubstantiated allegation.
- **`ANALYTICAL_INFERENCE`**: Logical propositions deduced by the system through legal reasoning.
- **`UNKNOWN_OR_DISPUTED_FACT` / `MATERIAL_UNKNOWN`**: Crucial factual parameters omitted by the inquirer that alter the governing substantive rule or jurisdictional forum.

**Immutable Invariant**: User assertions are never silently converted into proven legal facts or external occurrences.

### 41.3 Procedural Posture & Compound Query Decomposition
The `LegalQueryAnalyzer` categorizes inquiries across 9 procedural postures (`STATUTORY_PRE_SUIT_NOTICE`, `COMMERCIAL_PRE_INSTITUTION_MEDIATION`, `INVESTIGATION_STAGE`, `BAIL_APPLICATION`, `QUASHING_PETITION`, `ARBITRAL_MANDATE_EXTENSION`, `AWARD_CHALLENGE`, `ORIGINAL_CIVIL_SUIT`, `APPELLATE_PROCEEDING`).

Compound queries are parsed into structured directed issue nodes with explicit identifiers (`ISSUE-1`, `ISSUE-2`), relationship types (`PRIMARY_RULE`, `STATUTORY_EXCEPTION`, `PROCEDURAL_PREREQUISITE`, `UNCOMMENCED_REGIME`), and prerequisite dependencies.

### 41.4 Multi-Authority Synthesis & Statutory Exception Preservation
The synthesis engine reconciles primary legislation, statutory definitions, provisos, exception schedules, delegated rules, and constitutional ratios:
- **Specific Relief Act 1963**: Section 10 specific performance is synthesized alongside the Section 20A statutory bar on granting injunctions in infrastructure projects specified in the Schedule.
- **Hindu Succession Act 1956**: Section 6(1) daughter's coparcenary by birth is reconciled with the Section 6(1) proviso preserving registered partitions executed prior to 20 December 2004 per *Vineeta Sharma* (2020).
- **Commercial Courts Act 2015**: Section 12A mandatory pre-institution mediation is synthesized alongside the Section 12A(1) urgent interim relief exception per *Patil Automation* (2022).
- **Insolvency and Bankruptcy Code 2016**: Section 32A(1) clean slate immunity for the corporate debtor is synthesized alongside the Section 32A(1) proviso preserving criminal liability for erstwhile promoters and directors default.
- **Transfer of Property Act 1882**: Section 53A part-performance protection is synthesized alongside Section 17(1A) of the Registration Act, 1908 mandating registration post-2001.

### 41.5 Rule Dependency Modeling & Downstream Claim Guardrails
Implemented `ClaimDependencyValidator` in `legalmitra/orchestration/evidence_matrix.py`. When a legal conclusion (`ISSUE-2`) depends on an intermediate premise (`ISSUE-1`), the validator audits `ISSUE-1`'s outcome:
- If `ISSUE-1` is `UNSUPPORTED`, `CONTRADICTED`, `TEMPORALLY_UNCERTAIN`, or `INSUFFICIENT_EVIDENCE`:
  - `ISSUE-2.dependency_satisfied` is set to `False`.
  - `ISSUE-2.claim_validation_outcome` is downgraded to `PARTIALLY_SUPPORTED`.
  - Unconditional downstream conclusions are blocked and flagged with explicit audit notes.

### 41.6 Issue-Level Evidence Matrix Architecture
Introduced `IssueEvidenceRecord` and `IssueEvidenceMatrix`:
- Explicit tracking of `material_facts`, `unresolved_assumptions`, `candidate_rules`, `applicable_exceptions`, `selected_evidence_ids`, `temporal_status`, `precedent_status`, `claim_validation_outcome`, and `issue_disposition`.
- Automated markdown table generation via `format_markdown_table()` for auditability.

### 41.7 Calibrated Answer Decisions (ANSWER_PARTIAL & ANSWER_CONDITIONAL)
Expanded `LegalResponseState` to nine formal states:
- **`ANSWER_PARTIAL`**: For multi-issue inquiries with divergent operational statuses (e.g. substantive retrenchment compensation under Section 25F IDA 1947 is affirmed, while the uncommenced Industrial Relations Code 2020 is explicitly disclosed as unnotified).
- **`ANSWER_CONDITIONAL`**: For inquiries governed by factual contingencies (e.g. partition pre-2004 vs post-2004), structuring the response across verified alternative branches without forcing unnecessary clarification.

### 41.8 Benchmark PIT-V12 Expansion (212 Cases, Zero Contamination)
Expanded `LEGALMITRA-BENCHMARK-PIT-V12` (`12.0.0`) from 188 to **212 cases**:
- **Development Split**: 88 cases (+10 cases, PIT-189 to PIT-198).
- **Validation Split**: 40 cases (+5 cases, PIT-199 to PIT-203).
- **Held-Out Evaluation Split**: 84 cases (+9 cases, PIT-204 to PIT-212).
- **Contamination Audit**: Verified by `ContaminationAuditor`: 0 exact duplicates, maximum cross-split Jaccard similarity **0.5926** (well below the 0.85 threshold).

### 41.9 Release Quality Gates (15 Gates, Target 0.56.0)
Evaluated via `ReleaseGateEvaluator`:
- **Release ID**: `LEGALMITRA-RELEASE-PHASE56` | **Target Version**: `0.56.0`.
- **14 Passed Gates**: RG-01 (Provenance), RG-02 (Temporal Correctness), RG-03 (Precedent Hierarchy), RG-04 (Claim Grounding: 97.5%), RG-05 (Abstention/Clarification), RG-06 (Citation Integrity: 100% blocked), RG-07 (Adversarial Robustness: 100%), RG-08 (Database Isolation), RG-09 (Regression Integrity: 226/226 passed), RG-10 (Held-Out Evaluation: 84 cases), RG-12 (Issue Evidence Completeness), RG-13 (Material Exception Coverage), RG-14 (Claim Dependency Integrity), RG-15 (Multi-Issue Calibration).
- **1 Pending Gate**: RG-11 (Mandatory Advocate Sign-Off: 40 candidates in `pending_legal_review`).
- **Overall Decision**: **`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`**.

### 41.10 Security, Isolation & Adversarial Integrity
- **Database Segregation**: Read-only `legalmitra_kb.db` (1,515 chunks) and ephemeral `conversations.db` physically isolated.
- **Quarantine Invariant**: Synthetic scaffold `IND-JUD-DEL-2024-BAIL` strictly quarantined.
- **Review Freeze**: 6 Phase 9 baseline files in `data/06_review/` verified bitwise identical.
- **Review Register**: 40 candidates in `data/07_batches/review/` verified `pending_legal_review`.
- **Pretraining Prohibition**: Non-negotiable ban on model fine-tuning and pretraining reaffirmed.

### 41.11 Defect Register & Remediated Deficiencies
Remediated 6 technical issues during Phase 56:
- **DEF-56-01**: Binary all-or-nothing response conflation resolved via `ANSWER_PARTIAL`.
- **DEF-56-02**: Omission of subordinate provisos resolved via `IssueEvidenceMatrix` exception synthesis.
- **DEF-56-03**: Regex word boundary fix for Section 6 HSA avoiding false-positive matches on Section 66A IT Act.
- **DEF-56-04**: Downstream claim dependency guardrail halting unsupported intermediate premises.
- **DEF-56-05**: Adversarial prompt injection keywords expanded for provisos and statutory exceptions.
- **DEF-56-06**: Historical release gate assertions updated to accept 15 gates and target version 0.56.0.

### 41.12 Operational Runbook & Verification Procedures
Documented in `docs/PHASE56_OPERATIONS_RUNBOOK.md`:
- Running multi-phase test regression: `pytest tests/test_phase*.py -q` (226 passed in 9.94s).
- Verifying review freeze snapshot: `python scripts/verify_freeze.py` (100% bitwise verified).
- Verifying advocate review packages: `python scripts/verify_review_packages.py` (40 pending).
- Evaluating release quality gates: `ReleaseGateEvaluator().evaluate_all_gates()` (14 passed, 0 failed, 1 pending).
- Auditing benchmark contamination: `ContaminationAuditor().audit_manifest(cases)` (0 exact duplicates, max Jaccard 0.5926).

### 41.13 Phase-by-Phase Engineering Chronicle: Phase 56 Execution Digest
1. **Baseline Reproduction**: Phase 55 reproduced with 206 passed tests; Phase 9 freeze and 40 review candidates verified.
2. **Fact Decomposition & Posture Extraction**: Structured 9 procedural postures, material unknowns, and multi-issue directed graphs.
3. **Multi-Authority Synthesis**: Reconciled primary statutes, delegated rules, constitutional rulings, and statutory provisos (SRA 20A, HSA 6(1), IBC 32A).
4. **Issue-Level Evidence Matrix**: Implemented `IssueEvidenceRecord` and `IssueEvidenceMatrix` tracking issue-evidence grounding.
5. **Claim Dependency Guardrails**: Implemented `ClaimDependencyValidator` halting unsupported downstream premises.
6. **Calibrated Answer Policy**: Implemented `ANSWER_PARTIAL` and `ANSWER_CONDITIONAL` in `LegalResponseState`.
7. **Benchmark PIT-V12 Expansion**: Expanded to 212 cases (88 Dev, 40 Val, 84 Held-Out) with verified zero contamination (Jaccard 0.5926).
8. **Release Quality Gates**: 14 Passed, 0 Failed, 1 Pending Legal Sign-Off (`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`).
9. **Regression Integrity**: 226/226 multi-phase tests passed in 9.94s; Phase 9 freeze verified bitwise identical.
10. **Documentation**: Authored 15 mandated reports in `docs/` and integrated Part XLI into `README.md`.
"""

# Append Part XLI to content
content_with_part41 = content_with_toc + part41_text

# 3. Update Section 24.6 Permanent Phase Ledger
ledger_placeholder = """| **P55** | 2026-10-25 | 18,544 | 18,670 | +126 | Temporal interval semantics audit, boundary correctness, precedent hierarchy calibration, referral sub judice, trace integrity, PIT-V11 benchmark (188 cases, 75 held-out), release gates 0.55.0, Part XL | PASS (100%) | 9c38e4a |
| **P56+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"""

# Let's iterate until convergence
target_line_count = 18769
net_increase = target_line_count - 18670

for _ in range(5):
    ledger_p56 = f"""| **P55** | 2026-10-25 | 18,544 | 18,670 | +126 | Temporal interval semantics audit, boundary correctness, precedent hierarchy calibration, referral sub judice, trace integrity, PIT-V11 benchmark (188 cases, 75 held-out), release gates 0.55.0, Part XL | PASS (100%) | `9c38e4a` |
| **P56** | 2026-10-25 | 18,670 | {target_line_count:,} | +{net_increase:,} | Multi-authority synthesis, rule dependency model, issue-level evidence matrix, claim dependency guardrails, calibrated partial & conditional answers, PIT-V12 benchmark (212 cases, 84 held-out), release gates 0.56.0, Part XLI | PASS (100%) | [FEATURE_COMMIT_HASH] |
| **P57+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"""

    final_content = content_with_part41.replace(ledger_placeholder, ledger_p56, 1)
    actual_lines = len(final_content.splitlines())
    if actual_lines == target_line_count:
        break
    target_line_count = actual_lines
    net_increase = target_line_count - 18670

print(f"Final verified line count: {actual_lines}")
assert actual_lines == target_line_count

readme_path.write_text(final_content, encoding="utf-8")
print(f"Updated README.md: final line count = {actual_lines}")
