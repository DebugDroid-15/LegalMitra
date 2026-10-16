# LEGALMITRA: SECURITY AUDIT & HARDENING REPORT

**Date:** 2026-10-16  
**Auditor:** Senior AI Systems & Security Reliability Engineer  
**Status:** **AUDITED, HARDENED & VERIFIED**  

---

## 1. Security Architecture & Threat Model

LegalMitra provides an Indian legal intelligence interface backed by a SQLite/FTS5 knowledge base and generative LLMs. The threat model focuses on:
1. **Confidentiality**: Preventing cross-client conversation enumeration and secret leakage.
2. **Integrity**: Protecting the immutable legal corpus (`data/legalmitra_kb.db`) from tampering or unverified injection.
3. **Availability**: Mitigating DoS attacks, request flooding, and payload exhaustion on expensive inference endpoints.

---

## 2. Implemented Security Controls

### 2.1 Session Isolation & Access Control
- **Cryptographic Session Tokens**: Every client receives a cryptographically secure, random 24-byte session token via `HttpOnly`, `SameSite=Lax` cookie (`legalmitra_session`) or header `X-Session-ID`.
- **Strict Conversation Scoping**: All listing queries (`GET /api/v1/conversations`) filter strictly by `WHERE session_id = ?`.
- **Ownership Verification on Access & Write**: `GET /api/v1/conversations/{conv_id}/messages` and `POST /api/v1/chat` verify that `session_id` matches the conversation's owner. If mismatched, a `404 Not Found` or `403 Forbidden` is returned, preventing ID guessing or enumeration attacks.
- **Controlled Deletion**: Clients can delete their own conversations via `DELETE /api/v1/conversations/{conv_id}`.

### 2.2 Payload & Rate Limiting
- **Request Size Limiting**: Enforced a strict 64 KB maximum payload limit on HTTP requests via middleware, rejecting oversized inputs with HTTP 413.
- **Sliding-Window Rate Limiting**: Added in-memory rate limiting (default 30 requests/minute per session/IP). Requests exceeding the threshold receive HTTP 429 without invoking downstream models.

### 2.3 CORS & Browser Security Headers
- **Restricted CORS**: Permissive wildcard `allow_origins=["*"]` was removed. Allowed origins are now strictly loaded from `ALLOWED_ORIGINS` (defaulting to local loopback origins).
- **Hardened HTTP Headers**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: camera=(), microphone=(), geolocation=()`
  - `Content-Security-Policy`: Restricts scripts, styles, fonts, and images to trusted CDNs (Tailwind, Google Fonts, Google User Content) and local origins.

### 2.4 Database & Credential Safety
- **Storage Isolation**: The legal knowledge base (`data/legalmitra_kb.db`) is strictly separated from user conversation storage (`data/conversations.db`).
- **Silent DB Creation Prevention**: LegalKnowledgeBase now supports `must_exist=True` checks to ensure a missing database triggers a startup crash rather than silently creating an empty database.
- **Git Exclusions**: Updated `.gitignore` to exclude `*.db`, `*.sqlite`, `logs/`, and `backups/`.

