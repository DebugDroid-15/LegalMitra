# Phase 58 Artifact Inventory & Verification Matrix

**Project:** LegalMitra  
**Verification Target:** Release 0.58.0 / Phase 58  
**Verification Date:** October 2026  

---

## 1. Primary Knowledge Base & Database Artifacts

| Artifact Name | Path | Record Count | Integrity / Hash Status | Purpose / Invariants |
| :--- | :--- | :--- | :--- | :--- |
| **Legal Knowledge Base DB** | `data/legalmitra_kb.db` | 1,515 chunks | Verified (1,509 authentic, 6 quarantined) | Primary statutory & judicial extract repository. Physical separation from chat sessions. |
| **Conversations DB** | `data/conversations.db` | Isolated | Distinct file, zero KB tables | User conversation and session storage. Zero cross-contamination with legal KB. |
| **Scaffold Quarantine Marker** | `legal_chunks` table | 6 rows (`is_synthetic_scaffold=1`) | Quarantined (`IND-JUD-DEL-2024-BAIL`) | Synthetic test scaffold strictly excluded from production retrieval and evaluation. |

---

## 2. Benchmark Manifests & Datasets

| Manifest Name | Path | Cases | Split Breakdown | Invariant Status |
| :--- | :--- | :--- | :--- | :--- |
| **Point-in-Time V13 Manifest** | `data/22_central_legislation/temporal_benchmark_manifest.json` | 240 | 100 Dev, 46 Val, 94 Held-Out | Zero exact duplicates; Max token Jaccard 0.5926. |
| **Release Gates Manifest** | `data/22_central_legislation/release_gates_manifest.json` | 20 gates | 19 Passed, 1 Pending (`RG-11`), 0 Failed | Machine-readable release gate manifest for Release `0.58.0`. |
| **Phase 9 Review Manifest** | `data/06_review/PHASE9_REVIEW_SNAPSHOT_MANIFEST.json` | 6 files | 100% SHA-256 bitwise match | Frozen review baseline; immutable governance lock. |
| **Review Tracking Register** | `data/07_batches/review/review_tracking_register.json` | 40 records | 40 `pending_legal_review` | Statutory review tracking under Advocates Act, 1961. |

---

## 3. Review Package Components (Immutable Freeze)

| File Name | Location | Size (Bytes) | SHA-256 Digest | Status |
| :--- | :--- | :--- | :--- | :--- |
| `pilot_20_examples.jsonl` | `data/06_review/` | 44,542 | `e01b22f50f36c3927b595ecd03e2258c6889f299e6394644b2cd4cb359ffa953` | Frozen |
| `pilot_20_manifest.json` | `data/06_review/` | 21,705 | `9da3801fdc79514987dcd91ffacc81372ab5412a93002ddfd3d9c1c7050369a4` | Frozen |
| `pilot_20_review_sheet.csv` | `data/06_review/` | 35,396 | `6f519165d45bac465e2c25de20369b74d136543307a49ecb84559f68a7dadcab` | Frozen |
| `pilot_20_source_bundle.json` | `data/06_review/` | 62,870 | `3cf555e96743ece27b0e22d954d6535cea8a51cc9242c471416b9f46fb031f10` | Frozen |
| `pilot_20_open_issues.md` | `data/06_review/` | 7,903 | `0b82c4f6df0d9b6c755c6bf15ffb582c07cc6788a28d8ff610de4b645251f45e` | Frozen |
| `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md` | `data/06_review/` | 15,514 | `e5966e245c15f6cb96e48d57ede8e81be8a89ebe3aa843098afc961e86c2c508` | Frozen |
