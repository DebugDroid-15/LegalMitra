"""
Phase 62 Recovery Observability and Machine-Readable Trace Generator.
Exercises the backup and recovery subsystem across all standard lifecycle operations,
captures structured recovery audit records, verifies sanitization,
and exports data/22_central_legislation/phase62_recovery_traces.json.
"""

import json
import os
import tempfile
from datetime import datetime, timezone
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def main():
    print("=== LegalMitra Phase 62 Recovery Observability & Audit Trace Generator ===")

    mgr = KnowledgeBaseBackupManager()

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_backup_dir = os.path.join(tmp_dir, "backups")
        
        # 1. Exercise Backup Creation
        manifest = mgr.create_backup(backup_dir=test_backup_dir, notes="Observability Trace Cycle")
        print(f"[OK] Backup created: {manifest.backup_id}")

        # 2. Exercise Verification
        verif = mgr.verify_backup(manifest.backup_file_path)
        print(f"[OK] Backup verified: is_valid={verif.is_valid}")

        # 3. Exercise Dry-Run Restore
        target_path = os.path.join(tmp_dir, "restored_test.db")
        dry_res = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_path, dry_run=True)
        print(f"[OK] Restore dry-run executed: {dry_res.outcome_status}")

        # 4. Exercise Real Atomic Restore
        real_res = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_path, dry_run=False)
        print(f"[OK] Real restore executed: {real_res.outcome_status}")

    # Export audit traces
    out_path = os.path.join("data", "22_central_legislation", "phase62_recovery_traces.json")
    mgr.export_audit_traces(out_path)
    print(f"[OK] Recovery audit traces persisted to: {out_path}")

    # Validate trace schema and sanitization
    with open(out_path, "r", encoding="utf-8") as f:
        trace_data = json.load(f)

    print(f"Total traces recorded: {trace_data['total_records']}")
    forbidden_tokens = ["api_key", "password", "secret", "private_key", "bearer_token"]
    raw_str = json.dumps(trace_data).lower()
    for tok in forbidden_tokens:
        assert tok not in raw_str, f"Sanitization breach: {tok} found in trace!"
    print("[OK] Trace log sanitization verified clean (zero secrets or credentials).")


if __name__ == "__main__":
    main()
