# PHASE 62 OPERATOR CHECKLIST
**Role:** Operational Personnel & On-Call Engineers  
**Target Release:** 0.62.0  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Pre-Flight Checklist (Prior to Restore)
- [ ] **Lock Check:** Verify `data/legalmitra_kb.db.restore.lock` does not exist.
- [ ] **Disk Space:** Verify at least 15 MB free disk space on storage volume (target + staging + backup).
- [ ] **Backup Integrity:** Run `python scripts/backup_kb.py --list` and ensure selected backup shows `Valid: True`.
- [ ] **Target Verification:** Verify target path points to knowledge base (`data/legalmitra_kb.db`) and **NEVER** to `data/conversations.db`.
- [ ] **Worker Notification:** Post notification in operational channels that a controlled database restore is commencing.

---

## 2. In-Flight Monitoring Checklist
- [ ] **Lock Acquisition:** Confirm `.restore.lock` is acquired cleanly without contention errors.
- [ ] **Staging Verification:** Confirm `.tmp_restore` file is written and validated before target swap.
- [ ] **Swap Execution:** Confirm `.prev_before_restore` is created temporarily during atomic swap.
- [ ] **Rollback Monitor:** Watch for any unhandled exceptions triggering automated rollback.

---

## 3. Post-Flight Verification Checklist
- [ ] **Outcome Status:** Confirm script outputs `Outcome Status: RESTORE_VERIFIED`.
- [ ] **Lock Release:** Verify `data/legalmitra_kb.db.restore.lock` has been cleanly removed.
- [ ] **Corpus Reconciliation:** Run `python scripts/reconcile_corpus.py` (assert 62 sources, 1,515 chunks, 0 orphans).
- [ ] **Freeze Check:** Run `python scripts/verify_freeze.py` (assert 6/6 files bitwise identical).
- [ ] **Review Packages Check:** Run `python scripts/verify_review_packages.py` (assert 40/40 candidates pending).
- [ ] **Audit Trail:** Verify trace entry appended to `data/22_central_legislation/phase62_recovery_traces.json`.
- [ ] **Worker Resumption:** Announce completion and re-enable application worker query traffic.

## 4. Emergency Abort & Recovery Procedures

If an operator observes an abnormal condition during restore execution:

### In case of hanging process or unreleased lock:
```powershell
# 1. Identify running Python processes
Get-Process python

# 2. Inspect lock file contents
Get-Content data/legalmitra_kb.db.restore.lock

# 3. If process PID is dead, remove stale lock
Remove-Item data/legalmitra_kb.db.restore.lock
```

### In case of partial restore or swap failure:
```powershell
# 1. Check if temporary previous backup exists
Test-Path data/legalmitra_kb.db.prev_before_restore

# 2. Restore previous backup manually if auto-rollback did not trigger
Move-Item -Force data/legalmitra_kb.db.prev_before_restore data/legalmitra_kb.db

# 3. Clean up staging file
Remove-Item -Force -ErrorAction SilentlyContinue data/legalmitra_kb.db.tmp_restore

# 4. Verify database integrity
python scripts/reconcile_corpus.py
```
