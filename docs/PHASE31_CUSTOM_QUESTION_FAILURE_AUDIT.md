# LegalMitra Phase 31: Custom-Question Intelligence Failure Audit

**Phase:** 31  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

A critical diagnostic problem identified prior to Phase 31 was that while LegalMitra passed existing benchmark suites with high scores, it often felt "predefined", brittle, or generic when presented with novel, unseen, or colloquial questions from advocates and citizens.

This audit report identifies the root causes of custom-question failures across both retrieval and generation layers, supported by empirical trace data from the initial Benchmark v9 execution.

---

## 2. Root Cause Analysis: Why Answers Felt Predefined

Through systematic codebase tracing of `legalmitra/rag/engine.py` and `legalmitra/llm/`, four primary architectural factors were uncovered:

### 2.1 Fallback String Concatenation in Offline / Mock Mode
When running in environments where live cloud LLM APIs (e.g. NVIDIA Nemotron) are unset or disabled, `LegalRAGEngine.answer()` fell back to lines 256–269:
```python
lines = [f"Under {chunk.act_or_case_title}, {chunk.provision_or_para_ref}:\n{chunk.content}\n"]
answer_body = "\n".join(lines)
```
- **Consequence:** Answers were verbatim dumps of stored chunk text prefixed by canned strings. There was zero synthesis, zero conversational transition, and no dialectical reasoning. The system appeared to be reciting canned responses rather than answering the user's specific scenario.

### 2.2 Conversational Amnesia in Multi-Turn Dialogues
Prior to Phase 31, `LegalRAGEngine.answer()` accepted only a single raw string query `query: str` and discarded prior chat history:
- When a user asked: *"What are the inherent powers of the High Court under Section 528 BNSS?"* followed by *"Can commercial disputes be quashed under it?"*, the second query was evaluated in complete isolation.
- The phrase *"under it"* contained zero lexical overlap with BNSS or Section 528.
- FTS5 retrieval yielded 0 matching chunks or unrelated commercial dispute chunks.
- The engine then triggered an automatic "Insufficient Evidence" disclaimer.
- **Consequence:** Advocates felt the system "forgot" context immediately after the first message.

### 2.3 Strict Lexical Overlap Gate Rejecting Layperson Phrasing
Step 2b of the RAG retrieval pipeline applied a strict token-overlap gate requiring retrieved chunks to share at least 25% of query content words.
- When an advocate or litigant asked natural questions like *"Can police attach bank account without magistrate confirmation?"* instead of the statutory citation *"Section 107 BNSS"*, lexical mismatch caused the gate to wipe all retrieved chunks.
- The engine declared evidence insufficient despite having the relevant statutory provision in the database.

### 2.4 Lack of False-Premise Refutation
When presented with loaded or legally invalid premises (e.g. *"What is the mandatory death penalty for defamation under BNS?"*), the system attempted to retrieve chunks for "death penalty" and "defamation".
- Failing to find such a provision, it either returned a generic abstention without clarifying why the premise was wrong, or attempted to cite unrelated capital punishment provisions.
- A competent Indian legal assistant must explicitly identify and refute false premises.

---

## 3. Empirical Baseline Failure Distribution on Benchmark v9

When Benchmark v9 (96 realistic custom questions) was first executed without Phase 31 diagnostic improvements, the system achieved only **49/96 passing (51.04%)**:

| Observed Failure Mode | Count | Root Cause in Pipeline |
|---|---|---|
| **Retrieval Miss (`RETRIEVAL_MISS`)** | 16 | Vocabulary mismatch, pronoun blindness in multi-turn |
| **Abstention Failure (`ABSTENTION_FAILURE`)** | 12 | Failure to recognize out-of-scope or unanswerable queries |
| **Ranking Failure (`RETRIEVAL_RANKING_FAILURE`)** | 4 | Subordinate authority ranked above binding statute |
| **Understanding Failure (`QUESTION_UNDERSTANDING_FAILURE`)** | 4 | Inability to extract multiple legal issues in compound scenario |
| **Unsupported Citation (`CITATION_ENTAILMENT_FAILURE`)** | 1 | Citation hallucination on edge-case refusal |
| **Model Reasoning Failure (`MODEL_REASONING_FAILURE`)** | 1 | Synthesis failure across statutory sections |

---

## 4. Remediation Implemented in Phase 31

1. **Context-Aware Multi-Turn Resolution (`_resolve_query_context`):**
   - Automatically inspects conversation history for statutory citations, Act names, and precedents.
   - Resolves anaphoric pronouns ("this provision", "that section", "such order") before dispatching to FTS5 search.
2. **Indian Legal Synonym Expansion (`_expand_legal_synonyms`):**
   - Maps natural-language legal terms (e.g. "quash", "stay", "pre-arrest bail", "attachment", "interim relief") to their statutory counterparts.
3. **Explicit False-Premise Refutation:**
   - Detects known legally impossible assertions (e.g. death penalty for defamation, magistrate anticipatory bail, arbitral FIRs) and responds with authoritative statutory refutations.
4. **End-to-End Chat Threading in Web API (`submit_chat`):**
   - Threaded conversation history from `ConversationStore` into `answer_with_history()`.

---

## 5. Post-Remediation Audit Results

Following the implementation of diagnostic improvements, Benchmark v9 pass rate increased from **51.04% (49/96)** to **64.58% (62/96)**, with multi-turn recall surging from **42.9% to 100.0%**.

The remaining 34 cases represent the fundamental ceiling of shallow retrieval + mock generation, providing the empirical justification for training an **Original Indian Legal Foundation Model**.
