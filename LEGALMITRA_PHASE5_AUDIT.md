# LEGALMITRA — PHASE 5 AUDIT REPORT: INDEPENDENT RAG, DATA & REPOSITORY AUDIT
**Document ID**: `AUDIT-2026-PHASE5-001`  
**Date**: October 2026  
**Pipeline Version**: 0.5.0  
**Audit Standard**: Independent Systems, Legal-Informatics & Grounding Audit  
**Status**: COMPLETE / VERIFIED  

---

## 1. Executive Summary

This independent audit conducts an uncompromised verification of all data-engineering artefacts, database schemas, full-text search indexes, source provenances, validation pipelines, and benchmark scoring in the **LegalMitra** platform.

### Summary of Repository State vs. Prior Claims

| Dimension | Prior Reported State | Independently Verified State | Variance / Diagnostic Finding |
|---|---|---|---|
| **Registered Sources** | 9 records in registry | **9 records** in `registry/source_registry.jsonl` | Exact match. 7 normalized, 2 failed/unsupported. |
| **Knowledge Base Sources** | 9 sources indexed | **9 records** in `sources` table (`data/legalmitra_kb.db`) | Exact match. |
| **Knowledge Base Chunks** | 382 chunks reported | **382 chunks** in `legal_chunks` table & FTS5 | Exact match: 369 binding statutes, 7 binding precedents, 6 unverified scaffolds. |
| **Generated Examples** | 27 live pilot examples reported | **61 total examples** across 4 JSONL files in `data/03_generated/` | 27 live pilot examples + 34 Phase 1/2 synthetic test records. |
| **Offline Test Suite** | 64 passing tests | **64 passed, 2 live deselected** (27.31s in `pytest`) | 100% reproducible offline. Zero test regressions. |
| **Evaluation Benchmark** | 12 gold questions; "100% pass rate" reported | **12 items** in `held_out_eval.jsonl` | Evaluator passed 12/12, but **metric was flawed by lexical false-positives** and lack of semantic rubric grading. |
| **Active LLM Provider** | Reported as "Nemotron" / "Llama-3.2 on NIM" | **Meta Llama 3.2 11B Vision Instruct** | Nemotron endpoint currently unavailable; Llama-3.2 on NVIDIA NIM was used. |

---

## 2. Deep Database & Knowledge Base Inspection (`data/legalmitra_kb.db`)

The database was inspected using direct read-only SQL queries against `sources`, `legal_chunks`, and the FTS5 virtual table `legal_chunks_fts`.

### 2.1 Table Schemas & Record Counts

1. **`sources` table**:
   - Total rows: **9**
   - Columns: `document_id`, `title`, `source_url`, `source_type`, `jurisdiction`, `court`, `document_date`, `effective_date`, `is_historical`, `is_synthetic_scaffold`, `repeal_status`, `checksum`, `verification_status`, `metadata_json`.
   - Verified breakdown:
     - 6 statutes (`IND-STAT-BSA-2023-SEC61`, `IND-STAT-BSA-2023-SEC63`, `IND-STAT-DPDP-2023`, `IND-STAT-IT-2000`, `IND-STAT-POCSO-2012-SEC4`)
     - 2 judgments (`IND-JUD-SC-2017-PUTTASWAMY`, `IND-JUD-DEL-2024-BAIL` [scaffold])
     - 1 handbook/rule (`IND-GUIDE-SCI-PROC-2025` [extraction failed])
     - 1 unsupported dummy (`IND-UNSUPPORTED-001` [test failure case])

2. **`legal_chunks` table**:
   - Total rows: **382**
   - Chunks by Source:
     - `IND-STAT-IT-2000`: **230 chunks** (Sections, Subsections, Explanations across IT Act, 2000)
     - `IND-STAT-DPDP-2023`: **129 chunks** (Sections 1 through 44 of DPDP Act, 2023)
     - `IND-JUD-SC-2017-PUTTASWAMY`: **7 chunks** (Ratio Decidendi, Paras 1-6)
     - `IND-JUD-DEL-2024-BAIL`: **6 chunks** (Synthetic Scaffold Paras)
     - `IND-STAT-POCSO-2012-SEC4`: **4 chunks** (Section 4, Section 4(1), Proviso, Explanation)
     - `IND-STAT-BSA-2023-SEC61`: **3 chunks** (Section 61, Proviso, Explanation)
     - `IND-STAT-BSA-2023-SEC63`: **3 chunks** (Section 63, Subsections (1)-(4))
   - Chunks by Authority Level:
     - `binding_statute`: **369 chunks**
     - `binding_precedent`: **7 chunks**
     - `unverified_scaffold`: **6 chunks**

3. **`legal_chunks_fts` virtual table**:
   - Total indexed rows: **382**
   - FTS5 tokenizer: `porter unicode61`
   - Content synchronization: 1:1 match with `legal_chunks`.

### 2.2 Forensic Check of Scaffold Isolation
- In `sources`: `IND-JUD-DEL-2024-BAIL` has `is_synthetic_scaffold = 1` and `verification_status = 'flagged_unsupported'`.
- In `legal_chunks`: All 6 chunks for `IND-JUD-DEL-2024-BAIL` have `is_synthetic_scaffold = 1` and `authority_level = 'unverified_scaffold'`.
- Default query behavior in `LegalKnowledgeBase.search()` sets `include_synthetic = False`, enforcing `is_synthetic_scaffold = 0` filter. This prevents contaminated scaffold chunks from appearing in default RAG context.

### 2.3 Temporal and Jurisdiction Filter Verification
- In `LegalKnowledgeBase.search()`:
  - If `as_of_date` is provided, chunks with `effective_date IS NOT NULL AND effective_date > as_of_date` are excluded.
  - Chunks with `effective_date IS NULL` (e.g. judgments, or statutes with phased commencement) are preserved unless explicitly excluded.
  - Jurisdiction filtering: Chunks with `jurisdiction = 'IN'` (Central) match national queries, while state-specific chunks (e.g., `'IN-DL'`) require explicit match.

---

## 3. Consistency Audit: Registry, Normalized Data, and Generated Data

### 3.1 Registry (`registry/source_registry.jsonl`) vs. Normalized Files (`data/02_normalized/`)
- All 7 normalized sources in `registry/source_registry.jsonl` correspond exactly to a `.json` file in `data/02_normalized/`:
  1. `IND-STAT-BSA-2023-SEC61.json` (1 section)
  2. `IND-STAT-BSA-2023-SEC63.json` (1 section)
  3. `IND-STAT-POCSO-2012-SEC4.json` (1 section)
  4. `IND-STAT-DPDP-2023.json` (91 statutory components)
  5. `IND-STAT-IT-2000.json` (316 statutory components)
  6. `IND-JUD-SC-2017-PUTTASWAMY.json` (11 judgment components)
  7. `IND-JUD-DEL-2024-BAIL.json` (10 judgment components)
- Noticeable Bug in Normalized JSONs: The root property `title` is `null` in all 7 normalized JSONs because the normalizer populated `act_title` or `case_name` without copying to root `title`. When indexed into SQLite, `LegalKnowledgeBase.index_*` patched this by looking up the title from the registry record.

### 3.2 Generated Data Inconsistency: 27 vs. 61 Examples
- The Phase 4 documentation reported "27 generated examples".
- Actual files in `data/03_generated/`:
  - `legal_qa.jsonl`: **35 records** (21 from Phase 1/2 synthetic test scripts + 14 from Phase 3/4 live pilots)
  - `procedural_guide.jsonl`: **12 records** (9 Phase 1/2 test records + 3 Phase 3 live records)
  - `drafting_examples.jsonl`: **8 records** (7 Phase 1/2 test records + 1 Phase 3 live record)
  - `case_analysis.jsonl`: **6 records** (4 Phase 1/2 test records + 2 Phase 3 live records)
  - **Total**: **61 records**.
- **Audit Assessment**: The earlier "27 examples" referred only to the latest single live pilot execution run, but historical synthetic examples generated in earlier milestones remained appended in the files.
- **Risk Identified**: Procedural guide `PROC-BNSS-482-BAIL-001` in `data/03_generated/procedural_guide.jsonl` cites `IND-JUD-DEL-2024-BAIL` and contains flawed procedure for anticipatory bail filed by the State.

---

## 4. Source-by-Source Legal Veracity & Currency Audit

| Document ID | Official Authority | Court / Jurisdiction | Enactment / Commenced | Status in Indian Law | Outstanding Integrity Issues |
|---|---|---|---|---|---|
| `IND-STAT-BSA-2023-SEC61` | Parliament of India | Central (`IN`) | Assent: 2023-12-25<br>Enforced: 2024-07-01 | **Active Law**. Replaced s.65A Evidence Act, 1872. | Verified. Only s.61 present; full Act not indexed. |
| `IND-STAT-BSA-2023-SEC63` | Parliament of India | Central (`IN`) | Assent: 2023-12-25<br>Enforced: 2024-07-01 | **Active Law**. Replaced s.65B Evidence Act, 1872. | Verified. Only s.63 present; full Act not indexed. |
| `IND-STAT-POCSO-2012-SEC4` | Parliament of India | Central (`IN`) | Assent: 2012-06-19<br>Enforced: 2012-11-14 | **Active Law** (incorporates 2019 amendment). | Verified. Only s.4 present; full POCSO Act not indexed. |
| `IND-STAT-DPDP-2023` | Parliament of India | Central (`IN`) | Assent: 2023-08-11<br>Commencement: Phased | **Statute Passed, Substantively Unenforced**. Rules pending. | Full text present (44 sections). Section 1(2) phased commencement properly tracked. |
| `IND-STAT-IT-2000` | Parliament of India | Central (`IN`) | Assent: 2000-06-09<br>Enforced: 2000-10-17 | **Active Law**. Section 43A slated for repeal under DPDP s.44(2). | Full text present (90 sections). |
| `IND-JUD-SC-2017-PUTTASWAMY` | Supreme Court of India (9 Judges) | Supreme Court (`IN`) | Decision: 2017-08-24 | **Binding Landmark Precedent** under Art 141. | Only certified extracts (Order of Court & core ratio). Full 547-page judgment omitted. |
| `IND-JUD-DEL-2024-BAIL` | Unknown (Fabricated) | High Court (`IN-DL`) | Alleged: 2024-07-10 | **SPURIOUS / UNVERIFIED SCAFFOLD**. Legal impossibility. | Quarantined. Must never be used for legal reasoning. |
| `IND-GUIDE-SCI-PROC-2025` | Supreme Court Registry | Supreme Court (`IN`) | Published: 2025-10-06 | Official Guidance Manual. | Extraction failed due to 15-page Docling limit (278 pages). Not indexed in KB. |
| `IND-UNSUPPORTED-001` | Synthetic Test Fixture | Mock (`IN`) | N/A | **Non-Legal Negative Fixture**. | Intended negative control fixture. |

---

## 5. Audit of LLM Provider Abstraction & Model Lineage

1. **Hardware & Provider Reality**:
   - `legalmitra/llm/nemotron.py` is an HTTP client pointing to `https://integrate.api.nvidia.com/v1`.
   - The model requested is `meta/llama-3.2-11b-vision-instruct`.
   - Native NVIDIA Nemotron endpoints (`nvidia/llama-3.1-nemotron-70b-instruct`) are unavailable under the current API key entitlements.
   - Calling this system "Nemotron RAG" is technically inaccurate. It is **Meta Llama 3.2 on NVIDIA NIM**.
2. **Current LLM Status**:
   - As instructed by the user, **Nemotron is unavailable and will not be waited for or assumed**.
   - Analysis, benchmark design, and plan execution in Phase 5 are performed locally by the AI coding assistant within Antigravity without external API dependencies.

---

## 6. Offline Test Suite Reproducibility

- Test Command: `pytest -v`
- Execution Environment: Python 3.11.0, pytest 7.4.3 on Windows amd64.
- **Reproduced Result**:
  - **64 tests passed, 2 deselected** (live tests requiring API key).
  - Execution time: **27.31 seconds**.
  - All mock tests, schema validations, deduplications, FTS5 indexes, and temporal boundary checks passed cleanly.

