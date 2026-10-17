# LEGALMITRA — PHASE 16C: DELEGATED LEGISLATION & COMMENCEMENT NOTIFICATIONS REPORT

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

In Phase 16C, subordinate legislation and statutory commencement instruments were formally integrated into LegalMitra's authoritative knowledge base. Subordinate rules and commencement notifications possess statutory force under their enabling central Acts and are essential for resolving temporal applicability and compliance questions.

8 subordinate legal instruments (3 core rules/regulations and 5 official commencement notifications) were ingested, registered, and indexed into `data/legalmitra_kb.db`.

---

## 2. Ingested Subordinate Instruments

| Document ID | Official Title | Enabling Parent Statute | Gazette / S.O. Citation | Chunks Indexed | Extraction Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `IND-RULE-IT-SPDI-2011` | Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 | IT Act 2000 (s.43A & s.87(2)(ob)) | G.S.R. 313(E) | 4 | `partially_extracted` |
| `IND-RULE-IT-INTERMEDIARY-2021` | Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 | IT Act 2000 (s.79 & s.87(2)(z)/(zg)) | G.S.R. 139(E) | 2 | `partially_extracted` |
| `IND-RULE-CPA-ECOMMERCE-2020` | Consumer Protection (E-Commerce) Rules, 2020 | CPA 2019 (s.94 & s.101(2)(zg)) | G.S.R. 462(E) | 2 | `partially_extracted` |
| `IND-NOTIF-COMMENCE-BNSS-2024` | Commencement Notification for BNSS 2023 | BNSS 2023 (s.1(3)) | S.O. 848(E) | 1 | `fully_extracted` |
| `IND-NOTIF-COMMENCE-BNS-2024` | Commencement Notification for BNS 2023 | BNS 2023 (s.1(2)) | S.O. 849(E) | 1 | `fully_extracted` |
| `IND-NOTIF-COMMENCE-BSA-2024` | Commencement Notification for BSA 2023 | BSA 2023 (s.1(3)) | S.O. 850(E) | 1 | `fully_extracted` |
| `IND-NOTIF-COMMENCE-SRA-2018` | Commencement Notification for Specific Relief (Amendment) Act, 2018 | SRA Amendment 2018 (s.1(2)) | S.O. 4888(E) | 1 | `fully_extracted` |
| `IND-NOTIF-COMMENCE-CPA-2020` | Commencement Notification for Consumer Protection Act, 2019 | CPA 2019 (s.1(3)) | S.O. 2351(E) | 1 | `fully_extracted` |
| **TOTAL** | **8 Subordinate Instruments** | — | — | **13** | — |

---

## 3. Substantive Legal Scope & Enforceability

1. **Information Technology SPDI Rules 2011**:
   - Ingests Rule 3 (exhaustive 8-category definition of Sensitive Personal Data or Information including passwords, biometrics, financial and health data).
   - Ingests Rule 4 (mandatory privacy policy publication on body corporate website).
   - Ingests Rule 5 (prior consent standard and lawful purpose limitation).
   - Ingests Rule 8 (compliance through IS/ISO/IEC 27001 standard certification).

2. **IT Intermediary Rules 2021**:
   - Ingests Rule 3 (due diligence, user agreements, and mandatory 36-hour takedown standard post-judicial order or government notice).
   - Ingests Rule 4 (additional due diligence for significant social media intermediaries: Chief Compliance Officer, Nodal Officer, Resident Grievance Officer, and first originator identification under lawful orders).

3. **Consumer Protection E-Commerce Rules 2020**:
   - Ingests Rule 4 (mandatory duties of e-commerce entities, registered corporate structure, 48-hour complaint acknowledgment, 1-month dispute redressal).
   - Ingests Rule 5 (marketplace liabilities, prohibition on manipulative listings and discrimination among sellers).

4. **Commencement Dates Established**:
   - New Criminal Laws (`BNS`, `BNSS`, `BSA`): Came into legal effect on **1st July, 2024** (with s.106(2) BNS hit-and-run held in abeyance).
   - Specific Relief Amendment 2018: Commenced **1st October, 2018**.
   - Consumer Protection Act 2019: Commenced **20th July, 2020**.

---

## 4. Manifest Export & Verification

- Delegated legislation records exported to: `data/08_corpus/delegated_legislation.json`.
- Total Knowledge Base sources increased to **26**.
- Total active legal chunks increased to **1,316**.

