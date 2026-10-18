# LEGALMITRA PHASE 24: PRECEDENT GRAPH & ARTICLE 141 VALIDATION REPORT

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 24 — Master Expansion  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

LegalMitra implements Article 141 precedent intelligence and proposition-aware overruling mechanics via `legalmitra/caselaw/knowledge_graph.py`. In Phase 24, the national litigation knowledge graph was expanded from 20 nodes and 12 edges to **40 nodes and 31 edges**, accurately encoding constitutional linkages, statutory provisions, criminal procedural transitions, and judicial overrulings.

---

## 2. Precedent & Overruling Verification Matrix

| Precedent / Subject Case | Overruling / Affirming Authority | Relation Type | Scope & Legal Consequence |
| :--- | :--- | :--- | :--- |
| *Himangni Enterprises* (2017) | *Vidya Drolia v. Durga Trading Corp.* (2021) 2 SCC 1 | `OVERRULES` | Landlord-tenant disputes governed by the Transfer of Property Act, 1882 are arbitrable unless covered by special rent control legislation. |
| *Shafhi Mohammad* (2018) | *Arjun Panditrao Khotkar* (2020) 7 SCC 1 | `PARTIALLY_OVERRULES` | Clarified that Section 65B(4) / Section 63(4) certificate cannot be waived where secondary electronic evidence is produced. |
| *Krishna Janardhan Bhat* (2008) | *Rangappa v. Sri Mohan* (2010) 11 SCC 441 | `OVERRULES` | The statutory presumption under Section 139 of the NI Act extends to the existence of a legally enforceable debt. |
| *NN Global Mercantile* (2023) 5-Judge | *In Re: Arbitration Agreements & Stamp Act* (2024) 6 SCC 1 (7-Judge) | `OVERRULES` | Non-stamping or insufficient stamping of an arbitration agreement is a curable defect and does not render the agreement void ab initio at referral stage under Section 11. |
| *Gurbaksh Singh Sibbia* (1980) 5-Judge | *Sushila Aggarwal v. State (NCT of Delhi)* (2020) 5 SCC 1 (5-Judge) | `AFFIRMS` | Anticipatory bail under Section 438 CrPC (Section 482 BNSS) should not be subjected to invariable time limitations. |

---

## 3. Statutory-to-Precedent Linkages

The knowledge graph bridges statutory and constitutional provisions with binding case law:

- **Article 21 (Constitution)**: Linked to *Maneka Gandhi*, *Puttaswamy*, and *D.K. Basu*.
- **Article 368 (Constitution)**: Linked to *Kesavananda Bharati*.
- **Section 154 CrPC & Section 173 BNSS**: Linked to *Lalita Kumari* (Mandatory FIR registration upon disclosure of cognizable offence).
- **Section 41 CrPC & Section 35 BNSS**: Linked to *Arnesh Kumar* (Mandatory checklist for arrest in offences punishable up to 7 years).
- **Section 438 CrPC & Section 482 BNSS**: Linked to *Sushila Aggarwal* (Pre-arrest bail duration).
- **Section 66A IT Act**: Linked to *Shreya Singhal* (Unconstitutional).
- **Section 304A IPC & Section 106 BNS**: Linked to *Jacob Mathew* (Gross medical negligence standard).
- **Section 56 Indian Contract Act**: Linked to *Energy Watchdog* (Commercial difficulty / price rise is not frustration).
