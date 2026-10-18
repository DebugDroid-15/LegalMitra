# LegalMitra — Phase 38: Security, Privacy & Restricted Records Governance

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the privacy safeguards, statutory publication bars, and anonymization pipelines implemented in LegalMitra Phase 38. Operating an artificial intelligence system on judicial records requires active compliance with Indian privacy statutes, criminal codes protecting victims, juvenile justice protections, family law in-camera requirements, and national security restrictions.

Implemented in `legalmitra/judicial/restricted_records.py` and exported to `data/21_judicial_infrastructure/restricted_records_policy.json`.

---

## 2. Mandatory Statutory Publication Bars

### 2.1 Section 228A IPC / Section 72 Bharatiya Nyaya Sanhita (BNS) 2023
- **Statutory Mandate:** Absolute criminal bar on printing or publishing the name or any matter which may make known the identity of any person against whom an offence under Section 376, 376A, 376AB, 376B, 376C, 376D, 376DA, 376DB, or 376E IPC (or corresponding sections of BNS) is alleged or found to have been committed.
- **Punishment:** Imprisonment up to two years and fine.
- **Enforcement in LegalMitra:** Automatic token masking of survivor names and identifying references with `[VICTIM_ANONYMIZED]`.

### 2.2 Section 74 of the POCSO Act, 2012
- **Statutory Mandate:** No report in any newspaper, magazine, news-sheet or audio-visual media or other form of communication shall disclose the name, address, photograph, family details, school, neighbourhood or any other particulars which may lead to the identification of a child victim.
- **Enforcement in LegalMitra:** Any text matching POCSO indicators undergoes immediate deep anonymization, replacing identifying details with `[CHILD_VICTIM_ANONYMIZED]`.

### 2.3 Section 74 of the Juvenile Justice Act, 2015
- **Statutory Mandate:** Strict prohibition on disclosure of identity of children in conflict with law or children in need of care and protection.
- **Enforcement in LegalMitra:** Identity masking enforced before document indexing.

### 2.4 Section 11 of the Family Courts Act, 1984
- **Statutory Mandate:** In-camera proceedings upon request of either party or court discretion; matrimonial disputes and custody determinations shielded from public exposure.
- **Enforcement in LegalMitra:** Marked `IN_CAMERA_SEALED_BARRED` and completely excluded from general knowledge base ingestion.

### 2.5 Official Secrets Act, 1923 & Military Defence Classifications
- **Statutory Mandate:** Classified operational, intelligence, or defence judicial matters.
- **Enforcement in LegalMitra:** Hard pipeline block (`NATIONAL_SECURITY_CLASSIFIED_BARRED`).

---

## 3. Database Isolation Invariant

In full compliance with foundational architectural constraints:
- **`data/legalmitra_kb.db`** (Knowledge Base): Contains only public, lawfully eligible, source-verified legal texts, statutes, and anonymized judgments.
- **`data/conversations.db`** (User Session Store): Contains user session queries and interaction logs.
- **Separation Verification:** Physical file separation and distinct connection pools ensure zero cross-contamination between user private data and knowledge embeddings.

---

## 4. Scaffold Synthetic Chunks Quarantine

The six synthetic scaffold chunks (`IND-JUD-DEL-2024-BAIL-0001` through `0006`) remain strictly quarantined and barred from production retrieval and pretraining datasets, preserving absolute corpus authenticity.
