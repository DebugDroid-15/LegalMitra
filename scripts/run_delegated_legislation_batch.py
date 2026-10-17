"""
Batch Ingestion Script for Delegated Legislation & Commencement Notifications (Phase 16C)
Loads subordinate legal instruments, registers their source provenance,
and indexes verbatim sections into data/legalmitra_kb.db.
"""

import json
import logging
from pathlib import Path
from datetime import date

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.corpus.delegated import get_delegated_instruments
from legalmitra.ingestion.acquisition import LegislationAcquisitionManager
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.schemas.registry import SourceRegistryRecord

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger("run_delegated_batch")


def run_delegated_batch():
    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    reg_mgr = SourceRegistryManager(registry_file="registry/source_registry.jsonl")

    instruments = get_delegated_instruments()
    logger.info(f"Loaded {len(instruments)} delegated instruments for ingestion.")

    indexed_count = 0
    records_export = []

    for doc in instruments:
        # Determine source type
        is_commence = "NOTIF-COMMENCE" in doc.source_id
        src_type = SourceType.NOTIFICATION if is_commence else SourceType.RULES_REGULATION

        # Create/Register Source Registry Record
        source_rec = SourceRegistryRecord(
            document_id=doc.source_id,
            title=doc.act_title,
            source_url=f"https://egazette.gov.in/search/{doc.act_number}",
            source_type=src_type,
            jurisdiction=doc.jurisdiction,
            court=CourtType.NONE,
            document_date=doc.enactment_date,
            effective_date=doc.effective_date,
            licence_or_terms="Government of India Open Data License (GODL-India)",
            checksum="0000000000000000000000000000000000000000000000000000000000000000",
            raw_file_path=f"data/08_corpus/delegated/{doc.source_id}.txt",
            file_format=".txt",
            byte_size=sum(len(s.full_verbatim_text) for s in doc.sections),
            privacy_redaction_notes="Public statutory subordinate instrument. No privacy redactions needed."
        )

        # Clear existing chunks if any
        kb.clear_source_chunks(doc.source_id)

        # Index source and sections
        chunks_indexed = kb.index_statute_document(doc, source_rec=source_rec)
        indexed_count += chunks_indexed
        logger.info(f"Indexed delegated instrument {doc.source_id}: {chunks_indexed} chunks.")

        records_export.append({
            "source_id": doc.source_id,
            "title": doc.act_title,
            "gazette_number": doc.act_number,
            "source_type": src_type.value,
            "enactment_date": doc.enactment_date.isoformat(),
            "effective_date": doc.effective_date.isoformat() if doc.effective_date else None,
            "sections_indexed": len(doc.sections),
            "chunks_indexed": chunks_indexed,
            "extraction_status": "fully_extracted" if is_commence else "partially_extracted"
        })

    # Export records to data/08_corpus/delegated_legislation.json
    out_path = Path("data/08_corpus/delegated_legislation.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records_export, f, indent=2)

    logger.info(f"[OK] Saved delegated legislation manifest to {out_path}")
    print(f"\n=== Successfully indexed {len(instruments)} delegated instruments ({indexed_count} chunks) ===")


if __name__ == "__main__":
    run_delegated_batch()
