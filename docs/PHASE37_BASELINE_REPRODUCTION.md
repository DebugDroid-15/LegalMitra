# LegalMitra Phase 37 — Baseline Reproduction Audit

**Phase:** 37  
**Timestamp:** 2026-10-18T23:17:00Z  
**Branch:** `main`  
**Starting Commit:** `f2b0073da6d542e65479aa3bc58616a96f9e89cf`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Status:** VERIFIED & REPRODUCED EXACT MATCH

---

## 1. Executive Summary

Prior to initiating Phase 37 national legal corpus expansion and Hindi criminal codes acquisition, the baseline repository state was independently audited and verified against all Phase 36 release criteria. All test suites, frozen artifacts, review registries, database isolation boundaries, and model regression checkpoints were recomputed from disk.

The starting baseline reproduces bitwise fidelity with zero discrepancies across all dimensions.

---

## 2. Invariant Verification Results

| Invariant Item | Target Specification | Measured Value | Status |
| :--- | :--- | :--- | :--- |
| **Git Working Tree** | Clean, zero untracked/dirty files | Clean (`git status --short` empty) | **PASS** |
| **Git Commit HEAD** | `f2b0073` | `f2b0073da6d542e65479aa3bc58616a96f9e89cf` | **PASS** |
| **Remote Branches** | Synchronized with origin | Up to date with `origin/main` & `origin/master` | **PASS** |
| **Phase 9 Frozen Artifacts** | 6 files matching frozen SHA-256 | 6/6 verified bitwise identical | **PASS** |
| **Advocate Review Tracking** | 40 candidates in `pending_legal_review` | 40/40 strictly pending in tracking register | **PASS** |
| **Synthetic Scaffold Chunks** | Exactly 6 quarantined chunks in KB | 6 synthetic, 1,499 real chunks in `legalmitra_kb.db` | **PASS** |
| **Database Physical Boundary** | `legalmitra_kb.db` separated from `conversations.db` | Independent SQLite files; zero cross-table presence | **PASS** |
| **Non-Live Test Suite** | >= 315 passing tests | 315 passed, 2 deselected in 81.24s | **PASS** |
| **Root README Physical Lines** | >= 10,000 lines | 10,023 physical lines (8,664 non-empty) | **PASS** |

### 2.1 Frozen Artifact Checksums (Phase 9 Freeze Invariant)
```text
pilot_20_examples.jsonl:         e01b22f50f36c3927b595ecd03e2258c6889f299e6394644b2cd4cb359ffa953
pilot_20_manifest.json:          9da3801fdc79514987dcd91ffacc81372ab5412a93002ddfd3d9c1c7050369a4
pilot_20_review_sheet.csv:       6f519165d45bac465e2c25de20369b74d136543307a49ecb84559f68a7dadcab
pilot_20_source_bundle.json:     3cf555e96743ece27b0e22d954d6535cea8a51cc9242c471416b9f46fb031f10
pilot_20_open_issues.md:         0b82c4f6df0d9b6c755c6bf15ffb582c07cc6788a28d8ff610de4b645251f45e
PHASE8_OPEN_LEGAL_ISSUES_REG.md: e5966e245c15f6cb96e48d57ede8e81be8a89ebe3aa843098afc961e86c2c508
```

---

## 3. Pretraining Dataset Manifest v4 Baseline Reproduction

Evaluated using `IndianLegalTokenizerV2` (`research/original_model/tokenizer_v2.json`, vocabulary size 2,048):

| Metric | Recorded v4 Manifest | Independently Recomputed | Match Status |
| :--- | :--- | :--- | :--- |
| **Total Passages** | 1,559 | 1,559 | **EXACT MATCH** |
| **Train Passages** | 1,380 | 1,380 | **EXACT MATCH** |
| **Validation Passages** | 25 | 25 | **EXACT MATCH** |
| **Test Passages** | 154 | 154 | **EXACT MATCH** |
| **Total Usable Tokens** | 342,965 | 342,965 | **EXACT MATCH** |
| **English Tokens** | 334,348 | 334,348 | **EXACT MATCH** |
| **Hindi Tokens** | 8,617 | 8,617 | **EXACT MATCH** |
| **Train Partition Tokens** | 304,291 | 304,291 | **EXACT MATCH** |
| **Validation Partition Tokens**| 3,928 | 3,928 | **EXACT MATCH** |
| **Test Partition Tokens** | 34,746 | 34,746 | **EXACT MATCH** |
| **Dataset Manifest SHA-256** | `15088ea8e24555478a54fcb7d44bddefe39a1370fe3597bb298d2e3511f3cc4e` | Identical | **EXACT MATCH** |
| **Train Manifest SHA-256** | `cf3fc18f4bf87329e2f473ca49a9907fb2df16f86986cd1bc10ae98c06d0d822` | Identical | **EXACT MATCH** |
| **Val Manifest SHA-256** | `2e96962c9859c3f7824093cd9d9b754f6c2fa6d07a02aeb8d3ffe906c4fbf118` | Identical | **EXACT MATCH** |
| **Test Manifest SHA-256** | `818962fecbb7efafeddbf8080a7c3e2853a47bd38d9f28389c64e55e4abc0d23` | Identical | **EXACT MATCH** |

---

## 4. Small-Model Baseline Regression Reproduction

- **Model Architecture**: 4-layer Decoder Transformer (`d_model=128`, `n_heads=4`, `seq_len=128`)
- **Total Parameters**: 1,069,824 (1.07M)
- **Checkpoint Location**: `research/original_model/checkpoints/phase35_1m_baseline_regression.pt`
- **Checkpoint SHA-256**: `984dc882c92bd7960f1af98e2e1c76cf03e00f675c5e9c65ffa5fcabe5256711`
- **Measured Validation Loss**: **5.6607** (Evaluated on held-out validation partition of 42 batches)
- **Fidelity Status**: **EXACT MATCH**

---

## 5. Starting Milestone B Gap Assessment

- **Milestone B Target**: 1,000,000 verified legal tokens
- **Current Baseline**: 342,965 verified tokens
- **Token Deficit**: **657,035 tokens**
- **Hindi Representation**: 8,617 tokens (2.51% of corpus)
- **Immediate Priority**: Acquire authentic Hindi legal primary sources (BNS, BNSS, BSA) and national statutory coverage while adhering to strict Section 52(1)(q) rights safeguards and zero-leakage constraints.

