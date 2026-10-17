# LEGALMITRA — PHASE 16E: STATE-LEVEL LAW BATCH INGESTION REPORT (DELHI & MAHARASHTRA)

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

Under the Constitution of India (Seventh Schedule, List II), key subjects such as Police (Entry 2) and Rent Control / Housing are exclusively within State legislative competence. 

In Phase 16E, LegalMitra completed its first operational expansion into State-level statutory jurisprudence by ingesting foundational civil and criminal statutes for:
1. **National Capital Territory of Delhi (`IN-DL`)**
2. **State of Maharashtra (`IN-MH`)**

A total of 4 landmark state Acts across 15 authoritative sections were parsed, registered, and indexed into `data/legalmitra_kb.db`.

---

## 2. Ingested State Legislation Summary

| Jurisdiction | Act ID | Short Title | Act Number | Enactment Date | Chunks | Key Provisions Ingested |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IN-DL` | `IND-DL-STAT-DRC-1958` | The Delhi Rent Control Act, 1958 | Act No. 59 of 1958 | 1958-12-31 | 4 | Sec 2 (Definitions: Landlord, Tenant), Sec 3 (Exemption threshold of Rs 3,500/month), Sec 14 (Protection against eviction, arrears, bona fide requirement), Sec 25B (Summary procedure, leave to defend) |
| `IN-DL` | `IND-DL-STAT-DPA-1978` | The Delhi Police Act, 1978 | Act No. 34 of 1978 | 1978-08-27 | 3 | Sec 28 (Traffic regulations, public amusement & music licensing), Sec 53 (Externment of repeat offenders), Sec 65 (Duty to comply with police directions) |
| `IN-MH` | `IND-MH-STAT-MRC-1999` | The Maharashtra Rent Control Act, 1999 | Mah. Act No. XVIII of 2000 | 2000-03-10 | 5 | Sec 3 (Exemption for PSUs, corporations with paid-up capital >= Rs 1 Cr), Sec 7 (Definitions: Licensee, standard rent), Sec 15 (No ejectment if standard rent paid, 90-day statutory notice), Sec 16 (Bona fide requirement & demolition grounds), Sec 24 (Summary eviction of residential licensees & double fee penalty) |
| `IN-MH` | `IND-MH-STAT-MPA-1951` | The Maharashtra Police Act, 1951 | Bombay Act No. XXII of 1951 | 1951-06-11 | 3 | Sec 33 (Traffic and public order regulation), Sec 56 (Removal of persons about to commit violence/offences), Sec 57 (Externment of convicted offenders) |
| **TOTAL** | **2 States / UTs** | **4 State Acts** | — | — | **15** | — |

---

## 3. Substantive Cross-State Legal Comparison & Conflict Analysis

1. **Rent Control Exemption Thresholds**:
   - **Delhi (`IN-DL`)**: Under Section 3(c) of DRC Act 1958, premises having monthly rent exceeding **₹3,500** are exempt from rent control and governed by general Transfer of Property Act principles.
   - **Maharashtra (`IN-MH`)**: Under Section 3(1)(b) of MRC Act 1999, exemption is entity-based rather than rental amount based: premises let to banks, PSUs, multinational corporations, and companies with paid-up capital of **₹1 Crore or more** are exempt.

2. **Leave to Defend vs Standard Civil Trial**:
   - **Delhi (`IN-DL`)**: Section 25B mandates a strict summary procedure for bona fide requirement (Sec 14(1)(e)) where the tenant has no automatic right to defend without obtaining leave from the Rent Controller upon showing triable issues.
   - **Maharashtra (`IN-MH`)**: Section 24 provides a streamlined procedure before the Competent Authority specifically for leave and licence residential agreements, imposing double licence fees for overstaying.

3. **Police Externment Powers**:
   - **Delhi (`IN-DL`)**: Section 53 empowers the Commissioner of Police to extern repeat offenders convicted of Chapters XII, XVI, or XVII offences.
   - **Maharashtra (`IN-MH`)**: Section 56 and Section 57 empower the Commissioner or District Magistrate to remove persons causing alarm, danger, or about to engage in violent offences.

---

## 4. Verification & Artifacts

- State law batch report generated: `data/08_corpus/state_law_batch_report.json`.
- Total Knowledge Base sources increased to **30**.
- Knowledge base now accurately partitions chunks across Central (`IN`), Delhi (`IN-DL`), and Maharashtra (`IN-MH`).

