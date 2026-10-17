# LegalMitra Phase 23 Corpus Quality Standard & Ingestion Verification Policy
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Quality Dimensions for Indian Legal Materials

Every statutory provision, delegated notification, and court judgment ingested into LegalMitra must adhere to strict quality standards across five dimensions:

1. **Provision-Level Granularity:** Statutes must be segmented at the individual Section / Schedule / Order level rather than ingested as monolithic Act PDFs.
2. **Temporal Integrity:** Chunks must carry explicit effective dates, amendment references, and repeal status flags.
3. **Neutral Citation Normalization:** Precedent judgments must record authoritative neutral citations (e.g. `2020 INSC ...`, `(2020) 10 SCC ...`).
4. **Scaffold Quarantine:** Synthetic testing fixtures or unverified placeholders (specifically `IND-JUD-DEL-2024-BAIL`) must be tagged with `is_synthetic_scaffold = 1` and systematically excluded from all live search indexes.
5. **Traceability to Official Gazettes:** Each statutory enactment must maintain source URLs to official gazettes (egazette.gov.in, indiacode.nic.in, or state government gazettes).

---

## 2. Four-Tier Operational Readiness

| Tier | Status | Meaning in LegalMitra Pipeline | Count |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Registered** | Entity catalogued in legal universe inventory with gazette metadata | **101** |
| **Tier 2** | **Acquired** | Source text or gazette PDF acquired and present in `sources` registry | **42** |
| **Tier 3** | **Indexed** | Text segmented, parsed, and stored as provision chunks in `legal_chunks` | **1,405** |
| **Tier 4** | **Retrievable** | Chunk is active, non-quarantined (`is_synthetic_scaffold=0`), available for BM25/FTS/vector search | **1,399** |

---

## 3. Quarantined Asset Protocol

The 6 chunks belonging to `IND-JUD-DEL-2024-BAIL` were generated as synthetic scaffolding during initial pipeline development.
- **Protocol:** They are permanently quarantined with `is_synthetic_scaffold = 1`.
- **Query Filter:** Every database query executed by `LegalKnowledgeBase` and `LegalRAGEngine` enforces `WHERE is_synthetic_scaffold = 0`.
- **Automated Verification:** `scripts/verify_freeze.py` asserts zero leakage of scaffold records into production benchmarks.

