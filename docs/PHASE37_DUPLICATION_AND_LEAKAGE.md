# Phase 37 Duplication & Data Leakage Audit Report

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

Data leakage across training, validation, and test splits leads to artificially deflated evaluation loss and catastrophic failure of real-world legal generalization. In legal text corpora, naive random chunk splitting causes severe **intra-document leakage**, where adjacent sections of the same statute or paragraphs of the same judgment appear simultaneously in train and test sets.

To eliminate intra-document leakage, LegalMitra enforces **source-grouped partitioning**, where entire statutory instruments and judicial authorities are assigned exclusively to a single partition.

Phase 37 audited the 1,633 passages in `dataset_manifest_v5.json` for exact duplicate rates, near-duplicate rates, and cross-split source leakage.

---

## 2. Partition Inventory & Source Allocation

| Split Partition | Passages Count | Token Count | Language Breakdown | Assigned Source Identifiers |
| :--- | :--- | :--- | :--- | :--- |
| **Train Split** | 1,408 | 310,605 | English (dominant) + Hindi (`IND-STAT-BNS-2023-HI`, `IND-CONST-1950-HI`, etc.) | All primary KB chunks, BNS-2023-HI (33 sections), IT Intermediary Rules, TN Transparency in Tenders, Bombay HC Vodafone, Calcutta HC Green Earth, BNS Commencement Notification. |
| **Validation Split**| 43 | 6,961 | English (`NI-1881`, `SRA-1963`, `KLRA-1961`, `DHC-ORIG-2018`) + Hindi (`CPC-1908-HI`, `BSA-2023-HI`, `BSA Commencement`) | `IND-STAT-NI-1881`, `IND-STAT-SRA-1963`, `IND-STAT-CPC-1908-HI`, `IND-KA-STAT-KLRA-1961`, `IND-STAT-BSA-2023-HI`, `IND-DEL-RULE-DHC-ORIG-2018`, `IND-GAZ-COMMENCE-BSA-2024`. |
| **Test Split** | 182 | 39,792 | English (`LIMIT-1963`, `DPDP-2023`, `ARJUN-KHOTKAR`, `ROCHE-CIPLA`, `WBLR-1955`) + Hindi (`IT-2000-HI`, `BNSS-2023-HI`, `BNSS Commencement`) | `IND-STAT-LIMIT-1963`, `IND-STAT-DPDP-2023`, `IND-JUD-SC-2020-ARJUN-KHOTKAR`, `IND-STAT-IT-2000-HI`, `IND-JUD-BHC-2008-ROCHE-CIPLA`, `IND-STAT-BNSS-2023-HI`, `IND-WB-STAT-WBLR-1955`, `IND-GAZ-COMMENCE-BNSS-2024`. |
| **Total Corpus** | **1,633** | **357,358** | **337,487 EN / 19,871 HI** | **Zero cross-split overlap across all sources** |

---

## 3. Cross-Split Source Leakage Audit

Let $S_{train}$, $S_{val}$, and $S_{test}$ represent the disjoint sets of source identifiers present in the three partitions. The audit evaluated:

$$\left| S_{train} \cap S_{val} \right| = 0$$
$$\left| S_{train} \cap S_{test} \right| = 0$$
$$\left| S_{val} \cap S_{test} \right| = 0$$

- **Measured Train $\cap$ Val Overlap:** Exactly 0 sources (0 passages).
- **Measured Train $\cap$ Test Overlap:** Exactly 0 sources (0 passages).
- **Measured Val $\cap$ Test Overlap:** Exactly 0 sources (0 passages).
- **Audit Outcome:** **ZERO DATA LEAKAGE DETECTED (`leakage_detected = False`)**.

---

## 4. Textual Duplication Metrics

Evaluated using `CorpusQualityEngine` (`legalmitra/corpus/quality_engine.py`):

| Metric | Target Specification | Measured Value | Status |
| :--- | :--- | :--- | :--- |
| **Exact Duplicate Rate** | Exactly 0.0% (0 identical SHA-256 hashes) | **0.0% (0 / 1,633)** | **PASS** |
| **Near-Duplicate Rate** | $< 1.0\%$ (Character 5-gram Jaccard similarity $\ge 0.85$) | **0.0067 (0.67%)** | **PASS** |
| **Intra-Split Duplication** | 0 duplicate passages within any split | **0 duplicates** | **PASS** |
| **Cross-Split Duplication** | 0 shared text passages between any splits | **0 shared passages** | **PASS** |

The 0.67% near-duplicate rate is attributed to standard statutory formulaic phrases (e.g. enacting clauses and standard penalty penalty provisions across sections), which fall comfortably within allowable linguistic variations.

---

## 5. Audit Conclusion

The Phase 37 dataset manifests strictly satisfy all zero-leakage and anti-memorization gates. The held-out validation and test partitions provide completely unbiased, independent benchmarks for evaluating model generalization.

