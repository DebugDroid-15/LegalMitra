"""
LegalMitra Knowledge Base Backup & Recovery System.

Provides verified, cryptographically audited backup, integrity verification,
and atomic point-in-time recovery for legalmitra_kb.db.
"""

import hashlib
import json
import os
import shutil
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class BackupManifest:
    backup_id: str
    timestamp_utc: str
    source_db_path: str
    backup_file_path: str
    sha256_checksum: str
    file_size_bytes: int
    total_sources: int
    total_chunks: int
    authentic_chunks: int
    quarantined_scaffold_chunks: int
    target_release: str
    is_quarantine_compliant: bool
    status: str
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BackupVerificationResult:
    is_valid: bool
    backup_file_path: str
    computed_sha256: str
    expected_sha256: Optional[str]
    integrity_check_passed: bool
    schema_valid: bool
    total_chunks: int
    scaffold_chunks: int
    quarantine_intact: bool
    errors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RestoreResult:
    success: bool
    target_path: str
    backup_file_path: str
    restored_chunks: int
    restored_sources: int
    is_dry_run: bool
    verification: BackupVerificationResult
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def compute_file_sha256(filepath: str) -> str:
    """Computes SHA256 checksum of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class KnowledgeBaseBackupManager:
    """
    Manages production backup and disaster recovery for the LegalMitra Knowledge Base.
    """

    EXPECTED_TABLES = {"sources", "legal_chunks", "cases", "judicial_documents", "hearing_events"}

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.default_db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self.default_backup_dir = os.path.join(self.workspace_root, "data", "backups")

    def inspect_database_metrics(self, db_path: str) -> Dict[str, Any]:
        """Inspects structural and record counts of a LegalMitra database."""
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")

        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cur = conn.cursor()

        # Schema & integrity
        cur.execute("PRAGMA integrity_check")
        integrity_row = cur.fetchone()
        integrity_ok = integrity_row and integrity_row[0] == "ok"

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {r[0] for r in cur.fetchall()}

        total_chunks = 0
        authentic_chunks = 0
        scaffold_chunks = 0
        total_sources = 0

        if "legal_chunks" in tables:
            cur.execute("SELECT COUNT(*) FROM legal_chunks")
            total_chunks = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
            authentic_chunks = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
            scaffold_chunks = cur.fetchone()[0]

        if "sources" in tables:
            cur.execute("SELECT COUNT(*) FROM sources")
            total_sources = cur.fetchone()[0]

        conn.close()

        return {
            "integrity_ok": integrity_ok,
            "tables": sorted(list(tables)),
            "total_chunks": total_chunks,
            "authentic_chunks": authentic_chunks,
            "scaffold_chunks": scaffold_chunks,
            "total_sources": total_sources,
            "quarantine_compliant": scaffold_chunks > 0 and scaffold_chunks <= 10,
        }

    def create_backup(
        self,
        source_db_path: Optional[str] = None,
        backup_dir: Optional[str] = None,
        notes: str = "Phase 61 Operational Snapshot",
    ) -> BackupManifest:
        """
        Creates a verified snapshot backup with cryptographic manifest.
        Uses SQLite vacuum/copy into backup directory.
        """
        src = source_db_path or self.default_db_path
        dest_dir = backup_dir or self.default_backup_dir
        os.makedirs(dest_dir, exist_ok=True)

        if not os.path.exists(src):
            raise FileNotFoundError(f"Source database not found: {src}")

        metrics = self.inspect_database_metrics(src)
        if not metrics["integrity_ok"]:
            raise ValueError(f"Source database fails integrity check: {src}")

        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_id = f"KB-BACKUP-{timestamp_str}"
        backup_filename = f"legalmitra_kb_{timestamp_str}.db"
        backup_filepath = os.path.join(dest_dir, backup_filename)

        # Atomic SQLite online backup to ensure snapshot consistency without write race
        src_conn = sqlite3.connect(src)
        dst_conn = sqlite3.connect(backup_filepath)
        with dst_conn:
            src_conn.backup(dst_conn)
        dst_conn.close()
        src_conn.close()

        sha256 = compute_file_sha256(backup_filepath)
        file_size = os.path.getsize(backup_filepath)

        manifest = BackupManifest(
            backup_id=backup_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            source_db_path=os.path.abspath(src),
            backup_file_path=os.path.abspath(backup_filepath),
            sha256_checksum=sha256,
            file_size_bytes=file_size,
            total_sources=metrics["total_sources"],
            total_chunks=metrics["total_chunks"],
            authentic_chunks=metrics["authentic_chunks"],
            quarantined_scaffold_chunks=metrics["scaffold_chunks"],
            target_release="0.61.0",
            is_quarantine_compliant=metrics["quarantine_compliant"],
            status="VERIFIED_SNAPSHOT",
            notes=notes,
        )

        manifest_path = backup_filepath + ".meta.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=2)

        return manifest

    def verify_backup(
        self,
        backup_file_path: str,
        meta_file_path: Optional[str] = None,
    ) -> BackupVerificationResult:
        """
        Cryptographically and structurally validates a backup snapshot.
        """
        errors: List[str] = []

        if not os.path.exists(backup_file_path):
            return BackupVerificationResult(
                is_valid=False,
                backup_file_path=backup_file_path,
                computed_sha256="",
                expected_sha256=None,
                integrity_check_passed=False,
                schema_valid=False,
                total_chunks=0,
                scaffold_chunks=0,
                quarantine_intact=False,
                errors=["Backup file does not exist"],
            )

        computed_sha = compute_file_sha256(backup_file_path)
        expected_sha: Optional[str] = None

        meta_path = meta_file_path or (backup_file_path + ".meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                expected_sha = meta.get("sha256_checksum")
                if expected_sha and expected_sha != computed_sha:
                    errors.append(
                        f"Checksum mismatch: computed {computed_sha} != expected {expected_sha}"
                    )
            except Exception as e:
                errors.append(f"Failed to read backup metadata: {e}")

        # Database inspection
        try:
            metrics = self.inspect_database_metrics(backup_file_path)
            integrity_ok = metrics["integrity_ok"]
            if not integrity_ok:
                errors.append("SQLite PRAGMA integrity_check failed")

            tables = set(metrics["tables"])
            missing_tables = self.EXPECTED_TABLES - tables
            schema_valid = len(missing_tables) == 0
            if not schema_valid:
                errors.append(f"Missing expected tables: {sorted(list(missing_tables))}")

            total_chunks = metrics["total_chunks"]
            scaffold_chunks = metrics["scaffold_chunks"]
            quarantine_intact = metrics["quarantine_compliant"]

            if total_chunks < 1000:
                errors.append(f"Suspiciously low chunk count: {total_chunks}")
            if not quarantine_intact:
                errors.append(f"Quarantine invariant violated: {scaffold_chunks} scaffold chunks")

        except Exception as e:
            errors.append(f"Database verification exception: {e}")
            integrity_ok = False
            schema_valid = False
            total_chunks = 0
            scaffold_chunks = 0
            quarantine_intact = False

        is_valid = len(errors) == 0

        return BackupVerificationResult(
            is_valid=is_valid,
            backup_file_path=os.path.abspath(backup_file_path),
            computed_sha256=computed_sha,
            expected_sha256=expected_sha,
            integrity_check_passed=integrity_ok,
            schema_valid=schema_valid,
            total_chunks=total_chunks,
            scaffold_chunks=scaffold_chunks,
            quarantine_intact=quarantine_intact,
            errors=errors,
        )

    def restore_backup(
        self,
        backup_file_path: str,
        target_db_path: Optional[str] = None,
        dry_run: bool = False,
    ) -> RestoreResult:
        """
        Safely restores a backup to target_db_path after cryptographic and structural verification.
        Fails closed if the backup is tampered, corrupt, or missing.
        """
        target = target_db_path or self.default_db_path

        # Step 1: Pre-restore verification
        verification = self.verify_backup(backup_file_path)
        if not verification.is_valid:
            return RestoreResult(
                success=False,
                target_path=os.path.abspath(target),
                backup_file_path=os.path.abspath(backup_file_path),
                restored_chunks=0,
                restored_sources=0,
                is_dry_run=dry_run,
                verification=verification,
                error_message=f"Backup verification failed: {'; '.join(verification.errors)}",
            )

        if dry_run:
            metrics = self.inspect_database_metrics(backup_file_path)
            return RestoreResult(
                success=True,
                target_path=os.path.abspath(target),
                backup_file_path=os.path.abspath(backup_file_path),
                restored_chunks=metrics["total_chunks"],
                restored_sources=metrics["total_sources"],
                is_dry_run=True,
                verification=verification,
                error_message=None,
            )

        # Step 2: Atomic restoration
        target_dir = os.path.dirname(os.path.abspath(target))
        os.makedirs(target_dir, exist_ok=True)
        temp_target = target + ".tmp_restore"

        try:
            # Copy backup to temp target
            shutil.copy2(backup_file_path, temp_target)

            # Verify temp target
            temp_metrics = self.inspect_database_metrics(temp_target)
            if not temp_metrics["integrity_ok"] or not temp_metrics["quarantine_compliant"]:
                os.remove(temp_target)
                return RestoreResult(
                    success=False,
                    target_path=os.path.abspath(target),
                    backup_file_path=os.path.abspath(backup_file_path),
                    restored_chunks=0,
                    restored_sources=0,
                    is_dry_run=False,
                    verification=verification,
                    error_message="Temp restore target failed integrity checks",
                )

            # Atomic replace
            if os.path.exists(target):
                backup_prev = target + ".prev_before_restore"
                shutil.move(target, backup_prev)
                shutil.move(temp_target, target)
                if os.path.exists(backup_prev):
                    os.remove(backup_prev)
            else:
                shutil.move(temp_target, target)

            final_metrics = self.inspect_database_metrics(target)
            return RestoreResult(
                success=True,
                target_path=os.path.abspath(target),
                backup_file_path=os.path.abspath(backup_file_path),
                restored_chunks=final_metrics["total_chunks"],
                restored_sources=final_metrics["total_sources"],
                is_dry_run=False,
                verification=verification,
                error_message=None,
            )
        except Exception as e:
            if os.path.exists(temp_target):
                os.remove(temp_target)
            return RestoreResult(
                success=False,
                target_path=os.path.abspath(target),
                backup_file_path=os.path.abspath(backup_file_path),
                restored_chunks=0,
                restored_sources=0,
                is_dry_run=False,
                verification=verification,
                error_message=f"Restoration exception: {e}",
            )
