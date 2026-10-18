# Phase 35 Corpus Deduplication, Textual Quality and Leakage Audit

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Quality and Deduplication Methodology

The Phase 35 Quality Engine (`legalmitra/corpus/quality_engine.py`) performs deterministic corpus evaluation across four critical dimensions:
1. **Exact Duplicate Detection:** Full SHA-256 string matching on normalized provision text.
2. **Near-Duplicate Detection:** Word 3-gram Jaccard similarity evaluation (threshold $\ge 0.85$).
3. **Token Accounting:** Exact subword tokenization under `IndianLegalTokenizerV2` (bilingual BPE, vocabulary size 2,048).
4. **Source-Grouped Leakage Validation:** Zero cross-split source overlap between Train, Validation, and Test manifests.

---

## 2. Verified Corpus Metrics Audit

Auditing the 1,559 eligible pretraining passages:

```json
{
  "total_raw_passages": 1559,
  "total_eligible_passages": 1559,
  "excluded_passages_count": 0,
  "exact_duplicates_count": 0,
  "exact_duplicate_rate": 0.0,
  "near_duplicates_count": 2,
  "near_duplicate_rate": 0.0067,
  "total_tokens": 342965,
  "eligible_en_tokens": 334348,
  "eligible_hi_tokens": 8617,
  "excluded_tokens_count": 0,
  "leakage_detected": false,
  "leakage_details": []
}
```

### Analysis of Near-Duplicates:
- **Count:** Exactly 2 near-duplicate pairs identified (rate = 0.67%).
- **Nature of Repeated Language:** Both pairs correspond to standardized statutory enactments:
  1. Standard short title and commencement clauses across related central rules.
  2. Standard statutory severability and overriding effect clauses (`Section 3 / Section 4`).
- **Policy Decision:** Legitimate repeated statutory language is retained in the pretraining manifest. Removing standardized legal phrases distorts legal syntax and prevents models from learning authentic legal drafting conventions.

---

## 3. Train / Validation / Test Split Integrity

The source-grouped split strategy guarantees complete independence between pretraining, validation, and test evaluations:

| Split | Assigned Legal Sources | Passages | Tokens | Language Ratio |
|---|---|---|---|---|
| **Train** | All remaining eligible primary sources (33 Central/State statutes & judgments) | 1,380 | 304,291 | 97.4% EN / 2.6% HI |
| **Validation** | `IND-STAT-NI-1881`, `IND-STAT-SRA-1963`, `IND-STAT-CPC-1908-HI`, `IND-KA-STAT-KLRA-1961` | 25 | 3,928 | 91.2% EN / 8.8% HI |
| **Test** | `IND-STAT-LIMIT-1963`, `IND-STAT-DPDP-2023`, `IND-JUD-SC-2020-ARJUN-KHOTKAR`, `IND-STAT-IT-2000-HI`, `IND-JUD-BHC-2008-ROCHE-CIPLA` | 154 | 34,746 | 98.2% EN / 1.8% HI |
| **Total** | **Source Overlap: ZERO** | **1,559** | **342,965** | **100.0%** |

Zero data leakage was detected across all evaluation partitions.
