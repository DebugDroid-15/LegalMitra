# PHASE 20 — LEGISLATION RECONCILIATION & TAXONOMY CLARIFICATION

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Reconciliation

---

## 1. Executive Summary: Entity Taxonomy Distinction

A frequent defect in legal corpus inventories is conflating **actual ingested statutory text** with **registry portal entries**, **jurisdiction definitions**, or **unparsed catalogued items**.

Phase 20 rigorously reconciles the **101 catalogued entries** in `data/09_national_corpus/legal_universe_inventory.json` against actual database entities in `data/legalmitra_kb.db`.

---

## 2. Taxonomic Entity Classification Matrix

| Entity Category | Inventory Count | Ingested in KB | Real-world Nature & Distinctions |
| :--- | :--- | :--- | :--- |
| **Constitutional Charter** | 1 | 1 (31 chunks) | Foundational charter (*The Constitution of India, 1950*). |
| **Constitutional Amendments** | 6 | 0 (Queued) | Formal Amendment Acts (42nd, 44th, 86th, 101st, 103rd, 106th CAAs). |
| **Primary Central Acts** | 30 | 12 (1,286 chunks) | Primary enactments of Parliament. 12 have indexed provisions; 18 queued. |
| **State-Specific Acts** | 4 | 4 (15 chunks) | Ingested enactments for Delhi (DRC, DPA) and Maharashtra (MRC, MPA). |
| **State/UT Legislative Portals** | 34 | 0 (Portals) | Official portals mapping the remaining 34 States & UTs (`UNIV-STATE-CORPUS-*`). |
| **Delegated Legislation & Rules** | 3 | 3 (8 chunks) | Subordinate rules (IT SPDI, IT Intermediary, CPA E-Commerce). |
| **Court Procedural Rules** | 2 | 0 (Queued) | Delhi High Court Original Side Rules 2018, Supreme Court Rules 2013. |
| **Commencement Orders** | 5 | 5 (5 chunks) | Official Gazette S.O. notifications enforcing BNSS, BNS, BSA, SRA, CPA. |
| **Judicial Precedents** | 15 | 8 (39 chunks) | Supreme Court decisions establishing binding Article 141 ratios. |
| **Quarantined Scaffold** | 1 | 1 (6 chunks) | `UNIV-SCAFFOLD-DEL-2024-BAIL` test fixture (strictly isolated). |
| **Total Inventory Items** | **101** | **35 Sources** | **1,363 total chunks in KB** |

---

## 3. Scope of Legislative Expansion for Phase 20

To advance from partial statutory coverage to a deep, source-verifiable legislative corpus:
1. **Constitution of India**: Expand from 31 baseline chunks to cover Preamble, Fundamental Rights (Articles 12–35), Directive Principles (Articles 36–51), Fundamental Duties (Article 51A), Union Judiciary (Articles 124–147), High Courts (Articles 214–227), Emergency Provisions (Articles 352–360), and Amendment Powers (Article 368).
2. **Foundational Central Statutes**: Ingest core missing provisions for the Negotiable Instruments Act 1881 (Cheque dishonour Sections 138–142), Transfer of Property Act 1882 (Sections 53A, 54, 58, 105, 106), and Commercial Courts Act 2015.
3. **Amendment Reconstruction**: Link historical and substituted versions with explicit amending Acts and commencement Gazette notifications.
4. **All 36 States & UTs**: Create a machine-readable State/UT coverage matrix reflecting actual legislative data, rather than merely catalogued portal links.

