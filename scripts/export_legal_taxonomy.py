"""
Script to build and export the comprehensive Indian Legal Taxonomy to JSON (Phase 14B).
Outputs data/08_corpus/legal_taxonomy.json.
"""

from pathlib import Path
from legalmitra.corpus.taxonomy import build_default_indian_legal_taxonomy


def main() -> None:
    print("Building LegalMitra Indian Legal Taxonomy (Phase 14B)...")
    mgr = build_default_indian_legal_taxonomy()
    nodes = mgr.list_nodes()
    root_nodes = mgr.get_root_nodes()

    print(f"Total taxonomy nodes: {len(nodes)}")
    print(f"Root legal domains: {len(root_nodes)}")

    target_path = Path("data/08_corpus/legal_taxonomy.json")
    mgr.export_json(target_path)
    print(f"Exported taxonomy JSON: {target_path} ({target_path.stat().st_size} bytes)")

    print("\nRoot Legal Domains:")
    for root in root_nodes:
        children = mgr.get_children(root.code)
        print(f"  [{root.code}] {root.name} ({len(children)} sub-domains)")
        for child in children:
            print(f"     - [{child.code}] {child.name}")


if __name__ == "__main__":
    main()

