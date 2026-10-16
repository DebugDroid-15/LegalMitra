# LEGALMITRA: PRIVACY AND DATA RETENTION POLICY

**Date:** 2026-10-16  
**Document Classification:** Operations & User Privacy  
**Applies to:** LegalMitra Local & Staging Deployments  

---

## 1. Principles & Trust Boundary

1. **No Compulsory User Accounts**: LegalMitra operates on an anonymous, session-isolated basis. Users are not required to provide personal identifying information (PII), email addresses, or phone numbers to query legal provisions.
2. **Session Ownership & Data Isolation**:
   - Each browser session is assigned an opaque random identifier (`session_id`).
   - Conversations and user queries are accessible strictly by the browser session that created them.
   - Cross-client enumeration or inspection of other users' conversation histories is blocked at the database query level.
3. **Separation from Statutory Corpus**:
   - User conversations are stored in `data/conversations.db`.
   - The verified Indian legal knowledge base (`data/legalmitra_kb.db`) is read-only during normal inference and is never modified by user activity.

---

## 2. Retention Periods & Storage Locations

| Data Category | Storage Location | Retention Period | Deletion Path |
|:---|:---|:---|:---|
| **User Queries & Answers** | `data/conversations.db` | Retained locally for up to 30 days unless deleted by user. | `DELETE /api/v1/conversations/{id}` |
| **User Precision Feedback** | `data/conversations.db` | Retained for quality evaluation. | Associated with session ID. |
| **Server Diagnostics & Logs** | Local console / log files | Error messages only; sanitized of full query text and credentials. | Rotated daily; 14-day retention. |
| **Legal Knowledge Base** | `data/legalmitra_kb.db` | Permanent, immutable reference corpus. | Managed via formal source acquisition. |

---

## 3. Disclaimers Regarding Encryption at Rest

- In the current SQLite architecture, `data/conversations.db` is stored unencrypted on the host filesystem.
- For production staging deployments on cloud virtual machines, operating system-level disk encryption (e.g., BitLocker, LUKS, or cloud provider KMS-managed volume encryption) must be enabled.

