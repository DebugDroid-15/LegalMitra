# PHASE 62 INITIAL DEFECT REGISTER
**Phase Identifier:** LEGALMITRA-PHASE62  
**Target Release:** 0.62.0  
**Audit Scope:** Phase 61 Recovery and Release Candidate Baseline  
**Date:** 2026-10-26T19:20:00Z  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Audit Methodology & Scope

Prior to undertaking engineering enhancements, an independent architectural and forensic review was performed on the recovery mechanisms introduced in Phase 61 (`legalmitra/operations/backup_recovery.py` and associated scripts). The audit focused on edge conditions, concurrent access, failure during atomic operations, retention exhaustion, and cross-database boundary violations.

Six concrete defects and architectural gaps were identified and registered for resolution.

---

## 2. Identified Defects

### DEF-62-01: SQLite WAL Checkpoint Gap Prior to Checksum Computation
- **Severity:** HIGH
- **Component:** `KnowledgeBaseBackupManager.create_backup()`
- **Failure Mode:** In SQLite databases operating under Write-Ahead Logging (WAL) mode, dirty pages reside in `-wal` and `-shm` sidecars until checkpointed. Although `sqlite3.Connection.backup()` captures all committed pages into the target backup connection, the target backup database connection itself must be fully flushed and closed before computing the cryptographic SHA-256 hash. In the Phase 61 implementation, `PRAGMA wal_checkpoint(FULL)` was not explicitly issued on the source connection prior to backup, creating a potential edge case where uncheckpointed pages could cause subtle hash mismatches if the process was terminated before OS cache synchronization.
- **Remediation:** Explicitly execute `conn.execute("PRAGMA wal_checkpoint(FULL)")` on the source connection prior to initiating online backup page transfer, ensuring the disk file state is fully consolidated.
- **Verification:** `test_backup_transactional_consistency_and_metadata` validates that WAL mode checkpoints cleanly and hashes match bit-for-bit.

### DEF-62-02: Non-Atomic In-Place Restore Swap Risking Target Destruction
- **Severity:** CRITICAL
- **Component:** `KnowledgeBaseBackupManager.restore_backup()`
- **Failure Mode:** Phase 61 performed restoration by executing `shutil.copy2(backup_path, target_path)` directly over the existing database file. If an unhandled exception, power interruption, OS kill signal, or disk out-of-space error occurred midway through `shutil.copy2()`, the active production database would be left in a truncated, unrecoverable state, with the pre-restore production database already partially overwritten.
- **Remediation:** Implement a two-stage atomic restoration protocol:
  1. Stream copy backup to `<target>.tmp_restore`.
  2. Validate SQLite integrity and schema version on `.tmp_restore`.
  3. Rename current target to `<target>.prev_before_restore`.
  4. Rename `.tmp_restore` to target.
  5. If any validation or swap step fails, automatically restore `.prev_before_restore` back to target, setting `rollback_performed = True` and returning `RESTORE_FAILED_ORIGINAL_PRESERVED`.
- **Verification:** `test_restore_atomic_rollback_on_failed_swap` confirms that corrupted staging files trigger clean rollback to the original target.

### DEF-62-03: Lack of Mutual Exclusion File Lock During Restore Operations
- **Severity:** HIGH
- **Component:** `KnowledgeBaseBackupManager.restore_backup()`
- **Failure Mode:** If two administrative restore scripts or automated recovery processes were invoked concurrently against the same target database, both processes would attempt simultaneous file replacement, leading to race conditions, OS file lock contention, partial writes, or corrupted database headers.
- **Remediation:** Acquire an atomic mutual exclusion file lock (`<target>.restore.lock`) using `os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)` with guaranteed release in a `finally:` block. If lock acquisition fails, immediately abort the restore with an explicit concurrency error.
- **Verification:** `test_restore_concurrent_lock_prevents_collision` verifies lock acquisition blocks competing restore processes.

### DEF-62-04: Unbounded Backup Growth and Lack of Singleton-Safe Pruning
- **Severity:** MEDIUM
- **Component:** `KnowledgeBaseBackupManager`
- **Failure Mode:** Backups were created monotonically with no retention lifecycle or pruning automation. In continuous production environments, this creates disk exhaustion risks. Furthermore, naive pruning scripts that simply delete older files could delete all recovery points if an operator supplied an invalid retention count (e.g., 0).
- **Remediation:** Implement `list_backups()` and `prune_backups(keep_count)`. Enforce a singleton preservation invariant: if `len(backups) <= 1`, pruning will refuse to delete the sole existing backup regardless of `keep_count`. Synchronize deletion of accompanying `.meta.json` sidecar files.
- **Verification:** `test_backup_pruning_singleton_protection` and `test_backup_pruning_multi_backup`.

### DEF-62-05: Missing Cross-Database Restore Target Protection (`conversations.db`)
- **Severity:** HIGH
- **Component:** `KnowledgeBaseBackupManager._validate_path_security()`
- **Failure Mode:** The Phase 61 restore function permitted any target path within the workspace root. If an operator mistakenly specified `data/conversations.db` as the target of a knowledge base restore, all user conversation sessions, messages, and audit histories would be wiped and replaced with knowledge base chunks.
- **Remediation:** Add explicit path validation in `_validate_path_security()` checking if the target path resolves to or references `conversations.db`. If so, raise an immediate `ValueError` and halt execution.
- **Verification:** `test_security_restore_target_cannot_be_conversations_db` asserts targeting `data/conversations.db` raises `ValueError`.

### DEF-62-06: Subsecond Timestamp Collision in Rapid Backup Generation
- **Severity:** MEDIUM
- **Component:** `KnowledgeBaseBackupManager._generate_backup_filename()`
- **Failure Mode:** Backups used seconds-only timestamp formatting (`%Y%m%dT%H%M%SZ`). When running automated disaster-recovery test suites or high-speed recovery sequences within the same second, backup filenames collided, silently overwriting earlier backups and corrupting test assertions.
- **Remediation:** Update timestamp format to microsecond precision (`%Y%m%dT%H%M%S_%fZ`), guaranteeing unique filenames for any successive invocations.
- **Verification:** `test_backup_pruning_multi_backup` confirms multiple backups generated within fractions of a second receive distinct names.

---

## 3. Defect Remediation Tracking Matrix

| Defect ID | Title | Status | Resolution File | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| DEF-62-01 | WAL Checkpoint Gap | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_backup_transactional_consistency_and_metadata` |
| DEF-62-02 | Non-Atomic Restore Swap | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_restore_atomic_rollback_on_failed_swap` |
| DEF-62-03 | Missing Concurrency Lock | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_restore_concurrent_lock_prevents_collision` |
| DEF-62-04 | Unbounded Retention | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_backup_pruning_singleton_protection`, `test_backup_pruning_multi_backup` |
| DEF-62-05 | Target `conversations.db` | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_security_restore_target_cannot_be_conversations_db` |
| DEF-62-06 | Timestamp Collision | RESOLVED | `legalmitra/operations/backup_recovery.py` | `test_backup_pruning_multi_backup` |

## 4. Deep Forensic Analysis & Code Diffs

Below are the before-and-after implementation comparisons for the core defects remediated during Phase 62:

### 4.1 Remediation of DEF-62-01 (WAL Checkpoint Gap)
```python
# BEFORE (Phase 61):
with sqlite3.connect(str(self.kb_db_path)) as src_conn:
    with sqlite3.connect(str(staging_file)) as dst_conn:
        src_conn.backup(dst_conn, pages=-1)
# Potential issue: dirty pages in WAL log could cause target file to miss recent transactions

# AFTER (Phase 62):
with sqlite3.connect(str(self.kb_db_path)) as src_conn:
    # Explicitly checkpoint WAL frames back into main database file
    src_conn.execute("PRAGMA wal_checkpoint(FULL);")
    with sqlite3.connect(str(staging_file)) as dst_conn:
        src_conn.backup(dst_conn, pages=-1)
```

### 4.2 Remediation of DEF-62-02 (Non-Atomic In-Place Restore Swap)
```python
# BEFORE (Phase 61):
shutil.copy2(backup_path, target_path)
# CRITICAL RISK: Interruption midway overwrites target partially, resulting in irreversible corruption

# AFTER (Phase 62):
# Stage 1: Stream to temporary staging file
shutil.copy2(backup_file, tmp_restore)
self._verify_sqlite_file(tmp_restore)

# Stage 2: Preserve existing target database as rollback safety
if target_path.exists():
    target_path.replace(prev_target)

# Stage 3: Promote staging file to target
tmp_restore.replace(target_path)

# Stage 4: Verify post-swap integrity
try:
    self._verify_sqlite_file(target_path)
    if prev_target.exists():
        prev_target.unlink() # Clean up rollback snapshot
except Exception as swap_err:
    # Automatic rollback guarantee
    if prev_target.exists():
        if target_path.exists():
            target_path.unlink()
        prev_target.replace(target_path)
        rollback_performed = True
```

### 4.3 Remediation of DEF-62-03 (Missing Mutual Exclusion File Lock)
```python
# BEFORE (Phase 61):
# No concurrency lock; simultaneous restores execute in parallel causing file contention

# AFTER (Phase 62):
def _acquire_restore_lock(self, target_path: Path) -> Path:
    lock_file = target_path.with_name(f"{target_path.name}.restore.lock")
    try:
        # Atomic file creation using OS-level exclusive flag
        fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_RDWR)
        with os.fdopen(fd, "w") as f:
            f.write(f"pid={os.getpid()}\ntimestamp={datetime.now(timezone.utc).isoformat()}\n")
        return lock_file
    except FileExistsError:
        raise RuntimeError(f"Concurrent restore in progress: lock file {lock_file} exists")
```

### 4.4 Remediation of DEF-62-04 (Singleton Preservation Guard)
```python
# BEFORE (Phase 61):
# No pruning logic existed; backups accumulated indefinitely

# AFTER (Phase 62):
def prune_backups(self, keep_count: int = 5) -> List[str]:
    backups = self.list_backups()
    if len(backups) <= 1:
        # INVIOLABLE SINGLETON GUARD: Never prune the sole recovery point
        return []
    effective_keep = max(1, keep_count)
    if len(backups) <= effective_keep:
        return []
    # Only prune beyond effective_keep threshold
    ...
```

---

## 5. Security Threat Mitigation Matrix

| Threat Code | Vector | Consequence | Mitigating Control | Test Verification |
| :--- | :--- | :--- | :--- | :--- |
| `THR-62-A` | Target path traversal | Overwrite of arbitrary system files | Path resolution check in `_validate_path_security()` | `test_security_path_traversal_blocked` |
| `THR-62-B` | Target `conversations.db` | Accidental destruction of user chat history | Explicit blacklist of `conversations.db` in restore path | `test_security_restore_target_cannot_be_conversations_db` |
| `THR-62-C` | Race condition in restore | Truncated or corrupted SQLite database | Mutual exclusion file lock (`.restore.lock`) | `test_restore_concurrent_lock_prevents_collision` |
| `THR-62-D` | Incomplete write | Partial database file placed into production | Two-stage atomic swap with `.prev_before_restore` rollback | `test_restore_atomic_rollback_on_failed_swap` |
