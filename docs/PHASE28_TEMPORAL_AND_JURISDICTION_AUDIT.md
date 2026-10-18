# Phase 28: Temporal and Jurisdictional Integrity Audit Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 28  

---

## 1. Executive Summary

This report establishes the temporal and jurisdictional auditing architecture of LegalMitra Phase 28. It details the corrections made to inaccurate statutory commencement dates, the verification of transitional savings regimes, and the jurisdictional boundary enforcement between Central, State, and High Court materials.

---

## 2. Audited Temporal Data Model

The LegalMitra temporal engine distinguishes 8 distinct temporal timestamps rather than treating document publication as commencement:
1. **Document Date:** Date on which the instrument was signed, gazetted, or pronounced.
2. **Assent Date:** Date of Presidential or Gubernatorial assent.
3. **Commencement Date:** Date appointed by Central/State Government notification for provisions to come into force.
4. **Amendment Date:** Date on which an amending Act altered the provision.
5. **Repeal / Substitution Date:** Date on which a provision ceased to be operative.
6. **Date of Offence / Fact Accrual:** Material date determining substantive criminal/civil liability under Article 20(1).
7. **Date of Proceeding Institution:** Procedural date governing forum jurisdiction and procedural savings under BNSS Section 531.
8. **As-Of Query Date:** Temporal anchor supplied in user query or search filter.

---

## 3. Statutory Commencement Date Corrections

| Source ID | Act Title | Erroneous Date in KB | Authoritative Commencement Date | Statutory Citation / Gazette Instrument |
|---|---|---|---|---|
| `IND-ACT-1988-MVA` | The Motor Vehicles Act, 1988 | `2005-10-12` | **1989-07-01** | Gazette of India S.O. 368(E), dt. 22-05-1989 |
| `IND-ACT-2012-POCSO` | POCSO Act, 2012 | `2005-10-12` | **2012-11-14** | Gazette of India S.O. 2725(E), dt. 13-11-2012 |
| `IND-STAT-POCSO-2012-SEC4` | POCSO Act Section 4 | `2012-06-19` | **2012-11-14** | Gazette of India S.O. 2725(E), dt. 13-11-2012 |
| `IND-STAT-IT-2000` (Sec 43A, 66A-F) | IT Amendment Act, 2008 Provisions | `2000-10-17` | **2009-10-27** | Gazette of India S.O. 2689(E), dt. 27-10-2009 |
| `IND-STAT-DPDP-2023` | Digital Personal Data Protection Act, 2023 | `2023-08-11` | **Phased Commencement** | Section 1(2) DPDP Act; penalty provisions unnotified |

---

## 4. Transitional Scenarios & Savings Rules Audited

### A. IPC vs BNS Transitional Boundary (1 July 2024)
- **Substantive Rule:** Under Article 20(1) of the Constitution and Section 531 of the Bharatiya Nagarik Suraksha Sanhita (BNSS), any offence committed prior to 1 July 2024 remains punishable exclusively under the Indian Penal Code, 1860.
- **Verification:** Verified in `EVAL-TEMP-001` and `test_pilot_20.py::test_bnss_section_531_anti_conflation_regression`.

### B. Hit-and-Run Section 106(2) BNS Enforcement Deferral
- **Statutory Status:** Ministry of Home Affairs Notification S.O. 849(E) expressly deferred the commencement of sub-section (2) of Section 106 BNS. It is not currently operative.
- **Verification:** Verified in `EVAL-TEMP-003`.

### C. Specific Relief Act 2018 Amendment
- **Mandatory Specific Performance:** Prior to 1 October 2018, Section 10 was discretionary. Following the Specific Relief (Amendment) Act, 2018 (commenced 1 October 2018 via S.O. 4888(E)), specific performance is mandatory subject to Sections 11(2), 14, and 16.
- **Verification:** Verified in `EVAL-P28-STAT-002`.

---

## 5. Jurisdictional Boundary Enforcement

The system maintains strict jurisdictional separation:
- **Central Laws:** Jurisdiction `IN`, binding across all Indian states.
- **State Laws:** Jurisdiction `IN-DL` (Delhi Police Act, Delhi Rent Control), `IN-MH` (Maharashtra Police Act, Maharashtra Rent Control). When unindexed states (Nagaland, Mizoram, Meghalaya, Haryana) are queried, the engine refuses cross-jurisdictional substitution and cleanly abstains (`EVAL-P28-MISS-001`, `EVAL-P28-MISS-002`).
- **Supreme Court of India:** Binding under Article 141 across all courts.
- **High Court Authorities:** Persuasive outside territory, binding within jurisdiction.
