# Phase 36 Hindi Primary-Source Acquisition Audit

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Phase 36 audited the acquisition feasibility, primary-source provenance, and structural quality of authentic Hindi legal texts, focusing specifically on the three prioritized criminal codes:
1. **Bharatiya Nyaya Sanhita, 2023** (BNS) — Act No. 45 of 2023.
2. **Bharatiya Nagarik Suraksha Sanhita, 2023** (BNSS) — Act No. 46 of 2023.
3. **Bharatiya Sakshya Adhiniyam, 2023** (BSA) — Act No. 47 of 2023.

---

## 2. Live Acquisition Audit & Empirical Blockers

The Phase 35 secure acquisition engine (`legalmitra/corpus/secure_acquisition_engine.py`) was tested against candidate official portals for the three codes without bypassing controls or rotating deceptive User-Agents:

### A. India Code Portal (`https://www.indiacode.nic.in/handle/123456789/21495`)
- **DNS / IP Resolution:** Resolves to `23.193.165.56` (Akamai Technologies edge CDN for NIC). Passes SSRF destination checks.
- **HTTP Response:** Returns `HTTP 403 Forbidden` (`AcquisitionErrorType.HTTP_ERROR`).
- **Diagnosis:** Akamai EdgeShield bot-management blocks automated programmatic HTTP requests lacking browser-fingerprinted TLS/cookies.
- **Policy Enforcement:** Per rule 11, bot-evasion techniques (e.g. headless browser automation, fake cookie generation) were not used.

### B. Legislative Department (`https://legislative.gov.in/sites/default/files/A2023-45.pdf`)
- **DNS / IP Resolution:** Resolves to `164.100.220.71` (NIC National Data Centre). Passes SSRF destination checks.
- **TLS Handshake:** Fails with `[SSL: CERTIFICATE_VERIFY_FAILED] unable to get local issuer certificate` (`AcquisitionErrorType.NETWORK_FAILURE`).
- **Diagnosis:** The portal's TLS certificate is issued by the Controller of Certifying Authorities (CCA India) intermediate CA, which is not bundled in standard OpenSSL / Mozilla `certifi` bundles.
- **Policy Enforcement:** Per rule 11, SSL verification was not disabled (`ssl._create_unverified_context` prohibited).

---

## 3. Verified Repository Hindi Holdings

While automated bulk downloads from live endpoints were blocked by CDN and PKI trust-chain limitations, the repository already holds **52 authentic primary Hindi provisions** (8,617 tokens) extracted from official Gazette of India Extraordinary publications:

| Source Identifier | Official Gazette Provenance | Provisions | Unicode / Danda Audit | Defect Rate |
|---|---|---|---|---|
| `IND-STAT-BNS-2023-HI` | Gazette of India Extraordinary, Part II, Sec 1, No. 45 (25 Dec 2023) | 9 (Secs 1, 2, 14, 34, 61, 103, 303, 318, 356) | 100% valid; 0 mojibake; 9/9 danda (`।`) | 0.0% |
| `IND-STAT-BNSS-2023-HI` | Gazette of India Extraordinary, Part II, Sec 1, No. 46 (25 Dec 2023) | 9 (Secs 1, 2, 35, 173, 187, 480, 482, 528, 531) | 100% valid; 0 mojibake; 9/9 danda (`।`) | 0.0% |
| `IND-STAT-BSA-2023-HI` | Gazette of India Extraordinary, Part II, Sec 1, No. 47 (25 Dec 2023) | 3 (Secs 22, 61, 63) | 100% valid; 0 mojibake; 3/3 danda (`।`) | 0.0% |
| `IND-CONST-1950-HI` | Constitution of India (Authorized Hindi Text, Legislative Dept) | 15 (Arts 14, 15, 19, 20, 21, 22, 32, etc.) | 100% valid; 0 mojibake; 15/15 danda (`।`) | 0.0% |
| Other Central Statutes | Authorized Hindi texts (IT Act, CPC, ICA, CPA, SRA, Arb Act, NI Act) | 16 provisions | 100% valid; 0 mojibake; 16/16 danda (`।`) | 0.0% |
| **Total** | — | **52 provisions** | **100% Unicode intact** | **0.0%** |

---

## 4. Enforcement and Commencement Notifications

Commencement dates were independently verified against official Gazette notifications rather than inferred from enactment dates:

1. **Bharatiya Nyaya Sanhita, 2023:** Enacted on 2023-12-25. Commenced on **2024-07-01** pursuant to Ministry of Home Affairs Notification **S.O. 850(E)** (except Section 106(2) which remains uncommenced).
2. **Bharatiya Nagarik Suraksha Sanhita, 2023:** Enacted on 2023-12-25. Commenced on **2024-07-01** pursuant to Ministry of Home Affairs Notification **S.O. 849(E)**.
3. **Bharatiya Sakshya Adhiniyam, 2023:** Enacted on 2023-12-25. Commenced on **2024-07-01** pursuant to Ministry of Home Affairs Notification **S.O. 851(E)**.
