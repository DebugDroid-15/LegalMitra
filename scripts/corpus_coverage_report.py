"""
Script to compute, display, and export the National Indian Legal Corpus Coverage Report (Phase 14I).
Analyzes data/08_corpus/coverage_inventory.json and data/legalmitra_kb.db.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

from legalmitra.corpus.inventory import CorpusInventoryManager, CorpusStatus, DocumentClass


def main() -> None:
    print("=== LegalMitra National Indian Legal Corpus Coverage Audit (Phase 14I) ===\n")

    inv_path = Path("data/08_corpus/coverage_inventory.json")
    if not inv_path.exists():
        print(f"Error: Inventory file {inv_path} does not exist. Run scripts/generate_corpus_inventory.py first.")
        return

    mgr = CorpusInventoryManager.load_json(inv_path)
    items = mgr.list_items()
    total_sources = len(items)

    # Database metrics
    kb_path = Path("data/legalmitra_kb.db")
    if kb_path.exists():
        conn = sqlite3.connect(kb_path)
        cur = conn.cursor()
        total_chunks = cur.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        indexed_sources = cur.execute("SELECT COUNT(DISTINCT source_id) FROM legal_chunks").fetchone()[0]
        quarantined_chunks = cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1").fetchone()[0]
        conn.close()
    else:
        total_chunks = 0
        indexed_sources = 0
        quarantined_chunks = 0

    # Categorical distributions
    status_counts = Counter(i.corpus_status.value for i in items)
    class_counts = Counter(i.document_class.value for i in items)
    domain_counts = Counter(i.legal_domain for i in items)
    jurisdiction_counts = Counter(i.jurisdiction for i in items)

    # Ingestion & Validation metrics
    fully_extracted = sum(1 for i in items if i.extraction_status == "completed")
    inaccessible_failed = sum(1 for i in items if i.extraction_status == "failed" or i.corpus_status == CorpusStatus.INACCESSIBLE)
    quarantined_count = sum(1 for i in items if i.corpus_status == CorpusStatus.QUARANTINED)
    historical_count = sum(1 for i in items if i.corpus_status == CorpusStatus.HISTORICAL)
    current_count = sum(1 for i in items if i.corpus_status == CorpusStatus.CURRENT)
    pending_ingestion = sum(1 for i in items if i.extraction_status == "pending")

    # Display Metrics
    print("1. OVERALL METRICS & DENOMINATORS:")
    print(f"  - Total Identified Legal Sources (Denominator): {total_sources}")
    print(f"  - Currently Indexed in Knowledge Base:           {indexed_sources} sources ({total_chunks} chunks)")
    print(f"  - Fully Extracted & Validated:                  {fully_extracted} ({(fully_extracted/total_sources)*100:.1f}%)")
    print(f"  - Pending Ingestion Pipeline:                   {pending_ingestion} ({(pending_ingestion/total_sources)*100:.1f}%)")
    print(f"  - Inaccessible / Extraction Backlog:            {inaccessible_failed}")
    print(f"  - Strictly Quarantined Test Scaffolds:          {quarantined_count} ({quarantined_chunks} quarantined chunks)")

    print("\n2. COVERAGE BY LEGAL STATUS:")
    for status, count in status_counts.items():
        print(f"  - {status:15}: {count:2} ({(count/total_sources)*100:.1f}%)")

    print("\n3. COVERAGE BY DOCUMENT CLASS:")
    for doc_class, count in class_counts.items():
        print(f"  - {doc_class:20}: {count:2} ({(count/total_sources)*100:.1f}%)")

    print("\n4. COVERAGE BY JURISDICTION:")
    for jur, count in jurisdiction_counts.items():
        print(f"  - {jur:15}: {count:2} ({(count/total_sources)*100:.1f}%)")

    print("\n5. TOP LEGAL DOMAINS IN CORPUS:")
    for domain, count in domain_counts.most_common(6):
        print(f"  - {domain:35}: {count:2} sources")

    # Generate Machine-Readable Report
    report = {
        "audit_version": "1.0.0",
        "timestamp": "2026-10-16T23:54:00+05:30",
        "total_sources_identified": total_sources,
        "indexed_sources_count": indexed_sources,
        "total_indexed_chunks": total_chunks,
        "quarantined_chunks_count": quarantined_chunks,
        "status_distribution": dict(status_counts),
        "document_class_distribution": dict(class_counts),
        "jurisdiction_distribution": dict(jurisdiction_counts),
        "domain_distribution": dict(domain_counts),
        "gap_summary": {
            "pending_ingestion_count": pending_ingestion,
            "inaccessible_count": inaccessible_failed,
            "quarantined_count": quarantined_count,
        }
    }

    out_json = Path("data/08_corpus/coverage_summary.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n[OK] Machine-readable coverage summary saved to: {out_json}")


if __name__ == "__main__":
    main()

