"""
Script to build and export official Indian legal repositories catalog to JSON (Phase 14C).
Outputs data/08_corpus/source_repositories.json.
"""

from pathlib import Path
from legalmitra.corpus.discovery import build_default_source_catalog


def main() -> None:
    print("Building LegalMitra Official Source Repositories Catalog (Phase 14C)...")
    mgr = build_default_source_catalog()
    repos = mgr.list_repos()

    print(f"Total repositories registered: {len(repos)}")

    target_path = Path("data/08_corpus/source_repositories.json")
    mgr.export_json(target_path)
    print(f"Exported repositories JSON: {target_path} ({target_path.stat().st_size} bytes)")

    print("\nOfficial Repositories by Authority:")
    for r in repos:
        print(f"  [{r.repository_id}] {r.name}")
        print(f"     Authority: {r.authority} | Tier: {r.verification_tier.value} | Rate Limit: {r.rate_limit_per_minute}/min")


if __name__ == "__main__":
    main()

