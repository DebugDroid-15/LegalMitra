"""
CLI Script to restore and verify a LegalMitra Knowledge Base backup.
Usage:
    python scripts/restore_kb.py --backup <path-to-db> [--target <target-db>] [--dry-run] [--no-keep-prev]
    python scripts/restore_kb.py --rollback [--target <target-db>]
    python scripts/restore_kb.py --commit-restore [--target <target-db>]
    python scripts/restore_kb.py --reclaim-lock [--target <target-db>]
    python scripts/restore_kb.py --recover-interrupted [--target <target-db>]
"""

import argparse
import sys
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def main():
    parser = argparse.ArgumentParser(description="Restore and Manage LegalMitra Knowledge Base Recovery")
    parser.add_argument("--backup", default=None, help="Path to backup database file")
    parser.add_argument("--target", default="data/legalmitra_kb.db", help="Target database path")
    parser.add_argument("--dry-run", action="store_true", help="Validate and simulate restore without overwriting")
    parser.add_argument("--no-keep-prev", action="store_true", help="Discard previous pre-restore snapshot immediately")
    parser.add_argument("--rollback", action="store_true", help="Roll back to previous database snapshot (.prev_before_restore)")
    parser.add_argument("--commit-restore", action="store_true", help="Commit restoration by removing saved previous snapshot")
    parser.add_argument("--reclaim-lock", action="store_true", help="Reclaim stale lock if previous operation crashed")
    parser.add_argument("--recover-interrupted", action="store_true", help="Recover interrupted restore if target is missing and snapshot exists")
    args = parser.parse_args()

    print("=== LegalMitra Knowledge Base Restore Runner ===")
    manager = KnowledgeBaseBackupManager()

    if args.reclaim_lock:
        print(f"Reclaiming stale lock for target {args.target}...")
        rec_res = manager.reclaim_stale_lock(args.target)
        print(f"Result: {rec_res['status']} (reclaimed={rec_res['reclaimed']})")
        if not rec_res["reclaimed"] and rec_res["status"] != "NO_LOCK_PRESENT":
            sys.exit(1)
        return

    if args.recover_interrupted:
        print(f"Checking and recovering interrupted restore for {args.target}...")
        rec_res = manager.recover_interrupted_restore(args.target)
        print(f"Result: recovered_from_prev={rec_res['recovered_from_prev']}, target_healthy={rec_res['target_healthy']}")
        if not rec_res["target_healthy"]:
            sys.exit(1)
        return

    if args.rollback:
        print(f"Rolling back {args.target} from previous snapshot...")
        try:
            rb_res = manager.rollback_from_previous(args.target)
            print(f"[OK] Rollback successful! Restored {rb_res.restored_chunks} chunks from previous snapshot.")
        except Exception as e:
            print(f"[FAIL] Rollback failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.commit_restore:
        print(f"Committing restoration for {args.target}...")
        committed = manager.commit_restoration(args.target)
        if committed:
            print("[OK] Restoration committed successfully (previous snapshot removed).")
        else:
            print("[INFO] No pending previous snapshot to clean up.")
        return

    if not args.backup:
        print("[FAIL] --backup path is required for restore operation.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    result = manager.restore_backup(
        backup_file_path=args.backup,
        target_db_path=args.target,
        dry_run=args.dry_run,
        keep_previous_snapshot=not args.no_keep_prev,
    )

    print(f"\nRecovery Outcome Status: {result.outcome_status}")
    print(f"Original Database Preserved: {result.original_preserved}")
    print(f"Rollback Performed: {result.rollback_performed}")
    print(f"Audit Trace ID: {result.audit_trace_id}")
    if result.previous_snapshot_path:
        print(f"Previous Snapshot Preserved: {result.previous_snapshot_path}")

    if result.success:
        print(f"\n[OK] Restore {'dry-run' if result.is_dry_run else 'execution'} SUCCESSFUL!")
        print(f"  Source Backup: {result.backup_file_path}")
        print(f"  Target DB:     {result.target_path}")
        print(f"  Restored Sources: {result.restored_sources} | Chunks: {result.restored_chunks}")
        print(f"  Integrity Verified: {result.verification.integrity_check_passed}")
        print(f"  Quarantine Intact:  {result.verification.quarantine_intact}")
    else:
        print(f"\n[FAIL] Restore FAILED: {result.error_message}", file=sys.stderr)
        for err in result.verification.errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
