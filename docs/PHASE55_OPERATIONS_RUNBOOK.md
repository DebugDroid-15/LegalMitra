# PHASE 55: OPERATIONS & REPRODUCIBILITY RUNBOOK

**Project:** LegalMitra  
**Phase:** 55  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Quick Verification Commands

### 1.1 Run Multi-Phase Test Regression (206 Tests)
```powershell
python -c "import subprocess, glob; files = [f for f in glob.glob('tests/test_phase*.py') if any(f'phase{p}' in f for p in range(40, 56))]; cmd = ['pytest'] + files + ['-q']; res = subprocess.run(cmd, capture_output=True, text=True); print(res.stdout); print(res.stderr)"
```
Expected: `206 passed in ~22s`

### 1.2 Verify Phase 9 Freeze Snapshot
```powershell
python scripts/verify_freeze.py
```
Expected: `Package A is 100% byte-for-byte verified and pending review.`

### 1.3 Verify Advocate Review Packages
```powershell
python scripts/verify_review_packages.py
```
Expected: `Review tracking register verified: 40 total records, all pending review.`

### 1.4 Evaluate Phase 55 Release Gates
```powershell
python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; ev = ReleaseGateEvaluator(); summary = ev.evaluate_all_gates(); print(summary.overall_decision); print(f'Passed: {summary.passed_gates}, Failed: {summary.failed_gates}, Pending: {summary.pending_gates}')"
```
Expected: `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`, `Passed: 10, Failed: 0, Pending: 1`

### 1.5 Run Contamination Audit on PIT-V11 Benchmark
```powershell
python -c "import json; from legalmitra.evaluation.contamination import ContaminationAuditor; d = json.load(open('data/22_central_legislation/temporal_benchmark_manifest.json')); r = ContaminationAuditor().audit_manifest(d['test_cases']); print(f'Total: {len(d["test_cases"])}, Held-out: {r.split_counts["held_out_evaluation"]}, Max Jaccard: {r.max_cross_split_jaccard:.4f}, Verdict: {r.audit_verdict}')"
```
Expected: `Total: 188, Held-out: 75, Max Jaccard: 0.5789, Verdict: PASS`
