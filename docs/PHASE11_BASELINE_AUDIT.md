# LEGALMITRA: PHASE 11A BASELINE AUDIT REPORT

**Date:** 2026-10-16  
**Auditor:** Senior AI Systems & Security Reliability Engineer  
**Project Directory:** `C:\PROJECTS\LegalMitra`  
**Git Branch:** `master`  

---

## 1. Executive Summary & Verification

An independent audit was conducted on the LegalMitra codebase following Phase 10 completion. The audit confirmed the presence of the Constitutional Modernism interface, SQLite knowledge base, RAG retrieval engine, FastAPI web application, and conversation store. However, several critical architectural, security, and session-isolation gaps were identified that must be hardened before staging deployment.

### Pilot Freeze & Baseline Verification
- **Frozen 20-Example Pilot**: Verified via `scripts/verify_freeze.py`. All 20 records in `data/03_generated/pilot_20_examples.jsonl`, `pilot_20_manifest.json`, `pilot_20_review_sheet.csv`, `pilot_20_source_bundle.json`, `pilot_20_open_issues.md`, and `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md` match their exact SHA-256 hashes.
- **Review Status**: All 20 examples remain strictly `pending_legal_review` with blank decision and score fields.
- **Quarantine Check**: Zero occurrences of `IND-JUD-DEL-2024-BAIL` in active retrieval or pilot datasets.
- **Baseline Test Suite**: 104 passed offline tests (pytest -m "not live").

---

## 2. Environment & Dependency Audit

- **Python Runtime**: Python 3.11.0 (64-bit on Windows)
- **Key Installed Packages**:
  - `fastapi` 0.115.6, `uvicorn` 0.34.0, `pydantic` 2.10.4, `starlette` 0.41.3
  - `sqlite3` (Python built-in SQLite 3.42.0 with FTS5 support)
  - `requests` 2.32.3, `python-dotenv` 1.0.1, `pytest` 7.4.3
- **Primary Data Stores**:
  - `data/legalmitra_kb.db`: 1,149 indexed statutory provisions and case law paragraphs.
  - `data/conversations.db`: SQLite database for user sessions, messages, and feedback.

---

## 3. Critical Security & Privacy Findings

### Finding 1: Lack of Client Session Isolation & Insecure Conversation Access
- **Defect**: In `legalmitra/web/app.py` and `store.py`, `GET /api/v1/conversations` returns **all** conversations globally across every visitor, and `GET /api/v1/conversations/{conv_id}/messages` allows arbitrary reading of any conversation without ownership verification.
- **Risk**: Serious privacy violation in multi-user/staging environments.
- **Required Fix**: Implement cryptographic session-cookie-based conversation ownership (`session_id`), scoped conversation listing, and ownership validation before returning message history. Add conversation deletion capability.

### Finding 2: Permissive Wildcard CORS Configuration
- **Defect**: In `legalmitra/web/app.py`, `CORSMiddleware` was initialized with `allow_origins=["*"]` and `allow_credentials=True`.
- **Risk**: Combining `allow_origins=["*"]` with `allow_credentials=True` is an invalid/insecure configuration that violates web security standards and browser CORS policies.
- **Required Fix**: Configure explicit, environment-driven allowed origins (defaulting to localhost/127.0.0.1 for local and staging).

### Finding 3: Missing Request Size & Rate Limiting Controls
- **Defect**: The POST `/api/v1/chat` endpoint does not enforce request rate limits or body size limits beyond Pydantic max_length. An attacker could flood the endpoint with concurrent queries, causing denial of service or exhausting provider tokens.
- **Required Fix**: Implement request size guards (max 64KB HTTP payload) and in-memory IP/session rate limiting (e.g. 20 requests/minute per session).

### Finding 4: Silent Knowledge Base Creation Risk
- **Defect**: In `legalmitra/knowledge/knowledge_base.py`, `__init__` automatically executes `CREATE TABLE IF NOT EXISTS` and creates an empty database if `data/legalmitra_kb.db` is missing or the path is misconfigured.
- **Risk**: A missing production database would silently degrade into an empty database without throwing an alarm.
- **Required Fix**: Add a `must_exist=True` check or verification that the legal chunks table contains verified data, raising a clear configuration exception on startup.

### Finding 5: Live API Dependency in Unit Tests
- **Defect**: `tests/test_web_api.py` invoked `client.post("/api/v1/chat")` which triggered live external calls to the NVIDIA NIM endpoint when an API key was present in the environment.
- **Risk**: Flaky tests, network delays (50-100s per test run), and credit consumption during routine testing.
- **Required Fix**: Mock the LLM provider in standard offline web API tests and provide dedicated `-m live` marks for external model verification.

---

## 4. Audit Plan & Next Actions

1. Implement session cookie handling and conversation ownership validation in `legalmitra/web/store.py` and `legalmitra/web/app.py`.
2. Add rate limiting, CORS restrictions, and request body size validation.
3. Enhance readiness vs. liveness endpoints (`/api/v1/health` and `/api/v1/ready`).
4. Update `.gitignore` and `.env.example` with strict placeholders and database rules.
5. Add unit and regression tests for session isolation, rate limiting, and failure modes.

