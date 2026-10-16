# LEGALMITRA: STAGING READINESS & PRE-DEPLOYMENT CHECKLIST

**Date:** 2026-10-16  
**Target Environment:** Staging  
**Application Version:** 1.1.0  

---

## 1. Security & Configuration Verification

- [x] **No Plaintext Secrets in Codebase**: Verified that `git status` shows no committed `.env` files or API keys.
- [x] **Environment Template Complete**: `.env.example` provides explicit placeholders for `NEMOTRON_API_KEY`, `ALLOWED_ORIGINS`, `RATE_LIMIT_PER_MINUTE`, and storage paths.
- [x] **Restricted CORS**: `CORSMiddleware` configured with explicit allowed origins; wildcard `*` with credentials removed.
- [x] **Security Headers Active**: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy` verified via HTTP responses.
- [x] **Session Isolation Active**: Cryptographic session cookies (`legalmitra_session`) and `X-Session-ID` isolation tested. Cross-session conversation access returns HTTP 404/403.
- [x] **Payload Size Limits Active**: 64 KB maximum HTTP request body enforced.
- [x] **Rate Limiting Active**: 30 requests/minute per session/IP enforced with HTTP 429 response.

---

## 2. Legal Integrity & Safeguards Verification

- [x] **Frozen Pilot Preserved**: `scripts/verify_freeze.py` executed; all 6 Phase 9 review snapshot artifacts verified against original SHA-256 hashes.
- [x] **Status Integrity**: All 20 pilot examples remain strictly `pending_legal_review` with blank decision and score fields.
- [x] **Quarantine Enforcement**: Zero occurrences of `IND-JUD-DEL-2024-BAIL` in active retrieval or pilot datasets.
- [x] **Readiness Probe**: `/api/v1/ready` validates knowledge base connectivity and chunk count before accepting query traffic.
- [x] **Silent Creation Guard**: `LegalKnowledgeBase` raises `FileNotFoundError` if `must_exist=True` and database is missing.

---

## 3. Test Coverage Summary

- [x] **Offline Test Suite**: `python -m pytest -m "not live"` — **104 passed**
- [x] **Hardened Web API Suite**: `python -m pytest tests/test_web_api.py` — **10 passed**
- [x] **Total Passing Tests**: **114 passed**
- [x] **Zero Regressions**: No existing functionality compromised.

