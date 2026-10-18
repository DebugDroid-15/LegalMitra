# Phase 30: API Security & Input Validation Audit
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 30  

---

## 1. Perimeter Controls & Middleware Architecture

The LegalMitra FastAPI web layer (`legalmitra/web/app.py`) applies automated defenses across all endpoints:
1. **Payload Size Enforcement:** `security_and_limit_middleware` inspects incoming `Content-Length` headers, rejecting payloads exceeding **64KB** with HTTP `413 Request Entity Too Large`.
2. **Sliding-Window Rate Limiting:** Limits clients to **30 requests per minute** keyed by `session_id:client_ip`, returning HTTP `429 Too Many Requests`.
3. **Hardened Security Headers:** Injected on every response:
   - `X-Frame-Options: DENY` (Anti-Clickjacking)
   - `X-Content-Type-Options: nosniff` (MIME-confusion defense)
   - `X-XSS-Protection: 1; mode=block`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Permissions-Policy: camera=(), microphone=(), geolocation=()`
   - `Content-Security-Policy: default-src 'self' ...`

---

## 2. Input Validation & SQL Injection Defenses

### Parameterized Database Access:
All queries across `LegalKnowledgeBase` and `ConversationStore` use SQLite parameter substitution (`?` positional parameters or `:key` named bindings). 

### FTS5 Query Sanitization:
The `_sanitize_fts_query` helper filters punctuation and control characters, converting queries into safe space-separated tokens before executing SQLite FTS5 `MATCH` queries.

### Empirical Attack Testing:
- Payload: `' OR '1'='1`
- Payload: `'; DROP TABLE legal_chunks; --`
- Payload: `' UNION SELECT * FROM sources --`
- **Result:** Fully parameterized; zero SQL errors, table drops, or unauthorized data exposures occurred.

---

## 3. Server-Side Request Forgery (SSRF) Protection

In Phase 30, the dedicated utility `legalmitra.core.security.validate_outbound_legal_url` was instituted and integrated into `LegislationAcquisitionManager`:
- Blocks non-HTTP/HTTPS schemes (e.g. `file://`, `gopher://`, `ftp://`).
- Blocks loopback IP literals (`127.0.0.1`, `::1`) and named aliases (`localhost`).
- Blocks private IPv4 blocks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
- Blocks cloud metadata IP addresses (`169.254.169.254`) and hostname aliases (`metadata.google.internal`).
- Automatically quarantines any acquired record with an invalid or prohibited destination.
