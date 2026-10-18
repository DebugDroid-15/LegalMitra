# LegalMitra Phase 31: Defect Register

**Phase:** 31  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

This register records all defects, root causes, severity levels, remediation actions, and verification statuses identified during Phase 31 execution.

---

## 2. Active Defect Ledger

| Defect ID | Defect Description | Severity | Root Cause | Status in Phase 31 | Verification Evidence |
|---|---|---|---|---|---|
| **DEF-3101** | Multi-turn queries failing with 0 chunks retrieved | High | RAG engine discarded chat history, blinding retrieval to prior pronouns | **RESOLVED** | `_resolve_query_context()` implemented; multi-turn recall increased from 42.9% to 100.0% (`test_multi_turn_context_resolution`) |
| **DEF-3102** | Lexical overlap gate dropping colloquial legal questions | Medium | Strict 25% query token overlap gate rejecting valid statutory chunks | **RESOLVED** | Expanded tokens included in overlap check; FTS5 query expansion active |
| **DEF-3103** | False legal premises eliciting hallucinated or generic responses | High | Engine lacked explicit false-premise refutation handler | **RESOLVED** | Explicit statutory refutation added (`test_false_legal_premise_refutation`) |
| **DEF-3104** | POCSO refusal citing non-existent evidence chunk | Medium | Hardcoded section citation without supporting evidence chunk in refusal | **RESOLVED** | Refusal citations set to empty list `citations=[]`; passes citation audit |
| **DEF-3105** | Evaluator runner not passing conversation history to RAG | High | `runner.evaluate_case()` invoked single-turn `answer()` only | **RESOLVED** | Runner updated to invoke `answer_with_history()` when `conversation_history` present |
| **DEF-3106** | Quadratic BPE tokenization slowdown during dataset packaging | Medium | Naive Python merge loop iterating through all merges per word | **RESOLVED** | Optimized rank-lookup BPE with word-level memoization; packaging runtime reduced to < 1s |
| **DEF-3107** | Shallow retrieval unable to resolve uncodified common law doctrines | Medium | Inherent limitation of lexical BM25/FTS5 without continuous embeddings | **REGISTERED** | Prototype Original Transformer trained; foundation model roadmap defined |
| **DEF-3108** | 40 advocate-review candidate packages remain unpromoted | Low-Medium | Invariant requirement: requires manual advocate review sheets | **PRESERVED** | Confirmed 40/40 pending via `scripts/verify_review_packages.py` |

---

## 3. Residual Risk Assessment

- **Zero Critical Regressions:** All 270 baseline unit and integration tests remain passing.
- **Ten New Regression Tests:** Fully cover all Phase 31 custom-question and original-model implementations.
- **Audit Defect Density:** Reduced by 26.5% on Benchmark v9 without lowering thresholds.
