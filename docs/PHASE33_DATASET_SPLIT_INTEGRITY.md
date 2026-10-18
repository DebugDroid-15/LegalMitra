# LegalMitra Phase 33: Dataset Split Integrity and Leakage Elimination Report

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Master Manifest:** `research/original_model/manifests/dataset_manifest_v2.json`  
**Train Manifest:** `research/original_model/manifests/train_manifest_v2.json`  
**Val Manifest:** `research/original_model/manifests/val_manifest_v2.json`  
**Test Manifest:** `research/original_model/manifests/test_manifest_v2.json`  

---

## 1. Executive Summary

Phase 32 proved that naive sequential splitting (e.g. slicing 90% of corpus rows) introduces substantial intra-document leakage when chunks of the same statute span both splits. Phase 33 implements an enhanced `source_grouped_bilingual` dataset builder (`scripts/build_phase33_datasets.py`) that strictly partitions entire legislative instruments, judicial cases, and official gazettes across Train, Validation, and Held-out Test boundaries.

---

## 2. Split Partitioning & Source Grouping

```
Total Active Legal Universe: 57 Eligible Sources (1,528 passages, 336,892 tokens)
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
[TRAIN SET]           [VALIDATION SET]      [HELD-OUT TEST SET]
50 Sources (87.7%)    3 Sources (5.3%)      4 Sources (7.0%)
1,351 Passages        24 Passages           153 Passages
2,969 Samples         40 Samples            334 Samples
276,438 Tokens        13,674 Tokens         46,780 Tokens
(EN: 272,374 | HI: 4,064) (EN: 13,546 | HI: 128) (EN: 46,666 | HI: 114)
```

### Explicit Source Assignments
1. **Held-Out Test Sources (Never seen during training or validation):**
   - `IND-STAT-LIMIT-1963` (The Limitation Act, 1963 - Central Statute)
   - `IND-STAT-DPDP-2023` (Digital Personal Data Protection Act, 2023 - Modern Data Law)
   - `IND-JUD-SC-2020-ARJUN-KHOTKAR` (Supreme Court Landmark on Section 65B Electronic Evidence)
   - `IND-STAT-IT-2000-HI` (Information Technology Act, 2000 - Official Hindi Provisions)
2. **Validation Sources (Hyperparameter tuning & step-loss monitoring):**
   - `IND-STAT-NI-1881` (Negotiable Instruments Act, 1881)
   - `IND-STAT-SRA-1963` (Specific Relief Act, 1963)
   - `IND-STAT-CPC-1908-HI` (Code of Civil Procedure, 1908 - Official Hindi Provisions)
3. **Train Sources:** All 50 remaining Central Statutes, State Acts, Judgments, and Hindi provisions (Constitution, BNS, BNSS, BSA, ICA).

---

## 3. Cryptographic Leakage Verification

| Invariant Verification Property | Result | Status |
|---|---|---|
| **Cross-Split Source Overlap (Train $\cap$ Val)** | **0 sources** | **PASS** |
| **Cross-Split Source Overlap (Train $\cap$ Test)**| **0 sources** | **PASS** |
| **Cross-Split Source Overlap (Val $\cap$ Test)**  | **0 sources** | **PASS** |
| **Exact Duplicate Passages Across Splits**       | **0 duplicates** | **PASS** |
| **Quarantined Scaffold Inclusion**               | **0 chunks** (`IND-JUD-DEL-2024-BAIL` excluded) | **PASS** |
| **User Conversation Inclusion**                  | **0 chunks** (`conversations.db` isolated) | **PASS** |
| **Pending Review Candidate Inclusion**           | **0 records** (40 packages intact) | **PASS** |
| **Hidden Benchmark Ground Truth Inclusion**      | **0 records** (v1–v9 benchmarks excluded) | **PASS** |

---

## 4. Manifest Hashes (SHA-256)

- `train_manifest_v2.json`: `5e9fa56dd5e28a3f5a11c1d0f5195ea11a51a9ec67bc2f2162ca6f042e6d6342`
- `val_manifest_v2.json`: `097b69a2399990e66d216503b87fe2e4ba9b64ea7dcaec6369ddf3b92eb182e0`
- `test_manifest_v2.json`: `6599144421b5821c9a632e2764b855848bb226871a2aeb6014457eeaa8ec9a90`

