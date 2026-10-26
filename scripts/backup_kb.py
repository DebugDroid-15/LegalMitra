"""
CLI Script to create, list, and manage verified LegalMitra Knowledge Base backups.
Usage:
    python scripts/backup_kb.py [--notes "Backup note"] [--backup-dir data/backups]
    python scripts/backup_kb.py --list [--backup-dir data/backups]
    python scripts/backup_kb.py --prune 5 [--backup-dir data/backups]
"""

import argparse
import sys
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def main():
    parser = argparse.ArgumentParser(description="Backup LegalMitra Knowledge Base")
    parser.add_argument("--source", default="data/legalmitra_kb.db", help="Source SQLite database path")
    parser.add_argument("--backup-dir", default="data/backups", help="Target backup directory")
    parser.add_argument("--notes", default="Phase 62 Operational Snapshot", help="Notes for the backup manifest")
    parser.add_argument("--list", action="store_true", help="List all available backups in directory")
    parser.add_argument("--prune", type=int, default=None, help="Prune backups keeping N most recent (guarded)")
    args = parser.parse_args()

    print("=== LegalMitra Knowledge Base Backup Runner ===")
    manager = KnowledgeBaseBackupManager()

    if args.list:
        backups = manager.list_backups(backup_dir=args.backup_dir)
        print(f"\nFound {len(backups)} backups in {args.backup_dir}:")
        for i, b in enumerate(backups):
            meta = b.get("metadata", {})
            print(f"  [{i+1}] {b['filename']} ({b['size_bytes']:,} bytes) - {b['modified_time_utc']}")
            if meta:
                print(f"      SHA256: {meta.get('sha256_checksum')}")
                print(f"      Sources: {meta.get('total_sources')} | Chunks: {meta.get('total_chunks')} (Scaffold: {meta.get('quarantined_scaffold_chunks')})")
        return

    if args.prune is not None:
        print(f"\nPruning backups keeping {args.prune} most recent...")
        res = manager.prune_backups(keep_count=args.prune, backup_dir=args.backup_dir)
        print(f"Result: {res['status']} - {res.get('message', '')}")
        print(f"Pruned: {res['pruned_count']} | Retained: {res['retained_count']}")
        return

    try:
        manifest = manager.create_backup(
            source_db_path=args.source,
            backup_dir=args.backup_dir,
            notes=args.notes,
        )
        print(f"[OK] Backup created successfully: {manifest.backup_id}")
        print(f"  Backup File: {manifest.backup_file_path}")
        print(f"  SHA256: {manifest.sha256_checksum}")
        print(f"  Size: {manifest.file_size_bytes:,} bytes")
        print(f"  Sources: {manifest.total_sources} | Chunks: {manifest.total_chunks} (Authentic: {manifest.authentic_chunks}, Scaffold: {manifest.quarantined_scaffold_chunks})")
        print(f"  Quarantine Compliant: {manifest.is_quarantine_compliant}")
        print(f"  Schema Version: {manifest.schema_version}")
        print(f"  SQLite Version: {manifest.sqlite_version} ({manifest.journal_mode})")
    except Exception as e:
        print(f"[FAIL] Backup creation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
