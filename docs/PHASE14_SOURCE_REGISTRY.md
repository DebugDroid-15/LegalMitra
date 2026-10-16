# LegalMitra Official Source Discovery and Repository Registry

**Specification Document — Phase 14C**  
**Version:** 1.0.0  
**Machine-Readable Target:** `data/08_corpus/source_repositories.json`  
**Engine Implementation:** `legalmitra/corpus/discovery.py`  
**Classification:** Official Ingestion Endpoints, Access Policies & Verification Rules

---

## 1. Statutory Mandate & Legal Authority for Ingestion

LegalMitra ingests exclusively from official public government and judicial portals in compliance with Indian intellectual property law:
1. **Section 52(1)(q) of the Copyright Act, 1957:** Explicitly declares that the reproduction or publication of any Act of a Legislature, any statutory rule or order, and any judgment or order of a court, tribunal, or other judicial authority does not constitute an infringement of copyright.
2. **Government Open Data License (GODL-India):** Permits the use, adaptation, and sharing of government publications released into the public domain.

No copyrighted proprietary headnotes, commercial editorial commentary, or private database extracts are scraped or ingested into LegalMitra.

---

## 2. Catalog of Official Repositories

| Repository ID | Official Name | Issuing Authority | Verification Tier | Rate Limit | Supported Documents |
|---|---|---|:---:|:---:|---|
| `REPO-INDIA-CODE` | India Code Digital Repository | Legislative Dept, Ministry of Law and Justice | `primary_official` | 30/min | Central Acts, State Acts, Amendments, Schedules |
| `REPO-EGAZETTE` | e-Gazette of India | Directorate of Printing, MoHUA | `primary_official` | 20/min | Assents, Statutory Orders (S.O.), Commencement Notifications |
| `REPO-SCI-JUDGMENTS` | SCI Official Judgments Portal | Supreme Court of India | `primary_official` | 20/min | Reportable Judgments, Constitution Bench Rulings, Neutral Citations |
| `REPO-SCI-RULES` | SCI Rules & Practice Manuals | Supreme Court of India | `primary_official` | 30/min | Supreme Court Rules 2013, Circulars, Office Manuals |
| `REPO-MEITY` | MeitY Cyber Laws Repository | Ministry of Electronics and IT | `regulatory_official` | 40/min | IT Act 2000, IT Rules 2021, DPDP Rules & Guidance |
| `REPO-MCA` | MCA Corporate Law Portal | Ministry of Corporate Affairs | `regulatory_official` | 30/min | Companies Act 2013, Decriminalization Circulars, NCLT Rules |
| `REPO-MHA` | MHA Criminal Law Reforms Portal | Ministry of Home Affairs | `regulatory_official` | 30/min | BNS, BNSS, BSA Commencement Notifications & SOPs |
| `REPO-LAW-COMMISSION` | Law Commission of India Reports | Law Commission, Min. of Law & Justice | `academic_public` | 25/min | Commission Reports 1 to 289 (Legislative Intent) |
| `REPO-NGT` | National Green Tribunal Portal | National Green Tribunal | `regulatory_official` | 25/min | Environmental Rulings, EIA Orders, Pollution Directives |
| `REPO-DHC` | Delhi High Court Judgments Portal | High Court of Delhi | `state_official` | 30/min | High Court Judgments, Practice Directions |

---

## 3. Ingestion Policies & Access Guardrails

### 3.1 Rate Limiting & Controlled Retrieval
- All discovery agents and download scripts strictly enforce per-minute request caps (20-40 req/min) to prevent service degradation on public government servers.
- Exponential backoff with jitter is applied upon encountering HTTP 429 (Too Many Requests) or 503 (Service Unavailable).

### 3.2 Resumable Downloads & Cryptographic Checksumming
- Every downloaded document is saved with its source timestamp and immediate SHA-256 calculation.
- If a download is interrupted, partial byte chunks are checked against the server's `Content-Length` header; corrupt files are immediately quarantined.

### 3.3 Known Source Limitations & Compensating Controls
- **India Code PDF Formatting:** Older consolidated acts may have complex multi-column layouts; Docling structural parsing is supplemented by regex section boundary verifiers.
- **e-Gazette Scanned Images:** Historical notifications prior to 2015 often consist of scanned bitmaps requiring OCR and manual validation flags.
- **Supreme Court Large Manuals:** Practice manuals exceeding 15 pages are partitioned into structured sub-chapters prior to Docling extraction to respect memory boundaries.

