# Phase 57 Root-Cause Attribution Register

**Component:** `legalmitra.evaluation.error_attribution.RootCauseAttributor`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Attribution Engine Design

The `RootCauseAttributor` analyzes multi-component signals from `IndependentClaimEvaluator`, `AnswerCompletenessAuditor`, and `ClaimDependencyValidator`:
1. Distinguishes **established root causes** (verified by deterministic evidence, such as missing statutory terms or quarantined citation hashes) from **hypotheses** (unconfirmed candidate explanations).
2. Maps each attributed failure to affected pipeline components (`ClaimDependencyValidator`, `LegalDecisionPolicy`, `UnifiedEvidenceOrchestrator`, etc.).
3. Provides concrete, actionable suggested remediations for automated bug reporting and engineer review.
