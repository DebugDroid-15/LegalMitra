"""Audit record counts and provenance across LegalMitra data files."""

import json
import sqlite3
import os

def audit():
    print("=== Workstream B Record Reconciliation Audit ===")
    
    # 1. Existing caselaw baseline
    p1 = "data/21_judicial_infrastructure/existing_caselaw_baseline.json"
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
            print(f"existing_caselaw_baseline.json documents count: {len(d.get('documents', []))}")
            if "baseline_metrics" in d:
                print(f"  baseline_metrics: {d['baseline_metrics']}")

    # 2. Representative acquisition batch
    p2 = "data/21_judicial_infrastructure/representative_acquisition_batch.json"
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
            print(f"representative_acquisition_batch.json items count: {len(d)}")

    # 3. Judicial coverage matrix v2
    p3 = "data/21_judicial_infrastructure/judicial_coverage_matrix_v2.json"
    if os.path.exists(p3):
        with open(p3, "r", encoding="utf-8") as f:
            d = json.load(f)
            print(f"judicial_coverage_matrix_v2.json summary: {d.get('summary')}")
            assessments = d.get("assessments", {})
            print(f"  total institutions in v2: {len(assessments)}")
            sum_ingested = sum(a.get("ingested_record_count", 0) for a in assessments.values())
            sum_verified = sum(a.get("verified_record_count", 0) for a in assessments.values())
            print(f"  sum of ingested across v2 assessments: {sum_ingested}, verified: {sum_verified}")
            for cid, a in assessments.items():
                print(f"    v2 {cid}: ingested={a.get('ingested_record_count')} tier={a.get('tier_label')}")

    # 4. Judicial coverage matrix v3
    p4 = "data/21_judicial_infrastructure/judicial_coverage_matrix_v3.json"
    if os.path.exists(p4):
        with open(p4, "r", encoding="utf-8") as f:
            d = json.load(f)
            print(f"judicial_coverage_matrix_v3.json summary: {d.get('summary')}")
            assessments = d.get("assessments", {})
            print(f"  institutions in v3 assessments dictionary: {len(assessments)}")
            for cid, a in assessments.items():
                print(f"    v3 {cid}: ingested={a.get('ingested_record_count')} verified={a.get('verified_record_count')}")
            sum_ingested_v3 = sum(a.get("ingested_record_count", 0) for a in assessments.values())
            sum_verified_v3 = sum(a.get("verified_record_count", 0) for a in assessments.values())
            print(f"  sum of ingested across v3 assessments: {sum_ingested_v3}, verified: {sum_verified_v3}")

    # 5. SQLite legalmitra_kb.db
    p5 = "data/legalmitra_kb.db"
    if os.path.exists(p5):
        conn = sqlite3.connect(p5)
        cur = conn.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        print(f"\nlegalmitra_kb.db tables: {tables}")
        for t in tables:
            cnt = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            print(f"  table {t}: count={cnt}")
        
        cols = [r[1] for r in cur.execute("PRAGMA table_info(legal_chunks)").fetchall()]
        print(f"legal_chunks columns: {cols}")
        rows = cur.execute("SELECT chunk_id, is_synthetic_scaffold, source_id FROM legal_chunks WHERE chunk_id LIKE '%IND-JUD-DEL-2024-BAIL%'").fetchall()
        print(f"scaffold chunks found: {len(rows)}")
        for r in rows:
            print(f"  {r}")
        conn.close()

    # 6. SQLite conversations.db
    p6 = "data/conversations.db"
    if os.path.exists(p6):
        conn = sqlite3.connect(p6)
        cur = conn.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        print(f"\nconversations.db tables: {tables}")
        for t in tables:
            cnt = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            print(f"  table {t}: count={cnt}")
        conn.close()

if __name__ == "__main__":
    audit()
