# PHASE 54: OPERATIONS & REPRODUCIBILITY RUNBOOK

**Project:** LegalMitra  
**Phase:** 54  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Quick Verification Commands

### 1.1 Run Multi-Phase Test Regression
```powershell
python -c "import subprocess, glob; files = [f for f in glob.glob('tests/test_phase*.py') if any(f'phase{p}' in f for p in range(40, 55))]; cmd = ['pytest'] + files + ['-q']; res = subprocess.run(cmd, capture_output=True, text=True); print(res.stdout); print(res.stderr)"
```
Expected: `190 passed in ~45s`

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

### 1.4 Evaluate Phase 54 Release Gates
```powershell
python -c "from legalmitra.evaluation.release_gates import evaluate_release_gates; res = evaluate_release_gates('0.54.0'); print(res.overall_decision); print(f'Passed: {res.passed_gates}, Failed: {res.failed_gates}, Pending: {res.pending_gates}')"
```
Expected: `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`, `Passed: 10, Failed: 0, Pending: 1`

### 1.5 Validate Knowledge Graph Integrity
```powershell
python -c "from legalmitra.caselaw.knowledge_graph import build_default_knowledge_graph; g = build_default_knowledge_graph(); r = g.validate_graph_integrity(); print(r)"
```
Expected: `{'is_valid': True, 'dangling_edge_count': 0, 'orphan_node_count': 0, ...}`
