"""
Script to execute controlled, idempotent corpus ingestion for LegalMitra (Phase 14E).
Runs ingestion across available normalized sources, validates quality gates,
and updates data/08_corpus/coverage_inventory.json.
"""

from pathlib import Path
from legalmitra.corpus.inventory import CorpusInventoryManager
from legalmitra.ingestion.corpus_ingestor import CorpusIngestionPipeline
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


def main() -> None:
    print("=== LegalMitra National Indian Legal Corpus Ingestion Runner (Phase 14E) ===")

    kb = LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
    reg_mgr = SourceRegistryManager(registry_file="registry/source_registry.jsonl")

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

    normalized_dir = Path("data/02_normalized")
    candidate_files = [f for f in normalized_dir.glob("*.json") if f.is_file()]

    print(f"Found {len(candidate_files)} candidate normalized files in {normalized_dir}.")

    result = pipeline.execute_batch(
        batch_name="STAGE_2_CENTRAL_LEGISLATION",
        file_paths=candidate_files,
        force_reindex=False,
    )

    print("\nIngestion Batch Results:")
    print(f"  - Batch Name: {result.batch_name}")
    print(f"  - Total Candidates Evaluated: {result.total_sources}")
    print(f"  - Successfully Indexed: {result.successfully_indexed}")
    print(f"  - Skipped (Already Indexed / Idempotent): {result.skipped_existing}")
    print(f"  - Quarantined: {result.quarantined}")
    print(f"  - Failed: {result.failed}")
    print(f"  - New Indexed Chunks: {result.indexed_chunk_count}")

    if result.errors:
        print("\nErrors encountered:")
        for err in result.errors:
            print(f"  - [{err['document_id']}] {err['error']}")

    if inv_mgr:
        # Re-sync all live chunk counts from DB
        conn = kb.conn
        cur = conn.cursor()
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
        print(f"\n[OK] Updated coverage inventory with live chunk counts: {inv_path} & {csv_path}")

    # Display total chunks in Knowledge Base
    total_kb_chunks = kb.conn.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
    print(f"\nTotal Chunks in Legal Knowledge Base: {total_kb_chunks}")


if __name__ == "__main__":
    main()
