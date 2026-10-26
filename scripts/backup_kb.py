"""
CLI Script to create a verified LegalMitra Knowledge Base backup.
Usage:
    python scripts/backup_kb.py [--notes "Backup note"] [--backup-dir data/backups]
"""

import argparse
import sys
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def main():
    parser = argparse.ArgumentParser(description="Backup LegalMitra Knowledge Base")
    parser.add_argument("--source", default="data/legalmitra_kb.db", help="Source SQLite database path")
    parser.add_argument("--backup-dir", default="data/backups", help="Target backup directory")
    parser.add_argument("--notes", default="Phase 61 Operational Snapshot", help="Notes for the backup manifest")
    args = parser.parse_args()

    print("=== LegalMitra Knowledge Base Backup Runner ===")
    manager = KnowledgeBaseBackupManager()

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
    except Exception as e:
        print(f"[FAIL] Backup creation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
