# PHASE 53: OPERATIONS RUNBOOK & VERIFICATION SCRIPTS

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 53  

---

## 1. Standard Operational Commands

### 1.1 Verify Phase 9 Freeze Snapshot
```powershell
python scripts/verify_freeze.py
```

### 1.2 Verify 40 Review Packages
```powershell
python scripts/verify_review_packages.py
```

### 1.3 Run Phase 53 Test Suite
```powershell
pytest tests/test_phase53_evidence_reliability.py -v
```

### 1.4 Run Complete Multi-Phase Regression Suite (Phases 40–53)
```powershell
python -c "import subprocess, glob; files = [f for f in glob.glob('tests/test_phase*.py') if any(f'phase{p}' in f for p in range(40, 54))]; cmd = ['pytest'] + files + ['-q']; res = subprocess.run(cmd, capture_output=True, text=True); print(res.stdout); print(res.stderr)"
```

### 1.5 Generate Release Gates Manifest
```powershell
python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; ev = ReleaseGateEvaluator(); ev.generate_manifest('data/22_central_legislation/release_gates_manifest.json')"
```
