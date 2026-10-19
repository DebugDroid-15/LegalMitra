# PHASE 51: RUNBOOK 53 — RELEASE QUALITY GATE EVALUATION

**Project:** LegalMitra  
**Runbook Code:** `RB-53-RELEASE-GATES`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Purpose & Scope

This runbook outlines the operational evaluation of the 11 machine-readable release quality gates and generation of the authoritative release gate manifest `data/22_central_legislation/release_gates_manifest.json`.

---

## 2. Execution Command

Execute release gate evaluation and manifest generation:
```bash
python -c "
from legalmitra.evaluation.release_gates import ReleaseGateEvaluator
evaluator = ReleaseGateEvaluator()
path = evaluator.generate_manifest()
summary = evaluator.evaluate_all_gates()
print(f'Manifest generated at: {path}')
print(f'Overall Decision: {summary.overall_decision}')
print(f'Passed: {summary.passed_gates} | Pending: {summary.pending_gates} | Failed: {summary.failed_gates}')
for g in summary.gates:
    print(f'  [{g.status.value}] {g.gate_id}: {g.name}')
"
```

---

## 3. Decision Matrix & Release Policy

| Decision Output | Meaning & Permitted Action |
|:---|:---|
| `APPROVED_FOR_RELEASE` | All 11 gates passed including advocate sign-off. Approved for unrestricted public deployment. |
| `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF` | All 10 technical/algorithmic gates passed. Permitted for staging, evaluation, and advocate review. **Public deployment blocked.** |
| `BLOCKED_RELEASE_GATES_FAILED` | One or more technical gates failed. Release strictly blocked. Code remediation required. |

---

## 4. Advocate Review Handoff

When `overall_decision` is `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`:
1. Verify Package A in `data/06_review/PHASE9_REVIEW_SNAPSHOT_MANIFEST.json`.
2. Verify Package B in `data/07_batches/review/batch_01_handoff_manifest.json`.
3. Provide review sheets to counsel enrolled under the Advocates Act, 1961.
4. Record formal sign-off in `data/07_batches/review/review_tracking_register.json`.
