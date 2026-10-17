"""
LegalMitra State & Union Territory Legislative Coverage Generator (Phase 20)
Analyzes the 36 States and Union Territories in STATE_UT_REGISTRY against
the LegalKnowledgeBase database and outputs:
- data/10_legislation/state_ut_coverage.json
- data/10_legislation/state_ut_coverage.csv
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from legalmitra.corpus.state_registry import STATE_UT_REGISTRY


def generate_coverage_matrix(db_path: str = "data/legalmitra_kb.db") -> List[Dict[str, Any]]:
    # Query database for actual chunk and source counts per jurisdiction
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT jurisdiction, COUNT(DISTINCT source_id), COUNT(*)
        FROM legal_chunks
        WHERE is_synthetic_scaffold = 0
        GROUP BY jurisdiction
    """)
    db_stats = {row[0]: {"sources": row[1], "chunks": row[2]} for row in c.fetchall()}
    conn.close()

    coverage_data: List[Dict[str, Any]] = []

    for entry in STATE_UT_REGISTRY:
        j_code = entry.jurisdiction_code
        stats = db_stats.get(j_code, {"sources": 0, "chunks": 0})
        
        status = "Active Ingested" if stats["chunks"] > 0 else "Catalogued / Ready for Ingestion"
        
        item = {
            "jurisdiction_code": j_code,
            "name": entry.name,
            "category": entry.category,
            "official_portal_name": entry.official_portal_name,
            "official_portal_url": entry.official_portal_url,
            "gazette_portal_url": entry.gazette_portal_url or "N/A",
            "responsible_authority": entry.responsible_authority,
            "priority_level": entry.priority_level,
            "active_in_pilot": entry.active_in_pilot or (stats["chunks"] > 0),
            "ingested_sources_count": stats["sources"],
            "ingested_chunks_count": stats["chunks"],
            "ingestion_status": status,
        }
        coverage_data.append(item)

    return coverage_data


def main():
    coverage = generate_coverage_matrix()
    
    out_dir = Path("data/10_legislation")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = out_dir / "state_ut_coverage.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)
    print(f"[OK] Exported JSON: {json_path}")
    
    csv_path = out_dir / "state_ut_coverage.csv"
    fieldnames = [
        "jurisdiction_code",
        "name",
        "category",
        "official_portal_name",
        "official_portal_url",
        "gazette_portal_url",
        "responsible_authority",
        "priority_level",
        "active_in_pilot",
        "ingested_sources_count",
        "ingested_chunks_count",
        "ingestion_status",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in coverage:
            writer.writerow(row)
    print(f"[OK] Exported CSV: {csv_path}")


if __name__ == "__main__":
    main()

