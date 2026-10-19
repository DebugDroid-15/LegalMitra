# PHASE 52: EVIDENCE ELIGIBILITY ENGINE & FAIL-CLOSED GUARDS

**Project:** LegalMitra  
**Module:** `legalmitra.corpus.eligibility`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Purpose & Architectural Principles

The `EvidenceEligibilityEngine` provides deterministic gatekeeping before any candidate chunk or source is returned by the `UnifiedEvidenceOrchestrator`. It enforces:
1. **Scaffold Quarantine**: Chunks with `is_synthetic_scaffold = 1` or source `IND-JUD-DEL-2024-BAIL` are unconditionally rejected.
2. **Fixture Rejection**: Test fixtures (`IND-UNSUPPORTED-001`) and unparsed administrative handbooks (`IND-GUIDE-SCI-PROC-2025`) are rejected.
3. **Fail-Closed Unknown Sources**: Unregistered source IDs default to `is_eligible = False`.
4. **Temporal Warnings**: Post-dated statutes relative to query temporal anchor trigger explicit temporal warnings.
5. **Training Prohibition**: Pretraining on corpus chunks remains non-negotiable `STRICT NO-GO`.

---

## 2. Integration with Orchestrator

The engine is directly integrated into `legalmitra/orchestration/evidence_orchestrator.py` during raw search result iteration:

```python
verdict = eligibility_engine.evaluate_chunk_eligibility(
    source_id=r.source_id,
    chunk_id=r.chunk_id,
    is_synthetic_scaffold=bool(r.is_synthetic_scaffold),
    as_of_date=parsed_query.query_date,
)
if not verdict.is_eligible:
    continue
```
