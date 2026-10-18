# LegalMitra — Phase 39: National Judicial Coverage Analytics V2

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the National Judicial Coverage Analytics (Version 2) implemented in Phase 39 Workstream K. The framework enforces an 11-tier coverage metric (Tier 0 to Tier 10) with explicit, auditable gap accounting. It prevents misleading universal coverage claims by distinguishing between cataloging an institution and acquiring its records.

Machine-readable matrix: `data/21_judicial_infrastructure/judicial_coverage_matrix_v2.json`.

---

## 2. 11-Tier Metric Definitions

- **Tier 0 (Unmapped)**: Court exists but not yet catalogued.
- **Tier 1 (Catalogued)**: Institutional identity, jurisdiction, and historical predecessor established.
- **Tier 2 (Source Identified)**: Official digital portal, gazette, or repository located and validated.
- **Tier 3 (Pipeline Designed)**: Scraping, API, or gazette processing pipeline specified.
- **Tier 4 (Pipeline Tested)**: Operational pipeline verified with test fixtures.
- **Tier 5 (Sampling Validated)**: Representative sample ingested, OCR quality audited, metadata verified.
- **Tier 6 (Substantial Holdings)**: Significant percentage of reported judgments acquired and verified.
- **Tier 7 (Comprehensive Era)**: All officially reported judgments for specified era acquired.
- **Tier 8 (Precedent Integrated)**: Citations cross-referenced into typed precedent graph.
- **Tier 9 (Multilingual Expanded)**: Judgments available with authorized vernacular translations.
- **Tier 10 (Independently Evaluated)**: External legal review confirming coverage and accuracy.

---

## 3. Comprehensive National Coverage Matrix V2

| Court / Institution | Tier Level | Current Coverage Tier | Est. Records | Verified Ingested | OCR Quality | Documented Coverage Gaps |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Supreme Court of India** | APEX | **Tier 5** | ~75,000 | 185 | 0.985 | Retrospective batch 1950–1990 pending bulk transfer |
| **Federal Court of India** | HISTORICAL | **Tier 5** | ~350 | 8 | 0.952 | FCR volumes 1937–1950 digitized from NAI scans |
| **Privy Council (Indian Appeals)**| HISTORICAL | **Tier 5** | ~4,500 | 12 | 0.961 | Moore's Indian Appeals & L.R. I.A. via open repositories |
| **Delhi High Court** | HIGH_COURT | **Tier 5** | ~120,000 | 112 | 0.978 | Pre-2000 digital unreported decisions offline |
| **Bombay High Court** | HIGH_COURT | **Tier 2** | ~250,000 | 22 | 0.962 | Nagpur, Aurangabad, and Goa benches require dedicated crawlers |
| **Allahabad High Court** | HIGH_COURT | **Tier 2** | ~300,000 | 18 | 0.958 | Pre-2000 digital orders fragmented across Lucknow & Prayagraj |
| **Calcutta High Court** | HIGH_COURT | **Tier 2** | ~280,000 | 15 | 0.965 | Circuit Benches at Jalpaiguri and Port Blair require separate endpoints |
| **Madras High Court** | HIGH_COURT | **Tier 2** | ~260,000 | 16 | 0.962 | Madurai Bench digitization batch pending |
| **Gujarat High Court** | HIGH_COURT | **Tier 2** | ~180,000 | 10 | 0.970 | Gujarati vernacular orders require dedicated OCR pipeline |
| **Karnataka High Court** | HIGH_COURT | **Tier 2** | ~190,000 | 12 | 0.968 | Dharwad and Kalaburagi bench sync |
| **Punjab & Haryana High Court**| HIGH_COURT | **Tier 2** | ~220,000 | 14 | 0.964 | Pre-1995 decisions offline |
| **Patna High Court** | HIGH_COURT | **Tier 2** | ~150,000 | 8 | 0.951 | Digital portal connectivity intermittent |
| **Rajasthan High Court** | HIGH_COURT | **Tier 2** | ~160,000 | 10 | 0.955 | Jaipur Bench portal separation |
| **Telangana High Court** | HIGH_COURT | **Tier 2** | ~85,000 | 9 | 0.972 | Post-2019 bifurcation records clean; legacy records in Hyderabad |
| **NCLAT** | TRIBUNAL | **Tier 3** | ~15,000 | 18 | 0.981 | Chennai Bench requires distinct pagination handler |
| **NGT** | TRIBUNAL | **Tier 2** | ~28,000 | 12 | 0.974 | Zonal bench orders (Pune, Bhopal, Kolkata, Chennai) |
| **ITAT** | TRIBUNAL | **Tier 2** | ~95,000 | 11 | 0.968 | 63 Benches nationwide require unified connector |
| **Armed Forces Tribunal** | MILITARY | **Tier 2** | ~35,000 | 14 | 0.954 | Regional bench orders maintained in local registries |
| **District Courts (National)** | DISTRICT | **Tier 1** | ~15,000,000 | 35 | 0.941 | 680+ District complexes require distributed API infrastructure |

---

## 4. Truthful Reporting Invariant

No institution without complete, exhaustive empirical ingestion is marked Tier 6 or higher. This truthfulness standard prevents misleading claims of universal coverage.
