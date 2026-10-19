"""
Script to update README.md for Phase 52.
1. Adds Part XXXVII: Legal Source Integrity, Corpus Coverage Gap Analysis, Rights Verification & Evidence Reliability (Phase 52)
2. Updates TOC with Part XXXVII links
3. Updates Section 24.6 Permanent Phase Documentation Ledger
"""

import re
from pathlib import Path

README_PATH = Path("README.md")

TOC_PHASE52 = """- [Part XXXVII: Legal Source Integrity, Corpus Coverage Gap Analysis, Rights Verification & Evidence Reliability (Phase 52)](#part-xxxvii-legal-source-integrity-corpus-coverage-gap-analysis-rights-verification--evidence-reliability-phase-52)
  - [37.1 Authoritative Corpus Inventory & Forensic Reconciliation Report](#371-authoritative-corpus-inventory--forensic-reconciliation-report)
  - [37.2 Source Authenticity, Gazette Verification & Temporal Provenance Mapping](#372-source-authenticity-gazette-verification--temporal-provenance-mapping)
  - [37.3 Source Rights, Copyright Compliance & Pretraining Prohibition Invariant](#373-source-rights-copyright-compliance--pretraining-prohibition-invariant)
  - [37.4 Legal Coverage Gap Analysis Across 17 Jurisprudential Domains](#374-legal-coverage-gap-analysis-across-17-jurisprudential-domains)
  - [37.5 Prioritized Legal Acquisition Backlog & High-Risk Domain Identification](#375-prioritized-legal-acquisition-backlog--high-risk-domain-identification)
  - [37.6 Evidence Eligibility Engine & Fail-Closed Retrieval Safeguards](#376-evidence-eligibility-engine--fail-closed-retrieval-safeguards)
  - [37.7 Point-in-Time Benchmark Suite V8 (LEGALMITRA-BENCHMARK-PIT-V8: 120 Cases)](#377-point-in-time-benchmark-suite-v8-legalmitra-benchmark-pit-v8-120-cases)
  - [37.8 Machine-Readable Release Quality Gates (Phase 52 Evaluation)](#378-machine-readable-release-quality-gates-phase-52-evaluation)
  - [37.9 Defect Register, Failure Taxonomy & Pipeline Safeguards](#379-defect-register-failure-taxonomy--pipeline-safeguards)
  - [37.10 Operational Runbooks: Source Integrity, Rights & Eligibility (Runbooks 54–56)](#3710-operational-runbooks-source-integrity-rights--eligibility-runbooks-5456)
  - [37.11 Phase-by-Phase Engineering Chronicle: Phase 52 Execution Digest](#3711-phase-by-phase-engineering-chronicle-phase-52-execution-digest)
  - [37.12 Strategic Roadmap: Phase 53 Enterprise Multi-Agent Synthesis & Cross-Border Indian Law](#3712-strategic-roadmap-phase-53-enterprise-multi-agent-synthesis--cross-border-indian-law)
"""

PART_XXXVII_BODY = """
---

## Part XXXVII: Legal Source Integrity, Corpus Coverage Gap Analysis, Rights Verification & Evidence Reliability (Phase 52)

### 37.1 Authoritative Corpus Inventory & Forensic Reconciliation Report

Phase 52 established a machine-readable, forensic corpus inventory reconciler (`legalmitra/corpus/inventory_reconciler.py`) verifying physical alignment between registered sources, raw filesystem files, and SQLite database tables:
- **Registered & Acquired Sources**: 59 distinct sources verified across central statutes (26), judicial precedents (23), delegated rules (4), gazette notifications (5), and diagnostic test fixtures (1).
- **Indexed Chunks**: Exactly 1,505 rows in `legal_chunks` (1,499 active production chunks, 6 quarantined scaffold chunks).
- **Orphan Chunks & Duplicate IDs**: 0 orphan chunks (all 1,505 chunks join cleanly to `sources.document_id`); 0 duplicate source IDs; 0 stale index records.
- **Empty Sources Accounted For**: Exactly 2 sources contain 0 chunks: `IND-UNSUPPORTED-001` (test fixture for negative format verification) and `IND-GUIDE-SCI-PROC-2025` (unparsed 278-page Supreme Court practice handbook). Both are classified as `UNPROCESSED_FIXTURE` and blocked from retrieval.
- **Manifest**: `data/22_central_legislation/corpus_inventory_reconciliation.json` (`CORPUS-RECONCILIATION-PHASE52`).

### 37.2 Source Authenticity, Gazette Verification & Temporal Provenance Mapping

Implemented `SourceAuthenticityVerifier` (`legalmitra/corpus/authenticity.py`) providing primary official publication provenance, Gazette of India notification references, digital repository URLs (India Code / Supreme Court / High Courts), content checksums, and temporal classifications:
- **56 Authentic Primary Sources**: Primary statutory enactments and binding court rulings verified against official gazette notifications and official law reports.
- **1 Synthetic Test Scaffold**: `IND-JUD-DEL-2024-BAIL` classified as `SYNTHETIC_TEST_SCAFFOLD` and quarantined.
- **2 Diagnostic Fixtures**: `IND-UNSUPPORTED-001` and `IND-GUIDE-SCI-PROC-2025` classified as `UNPROCESSED_FIXTURE`.
- **Temporal Status Breakdown**: 57 `TEMPORALLY_VERIFIED`, 1 `PARTIALLY_IN_FORCE` (DPDP Act 2023), 1 `PROSPECTIVELY_AMENDED` (IT Act 2000).
- **Manifest**: `data/22_central_legislation/source_authenticity_register.json` (`SOURCE-AUTHENTICITY-REGISTER-PHASE52`).

### 37.3 Source Rights, Copyright Compliance & Pretraining Prohibition Invariant

Built `SourceRightsEngine` (`legalmitra/corpus/rights.py`) cataloging copyright exemptions and data licensing standards:
- **Section 52(1)(q) of the Copyright Act, 1957**: Reproduction of matter published in the Official Gazette (s.52(1)(q)(i)), acts of legislature (s.52(1)(q)(ii)), and court/tribunal judgments (s.52(1)(q)(iv)) does not constitute copyright infringement.
- **GODL-India**: Government Open Data License applies to central datasets.
- **Strict Prohibition on Foundation Model Pretraining**: Non-negotiable architectural invariant: Zero-shot retrieval-augmented orchestration is permitted; pretraining or fine-tuning foundation model weights on repository text is **STRICTLY PROHIBITED (NON-NEGOTIABLE)**.
- **Manifest**: `data/22_central_legislation/source_rights_registry.json` (`SOURCE-RIGHTS-REGISTRY-PHASE52`).

### 37.4 Legal Coverage Gap Analysis Across 17 Jurisprudential Domains

Implemented `CoverageGapAnalyzer` (`legalmitra/corpus/coverage_gaps.py`) auditing corpus completeness across 17 distinct legal domains of Indian jurisprudence:
- **High Coverage (8 domains)**: Criminal Law & Transition, Constitutional Law, Commercial Arbitration, Contracts & Property, Civil Procedure, Consumer Protection, Motor Accidents, Information Governance (RTI).
- **Moderate Coverage (5 domains)**: IT & Data Privacy, Banking & NI Act, Intellectual Property (IPR), Labour & Industrial Welfare, State Rent & Police Laws.
- **Low Coverage (4 domains)**: Corporate Law & Insolvency (IBC), Direct & Indirect Taxation, Environmental Law, Family & Succession Law.
- **Manifest**: `data/22_central_legislation/coverage_gap_analysis.json` (`COVERAGE-GAP-ANALYSIS-PHASE52`).

### 37.5 Prioritized Legal Acquisition Backlog & High-Risk Domain Identification

Formulated a prioritized acquisition backlog to prevent hallucination in complex or high-volume litigation areas:
1. **Rank 1 (CRITICAL)**: *Insolvency and Bankruptcy Code, 2016 (IBC)* — Section 7/9 financial debt admission standards and Section 14 moratorium rules.
2. **Rank 2 (HIGH)**: *Hindu Succession Act, 1956 (Section 6)* — Coparcenary rights and gender parity (*Vineeta Sharma* 2020) authentic statutory chunks.
3. **Rank 3 (HIGH)**: *Patents Act, 1970 (Section 3(d))* — Technical patentability and therapeutic efficacy doctrines (*Novartis* 2013).
4. **Rank 4 (MEDIUM)**: *Central Goods and Services Tax Act, 2017* — High-complexity fiscal statute; transitional input tax credit guards.
5. **Rank 5 (MEDIUM)**: *National Green Tribunal Act, 2010* — Section 14 and 15 environmental limitation and polluter pays doctrines.

### 37.6 Evidence Eligibility Engine & Fail-Closed Retrieval Safeguards

Built `EvidenceEligibilityEngine` (`legalmitra/corpus/eligibility.py`) and integrated it into `UnifiedEvidenceOrchestrator`:
- **Fail-Closed Retrieval**: Unregistered sources, unsupported format fixtures, and synthetic scaffolds are rejected prior to answer assembly.
- **Scaffold Quarantine Enforcement**: Chunks with `is_synthetic_scaffold = 1` or source `IND-JUD-DEL-2024-BAIL` are strictly filtered.
- **Temporal Warning Generation**: Queries evaluated against post-dated statutes or unnotified provisions receive explicit temporal warnings.

### 37.7 Point-in-Time Benchmark Suite V8 (LEGALMITRA-BENCHMARK-PIT-V8: 120 Cases)

Expanded the temporal benchmark from 100 cases (`PIT-V7`) to **120 cases (`PIT-V8`)**, adding 20 rigorous test cases (`PIT-101` to `PIT-120`):
- **Partitioning**: 50 Development (`PIT-01` to `PIT-50`), 20 Validation (`PIT-51` to `PIT-70`), **50 Held-Out Evaluation (`PIT-71` to `PIT-120`)**.
- **Contamination Audit**: 0 exact duplicates, 0 near-duplicates, maximum cross-split token Jaccard similarity of **0.3636** (well below the 0.85 threshold). Held-out split is strictly non-contaminated.

### 37.8 Machine-Readable Release Quality Gates (Phase 52 Evaluation)

Evaluated all 11 release gates via `ReleaseGateEvaluator`:
- **Release ID**: `LEGALMITRA-RELEASE-PHASE52` | **Target Version**: `0.52.0`.
- **Passed Gates (10)**: RG-01 (Provenance), RG-02 (Temporal Correctness), RG-03 (Precedent Hierarchy), RG-04 (Claim Grounding), RG-05 (Abstention/Clarification), RG-06 (Anti-Hallucination), RG-07 (Adversarial Robustness), RG-08 (Database Isolation), RG-09 (Regression Integrity), RG-10 (Held-Out Evaluation).
- **Pending Gate (1)**: RG-11 (Mandatory Advocate Sign-Off — 40 candidates in `pending_legal_review`).
- **Overall Decision**: **`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`**.
- **Manifest**: `data/22_central_legislation/release_gates_manifest.json`.

### 37.9 Defect Register, Failure Taxonomy & Pipeline Safeguards

Tracked and remediated 5 defects (`DEF-52-01` to `DEF-52-05`):
- Explicitly assigned `validation_verdict="UNSUPPORTED"` in `answer_assembler.py` for fabricated citation claims.
- Added `"cheating"` to decisive clarification trigger words in `query_understanding.py`.
- Normalized date types in `EvidenceEligibilityEngine` to prevent string/date comparison TypeError.
- Updated release gate evaluator RG-10 threshold to expect 50 held-out cases.
- Flexible version assertions in test harness accommodating benchmark expansions.

### 37.10 Operational Runbooks: Source Integrity, Rights & Eligibility (Runbooks 54–56)

Operational execution procedures documented in three dedicated runbooks:
- **Runbook 54 (`docs/PHASE52_RUNBOOK_54_SOURCE_INTEGRITY_AUDIT.md`)**: Auditing primary sources, calculating content checksums, and registering Gazette references.
- **Runbook 55 (`docs/PHASE52_RUNBOOK_55_RIGHTS_VERIFICATION.md`)**: Verifying Section 52(1)(q) copyright compliance and enforcing model training exclusion.
- **Runbook 56 (`docs/PHASE52_RUNBOOK_56_EVIDENCE_ELIGIBILITY_ENFORCEMENT.md`)**: Verifying fail-closed retrieval guards and scaffold quarantine.

### 37.11 Phase-by-Phase Engineering Chronicle: Phase 52 Execution Digest

Phase 52 established reproducible legal source integrity and evidence reliability for LegalMitra:
1. **Corpus Inventory Reconciliation**: Reconciled 59 sources, 1,505 chunks, 0 orphans, 0 duplicates, 0 stale records.
2. **Authenticity & Gazette Verification**: Verified 56 authentic primary sources, 1 quarantined scaffold, 2 diagnostic fixtures.
3. **Rights & Pretraining Exclusion**: Cataloged Section 52(1)(q) and GODL-India rights; enforced strict pretraining ban.
4. **Coverage Gap Analysis**: Audited 17 legal domains; published 5-tier prioritized acquisition backlog.
5. **Evidence Eligibility Engine**: Implemented fail-closed retrieval guards integrated into orchestrator.
6. **Benchmark PIT-V8 (120 Cases)**: Expanded suite with 50 held-out cases; verified 0 contamination (0.3636 max similarity).
7. **Release Quality Gates**: 10 Passed, 0 Failed, 1 Pending Advocate Review (`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`).
8. **Regression & Freeze Verification**: 100% Phase 9 freeze compliance (6 files), 40 review candidates pending, 171/171 phase tests passed.
9. **Comprehensive Documentation**: Authored 16 mandated reports in `docs/` and integrated Part XXXVII into root `README.md`.

### 37.12 Strategic Roadmap: Phase 53 Enterprise Multi-Agent Synthesis & Cross-Border Indian Law

Following Phase 52 source integrity verification, Phase 53 will focus on:
1. **Autonomous Multi-Agent Topology**: Deploying specialized sub-agents (Statutory Specialist, Case Law Analyst, Procedural Checker, Red-Team Validator) operating under a central supervisor.
2. **Cross-Border Indian Law & Commercial Arbitration**: Integrating Indian Bilateral Investment Treaties (BITs), UNCITRAL model law alignment, and enforcement of foreign arbitral awards under the New York Convention.
3. **Advocate Review Candidate Processing Pipeline**: Providing review tooling for licensed legal advocates to audit and score the 40 frozen review candidates once formal review initiates.
"""

LEDGER_ENTRY_P52 = """| **P52** | 2026-10-19 | 18,157 | {final_lines} | +{net_increase} | Legal source integrity, corpus inventory reconciliation (59 sources, 1,505 chunks), authenticity & Gazette register, Section 52(1)(q) rights registry, 17-domain coverage gap analysis & backlog, evidence eligibility engine, benchmark PIT-V8 (120 cases, 50 held-out), 16 reports | PASS (100%) | {commit_hash} |
| **P53+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |
"""


def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update TOC: insert after Part XXXVI
    toc_marker = "  - [36.11 Phase-by-Phase Engineering Chronicle: Phase 51 Execution Digest](#3611-phase-by-phase-engineering-chronicle-phase-51-execution-digest)\n"
    if toc_marker in content and "#part-xxxvii" not in content:
        content = content.replace(toc_marker, toc_marker + TOC_PHASE52)
        print("Updated TOC with Part XXXVII")

    # 2. Append Part XXXVII before EOF
    if "## Part XXXVII:" not in content:
        content = content.rstrip() + "\n" + PART_XXXVII_BODY
        print("Appended Part XXXVII body")

    # 3. Update Section 24.6 ledger table
    ledger_p52_placeholder = "| **P52+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"
    
    # Calculate preliminary line count
    lines = content.splitlines()
    total_lines = len(lines)
    net_inc = total_lines - 18157

    p52_row = LEDGER_ENTRY_P52.format(
        final_lines=f"{total_lines:,}",
        net_increase=f"{net_inc:,}",
        commit_hash="`PENDING_FEATURE_COMMIT`"
    )

    if ledger_p52_placeholder in content:
        content = content.replace(ledger_p52_placeholder, p52_row)
        print("Updated Section 24.6 ledger row")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")

    print(f"README.md successfully updated. Total lines: {len(content.splitlines())}")


if __name__ == "__main__":
    update_readme()
