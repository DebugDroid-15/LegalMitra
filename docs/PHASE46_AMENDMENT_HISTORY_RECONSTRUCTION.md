# LEGALMITRA — PHASE 46
## Gazette-Verified Amendment History Reconstruction Report (Batch 2)

**Project:** LegalMitra  
**Document ID:** `LM-P46-REP-006-AMENDMENT-RECONSTRUCTION`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** 2026-10-19  
**Status:** COMPLETE & GAZETTE-VERIFIED

---

### 1. Executive Summary

Workstream E reconstructs the official amendment histories for Central Legislation Batch 2 directly from Parliamentary Amendment Acts and Extraordinary Gazette of India commencement notifications.

In compliance with project standards:
- **No Inferred Dates**: Commencement dates are never assumed from enactment or Presidential assent dates.
- **Section-Wise Phased Enforcement**: Provisions are tracked with their distinct operational appointment dates.
- **Zero Historical Erasure**: Prior statutory texts are preserved in their respective $[t_{\text{start}}, t_{\text{end}})$ validity intervals.

---

### 2. Comprehensive Batch 2 Amendment Events

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                          BATCH 2 AMENDMENT EVENT LEDGER                                              |
+--------------------------+--------------------+---------------------+------------+--------------+--------------------+
| Event Identifier         | Target Act         | Amending Act        | Eff. Date  | Gazette Ref. | Legal Effect       |
+--------------------------+--------------------+---------------------+------------+--------------+--------------------+
| AMEND-EVT-COMP-2020-S135 | IND-STAT-COMP-2013 | Act No. 29 of 2020  | 2021-01-22 | S.O. 325(E)  | Decriminalized CSR |
| AMEND-EVT-IBC-2018-S29A  | IND-STAT-IBC-2016  | Act No. 8 of 2018   | 2017-11-23 | Ord. 7/2017  | Section 29A bar    |
| AMEND-EVT-IBC-2020-S32A  | IND-STAT-IBC-2016  | Act No. 1 of 2020   | 2019-12-28 | Ord. 16/2019 | Clean-slate immun. |
| AMEND-EVT-CONTRACT-1997  | IND-STAT-CONT-1872 | Act No. 1 of 1997   | 1997-01-08 | Act 1 of 1997| Section 28 clause b|
| AMEND-EVT-TPA-2001-S53A  | IND-STAT-TPA-1882  | Act No. 48 of 2001  | 2001-09-24 | Act 48/2001  | Mandatory reg. 53A |
| AMEND-EVT-CPC-2015-O8R1  | IND-STAT-CPC-1908  | Act No. 4 of 2016   | 2015-10-23 | Ord. 8/2015  | 120-day forfeiture |
| AMEND-EVT-MVA-2019-S164  | IND-STAT-MVA-1988  | Act No. 32 of 2019  | 2022-04-01 | S.O. 859(E)  | No-fault fixed comp|
| REPEAL-EVT-COMP-2013     | IND-STAT-COMP-1956 | Act No. 18 of 2013  | 2013-09-12 | S.O. 2754(E) | Repeal with savings|
+--------------------------+--------------------+---------------------+------------+--------------+--------------------+
```

---

### 3. Detailed Legal and Gazette Analysis

#### 1. Companies (Amendment) Act, 2020: Section 135 CSR Decriminalization
- **Pre-2020 Regime**: Section 135(5) required companies to state reasons for unspent amounts. Violations fell under general criminal default penalties (Section 450 fines up to INR 10,000 + per-day fines).
- **Post-2020 Regime**: Substituted Section 135(7) commenced on 22 January 2021 via MCA Notification S.O. 325(E), replacing penal fines with civil administrative penalties:
  - Company: Twice the unspent amount or INR 1 Crore, whichever is less.
  - Officer in Default: One-tenth of the unspent amount or INR 2 Lakhs, whichever is less.

#### 2. Insolvency and Bankruptcy Code (Amendment) Act, 2018: Section 29A Disqualification
- Promulgated initially via Insolvency and Bankruptcy Code (Amendment) Ordinance, 2017 on 23 November 2017, later enacted as Act 8 of 2018.
- Introduced strict eligibility criteria preventing wilful defaulters, undischarged insolvents, and promoters of companies with NPAs exceeding one year from submitting resolution plans (*ArcelorMittal India Pvt. Ltd. v. Satish Kumar Gupta* (2019) 2 SCC 1).

#### 3. Insolvency and Bankruptcy Code (Amendment) Act, 2020: Section 32A Clean Slate
- Inserted by Ordinance on 28 December 2019, followed by Act 1 of 2020.
- Guarantees that corporate debtors shall not be prosecuted for offences committed prior to the commencement of the CIRP once the resolution plan is approved by the Adjudicating Authority (NCLT) and control is transferred to an unrelated resolution applicant (*Ghanshyam Mishra & Sons v. Edelweiss Asset Reconstruction* (2021) 9 SCC 657).

#### 4. Indian Contract (Amendment) Act, 1997: Section 28 Substitution
- Published in Gazette of India on 8 January 1997 (Act 1 of 1997).
- Overruled the rule laid down in *Vulcan Insurance Co. Ltd. v. Maharaj Singh* (1976) 1 SCC 943 and *Food Corporation of India v. New India Assurance Co. Ltd.* (1994) 3 SCC 324, declaring void any contractual term that extinguishes the rights of a party or discharges a party from liability on the expiry of a specified period (*Union of India v. Indusind Bank Ltd.* (2016) 9 SCC 720).

#### 5. Registration and Other Related Laws (Amendment) Act, 2001: Section 53A Part Performance
- Enacted on 24 September 2001 (Act 48 of 2001).
- Concurrently amended Section 17 of the Registration Act, 1908 (inserting sub-section (1A)) and Section 53A of the Transfer of Property Act, 1882.
- An unregistered contract for sale executed on or after 24 September 2001 **cannot** be utilized as an equitable shield to protect possession against the transferor.

#### 6. Commercial Courts Act, 2015: CPC Order VIII Rule 1
- Commenced on 23 October 2015 (Act 4 of 2016).
- In Commercial Disputes, the court has no power to condone delay beyond 120 days from the date of service of summons. On the expiry of 120 days, the right of the defendant to file the written statement stands permanently forfeited.

#### 7. Motor Vehicles (Amendment) Act, 2019: Section 163A to Section 164
- While Act 32 of 2019 received assent on 9 August 2019, Section 51 (substituting Chapter XI and Sections 163A/164) was formally appointed only on **1 April 2022** via Ministry of Road Transport and Highways Notification S.O. 859(E) dated 25 February 2022.
- A claim for an accident occurring prior to 1 April 2022 was governed by Section 163A and the Second Schedule formula. Accidents occurring on or after 1 April 2022 are governed by Section 164.
