"""
Script to export authoritative Indian statutory amendment relationships to JSON (Phase 15D).
Outputs data/08_corpus/amendment_relationships.json.
"""

from pathlib import Path
from legalmitra.corpus.amendments import build_default_amendment_history


def main() -> None:
    print("Building LegalMitra Statutory Amendment Relationships (Phase 15D)...")
    mgr = build_default_amendment_history()
    instruments = mgr.list_instruments()
    relationships = mgr.list_relationships()

    print(f"Total amendment instruments registered: {len(instruments)}")
    print(f"Total provision-level amendment relationships: {len(relationships)}")

    target_path = Path("data/08_corpus/amendment_relationships.json")
    mgr.export_json(target_path)
    print(f"Exported amendment relationships JSON: {target_path} ({target_path.stat().st_size} bytes)")

    print("\nRegistered Amending Instruments:")
    for inst in instruments:
        rels = [r for r in relationships if r.amending_instrument_id == inst.instrument_id]
        print(f"  [{inst.instrument_id}] {inst.official_title}")
        print(f"     Act: {inst.act_number} ({inst.year}) | Commenced: {inst.commencement_date} | Affects: {len(rels)} provisions")


if __name__ == "__main__":
    main()

