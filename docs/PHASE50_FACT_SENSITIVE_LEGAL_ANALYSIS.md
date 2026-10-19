# LEGALMITRA — PHASE 50
## Fact-Sensitive Legal Analysis & IRAC Synthesis

**Document ID:** `LM-DOC-PHASE50-FACT-ANALYSIS-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED & TESTED  
**Date:** 2026-10-19  

---

### 1. Epistemic Separation Architecture

The `FactSensitiveAnalyzer` in `legalmitra/orchestration/fact_analyzer.py` classifies every statement into one of four epistemic categories:
1. `USER_PROVIDED_FACT`: Factual statements originating directly from the prompt.
2. `SOURCE_ESTABLISHED_FACT`: Verifiable statutory text, dates, bench strength, or official gazette notifications.
3. `ANALYTICAL_INFERENCE`: Legal conclusions deduced from applying rules to facts.
4. `UNKNOWN_OR_DISPUTED_FACT`: Ambiguous, conflicting, or unverified claims.

### 2. Structured IRAC Unit Generation

For every identified legal issue, the analyzer constructs an IRAC unit:
- **Issue:** Concise legal question.
- **Relevant Facts:** Material facts directly engaged by the issue.
- **Governing Rule:** Specific section, rule, or constitutional article with temporal validity.
- **Application:** Step-by-step statutory application.
- **Conclusion:** Grounded holding or qualification.
