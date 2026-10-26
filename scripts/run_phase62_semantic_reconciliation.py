"""
Phase 62 Semantic Reconciliation and Pre/Post Restoration Comparison Generator.
Conducts an isolated backup and restore cycle on disposable databases,
compares pre- and post-restoration semantic invariants,
and exports data/22_central_legislation/phase62_post_restore_comparison.json.
"""

import json
import os
import shutil
import tempfile
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager
from legalmitra.operations.reconciler import CorpusReconciler


def main():
    print("=== LegalMitra Phase 62 Post-Restore Semantic Reconciliation Runner ===")

    reconciler = CorpusReconciler()
    pre_report = reconciler.run_full_reconciliation()
    print(f"[OK] Pre-restoration inventory captured: {pre_report.total_sources} sources, {pre_report.total_chunks} chunks.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_mgr = KnowledgeBaseBackupManager(workspace_root=os.getcwd())
        test_backup_dir = os.path.join(tmp_dir, "backups")
        
        # 1. Create verified test backup
        manifest = backup_mgr.create_backup(backup_dir=test_backup_dir, notes="Phase 62 Semantic Comparison Test")
        print(f"[OK] Created test backup: {manifest.backup_id} (SHA-256: {manifest.sha256_checksum[:16]}...)")

        # 2. Restore into disposable target database
        disposable_target = os.path.join(tmp_dir, "restored_kb.db")
        restore_res = backup_mgr.restore_backup(manifest.backup_file_path, target_db_path=disposable_target, dry_run=False)
        assert restore_res.success, f"Restore failed: {restore_res.error_message}"
        print(f"[OK] Restored backup into disposable target: {disposable_target}")

        # 3. Reconcile post-restoration database
        post_reconciler = CorpusReconciler()
        post_reconciler.db_path = disposable_target
        post_report = post_reconciler.run_full_reconciliation()
        print(f"[OK] Post-restoration inventory captured: {post_report.total_sources} sources, {post_report.total_chunks} chunks.")

        # 4. Deep differential comparison
        comparison = reconciler.compare_pre_and_post_restore(pre_report, post_report)
        print(f"\nSemantic Comparison Status: {comparison['status']}")
        print(f"Semantically Identical:     {comparison['is_semantically_identical']}")
        print(f"Source Difference:          {comparison['metrics']['source_difference']}")
        print(f"Chunk Difference:           {comparison['metrics']['chunk_difference']}")
        print(f"Scaffold Difference:        {comparison['metrics']['scaffold_difference']}")
        print(f"Orphans in Post-Restore:    {comparison['metrics']['post_orphaned_chunks']}")
        print(f"Quarantine Preserved:       {comparison['quarantine_preserved']}")

        # 5. Persist comparison artifact
        out_path = os.path.join("data", "22_central_legislation", "phase62_post_restore_comparison.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(comparison, f, indent=2)
        print(f"\n[OK] Persisted comparison artifact to: {out_path}")


if __name__ == "__main__":
    main()
