# LegalMitra — Phase 38: Lawful Source Acquisition & Provenance Architecture

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document delineates the legal basis, source provenance safeguards, and acquisition pipelines for judicial records in LegalMitra. All data acquisition strictly respects Section 52(1)(q) of the Indian Copyright Act 1957, court portal terms of service, robots.txt, and privacy redaction mandates.

---

## 2. Legal Foundations of Judicial Document Usability

### 2.1 Section 52(1)(q) of the Copyright Act, 1957
Under Indian copyright law, the following do not constitute copyright infringement:
> *"The reproduction or publication of—*  
> *(iv) any judgment or order of a court, tribunal or other judicial authority, unless the reproduction or publication of such judgment or order is prohibited by the court, the tribunal or other judicial authority, as the case may be."*

### 2.2 Proprietary Headnotes vs. Raw Judicial Text
- Commercial legal databases claim copyright exclusively in their headnotes, editorial summaries, catchwords, and formatting (*Eastern Book Company v. D.B. Modak* (2008) 1 SCC 1).
- Raw judgments, orders, statutes, and decrees are open public law records and cannot be monopolized.
- **LegalMitra Safeguard**: Ingestion pipelines strictly extract raw judicial texts from official court repositories (Supreme Court portal, eSCR, High Court portals, eCourts CIS). Editorial headnotes or commercial annotations from proprietary databases are never scraped or ingested.

---

## 3. Official Provenance Records

Every acquired judicial record stores an immutable provenance object containing:
- `source_url`: Exact official portal endpoint where the record was retrieved.
- `acquisition_timestamp`: ISO 8601 UTC timestamp of retrieval.
- `sha256_checksum`: Cryptographic hash of the raw document file.
- `court_tier`: Tier of the issuing institution.
- `digital_signature_present`: Boolean indicating whether the downloaded PDF carries an e-Court or judge cryptographic signature.
- `redaction_audit_passed`: Boolean verifying that Section 228A IPC / Section 74 POCSO checks have been satisfied.
