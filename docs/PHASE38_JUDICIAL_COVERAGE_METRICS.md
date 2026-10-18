# LegalMitra — Phase 38: Judicial Coverage Metrics & Gap Accounting

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the multi-tier coverage evaluation framework and empirical gap accounting designed and implemented in LegalMitra Phase 38. The framework explicitly prevents misleading claims of universal or exhaustive coverage by tracking institutions across 11 discrete, measurable stages.

Implemented in `legalmitra/judicial/coverage_analytics.py` and exported to `data/21_judicial_infrastructure/judicial_coverage_matrix.json`.

---

## 2. 11-Tier Coverage Hierarchy (Tier 0 to Tier 10)

| Tier Level | Designation | Rigorous Criteria for Progression |
| :---: | :--- | :--- |
| **Tier 0** | `UNMAPPED` | The court or tribunal exists but is not catalogued in the system. |
| **Tier 1** | `CATALOGUED` | Institutional identity, official nomenclature, jurisdiction, and historical predecessor established. |
| **Tier 2** | `SOURCE_IDENTIFIED` | Official digital portal, gazette, or repository located, URL validated, and terms audited. |
| **Tier 3** | `PIPELINE_DESIGNED` | Scraping, API connector, or gazette ingestion processing pipeline specified. |
| **Tier 4** | `PIPELINE_TESTED` | Operational pipeline verified with test fixtures and mock records. |
| **Tier 5** | `SAMPLING_VALIDATED` | Representative sample of authentic judgments ingested, OCR quality audited, metadata verified. |
| **Tier 6** | `SUBSTANTIAL_HOLDINGS` | Significant percentage of reported judgments acquired and verified. |
| **Tier 7** | `COMPREHENSIVE_ERA` | All officially reported judgments for a specified historical era acquired with zero known gaps. |
| **Tier 8** | `PRECEDENT_INTEGRATED` | All citations cross-referenced and integrated into the typed precedent graph. |
| **Tier 9** | `MULTILINGUAL_EXPANDED` | Judgments available with authorized vernacular translations in scheduled languages. |
| **Tier 10** | `INDEPENDENTLY_EVALUATED` | External advocate and jurist review confirming 100% coverage and accuracy. |

---

## 3. Current Empirical Status Matrix

| Institution | Institutional Tier | Current Coverage Tier | Total Est. Records | Ingested & Verified | Average OCR Conf. | Documented Gaps |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Supreme Court of India** (`IND-SC`) | APEX | **Tier 5** | ~75,000 | 185 | 0.985 | Retrospective batch 1950–1990 pending bulk transfer |
| **Delhi High Court** (`IND-HC-DEL`) | HIGH_COURT | **Tier 5** | ~120,000 | 112 | 0.978 | Pre-2000 digital unreported decisions offline |
| **Bombay High Court** (`IND-HC-BOM`) | HIGH_COURT | **Tier 2** | ~250,000 | 22 | 0.962 | Benches at Nagpur, Aurangabad, Goa need crawler connectors |
| **Armed Forces Tribunal** (`IND-MIL-AFT`) | MILITARY_JUSTICE | **Tier 2** | ~35,000 | 14 | 0.954 | Regional bench orders maintained in local registries |
| **NCLAT** (`IND-TR-NCLAT`) | TRIBUNAL | **Tier 3** | ~15,000 | 18 | 0.981 | Chennai Bench requires distinct pagination handler |
| **NGT** (`IND-TR-NGT`) | TRIBUNAL | **Tier 2** | ~28,000 | 12 | 0.974 | Zonal bench orders (Pune, Bhopal, Kolkata, Chennai) |
| **District Courts (National)** (`IND-DIST-GENERIC`) | DISTRICT_COURT | **Tier 1** | ~15,000,000 | 35 (Pilot) | 0.941 | 680+ District complexes require distributed API infrastructure |

---

## 4. Truthful Reporting Invariant

Under no circumstances does LegalMitra report Tier 6+ or "universal" coverage for any court where empirical ingestion has not been completed. This transparency protects legal researchers and jurists from relying on incomplete digital representations.
