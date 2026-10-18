# LegalMitra — Phase 39: Representative Acquisition Batch Report

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the bounded, representative national acquisition batch executed in Phase 39 Workstream D. Rather than ingesting only famous Supreme Court judgments, the batch deliberately tests institutional diversity, jurisdictional heterogeneity, procedural variation, and multi-era archives across the full Indian judicial hierarchy.

Machine-readable payload: `data/21_judicial_infrastructure/representative_acquisition_batch.json`.

---

## 2. Representative Acquisition Batch Composition (20 Cases)

| Document ID | Court Tier | Court & Citation | Key Legal Topic / Ratio Anchor | OCR Conf. |
| :--- | :--- | :--- | :--- | :---: |
| `DOC-SC-1973-KESAVANANDA` | APEX | Supreme Court ((1973) 4 SCC 225) | Basic Structure Doctrine (Para 761) | 0.992 |
| `DOC-SC-1978-MANEKA` | APEX | Supreme Court ((1978) 1 SCC 248) | Substantive due process under Article 21 (Para 56) | 0.988 |
| `DOC-SC-2017-PUTTASWAMY` | APEX | Supreme Court ((2017) 10 SCC 1) | Fundamental Right to Privacy (Para 122) | 0.995 |
| `DOC-SC-2015-SHREYA` | APEX | Supreme Court ((2015) 5 SCC 1) | Invalidation of Section 66A IT Act (Para 119) | 0.991 |
| `DOC-SC-2018-NAVTEJ` | APEX | Supreme Court ((2018) 1 SCC 791) | Decriminalization of consensual intimacy (Para 268) | 0.994 |
| `DOC-SC-2023-PARASHOTAM` | APEX | Supreme Court (2023 INSC 261) | Article 226 judicial review over AFT orders (Para 35) | 0.996 |
| `DOC-SC-2023-HINDI-BAIL` | APEX | Supreme Court (2022 INSC 690 - Hindi) | Satyendar Antil bail guidelines in authentic Hindi (Para 25) | 0.988 |
| `DOC-HC-DEL-2009-NAZ` | HIGH_COURT | Delhi High Court (2009 (160) DLT 277) | Section 377 read down by High Court (Para 132) | 0.985 |
| `DOC-HC-DEL-2014-MUKESH` | HIGH_COURT | Delhi High Court (2014 (208) DLT 1) | Nirbhaya death sentence confirmation (Para 210) | 0.987 |
| `DOC-HC-BOM-2006-BARGIRLS`| HIGH_COURT| Bombay High Court (2006 (3) BomCR 705)| Dance bar prohibition struck down (Para 88) | 0.976 |
| `DOC-HC-ALL-1975-RAJNARAIN`| HIGH_COURT| Allahabad High Court (AIR 1975 All 287)| Election petition setting aside election (Para 140) | 0.968 |
| `DOC-HC-MAD-2012-AWBI` | HIGH_COURT | Madras High Court ((2012) 2 MLJ 45) | Animal welfare and statutory protection (Para 1) | 0.979 |
| `DOC-HC-CAL-2000-WETLANDS` | HIGH_COURT | Calcutta High Court (AIR 1993 Cal 215) | East Kolkata Wetlands conservation PIL (Para 1) | 0.972 |
| `DOC-TR-NCLAT-2019-TATA` | TRIBUNAL | NCLAT ([2020] 154 SCL 264) | Corporate oppression & conversion (Para 180) | 0.989 |
| `DOC-TR-NGT-2016-ALMITRA` | TRIBUNAL | NGT (2016 SCC OnLine NGT 1625) | Solid waste management directives (Para 74) | 0.984 |
| `DOC-TR-CAT-2018-PENSION` | TRIBUNAL | CAT Principal Bench (OA 1045/2017) | Civil service pension entitlement (Para 1) | 0.978 |
| `DOC-MIL-AFT-2019-DISABILITY`| MILITARY | Armed Forces Tribunal (OA 560/2018) | Disability pension attributable to military service (Para 15) | 0.981 |
| `DOC-HIST-FED-1942-NIHARENDU`| HISTORICAL| Federal Court of India ([1942] FCR 38) | Sedition gist requires public disorder (Para 12) | 0.952 |
| `DOC-HIST-PC-1939-PAKALA` | HISTORICAL| Privy Council ((1939) L.R. 66 I.A. 66) | Dying declaration & confession definition (Para 18) | 0.961 |
| `DOC-DIST-DEL-2021-BAIL` | DISTRICT | Tis Hazari Sessions Court (DLCT010012342021)| Regular bail order under Section 439 CrPC (Para 8) | 0.945 |

---

## 3. Acquisition Pipeline Invariant Checks

1. **Cryptographic Integrity**: Every acquired document has a verified 64-character hex SHA-256 hash.
2. **Paragraph Anchoring**: Every document includes discrete paragraph-level anchors mapping paragraph numbers, text snippets, and token counts.
3. **Retrieval vs Training Gating**: All 20 documents are marked `is_retrieval_eligible = True` and `is_training_eligible = False`.
