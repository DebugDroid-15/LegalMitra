# PHASE 62 RELEASE GATE NEGATIVE CONTROLS
**Module:** `legalmitra.evaluation.release_gates`  
**Test Suite:** `tests/test_phase62_disaster_recovery_assurance.py`  
**Target Release:** 0.62.0  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Purpose of Negative Controls

Release gates that only pass are vulnerable to false confidence. Fail-closed negative controls prove that release gates actively detect invalid conditions and immediately transition to `FAILED` status when integrity boundaries are violated.

---

## 2. Injected Negative Control Scenarios

### Negative Control 20.1: Tampered Backup Checksum
- **Injection:** Injected a modified `.meta.json` sidecar file where the SHA-256 hash was altered to `0000000000000000000000000000000000000000000000000000000000000000`.
- **Expected Behavior:** `ReleaseGateEvaluator` fails RG-20 with status `FAILED` and descriptive error message.
- **Observed Behavior:** RG-20 evaluated to `FAILED` (`"Backup verification failed: SHA-256 hash mismatch"`).
- **Test:** `test_release_gate_negative_control_tampered_backup` PASSED.

### Negative Control 20.2: Truncated Database Header
- **Injection:** Created a backup file containing only 32 bytes of random data.
- **Expected Behavior:** `verify_backup()` returns `is_valid = False` due to SQLite header parsing failure.
- **Observed Behavior:** Verification failed with `file is not a database`.
- **Test:** `test_restore_truncated_backup_fails_closed` PASSED.

### Negative Control 20.3: Unsupported Schema Version
- **Injection:** Created sidecar metadata specifying `schema_version = "99.0.0"`.
- **Expected Behavior:** Pre-flight restore check rejects backup as incompatible with engine version `1.0.0`.
- **Observed Behavior:** Restore blocked fail-closed; target unmodified.
- **Test:** `test_restore_unsupported_schema_version_fails_closed` PASSED.

### Negative Control 20.4: Orphaned Chunk Injection
- **Injection:** Inserted chunk into backup database referencing non-existent authority `ORPHAN-SRC-999`.
- **Expected Behavior:** Pre-flight foreign key reconciliation detects orphaned chunk and rejects restore.
- **Observed Behavior:** Restore aborted with `Orphaned chunks detected in backup (1 chunks)`; target preserved.
- **Test:** `test_restore_orphaned_chunks_fails_closed` PASSED.

### Negative Control 20.5: Concurrent Restore Contention
- **Injection:** Created unreleased lock file `data/legalmitra_kb.db.restore.lock` and invoked restore.
- **Expected Behavior:** Restore immediately aborts with concurrency lock error without attempting to write to target.
- **Observed Behavior:** Restore rejected with `Concurrent restore in progress`.
- **Test:** `test_restore_concurrent_lock_prevents_collision` PASSED.

---

## 3. Negative Controls Summary Across Releases

| Release Gate | Injected Failure Mode | Detected By | Gate Transition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **RG-01** | Injected failing test | Evaluator | PASS -> FAIL | VERIFIED |
| **RG-02** | Injected orphaned chunk | Corpus Reconciler | PASS -> FAIL | VERIFIED |
| **RG-03** | Injected table `chat_sessions` | Decoupling Audit | PASS -> FAIL | VERIFIED |
| **RG-04** | Set `is_synthetic_scaffold = 0` | Quarantine Audit | PASS -> FAIL | VERIFIED |
| **RG-05** | Modified byte in `data/06_review/` | Freeze Verifier | PASS -> FAIL | VERIFIED |
| **RG-11** | Attempted auto-signoff | Advocate Verifier | PENDING -> FAIL | VERIFIED |
| **RG-19** | SSRF loopback IP `127.0.0.1` | Network Adapter | PASS -> FAIL | VERIFIED |
| **RG-20** | Tampered backup SHA-256 | Backup Manager | PASS -> FAIL | VERIFIED |

---

## 4. Conclusion

All 8 major release gate negative controls operated deterministically. No release gate allowed invalid, corrupted, or unverified artifacts to slip through without triggering an explicit failure.

## 5. Fail-Closed Test Automation Architecture

The negative control tests are integrated directly into the automated CI test harness:

```python
def test_release_gate_negative_control_tampered_backup(tmp_path):
    # Setup test backup
    kb_mgr = KnowledgeBaseBackupManager(db_path, backup_dir=tmp_path)
    manifest = kb_mgr.create_backup("test_negative.db")
    meta_path = tmp_path / "test_negative.db.meta.json"
    
    # Tamper with recorded SHA-256
    with open(meta_path, "r") as f:
        meta = json.load(f)
    meta["sha256_hash"] = "0" * 64
    with open(meta_path, "w") as f:
        json.dump(meta, f)
        
    # Evaluate RG-20
    evaluator = ReleaseGateEvaluator(data_dir=str(data_dir))
    gate_result = evaluator._eval_rg20_backup_disaster_recovery()
    
    # Strict fail-closed assertions
    assert gate_result["status"] == "FAILED"
    assert "SHA-256 hash mismatch" in gate_result["reason"]
```

This verifies that the release gate cannot be tricked by corrupted or altered sidecars.
