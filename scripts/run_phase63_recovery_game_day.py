"""
Phase 63 Adversarial Disaster Recovery Game Day Harness.

Executes an exhaustive, multi-scenario recovery exercise validating:
1. Known-good backup creation and cryptographic identity binding verification.
2. Controlled database corruption and fail-closed restore rejection.
3. Interrupted restore crash simulation and automated state recovery.
4. Valid restoration with deep record-level cryptographic & semantic reconciliation.
5. Post-restoration rollback to previous snapshot on demand.
6. Stale concurrency lock reclamation under simulated process termination.
7. Corpus idempotency and scaffold quarantine invariant preservation.

Outputs comprehensive JSON evidence report to:
data/22_central_legislation/phase63_recovery_game_day.json
"""

import hashlib
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager, RecoveryOutcomeStatus
from legalmitra.operations.reconciler import CorpusReconciler


def run_recovery_game_day() -> Dict[str, Any]:
    print("=" * 70)
    print("LEGALMITRA PHASE 63 ADVERSARIAL DISASTER RECOVERY GAME DAY")
    print("=" * 70)

    start_time = datetime.now(timezone.utc).isoformat()
    workspace_root = os.getcwd()
    kb_path = os.path.join(workspace_root, "data", "legalmitra_kb.db")
    gameday_dir = os.path.join(workspace_root, "data", "backups", "phase63_gameday")
    os.makedirs(gameday_dir, exist_ok=True)

    manager = KnowledgeBaseBackupManager(workspace_root=workspace_root)
    reconciler = CorpusReconciler(workspace_root=workspace_root)

    scenarios: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # Scenario 1: Baseline Known-Good Backup & Identity Binding Verification
    # -------------------------------------------------------------
    print("\n--- Scenario 1: Baseline Backup & Cryptographic Identity Binding ---")
    s1_start = time.perf_counter()
    manifest = manager.create_backup(
        source_db_path=kb_path,
        backup_dir=gameday_dir,
        notes="Phase 63 Disaster Recovery Game Day Baseline Snapshot",
    )
    s1_elapsed = time.perf_counter() - s1_start

    # Verify backup
    verification = manager.verify_backup(manifest.backup_file_path)

    # Check internal binding table directly
    bind_conn = sqlite3.connect(f"file:{manifest.backup_file_path}?mode=ro", uri=True)
    bind_cur = bind_conn.cursor()
    bind_cur.execute("SELECT backup_id, schema_version, total_chunks, target_release FROM _backup_manifest_binding")
    binding_row = bind_cur.fetchone()
    bind_conn.close()

    s1_passed = (
        verification.is_valid
        and verification.integrity_check_passed
        and verification.quarantine_intact
        and verification.total_chunks == 1515
        and binding_row is not None
        and binding_row[0] == manifest.backup_id
        and binding_row[3] == "0.63.0"
    )

    scenarios.append({
        "scenario_id": "SCENARIO-01-BASELINE-BACKUP-AND-BINDING",
        "description": "Create verified backup and validate internal SQLite identity binding table",
        "duration_seconds": round(s1_elapsed, 3),
        "passed": s1_passed,
        "details": {
            "backup_id": manifest.backup_id,
            "backup_file": manifest.backup_file_path,
            "sha256": manifest.sha256_checksum,
            "total_chunks": manifest.total_chunks,
            "binding_table_row": binding_row,
            "verification_valid": verification.is_valid,
        },
    })
    print(f"Scenario 1 Passed: {s1_passed} (Duration: {s1_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 2: Controlled Corruption & Fail-Closed Restore Rejection
    # -------------------------------------------------------------
    print("\n--- Scenario 2: Controlled Corruption & Fail-Closed Restore ---")
    s2_start = time.perf_counter()
    corrupt_backup_path = os.path.join(gameday_dir, "corrupted_test_snapshot.db")
    shutil.copy2(manifest.backup_file_path, corrupt_backup_path)

    # Corrupt database header and middle sectors
    with open(corrupt_backup_path, "r+b") as f:
        f.seek(16)
        f.write(b"\x00\x00\x00\x00\x00\x00\x00\x00")
        f.seek(1024)
        f.write(b"CORRUPTED_LEGALMITRA_DATA_TEST_PAYLOAD" * 10)

    # Attempt restore to an isolated test target
    mock_target = os.path.join(gameday_dir, "mock_target_corrupt.db")
    shutil.copy2(kb_path, mock_target)

    restore_res_corrupt = manager.restore_backup(
        backup_file_path=corrupt_backup_path,
        target_db_path=mock_target,
    )

    s2_elapsed = time.perf_counter() - s2_start
    s2_passed = (
        not restore_res_corrupt.success
        and restore_res_corrupt.original_preserved
        and restore_res_corrupt.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
    )

    # Clean up mock target
    if os.path.exists(mock_target):
        os.remove(mock_target)

    scenarios.append({
        "scenario_id": "SCENARIO-02-CORRUPTION-FAIL-CLOSED",
        "description": "Simulate byte-level database corruption and verify fail-closed restore refusal",
        "duration_seconds": round(s2_elapsed, 3),
        "passed": s2_passed,
        "details": {
            "corrupt_backup_path": corrupt_backup_path,
            "outcome_status": restore_res_corrupt.outcome_status,
            "error_message": restore_res_corrupt.error_message,
            "original_preserved": restore_res_corrupt.original_preserved,
        },
    })
    print(f"Scenario 2 Passed: {s2_passed} (Duration: {s2_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 3: Interrupted Restore Simulation & Auto-Recovery
    # -------------------------------------------------------------
    print("\n--- Scenario 3: Interrupted Restore Crash & Auto-Recovery ---")
    s3_start = time.perf_counter()
    mock_target_crash = os.path.join(gameday_dir, "mock_target_crash.db")
    shutil.copy2(kb_path, mock_target_crash)

    # Simulate mid-restore interruption: mock_target_crash moved to .prev_before_restore, target deleted
    prev_snapshot = mock_target_crash + ".prev_before_restore"
    if os.path.exists(prev_snapshot):
        os.remove(prev_snapshot)
    shutil.move(mock_target_crash, prev_snapshot)

    # Assert target missing, snapshot present
    assert not os.path.exists(mock_target_crash)
    assert os.path.exists(prev_snapshot)

    # Execute auto-recovery
    rec_res = manager.recover_interrupted_restore(mock_target_crash)
    recovered = rec_res["recovered_from_prev"]
    rec_msg = f"recovered_from_prev={recovered}, target_healthy={rec_res['target_healthy']}"

    # Check that mock_target_crash is restored and healthy
    check_conn = sqlite3.connect(f"file:{mock_target_crash}?mode=ro", uri=True)
    check_chunks = check_conn.cursor().execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
    check_conn.close()

    s3_elapsed = time.perf_counter() - s3_start
    s3_passed = recovered and os.path.exists(mock_target_crash) and check_chunks == 1515

    if os.path.exists(mock_target_crash):
        os.remove(mock_target_crash)
    if os.path.exists(prev_snapshot):
        os.remove(prev_snapshot)

    scenarios.append({
        "scenario_id": "SCENARIO-03-INTERRUPTED-RESTORE-AUTO-RECOVERY",
        "description": "Simulate process crash during target replacement and verify automated state recovery",
        "duration_seconds": round(s3_elapsed, 3),
        "passed": s3_passed,
        "details": {
            "recovery_message": rec_msg,
            "target_restored_chunks": check_chunks,
        },
    })
    print(f"Scenario 3 Passed: {s3_passed} (Duration: {s3_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 4: Valid Restore & Deep Record-Level Reconciliation
    # -------------------------------------------------------------
    print("\n--- Scenario 4: Valid Restore & Deep Record-Level Reconciliation ---")
    s4_start = time.perf_counter()
    mock_target_valid = os.path.join(gameday_dir, "mock_target_valid.db")
    shutil.copy2(kb_path, mock_target_valid)

    restore_res_valid = manager.restore_backup(
        backup_file_path=manifest.backup_file_path,
        target_db_path=mock_target_valid,
        keep_previous_snapshot=True,
    )

    # Run deep record-level comparison
    deep_diff = reconciler.compare_databases_deep(kb_path, mock_target_valid)

    s4_elapsed = time.perf_counter() - s4_start
    s4_passed = (
        restore_res_valid.success
        and restore_res_valid.outcome_status == RecoveryOutcomeStatus.RESTORE_VERIFIED.value
        and deep_diff["is_identical"]
        and deep_diff["chunk_count_match"]
        and deep_diff["source_count_match"]
        and len(deep_diff["content_checksum_mismatches"]) == 0
        and len(deep_diff["quarantine_status_mismatches"]) == 0
    )

    scenarios.append({
        "scenario_id": "SCENARIO-04-VALID-RESTORE-DEEP-RECONCILIATION",
        "description": "Perform valid restore and cryptographically verify all 1,515 chunk records match exactly",
        "duration_seconds": round(s4_elapsed, 3),
        "passed": s4_passed,
        "details": {
            "restored_chunks": restore_res_valid.restored_chunks,
            "restored_sources": restore_res_valid.restored_sources,
            "is_semantically_identical": deep_diff["is_identical"],
            "checksum_mismatches": len(deep_diff["content_checksum_mismatches"]),
            "quarantine_mismatches": len(deep_diff["quarantine_status_mismatches"]),
        },
    })
    print(f"Scenario 4 Passed: {s4_passed} (Duration: {s4_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 5: Post-Restore Manual Rollback
    # -------------------------------------------------------------
    print("\n--- Scenario 5: Post-Restore Manual Rollback ---")
    s5_start = time.perf_counter()
    # mock_target_valid currently has a .prev_before_restore snapshot preserved
    prev_snapshot_path = mock_target_valid + ".prev_before_restore"
    assert os.path.exists(prev_snapshot_path), "Expected prev snapshot to exist"

    # Execute rollback
    rollback_res = manager.rollback_from_previous(mock_target_valid)

    # Validate rolled back state
    s5_elapsed = time.perf_counter() - s5_start
    s5_passed = (
        rollback_res.success
        and rollback_res.restored_chunks == 1515
        and rollback_res.verification.quarantine_intact
        and not os.path.exists(prev_snapshot_path)
    )

    if os.path.exists(mock_target_valid):
        os.remove(mock_target_valid)

    scenarios.append({
        "scenario_id": "SCENARIO-05-POST-RESTORE-ROLLBACK",
        "description": "Trigger rollback_from_previous to revert target DB to previous pre-restore snapshot",
        "duration_seconds": round(s5_elapsed, 3),
        "passed": s5_passed,
        "details": {
            "rolled_back_chunks": rollback_res.restored_chunks,
            "quarantine_compliant": rollback_res.verification.quarantine_intact,
        },
    })
    print(f"Scenario 5 Passed: {s5_passed} (Duration: {s5_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 6: Stale Concurrency Lock Reclamation
    # -------------------------------------------------------------
    print("\n--- Scenario 6: Stale Concurrency Lock Reclamation ---")
    s6_start = time.perf_counter()
    mock_target_lock = os.path.join(gameday_dir, "mock_target_lock.db")
    shutil.copy2(kb_path, mock_target_lock)
    lock_file = mock_target_lock + ".restore.lock"

    # Create stale lock file with dead PID (PID 999999)
    with open(lock_file, "w", encoding="utf-8") as f:
        f.write("PID:999999 TIME:2026-01-01T00:00:00Z\n")

    # Verify lock detected as stale
    is_stale, recorded_pid = manager.is_lock_stale(lock_file)

    # Perform restore which should automatically reclaim stale lock and succeed
    restore_reclaim = manager.restore_backup(
        backup_file_path=manifest.backup_file_path,
        target_db_path=mock_target_lock,
        keep_previous_snapshot=False,
    )

    s6_elapsed = time.perf_counter() - s6_start
    s6_passed = is_stale and recorded_pid == 999999 and restore_reclaim.success and not os.path.exists(lock_file)

    if os.path.exists(mock_target_lock):
        os.remove(mock_target_lock)

    scenarios.append({
        "scenario_id": "SCENARIO-06-STALE-LOCK-RECLAMATION",
        "description": "Simulate dead process lockfile and verify automated safe lock reclamation",
        "duration_seconds": round(s6_elapsed, 3),
        "passed": s6_passed,
        "details": {
            "stale_detected": is_stale,
            "recorded_pid": recorded_pid,
            "restore_succeeded_after_reclaim": restore_reclaim.success,
        },
    })
    print(f"Scenario 6 Passed: {s6_passed} (Duration: {s6_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Scenario 7: Corpus Quarantine & Isolation Invariants Verification
    # -------------------------------------------------------------
    print("\n--- Scenario 7: Corpus Quarantine & Isolation Invariants ---")
    s7_start = time.perf_counter()
    full_recon = reconciler.run_full_reconciliation()
    s7_elapsed = time.perf_counter() - s7_start

    s7_passed = (
        full_recon.overall_status == "PASSED"
        and full_recon.total_sources == 62
        and full_recon.total_chunks == 1515
        and full_recon.scaffold_quarantine_compliant
        and full_recon.quarantined_chunks == 6
        and full_recon.review_package_records == 40
        and full_recon.review_package_pending_count == 40
        and full_recon.benchmark_contamination_clean
    )

    scenarios.append({
        "scenario_id": "SCENARIO-07-CORPUS-QUARANTINE-AND-ISOLATION",
        "description": "Verify zero drift on primary knowledge base, scaffold quarantine, and review packages",
        "duration_seconds": round(s7_elapsed, 3),
        "passed": s7_passed,
        "details": {
            "overall_status": full_recon.overall_status,
            "total_sources": full_recon.total_sources,
            "total_chunks": full_recon.total_chunks,
            "quarantined_chunks": full_recon.quarantined_chunks,
            "review_pending_count": full_recon.review_package_pending_count,
        },
    })
    print(f"Scenario 7 Passed: {s7_passed} (Duration: {s7_elapsed:.2f}s)")

    # -------------------------------------------------------------
    # Summary & Output
    # -------------------------------------------------------------
    end_time = datetime.now(timezone.utc).isoformat()
    total_scenarios = len(scenarios)
    passed_scenarios = sum(1 for s in scenarios if s["passed"])
    failed_scenarios = total_scenarios - passed_scenarios

    game_day_report = {
        "report_id": f"GAMEDAY-PHASE63-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "target_release": "0.63.0",
        "start_time_utc": start_time,
        "end_time_utc": end_time,
        "overall_status": "PASSED" if failed_scenarios == 0 else "FAILED",
        "total_scenarios": total_scenarios,
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "scenarios": scenarios,
    }

    out_path = os.path.join(workspace_root, "data", "22_central_legislation", "phase63_recovery_game_day.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(game_day_report, f, indent=2)

    print("\n" + "=" * 70)
    print(f"GAME DAY COMPLETE: {passed_scenarios}/{total_scenarios} scenarios passed.")
    print(f"Report saved to: {out_path}")
    print("=" * 70)
    return game_day_report


if __name__ == "__main__":
    rep = run_recovery_game_day()
    if rep["failed_scenarios"] > 0:
        sys.exit(1)
