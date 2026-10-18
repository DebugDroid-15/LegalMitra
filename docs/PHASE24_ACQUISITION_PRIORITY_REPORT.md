# LegalMitra Phase 24 Acquisition Priority Report
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

This report establishes the transparent, evidence-grounded acquisition prioritization framework for expanding LegalMitra's Indian legal corpus in Phase 24. Prioritization explicitly favors legal utility, binding authority level, verified official source availability, and coverage gap size over indiscriminate volume.

---

## 2. Priority Scoring Mathematical Model

Each candidate instrument or judicial decision $d$ is scored on a $[0.0, 100.0]$ scale using:

$$\text{Score}(d) = \min\left(100.0, \, \left(W_{\text{authority}}(d) \times M_{\text{domain}}(d)\right) + B_{\text{gap}}(d)\right)$$

Where:
- $W_{\text{authority}} \in [0.0, 40.0]$: Authority weight (Supreme Constitutional: 40.0, Binding Central Statute: 35.0, Supreme Court Art. 141: 35.0, Binding State Statute: 25.0, Delegated Rule: 20.0, Scaffold: 0.0).
- $M_{\text{domain}} \in [1.0, 1.30]$: Domain multiplier based on practical legal research frequency across 14 high-utility areas.
- $B_{\text{gap}} \in \{5.0, 20.0\}$: Coverage gap bonus (20.0 if unindexed, 5.0 if partially indexed).

---

## 3. High-Utility Legal Domain Multipliers

| Domain | Weight Multiplier | Rationale & Practical Need |
| :--- | :---: | :--- |
| **Constitutional rights & remedies** | 1.30 | Foundational Article 14, 19, 21, 32, 226 remedies |
| **Police procedure, FIRs & criminal law** | 1.25 | Arrest guidelines, mandatory FIR, remand safeguards, BNS/BNSS |
| **Cybercrime & online fraud** | 1.25 | IT Act, digital frauds, Section 66A, electronic evidence |
| **Information technology & data protection** | 1.20 | DPDP 2023, IT Act intermediary rules |
| **Women's rights & protective legislation** | 1.20 | POCSO, sexual harassment (POSH), domestic violence |
| **Right to Information** | 1.15 | Transparency, public authority duties, disclosure exemptions |
| **Consumer protection** | 1.15 | Product liability, unfair trade practices, medical negligence |
| **Arbitration & dispute resolution** | 1.15 | Section 8, 9, 11, 34 challenges, stamp duty interplay |
| **Contract & commercial law** | 1.15 | Commercial Courts 12A mediation, Section 56 frustration |
| **Civil procedure & limitation** | 1.10 | Order 7 Rule 11, Section 5 condonation of delay |
| **Property, rental & tenancy** | 1.10 | Rent control acts, Transfer of Property Section 53A / 54 |
| **Traffic & motor vehicle law** | 1.10 | Road safety, MACT claims under MV Act 1988/2019 |
| **Employment & labour rights** | 1.10 | Industrial disputes, termination, wage protection |
| **Family law** | 1.10 | Maintenance under Section 125 CrPC / BNSS 144 |

---

## 4. Phase 24 Acquisition Priority Queue (Top Candidates)

| Rank | Priority | Candidate Source | Document Family | Legal Domain | Gap Status |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | **65.5** | *Maneka Gandhi v. Union of India* (1978) 1 SCC 248 | Supreme Court Judgment | Constitutional rights & remedies | Completely Unindexed |
| **2** | **65.5** | *Kesavananda Bharati v. State of Kerala* (1973) 4 SCC 225 | Supreme Court Judgment | Constitutional rights & remedies | Completely Unindexed |
| **3** | **63.8** | *D.K. Basu v. State of West Bengal* (1997) 1 SCC 416 | Supreme Court Judgment | Police procedure & criminal safeguards | Completely Unindexed |
| **4** | **63.8** | *Lalita Kumari v. Govt. of U.P.* (2014) 2 SCC 1 | Supreme Court Judgment | Police procedure & mandatory FIR | Completely Unindexed |
| **5** | **63.8** | *Arnesh Kumar v. State of Bihar* (2014) 8 SCC 273 | Supreme Court Judgment | Police procedure & arrest limits | Completely Unindexed |
| **6** | **63.8** | *Shreya Singhal v. Union of India* (2015) 5 SCC 1 | Supreme Court Judgment | Cybercrime & online speech | Completely Unindexed |
| **7** | **60.2** | Right to Information Act, 2005 (Act No. 22 of 2005) | Central Act | Right to Information | Completely Unindexed |
| **8** | **60.2** | *Jacob Mathew v. State of Punjab* (2005) 6 SCC 1 | Supreme Court Judgment | Consumer protection & medical negligence | Completely Unindexed |
| **9** | **60.2** | *Vidya Drolia v. Durga Trading Corp.* (2021) 2 SCC 1 | Supreme Court Judgment | Arbitration & tenancy disputes | Completely Unindexed |
| **10** | **60.2** | *Energy Watchdog v. CERC* (2017) 14 SCC 80 | Supreme Court Judgment | Contract & force majeure | Completely Unindexed |
| **11** | **48.8** | Bharatiya Sakshya Adhiniyam, 2023 (Expansion) | Central Act | Evidence & criminal procedure | Partially Indexed (6 chunks) |
| **12** | **48.8** | Bharatiya Nyaya Sanhita, 2023 (Expansion) | Central Act | Penal law & criminal procedure | Partially Indexed (28 chunks) |
| **13** | **47.0** | POCSO Act, 2012 (Expansion) | Central Act | Women's rights & child protection | Partially Indexed (4 chunks) |

The complete ranked queue is saved at `data/09_national_corpus/phase24_acquisition_queue.json`.
