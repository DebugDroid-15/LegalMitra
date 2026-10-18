# LegalMitra — Phase 38: District-to-Supreme Court Coverage Architecture

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document describes the end-to-end procedural and appellate flow linking District and Subordinate Courts, High Courts, and the Supreme Court of India. It details the structural framework for case progression, record digitization through eCourts, jurisdictional boundaries, and the empirical reality of subordinate court data acquisition.

---

## 2. Integrated Appellate Pathway

```
               +---------------------------------------------+
               |           Supreme Court of India            |
               | (Art. 32, 131, 132, 133, 134, 136, 137, 142)|
               +----------------------+----------------------+
                                      ^
               Special Leave / Appeals| (Arts. 132-136)
                                      |
               +----------------------+----------------------+
               |         Constitutional High Courts          |
               | (Arts. 214-227: Writs, Appeals, Revisions)  |
               +----------------------+----------------------+
                                      ^
          Appeals / Revisions / Writs | (Sec 96/100 CPC, Sec 374/397 CrPC)
                                      |
       +------------------------------+-------------------------------+
       |                                                              |
+------+----------------------+                    +------------------+-------------------+
|  District & Sessions Court  |                    | Specialized Tribunals (CAT, NCLAT)   |
| (Commercial Court / Special)|                    | (Statutory appeals / Writ review)    |
+--------------+--------------+                    +--------------------------------------+
               ^
               | Civil Appeals / Criminal Appeals
               |
+--------------+----------------------------------------------+
| Subordinate Adjudication Courts:                             |
| - CJM / CMM / JMFC / Metropolitan Magistrates               |
| - Civil Judge (Senior Division) / Sub-Judge                  |
| - Civil Judge (Junior Division) / Munsif Court               |
| - Small Causes Courts / Gram Nyayalayas                      |
+-------------------------------------------------------------+
```

---

## 3. Subordinate Court Digital Architecture (eCourts CIS)

- **eCourts Mission Mode Project**: Nationwide IT enablement overseen by the Supreme Court eCommittee and Department of Justice.
- **Case Information System (CIS 3.2)**: Standardized open-source software stack managing filing, case flow, daily orders, cause lists, and final judgments.
- **CNR Number (Case Number Record)**: Unique 16-character alphanumeric code identifying every case filed across Indian subordinate courts (Format: `[State Code][District Code][Establishment Code][Case Number][Year]`).
- **Scale**: Over 680 District Court complexes and 3,000+ subordinate court establishments handling ~4.4 crore pending cases.

---

## 4. Empirical Coverage Reality and Truthful Accounting

In compliance with LegalMitra's non-negotiable truthfulness standards:
1. **Subordinate Court Tier Designation**: District and Subordinate courts are currently held at **Tier 1 (Catalogued)** and **Tier 2 (Source Identified)** in the coverage matrix.
2. **No Universal Subordinate Ingestion Claim**: The platform does **not** claim complete acquisition of all 4.4 crore subordinate court records. Systematic subordinate acquisition requires specialized distributed API connectors, local language translation (Devanagari, Tamil, Telugu, Bengali, Kannada, Marathi, Gujarati, etc.), and multi-terabyte storage infrastructure.
3. **Verified Subordinate Sample**: A validated pilot sample of 35 subordinate judgments is maintained for testing schema compatibility and CNR resolution.
