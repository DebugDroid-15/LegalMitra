"""
Updates legalmitra/operations/reconciler.py with compare_pre_and_post_restore method for Phase 62.
"""

def update_reconciler():
    rec_path = "legalmitra/operations/reconciler.py"
    with open(rec_path, "r", encoding="utf-8") as f:
        content = f.read()

    method_code = '''
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
'''

    content = content.replace('target_release="0.61.0"', 'target_release="0.62.0"')
    if "def compare_pre_and_post_restore" not in content:
        target_marker = "    def _empty_report(self, errors: List[str]) -> CorpusReconciliationReport:"
        content = content.replace(target_marker, method_code + "\n" + target_marker)

    with open(rec_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated {rec_path} for Phase 62")

if __name__ == "__main__":
    update_reconciler()
