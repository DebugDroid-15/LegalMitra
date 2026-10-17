"""
Batch Ingestion Script for State Legislation (Phase 16E)
Acquires, normalizes, registers, and indexes Delhi and Maharashtra State Acts
into data/legalmitra_kb.db.
"""

import json
import logging
from pathlib import Path

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.ingestion.state_acts import get_state_statute_documents
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.schemas.registry import SourceRegistryRecord

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger("run_state_law_batch")


def run_state_law_batch():
    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    reg_mgr = SourceRegistryManager(registry_file="registry/source_registry.jsonl")

    state_docs = get_state_statute_documents()
    logger.info(f"Loaded {len(state_docs)} state statute documents for ingestion.")

    indexed_count = 0
    records_export = []

    for doc in state_docs:
        # Construct Source Registry Record
        source_rec = SourceRegistryRecord(
            document_id=doc.source_id,
            title=doc.act_title,
            source_url=f"https://www.indiacode.nic.in/handle/{doc.source_id}",
            source_type=SourceType.STATUTE,
            jurisdiction=doc.jurisdiction,
            court=CourtType.NONE,
            document_date=doc.enactment_date,
            effective_date=doc.effective_date,
            licence_or_terms="Government of India Open Data License (GODL-India)",
            checksum="0000000000000000000000000000000000000000000000000000000000000000",
            raw_file_path=f"data/08_corpus/state/{doc.source_id}.txt",
            file_format=".txt",
            byte_size=sum(len(s.full_verbatim_text) for s in doc.sections),
            privacy_redaction_notes="State legislative enactment. Open public data."
        )

        # Clear existing chunks if any
        kb.clear_source_chunks(doc.source_id)

        # Index document and sections
        chunks_indexed = kb.index_statute_document(doc, source_rec=source_rec)
        indexed_count += chunks_indexed
        logger.info(f"Indexed state act {doc.source_id} ({doc.jurisdiction.value}): {chunks_indexed} chunks.")

        records_export.append({
            "source_id": doc.source_id,
            "title": doc.act_title,
            "act_number": doc.act_number,
            "jurisdiction": doc.jurisdiction.value,
            "enactment_date": doc.enactment_date.isoformat(),
            "effective_date": doc.effective_date.isoformat() if doc.effective_date else None,
            "sections_indexed": len(doc.sections),
            "chunks_indexed": chunks_indexed,
            "extraction_status": "partially_extracted"
        })

    # Save state law batch report
    out_path = Path("data/08_corpus/state_law_batch_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records_export, f, indent=2)

    logger.info(f"[OK] Saved state law report to {out_path}")
    print(f"\n=== Successfully indexed {len(state_docs)} State Acts ({indexed_count} chunks) ===")


if __name__ == "__main__":
    run_state_law_batch()

