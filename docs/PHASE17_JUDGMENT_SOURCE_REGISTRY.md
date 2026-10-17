# LEGALMITRA — PHASE 17B: OFFICIAL JUDGMENT SOURCE REGISTRY & DISCOVERY REPORT

**Workspace:** `c:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

Under Indian law, reproduction and publication of judgments delivered by the Supreme Court of India, High Courts, and judicial tribunals are protected under **Section 52(1)(q)(iv) of the Copyright Act, 1957**, which declares that the reproduction or publication of any judgment or order of any court, tribunal, or other judicial authority does not constitute an infringement of copyright.

In Phase 17B, LegalMitra formally established the **Judicial Source Registry** to govern authentic, compliant acquisition of court decisions.

The registry is formalized in `legalmitra/corpus/judicial_registry.py` and serialized to `data/08_corpus/judicial_repositories.json`.

---

## 2. Cataloged Authoritative Judicial Repositories

| Repository ID | Judicial Authority | Jurisdiction | Document Types | Primary Access Method | Licensing & Reproduction Basis | Rate Limit | Verification Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `REPO-SCI-DIGITAL-SCR` | Supreme Court of India | `IN` | SCR Judgments, Neutral Citations | `direct_http` | Section 52(1)(q)(iv) Copyright Act, 1957 | 20 req/min | `primary_official` |
| `REPO-SCI-PORTAL` | Supreme Court of India | `IN` | Daily Orders, Signed Judgments | `portal_search` | Official Judicial Record | 20 req/min | `primary_official` |
| `REPO-DHC-JUDGMENTS` | High Court of Delhi | `IN-DL` | Reportable Judgments, Neutral Citations | `direct_http` | Section 52(1)(q)(iv) Copyright Act, 1957 | 30 req/min | `primary_official` |
| `REPO-BOM-JUDGMENTS` | High Court of Bombay | `IN-MH` | Judgments, Full Bench Rulings | `portal_search` | Section 52(1)(q)(iv) Copyright Act, 1957 | 25 req/min | `primary_official` |
| `REPO-ECOURTS-NJDG` | e-Courts Mission Mode Project | `IN` | High Court & Subordinate Judgments | `portal_search` | e-Courts Open Data Framework | 15 req/min | `primary_official` |
| `REPO-KAR-JUDGMENTS` | High Court of Karnataka | `IN-KA` | Reportable Orders & Judgments | `portal_search` | Section 52(1)(q)(iv) Copyright Act, 1957 | 25 req/min | `primary_official` |
| `REPO-ALL-JUDGMENTS` | High Court of Judicature at Allahabad | `IN-UP` | Reportable & Full Bench Judgments | `portal_search` | Section 52(1)(q)(iv) Copyright Act, 1957 | 20 req/min | `primary_official` |

---

## 3. Compliance and Ethical Ingestion Protocol

1. **No Scraping Overload**: Respectful rate pacing (15-30 requests per minute max) with randomized delays.
2. **No CAPTCHA Circumvention**: Strict avoidance of unauthorized headless session cracking or anti-bot circumvention.
3. **Statutory Victim Privacy Redaction**: Mandatory automatic compliance with:
   - Section 33(7) of the POCSO Act, 2012 (strict prohibition on disclosing identity of child victims).
   - Section 74 of the Juvenile Justice (Care and Protection of Children) Act, 2015.
   - Section 72 of the Bharatiya Nyaya Sanhita, 2023 (disclosure of identity of victims of certain sexual offences).
4. **Distinction of Unmodified Court Text**: Verbatim text preserves raw judicial language, clearly segregated from AI-generated extractive summaries.

