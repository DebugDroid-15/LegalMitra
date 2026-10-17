"""
Runner script for executing reproducible National Corpus Ingestion Batches (Phase 19).
Supports dry-run verification mode, batch selection, hash validation, and manifest generation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from legalmitra.ingestion.central_acts import list_central_act_documents
from legalmitra.ingestion.landmark_judgments import get_landmark_judgment_documents
from legalmitra.ingestion.national_corpus_pipeline import NationalCorpusPipeline
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


def main():
    parser = argparse.ArgumentParser(description="Run National Corpus Ingestion Batch")
    parser.add_argument("--batch-id", type=str, default="BATCH-PHASE19-EXPANSION-01", help="Unique identifier for the batch")
    parser.add_argument("--dry-run", action="store_true", help="Report planned changes without modifying database")
    parser.add_argument("--category", type=str, choices=["all", "statutes", "judgments"], default="all", help="Target corpus category")
    parser.add_argument("--db-path", type=str, default="data/legalmitra_kb.db", help="Path to SQLite knowledge base")
    args = parser.parse_args()

    print(f"=== LegalMitra National Corpus Ingestion: {args.batch_id} ===")
    print(f"Dry Run: {args.dry_run} | Category: {args.category} | DB: {args.db_path}")

    kb = LegalKnowledgeBase(db_path=args.db_path, must_exist=False)
    pipeline = NationalCorpusPipeline(kb=kb, db_path=Path(args.db_path))

    if args.category in ["all", "statutes"]:
        statutes = list_central_act_documents()
        print(f"Running statute batch with {len(statutes)} documents...")
        statute_manifest = pipeline.run_statute_batch(
            batch_id=f"{args.batch_id}-STATUTES",
            statute_docs=statutes,
            dry_run=args.dry_run
        )
        print(f"[OK] Statute Batch Complete: {statute_manifest.documents_indexed} docs, {statute_manifest.chunks_created} chunks.")

    if args.category in ["all", "judgments"]:
        judgments = get_landmark_judgment_documents()
        print(f"Running judgment batch with {len(judgments)} documents...")
        judgment_manifest = pipeline.run_judgment_batch(
            batch_id=f"{args.batch_id}-JUDGMENTS",
            judgment_docs=judgments,
            dry_run=args.dry_run
        )
        print(f"[OK] Judgment Batch Complete: {judgment_manifest.documents_indexed} docs, {judgment_manifest.chunks_created} chunks, {judgment_manifest.quarantined_count} quarantined.")

    kb.close()
    print("=== Batch Execution Concluded Successfully ===")


if __name__ == "__main__":
    main()

