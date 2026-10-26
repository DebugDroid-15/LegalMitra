# PHASE 62 INCIDENT RESPONSE GUIDE
**Incident Domain:** Knowledge Base Corruption & Recovery Failure  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Target Release:** 0.62.0  

---

## 1. Severity Classifications

| Severity | Definition | Target Resolution SLA |
| :--- | :--- | :--- |
| **SEV-1** | Production `legalmitra_kb.db` corrupted, queries failing, zero active recovery. | $< 15$ minutes |
| **SEV-2** | Restore attempt failed, automatic rollback preserved target, but recovery needed. | $< 1$ hour |
| **SEV-3** | Backup creation or pruning job failed; production serving queries normally. | $< 4$ hours |

---

## 2. SEV-1 Incident Response Playbook

1. **Triage & Containment:**
   - Stop application worker processes serving legal queries to avoid cascading errors.
2. **Identify Latest Healthy Backup:**
   - Run `python scripts/backup_kb.py --list`.
   - Inspect sidecar `.meta.json` files for latest valid backup with 1,515 chunks and 62 sources.
3. **Execute Atomic Restore:**
   - Execute `python scripts/restore_kb.py --backup data/backups/<latest_valid>.db --target data/legalmitra_kb.db`.
4. **Sanity Verification:**
   - Run `python scripts/reconcile_corpus.py`.
   - Run `pytest tests/test_phase62_disaster_recovery_assurance.py`.
5. **Resume Traffic:**
   - Restart application worker processes.
   - Monitor query error rates and trace logs.

---

## 3. SEV-2 Incident Response Playbook (Restore Rollback Triage)

If a restore operation triggers `RESTORE_FAILED_ORIGINAL_PRESERVED` with `rollback_performed = True`:
1. Inspect the console error message and trace ID.
2. Verify target database health using `python scripts/reconcile_corpus.py`.
3. Check why the candidate backup failed verification:
   - Check if the backup was truncated during network transfer.
   - Check if schema version was modified.
   - Check if orphaned chunks exist in the backup snapshot.
4. Select the preceding valid recovery point and retry the restore.

---

## 4. Post-Mortem & Incident Review Requirements

Within 24 hours of resolving a SEV-1 or SEV-2 recovery incident, the on-call engineer must file an incident review detailing:
- Exact timeline of failure detection, triage, and restore execution.
- Hash and filename of the backup utilized.
- Root cause of knowledge base failure or corrupted backup.
- Recommendations for backup retention, disk sizing, or testing enhancements.

## 5. Post-Mortem Template

All SEV-1 and SEV-2 recovery incidents require filing a post-mortem report within 24 hours of mitigation using this template:

```markdown
# INCIDENT POST-MORTEM: [INCIDENT-ID]
**Date:** YYYY-MM-DD  
**Severity:** SEV-1 | SEV-2  
**Incident Commander:** [Name]  
**Lead Investigator:** [Name]  

### 1. Executive Summary
- Brief 2-3 sentence overview of what broke, the user impact, and how it was restored.

### 2. Timeline (All times in UTC)
- HH:MM - First detection / alert triggered.
- HH:MM - Incident commander declared incident.
- HH:MM - Candidate backup identified.
- HH:MM - Restore script invoked.
- HH:MM - Database reconciled; traffic resumed.

### 3. Root Cause Analysis
- Detailed 5-Whys analysis explaining why the primary database failed and why the recovery was required.

### 4. Recovery Subsystem Performance
- Backup utilized: [Filename and SHA-256]
- Time to restore: [Seconds]
- Outcome status: [RESTORE_VERIFIED / RESTORE_FAILED_ORIGINAL_PRESERVED]
- Were rollback procedures required? [Yes / No]

### 5. Action Items & Corrective Actions
| Action Item | Owner | Priority | Target Due Date |
| :--- | :--- | :--- | :--- |
| e.g. Increase backup frequency | SRE Team | P1 | YYYY-MM-DD |
| e.g. Add disk storage alert | DevOps | P2 | YYYY-MM-DD |
```
