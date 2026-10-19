# PHASE 51: RUNBOOK 51 — TEMPORAL BENCHMARK EXECUTION

**Project:** LegalMitra  
**Runbook Code:** `RB-51-BENCHMARK`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Purpose & Scope

This runbook describes the procedure for executing the 100-case temporal benchmark suite (`LEGALMITRA-BENCHMARK-PIT-V7`) across `development`, `validation`, and `held_out_evaluation` partitions, auditing point-in-time correctness and logging telemetry.

---

## 2. Prerequisites & Environment

- Workspace: `C:\PROJECTS\LegalMitra`
- Python environment: Python 3.11 with `pytest`, `sqlite3`, `numpy`
- Authoritative Knowledge Base: `data/legalmitra_kb.db`
- Benchmark Manifest: `data/22_central_legislation/temporal_benchmark_manifest.json`

---

## 3. Step-by-Step Execution

### Step 1: Verify Manifest Integrity & Splits
```bash
python -c "
import json
m = json.load(open('data/22_central_legislation/temporal_benchmark_manifest.json', encoding='utf-8'))
assert len(m['test_cases']) == 100
assert m['split_counts'] == {'development': 50, 'validation': 20, 'held_out_evaluation': 30}
print('[OK] Manifest integrity verified: 100 cases across 3 splits.')
"
```

### Step 2: Run Contamination Audit
```bash
python -c "
import json
from legalmitra.evaluation.contamination import ContaminationAuditor
m = json.load(open('data/22_central_legislation/temporal_benchmark_manifest.json', encoding='utf-8'))
report = ContaminationAuditor().audit_manifest(m['test_cases'])
assert report.audit_verdict == 'PASS'
print(f'[OK] Contamination audit passed: Max Jaccard = {report.max_cross_split_jaccard:.4f}')
"
```

### Step 3: Execute Benchmark Evaluation
```bash
pytest tests/test_phase51_evaluation_framework.py::test_held_out_cases_sample_execution -v
```

### Step 4: Verify Expected Outputs
Expected pass rate: 100%. All held-out queries return their exact calibrated response state.
