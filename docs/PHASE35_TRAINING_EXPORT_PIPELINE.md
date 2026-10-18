# Phase 35 Training Corpus Export Pipeline & Manifest Specification

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Export Pipeline Architecture

The Phase 35 pretraining export pipeline (`legalmitra/corpus/training_exporter.py`) generates deterministic, versioned training manifests (`v4.0.0`) strictly from validated legal records.

### Mandatory Export Gates:
1. **Source State Gate:** Only sources in `TRAINING_ELIGIBLE` state in `UnifiedSourceRegistry` are exported.
2. **Rights Verification Gate:** Only records possessing verified statutory exemptions under Section 52(1)(q) of the Indian Copyright Act, 1957 are eligible.
3. **Synthetic Scaffold Quarantine:** Exactly 0 synthetic chunks (`IND-JUD-DEL-2024-BAIL`) are exported.
4. **Advocate Review Quarantine:** All 40 pending advocate candidates (20 Package A, 20 Package B) are excluded.
5. **Database Boundary:** Exports read only authoritative legal tables in `data/legalmitra_kb.db`, `data/09_national_corpus/hindi_statutory_corpus.json`, and `data/09_national_corpus/phase34_expanded_corpus.json`. The user conversation database (`data/conversations.db`) is physically excluded.
6. **Dry-Run Mode:** Full `--dry-run` flag support allowing pipeline audits and token estimations without modifying manifest files.

---

## 2. Generated Manifest Artifacts & SHA-256 Digests

The export pipeline generates versioned JSON manifests in `research/original_model/manifests/`:

| Manifest File | Passages | Tokens | SHA-256 Checksum |
|---|---|---|---|
| `dataset_manifest_v4.json` | 1,559 | 342,965 | `15088ea8e24555478a54fcb7d44bddefe39a1370fe3597bb298d2e3511f3cc4e` |
| `train_manifest_v4.json` | 1,380 | 304,291 | `cf3fc18f4bf87329e2f473ca49a9907fb2df16f86986cd1bc10ae98c06d0d822` |
| `val_manifest_v4.json` | 25 | 3,928 | `2e96962c9859c3f7824093cd9d9b754f6c2fa6d07a02aeb8d3ffe906c4fbf118` |
| `test_manifest_v4.json` | 154 | 34,746 | `818962fecbb7efafeddbf8080a7c3e2853a47bd38d9f28389c64e55e4abc0d23` |

### Invariant Checks Verified:
- Synthetic Scaffold Count in Manifests: **0** (Quarantined: 6 chunks in KB).
- Pending Advocate Review Count in Manifests: **0** (Pending: 40 candidates in tracking register).
- Pretraining Tokens: **342,965** (English: 334,348; Hindi: 8,617).
