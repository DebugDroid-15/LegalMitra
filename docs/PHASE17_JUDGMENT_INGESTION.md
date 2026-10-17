# LEGALMITRA — PHASE 17C: JUDGMENT ACQUISITION & STRUCTURAL INGESTION REPORT

**Workspace:** `c:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

In Phase 17C, LegalMitra completed the structural ingestion of authentic judicial decisions, transitioning from an in-memory precedent prototype to a source-grounded case-law database in `data/legalmitra_kb.db`.

7 foundational landmark judgments across the Supreme Court of India and High Courts were normalized, registered with SHA-256 digests, and indexed into SQLite with full-text search (FTS5). 

Total active judgment chunks expanded from **7 chunks** (Puttaswamy only) to **39 genuine judgment chunks** (45 chunks total including 6 strictly quarantined test scaffold chunks).

---

## 2. Ingested Judicial Decisions Inventory

| Case Identifier | Case Title & Citation | Court | Bench Coram | Chunks Indexed | Primary Subject | Precedent Treatment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IND-JUD-SC-2020-ARJUN-KHOTKAR` | *Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal* (2020) 7 SCC 1 (2020 INSC 452) | Supreme Court | R.F. Nariman, S. Ravindra Bhat, V. Ramasubramanian, JJ. | 7 | Electronic Evidence (BSA s.63 / IEA s.65B) | Affirms *Anvar P.V.*; Overrules *Shafhi Mohammad* |
| `IND-JUD-SC-2014-ANVAR-PV` | *Anvar P.V. v. P.K. Basheer* (2014) 10 SCC 473 (2014 INSC 650) | Supreme Court | R.M. Lodha, CJI, Kurian Joseph, R.F. Nariman, JJ. | 5 | Electronic Records Proof (*Generalia specialibus*) | Overrules *State v. Navjot Sandhu* on electronic records |
| `IND-JUD-SC-2018-SHAFHI-MOHAMMAD` | *Shafhi Mohammad v. State of H.P.* (2018) 2 SCC 801 (2018 INSC 92) | Supreme Court | A.K. Goel, U.U. Lalit, JJ. | 3 | Device Non-Possession Exemption (Overruled) | Overruled by 3-Judge Bench in *Arjun Khotkar* |
| `IND-JUD-SC-2022-ANTIL` | *Satender Kumar Antil v. CBI* (2022) 10 SCC 51 (2022 INSC 690) | Supreme Court | S.K. Kaul, M.M. Sundresh, JJ. | 5 | Bail Jurisprudence & Arrest Mandate (BNSS s.35 / CrPC s.41A) | National Bail Administration Guidelines |
| `IND-JUD-SC-2020-PERKINS-EASTMAN` | *Perkins Eastman Architects DPC v. HSCC (India) Ltd* (2020) 20 SCC 760 (2019 INSC 1289) | Supreme Court | U.U. Lalit, Indu Malhotra, JJ. | 4 | Arbitration Sole Arbitrator Nomination (A&C Act s.12(5)) | Extends *TRF Ltd.* disqualification to sole appointment |
| `IND-JUD-SC-1954-SATYABRATA` | *Satyabrata Ghose v. Mugneeram Bangur & Co.* (1954) SCR 310 | Supreme Court | B.K. Mukherjea, Vivian Bose, N.H. Bhagwati, JJ. | 4 | Frustration Doctrine & Impossibility (ICA s.56) | Foundational Authority on Indian Frustration |
| `IND-JUD-SC-2008-SATYAWATI` | *Satyawati Sharma v. Union of India* (2008) 5 SCC 287 | Supreme Court (Delhi) | B.N. Agrawal, G.S. Singhvi, JJ. | 4 | Delhi Rent Control Commercial Bona Fide Eviction (DRC s.14(1)(e)) | Strikes down discriminatory restriction under Article 14 |
| `IND-JUD-SC-2017-PUTTASWAMY` | *K.S. Puttaswamy v. Union of India* (2017) 10 SCC 1 (2017 INSC 650) | Supreme Court | 9-Judge Constitution Bench | 7 | Fundamental Right to Privacy (Art. 21) | Overrules *M.P. Sharma* and *Kharak Singh* |
| **TOTAL** | **8 Genuine Landmark Precedents** | — | — | **39 Genuine Chunks** | — | — |

---

## 3. Structural Extraction & Passage Fidelity

1. **Paragraph Numbering**:
   - Every paragraph chunk retains exact court numbering (e.g. `IND-JUD-SC-2020-ARJUN-KHOTKAR:PARA:51` for Paragraph 51, `PARA:72`, `PARA:73`).
2. **Issue Framing & Discrete Holdings**:
   - Separate chunks are created for explicit legal issues framed by the bench (`HOLDING:1`, `HOLDING:2`) linking issue statements to supporting paragraphs.
3. **Ratio Decidendi Isolation**:
   - The binding rule of law is indexed as a dedicated chunk (`:RATIO`) with coram and citation tags.
4. **Passage-Level Retrievability**:
   - Search queries can retrieve specific numbered paragraphs, isolated holdings, or general case summaries without returning monolithic raw documents.

