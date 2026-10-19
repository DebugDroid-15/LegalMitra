# LEGALMITRA — PHASE 48 RUNBOOK 43
## Operational Runbook: System Invariants & Safeguards Verification

**Runbook ID:** `LM-RUNBOOK-48-043`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Verify all non-negotiable architectural invariants: Phase 9 freeze, advocate review status, synthetic scaffold quarantine, and DB separation.

### 2. Operational Procedure
```bash
python tests/verify_freeze.py
python tests/verify_review_packages.py
pytest tests/test_phase9_freeze.py -q
```

### 3. Pass Criteria
All scripts must exit with code 0.
