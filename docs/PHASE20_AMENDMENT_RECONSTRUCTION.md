# PHASE 20 — AMENDMENT RECONSTRUCTION, COMMENCEMENT & HISTORICAL VERSIONING
## Modeling Statutory Evolution, Gazette Commencement, and Criminal Law Transition

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

Indian legislation evolves dynamically through amending Acts, Gazette notifications, and major code recodifications. Applying the correct historical version of a statutory provision at the precise date of cause of action or offence is a non-negotiable legal requirement under Article 20(1) of the Constitution (protection against retrospective penal laws).

Phase 20 audits LegalMitra's amendment reconstruction engine, commencement tracking, and transitional mapping between pre-2024 and post-2024 criminal frameworks.

---

## 2. Amendment Reconstruction Architecture

LegalMitra implements structural diffing and version reconstruction in `legalmitra/corpus/legal_diff.py` and `legalmitra/corpus/version_manager.py`:
- **Change Types**: Categorizes statutory mutations into substantive shifts (e.g., substitution of limitation periods, alteration of penalties, insertion of provisos) versus typographical or editorial corrigenda.
- **Bi-Temporal Validity**: Every statutory section and chunk records:
  1. `enactment_date`: Date of presidential or gubernatorial assent.
  2. `effective_date`: Date appointed by Gazette commencement notification.
  3. `repeal_date`: Date replaced, superseded, or sunsetted.
- **Historical Reconstruction**: Retrieves the exact statutory text in force on any arbitrary date $T_{\text{query}}$.

---

## 3. Commencement Events & Gazette Intelligence

In Indian statutory practice, an Act passed by Parliament does not automatically take effect upon assent unless an appointed-day clause operates immediately. Most complex enactments empower the Central Government to notify commencement via official Gazette (*The Gazette of India* published by the Directorate of Printing, Ministry of Housing and Urban Affairs).

Key commencement events modeled in LegalMitra:

| Enactment | Assent Date | Commencement Date | Gazette S.O. Notification | Provisions Brought into Force |
| :--- | :--- | :--- | :--- | :--- |
| **Bharatiya Nyaya Sanhita, 2023** | 2023-12-25 | 2024-07-01 | S.O. 850(E) | Full Act except Section 106(2) (hit-and-run pending consultation) |
| **Bharatiya Nagarik Suraksha Sanhita, 2023** | 2023-12-25 | 2024-07-01 | S.O. 851(E) | Complete procedural code replacing CrPC 1973 |
| **Bharatiya Sakshya Adhiniyam, 2023** | 2023-12-25 | 2024-07-01 | S.O. 852(E) | Evidentiary code replacing IEA 1872 |
| **Consumer Protection Act, 2019** | 2019-08-09 | 2020-07-20 | S.O. 2351(E) | Substantive provisions, CCPA, and Dispute Redressal Commissions |
| **Commercial Courts Act, 2015** | 2015-12-31 | 2015-10-23 | Retrospective Ordinance effect | Section 12A inserted via Act 28 of 2018 (commenced 2018-05-03) |
| **Negotiable Instruments (Amendment) Act, 2018**| 2018-08-02 | 2018-09-01 | S.O. 3965(E) | Inserted Section 143A (interim compensation) and 148 (appellate deposit) |

---

## 4. Transitional Law Audit: Criminal Code Migration

The transition from the Indian Penal Code, 1860 (IPC) to the Bharatiya Nyaya Sanhita, 2023 (BNS) represents the most extensive statutory overhaul in post-independence India.

LegalMitra's transitional legal model ensures:
1. **Temporal Segregation**:
   - Offences committed on or before **June 30, 2024**: Governed substantively by IPC 1860 and procedurally by CrPC 1973.
   - Offences committed on or after **July 1, 2024**: Governed substantively by BNS 2023 and procedurally by BNSS 2023.
2. **Repeal & Savings Clause (BNS Section 358)**:
   - Preserves pending investigations, trials, and legal liabilities incurred under the repealed IPC.
3. **Cross-Code Equivalency Mapping**:
   - `IPC s.302 (Murder)` $\rightarrow$ `BNS s.103`
   - `IPC s.378/379 (Theft)` $\rightarrow$ `BNS s.303`
   - `IPC s.420 (Cheating)` $\rightarrow$ `BNS s.318`
   - `IPC s.124A (Sedition - stayed)` $\rightarrow$ `BNS s.152 (Acts endangering sovereignty, unity, and integrity of India)`
   - `IPC s.304A (Negligent death)` $\rightarrow$ `BNS s.106(1)`

---

## 5. Verification & Retrieval Assurance

- **Temporal Query Filter**: LegalMitra queries automatically check `target_date` against `effective_date <= target_date < repeal_date`.
- **Zero Hallucination Guarantee**: When a user queries a 2022 offence date, LegalMitra cites IPC provisions and highlights non-applicability of BNS, preventing temporal legal errors.

