# LEGALMITRA PHASE 25: HISTORICAL VERSION & COMMENCEMENT AUDIT REPORT

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 25 — Independent Legal Authority Audit & Reliability Certification  
**Date:** October 2026  
**Status:** Audited & Verified  

---

## 1. Executive Summary

In Stage Two of Phase 25, an independent audit was performed on LegalMitra's temporal law engine (`legalmitra/temporal/engine.py`), amendment history manager (`legalmitra/corpus/amendments.py`), and historical provision version store.

The audit verified provision-level commencement mechanics, gazette notification boundaries, criminal-law transitions (IPC/CrPC/IEA to BNS/BNSS/BSA), and bitemporal applicability rules under Article 20(1) of the Constitution of India and Section 531 of the BNSS.

---

## 2. Temporal Boundaries & Commencement Verification

| Statute / Instrument | Commencement Instrument | Operational Date | Primary Temporal Finding |
| :--- | :--- | :--- | :--- |
| **Bharatiya Nyaya Sanhita, 2023** | MHA Notif. S.O. 849(E) | 2024-07-01 | All sections operative except Section 106(2) (hit-and-run enhanced penalty) deferred. Substantive offences prior to 2024-07-01 remain anchored to IPC pursuant to Article 20(1) protection against ex-post facto penal law. |
| **Bharatiya Nagarik Suraksha Sanhita, 2023** | MHA Notif. S.O. 850(E) | 2024-07-01 | Operative 2024-07-01. Section 531(2)(a) explicitly saves pending trials, appeals, inquiries, and investigations instituted prior to July 1, 2024, continuing under CrPC 1973. |
| **Bharatiya Sakshya Adhiniyam, 2023** | MHA Notif. S.O. 848(E) | 2024-07-01 | Section 170 saves prior applications/proceedings. Electronic certificate under Section 63(4) mirrors Section 65B(4) IEA (*Arjun Khotkar* binding standard). |
| **Specific Relief (Amendment) Act, 2018** | Law Min. Notif. S.O. 4888(E) | 2018-10-01 | Pre-2018 contracts governed by discretionary specific performance (*Version 1*); post-2018 contracts governed by mandatory specific performance (*Version 2*). |
| **Arbitration & Conciliation (Amendment) Act, 2015** | Act No. 3 of 2016 | 2015-10-23 | Section 29A mandatory 12-month award timeline operative post-2015; does not exist in pre-2015 arbitrations. |
| **Consumer Protection Act, 2019** | Notif. S.O. 2398(E) | 2020-07-20 | Replaced 1986 Act; statutory product liability and CCPA regulator active for post-2020 causes of action. |

---

## 3. Provision-Level Version Query Audit

The bitemporal query function `engine.query_provision_at_date(provision_id, target_date)` was tested across historical boundaries:
- `SRA-SEC-10` at `2015-05-01`: Returns Version 1 ("discretion of the court").
- `SRA-SEC-10` at `2022-05-01`: Returns Version 2 ("specific performance... shall be enforced").
- `ARB-SEC-29A` at `2014-01-01`: Correctly returns `None` (provision not yet enacted).
- `ARB-SEC-29A` at `2020-01-01`: Correctly returns Version 1 ("twelve months from completion of pleadings").
- `CONST-ART-330A` at `2022-01-01`: Correctly returns `None` (Constitution 106th Amendment not yet enacted).
- `CONST-ART-330A` at `2024-01-01`: Correctly returns Version 1 (women's reservation in Lok Sabha).

---

## 4. Criminal Law Transition Integrity

The engine's `resolve_criminal_law_regime(offence_date, proceedings_institute_date)` enforces three immutable legal rules:
1. **Offence Date Governs Substantive Law**: If `offence_date < 2024-07-01`, substantive law is IPC 1860; if `>= 2024-07-01`, substantive law is BNS 2023.
2. **Institution Date Governs Procedure**: If proceedings instituted prior to `2024-07-01`, Section 531(2)(a) BNSS mandates CrPC 1973 applies.
3. **Historic Judgments Attribution**: Historical precedents (e.g. *Rangappa*, *Sibbia*, *Jacob Mathew*, *Arnesh Kumar*) interpreted IPC and CrPC provisions. The system explicitly records the original provision interpreted and links the modern successor as a related entity rather than retroactively rewriting judicial quotations.
