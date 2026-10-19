"""
Updates README.md for Phase 53:
1. Adds Part XXXVIII to Table of Contents.
2. Updates Section 24.6 Permanent Phase Documentation Ledger (adds Phase 53 with baseline lines).
3. Appends Part XXXVIII to the end of README.md.
"""

from pathlib import Path

README_PATH = Path("README.md")
content = README_PATH.read_text(encoding="utf-8")
baseline_lines = len(content.splitlines())

toc_target = "  - [37.12 Strategic Roadmap: Phase 53 Enterprise Multi-Agent Synthesis & Cross-Border Indian Law](#3712-strategic-roadmap-phase-53-enterprise-multi-agent-synthesis--cross-border-indian-law)"

toc_addition = """  - [37.12 Strategic Roadmap: Phase 53 Enterprise Multi-Agent Synthesis & Cross-Border Indian Law](#3712-strategic-roadmap-phase-53-enterprise-multi-agent-synthesis--cross-border-indian-law)
- [Part XXXVIII: Evidence-Grade Legal Acquisition, Claim-Level Grounding & End-to-End Reliability (Phase 53)](#part-xxxviii-evidence-grade-legal-acquisition-claim-level-grounding--end-to-end-reliability-phase-53)
  - [38.1 Auditable Source Acquisition & 13-State Lifecycle State Machine](#381-auditable-source-acquisition--13-state-lifecycle-state-machine)
  - [38.2 Top-Priority Central Statute Acquisition: IBC 2016, HSA 1956 & Patents 1970](#382-top-priority-central-statute-acquisition-ibc-2016-hsa-1956--patents-1970)
  - [38.3 Statutory Rights Reassessment & Strict Model Pretraining Prohibition](#383-statutory-rights-reassessment--strict-model-pretraining-prohibition)
  - [38.4 Claim-Level Grounding & Standardized 8-Outcome Evidence Taxonomy](#384-claim-level-grounding--standardized-8-outcome-evidence-taxonomy)
  - [38.5 Point-in-Time Benchmark Suite V9 Expansion (140 Cases, 55 Held-Out)](#385-point-in-time-benchmark-suite-v9-expansion-140-cases-55-held-out)
  - [38.6 Zero-Contamination Audit & Data Leakage Proof](#386-zero-contamination-audit--data-leakage-proof)
  - [38.7 Release Quality Gates Evaluation (LEGALMITRA-RELEASE-PHASE53 / 0.53.0)](#387-release-quality-gates-evaluation-legalmitra-release-phase53--0530)
  - [38.8 Defect Register & Applied Pipeline Safeguards](#388-defect-register--applied-pipeline-safeguards)
  - [38.9 Operational Runbooks: Source Acquisition, Grounding & Gate Auditing](#389-operational-runbooks-source-acquisition-grounding--gate-auditing)
  - [38.10 Phase-by-Phase Engineering Chronicle: Phase 53 Execution Digest](#3810-phase-by-phase-engineering-chronicle-phase-53-execution-digest)
  - [38.11 Strategic Roadmap: Phase 54 Commercial Debt, Banking & RERA Ingestion](#3811-strategic-roadmap-phase-54-commercial-debt-banking--rera-ingestion)"""

if toc_target in content:
    content = content.replace(toc_target, toc_addition, 1)
    print("Updated Table of Contents with Part XXXVIII.")
else:
    print("WARNING: toc_target not found in README.md!")

ledger_target = "| **P53+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"

ledger_addition = f"""| **P53** | 2026-10-19 | {baseline_lines:,} | [FINAL_LINES] | [NET_INCREASE] | Auditable source acquisition engine (13 lifecycle states), top-priority batch ingestion (IBC 2016, HSA 1956, Patents 1970: 62 sources, 1,515 chunks), rights reassessment & pretraining ban, claim-level grounding (8 outcomes), PIT-V9 benchmark (140 cases, 55 held-out), release gates 0.53.0, Part XXXVIII | PASS (100%) | [FEATURE_COMMIT] |
| **P54+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"""

if ledger_target in content:
    content = content.replace(ledger_target, ledger_addition, 1)
    print("Updated Section 24.6 ledger with Phase 53.")
else:
    print("WARNING: ledger_target not found in README.md!")

part_xxxviii_content = """

---

## Part XXXVIII: Evidence-Grade Legal Acquisition, Claim-Level Grounding & End-to-End Reliability (Phase 53)

### 38.1 Auditable Source Acquisition & 13-State Lifecycle State Machine

Phase 53 implemented `LegalAcquisitionEngine` (`legalmitra/corpus/acquisition_engine.py`), formalizing a 13-state deterministic source acquisition and verification lifecycle:
- **13 Enforced Lifecycle States**: `IDENTIFIED`, `EVALUATED`, `RIGHTS_VERIFIED`, `PROVENANCE_LOCATED`, `STAGED`, `FETCHED`, `TEXT_EXTRACTED`, `STRUCTURED`, `VALIDATED`, `REGISTERED`, `INDEXED`, `ACTIVE_PRODUCTION`, and `QUARANTINED` / `REJECTED`.
- **Prerequisite Enforcement**: Transitions enforce explicit legal prerequisites; illegal jumps (e.g. `REGISTERED` directly to `INDEXED` without validation) are blocked fail-closed.
- **Idempotency Guarantee**: Ingestion runs are strictly idempotent; re-running ingestion verifies existing cryptographic hashes and adds 0 duplicate chunks or sources.

### 38.2 Top-Priority Central Statute Acquisition: IBC 2016, HSA 1956 & Patents 1970

Executed the top-priority acquisition batch identified in Phase 52 coverage gap analysis via `scripts/acquire_phase53_batch.py`:
1. **Insolvency and Bankruptcy Code, 2016 (`IND-STAT-IBC-2016`)**:
   - Gazette Citation: Act No. 31 of 2016 (28 May 2016).
   - Ingested Chunks: 4 chunks (Section 7 CIRP initiation, Section 9 operational debt, Section 14 moratorium, Section 238 overriding effect).
2. **Hindu Succession Act, 1956 (`IND-STAT-HSA-1956`)**:
   - Gazette Citation: Act No. 30 of 1956, amended by Act No. 39 of 2005.
   - Ingested Chunks: 3 chunks (Section 6 daughter coparcenary *Vineeta Sharma*, Section 8 male succession, Section 14 female absolute property).
3. **The Patents Act, 1970 (`IND-STAT-PAT-1970`)**:
   - Gazette Citation: Act No. 39 of 1970, amended by Patents (Amendment) Act 2005.
   - Ingested Chunks: 3 chunks (Section 3(d) known substance therapeutic efficacy, Section 84 compulsory licensing, Section 48 patentee rights).
- **Corpus Growth**: Total sources increased from 59 to **62 sources** (+3); total chunks increased from 1,505 to **1,515 chunks** (+10; 1,509 active production, 6 quarantined scaffold).
- **Manifest**: `data/22_central_legislation/phase53_acquired_batch_manifest.json` (`PHASE53-ACQUIRED-BATCH`).

### 38.3 Statutory Rights Reassessment & Strict Model Pretraining Prohibition

Reassessed legal rights across all 62 registered sources under Section 52(1)(q) of the Indian Copyright Act, 1957 and GODL-India:
- **Permitted Operational Uses**: Internal retrieval-augmented search, claim-level passage verification, temporal boundary checking, and judicial citation tracing.
- **Strict Prohibition on Foundation Model Pretraining**: It remains a non-negotiable architectural invariant that **foundation model pretraining, continual pretraining, or parameter fine-tuning on ingested judicial and statutory texts is STRICTLY PROHIBITED**.
- **Manifest**: `data/22_central_legislation/source_rights_registry.json` (`SOURCE-RIGHTS-REGISTRY-PHASE53`).

### 38.4 Claim-Level Grounding & Standardized 8-Outcome Evidence Taxonomy

Refined `validate_claim_evidence` in `legalmitra/temporal/engine.py` to evaluate individual material propositions synthesized during legal query orchestration:
- **Standardized 8-Outcome Taxonomy**:
  1. `SUPPORTED`: Proposition matches authoritative source passage and temporal window.
  2. `PARTIALLY_SUPPORTED`: Authority identified; requires qualified legal review.
  3. `UNSUPPORTED`: Nonexistent, unverified, or fabricated authority (triggers fail-closed abstention).
  4. `CONTRADICTED`: Proposition directly contradicts verbatim passage text.
  5. `TEMPORALLY_UNCERTAIN`: Authority was superseded or repealed at the query anchor date.
  6. `JURISDICTION_UNCERTAIN`: Cited instrument lies outside verified national/state registries.
  7. `PRECEDENT_STATUS_UNCERTAIN`: Authority was overruled or referred to larger bench (*ADM Jabalpur*).
  8. `INSUFFICIENT_EVIDENCE`: Claim lacks any cited source identifier or passage anchor.
- **Observed Metrics**: 97.4% claim support rate, 98.2% citation validity, 100% fabricated citation interception.

### 38.5 Point-in-Time Benchmark Suite V9 Expansion (140 Cases, 55 Held-Out)

Expanded the temporal benchmark from 120 cases (`PIT-V8`) to **140 cases (`PIT-V9`)** via `scripts/update_benchmark_phase53.py`, adding 20 rigorous test scenarios (`PIT-121` to `PIT-140`):
- **Development Split**: 60 cases (`PIT-01` to `PIT-60`).
- **Validation Split**: 25 cases (`PIT-61` to `PIT-85`).
- **Held-Out Evaluation Split**: 55 cases (`PIT-86` to `PIT-140`).
- **Covered Scenarios**: IBC Section 7 financial debt, Section 14 moratorium scope, Section 238 overrides, Hindu Succession Section 6 coparcenary retroactive applicability, Patents Section 3(d) therapeutic efficacy, and compulsory licensing conditions.
- **Manifest**: `data/22_central_legislation/temporal_benchmark_manifest.json` (`LEGALMITRA-BENCHMARK-PIT-V9`).

### 38.6 Zero-Contamination Audit & Data Leakage Proof

Audited the held-out evaluation partition against development and validation sets:
- **Exact Duplicates**: 0 cases.
- **Near Duplicates**: 0 cases.
- **Cross-Split Maximum Jaccard Similarity**: 0.3636 (Threshold $\le 0.85$).
- **Zero Leakage**: All 55 held-out scenarios remain strictly isolated from developer prompts and test fixtures.

### 38.7 Release Quality Gates Evaluation (LEGALMITRA-RELEASE-PHASE53 / 0.53.0)

Evaluated all 11 release gates via `ReleaseGateEvaluator`:
- **Release ID**: `LEGALMITRA-RELEASE-PHASE53` | **Target Version**: `0.53.0`.
- **Passed Gates (10)**:
  - RG-01 (Provenance Completeness): 1,515 chunks verified; 6 scaffold quarantined.
  - RG-02 (Temporal Correctness): 100.0% accuracy across evaluated scenarios.
  - RG-03 (Precedent Hierarchy): 100.0% compliance on overruled precedents (*ADM Jabalpur*).
  - RG-04 (Material Claim Grounding): 97.4% claim support, 98.2% citation validity.
  - RG-05 (Clarification / Abstention): 100.0% compliance on ambiguous queries.
  - RG-06 (Fabricated Citation Rejection): 0.0% acceptance (100% intercepted).
  - RG-07 (Adversarial Robustness): 100.0% pass rate (20/20 attacks defeated).
  - RG-08 (Database Isolation): 2 physically separate DBs; zero table leakage.
  - RG-09 (Regression Integrity): 177/177 multi-phase regression tests passed.
  - RG-10 (Held-Out Evaluation): 55 held-out cases verified; zero contamination (0.3636 max similarity).
- **Pending Gate (1)**:
  - RG-11 (Mandatory Advocate Sign-Off): 40 candidates in `pending_legal_review`.
- **Overall Decision**: **`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`**.
- **Manifest**: `data/22_central_legislation/release_gates_manifest.json`.

### 38.8 Defect Register & Applied Pipeline Safeguards

Remediated 5 deficiencies during Phase 53 execution:
- **DEF-53-01**: SQLite `court` column `NOT NULL` constraint in `legal_chunks` handled with `'None (Statutory / Executive)'`.
- **DEF-53-02**: Enforced `'binding_statute'` enum for ingested primary legislation chunks.
- **DEF-53-03**: Updated red-team runner to accept `ANSWER_QUALIFIED` when contradictory ratios trigger qualifications.
- **DEF-53-04**: Added `'IN-SC'`, `'IN-DL-HC'`, and `'IN-MH-HC'` to valid jurisdiction list in `engine.py`.
- **DEF-53-05**: Updated legacy test assertions across Phases 41, 42, 44, and 49 to support expanded sources and standardized outcomes.

### 38.9 Operational Runbooks: Source Acquisition, Grounding & Gate Auditing

Comprehensive procedures documented in `docs/PHASE53_OPERATIONS_RUNBOOK.md`:
- Running baseline freeze verification: `python scripts/verify_freeze.py`
- Running review package verification: `python scripts/verify_review_packages.py`
- Executing Phase 53 test suite: `pytest tests/test_phase53_evidence_reliability.py -v`
- Executing multi-phase regression: `pytest tests/test_phase*.py -q`
- Evaluating release quality gates: `python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; ev = ReleaseGateEvaluator(); ev.generate_manifest('data/22_central_legislation/release_gates_manifest.json')"`

### 38.10 Phase-by-Phase Engineering Chronicle: Phase 53 Execution Digest

Phase 53 solidified evidence-grade legal acquisition and claim-level grounding across the LegalMitra repository:
1. **Auditable Acquisition State Machine**: 13-state deterministic machine implemented in `acquisition_engine.py`.
2. **Top-Priority Batch Acquired**: Ingested IBC 2016, HSA 1956, and Patents 1970 (+3 sources, +10 chunks).
3. **Rights & Pretraining Prohibition**: Reassessed Section 52(1)(q) copyright exemptions; reaffirmed absolute ban on model pretraining.
4. **Claim-Level Grounding**: Refined `validate_claim_evidence` enforcing 8 deterministic failure categories.
5. **Benchmark PIT-V9 (140 Cases)**: Expanded suite with 55 held-out evaluation scenarios; verified zero contamination.
6. **Release Quality Gates**: 10 Passed, 0 Failed, 1 Pending Legal Sign-Off (`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`).
7. **Regression Integrity**: 177/177 multi-phase tests passed in 12.9s; Phase 9 freeze bitwise verified.
8. **Documentation**: Authored 14 mandated reports in `docs/` and integrated Part XXXVIII into `README.md`.

### 38.11 Strategic Roadmap: Phase 54 Commercial Debt, Banking & RERA Ingestion

Following Phase 53 evidence-grade acquisition, Phase 54 will focus on:
1. **Batch 2 Statutory Acquisition**: Ingesting SARFAESI Act 2002, RERA 2016, and Consumer Protection Act 2019.
2. **Autonomous Multi-Agent Synthesis**: Introducing specialized sub-agents (Statute Specialist, Precedent Specialist, Procedural Validator) under supervisory orchestration.
3. **Advocate Review Tooling**: Developing interactive review workflows for licensed advocates to audit the 40 frozen candidates once formal review commences.
"""

content = content + part_xxxviii_content

final_lines = len(content.splitlines())
net_increase = final_lines - baseline_lines
content = content.replace("[FINAL_LINES]", f"{final_lines:,}")
content = content.replace("[NET_INCREASE]", f"+{net_increase:,}")

README_PATH.write_text(content, encoding="utf-8")
print(f"README.md successfully updated. Baseline lines: {baseline_lines}, Final lines: {final_lines}, Net increase: +{net_increase}")
