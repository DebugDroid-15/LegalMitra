# Phase 29: State and Union Territory Source Registry & Maturity Model
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. National Scope & Purpose

LegalMitra maintains a canonical inventory of all 28 States and 8 Union Territories in India. The objective of the State and Union Territory Source Registry is to establish verifiable provenance for state enactments, subordinate rules, and High Court decisions, ensuring every statutory assertion links back to an authentic official gazette or legislative portal.

---

## 2. 12-State Coverage Maturity Model

To eliminate ambiguities regarding what is indexed versus merely known, LegalMitra implements a strict 12-state progressive maturity lifecycle:

```
[not_discovered] ──> [discovered] ──> [registered] ──> [accessible] 
       │
       ▼
   [acquired] ──> [parsed] ──> [structurally_validated] ──> [authenticity_verified] 
       │
       ▼
   [indexed] ──> [retrieval_verified] ──> [temporally_verified] ──> [legally_reviewed]
```

### Definitions:
1. `not_discovered`: Jurisdiction or body identified only by statutory jurisdiction list.
2. `discovered`: Official portal, gazette repository, and responsible authority verified.
3. `registered`: Canonical schema record entered in `state_ut_registry.json`.
4. `accessible`: Automated crawler or API connectivity confirmed.
5. `acquired`: Raw gazette PDFs / bare acts downloaded with cryptographic SHA256.
6. `parsed`: Extracted into structured text and section-level provisions.
7. `structurally_validated`: Verified for sections, subsections, provisos, and schedules.
8. `authenticity_verified`: Corroborated against official gazette notification numbers.
9. `indexed`: Ingested into SQLite knowledge base (`legal_chunks` & `sources`).
10. `retrieval_verified`: Confirmed retrievable via BM25/FTS5 under jurisdiction filters.
11. `temporally_verified`: Enactment, commencement, and amendment dates verified.
12. `legally_reviewed`: Signed off by advocate reviewer with Bar Council credentials.

---

## 3. Canonical Registry Summary (`state_ut_registry.json`)

All 36 Indian sub-national jurisdictions are catalogued in `data/08_corpus/state_ut_registry.json`:
- **States (28):** Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal.
- **Union Territories (8):** Andaman & Nicobar Islands, Chandigarh, Dadra & Nagar Haveli and Daman & Diu, Delhi (NCT), Jammu & Kashmir, Ladakh, Lakshadweep, Puducherry.

### Current Maturity Distribution:
- **`temporally_verified`:** NCT of Delhi (`IN-DL`), Maharashtra (`IN-MH`)
- **`discovered`:** Remaining 27 States, 7 Union Territories
- **`legally_reviewed`:** 0 (Awaiting formal advocate review execution)

The machine-readable matrix is maintained in `data/09_national_corpus/jurisdiction_coverage_matrix.json`.
