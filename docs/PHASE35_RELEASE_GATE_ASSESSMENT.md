# Phase 35 Release Gate Assessment & Governance Decisions

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Release Gate Framework

LegalMitra enforces separate release decisions for:
1. **Legal Data Engine Infrastructure:** Source registry FSM, discovery, secure acquisition, parsing, quality audit, and pretraining export.
2. **Pretraining Corpus Readiness:** Eligible unique token yield and multilingual balance.
3. **Original Model Scaling:** Parameter expansion to 10M, 125M, or 1.3B weights.
4. **Production Legal-Answer Generation:** End-user RAG search and citation generation.

---

## 2. Subsystem Gate Decisions

### A. Legal Data Engine Infrastructure: **GO**
- Unified Source Registry FSM prevents illegal state skips and records immutable transition logs.
- Source Discovery engine successfully prioritizes legal significance, language gaps, and Section 52(1)(q) rights.
- Secure Acquisition engine blocks SSRF, hop-by-hop redirects, private IP spaces, payload bombs, and corrupt files.
- Legal Parser detects structural defects (truncation, mojibake, header leakage).
- All 9 Phase 35 validation tests pass with zero errors.

### B. Pretraining Corpus Readiness: **PARTIAL GO (Milestone A Verified / Milestone B in Progress)**
- 342,965 usable tokens (334,348 English; 8,617 authentic Hindi) across 1,559 passages.
- Zero split leakage across source-grouped partitions.
- 10 national priority candidates cataloged for upcoming acquisition batches.
- Advancing to Milestone B (1M tokens) requires executing the acquisition pipeline against the 10 cataloged sources.

### C. Foundation Model Scaling (10M / 125M / 1.3B): **STRICT NO-GO**
- **Reason:** The verified eligible corpus (342k tokens) remains in a 615x deficit against the 211M token Chinchilla pretraining optimum for a 10.55M model.
- Training large models on starved data results in overfitting and high hallucination risk.
- Scaling is strictly blocked until Milestone D (50M tokens) is achieved.

### D. Production Legal Answers (Grounded RAG): **GO**
- Grounded RAG retrieval path in `legalmitra/rag/engine.py` remains the sole authoritative engine for user-facing legal answers.
- 1,499 verified knowledge base chunks remain completely untouched by pretraining experimental code.
- Phase 30 security controls, rate limiting, and session boundaries remain fully operational.

---

## 3. Governance Summary Table

| Subsystem | Decision | Primary Justification | Next Phase Requirement |
|---|---|---|---|
| National Legal Data Engine | **GO** | All 7 workstreams implemented, verified, and regression tested (45/45 tests passing) | Maintain FSM transition enforcement |
| Pretraining Corpus Readiness | **PARTIAL GO** | Milestone A reproduced; Milestone B candidates discovered | Execute batch acquisition for BNS/BNSS/BSA Hindi |
| Foundation Model Scaling | **STRICT NO-GO** | 615x token deficit; 342k tokens insufficient for >1.07M models | Acquire 50M tokens before scaling |
| Production Legal Answers | **GO** | RAG engine isolated, 100% frozen asset integrity maintained | Continue strict advocate review workflow |
