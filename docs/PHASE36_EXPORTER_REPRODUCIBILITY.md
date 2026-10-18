# Phase 36 Training Exporter Hardening & Reproducibility Audit

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Phase 36 audited and hardened the training corpus export engine (`legalmitra/corpus/training_exporter.py`). The audit verified that the exporter produces strictly deterministic outputs, enforces manifest immutability (preventing accidental overwrites of historical versions), operates cleanly in `--dry-run` mode without network or disk mutations, and generates comprehensive exclusion reports.

---

## 2. Hardening Enhancements Implemented in Phase 36

### A. Manifest Immutability Guard
In `TrainingCorpusExporter.export()`:
```python
target_manifest = self.manifest_dir / f"dataset_manifest_{version}.json"
if not dry_run and target_manifest.exists() and not overwrite:
    raise FileExistsError(
        f"Manifest {target_manifest} already exists. Immutable manifests cannot be overwritten. "
        "Use a new version tag (e.g. v5) or explicitly pass overwrite=True."
    )
```
Historical manifests (`dataset_manifest_v3.json`, `dataset_manifest_v4.json`) cannot be silently modified or corrupted.

### B. Automated Exclusion Reporting
Implemented `generate_exclusion_report()`, which audits and documents all excluded records:
- **Synthetic Scaffold Quarantine:** Exactly 6 chunks (`IND-JUD-DEL-2024-BAIL`) strictly excluded.
- **Advocate Review Candidates:** Exactly 40 pending review items (20 Package A, 20 Package B) strictly excluded.
- **User Conversation Database:** `data/conversations.db` physically isolated from queries.
- **Unindexed / Discovery Candidates:** 78 unindexed catalog records and discovery candidates excluded until verified on disk.

### C. Side-Effect Free Dry-Run
Verified that `--dry-run` mode performs in-memory tokenization and hash calculation without writing any manifest files to disk or initiating network calls.

---

## 3. Manifest Byte Digest Verification

Recomputed byte digests for all active manifests in `research/original_model/manifests/`:

| Manifest File | Version | Passages | Tokens | SHA-256 Digest | Status |
|---|---|---|---|---|---|
| `dataset_manifest_v4.json` | `v4.0.0` | 1,559 | 342,965 | `15088ea8e24555478a54fcb7d44bddefe39a1370fe3597bb298d2e3511f3cc4e` | **BITWISE MATCH** |
| `train_manifest_v4.json` | `v4.0.0` | 1,380 | 304,291 | `cf3fc18f4bf87329e2f473ca49a9907fb2df16f86986cd1bc10ae98c06d0d822` | **BITWISE MATCH** |
| `val_manifest_v4.json` | `v4.0.0` | 25 | 3,928 | `2e96962c9859c3f7824093cd9d9b754f6c2fa6d07a02aeb8d3ffe906c4fbf118` | **BITWISE MATCH** |
| `test_manifest_v4.json` | `v4.0.0` | 154 | 34,746 | `818962fecbb7efafeddbf8080a7c3e2853a47bd38d9f28389c64e55e4abc0d23` | **BITWISE MATCH** |

The exporter demonstrates 100% deterministic reproducibility across multiple runs.
