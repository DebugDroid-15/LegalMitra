# PHASE 62 DISASTER RECOVERY RUNBOOK
**Audience:** Site Reliability Engineers, DevOps, Systems Administrators  
**Applicability:** Production & Staging Environments  
**Target Release:** 0.62.0  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Overview & Prerequisites

This runbook specifies exact operational procedures for executing disaster recovery against the LegalMitra knowledge base (`data/legalmitra_kb.db`).

### Required Permissions & Environment:
- Access to workspace root (`C:\PROJECTS\LegalMitra` or production equivalent).
- Python 3.11 environment with project virtual environment activated.
- Write permissions on `data/` and `data/backups/`.

---

## 2. Recovery Procedures

### Scenario 1: Standard Restoration from Latest Verified Backup
1. Check available backups:
   ```bash
   python scripts/backup_kb.py --list
   ```
2. Select the desired verified backup (e.g. `data/backups/legalmitra_kb_20261026T115207Z.db`).
3. Execute restore command:
   ```bash
   python scripts/restore_kb.py --backup data/backups/legalmitra_kb_20261026T115207Z.db --target data/legalmitra_kb.db
   ```
4. Verify console output reports:
   ```text
   Outcome Status: RESTORE_VERIFIED
   Rollback Performed: False
   Trace ID: <uuid>
   SUCCESS: Database restored and verified.
   ```
5. Run post-restore reconciliation:
   ```bash
   python scripts/reconcile_corpus.py
   ```

### Scenario 2: Rollback Handling (Automatic or Manual)
If restoration encounters a corrupted backup or disk failure during swap, the system automatically rolls back from `<target>.prev_before_restore`.

If an external catastrophic interruption killed the process mid-swap:
1. Check for `<target>.prev_before_restore`.
2. Check for `<target>.restore.lock`.
3. If lock exists and no process is running, remove `<target>.restore.lock`.
4. If `<target>` is missing or corrupt but `<target>.prev_before_restore` exists:
   ```bash
   mv data/legalmitra_kb.db.prev_before_restore data/legalmitra_kb.db
   ```
5. Re-run `python scripts/reconcile_corpus.py`.

---

## 3. Backup Retention Maintenance
Prune backups periodically keeping the 5 most recent snapshots:
```bash
python scripts/backup_kb.py --prune 5
```

---

## 4. Troubleshooting Guide

| Symptom | Probable Cause | Action |
| :--- | :--- | :--- |
| `PermissionError: [WinError 32]` | Target database open in another process (e.g. DB Browser) | Close DB Browser / query processes and retry. |
| `Concurrent restore in progress` | Stale `.restore.lock` file left after crash | Inspect process list; if no restore running, delete `.restore.lock`. |
| `SHA-256 hash mismatch` | Backup file tampered or corrupted in storage | Select previous recovery point from `python scripts/backup_kb.py --list`. |
| `Target cannot be conversations.db` | Operator entered wrong target argument | Correct target argument to `data/legalmitra_kb.db`. |

## 5. Disaster Recovery Exercise (Game Day Scenario)

To maintain operational readiness, SRE teams must execute a semi-annual Disaster Recovery Game Day:
1. **Setup:** Provision a staging cluster mirroring production data.
2. **Simulation:** Execute a simulated corruption script that injects garbage bytes into the staging database.
3. **Execution:** On-call engineer receives mock SEV-1 page, executes `scripts/restore_kb.py`, runs reconciliation, and posts status.
4. **Target Time:** Entire recovery exercise must be completed within 10 minutes.

## 6. SRE Command Cheat Sheet for Disaster Recovery

| Scenario | Command | Expected Output |
| :--- | :--- | :--- |
| Check all backups | `python scripts/backup_kb.py --list` | Table of available backups with timestamps and validity. |
| Create immediate snapshot | `python scripts/backup_kb.py --verify` | Backup created and verified in `data/backups/`. |
| Prune old snapshots | `python scripts/backup_kb.py --prune 5` | Retains 5 newest, prunes older snapshots and metadata. |
| Restore production database | `python scripts/restore_kb.py --backup data/backups/<file>.db` | Outcome: `RESTORE_VERIFIED`, target swapped atomically. |
| Verify post-restore corpus | `python scripts/reconcile_corpus.py` | 62 sources, 1,515 chunks, 0 orphans, 0 duplicates. |
| Check governance freeze | `python scripts/verify_freeze.py` | 6/6 files bitwise identical. |
| Check pending review packages | `python scripts/verify_review_packages.py` | 40/40 candidates pending legal review. |
