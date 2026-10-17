# LegalMitra Phase 23 Review Package Import/Export Specification
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Package Export Protocol

Review packages group candidate records with their statutory context, query formulations, and evaluation rubrics into a portable, cryptographically verifiable JSON package.

### Export Structure:
```json
{
  "package_id": "PKG-BATCH-01-EXPANSION",
  "exported_at": "2026-10-17T23:50:00Z",
  "total_records": 20,
  "records": [
    {
      "example_id": "QA-BNSS-001",
      "legal_review_status": "pending_legal_review",
      "question": "...",
      "statutory_citations": ["The Bharatiya Nagarik Suraksha Sanhita, 2023, Section 482"],
      "answer": "..."
    }
  ]
}
```
- **Checksum Verification:** The export pipeline calculates and logs a SHA-256 digest of the serialized output.
- **Role Requirement:** Restricted to `LEGAL_RESEARCHER`, `AUDITOR`, and `SYSTEM_ADMIN`.

---

## 2. Dry-Run Import & Verification Mode

To prevent corpus corruption, imports default to `dry_run = True`.

### Import Pipeline Stages:
1. **Authorization Check:** Ensures actor role is `SYSTEM_ADMIN` or `AUDITOR`.
2. **File Existence & JSON Validation:** Validates physical file presence and syntactic JSON compliance.
3. **Record Identifier Verification:** Ensures every record has a non-empty `example_id` or `qa_id`.
4. **Review Status Schema Check:** Verifies that reported statuses conform to `ReviewStatus` enumerations (`pending_legal_review`, `under_review`, `approved`, `rejected`, `needs_revision`, `disputed`).
5. **Dry-Run Simulation:** Reports total records, valid records, and any syntax/schema discrepancies without modifying underlying database tables or JSONL files.
6. **Transactional Commit (when `dry_run=False`):** Applies changes atomically. If any record fails validation, the entire batch rolls back.

---

## 3. Preservation of Existing Review Freeze

The 40 candidates across Package A (Frozen Pilot 20) and Package B (Batch 1 Candidates) are safeguarded:
- Their primary storage files (`data/03_generated/pilot_20_examples.jsonl`, `data/07_batches/batch_01_candidates/batch_01_examples.jsonl`) are monitored by SHA-256 manifests.
- Import operations write to independent audit registers and cannot overwrite frozen baseline files without failing `scripts/verify_freeze.py`.

