# PHASE 56: OPERATIONS RUNBOOK AND VERIFICATION GUIDE

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  

---

## 1. Purpose and Scope

This runbook provides reproducible operational procedures for verifying the multi-authority synthesis layer, executing the PIT-V12 benchmark, evaluating release quality gates, and auditing governance invariants.

---

## 2. Standard Operational Verification Commands

### 2.1 Governance Freeze & Review Package Audit
```powershell
python scripts/verify_freeze.py
python scripts/verify_review_packages.py
```
*Expected Result:* 100% byte-for-byte match on 6 Phase 9 files; 40 review candidates pending.

### 2.2 Phase 56 Test Suite Execution
```powershell
pytest tests/test_phase56_multi_authority_synthesis.py -v
```
*Expected Result:* 20 passed in ~2s.

### 2.3 Full Multi-Phase Regression Suite (Phases 40–56)
```powershell
pytest (Get-ChildItem tests	est_phase*.py | Where-Object { $_.Name -match 'test_phase(4[0-9]|5[0-6])' } | ForEach-Object { $_.FullName }) -q
```
*Expected Result:* 226 passed in ~10s.

### 2.4 Release Quality Gates Evaluation
```powershell
python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; e = ReleaseGateEvaluator(); e.generate_manifest(); s = e.evaluate_all_gates(); print(f'{s.passed_gates}/{s.total_gates} gates passed; Overall: {s.overall_decision}')"
```
*Expected Result:* 14/15 gates passed; Overall: `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`.

### 2.5 Benchmark Contamination Audit
```powershell
python -c "import json; from legalmitra.evaluation.contamination import ContaminationAuditor; data = json.load(open('data/22_central_legislation/temporal_benchmark_manifest.json', encoding='utf-8')); r = ContaminationAuditor().audit_manifest(data['test_cases']); print(f'Cases: {r.total_cases_audited}, Max Jaccard: {r.max_cross_split_jaccard:.4f}, Verdict: {r.audit_verdict}')"
```
*Expected Result:* 212 cases, max Jaccard $\le 0.85$, Verdict: `PASS`.
