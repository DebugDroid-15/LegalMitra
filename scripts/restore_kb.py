"""
CLI Script to restore and verify a LegalMitra Knowledge Base backup.
Usage:
    python scripts/restore_kb.py --backup <path-to-db> [--target <target-db>] [--dry-run]
"""

import argparse
import sys
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def main():
    parser = argparse.ArgumentParser(description="Restore LegalMitra Knowledge Base")
    parser.add_argument("--backup", required=True, help="Path to backup database file")
    parser.add_argument("--target", default="data/legalmitra_kb.db", help="Target database path")
    parser.add_argument("--dry-run", action="store_true", help="Validate and simulate restore without overwriting")
    args = parser.parse_args()

    print("=== LegalMitra Knowledge Base Restore Runner ===")
    manager = KnowledgeBaseBackupManager()

    result = manager.restore_backup(
        backup_file_path=args.backup,
        target_db_path=args.target,
        dry_run=args.dry_run,
    )

    if result.success:
        print(f"[OK] Restore {'dry-run' if result.is_dry_run else 'execution'} SUCCESSFUL!")
        print(f"  Source Backup: {result.backup_file_path}")
        print(f"  Target DB:     {result.target_path}")
        print(f"  Restored Sources: {result.restored_sources} | Chunks: {result.restored_chunks}")
        print(f"  Integrity Verified: {result.verification.integrity_check_passed}")
        print(f"  Quarantine Intact:  {result.verification.quarantine_intact}")
    else:
        print(f"[FAIL] Restore FAILED: {result.error_message}", file=sys.stderr)
        for err in result.verification.errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
