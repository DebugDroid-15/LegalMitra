"""
Script: scripts/run_phase24_central_acts.py
Executes controlled, verifiable batch ingestion of Phase 24 Central Legislation:
- Bharatiya Sakshya Adhiniyam, 2023 (BSA)
- Bharatiya Nyaya Sanhita, 2023 (BNS)
- Protection of Children from Sexual Offences (POCSO) Act, 2012
- Right to Information Act, 2005 (RTI)
- Motor Vehicles Act, 1988 (MVA)
"""

from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.ingestion.central_acts_phase24 import list_phase24_statute_documents
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.schemas.registry import SourceRegistryRecord


def run_phase24_central_acts():
    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    docs = list_phase24_statute_documents()
    print(f"Loaded {len(docs)} central statute documents for Phase 24 expansion.")

    total_new_chunks = 0
    results = []

    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    for doc in docs:
        doc_id = doc.source_id
        doc_title = doc.act_title
        total_text = " ".join(s.full_verbatim_text for s in doc.sections)
        sha256 = hashlib.sha256(total_text.encode("utf-8")).hexdigest()

        # Check or insert into sources table
        c.execute("SELECT document_id FROM sources WHERE document_id = ?", (doc_id,))
        exists = c.fetchone()
        if not exists:
            c.execute("""
                INSERT INTO sources (
                    document_id, title, source_url, source_type, jurisdiction, court,
                    document_date, effective_date, is_historical, is_synthetic_scaffold,
                    repeal_status, checksum, verification_status, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc_id,
                doc_title,
                f"https://www.indiacode.nic.in/handle/123456789/{doc_id}",
                "statute",
                "IN",
                "None",
                doc.enactment_date.isoformat() if doc.enactment_date else "2023-12-25",
                "2024-07-01" if "2023" in doc_id else "2005-10-12",
                0,
                0,
                "in_force",
                sha256,
                "verified_authoritative",
                json.dumps({"act_number": doc.act_number, "phase": "phase_24"})
            ))
            conn.commit()
            print(f"Registered new source record: {doc_id} ({doc_title})")

        # Index individual sections
        added_for_doc = 0
        for sec in doc.sections:
            chunk_id = f"{sec.source_id}:{sec.section_number.replace(' ', '_').upper()}"

            # Check if chunk already exists
            c.execute("SELECT chunk_id FROM legal_chunks WHERE chunk_id = ?", (chunk_id,))
            if c.fetchone():
                continue

            # Insert chunk into legal_chunks
            c.execute("""
                INSERT INTO legal_chunks (
                    chunk_id, source_id, doc_type, act_or_case_title, provision_or_para_ref,
                    hierarchy_level, section_number, paragraph_number, jurisdiction, court,
                    document_date, effective_date, is_historical, is_synthetic_scaffold,
                    authority_level, content, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chunk_id,
                doc_id,
                "statute",
                doc_title,
                f"{sec.section_number} - {sec.section_title}",
                "section",
                sec.section_number,
                None,
                "IN",
                "None",
                doc.enactment_date.isoformat() if doc.enactment_date else "2023-12-25",
                "2024-07-01" if "2023" in doc_id else "2005-10-12",
                0,
                0,
                "binding_statute",
                f"{sec.section_number} ({sec.section_title}):\n{sec.full_verbatim_text}",
                json.dumps({
                    "chapter_number": sec.chapter_number,
                    "chapter_title": sec.chapter_title,
                    "section_title": sec.section_title,
                    "phase": "phase_24",
                })
            ))

            # Insert into FTS5
            c.execute("""
                INSERT INTO legal_chunks_fts (chunk_id, content, act_or_case_title, provision_or_para_ref)
                VALUES (?, ?, ?, ?)
            """, (
                chunk_id,
                f"{sec.section_number} ({sec.section_title}):\n{sec.full_verbatim_text}",
                doc_title,
                f"{sec.section_number} - {sec.section_title}",
            ))

            added_for_doc += 1
            total_new_chunks += 1

        conn.commit()
        print(f"Indexed {added_for_doc} new sections for {doc_title} (Source ID: {doc_id}).")
        results.append({
            "source_id": doc_id,
            "title": doc_title,
            "new_chunks_indexed": added_for_doc,
            "total_sections": len(doc.sections),
        })

    conn.close()

    # Save summary report
    out_path = Path("data/08_corpus/phase24_central_acts_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "batch_id": "BATCH_24_CENTRAL_ACTS_COMPLETION",
            "total_new_chunks": total_new_chunks,
            "documents": results,
        }, f, indent=2)

    print(f"\n[OK] Phase 24 Central Legislation Batch Completed: {total_new_chunks} new chunks indexed.")
    return results


if __name__ == "__main__":
    run_phase24_central_acts()
