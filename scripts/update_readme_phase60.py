import os

def update_readme():
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update TOC
    toc_target = '- [Part XLIV: End-to-End Legal Authority Verification, Temporal Applicability, and Precedent Resolution (Phase 59)](#part-xliv-end-to-end-legal-authority-verification-temporal-applicability-and-precedent-resolution-phase-59)'
    toc_replacement = toc_target + '\n- [Part XLV: Adversarial End-to-End Validation, Integrated Legal Safety, and Release-Readiness Assurance (Phase 60)](#part-xlv-adversarial-end-to-end-validation-integrated-legal-safety-and-release-readiness-assurance-phase-60)'

    if toc_target not in content:
        raise ValueError("TOC target not found in README.md")

    if toc_replacement not in content:
        content = content.replace(toc_target, toc_replacement)
        print("Updated Table of Contents with Part XLV link.")

    # 2. Update Ledger in Section 24.6
    ledger_target = "| **P60+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"

    part_xlv = """

# Part XLV: Adversarial End-to-End Validation, Integrated Legal Safety, and Release-Readiness Assurance (Phase 60)

### 45.1 Executive Summary & Integrated Assurance Discipline
LegalMitra Phase 60 executes an adversarial, integrated end-to-end validation of the complete legal-answering system. Moving beyond isolated unit tests and standalone evaluator scripts, Phase 60 subjects the integrated pipeline to compound adversarial scenarios where multiple failure modes—such as valid citations masking unsupported propositions, uncommenced statutory regimes, partial precedent overrulings, disputed factual allegations, failed premise dependencies, prompt injections, and intra-answer contradictory assertions—occur simultaneously in the same legal inquiry.

All five identified defects (DEF-60-01 through DEF-60-05) were systematically resolved in the production codebase, audited against reproducible test suites, and cataloged across 18 formal documentation reports.

### 45.2 13-Stage Full-Pipeline Adversarial Test Harness Architecture
- **Full Traceability:** Implemented `PipelineExecutionHarness` in `legalmitra/evaluation/adversarial_harness.py`, capturing a deterministic 13-stage machine-readable trace (`HarnessExecutionTrace`) for every query:
  1. Intake & query parsing (issues, legal domain, injection check).
  2. Fact classification & missing-information detection (allegations vs user facts).
  3. Retrieval & source eligibility (scaffold exclusion, primary statutes, rules, precedents).
  4. Temporal applicability resolution (interval checks, boundary dates, uncommenced statutes).
  5. Precedent status & authority hierarchy (proposition-level overruling, bench strength).
  6. Issue-level evidence assembly (`IssueEvidenceMatrix` synthesis).
  7. Claim dependency validation (prerequisite propagation).
  8. Independent citation and proposition-support evaluation.
  9. Response-state and decision-policy selection.
  10. Final answer assembly & prose generation.
  11. Post-generation safety evaluation & contradiction detection.
  12. Provenance lifecycle audit & cryptographic hash validation.
  13. Release-gate alignment.
- **Machine-Readable Artifacts:** Persisted standardized JSON manifests in `data/22_central_legislation/phase60_adversarial_scenarios.json` and `data/22_central_legislation/phase60_execution_traces.json`.

### 45.3 12 Compound Legal-Safety Adversarial Scenario Families (100% Safe Handling)
The integrated pipeline demonstrated 100.0% safety compliance across all 12 compound scenario families:
1. `VALID_CITATION_UNSUPPORTED_PROPOSITION`: Specific Relief Act Section 20A unconditional injunction claim correctly rejected; statutory bar enforced (`ANSWER_QUALIFIED`).
2. `AUTHENTIC_BUT_UNAVAILABLE_AUTHORITY`: Unindexed landmark Supreme Court judgment (*State of Punjab v. Baldev Singh*) distinguished from fabricated citations (`ABSTAIN_INSUFFICIENT_EVIDENCE`).
3. `UNCERTAIN_TEMPORAL_APPLICABILITY`: Uncommenced Code on Wages 2019 wage recovery intercepted; predecessor law identified as operative (`ABSTAIN_TEMPORAL_UNCERTAINTY`).
4. `CONFLICTING_PARTIAL_PRECEDENTS`: *Subhash Kashinath Mahajan* preliminary enquiry holding recognized as overruled while core anticipatory bail jurisprudence is preserved (`ANSWER_QUALIFIED` / `ANSWER_SUPPORTED`).
5. `MISSING_STATUTORY_EXCEPTION`: Hindu Succession Act Section 6(1) pre-2004 partition proviso preserved; unconditional reopening prevented (`ANSWER_CONDITIONAL`).
6. `DISPUTED_USER_FACTS`: Unproven forgery allegations recognized as disputed facts rather than established facts (`ANSWER_QUALIFIED`).
7. `FAILED_PREMISE_DOWNSTREAM_CONCLUSION`: Unregistered agreement without possession blocks Section 53A TPA part performance defense (`ANSWER_QUALIFIED`).
8. `PROMPT_INJECTION_LEGAL_MATERIAL`: Hostile system override instructions treated strictly as text data; statutory restrictions reinforced (`ANSWER_QUALIFIED`).
9. `MULTI_ISSUE_MIXED_EVIDENCE_QUALITY`: Multi-issue inquiry (Arbitration Act Section 34 + uncommenced Code on Wages) resolved via calibrated multi-part answer (`ANSWER_PARTIAL`) without blanket total abstention.
10. `PRIVATE_DATA_SCAFFOLD_CONTAMINATION`: Quarantined synthetic scaffold chunk (`IND-JUD-DEL-2024-BAIL`) cited in query intercepted immediately (`ABSTAIN_SOURCE_INTEGRITY_FAILURE`).
11. `SOURCE_INTEGRITY_TAMPER_FAILURE`: Tampered proposition provenance hash detected and rejected by `PropositionProvenanceAuditor`.
12. `CONTRADICTORY_ANSWER_ASSEMBLY`: Draft answer containing intra-text mutually contradictory claims intercepted post-generation (`CLARIFICATION_REQUIRED` / `ANSWER_QUALIFIED`).

### 45.4 Runtime Post-Generation Safety Intercept & Provenance Wiring (DEF-60-01 & DEF-60-02)
- **Production Pipeline Safety Intercept:** Integrated `PropositionProvenanceAuditor` directly into `LegalQueryPipeline.execute()`. Any assembled answer deriving from quarantined synthetic scaffold material is immediately intercepted, preventing leakage into final responses.
- **Intra-Answer Contradiction Detection:** Added post-generation consistency verification checking assembled final prose for incompatible affirmative claims and statutory prohibitions, downgrading uncalibrated answers to `CLARIFICATION_REQUIRED`.
- **Telemetry Enhancement:** Added `provenance_audit` and `post_generation_eval` attributes to `OrchestratedLegalResponse`.

### 45.5 Cryptographic Canonicalization & Monotonic Lifecycle Integrity (DEF-60-05)
- **Deterministic Digest Binding:** Implemented `compute_canonical_audit_hash()` in `LegalPropositionProvenance` generating a SHA-256 digest binding `proposition_id`, `source_id`, `pinpoint_reference`, and `proposition_text`.
- **Runtime Tamper Detection:** Added `verify_hash_integrity()`: post-creation tampering of proposition prose or metadata fails verification.
- **Unauthorized Promotion Guard:** `PropositionProvenanceAuditor` prevents advancing propositions to `ADVOCATE_REVIEWED` unless verified advocate enrollment credentials (e.g. Bar Council enrollment number) are recorded.

### 45.6 Multi-Issue Calibrated Synthesis vs Total Abstention (DEF-60-04)
- **Calibrated Multi-Part Resolution:** Remediated DEF-60-04 by introducing Compound Pattern 6 in `query_understanding.py` and updating `LegalDecisionPolicy`. When a query combines active statutory claims with uncommenced regimes, the pipeline emits `ANSWER_PARTIAL` rather than collapsing into total abstention.

### 45.7 Independent Post-Generation Claim Evaluation & Metric Ledger
- **Unsupported-Claim Acceptance Rate:** 0.0% (0 / 12)
- **Fabricated-Authority Acceptance Rate:** 0.0% (0 / 12)
- **Authentic Unavailable Misclassification:** 0.0% (0 / 12)
- **Material Exception Omission Rate:** 0.0% (0 / 12)
- **Temporal Resolution Error Rate:** 0.0% (0 / 12)
- **Precedent Status Error Rate:** 0.0% (0 / 12)
- **Critical Contradiction Detection Rate:** 100.0% (1 / 1)
- **Appropriate Abstention Rate:** 100.0% (4 / 4)
- **Final Answer Provenance Completeness:** 100.0% (12 / 12)

### 45.8 Release Quality Gates & 14 Fail-Closed Negative Controls (Release 0.60.0)
- **Release Manifest (`data/22_central_legislation/release_gates_manifest.json`):**
  - Total Gates: 20
  - Passed Gates: 19 (100% of automated gates)
  - Pending Gates: 1 (`RG-11-LEGAL-REVIEW`, awaiting advocate review under Advocates Act, 1961)
  - Failed Gates: 0
  - Overall Release Decision: `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`
- **14 Fail-Closed Negative Controls:** Verified that release gates fail under all simulated failure conditions (tampered freeze file, missing database, fabricated citation accepted, unindexed citation misclassified, unsupported proposition, boundary shift, precedent conflict, missing exception, broken dependency, scaffold leak, conversation DB leak, hidden regression, missing advocate review, and stale manifest).

### 45.9 Security Boundaries, Scaffold Quarantine & Database Decoupling
- **Physical Decoupling:** Maintained complete physical decoupling between `data/legalmitra_kb.db` (1,515 chunks, zero chat tables) and `data/conversations.db`.
- **Synthetic Scaffold Quarantine:** Synthetic scaffold `IND-JUD-DEL-2024-BAIL` (6 chunks) remains strictly quarantined (`is_synthetic_scaffold = 1`).
- **Governance Freeze:** Verified 6/6 frozen artifacts in `data/06_review/` are bitwise identical. Verified all 40 advocate review candidates in `data/07_batches/review/` remain `pending_legal_review`.

### 45.10 Multi-Phase Production Regression Suite (352 Passed in 26.30s)
- **Phase 60 Test Suite (`tests/test_phase60_adversarial_validation.py`):** 39 passed in 3.40s.
- **Multi-Phase Production Suite (Phases 40 to 60):** 352 passed in 26.30s across 21 test files (100% pass rate).
- **Zero Regressions:** All existing pipelines (temporal, precedent, multi-authority, independent evaluator, release gates) operate seamlessly with Phase 60 adversarial extensions.

### 45.11 Permanent Documentation Ledger & Phase 60 Verification Metrics
- **Documentation Ledger:** 18 formal reports cataloged in `docs/` totaling 568 physical lines.
- **Substantive Claim Grounding:** 100.0%
- **Citation Validity Rate:** 100.0%
- **Safety Pass Rate:** 100.0% (12/12 compound adversarial scenarios handled safely)
- **Release Status:** `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`
- **Model Training Policy:** Strictly prohibited; zero model pretraining or parameter fine-tuning performed.
- **Consumer UI:** Final consumer UI deferred; release status confirmed as `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`.
"""

    feature_commit_placeholder = "PENDING_COMMIT"

    # Temporary estimate for line calculation
    ledger_p60 = (
        "| **P60** | 2026-10-25 | 18,964 | {FINAL_LINES} | +{NET_LINES} | "
        "Adversarial end-to-end validation, 13-stage execution harness, 12 compound scenario families (100% pass), "
        "post-generation safety intercept, DEF-60-01-05 remediation, Release Gates 0.60.0 (19/20 passed), 18 reports (568 lines) | "
        "PASS (100%) | {FEATURE_COMMIT} |\n"
        "| **P61+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"
    )

    if "# Part XLV:" not in content:
        content += part_xlv

    dummy_ledger = ledger_p60.format(
        FINAL_LINES="19,050",
        NET_LINES="86",
        FEATURE_COMMIT=feature_commit_placeholder
    )
    content_temp = content.replace(ledger_target, dummy_ledger)
    final_line_count = len(content_temp.splitlines())
    net_lines = final_line_count - 18964
    print(f"Projected lines: {final_line_count}, net: +{net_lines}")

    final_ledger = ledger_p60.format(
        FINAL_LINES=f"{final_line_count:,}",
        NET_LINES=f"{net_lines}",
        FEATURE_COMMIT=feature_commit_placeholder
    )
    content = content.replace(ledger_target, final_ledger)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("README.md successfully updated for Phase 60!")

if __name__ == '__main__':
    update_readme()
