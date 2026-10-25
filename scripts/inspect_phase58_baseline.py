import sqlite3
import json
import hashlib
import os

def get_hash(path):
    if not os.path.exists(path):
        return 'MISSING'
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

kb_path = 'data/legalmitra_kb.db'
if os.path.exists(kb_path):
    conn = sqlite3.connect(kb_path)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM legal_chunks')
    tot_chunks = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1')
    scaffolds = cur.fetchone()[0]
    conn.close()
else:
    tot_chunks = scaffolds = 0

bm_path = 'data/22_central_legislation/temporal_benchmark_manifest.json'
rg_path = 'data/22_central_legislation/release_gates_manifest.json'

bm_data = json.load(open(bm_path, 'r', encoding='utf-8'))
rg_data = json.load(open(rg_path, 'r', encoding='utf-8'))

print('Total chunks:', tot_chunks)
print('Quarantined scaffolds:', scaffolds)
print('Benchmark:', bm_data.get('benchmark_suite_id'), bm_data.get('version'), len(bm_data.get('test_cases', [])), bm_data.get('split_counts'))
print('Benchmark hash:', get_hash(bm_path))
print('Release gates:', rg_data.get('release_id'), rg_data.get('target_version'), rg_data.get('overall_decision'), f"{rg_data.get('passed_gates')}/{rg_data.get('total_gates')} passed")
print('Release gates hash:', get_hash(rg_path))

conv_path = 'data/conversations.db'
print('Conversations DB exists:', os.path.exists(conv_path))
if os.path.exists(conv_path):
    conn = sqlite3.connect(conv_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print('Conversations tables:', tables)
    conn.close()
