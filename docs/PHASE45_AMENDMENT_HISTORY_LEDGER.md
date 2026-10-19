# LEGALMITRA — PHASE 45 AMENDMENT HISTORY LEDGER
## Comprehensive Event Reconstruction, Provision-Level Mutations & Legal Effect Analysis

**Audit Date:** 2026-10-19T11:57:15+05:30  
**Target Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Auditor:** Shatrujeet Audit & Infrastructure Engineering Team  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

### 1. Executive Summary

Phase 45 engineered an immutable, machine-readable amendment ledger (`data/22_central_legislation/amendment_event_ledger.json`) tracking the statutory lifecycle and text mutations across key Central Acts.

In legal retrieval, an amendment event cannot be modeled merely as text replacement. Each legislative event represents a distinct jurisprudential transition:
- **`SUBSTITUTION`**: Replaces the text of a provision while maintaining continuity of numbering.
- **`INSERTION`**: Adds an entirely new section, subsection, proviso, or explanation.
- **`OMISSION`**: Deletes a provision from the statute book.
- **`REPEAL_WITH_SAVINGS`**: Extinguishes the parent enactment while establishing a statutory bridge (savings clause) preserving pending proceedings or vested rights.
- **`OMISSION_PENDING_COMMENCEMENT`**: An enacted legislative amendment where the operative provision has not yet been appointed for commencement under a phased commencement clause.

---

### 2. Structured Event Ledger Summary

| Event ID | Parent Act | Amending Instrument | Effective Date | Affected Provision | Mutation Type | Legal Consequence |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| `AMEND-EVT-SRA-2018-SEC10` | SRA 1963 | Act 18 of 2018 (S.O. 4888(E)) | 2018-10-01 | Section 10 | `SUBSTITUTION` | Discretionary relief replaced by mandatory specific performance rule. |
| `AMEND-EVT-SRA-2018-SEC20A` | SRA 1963 | Act 18 of 2018 (S.O. 4888(E)) | 2018-10-01 | Section 20A | `INSERTION` | Statutory bar prohibiting injunctions in infrastructure projects. |
| `AMEND-EVT-ARB-2015-SEC34` | ARB 1996 | Act 3 of 2016 (Ord. 9/2015) | 2015-10-23 | Section 34(2A) | `INSERTION` | Restricts patent illegality challenge to domestic awards; bars merits review. |
| `AMEND-EVT-ARB-2015-SEC29A` | ARB 1996 | Act 3 of 2016 | 2015-10-23 | Section 29A | `INSERTION` | 12-month statutory deadline for making arbitral awards. |
| `AMEND-EVT-IT-2008-SEC43A` | IT Act 2000 | Act 10 of 2009 (S.O. 2689(E)) | 2009-10-27 | Section 43A | `INSERTION` | Compensation liability for corporate negligence regarding sensitive data. |
| `AMEND-EVT-DPDP-2023-SEC44` | IT Act 2000 | DPDP Act 2023 (Act 22/2023) | *Unappointed* | Section 43A | `OMISSION_PENDING` | Section 44(2) omits IT s.43A, but remains uncommenced under s.1(2). |
| `AMEND-EVT-BNSS-2023-REPEAL`| CrPC 1973 | BNSS 2023 (S.O. 848(E)) | 2024-07-01 | Whole Act | `REPEAL_SAVINGS` | Repeals CrPC; s.531(2)(a) saves pending pre-01.07.2024 proceedings. |
| `AMEND-EVT-BNS-2023-REPEAL` | IPC 1860 | BNS 2023 (S.O. 849(E)) | 2024-07-01 | Whole Act | `REPEAL_SAVINGS` | Repeals IPC; s.358(2) & Art. 20(1) save pre-01.07.2024 offenses. |
| `AMEND-EVT-BSA-2023-REPEAL` | IEA 1872 | BSA 2023 (S.O. 850(E)) | 2024-07-01 | Whole Act | `REPEAL_SAVINGS` | Repeals IEA; s.170(2) saves pre-01.07.2024 evidence proceedings. |
| `AMEND-EVT-CPA-2019-REPEAL` | CPA 1986 | CPA 2019 (S.O. 2351(E)) | 2020-07-20 | Whole Act | `REPEAL_SAVINGS` | Repeals CPA 1986; s.107(2) saves pending consumer complaints. |
| `AMEND-EVT-CONST-106TH` | Constitution | 106th Amendment (Act 23/2023) | 2023-09-28 | Article 330A | `INSERTION` | Women's reservation (1/3rd seats) in House of the People. |
| `AMEND-EVT-CONST-103RD` | Constitution | 103rd Amendment (Act 1/2019) | 2019-01-14 | Arts. 15(6), 16(6) | `INSERTION` | Up to 10% affirmative action reservation for EWS. |

---

### 3. Evidentiary Audit of Amendment Lineage

Every event recorded in the ledger was cross-verified against three independent primary artifacts:
1. **The Amending Act text** in the Gazette of India Extraordinary Part II Section 1.
2. **The Commencement Notification** issued by the administrative ministry in the Gazette of India Extraordinary Part II Section 3(ii).
3. **The India Code Consolidated Record** validating that footnotes and historical antecedents accurately reflect the Gazette terms.

Zero inferred or synthetic amendment dates were entered into the ledger.
