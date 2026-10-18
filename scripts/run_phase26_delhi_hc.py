"""
Script: scripts/run_phase26_delhi_hc.py
Executes controlled batch ingestion of Delhi High Court Phase 26 judgments, cases,
procedural orders, and hearing events into data/legalmitra_kb.db.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from legalmitra.ingestion.delhi_high_court_phase26 import (
    get_delhi_hc_phase26_hearing_events,
    get_delhi_hc_phase26_judgments,
    get_delhi_hc_phase26_orders,
    get_delhi_hc_phase26_unified_cases,
)
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


def run_phase26_delhi_hc():
    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    print(f"Connected to Knowledge Base: {kb.db_path}")

    # 1. Ingest Judgment Documents
    judgments = get_delhi_hc_phase26_judgments()
    total_new_chunks = 0
    judgment_results = []
    print(f"\n[1/4] Ingesting {len(judgments)} Delhi High Court Judgments...")
    for doc in judgments:
        count = kb.index_judgment_document(doc, is_synthetic_scaffold=False)
        total_new_chunks += count
        judgment_results.append({
            "source_id": doc.source_id,
            "case_title": doc.case_title,
            "chunks_indexed": count,
            "court": str(doc.court),
            "date": doc.judgment_date.isoformat(),
        })
        print(f"  -> Indexed '{doc.case_title}': {count} chunks.")

    # 2. Ingest Unified Cases
    cases = get_delhi_hc_phase26_unified_cases()
    print(f"\n[2/4] Ingesting {len(cases)} Delhi High Court Case Identity records...")
    for c in cases:
        kb.index_case(
            case_id=c.case_id,
            court_code=c.court_code,
            case_type=c.case_type,
            case_number=c.case_number,
            filing_year=c.filing_year,
            petitioner=c.petitioner_or_appellant,
            respondent=c.respondent,
            neutral_citation=c.neutral_citation,
            institution_date=c.institution_date.isoformat() if c.institution_date else None,
            disposal_date=c.disposal_date.isoformat() if c.disposal_date else None,
            status=c.status.value if hasattr(c.status, "value") else str(c.status),
            metadata={"citations": c.reporter_citations, "phase": "phase_26"}
        )
        print(f"  -> Ingested Case: {c.case_id} ({c.petitioner_or_appellant} v. {c.respondent})")

    # 3. Ingest Judicial Orders
    orders = get_delhi_hc_phase26_orders()
    print(f"\n[3/4] Ingesting {len(orders)} Delhi High Court Procedural / Interim Orders...")
    for o in orders:
        kb.index_judicial_document_record(
            document_id=o.document_id,
            case_id=o.case_id,
            classification=o.classification.value if hasattr(o.classification, "value") else str(o.classification),
            procedural_effect=o.procedural_effect.value if hasattr(o.procedural_effect, "value") else str(o.procedural_effect),
            order_date=o.order_or_judgment_date.isoformat(),
            bench_coram=o.bench_coram,
            verbatim_text=o.verbatim_text,
            source_url=o.source_url,
            sha256_hash=o.sha256_hash,
            is_synthetic=0,
            verification_status="verified_authoritative",
            metadata={"provisions": o.statutory_provisions_cited, "phase": "phase_26"}
        )
        print(f"  -> Ingested Order: {o.document_id} (Case: {o.case_id}, Type: {o.classification})")

    # 4. Ingest Hearing Events
    events = get_delhi_hc_phase26_hearing_events()
    print(f"\n[4/4] Ingesting {len(events)} Delhi High Court Dated Hearing Events...")
    for ev in events:
        kb.index_hearing_event_record(
            event_id=ev["event_id"],
            case_id=ev["case_id"],
            listing_date=ev["listing_date"],
            hearing_type=ev["hearing_type"],
            presiding_bench=ev["presiding_bench"],
            procedural_outcome=ev["procedural_outcome"],
            daily_order_id=ev.get("daily_order_id"),
            next_listing_date=ev.get("next_listing_date"),
            is_cause_list_verified=ev.get("is_cause_list_verified", 1),
            metadata={"phase": "phase_26"}
        )
        print(f"  -> Ingested Hearing Event: {ev['event_id']} (Case: {ev['case_id']}, Date: {ev['listing_date']})")

    kb.close()

    # Reconcile database state
    conn = sqlite3.connect("data/legalmitra_kb.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sources")
    sources_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM legal_chunks")
    chunks_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    active_chunks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM cases")
    cases_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM judicial_documents")
    docs_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM hearing_events")
    events_cnt = c.fetchone()[0]
    conn.close()

    out_file = Path("data/08_corpus/phase26_delhi_hc_ingestion_report.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "batch_id": "BATCH_26_DELHI_HIGH_COURT",
        "new_judgments_count": len(judgments),
        "total_new_chunks": total_new_chunks,
        "database_summary": {
            "sources": sources_cnt,
            "total_chunks": chunks_cnt,
            "active_retrievable_chunks": active_chunks,
            "cases": cases_cnt,
            "judicial_documents": docs_cnt,
            "hearing_events": events_cnt,
        },
        "judgments": judgment_results,
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print("\n==========================================")
    print("PHASE 26 DELHI HIGH COURT BATCH COMPLETE")
    print(f"Sources Registered: {sources_cnt}")
    print(f"Total Chunks: {chunks_cnt} (Active: {active_chunks})")
    print(f"Cases: {cases_cnt}")
    print(f"Judicial Documents: {docs_cnt}")
    print(f"Hearing Events: {events_cnt}")
    print("==========================================")
    return report_data


if __name__ == "__main__":
    run_phase26_delhi_hc()
