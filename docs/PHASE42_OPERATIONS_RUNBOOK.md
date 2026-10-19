# LegalMitra Phase 42 — Operations Runbook

**Date:** October 19, 2026  
**Audience:** Site Reliability Engineers, Legal Data Pipeline Operators, Corpus Auditors  

---

## 1. Daily Invariant & System Integrity Verification

Execute every morning or before any release tag:

```powershell
# 1. Verify Phase 9 Freeze Files
python scripts/verify_freeze.py

# 2. Verify Advocate Review Packages & Tracking Register
python scripts/verify_review_packages.py

# 3. Verify Corpus Reconciliation & Physical DB Separation
python scripts/reconcile_phase42_corpus.py

# 4. Execute Full Regression Test Suite
pytest -q
```

---

## 2. Ingesting Authorized Subordinate eCourts Dumps

When official CIS batch records are received from eCommittee partners:

1. **Place Dump File in Staging Directory:**
   Save verified JSON export to `data/21_judicial_infrastructure/authorized_dumps/batch_<DATE>.json`.
2. **Execute Staging Ingestion:**
   ```powershell
   python -c "
   from legalmitra.judicial.ecourts_adapter import AuthorizedECourtsAdapter
   adapter = AuthorizedECourtsAdapter()
   records = adapter.ingest_staging_dump('data/21_judicial_infrastructure/authorized_dumps/batch_20261019.json')
   print(f'Successfully ingested and verified {len(records)} subordinate court records.')
   "
   ```
3. **Verify Privacy Gating:**
   Ensure records involving POCSO / Sec 228A IPC are classified `BLOCKED_RESTRICTED` and omitted from retrieval indexes.

---

## 3. Running Scanned Hindi OCR Evaluation Benchmark

To audit Devanagari OCR accuracy against newly added courtroom scans:

```powershell
python scripts/evaluate_real_world_ocr.py
```
Expected production baseline thresholds:
- Normalized Character Error Rate (CER): $\le 2.0\%$
- Normalized Word Error Rate (WER): $\le 4.0\%$
- Statutory Legal Token Sensitivity: $\ge 98.0\%$

---

## 4. Executing Controlled High Court Pilot

To test High Court connector network boundaries and preflight checks:

```powershell
# Execute in safe controlled fixture mode (default)
python scripts/run_controlled_high_court_pilot.py --limit 3

# If institutional API authorization is granted by registrar:
python scripts/run_controlled_high_court_pilot.py --live --limit 3
```
