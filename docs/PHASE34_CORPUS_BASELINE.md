# LegalMitra Phase 34: Baseline Corpus Reproduction & Structural Verification Report

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Reference Artifacts:** `data/20_evaluation/corpus_inventory_v1.json`, `research/original_model/manifests/dataset_manifest_v2.json`  

---

## 1. Executive Summary

Phase 34 independently reproduced and verified the Phase 33 corpus baseline before undertaking national legal expansion. The audit confirmed that historical claims of possessing 200M training tokens were groundless, and established the verified starting baseline of the repository across all document and token dimensions.

---

## 2. Verified Baseline Metrics Matrix

| Baseline Dimension | Reported Phase 33 Value | Independently Reproduced Value | Verification Verdict |
|---|---|---|---|
| **Total Registered Sources** | 59 | **59** | Bitwise Matched |
| **Eligible Pretraining Sources**| 57 | **57** | Verified under Section 52(1)(q) |
| **Excluded Sources** | 2 | **2** (`IND-JUD-DEL-2024-BAIL`, `IND-UNSUPPORTED-001`) | Quarantined / Scaffold |
| **Total Chunks in Knowledge Base**| 1,505 | **1,505** | Confirmed via SQLite PRAGMA |
| **Quarantined Synthetic Chunks**| 6 | **6** (`is_synthetic_scaffold = 1`) | Isolated |
| **Active Retrievable Chunks** | 1,499 | **1,499** | Confirmed |
| **Unique Normalized Passages**| 1,463 | **1,463** | SHA-256 Hashing |
| **Exact Duplicate Chunks** | 36 | **36** | Identified |
| **Near-Duplicate Pairs (>0.85 Jaccard)**| 403 | **403** | Shingle Analysis |
| **Usable Pretraining Tokens (V2)**| 336,892 | **336,892** | Tokenizer V2 Count |
| **English Usable Tokens** | 332,586 | **332,586** | 98.72% Share |
| **Authentic Hindi Tokens** | 4,306 | **4,306** | 1.28% Share (29 Provisions) |
| **Advocate Review Packages** | 40 pending | **40 pending** | Verified via Tracker |
| **Phase 9 Frozen Artifacts** | 6 byte-for-byte | **6 byte-for-byte** | SHA-256 Manifest Verified |

---

## 3. Distinction of Corpus Counting Layers

To prevent future conflation between database records and actual language model training volume, Phase 34 enforces strict categorization across 4 distinct layers:

1. **Layer 1: Registered Universe Records (59 Sources)** — Legal entities cataloged in source registries and metadata tables.
2. **Layer 2: RAG Knowledge Base Chunks (1,499 Active Chunks)** — Text fragments segmented specifically for BM25/FTS5 keyword search and retrieval.
3. **Layer 3: Normalized Pretraining Passages (1,528 Passages in Phase 33)** — Complete legal provisions with statutory context (`Act - Section: Text`), cleaned via NFC Unicode normalization.
4. **Layer 4: Tokenizer-Extracted Usable Tokens (336,892 Tokens in Phase 33)** — Input token sequences processed through `IndianLegalTokenizerV2`.

**Conclusion:** Chunk count cannot be equated with pretraining token volume. A 1,499-chunk database yields ~336k tokens, representing a severe deficit relative to the 200M tokens required for 10M-parameter pretraining.

