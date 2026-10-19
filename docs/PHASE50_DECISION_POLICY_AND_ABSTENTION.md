# LEGALMITRA — PHASE 50
## Decision Policy, Response States & Abstention Evaluation

**Document ID:** `LM-DOC-PHASE50-DECISION-POLICY-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED & TESTED  
**Date:** 2026-10-19  

---

### 1. Seven Mutually Exclusive Response States

The `LegalDecisionPolicy` in `legalmitra/orchestration/decision_policy.py` assigns every query to one of seven deterministic response states:

| Response State | Trigger Condition | Policy Action |
|---|---|---|
| `ANSWER_SUPPORTED` | All material propositions supported by retrieved evidence; no unresolved conflicts | Full structured legal response with citations |
| `ANSWER_QUALIFIED` | Supported answer subject to interim stays, larger-bench referrals, or statutory amendments | Answer presented alongside explicit qualifications |
| `CLARIFICATION_REQUIRED` | Missing material date, forum, or registration fundamentally alters governing law | Surface preliminary framework and ask targeted question |
| `ABSTAIN_INSUFFICIENT_EVIDENCE` | No relevant primary statutory provisions or precedents retrieved | Explicitly state evidence boundary and decline to answer |
| `ABSTAIN_AUTHORITY_CONFLICT` | Unresolved coordinate High Court split with missing user jurisdiction | Explain territorial split and request target jurisdiction |
| `ABSTAIN_TEMPORAL_UNCERTAINTY` | Direct enforcement sought under uncommenced enactment (e.g. Labour Codes) | Abstain from treating uncommenced code as operative law |
| `ABSTAIN_SOURCE_INTEGRITY_FAILURE` | Fabricated citation or forged circular detected | Decline proposition and warn of citation integrity failure |
