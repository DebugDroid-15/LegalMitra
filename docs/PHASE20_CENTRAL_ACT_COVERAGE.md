# PHASE 20 — CENTRAL ACTS COMPREHENSIVE COVERAGE
## Ingestion of Negotiable Instruments Act, Transfer of Property Act & Commercial Courts Act

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

Phase 20 expands LegalMitra's statutory knowledge base by ingesting three critical commercial, civil, and banking enactments of the Indian Parliament:
1. **The Negotiable Instruments Act, 1881** (`IND-STAT-NI-1881`): Sections 138 to 142 (Cheque Dishonour jurisprudence).
2. **The Transfer of Property Act, 1882** (`IND-STAT-TPA-1882`): Sections 53A, 54, 58, 105, 106 (Conveyance, Mortgages, and Leases).
3. **The Commercial Courts Act, 2015** (`IND-STAT-COMM-COURTS-2015`): Sections 2(1)(c), 6, 12A, 16 (Commercial dispute definitions, Pre-institution mediation, CPC modifications).

With these additions, LegalMitra now indexes **11 comprehensive Central Acts** comprising **184 active statutory chunks** in `data/legalmitra_kb.db`.

---

## 2. Ingested Central Acts Breakdown

| Source ID | Act Title | Act No. / Year | Ingested Sections | Indexed Chunks |
| :--- | :--- | :--- | :--- | :--- |
| `IND-CONST-1950` | The Constitution of India | 1950 | Preamble, Arts 12-16, 19-22, 25, 32, 38, 39A, 44, 51A, 124, 136, 141, 142, 214, 226, 227, 300A, 330A, 352, 356, 368 | 41 |
| `IND-STAT-BNS-2023` | The Bharatiya Nyaya Sanhita, 2023 | Act 45 of 2023 | Secs 1, 4, 14, 20, 22, 34, 35, 63, 100, 103, 109, 115, 117, 152, 303, 316, 358 | 28 |
| `IND-STAT-CPC-1908` | The Code of Civil Procedure, 1908 | Act 5 of 1908 | Secs 9, 10, 11, 15, 16, 20, 96, 100, 114, 115; O. VII R. 11, O. XXXIX R. 1-2 | 20 |
| `IND-STAT-LIMIT-1963` | The Limitation Act, 1963 | Act 36 of 1963 | Secs 3, 4, 5, 6, 17, 19; Sched Arts 54, 65, 137 | 14 |
| `IND-STAT-ICA-1872` | The Indian Contract Act, 1872 | Act 9 of 1872 | Secs 2, 10, 11, 13, 14, 15, 16, 17, 18, 23, 25, 73, 74, 124, 126, 148, 182 | 21 |
| `IND-STAT-SRA-1963` | The Specific Relief Act, 1963 | Act 47 of 1963 | Secs 5, 6, 10, 14, 16, 20, 34, 38; Schedule | 13 |
| `IND-STAT-ARB-1996` | The Arbitration & Conciliation Act, 1996 | Act 26 of 1996 | Secs 7, 8, 9, 11, 12, 16, 17, 31, 34, 36, 37; 7th Sched | 13 |
| `IND-STAT-CPA-2019` | The Consumer Protection Act, 2019 | Act 35 of 2019 | Secs 2, 10, 18, 21, 35, 38, 47, 58, 83, 86, 87, 107 | 14 |
| `IND-STAT-NI-1881` | The Negotiable Instruments Act, 1881 | Act 26 of 1881 | Secs 138, 139, 140, 141, 142 | 9 |
| `IND-STAT-TPA-1882` | The Transfer of Property Act, 1882 | Act 4 of 1882 | Secs 53A, 54, 58, 105, 106 | 5 |
| `IND-STAT-COMM-COURTS-2015` | The Commercial Courts Act, 2015 | Act 4 of 2016 | Secs 2(1)(c), 6, 12A, 16 | 6 |
| **TOTAL** | **11 Central Enactments** | | | **184** |

---

## 3. Detailed Provision Analysis

### 3.1 Negotiable Instruments Act, 1881 (`IND-STAT-NI-1881`)
- **Section 138 (Dishonour of Cheque)**: Establishes criminal liability for cheque bounces due to insufficient funds. Indexes the essential statutory conditions:
  - 3-month presentation requirement.
  - 30-day statutory demand notice from receipt of bank return memo.
  - 15-day grace period for payment before cause of action arises.
- **Section 139 (Presumption in favour of holder)**: Rebuttable statutory presumption under reverse onus doctrine (*Rangappa v. Sri Mohan*).
- **Section 140 (Defence not allowed)**: Drawer cannot claim absence of reason to believe dishonour would occur.
- **Section 141 (Offences by companies)**: Vicarious liability for directors and persons in charge of company affairs.
- **Section 142 (Cognizance of offences)**: Mandatory written complaint within 1 month, non-obstante CrPC clause, proviso allowing condonation of delay upon showing sufficient cause.

### 3.2 Transfer of Property Act, 1882 (`IND-STAT-TPA-1882`)
- **Section 53A (Part Performance)**: Doctrine of part performance debarring transferor from dispossessing transferee under an unperfected registered contract.
- **Section 54 (Sale & Contract for Sale)**: Distinction between conveyance of ownership (mandatorily registered for value $\ge$ Rs. 100) and contract for sale (creates no proprietary interest or charge).
- **Section 58 (Mortgages)**: Definitions of mortgagor, mortgagee, mortgage-money, and mortgage-deed across simple, conditional, usufructuary, and English mortgages.
- **Section 105 (Leases)**: Definition of lessor, lessee, premium, and rent.
- **Section 106 (Duration & Termination of Leases)**: Statutory presumptions: year-to-year terminable on 6 months' notice for agricultural/manufacturing; month-to-month terminable on 15 days' notice for other purposes.

### 3.3 Commercial Courts Act, 2015 (`IND-STAT-COMM-COURTS-2015`)
- **Section 2(1)(c) (Commercial Dispute Definition)**: Exhaustive enumeration across 22 commercial transactions (trade, export/import, maritime, IP, shareholder agreements).
- **Section 6 (Jurisdiction)**: Territorial and specified value jurisdiction of commercial courts.
- **Section 12A (Pre-Institution Mediation & Settlement)**: Mandatory pre-institution mediation for suits not contemplating urgent interim relief (*Patil Automation v. Rakheja Engineers*).
- **Section 16 (Amendments to CPC)**: Overriding procedural amendments to CPC for commercial matters (strict written statement timelines, discovery rules, case management hearings).

---

## 4. Verification and Database Integrity

All chunks were validated using `NationalCorpusPipeline` and verified via SQLite schema constraints:
- `is_synthetic_scaffold = 0` for all 184 statutory chunks.
- All 11 central enactments registered in `sources` table.
- Bitwise freeze check (`python scripts/verify_freeze.py`) verified 100% clean with zero drift.

