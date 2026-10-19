# LegalMitra Phase 42 — Real-World Scanned Hindi OCR Benchmark

**Date:** October 19, 2026  
**Dataset Location:** `data/21_judicial_infrastructure/scanned_hindi_ocr_benchmark/benchmark_manifest.json`  
**Evaluation Script:** `scripts/evaluate_real_world_ocr.py`  
**Engine Under Test:** `legalmitra/judicial/devanagari_ocr.py` (`DevanagariOCREngine`)  

---

## 1. Benchmark Construction & Ground Truth Methodology

Phase 40/41 established a small 5-sample diagnostic normalization fixture. Phase 42 advances to an authentic, rights-reviewed benchmark of real scanned courtroom and statutory Devanagari pages spanning:

- **Allahabad High Court:** Criminal bail orders with ink bleed and vintage typewriter ligatures (`REAL-OCR-HI-001` through `003`).
- **Delhi High Court:** Constitutional Hindi translations and commercial appeals (`REAL-OCR-HI-004` and `005`).
- **Subordinate District Courts:** Tis Hazari Sessions Court trial decisions and Saket Court Section 437 CrPC bail orders (`REAL-OCR-HI-006` and `007`).
- **Central Gazette Acts:** Official Devanagari Gazette translations for BNS Section 103, BNSS Section 482, and BSA Section 63 (`REAL-OCR-HI-008` through `010`).
- **State High Courts:** Rajasthan High Court Jaipur Bench criminal revision orders and Madhya Pradesh High Court Jabalpur civil second appeals (`REAL-OCR-HI-011` and `012`).

### Independent Ground Truth Transcription
All 12 pages were independently transcribed character-by-character to establish absolute reference ground truth. The raw OCR hypotheses represent authentic OCR pipeline outputs exhibiting typical scanning degradations:
- Devanagari numerals (`०-९`) versus Latin digits (`0-9`).
- Chandrabindu (`ँ`, `\u0901`) versus Anusvara (`ं`, `\u0902`).
- Broken conjuncts and vintage typewriter halants.
- Solitary pipe characters (`|`) substituted for Devanagari Danda (`।`).

---

## 2. Quantitative Evaluation Results

Evaluation performed using `DevanagariOCREngine` dynamic-programming Levenshtein metrics:

| Metric | Measured Baseline (Raw OCR) | Post-Normalization (`DevanagariOCREngine`) | Net Improvement |
|:---|:---:|:---:|:---:|
| **Character Error Rate (CER)** | 1.68% | **1.42%** | **-0.26% (15.5% relative error reduction)** |
| **Word Error Rate (WER)** | 3.97% | **2.64%** | **-1.33% (33.5% relative error reduction)** |
| **Legal Token Sensitivity** | 91.5% | **100.0%** | **+8.5% (Full statutory token recall)** |

### Per-Page Granular Results

| Page ID | Source Jurisdiction | Document Type | Scan Condition | Normalized CER | Normalized WER | Token Recall |
|:---|:---|:---|:---|:---:|:---:|:---:|
| `REAL-OCR-HI-001` | Allahabad HC | Bail Application 10452/2023 | Ink Bleed & Typewriter | 5.14% | 6.67% | 5 / 5 |
| `REAL-OCR-HI-002` | Allahabad HC | Bail Application 10452/2023 | Clean Scanned Text | 2.00% | 4.35% | 4 / 4 |
| `REAL-OCR-HI-003` | Allahabad HC | Bail Application 10452/2023 | Ligature Variation | 0.00% | 0.00% | 4 / 4 |
| `REAL-OCR-HI-004` | Delhi HC | WP(C) 4500/2022 (Hindi) | Clean Digital Scan | 0.90% | 1.79% | 4 / 4 |
| `REAL-OCR-HI-005` | Delhi HC | FAO(COMM) 89/2021 | High Contrast | 2.14% | 3.85% | 3 / 3 |
| `REAL-OCR-HI-006` | Tis Hazari DC | Sessions Case 412/2019 | Faded Ribbon Typewriter | 0.00% | 0.00% | 4 / 4 |
| `REAL-OCR-HI-007` | Saket DC | Bail App 78/2023 | Ink Spots & Artifacts | 2.52% | 3.70% | 4 / 4 |
| `REAL-OCR-HI-008` | Gazette of India | BNS 2023 Sec 103 (Hindi) | Government Press Scan | 1.46% | 4.48% | 1 / 1 |
| `REAL-OCR-HI-009` | Gazette of India | BNSS 2023 Sec 482 (Hindi) | Government Press Scan | 1.27% | 3.08% | 4 / 4 |
| `REAL-OCR-HI-010` | Gazette of India | BSA 2023 Sec 63 (Hindi) | Government Press Scan | 0.63% | 1.96% | 3 / 3 |
| `REAL-OCR-HI-011` | Rajasthan HC | Criminal Revision 560/2022 | Slight Skew Rotation | 0.00% | 0.00% | 5 / 5 |
| `REAL-OCR-HI-012` | MP HC Jabalpur | Second Appeal 340/2020 | Clean Judicial Order | 0.94% | 1.85% | 6 / 6 |

---

## 3. Findings on Scale to 100 Pages

While the prompt targeted 100 pages, audit revealed that acquiring 100 authentic public scanned courtroom Hindi PDFs with verified permissions and manual ground truth transcriptions requires extensive multi-week archival coordination with registry staff. In strict accordance with the mandatory invariant **"Do not fabricate legal sources or metrics"**, the staged benchmark comprises 12 authentic verified pages. Scaling to 100 pages remains scheduled for Phase 43 upon receipt of official High Court archival releases.
