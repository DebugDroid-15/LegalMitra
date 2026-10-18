# Phase 37 National Legal Acquisition Results

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

Phase 37 expanded LegalMitra's national legal corpus across primary statutes, delegated legislation, court procedural rules, and high court precedents. Ten discovery candidates cataloged in Phase 35/36 were physically acquired, processed through the `BilingualLegalPipeline`, cryptographically verified, and promoted to `TRAINING_ELIGIBLE` status.

The acquisition added **74 verified passages** and **14,393 tokens** to the pretraining corpus, with zero duplicate leakage and 100% Section 52(1)(q) copyright compliance.

---

## 2. Inventory of Acquired National Sources

| Source Identifier | Official Title | Jurisdiction | Language | Category | Acquired Provisions | Token Yield |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IND-STAT-BNS-2023-HI` | भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita) | IN (Central) | Hindi | Penal Substantive | 33 | 6,342 |
| `IND-STAT-BNSS-2023-HI` | भारतीय नागरिक सुरक्षा संहिता, 2023 (BNSS) | IN (Central) | Hindi | Criminal Procedure | 16 | 3,118 |
| `IND-STAT-BSA-2023-HI` | भारतीय साक्ष्य अधिनियम, 2023 (BSA) | IN (Central) | Hindi | Evidence Law | 12 | 1,794 |
| `IND-GAZ-COMMENCE-BNS-2024` | Notification S.O. 850(E) - BNS Commencement | IN (Central) | English | Gazette Notification | 1 | 96 |
| `IND-GAZ-COMMENCE-BNSS-2024`| Notification S.O. 849(E) - BNSS Commencement | IN (Central) | English | Gazette Notification | 1 | 89 |
| `IND-GAZ-COMMENCE-BSA-2024` | Notification S.O. 851(E) - BSA Commencement | IN (Central) | English | Gazette Notification | 1 | 91 |
| `IND-RULE-IT-INTERMEDIARY-2021` | IT (Intermediary Guidelines & Digital Ethics) Rules 2021 | IN (Central) | English | Delegated Rule | 2 | 496 |
| `IND-WB-STAT-WBLR-1955` | West Bengal Land Reforms Act, 1955 | IN-WB (State) | English | Land & Tenancy | 2 | 268 |
| `IND-TN-STAT-TNTT-1998` | Tamil Nadu Transparency in Tenders Act, 1998 | IN-TN (State) | English | Public Procurement | 2 | 312 |
| `IND-DEL-RULE-DHC-ORIG-2018` | Delhi High Court (Original Side) Rules, 2018 | IN-DL (Court) | English | Civil Procedure | 2 | 314 |
| `IND-JUD-BHC-2024-VODAFONE` | Vodafone Idea Ltd v. UOI (Bombay High Court) | IN-MH (Judicial) | English | Tax & Telecom | 1 | 682 |
| `IND-JUD-CAL-2023-GREENEARTH`| Green Earth Foundation v. State of WB (Calcutta HC) | IN-WB (Judicial) | English | Environmental Law | 1 | 791 |
| **Total Acquired Phase 37** | — | — | — | — | **74** | **14,393** |

---

## 3. Promotion & FSM State Machine Progression

All newly acquired sources successfully traversed the Finite State Machine transitions enforced by `UnifiedSourceRegistry` (`legalmitra/corpus/source_registry_engine.py`):

```
DISCOVERED
   |  (Metadata validated in national registry)
   v
REGISTERED
   |  (Document retrieved from official Gazette / certified portal)
   v
ACQUIRED
   |  (Parsed into structured provisions by LegalDocumentParser)
   v
PARSED
   |  (Zero replacement chars \ufffd, dandas verified, SHA256 hashed)
   v
AUTHENTICITY_VERIFIED
   |  (Checked against Section 52(1)(q); no commercial commentary)
   v
RIGHTS_REVIEWED
   |  (Promoted to pretraining corpus)
   v
TRAINING_ELIGIBLE
```

No invalid transition or illegal FSM jump occurred. All 12 source units stand at state `TRAINING_ELIGIBLE` with evidence completeness scores of **1.0**.

---

## 4. Corpus Growth Metrics

| Metric | Phase 36 Baseline | Phase 37 Expansion | Net Change | Growth % |
| :--- | :--- | :--- | :--- | :--- |
| **Total Pretraining Passages** | 1,559 | 1,633 | +74 | +4.75% |
| **Total Pretraining Tokens** | 342,965 | 357,358 | +14,393 | +4.20% |
| **Authentic Hindi Tokens** | 8,617 | 19,871 | +11,254 | **+130.6%** |
| **English Legal Tokens** | 334,348 | 337,487 | +3,139 | +0.94% |
| **Training Eligible Sources** | 33 | 47 | +14 | +42.4% |
| **Jurisdictions Covered** | Central, MH, KA, TN | Central, MH, KA, TN, WB, DL | +2 | +50.0% |

