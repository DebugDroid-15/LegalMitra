"""
LegalMitra National Judicial Coverage Dashboard & Report Generator (Phase 21)
Measures authentic judicial assets in the knowledge base and output:
- data/11_judicial_corpus/judicial_coverage.json
- data/11_judicial_corpus/judicial_coverage.csv
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from legalmitra.corpus.judicial_registry import JUDICIAL_SOURCE_REGISTRY


def generate_judicial_coverage(db_path: str = "data/legalmitra_kb.db") -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Total chunk counts
    c.execute("""
        SELECT COUNT(*), COUNT(DISTINCT source_id)
        FROM legal_chunks
        WHERE is_synthetic_scaffold = 0 AND doc_type = 'judgment'
    """)
    row = c.fetchone()
    active_judgment_chunks = row[0]
    active_judgment_sources = row[1]

    # 2. Cases count
    c.execute("SELECT COUNT(*) FROM cases")
    total_cases = c.fetchone()[0]

    # 3. Judicial documents count
    c.execute("SELECT COUNT(*) FROM judicial_documents WHERE is_synthetic_scaffold = 0")
    total_judicial_docs = c.fetchone()[0]

    # 4. Hearing events count
    c.execute("SELECT COUNT(*) FROM hearing_events")
    total_hearing_events = c.fetchone()[0]

    # 5. Distinct judgment sources breakdown
    c.execute("""
        SELECT source_id, act_or_case_title, court, COUNT(*) as chunk_cnt
        FROM legal_chunks
        WHERE is_synthetic_scaffold = 0 AND doc_type = 'judgment'
        GROUP BY source_id, act_or_case_title, court
        ORDER BY chunk_cnt DESC
    """)
    ingested_judgments = [dict(r) for r in c.fetchall()]

    # 6. Scaffolds
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    quarantined_scaffolds = c.fetchone()[0]

    conn.close()

    # Match against registry
    registry_summary = []
    for reg in JUDICIAL_SOURCE_REGISTRY:
        registry_summary.append({
            "source_id": reg.source_id,
            "body_name": reg.body_name,
            "tier": reg.tier.value,
            "jurisdiction_code": reg.jurisdiction_code,
            "official_domain": reg.official_domain,
            "has_neutral_citation": reg.neutral_citation_system,
            "ecourts_integrated": reg.ecourts_integrated,
            "public_access_policy": reg.public_access_policy,
        })

    summary = {
        "phase": 21,
        "database_path": db_path,
        "registered_judicial_repositories": len(JUDICIAL_SOURCE_REGISTRY),
        "active_judgment_sources": active_judgment_sources,
        "active_judgment_chunks": active_judgment_chunks,
        "total_unified_cases": total_cases,
        "total_judicial_orders_and_docs": total_judicial_docs,
        "total_hearing_events": total_hearing_events,
        "quarantined_synthetic_scaffolds": quarantined_scaffolds,
        "ingested_judgments": ingested_judgments,
        "repositories": registry_summary,
    }

    return summary


def main():
    coverage = generate_judicial_coverage()
    out_dir = Path("data/11_judicial_corpus")
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "judicial_coverage.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)
    print(f"[OK] Exported JSON: {json_path}")

    csv_path = out_dir / "judicial_coverage.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Source ID", "Case / Body Name", "Court / Tier", "Jurisdiction", "Total Chunks / Status"
        ])
        for j in coverage["ingested_judgments"]:
            writer.writerow([
                j["source_id"], j["act_or_case_title"], j["court"], "IN", j["chunk_cnt"]
            ])
        for r in coverage["repositories"]:
            writer.writerow([
                r["source_id"], r["body_name"], r["tier"], r["jurisdiction_code"], "Catalogued Repository"
            ])
    print(f"[OK] Exported CSV: {csv_path}")


if __name__ == "__main__":
    main()

