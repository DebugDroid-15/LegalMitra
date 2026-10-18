# Phase 29: State Legislation Ingestion & Structured Modeling Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. Statutory Ingestion Architecture

LegalMitra ingests State and Central legislation using a strict hierarchical model that preserves the legislative draftsman's exact structure:
- **Level 1 (Act Title & Preamble):** Context, year, enactment date, territorial extent.
- **Level 2 (Chapters & Parts):** Broad thematic divisions.
- **Level 3 (Sections):** Core operative statutory unit.
- **Level 4 (Subsections & Clauses):** Subordinate conditions and qualifications.
- **Level 5 (Provisos & Explanations):** Exceptions, limitations, and statutory clarifications.

---

## 2. Ingested State Legislation Core Slices

### 1. National Capital Territory of Delhi (`IN-DL`)
- **Delhi Rent Control Act, 1958 (`IND-DL-STAT-DRC-1958`):**
  - Ingested provisions: Section 2 (Definitions of landlord, tenant, premises), Section 3 (Exemptions), Section 14 (Protection against eviction), Section 25B (Summary procedure for bona fide need).
  - Effective date: 1959-02-09.
  - Judicial interpretation linkage: Supreme Court ruling in *Satyawati Sharma (Dead) by LRs v. Union of India* (2008), striking down Section 14(1)(e)'s restriction to residential premises.
- **Delhi Police Act, 1978 (`IND-DL-STAT-DPA-1978`):**
  - Ingested provisions: Section 28 (Regulations for traffic and order), Section 53 (Externment of offenders), Section 65 (Duty to comply with police directions).
  - Effective date: 1978-07-01.

### 2. State of Maharashtra (`IN-MH`)
- **Maharashtra Rent Control Act, 1999 (`IND-MH-STAT-MRC-1999`):**
  - Ingested provisions: Section 3 (Exemptions), Section 7 (Definitions), Section 15 (Bar on ejectment if tenant pays rent; mandatory 90-day notice requirement), Section 16 (Grounds for eviction), Section 24 (Recovery of premises given on licence).
  - Effective date: 2000-03-31 (Maharashtra Gazette Extraordinary).
- **Maharashtra Police Act, 1951 (`IND-MH-STAT-MPA-1951`):**
  - Ingested provisions: Section 33 (Traffic and public order rules), Section 56 (Removal of persons about to commit offences), Section 57 (Removal of convicted offenders).
  - Effective date: 1951-06-11.

---

## 3. Provenance & Gazette Verification Standards

Every state statutory chunk in `legal_chunks` is stamped with:
1. `source_id`: Canonical document identifier.
2. `jurisdiction`: Explicit ISO sub-tag (`IN-DL`, `IN-MH`).
3. `effective_date`: Authentic gazette commencement date.
4. `authority_level`: Set strictly to `binding_statute`.
5. `is_historical`: Flag indicating whether provision is superseded.
6. `is_synthetic_scaffold`: Confirmed `0`.
