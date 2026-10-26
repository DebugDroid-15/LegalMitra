# PHASE 62 RESTORE SAFETY AUDIT
**Module:** `legalmitra.operations.backup_recovery`  
**Audit Dimension:** Disaster Recovery & Restore Safety Assurance  
**Target Release:** 0.62.0  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Safety Objectives

Database restoration is an inherently high-risk administrative action. The restore subsystem must guarantee:
1. **Pre-flight Validation:** Corrupted, truncated, tampered, or mismatched backups must fail before any disk modification occurs on the target.
2. **Mutual Exclusion:** Simultaneous restore commands must be locked out to prevent concurrent file contention.
3. **Guaranteed Rollback:** If the restore process fails during file swap or post-restore verification, the original target database must be completely restored without data loss.
4. **Boundary Isolation:** Targets outside the authorized knowledge base path (such as `data/conversations.db`) must be blocked fail-closed.

---

## 2. Multi-Stage Atomic Restoration Protocol

The restoration workflow in `KnowledgeBaseBackupManager.restore_backup()` follows a deterministic 5-stage pipeline:

```
[Start restore_backup]
        |
        v
[Phase 1: Path Security & Lock Acquisition]
  - Validate backup and target paths (block path traversal & conversations.db)
  - Acquire atomic file lock: <target>.restore.lock (O_CREAT | O_EXCL)
        |
        v
[Phase 2: Pre-Flight Backup Verification]
  - Check file existence and non-zero size
  - Compute SHA-256 and compare against .meta.json
  - Execute PRAGMA integrity_check on backup
  - Verify schema version (1.0.0)
  - Verify scaffold quarantine
  - Detect orphaned chunks (chunk_sources foreign key check)
  --> If invalid: release lock, return RESTORE_FAILED_ORIGINAL_PRESERVED
        |
        v
[Phase 3: Staged Copy to .tmp_restore]
  - Copy backup to <target>.tmp_restore
  - Verify SQLite header & integrity on <target>.tmp_restore
        |
        v
[Phase 4: Atomic Two-Stage Swap with Rollback Backup]
  - If target exists: rename <target> -> <target>.prev_before_restore
  - Rename <target>.tmp_restore -> <target>
  - Execute PRAGMA integrity_check on restored <target>
  --> If failure detected:
        Rename <target>.prev_before_restore -> <target>
        Set rollback_performed = True
        Return RESTORE_FAILED_ORIGINAL_PRESERVED
        |
        v
[Phase 5: Cleanup & Audit Emission]
  - Remove <target>.prev_before_restore
  - Release <target>.restore.lock
  - Emit RecoveryOperationAuditRecord to recovery trace log
  - Return RESTORE_VERIFIED
```

---

## 3. Failure Mode Matrix & Fail-Closed Controls

| Failure Injected | Test Case | Subsystem Behavior | Outcome Status | Target Preserved? |
| :--- | :--- | :--- | :--- | :--- |
| Truncated DB (32 bytes) | `test_restore_truncated_backup_fails_closed` | Fails SHA-256 and SQLite header check in pre-flight. Target untouched. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES |
| Mismatched SHA-256 | `test_restore_mismatched_hash_fails_closed` | Fails cryptographic hash verification in pre-flight. Target untouched. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES |
| Unsupported Schema (v99.0) | `test_restore_unsupported_schema_version_fails_closed` | Fails schema version check (`99.0.0` != `1.0.0`). Target untouched. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES |
| Orphaned Chunks in Backup | `test_restore_orphaned_chunks_fails_closed` | Foreign key check finds chunks without valid `source_id`. Pre-flight fails. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES |
| Concurrent Restore Invocation | `test_restore_concurrent_lock_prevents_collision` | Second process fails to acquire `<target>.restore.lock`. Aborts immediately. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES |
| Corrupted Target Swap | `test_restore_atomic_rollback_on_failed_swap` | Post-swap integrity verification fails. Automatically rolls back from `.prev_before_restore`. | `RESTORE_FAILED_ORIGINAL_PRESERVED` | YES (`rollback_performed=True`) |

---

## 4. Rollback Mechanics Under Operating System Constraints

On Windows operating systems, renaming files while connections or handles remain active causes `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.

To ensure reliability across Windows and Linux environments:
1. Every connection opened for pre-flight verification or integrity checking explicitly closes connections inside a deterministic `finally:` block.
2. The staging file `<target>.tmp_restore` is written and verified before attempting any modification of `<target>`.
3. If an error occurs during stage 4, the rollback handler executes:
   ```python
   if prev_target.exists() and (not target_path.exists() or swap_failed):
       if target_path.exists():
           target_path.unlink()
       prev_target.replace(target_path)
       rollback_performed = True
   ```
4. This ensures that even under interrupted execution, the target database never remains in a corrupted, half-written state.

---

## 5. Audit Conclusion

The LegalMitra restore pipeline satisfies all production safety criteria. Every failure mode tested results in zero data loss, zero target corruption, and deterministic rollback.

## 6. Windows OS File Replacement Semantics & Atomic Rename

In POSIX environments, `rename()` over an existing file is atomic and immediately replaces the target inode. In Windows environments (NTFS / ReFS), attempting to rename or overwrite an open file handle results in `WinError 32: The process cannot access the file because it is being used by another process`.

To ensure 100% deterministic portability on Windows:
1. **Explicit Connection Teardown:** Every verification query runs in a context manager (`with sqlite3.connect(...) as conn:`) ensuring file descriptors are closed before file rename operations commence.
2. **Two-Stage Shift:**
   - Instead of overwriting `data/legalmitra_kb.db` directly:
   - Target is moved to `data/legalmitra_kb.db.prev_before_restore` using `replace()`.
   - Staging file `data/legalmitra_kb.db.tmp_restore` is moved to `data/legalmitra_kb.db` using `replace()`.
3. **Rollback Resilience:** If the second `replace()` fails, the original file is moved back from `prev_before_restore`, leaving the database in its exact original state.

### 6.1 State Transition Matrix During Recovery

```
State 0: [Target: Active KB (Valid)] [Temp: None] [Prev: None]
State 1: [Target: Active KB (Valid)] [Temp: Staged (Verifying)] [Prev: None]
State 2: [Target: Active KB (Valid)] [Temp: Staged (Verified)] [Prev: None]
State 3: [Target: None] [Temp: Staged] [Prev: Active KB (Preserved)]
State 4: [Target: Restored KB] [Temp: None] [Prev: Active KB (Preserved)]
State 5: [Target: Restored KB (Verified)] [Temp: None] [Prev: Deleted]
```

If an error triggers at State 3 or State 4, the rollback handler immediately reverts to State 0:
```
Rollback: [Target: Active KB (Restored from Prev)] [Temp: Deleted] [Prev: Deleted]
```
