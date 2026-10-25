# Phase 58 Reproducibility Runbook

**Environment Requirements:** Python 3.11.0, Windows 11 / Linux, SQLite 3.42+

---

## 1. Step-by-Step Reproduction Commands

```powershell
# 1. Verify Git working tree cleanliness
git status

# 2. Verify Phase 9 review freeze snapshot integrity
python scripts/verify_freeze.py

# 3. Verify Advocate review packages and tracking register
python scripts/verify_review_packages.py

# 4. Run Phase 58 Evaluator Integrity & Negative Controls Test Suite
pytest tests/test_phase58_evaluator_integrity.py -v

# 5. Run Full Multi-Phase Regression Suite (Phases 40 to 58)
powershell -Command "pytest (Get-ChildItem tests/test_phase4*.py, tests/test_phase5*.py | Select-Object -ExpandProperty FullName)"

# 6. Execute Live Release Quality Gate Evaluation & Manifest Generation
python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; ev = ReleaseGateEvaluator(); manifest = ev.generate_manifest(); print('Generated:', manifest)"
```

---

## 2. Expected Verification Outputs

- `verify_freeze.py`: All 6 files match SHA-256 digests bitwise; 20 records pending review.
- `verify_review_packages.py`: 40 records verified pending review.
- `test_phase58_evaluator_integrity.py`: **30 passed in < 3s**.
- Multi-phase regression suite: **281 passed in < 30s** (0 failed).
- Release Gate Evaluator: **20 total gates, 19 passed, 1 pending review (`RG-11`), 0 failed**, decision `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`.
