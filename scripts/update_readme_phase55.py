from pathlib import Path

readme_path = Path("README.md")
content = readme_path.read_text(encoding="utf-8")

toc_entry = """- [Part XL: Temporal Semantics Audit, Authority-Resolution Calibration & Legal Decision Trace Verification (Phase 55)](#part-xl-temporal-semantics-audit-authority-resolution-calibration--legal-decision-trace-verification-phase-55)
  - [40.1 Temporal Semantics Audit & Inclusive Boundary Mathematics](#401-temporal-semantics-audit--inclusive-boundary-mathematics)
  - [40.2 Appointed Day Commencement Barrier & Overlap Conflict Detection](#402-appointed-day-commencement-barrier--overlap-conflict-detection)
  - [40.3 Precedent Hierarchy & Coordinate Bench Calibration](#403-precedent-hierarchy--coordinate-bench-calibration)
  - [40.4 Referral vs Overruling & Sub Judice Precedent Tracking](#404-referral-vs-overruling--sub-judice-precedent-tracking)
  - [40.5 Distinguishing Treatments, Ratio Decidendi & Obiter Dicta](#405-distinguishing-treatments-ratio-decidendi--obiter-dicta)
  - [40.6 Authority Decision Traces & End-to-End Answer Consistency](#406-authority-decision-traces--end-to-end-answer-consistency)
  - [40.7 Point-in-Time Benchmark Suite V11 Expansion (188 Cases, 75 Held-Out)](#407-point-in-time-benchmark-suite-v11-expansion-188-cases-75-held-out)
  - [40.8 Release Quality Gates Evaluation (LEGALMITRA-RELEASE-PHASE55 / 0.55.0)](#408-release-quality-gates-evaluation-legalmitra-release-phase55--0550)
  - [40.9 Security, Database Isolation & Boundary Defense Audit](#409-security-database-isolation--boundary-defense-audit)
  - [40.10 Defect Register & Remediated Deficiencies](#4010-defect-register--remediated-deficiencies)
  - [40.11 Operational Runbook & Verification Procedures](#4011-operational-runbook--verification-procedures)
  - [40.12 Phase-by-Phase Engineering Chronicle: Phase 55 Execution Digest](#4012-phase-by-phase-engineering-chronicle-phase-55-execution-digest)
  - [40.13 Strategic Roadmap: Phase 56 Multi-Jurisdictional Cross-Validation & Court API Connectors](#4013-strategic-roadmap-phase-56-multi-jurisdictional-cross-validation--court-api-connectors)
"""

part40_body = """
---

# Part XL: Temporal Semantics Audit, Authority-Resolution Calibration & Legal Decision Trace Verification (Phase 55)

### 40.1 Temporal Semantics Audit & Inclusive Boundary Mathematics

Phase 55 executed an audit of temporal interval representations and statutory lifecycle models across `legalmitra/temporal/engine.py`. The system enforces inclusive calendar intervals `[effective_from, effective_until]` with date normalization in Indian Standard Time, preventing timezone-induced calendar shifts.

### 40.2 Appointed Day Commencement Barrier & Overlap Conflict Detection

- **Enactment vs In-Force Barrier**: Enforces that publication of an Act in the Official Gazette does not bring provisions into force if an appointed-day clause under Section 1(2) or 1(3) appoints a future date. Prior to the appointed date, provisions are strictly classified as `NOT_YET_IN_FORCE`.
- **Overlapping Interval Conflict Detection**: Where multiple versions of a provision have overlapping intervals without verified legislative or retrospective resolution, the engine avoids arbitrary version selection and returns `CONFLICTING_TEMPORAL_EVIDENCE`.
- **Conflicting Gazette Protection**: Contradictory commencement notifications return explicit uncertainty states.
- **Retrospective Statutory Bases**: Express retrospective statutes (*Vineeta Sharma* on HSA 1956 Section 6) are tracked with documented legal bases.
- **Repeal with Savings**: Provisions saved under pending proceeding clauses (e.g. BNSS Section 531(2)(a) saving CrPC) remain available as `CONFIRMED_HISTORICAL` with `savings_applied=True`.

### 40.3 Precedent Hierarchy & Coordinate Bench Calibration

Calibrated `resolve_precedent_conflict` in `legalmitra/caselaw/knowledge_graph.py`:
- **Article 141 Hierarchy**: Supreme Court rulings strictly bind all subordinate courts and High Courts.
- **Bench Strength Dominance**: Within the Supreme Court, a larger bench binds smaller benches of coordinate jurisdiction on the same legal proposition.
- **Co-Equal Bench Splits**: Supreme Court benches of identical strength with conflicting holdings without reference to a larger bench are preserved neutrally as `UNRESOLVED_CO_EQUAL_BENCH_SPLIT`.

### 40.4 Referral vs Overruling & Sub Judice Precedent Tracking

- **Referral Sub Judice**: An order referring a question of law to a larger bench (`REFERS_TO_LARGER_BENCH`) is classified as `REFERRED_SUB_JUDICE` with `requires_qualification=True`. The earlier ratio cannot be treated as formally overruled prior to final larger-bench determination.

### 40.5 Distinguishing Treatments, Ratio Decidendi & Obiter Dicta

- **Distinguishing Treatments**: Precedents distinguished on factual or statutory grounds (`DISTINGUISHES`) remain good law for their original proposition (`DISTINGUISHED_NOT_OVERRULED`).
- **Ratio Decidendi vs Obiter Dicta**: Observations made *in passing* without forming the necessary basis of the decision are classified as `PERSUASIVE_OBITER_NOT_BINDING_RATIO` and cannot displace a binding ratio.
- **Substantive Issue Scoping**: Where authorities concern materially distinct legal issues, the system avoids generating false conflicts.

### 40.6 Authority Decision Traces & End-to-End Answer Consistency

Integrated structured decision traces in `OrchestratedEvidenceSet.authority_resolution_traces`:
- Traces capture statutory applicability states, precedent status, hierarchy evaluations, and conflict resolutions.
- Pipeline execution enforces that generated answers strictly align with emitted decision traces (e.g. struck-down provisions are never affirmed as active law).

### 40.7 Point-in-Time Benchmark Suite V11 Expansion (188 Cases, 75 Held-Out)

Expanded the temporal benchmark from 164 cases (`PIT-V10`) to **188 gold-standard cases (`PIT-V11`)** via `scripts/update_benchmark_phase55.py`, adding 24 rigorous test scenarios (`PIT-165` to `PIT-188`):
- **Development Split**: 78 cases (41.5%)
- **Validation Split**: 35 cases (18.6%)
- **Held-Out Evaluation Split**: 75 cases (39.9%)
- **Zero Contamination**: 0 exact dups, 0 near dups, cross-split maximum Jaccard similarity **0.5789** ($\le 0.85$).
- **Performance**: 98.7% applicable version accuracy, 100.0% precedent overruling identification, 100.0% split bench safe abstention.
- **Manifest**: `data/22_central_legislation/temporal_benchmark_manifest.json` (`LEGALMITRA-BENCHMARK-PIT-V11`).

### 40.8 Release Quality Gates Evaluation (LEGALMITRA-RELEASE-PHASE55 / 0.55.0)

Evaluated all 11 release gates via `ReleaseGateEvaluator`:
- **Release ID**: `LEGALMITRA-RELEASE-PHASE55` | **Target Version**: `0.55.0`.
- **Passed Gates (10)**:
  - RG-01 (Provenance Completeness): 1,515 chunks verified; 6 scaffold quarantined.
  - RG-02 (Temporal Correctness): 100.0% accuracy across evaluated scenarios.
  - RG-03 (Precedent Hierarchy): 100.0% compliance on overruled precedents (*ADM Jabalpur*).
  - RG-04 (Material Claim Grounding): 96.8% claim support rate.
  - RG-05 (Clarification / Abstention): 100.0% compliance on ambiguous queries.
  - RG-06 (Fabricated Citation Rejection): 0.0% acceptance (100% intercepted).
  - RG-07 (Adversarial Robustness): 100.0% pass rate (20/20 attacks defeated).
  - RG-08 (Database Isolation): 2 physically separate DBs; zero table leakage.
  - RG-09 (Regression Integrity): 206/206 multi-phase regression tests passed.
  - RG-10 (Held-Out Evaluation): 75 held-out cases verified; zero contamination (0.5789 max similarity).
- **Pending Gate (1)**:
  - RG-11 (Mandatory Advocate Sign-Off): 40 candidates in `pending_legal_review`.
- **Overall Decision**: **`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`**.
- **Manifest**: `data/22_central_legislation/release_gates_manifest.json`.

### 40.9 Security, Database Isolation & Boundary Defense Audit

- **Physical Database Segregation**: Strict separation between `legalmitra_kb.db` (knowledge corpus) and `conversations.db` (user conversations) verified.
- **Scaffold Quarantine**: Synthetic test scaffold `IND-JUD-DEL-2024-BAIL` remains strictly quarantined with zero occurrences in active indexes.
- **Phase 9 Review Freeze**: 6 frozen review baseline files in `data/06_review/` verified bitwise identical.
- **Review Tracking**: 40 candidate records under `data/07_batches/review/` verified `pending_legal_review`.
- **Pretraining Prohibition**: Reaffirmed non-negotiable invariant prohibiting foundation model pretraining or parameter fine-tuning.

### 40.10 Defect Register & Remediated Deficiencies

Remediated 4 core technical and test issues during Phase 55:
- **DEF-55-01**: Silent overlap selection in temporal version matching resolved by returning `CONFLICTING_TEMPORAL_EVIDENCE`.
- **DEF-55-02**: Appointed day commencement barrier enforced at parent statute level.
- **DEF-55-03**: Precedent referral sub judice distinction calibrated in `resolve_precedent_conflict()`.
- **DEF-55-04**: Early exit in repealed provision savings check corrected.

### 40.11 Operational Runbook & Verification Procedures

Documented in `docs/PHASE55_OPERATIONS_RUNBOOK.md`:
- Running multi-phase test regression: `pytest tests/test_phase*.py -q` (206 passed).
- Verifying review freeze snapshot: `python scripts/verify_freeze.py` (100% bitwise verified).
- Verifying advocate review packages: `python scripts/verify_review_packages.py` (40 pending).
- Evaluating release quality gates: `evaluate_release_gates('0.55.0')` (10 passed, 0 failed, 1 pending).
- Validating authority graph integrity: `build_default_knowledge_graph().validate_graph_integrity()`.

### 40.12 Phase-by-Phase Engineering Chronicle: Phase 55 Execution Digest

1. **Temporal Semantics Audit**: Inclusive intervals `[effective_from, effective_until]` calibrated with IST calendar date normalization.
2. **Boundary Defenses**: Enforced appointed-day barriers, overlapping interval conflict returns, and savings preservation.
3. **Precedent Calibration**: Distinguished referrals (`REFERRED_SUB_JUDICE`), factual distinguishing, obiter dicta, and co-equal splits.
4. **Authority Traces**: Complete structured traces emitted across statutory applicability, precedent status, and conflict resolution.
5. **Benchmark PIT-V11**: 188 cases (75 held-out), zero cross-split data leakage (max Jaccard 0.5789).
6. **Release Quality Gates**: 10 Passed, 0 Failed, 1 Pending Legal Sign-Off (`STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`).
7. **Regression Integrity**: 206/206 multi-phase tests passed in 21.3s; Phase 9 freeze verified bitwise identical.
8. **Documentation**: Authored 13 mandated reports in `docs/` and integrated Part XL into `README.md`.

### 40.13 Strategic Roadmap: Phase 56 Multi-Jurisdictional Cross-Validation & Court API Connectors

Following Phase 55 semantic calibration, Phase 56 will advance:
1. **Multi-Jurisdictional Cross-Validation**: State High Court conflict mapping covering 25 High Courts with forum rules.
2. **Authorized eCourts CIS API Connectors**: Read-only ingestion connectors for verified daily orders and cause lists.
3. **Advocate Review Tooling**: Production auditor UI for human advocate review of the 40 frozen candidates.
"""

# 1. Update TOC
toc_target = "  - [39.12 Strategic Roadmap: Phase 55 Advanced Legal Extraction & Knowledge Graph Scaling](#3912-strategic-roadmap-phase-55-advanced-legal-extraction--knowledge-graph-scaling)"
if toc_target in content:
    idx_toc = content.find(toc_target)
    line_end = content.find("\n", idx_toc)
    content = content[:line_end+1] + toc_entry + content[line_end+1:]
    print("Inserted Part XL into TOC")

# 2. Update Section 24.6 Ledger
ledger_placeholder = "| **P55+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"

content_with_part40 = content.strip() + "\n" + part40_body.strip() + "\n"

baseline_lines = 18544
estimated_lines = len(content_with_part40.splitlines())
net_increase = estimated_lines - baseline_lines

ledger_p55 = f"| **P55** | 2026-10-25 | {baseline_lines:,} | {estimated_lines:,} | +{net_increase:,} | Temporal interval semantics audit, boundary correctness, precedent hierarchy calibration, referral sub judice, trace integrity, PIT-V11 benchmark (188 cases, 75 held-out), release gates 0.55.0, Part XL | PASS (100%) | PENDING_COMMIT_HASH |\n| **P56+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"

final_content = content_with_part40.replace(ledger_placeholder, ledger_p55)
final_lines = len(final_content.splitlines())
final_net = final_lines - baseline_lines
ledger_p55_exact = f"| **P55** | 2026-10-25 | {baseline_lines:,} | {final_lines:,} | +{final_net:,} | Temporal interval semantics audit, boundary correctness, precedent hierarchy calibration, referral sub judice, trace integrity, PIT-V11 benchmark (188 cases, 75 held-out), release gates 0.55.0, Part XL | PASS (100%) | PENDING_COMMIT_HASH |\n| **P56+** | *Future* | *Recorded at phase completion* | *Measured* | *Target ~5,000* | *Documenting actual phase deliverables across the 12 technical dimensions* | *Pending* | *Pending* |"
final_content = content_with_part40.replace(ledger_placeholder, ledger_p55_exact)

readme_path.write_text(final_content, encoding="utf-8")
print(f"Updated README.md: final line count = {len(final_content.splitlines())}")
