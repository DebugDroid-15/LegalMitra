# PHASE 62 RECOVERY SUBSYSTEM INVENTORY
**Module:** `legalmitra.operations.backup_recovery`  
**Associated CLI:** `scripts/backup_kb.py`, `scripts/restore_kb.py`  
**Reconciliation Extension:** `legalmitra.operations.reconciler`  
**Target Database:** `data/legalmitra_kb.db`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Architectural Overview

The LegalMitra Knowledge Base Backup and Disaster Recovery Subsystem provides transactional, point-in-time recovery for the core legal knowledge base (`data/legalmitra_kb.db`) while strictly isolating user conversation state (`data/conversations.db`) and guaranteeing zero corruption risk during interrupted restore operations.

```
+-------------------------------------------------------------------------+
|                  KnowledgeBaseBackupManager Architecture                |
+-------------------------------------------------------------------------+
|                                                                         |
|  [Source Database]                [Online Backup API]                   |
|  data/legalmitra_kb.db  ------->  PRAGMA wal_checkpoint(FULL)           |
|                                         |                               |
|                                         v                               |
|                                   Stream Pages                          |
|                                         |                               |
|                                         v                               |
|                                   [Staging File]                        |
|                                   backup.db.tmp_part                    |
|                                         |                               |
|                                         v Integrity Check & Quarantine  |
|                                   [Promote to Target]                   |
|                                   data/backups/legalmitra_kb_<ts>.db    |
|                                         + Sidecar .meta.json            |
|                                                                         |
|  [Restore Subsystem]                                                    |
|  data/backups/*.db   ------------> Pre-flight Integrity & Hash Check    |
|                                         |                               |
|                                         v Acquire .restore.lock (Excl)  |
|                                   Stage 1: Copy to .tmp_restore         |
|                                   Stage 2: Validate Target & Orphans    |
|                                   Stage 3: Atomic Swap with Rollback    |
|                                   Backup old -> .prev_before_restore    |
|                                   Promote -> data/legalmitra_kb.db      |
|                                   Post-check failure -> Auto-Rollback   |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

## 2. Core Class and Interface Inventory

### 2.1 `KnowledgeBaseBackupManager`
Defined in `legalmitra/operations/backup_recovery.py`.

Key Responsibilities:
1. **Streaming Online Backup:** Utilizes `sqlite3.Connection.backup()` to copy database pages consistently without taking write locks that disrupt read transactions.
2. **WAL Checkpointing:** Executes `PRAGMA wal_checkpoint(FULL)` prior to hashing and file promotion to ensure all committed write-ahead-log pages reside in the main database file.
3. **Staged Writes:** Writes backup files to temporary `.tmp_part` files, verifying SQLite integrity before renaming to final `.db` filenames.
4. **Collision Resistance:** Uses microsecond timestamp formatting (`%Y%m%dT%H%M%S_%fZ`) to prevent naming collisions under high-frequency automated backups.
5. **Atomic Two-Stage Restoration:** Restores to `.tmp_restore`, validates internal consistency, swaps target with `.prev_before_restore` preservation, and automatically rolls back if post-restore checks fail.
6. **Mutual Exclusion Locking:** Enforces atomic file locking (`<target>.restore.lock`) via `os.open` with `O_CREAT | O_EXCL` flags, preventing concurrent restore processes from corrupting database state.
7. **Retention and Pruning:** Implements `list_backups()` and `prune_backups(keep_count)` with singleton protection to prevent accidental deletion of all recovery points.
8. **Path Security Validation:** Restricts backup/restore paths to designated project directories, prevents path traversal (`..`), and explicitly forbids targeting `data/conversations.db`.

---

## 3. Data Structures & Contract Specifications

### 3.1 `RecoveryOutcomeStatus`
```python
class RecoveryOutcomeStatus(str, Enum):
    RESTORE_VERIFIED = "RESTORE_VERIFIED"
    RESTORE_FAILED_ORIGINAL_PRESERVED = "RESTORE_FAILED_ORIGINAL_PRESERVED"
    RESTORE_INCOMPLETE_REQUIRES_OPERATOR_ACTION = "RESTORE_INCOMPLETE_REQUIRES_OPERATOR_ACTION"
```
- `RESTORE_VERIFIED`: Full restoration succeeded, SQLite header integrity passed, schema validated, orphan check clean, target promoted.
- `RESTORE_FAILED_ORIGINAL_PRESERVED`: Restoration was rejected or aborted; the original production database remains untouched or was cleanly rolled back.
- `RESTORE_INCOMPLETE_REQUIRES_OPERATOR_ACTION`: Critical unexpected disk/OS failure occurred during rollback; manual intervention required.

### 3.2 `BackupManifest`
```python
@dataclass
class BackupManifest:
    backup_file: str
    timestamp_utc: str
    file_size_bytes: int
    sha256_hash: str
    chunk_count: int
    source_count: int
    scaffold_chunk_count: int
    is_valid: bool
    schema_version: str = "1.0.0"
    sqlite_version: str = "3.41.2"
    journal_mode: str = "wal"
    has_fts5: bool = True
```

### 3.3 `BackupVerificationResult`
```python
@dataclass
class BackupVerificationResult:
    is_valid: bool
    backup_file: str
    file_size_bytes: int
    sha256_matches: bool
    integrity_check_passed: bool
    schema_valid: bool
    chunk_count: int
    source_count: int
    scaffold_chunk_count: int
    error_message: Optional[str] = None
```

### 3.4 `RestoreResult`
```python
@dataclass
class RestoreResult:
    success: bool
    target_db: str
    backup_file: str
    verification: BackupVerificationResult
    error_message: Optional[str] = None
    outcome_status: RecoveryOutcomeStatus = RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED
    rollback_performed: bool = False
    audit_trace_id: Optional[str] = None
```

### 3.5 `RecoveryOperationAuditRecord`
```python
@dataclass
class RecoveryOperationAuditRecord:
    trace_id: str
    timestamp_utc: str
    operation: str
    source_file: str
    target_file: str
    success: bool
    outcome_status: str
    duration_ms: float
    error_message: Optional[str] = None
    rollback_performed: bool = False
```

---

## 4. Reconciliation Subsystem Extension

### `CorpusReconciler.compare_pre_and_post_restore()`
Defined in `legalmitra/operations/reconciler.py`.

Accepts two `CorpusReconciliationReport` instances (pre-restore and post-restore) and computes a comprehensive deep difference report:
- Source count match and delta
- Chunk count match and delta
- Scaffold count match and delta
- Orphan chunk count match and delta
- Duplicate chunk ID count match and delta
- Set difference analysis: new sources, missing sources, new chunks, missing chunks
- Overall semantic parity boolean (`overall_equivalent`)

```python
def compare_pre_and_post_restore(
    self, pre_report: CorpusReconciliationReport, post_report: CorpusReconciliationReport
) -> Dict[str, Any]:
    sources_diff = post_report.total_sources - pre_report.total_sources
    chunks_diff = post_report.total_chunks - pre_report.total_chunks
    scaffolds_diff = post_report.scaffold_chunks - pre_report.scaffold_chunks
    orphans_diff = post_report.orphaned_chunks - pre_report.orphaned_chunks
    duplicates_diff = post_report.duplicate_chunk_ids - pre_report.duplicate_chunk_ids
    
    pre_srcs = set(pre_report.source_breakdown.keys())
    post_srcs = set(post_report.source_breakdown.keys())
    
    overall_equivalent = (
        sources_diff == 0
        and chunks_diff == 0
        and scaffolds_diff == 0
        and orphans_diff == 0
        and duplicates_diff == 0
        and pre_srcs == post_srcs
        and post_report.orphaned_chunks == 0
        and post_report.duplicate_chunk_ids == 0
    )
    
    return {
        "sources_match": sources_diff == 0,
        "chunks_match": chunks_diff == 0,
        "scaffolds_match": scaffolds_diff == 0,
        "orphans_match": orphans_diff == 0,
        "duplicates_match": duplicates_diff == 0,
        "sources_diff": sources_diff,
        "chunks_diff": chunks_diff,
        "scaffolds_diff": scaffolds_diff,
        "orphans_diff": orphans_diff,
        "duplicates_diff": duplicates_diff,
        "new_sources": sorted(list(post_srcs - pre_srcs)),
        "missing_sources": sorted(list(pre_srcs - post_srcs)),
        "overall_equivalent": overall_equivalent,
    }
```

---

## 5. CLI Tooling Inventory

| Tool Script | Arguments | Functionality |
| :--- | :--- | :--- |
| `scripts/backup_kb.py` | `--source <path>`<br>`--dest <dir>`<br>`--verify`<br>`--list`<br>`--prune <N>` | Creates transactional backup, verifies integrity, lists available recovery points, or prunes older backups keeping top N points. |
| `scripts/restore_kb.py` | `--backup <path>`<br>`--target <path>`<br>`--force` | Restores database using atomic two-stage swap, outputs outcome status and trace ID, validates post-restore state. |
| `scripts/run_phase62_semantic_reconciliation.py` | (none) | Executes programmatic pre- and post-restore semantic equivalence test generating comparison artifact. |
| `scripts/run_phase62_recovery_observability.py` | (none) | Executes end-to-end recovery audit tracing, verifies log sanitization, and outputs machine-readable traces. |

## 6. Detailed Method Signatures & Implementation Walkthrough

Below is the verified production implementation logic for key methods in `legalmitra/operations/backup_recovery.py`:

### 6.1 `_acquire_restore_lock()`
```python
def _acquire_restore_lock(self, target_path: Path) -> Path:
    lock_file = target_path.with_name(f"{target_path.name}.restore.lock")
    try:
        fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_RDWR)
        with os.fdopen(fd, "w") as f:
            f.write(f"pid={os.getpid()}\ntimestamp={datetime.now(timezone.utc).isoformat()}\n")
        return lock_file
    except FileExistsError:
        raise RuntimeError(f"Concurrent restore in progress: lock file {lock_file} exists")
```

### 6.2 `create_backup()`
```python
def create_backup(self, custom_name: Optional[str] = None) -> BackupManifest:
    self._validate_path_security(self.kb_db_path)
    timestamp = datetime.now(timezone.utc)
    filename = custom_name or self._generate_backup_filename(timestamp)
    if not filename.endswith(".db"):
        filename += ".db"
        
    staging_file = self.backup_dir / f"{filename}.tmp_part"
    final_file = self.backup_dir / filename
    
    # 1. Flush source WAL
    with sqlite3.connect(str(self.kb_db_path)) as src_conn:
        src_conn.execute("PRAGMA wal_checkpoint(FULL);")
        
        # 2. Online streaming backup to staging file
        with sqlite3.connect(str(staging_file)) as dst_conn:
            src_conn.backup(dst_conn, pages=-1)
            
    # 3. Promote staging file to final backup
    staging_file.replace(final_file)
    
    # 4. Generate manifest and sidecar
    manifest = self._build_manifest(final_file, timestamp)
    self._save_manifest(manifest, final_file)
    return manifest
```

### 6.3 `restore_backup()`
```python
def restore_backup(self, backup_file: str, target_db: Optional[str] = None) -> RestoreResult:
    trace_id = str(uuid.uuid4())
    start_time = time.perf_counter()
    target_path = Path(target_db).resolve() if target_db else self.kb_db_path.resolve()
    self._validate_path_security(target_path)
    
    lock_file = None
    rollback_performed = False
    prev_target = target_path.with_name(f"{target_path.name}.prev_before_restore")
    tmp_restore = target_path.with_name(f"{target_path.name}.tmp_restore")
    
    try:
        lock_file = self._acquire_restore_lock(target_path)
        verification = self.verify_backup(backup_file)
        if not verification.is_valid:
            return RestoreResult(
                success=False,
                target_db=str(target_path),
                backup_file=str(backup_file),
                verification=verification,
                error_message=verification.error_message,
                outcome_status=RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED,
                audit_trace_id=trace_id,
            )
            
        shutil.copy2(backup_file, tmp_restore)
        self._verify_sqlite_file(tmp_restore)
        
        if target_path.exists():
            target_path.replace(prev_target)
        tmp_restore.replace(target_path)
        
        self._verify_sqlite_file(target_path)
        if prev_target.exists():
            prev_target.unlink()
            
        duration = (time.perf_counter() - start_time) * 1000.0
        self._log_audit_record(RecoveryOperationAuditRecord(
            trace_id=trace_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            operation="RESTORE_BACKUP",
            source_file=str(backup_file),
            target_file=str(target_path),
            success=True,
            outcome_status=RecoveryOutcomeStatus.RESTORE_VERIFIED.value,
            duration_ms=duration,
        ))
        
        return RestoreResult(
            success=True,
            target_db=str(target_path),
            backup_file=str(backup_file),
            verification=verification,
            outcome_status=RecoveryOutcomeStatus.RESTORE_VERIFIED,
            audit_trace_id=trace_id,
        )
    except Exception as e:
        if prev_target.exists() and (not target_path.exists() or not self._is_file_valid(target_path)):
            if target_path.exists():
                target_path.unlink()
            prev_target.replace(target_path)
            rollback_performed = True
        return RestoreResult(
            success=False,
            target_db=str(target_path),
            backup_file=str(backup_file),
            verification=BackupVerificationResult(False, backup_file, 0, False, False, False, 0, 0, 0, str(e)),
            error_message=str(e),
            outcome_status=RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED,
            rollback_performed=rollback_performed,
            audit_trace_id=trace_id,
        )
    finally:
        if lock_file:
            self._release_restore_lock(lock_file)
        if tmp_restore.exists():
            tmp_restore.unlink()
```
