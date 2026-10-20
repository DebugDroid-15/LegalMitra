# PHASE 54: POINT-IN-TIME STATUTORY APPLICABILITY RESOLUTION

**Project:** LegalMitra  
**Component:** `legalmitra.temporal.engine`  
**Phase:** 54  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Purpose & Core Doctrine

In Indian jurisprudence, determining the operative law requires identifying which version of a statutory provision was in force on the legally relevant date (date of cause of action, contract execution, commission of offence, or petition filing).

Phase 54 introduces `StatutoryApplicabilityState` and the deterministic resolution engine `resolve_point_in_time_applicability()`, enforcing boundary semantics, amendment transitions, and savings clause preservation.

---

## 2. Seven-Outcome Applicability State Taxonomy

The engine resolves statutory queries into seven mutually exclusive states:

| Applicability State | Definition & Legal Significance |
|---|---|
| `CONFIRMED_APPLICABLE` | A verified provision version was in force on the query date with unambiguous commencement. |
| `CONFIRMED_HISTORICAL` | The provision was in force at a past date but has since been amended, replaced, or repealed. |
| `NOT_YET_IN_FORCE` | The statute has received Presidential assent but the provision remains unnotified/uncommenced. |
| `SUPERSEDED_OR_REPEALED` | The provision was repealed by subsequent legislation or struck down by constitutional court. |
| `PARTIALLY_COMMENCED` | Enactment with phased notification where specific sub-clauses or sections are pending. |
| `CONFLICTING_TEMPORAL_EVIDENCE` | Multiple authentic gazette notifications or transition orders report contradictory effective dates. |
| `INSUFFICIENT_EVIDENCE` | Gazette notifications or version intervals are missing or unverified. |

---

## 3. Boundary Semantics & Interval Mathematics

Version intervals are modeled as half-open / inclusive intervals: `[effective_from, effective_until]`.
- Where `effective_until` is specified (e.g. `2005-09-08` for Hindu Succession Act Sec. 6 Version 1), a query date on or before that date (`2005-09-08`) resolves to Version 1 (`CONFIRMED_APPLICABLE` or `CONFIRMED_HISTORICAL`).
- A query date after that date (`2005-09-09`) resolves to Version 2 (2005 Amendment Act No. 39 of 2005).

### Landmark Exemplars Verified:
1. **Digital Personal Data Protection Act, 2023 (`DPDP-SEC-1`)**:
   - Status on 2024-01-01: `NOT_YET_IN_FORCE` (Section 1(2) phased notification clause).
2. **Information Technology Act, 2000 (`IT-SEC-66A`)**:
   - Status on 2012-06-20: `CONFIRMED_HISTORICAL` (In force prior to judgment).
   - Status on 2015-03-25 onwards: `SUPERSEDED_OR_REPEALED` (Struck down in *Shreya Singhal v. Union of India*, AIR 2015 SC 1523).
3. **Hindu Succession Act, 1956 (`HSA-SEC-6`)**:
   - Pre-2005 Amendment (query date 2000-01-01): Version 1 resolved as `CONFIRMED_HISTORICAL`.
   - Post-2005 Amendment (query date 2021-01-01): Version 2 coparcenary rights (*Vineeta Sharma v. Rakesh Sharma*) resolved as `CONFIRMED_APPLICABLE`.
