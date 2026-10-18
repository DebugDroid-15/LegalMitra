# LegalMitra Phase 37 — Authorized Source Access Protocol & Portal Audit

**Phase:** 37  
**Timestamp:** 2026-10-18T23:19:00Z  
**Branch:** `main`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Status:** VERIFIED & AUDITED

---

## 1. Executive Summary

Phase 37 establishes the operational protocol for lawful, authorized acquisition of primary legal sources in India. Under Mandatory Rule 12 and Section 52(1)(q) of the Indian Copyright Act, 1957, LegalMitra enforces strict technical, cryptographic, and legal safeguards during all source ingestion activities. 

Specifically, the system prohibits:
1. Bypassing TLS/SSL certificate verification (`ssl._create_unverified_context` or `verify=False`).
2. Evading CDN bot protections through deceptive User-Agents, header spoofing, or headless browser session theft.
3. Ingesting private editorial enhancements (commercial headnotes, commentary, proprietary annotations).

---

## 2. Portal Accessibility Audit & Security Findings

During Phase 36 and Phase 37, programmatic access was systematically probed across major official legal portals using `SecureAcquisitionEngine` (`legalmitra/corpus/secure_acquisition_engine.py`):

| Target Portal | Official Entity | Resolved IP / CDN | Network / Security Response | Diagnosis & Policy Compliance |
| :--- | :--- | :--- | :--- | :--- |
| `https://www.indiacode.nic.in` | Ministry of Law & Justice / NIC | `23.193.165.56` (Akamai CDN) | `HTTP 403 Forbidden` (`AcquisitionErrorType.HTTP_ERROR`) | Akamai EdgeShield bot management restricts automated programmatic HTTP requests. Per project rules, bot evasion is strictly prohibited; no bypass attempted. |
| `https://legislative.gov.in` | Legislative Department / NIC | `164.100.220.71` (NIC Data Centre) | `[SSL: CERTIFICATE_VERIFY_FAILED]` (`AcquisitionErrorType.NETWORK_FAILURE`) | Root certificate is signed by CCA India intermediate CA, not included in Mozilla/OpenSSL `certifi` bundle. SSL verification is never disabled. |
| `https://egazette.gov.in` | Directorate of Printing, GoI | `164.100.153.22` (NIC Web Server) | `HTTP 200 OK` (when valid cert chain presented) | Primary authoritative publisher for Gazette Extraordinary notifications and statutory acts under Section 52(1)(q). |
| `https://delhihighcourt.nic.in` | Delhi High Court IT Cell | `164.100.208.5` (NIC Server) | `HTTP 200 OK` (direct public rule documents) | Public repository for Delhi High Court procedural rules and practice directions. |
| `https://bombayhighcourt.nic.in` | Bombay High Court CIS | `164.100.112.18` (NIC Server) | `HTTP 200 OK` (certified public judgments) | Public domain judicial orders; bare text exempt under Section 52(1)(q)(iv). |

---

## 3. Lawful & Authorized Ingestion Architecture

Because live scraping against CDN-protected endpoints is both technically fragile and ethically impermissible, LegalMitra operates an **Authorized Offline/Mirror Ingestion Architecture**:

```
+-----------------------------------------------------------------------------------------+
|                               OFFICIAL PRIMARY SOURCE                                   |
| (Gazette of India Extraordinary / Legislative Dept Acts / High Court Certified Records) |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
|                             AUTHORIZED ACQUISITION HUB                                  |
| - Verifies Official Gazette Notification Number (e.g. No. 45 of 2023, S.O. 850(E))      |
| - Validates Authority Level (Central Statute, High Court Order, Delegated Rule)         |
| - Strips commercial/editorial commentary, preserving 100% bare legislative text         |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
|                             CRYPTOGRAPHIC VERIFICATION                                  |
| - SHA-256 Digest Computation                                                            |
| - SSRF URL & Domain Validation (`validate_outbound_legal_url`)                           |
| - Atomic Staging into `data/09_national_corpus/raw_sources/` & Acquired Datasets        |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
|                             PARSER & QUALITY ENGINE                                     |
| - Devanagari Unicode Normalization (U+0900 to U+097F)                                   |
| - Danda (`।`) and Double Danda (`॥`) Structural Preservation                           |
| - Zero Replacement Characters (`\ufffd`) & Zero Mojibake Validation                     |
+-----------------------------------------------------------------------------------------+
```

---

## 4. Rights Exemption Boundaries under Section 52(1)(q)

All acquired records are audited against the four statutory limbs of Section 52(1)(q) of the Indian Copyright Act, 1957:
1. **Clause 52(1)(q)(i):** The reproduction or publication of any matter which has been published in any Official Gazette.
2. **Clause 52(1)(q)(ii):** The reproduction or publication of any Act of a Legislature.
3. **Clause 52(1)(q)(iii):** The reproduction or publication of any report of any committee appointed by the Government.
4. **Clause 52(1)(q)(iv):** The reproduction or publication of any judgment or order of a court, tribunal or other judicial authority.

Editorial commentary, headnotes, case digests, and proprietary taxonomies from private publishers (*Eastern Book Company v. D.B. Modak*) are strictly barred from the acquisition pipeline.

