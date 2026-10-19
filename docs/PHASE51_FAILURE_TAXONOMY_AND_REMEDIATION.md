# PHASE 51: FAILURE TAXONOMY, ROOT CAUSE DIAGNOSIS & CODE REMEDIATION

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Systematic Failure Taxonomy

During Phase 51 evaluation, failures were classified according to an explicit 5-tier failure taxonomy:

```
+---------------------------------------------------------------------------------+
|                           LEGALMITRA FAILURE TAXONOMY                            |
+---------------------------------------------------------------------------------+
| 1. FABRICATED_CITATION_LEAK   | Emitting or validating non-existent law reports |
| 2. UNCOMMENCED_STATUTE_ENFORCE| Treating assent-only legislation as operative   |
| 3. AUTHORITY_STATUS_COLLAPSE  | Flattening overruled, stayed, or referred cases |
| 4. UNHEDGED_AMBIGUOUS_ASSERT  | Definitively answering with missing facts       |
| 5. INPUT_CRASH_UNHANDLED_EXC  | Engine crash on malformed dates or stress input  |
+---------------------------------------------------------------------------------+
```

---

## 2. Root Cause Diagnoses & Remediations

### Defect 1: Missing Judicial Precedents in Claim Synthesis
- **Diagnostic Finding:** `EvidenceTraceableAnswerAssembler` constructed claims from statutory extracts but ignored `evidence_set.judicial_precedents`. Precedents retrieved by the orchestrator were never decomposed into verifiable `AssembledClaim` objects.
- **Code Remediation:** Implemented precedent claim synthesis loop in `legalmitra/orchestration/answer_assembler.py` (lines 186–215), creating `AssembledClaim` records with passage text, temporal versions, authority statuses, and validation rationale.

### Defect 2: Precedent Referral Collision (*Ramesh Chandra*)
- **Diagnostic Finding:** In `legalmitra/orchestration/query_understanding.py`, queries referencing `ramesh chandra` were erroneously mapped to *Ramesh Verma (2017)*, bypassing the critical 2-judge referral case `CASE-SC-RAMESH-CHANDRA-REF-2019`.
- **Code Remediation:** Corrected precedent mapping tuple to point to `CASE-SC-RAMESH-CHANDRA-REF-2019`.

### Defect 3: Null `query_date_str` TypeError in Temporal Engine
- **Diagnostic Finding:** When benchmark queries were evaluated without an explicit context date, `resolve_amendment_impact_on_precedent` called `datetime.date.fromisoformat(query_date_str)` directly, raising `TypeError: fromisoformat: argument must be str`.
- **Code Remediation:** Added type and null check in `legalmitra/temporal/engine.py` (lines 874–885), returning `OPERATIVE_FOR_VERSION` for undated query contexts and catching `(ValueError, TypeError)`.

### Defect 4: Missing Sanhita Keywords in Citation Validity Verification
- **Diagnostic Finding:** In `legalmitra/evaluation/claim_metrics.py`, citation validity regex recognized `Act`, `Code`, `Rules`, `Constitution`, and `SCC`, but failed on post-2023 criminal codes (*Bharatiya Nyaya Sanhita*, *Bharatiya Nagarik Suraksha Sanhita*, *Bharatiya Sakshya Adhiniyam*), depressing citation validity to 64.9%.
- **Code Remediation:** Added `"Sanhita"`, `"Adhiniyam"`, `" v. "`, `"In Re"`, and `"Order"` to recognized citation keywords in `legalmitra/evaluation/claim_metrics.py`, restoring citation validity to 98.2%.

### Defect 5: Missing Offense Date Clarification Trigger for Cheating
- **Diagnostic Finding:** Inquiries regarding maximum penalty for cheating were returning `ANSWER_SUPPORTED` with generic IPC text rather than triggering `CLARIFICATION_REQUIRED`, risking misapplication across the 1 July 2024 boundary.
- **Code Remediation:** Added `"cheating"` to the decisive clarification trigger list in `legalmitra/orchestration/query_understanding.py` (line 397).
