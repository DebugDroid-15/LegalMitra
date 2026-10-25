# LegalMitra Phase 59 — Reproducibility Runbook

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Preflight Verification Commands

To reproduce all Phase 59 results from clean repository checkout:

```powershell
# 1. Verify Phase 9 Review Baseline Freeze (6/6 bitwise identical)
python scripts/verify_freeze.py

# 2. Verify Review Tracking Register (40 records pending legal review)
python scripts/verify_review_packages.py

# 3. Verify PIT-V14 Benchmark Suite (280 cases, zero contamination)
python -c "
import json
from legalmitra.evaluation.contamination import ContaminationAuditor
with open('data/22_central_legislation/temporal_benchmark_manifest.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
assert d['total_test_cases'] == 280
rep = ContaminationAuditor().audit_manifest(d['test_cases'])
assert rep.is_split_isolated is True
print('PIT-V14 Clean:', rep.is_split_isolated, 'Max Jaccard:', rep.max_cross_split_jaccard)
"

# 4. Evaluate all 20 Release Quality Gates
python -c "
from legalmitra.evaluation.release_gates import ReleaseGateEvaluator
evaluator = ReleaseGateEvaluator()
summary = evaluator.evaluate_all_gates()
print('Release:', summary.release_id, summary.target_version)
print('Passed:', summary.passed_gates, 'Failed:', summary.failed_gates, 'Pending:', summary.pending_gates)
assert summary.passed_gates == 19
assert summary.pending_gates == 1
assert summary.overall_decision == 'STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF'
"
```

---

## 2. Test Execution Commands

```powershell
# Run Phase 59 Authority Verification Suite (32 tests)
pytest tests/test_phase59_authority_verification.py -v

# Run Full Regression Suite across Phases 40 through 59 (313 tests)
python scripts/run_regression_suite.py
```
