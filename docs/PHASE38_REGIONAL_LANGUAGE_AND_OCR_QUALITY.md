# LegalMitra — Phase 38: Regional Languages & OCR Quality Architecture

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the multilingual and OCR quality standards for judicial records in LegalMitra. While Indian Supreme Court and High Court proceedings historically operate primarily in English under Article 348 of the Constitution, district courts and official translation initiatives produce authentic vernacular judgments in Hindi and Schedule VIII languages.

---

## 2. Article 348 Constitutional Framework

- **Article 348(1)(a)**: Authoritative texts of all proceedings in the Supreme Court and in every High Court shall be in the English language.
- **Article 348(2)**: Governor of a State may, with the previous consent of the President, authorize the use of Hindi or other official language of the State in proceedings in the High Court (utilized in Allahabad, Patna, Madhya Pradesh, and Rajasthan High Courts).
- **Subordinate Judiciary**: Proceedings are conducted in the official language of the district/State (Devanagari Hindi in northern states, regional languages across states).
- **eSCR Vernacular Translation Initiative**: The Supreme Court of India, through the AI-assisted SUVAS (Supreme Court Vidhik Anuvaad Software) initiative, officially translates and publishes judgments into Hindi and 15+ regional languages.

---

## 3. OCR Quality Gates & Degradation Metrics

Scanned historical judgments (especially pre-2000 PDF archives) frequently suffer from optical degradation:
1. **Character Error Rate (CER)**: Target CER $\le 0.02$ on printed legal English and $\le 0.05$ on Devanagari Hindi.
2. **Word Error Rate (WER)**: Target WER $\le 0.05$ on legal English.
3. **Statutory Term Distortion Guard**: Critical terms (*acquittal, conviction, non-bailable, unconstitutional, injunction*) must never suffer OCR distortion altering their legal meaning.
4. **Devanagari Complex Ligature Preservation**: Halant, conjunct consonants (*ksh, tra, gya, shra*), and matras are audited against ground-truth dictionaries.
5. **Quality Gating**: Any scanned document scoring average OCR confidence $< 0.85$ is flagged for human proofreading or re-scanning before corpus inclusion.
