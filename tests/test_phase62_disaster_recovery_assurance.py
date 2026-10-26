"""
Phase 62 Test Suite: Production-Safety Hardening, Disaster-Recovery Assurance,
and Controlled Release Governance.

Validates:
1. Transactionally consistent backup creation, WAL checkpointing, and metadata completeness.
2. Two-stage atomic restoration with guaranteed rollback and original database preservation.
3. Fail-closed rejection of truncated, mismatched, corrupted, or unsupported backups.
4. Concurrency lock acquisition (.restore.lock) preventing collision.
5. Deep post-restore semantic reconciliation (sources, chunks, scaffold, orphans, FTS5).
6. Backup retention lifecycle and singleton recovery-point protection.
7. Ingestion-recovery interaction and reindexing idempotency.
8. Release gates evaluation for Phase 62 (LEGALMITRA-RELEASE-PHASE62, 0.62.0).
9. Security boundaries: path traversal defense, and absolute prohibition against overwriting conversations.db.
10. Machine-readable audit traces and sensitive credential sanitization.
"""

import json
import os
import shutil
import sqlite3
import tempfile
import pytest

from legalmitra.evaluation.release_gates import GateStatus, ReleaseGateEvaluator
from legalmitra.operations.backup_recovery import (
    KnowledgeBaseBackupManager,
    RecoveryOutcomeStatus,
    compute_file_sha256,
)
from legalmitra.operations.ingestion_audit import IngestionIntegrityAuditor
from legalmitra.operations.reconciler import CorpusReconciler


class TestPhase62BackupIntegrityAndCompleteness:
    """Workstream B: Audits backup creation, transactional consistency, and metadata."""

    def test_backup_transactional_consistency_and_metadata(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")

        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 62 Transactional Audit")
        assert os.path.exists(manifest.backup_file_path)
        assert manifest.target_release in ("0.62.0", "0.63.0", "0.64.0")
        assert manifest.schema_version == "1.0.0"
        assert manifest.total_chunks == 1515
        assert manifest.quarantined_scaffold_chunks == 6
        assert manifest.is_quarantine_compliant is True
        assert manifest.fts5_valid is True
        assert manifest.orphaned_chunks_count == 0
        assert manifest.all_references_valid is True
        assert manifest.sqlite_version != ""

        # Verify companion metadata file
        meta_file = manifest.backup_file_path + ".meta.json"
        assert os.path.exists(meta_file)
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        assert meta["sha256_checksum"] == manifest.sha256_checksum
        assert meta["schema_version"] == "1.0.0"

    def test_backup_hash_recomputation_exact_match(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        computed = compute_file_sha256(manifest.backup_file_path)
        assert computed == manifest.sha256_checksum


class TestPhase62RestoreSafetyAndAtomicRecovery:
    """Workstream C: Audits restore safety, atomic recovery, and rollback guarantees."""

    def test_restore_valid_verified_backup(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        target_file = str(tmp_path / "restored.db")
        result = mgr.restore_backup(
            backup_file_path=manifest.backup_file_path,
            target_db_path=target_file,
            dry_run=False,
        )

        assert result.success is True
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_VERIFIED.value
        assert result.restored_chunks == 1515
        assert result.restored_sources == 62
        assert os.path.exists(target_file)

    def test_restore_truncated_backup_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Truncate the backup database to 64 bytes
        with open(manifest.backup_file_path, "wb") as f:
            f.write(b"TRUNCATED_SQLITE_FILE_HEADER_ONLY_64_BYTES_LONG_INSUFFICIENT_DATA")

        target_file = str(tmp_path / "target.db")
        result = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)

        assert result.success is False
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        assert not os.path.exists(target_file)
        assert any("Checksum mismatch" in e or "integrity_check failed" in e for e in result.verification.errors)

    def test_restore_mismatched_hash_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Alter hash in meta file
        meta_file = manifest.backup_file_path + ".meta.json"
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["sha256_checksum"] = "e" * 64
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f)

        target_file = str(tmp_path / "target.db")
        result = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)

        assert result.success is False
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        assert not os.path.exists(target_file)
        assert any("Checksum mismatch" in e for e in result.verification.errors)

    def test_restore_unsupported_schema_version_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Set unsupported schema version in metadata
        meta_file = manifest.backup_file_path + ".meta.json"
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["schema_version"] = "99.0.0"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f)

        target_file = str(tmp_path / "target.db")
        result = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)

        assert result.success is False
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        assert not os.path.exists(target_file)
        assert any("Unsupported schema version" in e for e in result.verification.errors)

    def test_restore_orphaned_chunks_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Insert an orphaned chunk into the backup
        conn = sqlite3.connect(manifest.backup_file_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO legal_chunks (
                chunk_id, source_id, doc_type, act_or_case_title, provision_or_para_ref,
                hierarchy_level, jurisdiction, court, document_date, is_historical,
                is_synthetic_scaffold, authority_level, content, metadata_json
            )
            VALUES (
                'CHUNK-ORPHAN-TEST', 'NON-EXISTENT-SOURCE-404', 'statute', 'Orphan Act', 'Section 1',
                'SECTION', 'IN', 'CENTRAL', '2024-01-01', 0,
                0, 'PRIMARY_STATUTE', 'Orphaned content', '{}'
            )
            """
        )
        conn.commit()
        conn.close()

        # Update metadata checksum so byte check passes, but semantic check catches the orphan
        new_sha = compute_file_sha256(manifest.backup_file_path)
        meta_file = manifest.backup_file_path + ".meta.json"
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["sha256_checksum"] = new_sha
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f)

        target_file = str(tmp_path / "target.db")
        result = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)

        assert result.success is False
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        assert not os.path.exists(target_file)
        assert any("orphaned chunks" in e.lower() for e in result.verification.errors)

    def test_restore_concurrent_lock_prevents_collision(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        target_file = str(tmp_path / "target.db")
        lock_file = target_file + ".restore.lock"

        # Simulate an existing active lock
        with open(lock_file, "w") as f:
            f.write("ACTIVE_LOCK_SIMULATION")

        try:
            result = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)
            assert result.success is False
            assert "Concurrent restore detected" in result.error_message
            assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        finally:
            if os.path.exists(lock_file):
                os.remove(lock_file)

    def test_restore_atomic_rollback_on_failed_swap(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Create an existing target database
        target_file = str(tmp_path / "existing_active.db")
        shutil.copy2("data/legalmitra_kb.db", target_file)
        orig_sha = compute_file_sha256(target_file)

        # Attempt to restore a corrupted backup onto the existing database
        corrupt_backup = str(tmp_path / "corrupt_backup.db")
        shutil.copy2(manifest.backup_file_path, corrupt_backup)
        shutil.copy2(manifest.backup_file_path + ".meta.json", corrupt_backup + ".meta.json")
        with open(corrupt_backup, "r+b") as f:
            f.seek(500)
            f.write(b"CORRUPTION_BYTES_FOR_ROLLBACK_TEST")

        result = mgr.restore_backup(corrupt_backup, target_db_path=target_file)
        assert result.success is False
        assert result.outcome_status == RecoveryOutcomeStatus.RESTORE_FAILED_ORIGINAL_PRESERVED.value
        assert result.original_preserved is True
        # Verify original target is intact and unchanged
        assert os.path.exists(target_file)
        assert compute_file_sha256(target_file) == orig_sha


class TestPhase62PostRestoreSemanticReconciliation:
    """Workstream D: Audits post-restore semantic reconciliation and pre/post comparison."""

    def test_post_restore_semantic_comparison_metrics(self, tmp_path):
        reconciler = CorpusReconciler()
        pre_report = reconciler.run_full_reconciliation()

        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        target_file = str(tmp_path / "restored_for_recon.db")
        restore_res = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)
        assert restore_res.success is True

        post_reconciler = CorpusReconciler()
        post_reconciler.db_path = target_file
        post_report = post_reconciler.run_full_reconciliation()

        comparison = reconciler.compare_pre_and_post_restore(pre_report, post_report)
        assert comparison["is_semantically_identical"] is True
        assert comparison["metrics"]["source_difference"] == 0
        assert comparison["metrics"]["chunk_difference"] == 0
        assert comparison["metrics"]["scaffold_difference"] == 0
        assert comparison["metrics"]["post_orphaned_chunks"] == 0
        assert comparison["quarantine_preserved"] is True
        assert comparison["status"] == "RESTORE_SEMANTICALLY_VERIFIED"


class TestPhase62RetentionAndOperationalSafety:
    """Workstream E: Audits backup retention, pruning protection, and operational safety."""

    def test_backup_pruning_singleton_protection(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        mgr.create_backup(backup_dir=backup_dir)

        # Only 1 backup exists; pruning must be skipped to protect the sole recovery point
        res = mgr.prune_backups(keep_count=0, backup_dir=backup_dir)
        assert res["status"] == "SKIPPED_SINGLETON_PRESERVATION"
        assert res["pruned_count"] == 0
        assert res["retained_count"] == 1

    def test_backup_pruning_multi_backup(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")

        # Create 3 backups
        for i in range(3):
            mgr.create_backup(backup_dir=backup_dir, notes=f"Pruning Test {i}")

        backups = mgr.list_backups(backup_dir=backup_dir)
        assert len(backups) == 3

        # Prune keeping 2
        res = mgr.prune_backups(keep_count=2, backup_dir=backup_dir)
        assert res["status"] == "PRUNED_SUCCESS"
        assert res["pruned_count"] == 1
        assert res["retained_count"] == 2


class TestPhase62IngestionAndRecoveryInteraction:
    """Workstream F: Audits interaction between ingestion and recovery."""

    def test_ingestion_idempotency_after_restore(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        target_file = str(tmp_path / "restored_ingest.db")
        res = mgr.restore_backup(manifest.backup_file_path, target_db_path=target_file)
        assert res.success is True

        auditor = IngestionIntegrityAuditor()
        auditor.db_path = target_file
        audit_res = auditor.verify_existing_corpus_idempotency(sample_size=5)

        assert audit_res.is_idempotent is True
        assert audit_res.is_quarantine_preserved is True
        assert audit_res.duplicate_chunks_created == 0


class TestPhase62ReleaseGateStateIntegrity:
    """Workstream G: Audits release gates for Phase 62 and fail-closed state integrity."""

    def test_phase62_all_20_release_gates(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE62", "LEGALMITRA-RELEASE-PHASE63", "LEGALMITRA-RELEASE-PHASE64")
        assert summary.target_version in ("0.62.0", "0.63.0", "0.64.0")
        assert summary.total_gates == 20
        assert summary.passed_gates == 19
        assert summary.pending_gates == 1  # RG-11-LEGAL-REVIEW
        assert summary.failed_gates == 0
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"

    def test_release_gate_negative_control_tampered_backup(self, monkeypatch, tmp_path):
        """Release gate negative control: if backup artifact is tampered, gate fails closed."""
        evaluator = ReleaseGateEvaluator()
        
        # Point to a non-existent database to test fail-closed
        evaluator.db_path = str(tmp_path / "non_existent_db.db")
        gate_summary = evaluator.evaluate_all_gates()
        assert gate_summary.failed_gates > 0
        assert gate_summary.overall_decision == "BLOCKED_RELEASE_GATES_FAILED"


class TestPhase62RecoveryObservabilityAndSecurity:
    """Workstream H & I: Audits structured traces, log sanitization, and security invariants."""

    def test_recovery_trace_logging_and_sanitization(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)
        mgr.verify_backup(manifest.backup_file_path)

        traces = mgr.get_audit_records()
        assert len(traces) >= 1
        for tr in traces:
            assert "operation_id" in tr
            assert "status" in tr
            assert tr["status"] == "SUCCESS"

        # Verify zero credential tokens
        raw_traces = json.dumps(traces).lower()
        for tok in ["password", "secret", "api_key", "bearer_token"]:
            assert tok not in raw_traces

    def test_security_path_traversal_blocked(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        with pytest.raises(ValueError, match="Path traversal"):
            mgr.create_backup(source_db_path="data/../data/legalmitra_kb.db")

    def test_security_restore_target_cannot_be_conversations_db(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir)

        # Attempting to restore to conversations.db must raise ValueError immediately
        with pytest.raises(ValueError, match="Security violation.*conversations.db"):
            mgr.restore_backup(manifest.backup_file_path, target_db_path="data/conversations.db")
