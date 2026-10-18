# LEGALMITRA PHASE 26: DATABASE MIGRATION & REVERSIBILITY PROTOCOL

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 26 — Human Legal Review Operations, Structured Statutory Modeling & High Court Precedent Expansion  
**Date:** October 2026  
**Status:** Implemented & Verified  

---

## 1. Executive Summary

LegalMitra enforces an additive, non-destructive migration standard for `data/legalmitra_kb.db`. Under no circumstances are existing production tables dropped, columns renamed destructively, or historical chunks truncated.

This protocol documents the migration compatibility and rollback guarantees governing Phase 26 statutory modeling and High Court precedent expansion.

---

## 2. Additive Migration Principles

1. **Table Schema Stability**:
   - Primary tables (`sources`, `legal_chunks`, `legal_chunks_fts`, `cases`, `judicial_documents`, `hearing_events`) retain their canonical schemas.
   - New sub-entities (e.g. `hierarchy_level = 'illustration'`) integrate cleanly via existing enum values without requiring DDL alterations.

2. **Idempotency & Upsert Guarantees**:
   - All insertion routines implement `INSERT OR REPLACE INTO` / check-before-insert logic based on unique deterministic chunk IDs (e.g. `IND-STAT-BNSS-2023:SEC:482:PROVISO:1`).
   - Re-running ingestion pipelines does not generate duplicate records or inflate corpus counts.

3. **FTS5 Virtual Table Synchronization**:
   - `legal_chunks_fts` uses explicit deletion before insertion (`DELETE FROM legal_chunks_fts WHERE chunk_id = ?`) to ensure virtual indexes remain in strict 1:1 synchronization with physical SQLite rows.

---

## 3. Rollback & Disaster Recovery Procedure

In the event of an ingestion defect or unintended corruption during batch expansion:
1. **Pre-Migration Snapshot**: A binary backup of `data/legalmitra_kb.db` is maintained prior to multi-source batch ingestion.
2. **Selective Rollback SQL**:
   ```sql
   -- To rollback a specific batch by source_id:
   DELETE FROM legal_chunks WHERE source_id = 'BATCH_SOURCE_ID';
   DELETE FROM legal_chunks_fts WHERE chunk_id LIKE 'BATCH_SOURCE_ID:%';
   DELETE FROM sources WHERE document_id = 'BATCH_SOURCE_ID';
   ```
3. **Quarantine Protection**: Rollbacks never touch the 6 permanently isolated scaffold records belonging to `IND-JUD-DEL-2024-BAIL` (`is_synthetic_scaffold = 1`).
