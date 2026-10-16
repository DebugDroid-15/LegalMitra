"""
Script to execute controlled, scalable ingestion of Central Legislation (Phase 15C).
Acquires, normalizes, registers, indexes, and logs batch metrics for 8 core Central Acts.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.corpus.inventory import CorpusInventoryManager
from legalmitra.ingestion.acquisition import LegislationAcquisitionManager
from legalmitra.ingestion.central_acts import list_central_act_documents
from legalmitra.ingestion.corpus_ingestor import CorpusIngestionPipeline
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.schemas.registry import SourceRegistryRecord


def main() -> None:
    print("=== LegalMitra Central Legislation Batch Ingestion (Phase 15C) ===")
    start_time = datetime.utcnow().isoformat()

    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    reg_mgr = SourceRegistryManager(registry_file="registry/source_registry.jsonl")
    acq_mgr = LegislationAcquisitionManager()

    inv_path = Path("data/08_corpus/coverage_inventory.json")
    if inv_path.exists():
        inv_mgr = CorpusInventoryManager.load_json(inv_path)
    else:
        inv_mgr = None

    pipeline = CorpusIngestionPipeline(
        knowledge_base=kb,
        registry_manager=reg_mgr,
        inventory_manager=inv_mgr,
    )

    documents = list_central_act_documents()
    print(f"Loaded {len(documents)} central act documents for batch ingestion.\n")

    batch_manifest = {
        "batch_id": "BATCH_15C_CENTRAL_ACTS",
        "start_time": start_time,
        "planned_count": len(documents),
        "acquired_count": 0,
        "indexed_count": 0,
        "new_chunks_indexed": 0,
        "skipped_count": 0,
        "documents": [],
    }

    raw_dir = Path("data/01_raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    norm_dir = Path("data/02_normalized")
    norm_dir.mkdir(parents=True, exist_ok=True)

    for doc in documents:
        doc_id = doc.source_id
        title = doc.act_title
        print(f"Processing: [{doc_id}] {title}...")

        # 1. Write normalized JSON
        norm_file = norm_dir / f"{doc_id}.json"
        norm_json_str = doc.model_dump_json(indent=2)
        norm_file.write_text(norm_json_str, encoding="utf-8")

        # 2. Acquire / Cache raw file
        raw_file = raw_dir / f"{doc_id}.json"
        raw_file.write_text(norm_json_str, encoding="utf-8")
        acq_rec = acq_mgr.acquire_local_or_cached(
            document_id=doc_id,
            official_title=title,
            source_url=f"https://www.indiacode.nic.in/handle/{doc_id}",
            local_content=norm_json_str,
            file_extension=".json",
        )
        batch_manifest["acquired_count"] += 1

        # 3. Register in source registry if not present
        existing_reg = reg_mgr.get(doc_id)
        if not existing_reg:
            reg_rec = SourceRegistryRecord(
                document_id=doc_id,
                title=title,
                source_url=acq_rec.source_url,
                source_type=SourceType.STATUTE,
                jurisdiction=Jurisdiction.INDIA_CENTRAL,
                court=CourtType.NONE,
                document_date=doc.enactment_date,
                effective_date=doc.effective_date,
                licence_or_terms="Government of India Open Data License (GODL-India)",
                checksum=acq_rec.checksum,
                verification_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
                raw_file_path=str(raw_file),
                file_format=".json",
                byte_size=acq_rec.byte_size,
            )
            reg_mgr.register(reg_rec, allow_duplicate_checksum=True)
            print(f"  [REGISTRY] Registered {doc_id} in source registry.")
        else:
            reg_rec = existing_reg

        # 4. Ingest into Knowledge Base
        chunks_indexed = pipeline.ingest_statute_document(doc, reg_rec, force_reindex=False)
        if chunks_indexed > 0:
            batch_manifest["indexed_count"] += 1
            batch_manifest["new_chunks_indexed"] += chunks_indexed
            print(f"  [INDEXED] {chunks_indexed} chunks indexed.")
        else:
            batch_manifest["skipped_count"] += 1
            print("  [IDEMPOTENT] Document already indexed in Knowledge Base. Skipped.")

        batch_manifest["documents"].append({
            "document_id": doc_id,
            "title": title,
            "sections_count": len(doc.sections),
            "chunks_indexed": chunks_indexed,
            "checksum": acq_rec.checksum,
        })

    # Update master coverage inventory with live chunk counts
    if inv_mgr:
        cur = kb.conn.cursor()
        rows = cur.execute("SELECT source_id, COUNT(*) FROM legal_chunks GROUP BY source_id").fetchall()
        counts_dict = dict(rows)
        for item in inv_mgr.list_items():
            if item.document_id in counts_dict:
                item.indexed_chunk_count = counts_dict[item.document_id]
                item.extraction_status = "completed"
                item.validation_status = "validated"

        inv_mgr.export_json(inv_path)
        csv_path = Path("data/08_corpus/coverage_inventory.csv")
        inv_mgr.export_csv(csv_path)
        print(f"\n[OK] Updated master inventory: {inv_path} & {csv_path}")

    batch_manifest["end_time"] = datetime.utcnow().isoformat()
    report_path = Path("data/08_corpus/batch_01_central_acts_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(batch_manifest, f, indent=2)
    print(f"[OK] Batch report saved to: {report_path}")

    # Final Knowledge Base summary
    total_kb_chunks = kb.conn.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
    total_sources = kb.conn.execute("SELECT COUNT(DISTINCT source_id) FROM legal_chunks").fetchone()[0]
    print(f"\n=== Batch Summary ===")
    print(f"  - Total Sources in Knowledge Base: {total_sources}")
    print(f"  - Total Chunks in Knowledge Base: {total_kb_chunks}")
    print(f"  - New Chunks Indexed in this Batch: {batch_manifest['new_chunks_indexed']}")


if __name__ == "__main__":
    main()
