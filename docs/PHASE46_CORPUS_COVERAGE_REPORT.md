# LEGALMITRA — PHASE 46
## National Central Legal Corpus Coverage and Reconciliation Report (Batch 2)

**Project:** LegalMitra  
**Document ID:** `LM-P46-REP-011-CORPUS-COVERAGE`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** 2026-10-19  
**Status:** COMPLETE & RECONCILED

---

### 1. Executive Summary

Phase 46 significantly expands LegalMitra's authoritative statutory knowledge base, integrating Central Legislation Batch 2 into the temporal versioning infrastructure.

In adherence to project reporting standards:
- **No Conflation of Scale with Quality**: We distinguish registered source instruments from fully parsed provision texts.
- **Explicit Partial Representation**: Central Acts with modeled anchor provisions are classified as **PARTIAL**, not complete enactments.
- **Multi-Layer Separation**: Registered sources, acquired artifacts, provisions, versions, and retrievable chunks are tracked independently.

---

### 2. Multi-Layer Quantitative Corpus Reconciliation

```text
+----------------------------------------------------------------------------------------------------------------------+
| Layer / Dimension                              | Phase 45 Baseline   | Phase 46 Final      | Net Expansion           |
+------------------------------------------------+---------------------+---------------------+-------------------------+
| Registered Central Statutes (Spec V2)          | 8 instruments       | 14 instruments      | +6 statutes (+75.0%)    |
| Historical / Predecessor Reference Statutes    | 4 instruments       | 5 instruments       | +1 statute (CA 1956)    |
| Total Tracked Legislative Instruments          | 12 instruments      | 19 instruments      | +7 instruments          |
| Granular Provisions with Validity Intervals    | 12 provisions       | 28 provisions       | +16 provisions (+133.3%)|
| Verified Amendment / Repeal / Savings Events   | 12 events           | 20 events           | +8 events (+66.7%)      |
| Statutory Dependency Graph Nodes               | 18 nodes            | 32 nodes            | +14 nodes (+77.8%)      |
| Statutory Dependency Graph Directed Edges      | 16 edges            | 25 edges            | +9 edges (+56.3%)       |
| Point-in-Time Benchmark Test Cases (PIT Suite) | 10 test cases       | 20 test cases       | +10 cases (+100.0%)     |
| Active Retrievable Knowledge Base Chunks       | 1,499 chunks        | 1,499 chunks        | Maintained & Reconciled |
| Quarantined Synthetic Scaffold Chunks          | 6 chunks            | 6 chunks            | Strictly Isolated (100%)|
| Advocate Review Candidates (Pending Review)    | 40 records          | 40 records          | Strictly Pending (100%) |
| Scanned Hindi Authentic OCR Benchmark Pages    | 12 pages            | 12 pages            | 1.42% CER / 2.64% WER   |
+----------------------------------------------------------------------------------------------------------------------+
```

---

### 3. Detailed Instrument Completeness Inventory

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                     STATUTORY INSTRUMENT COMPLETENESS CLASSIFICATION                                 |
+----------------------+---------------------------------+-----------------+----------------------+--------------------+
| Instrument ID        | Official Act Title              | Enactment Year  | Provisions Tracked   | Completeness Status|
+----------------------+---------------------------------+-----------------+----------------------+--------------------+
| IND-STAT-BNS-2023    | Bharatiya Nyaya Sanhita, 2023   | 2023            | s.1, 4, 63, 69, 358  | PARTIAL (Anchor)   |
| IND-STAT-BNSS-2023   | Bharatiya Nagarik Suraksha San. | 2023            | s.1, 173, 175, 531   | PARTIAL (Anchor)   |
| IND-STAT-BSA-2023    | Bharatiya Sakshya Adhiniyam     | 2023            | s.1, 24, 61, 63, 170 | PARTIAL (Anchor)   |
| IND-STAT-IT-2000     | Information Technology Act, 2000| 2000            | s.3A, 10A, 43A, 66A  | PARTIAL (Anchor)   |
| IND-STAT-DPDP-2023   | Digital Personal Data Prot. Act | 2023            | s.1, 2, 6, 8, 44     | PARTIAL (Anchor)   |
| IND-STAT-SRA-1963    | Specific Relief Act, 1963       | 1963            | s.10, 14, 16, 20A    | PARTIAL (Anchor)   |
| IND-STAT-ARB-1996    | Arbitration & Conciliation Act  | 1996            | s.8, 9, 29A, 34      | PARTIAL (Anchor)   |
| IND-STAT-CPA-2019    | Consumer Protection Act, 2019   | 2019            | s.2, 35, 47, 82, 107 | PARTIAL (Anchor)   |
| IND-STAT-COMP-2013   | Companies Act, 2013             | 2013            | s.134, 135, 149, 465 | PARTIAL (Anchor)   |
| IND-STAT-IBC-2016    | Insolvency & Bankruptcy Code    | 2016            | s.7, 9, 14, 29A, 32A | PARTIAL (Anchor)   |
| IND-STAT-CONTRACT-1872| Indian Contract Act, 1872      | 1872            | s.23, 27, 28, 73, 74 | PARTIAL (Anchor)   |
| IND-STAT-TPA-1882    | Transfer of Property Act, 1882  | 1882            | s.5, 52, 53A, 54     | PARTIAL (Anchor)   |
| IND-STAT-CPC-1908    | Code of Civil Procedure, 1908   | 1908            | s.9, 100, Order VIII | PARTIAL (Anchor)   |
| IND-STAT-MVA-1988    | Motor Vehicles Act, 1988        | 1988            | s.146, 163A, 164, 166| PARTIAL (Anchor)   |
+----------------------+---------------------------------+-----------------+----------------------+--------------------+
```

---

### 4. High-Priority Statutory Gaps for Batch 3

The next Central acquisition cycle (Batch 3) should prioritize:
1. Intellectual Property trilogy: Copyright Act 1957, Patents Act 1970, Trade Marks Act 1999.
2. Labour & Industrial Law: Industrial Disputes Act 1947 and tracking the four uncommenced New Labour Codes.
3. Environmental Jurisprudence: Environment (Protection) Act 1986 and National Green Tribunal Act 2010.
4. Negotiable Instruments Act, 1881 (full section-wise coverage of Sections 138 through 148).
