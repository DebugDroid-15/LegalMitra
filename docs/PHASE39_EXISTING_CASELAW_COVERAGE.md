# LegalMitra — Phase 39: Existing Case-Law Coverage Baseline

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document establishes the empirical baseline of LegalMitra's existing judicial corpus in compliance with Workstream C. All numbers reflect actual database entities, indexed documents, cryptographic SHA-256 hashes, and paragraph-level anchors rather than projected or unmeasured estimates.

Machine-readable baseline: `data/21_judicial_infrastructure/existing_caselaw_baseline.json`.

---

## 2. Empirical Corpus Baseline Metrics

| Metric Category | Count / Value | Verification Status |
| :--- | :---: | :--- |
| **Total Acquired Primary Judicial Documents** | **20** | Verified with SHA-256 & provenance URLs |
| **Unique Canonical Case Identities** | **20** | Disambiguated via `CaseIdentityResolver` |
| **Authenticity-Verified Documents** | **20 (100%)** | Validated against official reporters / eSCR |
| **Documents with Verified SHA-256 Hashes** | **20 (100%)** | 64-hex SHA-256 digests recorded |
| **Documents with Paragraph-Level Anchors** | **20 (100%)** | Exact paragraph numbers & token counts mapped |
| **Documents with Verified Parallel Citations** | **20 (100%)** | Neutral, SCC, SCR, AIR, ILR reconciled |
| **Documents Linked to Statutory Provisions** | **20 (100%)** | Substantive and procedural sections indexed |
| **Historical Pre-1950 Judicial Documents** | **2** | Federal Court (1942), Privy Council (1939) |
| **Regional-Language (Hindi) Documents** | **1** | Authentic Hindi eSCR Judgment (2022 INSC 690) |
| **Retrieval-Eligible Documents** | **20** | Approved for grounded RAG query synthesis |
| **Training-Eligible Documents** | **0** | **STRICT NO-GO** preserved under Phase 39 Gate |
| **Quarantined Synthetic Scaffold Chunks** | **6** | `IND-JUD-DEL-2024-BAIL` strictly isolated |

---

## 3. Institutional & Jurisdictional Distribution

| Court / Adjudicatory Body | Institutional Tier | Acquired Documents | Average OCR Quality |
| :--- | :--- | :---: | :---: |
| **Supreme Court of India (`IND-SC`)** | APEX | 7 | 0.993 |
| **High Court of Delhi (`IND-HC-DEL`)** | HIGH_COURT | 2 | 0.986 |
| **Bombay High Court (`IND-HC-BOM`)** | HIGH_COURT | 1 | 0.976 |
| **Allahabad High Court (`IND-HC-ALL`)** | HIGH_COURT | 1 | 0.968 |
| **Calcutta High Court (`IND-HC-CAL`)** | HIGH_COURT | 1 | 0.972 |
| **Madras High Court (`IND-HC-MAD`)** | HIGH_COURT | 1 | 0.979 |
| **National Company Law Appellate Tribunal (`IND-TR-NCLAT`)** | TRIBUNAL | 1 | 0.989 |
| **National Green Tribunal (`IND-TR-NGT`)** | TRIBUNAL | 1 | 0.984 |
| **Central Administrative Tribunal (`IND-TR-CAT`)** | TRIBUNAL | 1 | 0.978 |
| **Armed Forces Tribunal (`IND-MIL-AFT`)** | MILITARY_JUSTICE | 1 | 0.981 |
| **Federal Court of India (`HIST-FED-COURT`)** | HISTORICAL_ARCHIVE | 1 | 0.952 |
| **Privy Council (`HIST-PRIVY-COUNCIL`)** | HISTORICAL_ARCHIVE | 1 | 0.961 |
| **District Sessions Court (`IND-DIST-GENERIC`)** | DISTRICT_COURT | 1 | 0.945 |

---

## 4. Corpus Integrity Safeguards

1. **Separation of Statuses**: Registration, acquisition, parsing, authenticity verification, rights review, indexing, and retrieval eligibility are preserved as strictly independent lifecycle stages.
2. **Pretraining Quarantine**: No acquired judicial record is marked `is_training_eligible = True`. Pretraining gates remain locked.
