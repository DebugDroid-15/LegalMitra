"""
Script: scripts/run_phase24_judicial_batch.py
Executes controlled, verifiable batch ingestion of Phase 24 Judicial Decisions:
- 10 Landmark Supreme Court Judgments (Maneka Gandhi, Kesavananda, DK Basu, Lalita Kumari, Arnesh Kumar, Shreya Singhal, Sushila Aggarwal, Vidya Drolia, Jacob Mathew, Energy Watchdog)
- 10 UnifiedCaseIdentity entries
- 4 JudicialDocumentRecords (Notice orders, reference orders)
- 4 Dated HearingEvents

Maintains source traceability, synthetic scaffold segregation, and Article 141 precedent hierarchy.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from legalmitra.caselaw.case_identity import CaseStatus
from legalmitra.ingestion.landmark_judgments_phase24 import (
    get_phase24_hearing_events,
    get_phase24_orders_and_proceedings,
    get_phase24_judgment_documents,
    get_phase24_unified_cases,
)
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


def run_phase24_judicial_batch():
    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    print(f"Connecting to Knowledge Base at: {kb.db_path}")

    # 1. Ingest Judgment Documents into KB (sources + legal_chunks + FTS5)
    judgments = get_phase24_judgment_documents()
    print(f"\n[1/4] Ingesting {len(judgments)} Landmark Judgment Documents...")
    judgment_results = []
    total_new_chunks = 0

    for doc in judgments:
        chunks_count = kb.index_judgment_document(doc, is_synthetic_scaffold=False)
        total_new_chunks += chunks_count
        judgment_results.append({
            "source_id": doc.source_id,
            "case_title": doc.case_title,
            "chunks_indexed": chunks_count,
            "court": doc.court.value if hasattr(doc.court, "value") else str(doc.court),
            "date": doc.judgment_date.isoformat(),
        })
        print(f"  -> Indexed '{doc.case_title}': {chunks_count} chunks.")

    # 2. Ingest UnifiedCaseIdentity records
    cases = get_phase24_unified_cases()
    print(f"\n[2/4] Ingesting {len(cases)} Unified Case Identity records...")
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
            metadata={"phase": "phase_24", "citations": c.reporter_citations}
        )
        print(f"  -> Ingested Case: {c.case_id} ({c.petitioner_or_appellant} v. {c.respondent})")

    # 3. Ingest JudicialDocumentRecord (Orders)
    orders = get_phase24_orders_and_proceedings()
    print(f"\n[3/4] Ingesting {len(orders)} Interim / Notice Judicial Orders...")
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
            is_synthetic=1 if o.is_synthetic_scaffold else 0,
            verification_status=o.verification_status.value if hasattr(o.verification_status, "value") else str(o.verification_status),
            metadata={"statutory_provisions": o.statutory_provisions_cited, "precedents_cited": o.precedents_cited, "phase": "phase_24"}
        )
        print(f"  -> Ingested Order: {o.document_id} (Case: {o.case_id}, Type: {o.classification})")

    # 4. Ingest Hearing Events
    events = get_phase24_hearing_events()
    print(f"\n[4/4] Ingesting {len(events)} Dated Hearing Events...")
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
            metadata={"phase": "phase_24"}
        )
        print(f"  -> Ingested Hearing Event: {ev['event_id']} (Case: {ev['case_id']}, Date: {ev['listing_date']})")

    kb.close()

    # Re-verify database state
    conn = sqlite3.connect("data/legalmitra_kb.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sources")
    sources_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM legal_chunks")
    chunks_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    active_chunks_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM cases")
    cases_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM judicial_documents")
    docs_cnt = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM hearing_events")
    events_cnt = c.fetchone()[0]
    conn.close()

    # Save summary report
    out_path = Path("data/08_corpus/phase24_judicial_batch_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "batch_id": "BATCH_24_JUDICIAL_EXPANSION",
        "new_judgments_count": len(judgments),
        "total_new_chunks": total_new_chunks,
        "database_summary": {
            "sources": sources_cnt,
            "total_chunks": chunks_cnt,
            "active_retrievable_chunks": active_chunks_cnt,
            "cases": cases_cnt,
            "judicial_documents": docs_cnt,
            "hearing_events": events_cnt,
        },
        "judgments": judgment_results,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print("\n==========================================")
    print("PHASE 24 JUDICIAL BATCH EXECUTION COMPLETE")
    print(f"Sources Registered: {sources_cnt}")
    print(f"Total Chunks: {chunks_cnt} (Active: {active_chunks_cnt})")
    print(f"Cases: {cases_cnt}")
    print(f"Judicial Documents: {docs_cnt}")
    print(f"Hearing Events: {events_cnt}")
    print("==========================================")
    return report_data


if __name__ == "__main__":
    run_phase24_judicial_batch()
