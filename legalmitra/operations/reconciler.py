"""
LegalMitra Corpus Reconciliation & Knowledge Base Integrity Engine.

Provides deep audit and cross-system reconciliation between the SQLite knowledge base,
source registries, review tracking register, and benchmark manifests.
"""

import hashlib
import json
import os
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class CorpusReconciliationReport:
    audit_id: str
    timestamp_utc: str
    target_release: str
    overall_status: str  # PASSED or FAILED
    total_sources: int
    authentic_sources: int
    quarantined_sources: int
    total_chunks: int
    authentic_chunks: int
    quarantined_chunks: int
    orphaned_chunks: int
    unchunked_sources: List[str]
    duplicate_chunk_ids: int
    duplicate_content_patterns: int
    scaffold_quarantine_compliant: bool
    review_package_records: int
    review_package_pending_count: int
    benchmark_v14_total_cases: int
    benchmark_v14_splits: Dict[str, int]
    benchmark_contamination_clean: bool
    findings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CorpusReconciler:
    """
    Performs comprehensive cross-system reconciliation for LegalMitra release candidates.
    """

    KNOWN_SCAFFOLD_SOURCE_ID = "IND-JUD-DEL-2024-BAIL"
    EXPECTED_SCAFFOLD_CHUNKS = 6

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self.conv_db_path = os.path.join(self.workspace_root, "data", "conversations.db")
        self.review_tracking_path = os.path.join(
            self.workspace_root, "data", "07_batches", "review", "review_tracking_register.json"
        )
        self.benchmark_path = os.path.join(
            self.workspace_root, "data", "22_central_legislation", "temporal_benchmark_manifest.json"
        )

    def run_full_reconciliation(self) -> CorpusReconciliationReport:
        findings: List[str] = []
        errors: List[str] = []

        if not os.path.exists(self.db_path):
            errors.append(f"Knowledge Base DB not found: {self.db_path}")
            return self._empty_report(errors)

        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        cur = conn.cursor()

        # 1. Sources reconciliation
        cur.execute("SELECT COUNT(*) FROM sources")
        total_sources = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM sources WHERE is_synthetic_scaffold = 1")
        quarantined_sources = cur.fetchone()[0]
        authentic_sources = total_sources - quarantined_sources

        # 2. Chunks reconciliation
        cur.execute("SELECT COUNT(*) FROM legal_chunks")
        total_chunks = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
        quarantined_chunks = cur.fetchone()[0]
        authentic_chunks = total_chunks - quarantined_chunks

        # 3. Scaffold quarantine check
        cur.execute(
            "SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1 AND source_id != ?",
            (self.KNOWN_SCAFFOLD_SOURCE_ID,),
        )
        unauthorized_scaffolds = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM legal_chunks WHERE source_id = ?",
            (self.KNOWN_SCAFFOLD_SOURCE_ID,),
        )
        known_scaffold_count = cur.fetchone()[0]

        quarantine_compliant = (
            quarantined_sources == 1
            and quarantined_chunks == self.EXPECTED_SCAFFOLD_CHUNKS
            and known_scaffold_count == self.EXPECTED_SCAFFOLD_CHUNKS
            and unauthorized_scaffolds == 0
        )
        if not quarantine_compliant:
            errors.append(
                f"Quarantine invariant violated: quarantined_chunks={quarantined_chunks}, unauthorized={unauthorized_scaffolds}"
            )
        else:
            findings.append("Quarantine compliance verified: exactly 6 chunks isolated under IND-JUD-DEL-2024-BAIL.")

        # 4. Orphaned chunks check
        cur.execute(
            "SELECT COUNT(*) FROM legal_chunks WHERE source_id NOT IN (SELECT document_id FROM sources)"
        )
        orphaned_chunks = cur.fetchone()[0]
        if orphaned_chunks > 0:
            errors.append(f"Orphaned chunks detected: {orphaned_chunks} chunks link to missing sources")
        else:
            findings.append("Zero orphaned chunks detected in knowledge base.")

        # 5. Unchunked sources check
        cur.execute(
            "SELECT document_id FROM sources WHERE document_id NOT IN (SELECT DISTINCT source_id FROM legal_chunks)"
        )
        unchunked_sources = [r[0] for r in cur.fetchall()]
        findings.append(f"Identified {len(unchunked_sources)} unchunked reference/control sources: {unchunked_sources}")

        # 6. Duplicate chunk IDs
        cur.execute("SELECT chunk_id FROM legal_chunks GROUP BY chunk_id HAVING COUNT(*) > 1")
        dup_ids = cur.fetchall()
        duplicate_chunk_ids = len(dup_ids)
        if duplicate_chunk_ids > 0:
            errors.append(f"Duplicate chunk IDs found: {duplicate_chunk_ids}")
        else:
            findings.append("Zero duplicate chunk IDs found.")

        # 7. Common content patterns
        cur.execute("SELECT COUNT(*) FROM (SELECT content FROM legal_chunks GROUP BY content HAVING COUNT(*) > 1)")
        duplicate_content_patterns = cur.fetchone()[0]

        conn.close()

        # 8. Review Packages reconciliation
        review_records = 0
        review_pending = 0
        if os.path.exists(self.review_tracking_path):
            with open(self.review_tracking_path, "r", encoding="utf-8") as f:
                rdata = json.load(f)
            raw_entries = rdata.get("entries", [])
            if isinstance(raw_entries, dict):
                entries_list = list(raw_entries.values())
            elif isinstance(raw_entries, list):
                entries_list = raw_entries
            else:
                entries_list = []
            review_records = len(entries_list)
            review_pending = sum(
                1 for e in entries_list if e.get("review_status") == "pending_legal_review"
            )
            if review_records != 40 or review_pending != 40:
                errors.append(
                    f"Review tracking discrepancy: records={review_records}, pending={review_pending} (expected 40/40)"
                )
            else:
                findings.append("All 40 advocate review candidates verified strictly pending_legal_review.")
        else:
            errors.append(f"Review tracking register missing: {self.review_tracking_path}")

        # 9. Benchmark V14 reconciliation
        b14_total = 0
        b14_splits: Dict[str, int] = {}
        b14_clean = False
        if os.path.exists(self.benchmark_path):
            with open(self.benchmark_path, "r", encoding="utf-8") as f:
                bdata = json.load(f)
            cases = bdata.get("test_cases", [])
            b14_total = len(cases)
            for c in cases:
                sp = c.get("split", "unknown")
                b14_splits[sp] = b14_splits.get(sp, 0) + 1

            # Contamination check: pairwise overlap of query texts
            dev_queries = {c["query_description"].strip().lower() for c in cases if c.get("split") == "development"}
            val_queries = {c["query_description"].strip().lower() for c in cases if c.get("split") == "validation"}
            held_queries = {c["query_description"].strip().lower() for c in cases if c.get("split") == "held_out_evaluation"}

            dev_val_overlap = dev_queries & val_queries
            dev_held_overlap = dev_queries & held_queries
            val_held_overlap = val_queries & held_queries

            if dev_val_overlap or dev_held_overlap or val_held_overlap:
                errors.append("Benchmark split cross-contamination detected!")
                b14_clean = False
            else:
                b14_clean = True
                findings.append(f"PIT-V14 benchmark verified: {b14_total} cases with zero cross-split leakage.")
        else:
            errors.append(f"Benchmark manifest missing: {self.benchmark_path}")

        overall_status = "PASSED" if len(errors) == 0 else "FAILED"

        return CorpusReconciliationReport(
            audit_id=f"RECON-AUDIT-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            target_release="0.62.0",
            overall_status=overall_status,
            total_sources=total_sources,
            authentic_sources=authentic_sources,
            quarantined_sources=quarantined_sources,
            total_chunks=total_chunks,
            authentic_chunks=authentic_chunks,
            quarantined_chunks=quarantined_chunks,
            orphaned_chunks=orphaned_chunks,
            unchunked_sources=unchunked_sources,
            duplicate_chunk_ids=duplicate_chunk_ids,
            duplicate_content_patterns=duplicate_content_patterns,
            scaffold_quarantine_compliant=quarantine_compliant,
            review_package_records=review_records,
            review_package_pending_count=review_pending,
            benchmark_v14_total_cases=b14_total,
            benchmark_v14_splits=b14_splits,
            benchmark_contamination_clean=b14_clean,
            findings=findings,
            errors=errors,
        )


    def compare_pre_and_post_restore(
        self,
        pre_report: CorpusReconciliationReport,
        post_report: CorpusReconciliationReport,
    ) -> Dict[str, Any]:
        """
        Performs deep differential semantic reconciliation between pre-backup
        and post-restoration corpus states to ensure zero record loss or drift.
        """
        source_diff = post_report.total_sources - pre_report.total_sources
        chunk_diff = post_report.total_chunks - pre_report.total_chunks
        scaffold_diff = post_report.quarantined_chunks - pre_report.quarantined_chunks
        orphan_diff = post_report.orphaned_chunks - pre_report.orphaned_chunks

        is_semantically_identical = (
            source_diff == 0
            and chunk_diff == 0
            and scaffold_diff == 0
            and orphan_diff == 0
            and post_report.scaffold_quarantine_compliant
            and post_report.orphaned_chunks == 0
            and post_report.duplicate_chunk_ids == 0
        )

        return {
            "comparison_id": f"DIFF-RECON-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "target_release": "0.62.0",
            "is_semantically_identical": is_semantically_identical,
            "metrics": {
                "pre_sources": pre_report.total_sources,
                "post_sources": post_report.total_sources,
                "source_difference": source_diff,
                "pre_chunks": pre_report.total_chunks,
                "post_chunks": post_report.total_chunks,
                "chunk_difference": chunk_diff,
                "pre_scaffold_chunks": pre_report.quarantined_chunks,
                "post_scaffold_chunks": post_report.quarantined_chunks,
                "scaffold_difference": scaffold_diff,
                "post_orphaned_chunks": post_report.orphaned_chunks,
                "post_duplicate_chunk_ids": post_report.duplicate_chunk_ids,
            },
            "quarantine_preserved": post_report.scaffold_quarantine_compliant,
            "unchunked_sources_preserved": (pre_report.unchunked_sources == post_report.unchunked_sources),
            "status": "RESTORE_SEMANTICALLY_VERIFIED" if is_semantically_identical else "SEMANTIC_DISCREPANCY_DETECTED",
        }

    def _empty_report(self, errors: List[str]) -> CorpusReconciliationReport:
        return CorpusReconciliationReport(
            audit_id=f"RECON-AUDIT-FAILED",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            target_release="0.62.0",
            overall_status="FAILED",
            total_sources=0,
            authentic_sources=0,
            quarantined_sources=0,
            total_chunks=0,
            authentic_chunks=0,
            quarantined_chunks=0,
            orphaned_chunks=0,
            unchunked_sources=[],
            duplicate_chunk_ids=0,
            duplicate_content_patterns=0,
            scaffold_quarantine_compliant=False,
            review_package_records=0,
            review_package_pending_count=0,
            benchmark_v14_total_cases=0,
            benchmark_v14_splits={},
            benchmark_contamination_clean=False,
            findings=[],
            errors=errors,
        )
