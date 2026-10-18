# LegalMitra — Phase 39: National Judicial Source Registry

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the authoritative National Judicial Source Registry established in Phase 39. It expands beyond conceptual institutional ontology into verified operational access channels across the Supreme Court of India, State/UT High Courts, Subordinate/District Courts, Specialized Tribunals, Military Justice, and Historical Pre-1950 Judicial Archives.

Machine-readable source registry: `data/21_judicial_infrastructure/national_judicial_source_inventory.json`.

---

## 2. 16-Field Mandatory Specification Standard

In compliance with Phase 39 Workstream B, every judicial source registered in LegalMitra enforces all 16 standardized metadata fields:
1. `source_id`: Stable alphanumeric identifier (e.g. `SRC-SC-ESCR`).
2. `institution_id`: Linked institutional entity in the judicial ontology (`IND-SC`, `IND-HC-*`, etc.).
3. `institution_name`: Full official name of the court or tribunal.
4. `jurisdiction`: Territorial or subject-matter jurisdiction.
5. `source_url`: Validated official portal endpoint.
6. `source_type`: Architectural category (`APEX_PORTAL`, `ESCR_REPOSITORY`, `HIGH_COURT_PORTAL`, `ECOURTS_SERVICES`, `TRIBUNAL_PORTAL`, `MILITARY_PORTAL`, `HISTORICAL_DIGITAL_ARCHIVE`, `GAZETTE_ARCHIVE`).
7. `available_years`: Historical and digital year range covered.
8. `document_types`: Authorized record types (Judgments, Orders, Decrees, Advisory References).
9. `languages`: Official and vernacular languages present (`en`, `hi`, `mr`, `ta`, etc.).
10. `acquisition_method`: Technical connector type (`PUBLIC_PORTAL_CONNECTOR`, `REST_API`, `ARCHIVAL_REPOSITORY_INGESTION`).
11. `access_restrictions`: Real-world access barriers (`OPEN_PUBLIC`, `CAPTCHA_GATED`, `RATE_LIMITED`, `IN_CAMERA_RESTRICTED`).
12. `reuse_status`: Legal usability basis under Section 52(1)(q) of the Indian Copyright Act 1957.
13. `source_health`: Empirical operational status (`HEALTHY_ACTIVE`, `RATE_LIMITED`, `SCHEMA_DEGRADED`).
14. `last_checked_timestamp`: ISO 8601 UTC audit timestamp.
15. `last_successful_acquisition`: Timestamp of latest verified payload acquisition.
16. `verification_method`: Ground-truth audit technique (Watermark, CNR, Digest hash, Neutral citation).
17. `known_coverage_gaps`: Explicitly documented gaps to avoid false universal coverage claims.
18. `acquisition_priority`: Triage tier (`P0_IMMEDIATE`, `P1_HIGH`, `P2_MEDIUM`, `P3_LONG_TERM`).
19. `blocker_details`: Specific blockers preventing unrestricted automated ingestion.

---

## 3. Registered Institutional Sources Summary

| Source ID | Institution | Source Type | Available Era | Languages | Access Gating | Priority |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| `SRC-SC-ESCR` | Supreme Court of India (eSCR) | `ESCR_REPOSITORY` | 1950–2024 | English, Hindi | Rate Limited | **P0** |
| `SRC-SC-SCI-GOV` | Supreme Court Official Portal | `APEX_PORTAL` | 1990–2024 | English | CAPTCHA Gated | **P1** |
| `SRC-HC-DEL-PORTAL` | High Court of Delhi | `HIGH_COURT_PORTAL` | 1966–2024 | English | Rate Limited | **P0** |
| `SRC-HC-BOM-PORTAL` | High Court of Judicature at Bombay | `HIGH_COURT_PORTAL` | 1990–2024 | English, Marathi | Rate Limited | **P1** |
| `SRC-HC-CAL-PORTAL` | Calcutta High Court | `HIGH_COURT_PORTAL` | 1995–2024 | English | Rate Limited | **P1** |
| `SRC-HC-MAD-PORTAL` | Madras High Court | `HIGH_COURT_PORTAL` | 1995–2024 | English, Tamil | Rate Limited | **P1** |
| `SRC-HC-ALL-PORTAL` | Allahabad High Court | `HIGH_COURT_PORTAL` | 1990–2024 | English, Hindi | Rate Limited | **P1** |
| `SRC-ECOURTS-SERVICES` | eCourts Services (680+ District Courts) | `ECOURTS_SERVICES` | 2013–2024 | English, 11 Vernaculars | CAPTCHA Gated | **P1** |
| `SRC-TR-NCLAT-PORTAL` | NCLAT Principal & Chennai Benches | `TRIBUNAL_PORTAL` | 2016–2024 | English | Rate Limited | **P0** |
| `SRC-TR-NGT-PORTAL` | National Green Tribunal | `TRIBUNAL_PORTAL` | 2011–2024 | English | Rate Limited | **P1** |
| `SRC-TR-CAT-PORTAL` | Central Administrative Tribunal | `TRIBUNAL_PORTAL` | 2005–2024 | English, Hindi | Rate Limited | **P1** |
| `SRC-MIL-AFT-PORTAL` | Armed Forces Tribunal | `MILITARY_PORTAL` | 2009–2024 | English | Rate Limited | **P1** |
| `SRC-HIST-FED-COURT` | Federal Court of India (NAI) | `HISTORICAL_DIGITAL_ARCHIVE` | 1937–1950 | English | Open Public | **P1** |
| `SRC-HIST-PRIVY-COUNCIL`| Judicial Committee of Privy Council | `HISTORICAL_DIGITAL_ARCHIVE` | 1836–1949 | English | Open Public | **P2** |

---

## 4. Truthfulness & Operational Principle

A registered URL does not imply exhaustive corpus holdings. LegalMitra strictly distinguishes between an institution that has been **catalogued and source-verified** and one that has been **comprehensively acquired**.
