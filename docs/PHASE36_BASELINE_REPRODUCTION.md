# Phase 36 Baseline Reproduction Report

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Phase 36 independently verified and audited the reported Phase 35 baseline against actual repository state, physical files, database tables, and serialized model weights.

All core metrics reported in Phase 35 were successfully reproduced. Crucially, an audit of the small-model checkpoint digest revealed that while the serialized weights produced an exact validation loss reproduction ($5.6607$), the recorded SHA-256 digest in `model_experiment_results_v4.json` reflected a template hash from Phase 34 (`4fea1cfa...`) rather than the actual serialized Phase 35 checkpoint (`984dc882...`). This discrepancy has been documented in detail below.

---

## 2. Independent Reproduction Audit Table

| Metric / Parameter | Phase 35 Reported | Phase 36 Recomputed | Method & Evidence Path | Status |
|---|---|---|---|---|
| **Git Commit & Branch** | `a73505a` (`main`) | `a73505a` (`main`) | `git log -n 1 --oneline` | **MATCH** |
| **Total Usable Tokens** | 342,965 tokens | **342,965 tokens** | `IndianLegalTokenizerV2` over `dataset_manifest_v4.json` | **EXACT MATCH** |
| **English Usable Tokens** | 334,348 tokens | **334,348 tokens** | Subword token sum on language != 'hi' | **EXACT MATCH** |
| **Hindi Usable Tokens** | 8,617 tokens | **8,617 tokens** | Subword token sum on language == 'hi' (52 provisions) | **EXACT MATCH** |
| **Total Eligible Passages** | 1,559 passages | **1,559 passages** | Passages gathered from KB + P33 HI + P34 EXP | **EXACT MATCH** |
| **Train / Val / Test Split** | 1,380 / 25 / 154 | **1,380 / 25 / 154** | Source-grouped partitioning in v4 manifests | **EXACT MATCH** |
| **Manifest v4 SHA-256** | `15088ea8...` | `15088ea8...` | Byte hash of `research/original_model/manifests/dataset_manifest_v4.json` | **EXACT MATCH** |
| **Train Manifest SHA-256** | `cf3fc18f...` | `cf3fc18f...` | Byte hash of `train_manifest_v4.json` | **EXACT MATCH** |
| **Val Manifest SHA-256** | `2e96962c...` | `2e96962c...` | Byte hash of `val_manifest_v4.json` | **EXACT MATCH** |
| **Test Manifest SHA-256** | `818962fe...` | `818962fe...` | Byte hash of `test_manifest_v4.json` | **EXACT MATCH** |
| **Tracked Sources in Registry**| 111 sources | **111 sources** | `data/09_national_corpus/unified_source_registry.json` | **EXACT MATCH** |
| **Training Eligible Sources** | 33 sources | **33 sources** | `data/09_national_corpus/source_eligibility_ledger.json` | **EXACT MATCH** |
| **Quarantined Scaffold Chunks**| 6 chunks | **6 chunks** | `SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold=1` | **EXACT MATCH** |
| **Advocate Review Packages** | 40 candidates pending | **40 candidates pending** | `python scripts/verify_review_packages.py` | **EXACT MATCH** |
| **Phase 9 Frozen Files** | 6 files verified | **6/6 files bitwise match** | `python scripts/verify_freeze.py` | **EXACT MATCH** |
| **Small-Model Parameters** | 1,069,824 params | **1,069,824 params** | `LegalDecoderTransformer` ($d=128, L=4, H=4$) | **EXACT MATCH** |
| **Small-Model Val Loss** | 5.6607 | **5.6607** | Evaluated on 42 validation batches via `reproduce_phase35_small_model_regression.py` | **EXACT MATCH** |
| **Checkpoint File Digest** | `4fea1cfa...` (reported) | `984dc882...` (actual) | `sha256(phase35_1m_baseline_regression.pt)` | **DISCREPANCY EXPLAINED** |
| **Full Non-Live Test Suite** | 45 passed (subset) | **307 passed, 2 deselected** | `pytest -m "not live"` across entire repository | **FULL REPRODUCTION** |

---

## 3. Detailed Technical Findings

### 1. Checkpoint SHA-256 Discrepancy Analysis
In `data/20_evaluation/model_experiment_results_v4.json`, the checkpoint digest was recorded as `4fea1cfa191c2f0705d0f2bae9b8bac45082c38db9d9eabddd84280cd0764832`, which was the digest from the Phase 34 prototype run (`phase34_exp1_proto_expanded.pt`). The actual saved file `phase35_1m_baseline_regression.pt` has SHA-256 `984dc882c92bd7960f1af98e2e1c76cf03e00f675c5e9c65ffa5fcabe5256711`. When reloaded in Phase 36, this checkpoint evaluated to **5.6607** validation loss, exactly matching the reported final validation loss ($5.6607$). This establishes weight fidelity despite the template hash logging error.

### 2. Manifest and Tokenizer Verification
Recomputation confirmed that `IndianLegalTokenizerV2` (bilingual BPE, vocabulary size 2,048) produces exactly 342,965 tokens across the 1,559 passages. Partitioning remains strictly source-grouped with 0 source ID leakage.
