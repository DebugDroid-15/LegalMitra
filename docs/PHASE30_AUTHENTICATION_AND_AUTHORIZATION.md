# Phase 30: Authentication, Authorization and Session Isolation Audit
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 30  

---

## 1. Authentication & Session Architecture

LegalMitra implements stateless, cookie-based session isolation via the `legalmitra_session` cookie:
- **Entropy & Generation:** Generated using Python `secrets.token_urlsafe(24)`, providing 192 bits of cryptographic entropy.
- **Cookie Security Flags:**
  - `HttpOnly`: Enforced (`True`), preventing client-side JavaScript access and XSS token exfiltration.
  - `SameSite`: Set to `lax` to mitigate cross-site request forgery (CSRF).
  - `Secure`: Dynamically toggled via `IS_PRODUCTION` (`True` in production deployments).
  - `Max-Age`: 30 days (86,400 * 30 seconds).

---

## 2. Object-Level Authorization & Cross-Session Protection

All conversational endpoints (`/api/v1/conversations`, `/api/v1/conversations/{conv_id}/messages`, `/api/v1/conversations/{conv_id}`) enforce strict ownership:
- **Read Isolation:** When User B requests `/api/v1/conversations/{conv_id}/messages` owned by User A, the system queries `conversations WHERE conversation_id = ? AND session_id = ?`. If `session_id != owner`, access is denied returning HTTP `404 Not Found` (preventing ID enumeration).
- **Write Isolation:** Submitting a chat query with an existing `conversation_id` validates `get_conversation_owner(conv_id)`. If mismatched, HTTP `403 Forbidden` is returned immediately.
- **Delete Isolation:** Deleting a thread validates ownership, returning HTTP `404 Not Found` if attempted by an unauthorized session.

### Empirical Test Evidence:
- Verified via `test_cross_user_session_isolation`: User B attempting to read, write, or delete User A's thread resulted in `404`, `403`, and `404` status codes respectively. Zero conversational leakage observed.

---

## 3. Review Role Privilege Boundaries

The advocate-review subsystem (`legalmitra/review/workflow.py`) enforces strict separation between advocate evaluators and administrative roles:

| User Role | Permitted Actions | Blocked Actions |
|---|---|---|
| `ADVOCATE_REVIEWER` | `START_REVIEW`, `SUBMIT_DECISION`, `APPROVE`, `REJECT`, `REQUEST_REVISION`, `ABSTAIN` | `EXPORT_PACKAGE`, `IMPORT_PACKAGE` |
| `SENIOR_ADVOCATE` | `START_REVIEW`, `SUBMIT_DECISION`, `APPROVE`, `REJECT`, `REQUEST_REVISION`, `ABSTAIN`, `DISPUTE` | `EXPORT_PACKAGE`, `IMPORT_PACKAGE` |
| `LEGAL_RESEARCHER` | `EXPORT_PACKAGE` | `APPROVE`, `REJECT`, `SUBMIT_DECISION`, `IMPORT_PACKAGE` |
| `AUDITOR` | `DISPUTE`, `EXPORT_PACKAGE`, `IMPORT_PACKAGE` | `APPROVE`, `REJECT`, `SUBMIT_DECISION` |
| `SYSTEM_ADMIN` | `EXPORT_PACKAGE`, `IMPORT_PACKAGE` | `APPROVE`, `REJECT`, `SUBMIT_DECISION` |

**Invariant:** System Administrators, Auditors, and Researchers cannot approve review records; approval authority is strictly reserved for verified Advocates with valid Bar Council credentials.
