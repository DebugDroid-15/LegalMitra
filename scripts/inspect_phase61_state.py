import sqlite3
import json
import os

def inspect_state():
    print("=== Phase 61 State Inspection ===")
    
    # 1. KB Database
    if os.path.exists("data/legalmitra_kb.db"):
        conn = sqlite3.connect("data/legalmitra_kb.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM legal_chunks")
        total_chunks = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
        scaffold_chunks = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
        authentic_chunks = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM sources")
        total_sources = c.fetchone()[0]
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in c.fetchall()]
        print(f"KB Database:")
        print(f"  Total chunks: {total_chunks}")
        print(f"  Authentic chunks: {authentic_chunks}")
        print(f"  Scaffold chunks: {scaffold_chunks}")
        print(f"  Total sources: {total_sources}")
        print(f"  Tables: {tables}")
        conn.close()
    else:
        print("KB Database not found!")

    # 2. Conversations Database
    if os.path.exists("data/conversations.db"):
        conn = sqlite3.connect("data/conversations.db")
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in c.fetchall()]
        print(f"Conversations Database:")
        print(f"  Tables: {tables}")
        for t in tables:
            c.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = c.fetchone()[0]
            print(f"    {t}: {cnt} rows")
        conn.close()

    # 3. Source Registry
    if os.path.exists("data/09_national_corpus/source_monitoring_state.json"):
        with open("data/09_national_corpus/source_monitoring_state.json", encoding="utf-8") as f:
            src_state = json.load(f)
        if isinstance(src_state, dict):
            src_len = len(src_state.get('sources', src_state))
        elif isinstance(src_state, list):
            src_len = len(src_state)
        else:
            src_len = "unknown"
        print(f"Source Monitoring State: {src_len} entries")
    
    # 4. Review Tracking Register
    if os.path.exists("data/07_batches/review/review_tracking_register.json"):
        with open("data/07_batches/review/review_tracking_register.json", encoding="utf-8") as f:
            review_state = json.load(f)
        records = review_state.get("records", [])
        statuses = {}
        for r in records:
            st = r.get("review_status", "UNKNOWN")
            statuses[st] = statuses.get(st, 0) + 1
        print(f"Review Tracking Register:")
        print(f"  Total records: {len(records)}")
        print(f"  Status breakdown: {statuses}")

    # 5. Benchmark V14
    if os.path.exists("data/22_central_legislation/benchmark_v14_manifest.json"):
        with open("data/22_central_legislation/benchmark_v14_manifest.json", encoding="utf-8") as f:
            b14 = json.load(f)
        print(f"Benchmark V14 Manifest:")
        print(f"  Benchmark ID: {b14.get('benchmark_id')}")
        print(f"  Total cases: {b14.get('total_cases')}")
        splits = b14.get("splits", {})
        print(f"  Splits: { {k: len(v) for k, v in splits.items()} }")

    # 6. Release Gates Manifest
    if os.path.exists("data/22_central_legislation/release_gates_manifest.json"):
        with open("data/22_central_legislation/release_gates_manifest.json", encoding="utf-8") as f:
            rg = json.load(f)
        print(f"Release Gates Manifest:")
        print(f"  Release ID: {rg.get('release_id')}")
        print(f"  Target release: {rg.get('target_release')}")
        print(f"  Gate count: {len(rg.get('gates', {}))}")
        print(f"  Overall decision: {rg.get('overall_decision')}")

if __name__ == "__main__":
    inspect_state()
