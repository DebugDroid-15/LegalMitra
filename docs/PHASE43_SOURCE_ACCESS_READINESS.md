# LegalMitra Phase 43 — Source-Access Readiness & Connector Authorization Roadmap

**Date:** October 19, 2026  
**Auditor:** Regulatory Compliance & Security Architecture Lead  

---

## 1. Investigation of Outstanding Phase 42 Blockers

Phase 42 identified two foundational access blockers that protect LegalMitra from violating third-party access controls:
1. `BLOCKED_PENDING_ECOMMITTEE_CREDENTIALS` (eCourts Services)
2. `LIVE_PERMISSION_UNVERIFIED` (Delhi & Bombay High Courts)

Phase 43 investigated the precise technical and institutional prerequisites required to resolve each blocker:

---

## 2. eCourts CIS Integration Prerequisites

| Dimension | Current Operational State | Authorized Live Transition Prerequisite |
|:---|:---|:---|
| **Authentication Header** | Empty environment variables | `ECOURTS_API_TOKEN` (Bearer $\ge 16$ chars) & `ECOURTS_CLIENT_ID` |
| **Institutional Agreement** | None | Executed Memorandum of Understanding (MOU) with Supreme Court eCommittee |
| **Endpoint Access** | Offline staging fallback active | Whitelisted IP access to `https://api.ecommitteesci.gov.in/v1/` |
| **CAPTCHA Policy** | **Strict Zero-Bypass** | Maintained permanently. Direct scraping of web forms prohibited. |
| **Interim Fallback** | `AuthorizedECourtsAdapter.ingest_staging_dump()` | Continues as primary production mode for local batch data. |

---

## 3. High Court Live Connector Pilot: Bounded Execution Plan

To execute live acquisition when permissions are granted, LegalMitra has documented a 10-point Bounded Live-Pilot Plan:

1. **Authorization Evidence:** Written permission letter from Registrar General citing academic/research exemption.
2. **Permitted Endpoints:** Strictly limited to judgment search APIs on `delhihighcourt.nic.in` and `bombayhighcourt.nic.in`.
3. **Approved Operating Window:** Off-peak judicial hours (01:00 to 05:00 IST).
4. **Rate Limit:** Strict token bucket at max 0.5 requests/second (30 req/minute).
5. **Request Budget:** Maximum bounded budget of 50 documents per court per pilot run.
6. **Timeout & Stop Conditions:** Connection timeout set to 15 seconds; pilot terminates immediately upon receiving HTTP 429, 403, or 503.
7. **SSRF & Redirect Safeguards:** `SafeRedirectHandler` re-validates every redirect hop against destination IP and domain allowlists.
8. **Cryptographic Ingestion:** Every acquired byte stream hashed via SHA-256 and checked for duplication before storage.
9. **Privacy Gating:** Automatic inspection by `RestrictedRecordsPolicyEngine` before indexing.
10. **Rollback & Incident Response:** Emergency kill-switch clears pending queues and restores local staging mode.
