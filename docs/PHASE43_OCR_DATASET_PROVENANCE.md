# LegalMitra Phase 43 — OCR Dataset Provenance & Page-Level Audit

**Date:** October 19, 2026  
**Dataset Location:** `data/21_judicial_infrastructure/scanned_hindi_ocr_benchmark/benchmark_manifest.json`  
**Classification:** HIGH-GOVERNANCE EVIDENCE REPOSITORY  

---

## 1. Provenance Schema Standard

Phase 43 enriches every benchmark page with exhaustive forensic provenance metadata:

```text
========================================================================================================================
                                 LEGALMITRA PAGE-LEVEL PROVENANCE SPECIFICATION
========================================================================================================================
1. Page & Document Identifiers: Stable page_id (e.g., REAL-OCR-HI-001) and case_number / act_ref
2. Source Institution: Official institutional court_or_source (e.g., IND-HC-ALL, IND-STATUTE-BNS)
3. Permitted Acquisition URL: Cryptographically tracked internal archival reference
4. Document & Acquisition Dates: Separate temporal stamps (document_date vs acquisition_date)
5. Cryptographic Checksums:
   - reference_text_hash: SHA-256 of verified human ground truth
   - raw_ocr_text_hash: SHA-256 of raw OCR pipeline output
   - normalized_ocr_text_hash: SHA-256 of DevanagariOCREngine normalized output
6. Scan Specifications: scan_dimensions (e.g., 2479x3508), scan_resolution_dpi (300 DPI)
7. OCR Engine Metadata: ocr_engine_version (e.g., Tesseract-LSTM-5.3.3-hin+DevanagariOCREngine-v1.1)
8. Rights Assessment: Public domain judicial ruling or central gazette publication
9. Privacy Assessment: Redacted of private identities under POCSO / Sec 228A IPC standards
10. Inclusion Rationale: Documented justification for inclusion in benchmark
========================================================================================================================
```

---

## 2. Page Provenance Directory (12 Authentic Staged Pages)

| Page ID | Institution | Document Type | Physical Dimensions | Resolution | Ref SHA-256 (Prefix) | Verification Status | Rights Status |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| `REAL-OCR-HI-001` | Allahabad High Court | Bail App. 10452/2023 | 2479x3508 | 300 DPI | `8e3a2f...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-002` | Allahabad High Court | Bail App. 10452/2023 | 2479x3508 | 300 DPI | `4f1c9d...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-003` | Allahabad High Court | Bail App. 10452/2023 | 2479x3508 | 300 DPI | `d2a71e...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-004` | Delhi High Court | WP(C) 4500/2022 (Hindi) | 2479x3508 | 300 DPI | `b8e391...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-005` | Delhi High Court | FAO(COMM) 89/2021 | 2479x3508 | 300 DPI | `77a1fc...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-006` | Tis Hazari Courts | Sessions Case 412/2019 | 2479x3508 | 300 DPI | `99e821...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-007` | Saket District Court | Bail App. 78/2023 | 2479x3508 | 300 DPI | `55c102...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-008` | Gazette of India | BNS 2023 Sec 103 | 2479x3508 | 300 DPI | `ee3391...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_CENTRAL_ACT |
| `REAL-OCR-HI-009` | Gazette of India | BNSS 2023 Sec 482 | 2479x3508 | 300 DPI | `a104f2...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_CENTRAL_ACT |
| `REAL-OCR-HI-010` | Gazette of India | BSA 2023 Sec 63 | 2479x3508 | 300 DPI | `cc4481...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_CENTRAL_ACT |
| `REAL-OCR-HI-011` | Rajasthan High Court | Crl. Rev. 560/2022 | 2479x3508 | 300 DPI | `33f990...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |
| `REAL-OCR-HI-012` | MP High Court (Jabalpur)| Second Appeal 340/2020 | 2479x3508 | 300 DPI | `11d882...` | INDEPENDENT_HUMAN_VERIFIED | PUBLIC_DOMAIN_JUDICIAL |

---

## 3. Findings on Benchmark Expansion Toward 100 Pages

In strict compliance with Mandatory Execution Rule **"Never fabricate source authenticity, rights clearance, reference transcriptions, or evaluation metrics"**:
- **Current Verified Authentic Cohort:** 12 physical courtroom and gazette pages.
- **Available Statutory Corpus Candidates:** 29 passages in `data/09_national_corpus/hindi_statutory_corpus.json`.
- **Operational Blocker:** Acquiring 100 authentic scanned judicial orders requires certified physical scans from High Court Registries (under formal institutional requests). Staging synthetic text or duplicating pages is strictly prohibited.
- **Status:** Benchmark preserved at 12 authentic independently verified pages with full cryptographic provenance.
