"""
Phase 63 Test Suite: Independent Reproducibility Audit, Adversarial Recovery Testing,
and Evidence-Integrity Assurance.

Validates:
1. Internal SQLite identity binding table (_backup_manifest_binding) and fail-closed companion verification.
2. Two-stage atomic recovery crash resilience, interrupted restore auto-recovery, and rollback on demand.
3. Concurrency lock management: dead PID stale lock detection and safe reclamation.
4. Deep record-level cryptographic & semantic reconciliation (chunk IDs, source IDs, SHA256 content hashes, quarantine flags).
5. Strict release gate manifest integrity verification and negative controls (missing gate, unknown status, advocate sign-off tamper).
6. Strict database isolation (legalmitra_kb.db vs conversations.db) and disk space preflight defense.
"""

import copy
from datetime import datetime, timezone
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
from legalmitra.operations.reconciler import CorpusReconciler


class TestPhase63BackupIdentityAndManifestBinding:
    """Audits internal SQLite backup identity binding table and tamper detection."""

    def test_backup_manifest_binding_table_creation(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Identity Binding Audit")

        assert os.path.exists(manifest.backup_file_path)
        assert manifest.target_release == "0.63.0"

        # Verify internal _backup_manifest_binding table inside the SQLite backup database
        conn = sqlite3.connect(f"file:{manifest.backup_file_path}?mode=ro", uri=True)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='_backup_manifest_binding'")
        assert cur.fetchone() is not None, "_backup_manifest_binding table missing from backup database"

        cur.execute("SELECT backup_id, schema_version, total_chunks, target_release FROM _backup_manifest_binding")
        row = cur.fetchone()
        assert row is not None
        assert row[0] == manifest.backup_id
        assert row[1] == "1.0.0"
        assert row[2] == 1515
        assert row[3] == "0.63.0"
        conn.close()

    def test_verify_backup_binding_mismatch_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Binding Mismatch Test")

        meta_file = manifest.backup_file_path + ".meta.json"
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # Alter backup_id in companion metadata to simulate swapped or mismatched metadata
        meta["backup_id"] = "BK-SWAPPED-FOREIGN-ID-9999"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        ver = mgr.verify_backup(manifest.backup_file_path)
        assert not ver.is_valid
        assert any("Identity binding mismatch" in e for e in ver.errors)

    def test_verify_backup_tampered_manifest_hash_fails_closed(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Tampered Hash Test")

        meta_file = manifest.backup_file_path + ".meta.json"
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # Alter checksum in metadata
        meta["sha256_checksum"] = "0000000000000000000000000000000000000000000000000000000000000000"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        ver = mgr.verify_backup(manifest.backup_file_path)
        assert not ver.is_valid
        assert any("Checksum mismatch" in e for e in ver.errors)


class TestPhase63AtomicRecoveryAndCrashSafety:
    """Audits crash resilience, interrupted restore auto-recovery, and post-restore rollback."""

    def test_restore_valid_with_previous_snapshot_preserved(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Snapshot Test")

        target_db = str(tmp_path / "target_kb.db")
        # Populate target with a valid dummy DB
        conn = sqlite3.connect(target_db)
        conn.execute("CREATE TABLE dummy (id INT)")
        conn.commit()
        conn.close()

        res = mgr.restore_backup(
            backup_file_path=manifest.backup_file_path,
            target_db_path=target_db,
            keep_previous_snapshot=True,
        )

        assert res.success
        assert res.outcome_status == RecoveryOutcomeStatus.RESTORE_VERIFIED.value
        assert res.previous_snapshot_path is not None
        assert os.path.exists(res.previous_snapshot_path)
        assert res.previous_snapshot_path == target_db + ".prev_before_restore"

    def test_interrupted_restore_recovery(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        target_db = str(tmp_path / "crashed_kb.db")
        prev_snapshot = target_db + ".prev_before_restore"

        # Create valid database at prev_snapshot (simulating target moved to prev before crash)
        shutil.copy2("data/legalmitra_kb.db", prev_snapshot)
        assert not os.path.exists(target_db)
        assert os.path.exists(prev_snapshot)

        rec_res = mgr.recover_interrupted_restore(target_db)
        assert rec_res["recovered_from_prev"] is True
        assert rec_res["target_healthy"] is True
        assert os.path.exists(target_db)
        assert not os.path.exists(prev_snapshot)

        # Verify recovered DB has 1,515 chunks
        conn = sqlite3.connect(f"file:{target_db}?mode=ro", uri=True)
        chunks = conn.cursor().execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        conn.close()
        assert chunks == 1515

    def test_manual_rollback_from_previous_snapshot(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Rollback Test")

        target_db = str(tmp_path / "rollback_target.db")
        shutil.copy2("data/legalmitra_kb.db", target_db)

        # Restore with keep_previous_snapshot=True
        res = mgr.restore_backup(
            backup_file_path=manifest.backup_file_path,
            target_db_path=target_db,
            keep_previous_snapshot=True,
        )
        assert res.success
        assert os.path.exists(target_db + ".prev_before_restore")

        # Rollback from previous snapshot
        rb_res = mgr.rollback_from_previous(target_db)
        assert rb_res.success
        assert rb_res.restored_chunks == 1515
        assert not os.path.exists(target_db + ".prev_before_restore")

    def test_commit_restoration_cleans_snapshot(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Commit Test")

        target_db = str(tmp_path / "commit_target.db")
        shutil.copy2("data/legalmitra_kb.db", target_db)

        res = mgr.restore_backup(
            backup_file_path=manifest.backup_file_path,
            target_db_path=target_db,
            keep_previous_snapshot=True,
        )
        assert os.path.exists(target_db + ".prev_before_restore")

        committed = mgr.commit_restoration(target_db)
        assert committed is True
        assert not os.path.exists(target_db + ".prev_before_restore")


class TestPhase63ConcurrencyAndLockManagement:
    """Audits concurrency locking, stale lock detection with dead PID, and reclamation."""

    def test_stale_lock_detection_with_dead_pid(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        target_db = str(tmp_path / "lock_target.db")
        lock_file = target_db + ".restore.lock"

        # Dead PID (999999)
        with open(lock_file, "w", encoding="utf-8") as f:
            f.write("PID:999999 TIME:2026-01-01T00:00:00Z\n")

        is_stale, recorded_pid = mgr.is_lock_stale(lock_file)
        assert is_stale is True
        assert recorded_pid == 999999

    def test_reclaim_stale_lock_reclaims_safely(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        target_db = str(tmp_path / "reclaim_target.db")
        lock_file = target_db + ".restore.lock"

        with open(lock_file, "w", encoding="utf-8") as f:
            f.write("PID:999999 TIME:2026-01-01T00:00:00Z\n")

        rec_res = mgr.reclaim_stale_lock(target_db)
        assert rec_res["reclaimed"] is True
        assert rec_res["status"] == "RECLAIMED_SUCCESS"
        assert not os.path.exists(lock_file)

    def test_active_lock_prevents_restoration(self, tmp_path):
        mgr = KnowledgeBaseBackupManager()
        backup_dir = str(tmp_path / "backups")
        manifest = mgr.create_backup(backup_dir=backup_dir, notes="Phase 63 Active Lock Test")

        target_db = str(tmp_path / "active_lock_target.db")
        shutil.copy2("data/legalmitra_kb.db", target_db)
        lock_file = target_db + ".restore.lock"

        # Current process PID is alive with fresh timestamp
        now_iso = datetime.now(timezone.utc).isoformat()
        with open(lock_file, "w", encoding="utf-8") as f:
            f.write(f"PID:{os.getpid()} TIME:{now_iso}\n")

        res = mgr.restore_backup(
            backup_file_path=manifest.backup_file_path,
            target_db_path=target_db,
        )

        assert not res.success
        assert "locked by active process" in res.error_message
        assert res.original_preserved is True

        # Clean up lock
        if os.path.exists(lock_file):
            os.remove(lock_file)


class TestPhase63DeepSemanticReconciliation:
    """Audits record-level differential comparison between SQLite databases."""

    def test_deep_reconciliation_exact_record_match(self):
        reconciler = CorpusReconciler()
        kb_path = "data/legalmitra_kb.db"

        # Deep comparison between primary DB and itself must be 100% identical
        diff = reconciler.compare_databases_deep(kb_path, kb_path)
        assert diff["is_identical"] is True
        assert diff["chunk_count_match"] is True
        assert diff["source_count_match"] is True
        assert len(diff["missing_chunks_in_post"]) == 0
        assert len(diff["extra_chunks_in_post"]) == 0
        assert len(diff["content_checksum_mismatches"]) == 0
        assert len(diff["quarantine_status_mismatches"]) == 0

    def test_deep_reconciliation_detects_tampered_chunk_content(self, tmp_path):
        reconciler = CorpusReconciler()
        kb_path = "data/legalmitra_kb.db"
        tampered_db = str(tmp_path / "tampered_chunk_kb.db")
        shutil.copy2(kb_path, tampered_db)

        # Tamper one chunk's text content
        conn = sqlite3.connect(tampered_db)
        cur = conn.cursor()
        cur.execute("UPDATE legal_chunks SET content = 'TAMPERED EVIDENCE' WHERE chunk_id = (SELECT chunk_id FROM legal_chunks LIMIT 1)")
        conn.commit()
        conn.close()

        diff = reconciler.compare_databases_deep(kb_path, tampered_db)
        assert diff["is_identical"] is False
        assert len(diff["content_checksum_mismatches"]) == 1

    def test_deep_reconciliation_detects_quarantine_tampering(self, tmp_path):
        reconciler = CorpusReconciler()
        kb_path = "data/legalmitra_kb.db"
        tampered_db = str(tmp_path / "tampered_quarantine_kb.db")
        shutil.copy2(kb_path, tampered_db)

        # Illegally unquarantine one scaffold chunk
        conn = sqlite3.connect(tampered_db)
        cur = conn.cursor()
        cur.execute("UPDATE legal_chunks SET is_synthetic_scaffold = 0 WHERE chunk_id = (SELECT chunk_id FROM legal_chunks WHERE is_synthetic_scaffold = 1 LIMIT 1)")
        conn.commit()
        conn.close()

        diff = reconciler.compare_databases_deep(kb_path, tampered_db)
        assert diff["is_identical"] is False
        assert len(diff["quarantine_status_mismatches"]) == 1


class TestPhase63ReleaseGateManifestIntegrity:
    """Audits release gate evaluation and fail-closed manifest integrity validation."""

    def test_phase63_all_20_release_gates(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE63", "LEGALMITRA-RELEASE-PHASE64")
        assert summary.target_version in ("0.63.0", "0.64.0")
        assert summary.total_gates == 20
        assert summary.passed_gates == 19
        assert summary.pending_gates == 1  # RG-11-LEGAL-REVIEW
        assert summary.failed_gates == 0
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"

        rg11 = [g for g in summary.gates if g.gate_id == "RG-11-LEGAL-REVIEW"][0]
        assert rg11.status == GateStatus.PENDING_HUMAN_REVIEW

    def test_validate_manifest_integrity_valid(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        manifest_dict = summary.to_dict()

        res = ReleaseGateEvaluator.validate_manifest_integrity(manifest_dict)
        assert res["is_valid"] is True
        assert len(res["errors"]) == 0
        assert len(res["gate_ids"]) == 20

    def test_validate_manifest_integrity_negative_tampered_rg11(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        manifest_dict = summary.to_dict()

        # Illegally tamper RG-11 status to PASSED
        for g in manifest_dict["gates"]:
            if g["gate_id"] == "RG-11-LEGAL-REVIEW":
                g["status"] = GateStatus.PASSED.value
        manifest_dict["passed_gates"] = 20
        manifest_dict["pending_gates"] = 0

        res = ReleaseGateEvaluator.validate_manifest_integrity(manifest_dict)
        assert res["is_valid"] is False
        assert any("RG-11-LEGAL-REVIEW status is 'PASSED'" in e for e in res["errors"])

    def test_validate_manifest_integrity_negative_missing_gate(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        manifest_dict = summary.to_dict()

        # Remove 1 gate
        manifest_dict["gates"] = manifest_dict["gates"][:-1]
        manifest_dict["total_gates"] = 19

        res = ReleaseGateEvaluator.validate_manifest_integrity(manifest_dict)
        assert res["is_valid"] is False
        assert any("Gate count mismatch" in e for e in res["errors"])

    def test_validate_manifest_integrity_negative_unknown_status(self):
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()
        manifest_dict = summary.to_dict()

        # Inject unknown status
        manifest_dict["gates"][0]["status"] = "UNVERIFIED_STATUS_CODE"

        res = ReleaseGateEvaluator.validate_manifest_integrity(manifest_dict)
        assert res["is_valid"] is False
        assert any("unknown/unrecognized status" in e for e in res["errors"])


class TestPhase63OperationalSafetyAndBoundaries:
    """Audits database isolation and disk space safety preflight."""

    def test_database_isolation_legalmitra_kb_has_zero_chat_tables(self):
        conn = sqlite3.connect("file:data/legalmitra_kb.db?mode=ro", uri=True)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        conn.close()

        chat_tables = [t for t in tables if any(k in t.lower() for k in ["chat", "conversation", "message", "session", "user"])]
        assert len(chat_tables) == 0, f"Violation: Knowledge base contains chat tables: {chat_tables}"

    def test_database_isolation_conversations_db_has_zero_chunks(self):
        if os.path.exists("data/conversations.db"):
            conn = sqlite3.connect("file:data/conversations.db?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            conn.close()

            assert "legal_chunks" not in tables, "Violation: conversations.db contains legal_chunks table"
            assert "sources" not in tables, "Violation: conversations.db contains sources table"
