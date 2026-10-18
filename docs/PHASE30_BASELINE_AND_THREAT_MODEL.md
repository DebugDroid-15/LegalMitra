# Phase 30: Baseline and Security Threat Model Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 30  

---

## 1. Executive Summary & Verification Mandate

This report establishes the baseline security posture of LegalMitra at commit `ffb6363` and documents a comprehensive, implementation-focused threat model. Phase 30 systematically evaluates realistic attack vectors across the web application, REST APIs, session management, RAG pipeline, knowledge base, source acquisition, and advocate-review operations.

---

## 2. Baseline Checkout & Integrity Verification

- **Workspace:** `C:\PROJECTS\LegalMitra`
- **Repository:** `https://github.com/DebugDroid-15/LegalMitra`
- **Starting Commit:** `ffb6363` (`Phase 29: national legal coverage expansion, high court precedent intelligence & source provenance automation (100% pass rate, Gate GO)`)
- **Git Branch:** `main` (verified clean working tree)
- **Remote:** `origin` (`https://github.com/DebugDroid-15/LegalMitra.git`)

### Governance Baseline Execution:
1. `python scripts/verify_freeze.py`:
   - All 6 Phase 9 frozen snapshot artifacts verified 100% bitwise identical (`Exit Code 0`).
   - Zero references to quarantined scaffold `IND-JUD-DEL-2024-BAIL`.
2. `python scripts/verify_review_packages.py`:
   - Package A and Package B verified 100% (`Exit Code 0`).
   - Exactly 40 records preserved in `pending_legal_review` status. Zero automated self-approvals.
3. `pytest -m "not live"`:
   - 262/262 passed, 2 deselected in 24.93s (`Exit Code 0`).
4. Benchmark v7 Reproduction:
   - 80/80 passed (100.00%), Manifest SHA256 verified, Gate: GO.

---

## 3. Threat Model & Trust Boundaries

LegalMitra enforces strict trust boundaries separating untrusted client inputs, external source URLs, verified knowledge storage, and internal application state:

```
[ External User / Client ] 
           │ (Untrusted HTTP / Cookies / Headers)
           ▼
[ FastAPI App Boundary ] ──(Rate Limit / Max 64KB Body / Security Headers)
           │
           ├──> [ ConversationStore (conversations.db) ] (Session Isolation)
           │
           ▼
[ LegalRAGEngine ] ──(Adversarial Filters / Privacy Redaction / Re-ranking)
           │
           ▼
[ LegalKnowledgeBase (legalmitra_kb.db) ] ──(Parameterized SQL / Scaffold Quarantine)
           ▲
           │
[ LegislationAcquisitionManager ] ──(Outbound URL SSRF Validator / Zero-Byte Quarantine)
```

### Threat Matrix:
1. **Anonymous External Users:** May attempt denial-of-service via oversized payloads or rate exhaustion. *Control:* 64KB body capping middleware, sliding-window in-memory rate limiter (30 req/min).
2. **Cross-Session Conversation Snooping:** User B attempts to view or overwrite User A's private legal consultation. *Control:* Session-scoped cryptographic token cookie (`legalmitra_session`), strict ownership validation in `ConversationStore` returning 404/403.
3. **Server-Side Request Forgery (SSRF):** Attacker injects loopback (`127.0.0.1`), cloud metadata (`169.254.169.254`), or private subnet URLs into acquisition pipelines. *Control:* `validate_outbound_legal_url` enforcing scheme and IP subnet blocks.
4. **Prompt Injection in Legal Queries:** Malicious prompt attempting to override system instructions or dump credentials. *Control:* Pre-retrieval pattern interceptor in `LegalRAGEngine` returning instant refusal.
5. **Sensitive Personal & Child Data Exfiltration:** Query requesting POCSO minor victim names or investigator contact details. *Control:* Pre-retrieval privacy filters checking POCSO and personal PII keywords, returning statutory refusal.
6. **Privilege Escalation in Review Workflow:** Unauthorized user attempting to approve review candidates. *Control:* Role-based permissions matrix `ROLE_PERMISSIONS` strictly barring non-advocates from approval actions.
