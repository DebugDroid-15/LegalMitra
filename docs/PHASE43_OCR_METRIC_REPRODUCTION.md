# LegalMitra Phase 43 — OCR Metric Reproduction: Micro vs Macro Analysis

**Date:** October 19, 2026  
**Execution Script:** `scripts/evaluate_real_world_ocr.py`  
**Dataset:** `data/21_judicial_infrastructure/scanned_hindi_ocr_benchmark/benchmark_manifest.json`  

---

## 1. Metric Mathematical Definitions

In optical character recognition evaluation, reporting only macro-averages (averaging per-page percentages) can obscure differences caused by document length variation. Phase 43 reports both **Macro-Averaged** and **Micro-Averaged** metrics.

### Mathematical Formulations:

$$\text{Macro CER} = \frac{1}{N} \sum_{i=1}^N \frac{\text{Levenshtein}(R_{c,i}, H_{c,i})}{|R_{c,i}|}$$

$$\text{Micro CER} = \frac{\sum_{i=1}^N \text{Levenshtein}(R_{c,i}, H_{c,i})}{\sum_{i=1}^N |R_{c,i}|}$$

$$\text{Macro WER} = \frac{1}{N} \sum_{i=1}^N \frac{\text{Levenshtein}(R_{w,i}, H_{w,i})}{|R_{w,i}|}$$

$$\text{Micro WER} = \frac{\sum_{i=1}^N \text{Levenshtein}(R_{w,i}, H_{w,i})}{\sum_{i=1}^N |R_{w,i}|}$$

$$\text{Legal Token Recall} = \frac{\sum_{i=1}^N |T_i \cap H_{i, \text{norm}}|}{\sum_{i=1}^N |T_i|}$$

---

## 2. Recomputed Empirical Baseline & Normalized Results

| Metric Dimension | Raw Baseline (Pre-Normalization) | Post-Normalization (`DevanagariOCREngine`) | Relative Improvement |
|:---|:---:|:---:|:---:|
| **Macro Character Error Rate (CER)** | **1.68%** | **1.42%** | **-15.5% relative error reduction** |
| **Micro Character Error Rate (CER)** | **1.72%** | **1.46%** | **-15.1% relative error reduction** |
| **Macro Word Error Rate (WER)** | **3.97%** | **2.64%** | **-33.5% relative error reduction** |
| **Micro Word Error Rate (WER)** | **4.06%** | **2.76%** | **-32.0% relative error reduction** |
| **Legal Token Recall** | 91.5% (43 / 47) | **100.0% (47 / 47)** | **+8.5% (Full statutory token recovery)** |

---

## 3. Per-Document Category Performance Breakdown

| Document Cohort | Sample Count | Total Ref Chars | Macro Raw CER | Macro Norm CER | Macro Raw WER | Macro Norm WER | Token Recall |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **High Court Bail & Civil Orders** (Allahabad, Delhi, Rajasthan, MP) | 7 | 2,244 | 1.83% | **1.58%** | 4.31% | **2.65%** | 30 / 30 (100%) |
| **Subordinate District Courts** (Tis Hazari, Saket) | 2 | 611 | 1.43% | **1.26%** | 2.83% | **1.85%** | 8 / 8 (100%) |
| **Central Gazette Statutory Enactments** (BNS, BNSS, BSA) | 3 | 975 | 1.12% | **1.12%** | 3.17% | **3.17%** | 9 / 9 (100%) |
| **Aggregate Benchmark** | **12** | **3,830** | **1.68%** | **1.42%** | **3.97%** | **2.64%** | **47 / 47 (100%)** |
