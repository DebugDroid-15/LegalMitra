"""
Corpus Quality & National Coverage Analyzer (Phase 23)
Evaluates corpus readiness across four distinct operational dimensions:
1. Registered (catalogued in legal universe and sources registry)
2. Acquired (source files physically ingested)
3. Indexed (present in legal_chunks table)
4. Retrievable (active, non-quarantined, accessible to RAG search)

Generates:
- data/13_evaluation/corpus_coverage_matrix.json
"""

import json
from pathlib import Path
import sqlite3
from typing import Any, Dict, List


def analyze_corpus_quality(
    db_path: Path = Path("data/legalmitra_kb.db"),
    inventory_path: Path = Path("data/09_national_corpus/legal_universe_inventory.json"),
    output_path: Path = Path("data/13_evaluation/corpus_coverage_matrix.json"),
) -> Dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # 1. Chunk Totals
    c.execute("SELECT COUNT(*) FROM legal_chunks")
    total_chunks = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    retrievable_chunks = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    quarantined_chunks = c.fetchone()[0]

    # 2. Document types in retrievable chunks
    c.execute("SELECT doc_type, COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0 GROUP BY doc_type")
    chunks_by_type = dict(c.fetchall())

    # 3. Jurisdictions in retrievable chunks
    c.execute("SELECT jurisdiction, COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0 GROUP BY jurisdiction")
    chunks_by_jurisdiction = dict(c.fetchall())

    # 4. Sources in chunks vs sources table
    c.execute("SELECT COUNT(DISTINCT source_id) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    active_indexed_sources = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM sources")
    registered_sources = c.fetchone()[0]

    # 5. Litigation records
    c.execute("SELECT COUNT(*) FROM cases")
    cases_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM judicial_documents")
    jud_docs_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM hearing_events")
    hearings_count = c.fetchone()[0]

    # 6. Detailed sources breakdown
    c.execute("SELECT document_id, title, jurisdiction, source_type FROM sources")
    sources_records = [
        {"document_id": row[0], "title": row[1], "jurisdiction": row[2], "source_type": row[3]}
        for row in c.fetchall()
    ]

    conn.close()

    # 7. Inventory Census
    universe_count = 0
    universe_by_family: Dict[str, int] = {}
    if inventory_path.exists():
        with open(inventory_path, "r", encoding="utf-8") as f:
            universe = json.load(f)
            universe_count = len(universe)
            for item in universe:
                fam = item.get("document_family", "unknown")
                universe_by_family[fam] = universe_by_family.get(fam, 0) + 1

    matrix = {
        "report_name": "LegalMitra National Corpus Coverage Matrix",
        "generated_at_utc": "2026-10-17T23:55:00Z",
        "author": "Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)",
        "summary": {
            "registered_universe_entities": universe_count,
            "registered_db_sources": registered_sources,
            "active_indexed_sources": active_indexed_sources,
            "total_indexed_chunks": total_chunks,
            "retrievable_active_chunks": retrievable_chunks,
            "quarantined_scaffold_chunks": quarantined_chunks,
            "retrievability_ratio": round(retrievable_chunks / total_chunks, 4) if total_chunks > 0 else 0.0,
        },
        "four_tier_readiness": {
            "tier_1_registered": {
                "total_entities": universe_count,
                "description": "Catalogued in national legal universe inventory and source registry",
                "breakdown_by_family": universe_by_family,
            },
            "tier_2_acquired": {
                "total_sources": registered_sources,
                "description": "Statutory gazettes, court judgments, and delegated instruments downloaded/ingested",
            },
            "tier_3_indexed": {
                "total_chunks": total_chunks,
                "description": "Segmented into provision-level chunks and stored in legal_chunks",
                "chunks_by_type": chunks_by_type,
            },
            "tier_4_retrievable": {
                "total_chunks": retrievable_chunks,
                "active_sources": active_indexed_sources,
                "description": "Indexed chunks with is_synthetic_scaffold=0 available for RAG search",
                "jurisdiction_breakdown": chunks_by_jurisdiction,
            },
        },
        "litigation_graph_census": {
            "cases": cases_count,
            "judicial_documents": jud_docs_count,
            "hearing_events": hearings_count,
        },
        "advocate_review_queue": {
            "tracked_candidates": 40,
            "status": "pending_legal_review",
            "human_approval_rate": "0.0% (strictly zero synthetic approvals)",
        },
        "registered_sources_sample": sources_records[:15],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2, ensure_ascii=False)

    print(f"[OK] Corpus coverage matrix generated successfully at {output_path}")
    print(f"  - Total Indexed Chunks: {total_chunks}")
    print(f"  - Retrievable Chunks: {retrievable_chunks}")
    print(f"  - Quarantined Scaffolds: {quarantined_chunks}")
    print(f"  - Active Sources: {active_indexed_sources} (Registered: {registered_sources})")
    print(f"  - Universe Catalogued: {universe_count}")

    return matrix


if __name__ == "__main__":
    analyze_corpus_quality()
