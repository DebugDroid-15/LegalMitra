# LegalMitra Phase 23 Advocate Review Governance Policy
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Governance Principles

1. **Human Supremacy in Legal Review:**
   No statistical, algorithmic, or LLM-based evaluation may supersede or emulate human advocate validation. The 40 review candidates remain strictly in `pending_legal_review` status until reviewed by qualified advocates enrolled with the Bar Council.
2. **Auditability & Non-Repudiation:**
   Every review transition creates an immutable entry in `data/06_review/audit/` documenting the reviewer's bar credentials, timestamp, old status, new status, score, and legal grounds.
3. **Dispute Resolution Mechanism:**
   When conflicting High Court opinions exist (e.g. diverging interpretations between the Delhi High Court and Bombay High Court on stamp duty arbitration impounding), records are transitioned to `disputed` rather than artificially forced into `approved`.

---

## 2. Review Quality Standards

- **Approved:** An affirmative decision indicating that the answer accurately represents prevailing Indian law, correctly identifies the active statutory enactment, contains zero anachronistic citations, and correctly states judicial precedent.
- **Needs Revision:** The legal principle is sound, but phrasing, missing caveats, or citation format requires rectification.
- **Rejected:** The answer contains legally erroneous propositions, hallucinates non-existent statutory sections, fails temporal regime checks, or violates statutory privacy constraints.
- **Disputed:** The legal proposition involves unsettled questions of law currently pending before a Constitution Bench or subject to conflicting Division Bench rulings.

---

## 3. Strict Fine-Tuning Prohibition

LegalMitra maintains a **STRICT NO-GO** on model fine-tuning. Fine-tuning models on unreviewed legal answers creates catastrophic hallucination risks and solidifies temporal inaccuracies. All model responses are generated through strictly grounded RAG retrieval against authoritative primary sources.

