# PHASE 19 — DATA RECONCILIATION & RECORD PROVENANCE AUDIT

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Data Reconciliation  

---

## 1. Executive Summary

A critical failure mode in large-scale legal retrieval systems is confusing the *number of registered or discovered records* with *actual indexed, retrievable text chunks*. LegalMitra maintains an auditable distinction across every stage of document provenance:
- **Discovered/Catalogued**: Known to exist in Indian legal repositories.
- **Acquired/Preserved**: Raw document stored locally with SHA-256 hash.
- **Parsed/Structured**: Processed into section/proviso/paragraph structures.
- **Indexed**: Stored in SQLite knowledge base and FTS index.
- **Legally Reviewed**: Evaluated and approved by licensed advocates.
- **Quarantined**: Synthetic fixtures strictly excluded from retrieval.

---

## 2. Quantitative Reconciliation Matrix (Ten Dimensions)

| Dimension | Measured Count | Scope & Details |
| :--- | :--- | :--- |
| **1. Registered Sources in DB** | 37 | Entries in `sources` table of `data/legalmitra_kb.db`. |
| **2. Sources with Raw Files** | 19 | Verified raw PDFs and HTML documents in `data/01_raw/`. |
| **3. Sources with Parsed Documents** | 17 | Normalized JSON document trees in `data/02_normalized/`. |
| **4. Sources with Indexed Chunks** | 35 | Distinct `source_id` keys present in `legal_chunks` table. |
| **5. Sources with Validated Metadata** | 37 | All DB sources possess valid JSON metadata, jurisdiction, dates. |
| **6. Sources with Verified Currentness** | 37 | All 37 evaluated for repeal status, commencement, and temporal range. |
| **7. Sources with Human-Reviewed Propositions** | 0 | All 40 review candidates strictly remain `pending_legal_review`. |
| **8. Quarantined Sources & Chunks** | 1 source / 6 chunks | `IND-JUD-DEL-2024-BAIL` (6 chunks in KB; strictly filtered). |
| **9. Catalogued Universe Items** | 50 | Catalogued foundational instruments in `data/09_national_corpus/`. |
| **10. Total Stored Chunks vs Active Chunks** | 1,363 stored / 1,357 active | 6 chunks quarantined; 1,357 retrievable via search. |

---

## 3. Discrepancy Resolution & Audit Findings

1. **Total Chunks (1,363) vs. Active Chunks (1,357)**:
   - Reporting code must never conflate total stored rows with active retrievable chunks.
   - 6 chunks belong to synthetic test fixture `IND-JUD-DEL-2024-BAIL` and are excluded at the SQL level (`WHERE is_synthetic_scaffold = 0`).
2. **Registered Sources (37) vs. Indexed Sources (35)**:
   - Exactly two registered sources have zero chunks:
     - `IND-UNSUPPORTED-001`: Intentionally empty negative test fixture for unsupported document formats (`.xyz`).
     - `IND-GUIDE-SCI-PROC-2025`: High-value practice handbook catalogued but kept in OCR remediation backlog.
3. **Registry File Synchronisation**:
   - `registry/source_registry.jsonl` contains 18 historical seeds; the database `sources` table contains 37 fully tracked sources, and `data/09_national_corpus/` inventories 50 national instruments. In Phase 19, the unified discovery and inventory engine will establish continuous synchronization across all tiers.

