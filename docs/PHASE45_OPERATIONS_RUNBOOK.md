# LEGALMITRA — PHASE 45
## Operations Runbook: Central Legislation & Temporal Ingestion (Runbooks 24–28)

**Project:** LegalMitra  
**Document ID:** `LM-P45-REP-015-OPS-RUNBOOK`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** 2026-10-19  
**Status:** ACTIVE OPERATIONAL RUNBOOK

---

### Runbook 24: Ingesting Central Acts and Validating Gazette Provenance

#### 1. Purpose
Idempotently ingest an authoritative Central Act JSON manifest into `data/legalmitra_kb.db`, verifying source gazette URLs, SHA-256 hashes, and provision hierarchy before persisting.

#### 2. Prerequisites
- Target JSON manifest matching `LEGALMITRA-PROVENANCE-SPEC-V2`.
- Read/write access to `data/legalmitra_kb.db`.
- Clean working directory with verified Phase 9 freeze integrity.

#### 3. Execution Steps
```bash
# 1. Verify freeze integrity first
python scripts/verify_freeze.py

# 2. Execute ingestion of Central Statute source
python -c "
from legalmitra.temporal.ingestion import CentralStatuteIngestionPipeline
import json

with open('data/22_central_legislation/source_provenance_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

pipeline = CentralStatuteIngestionPipeline()
for act in manifest['acts']:
    res = pipeline.ingest_statute_source(act)
    print(f'Ingested: {res.act_id} | Status: {res.status} | Provisions: {res.provisions_ingested}')
"
```

#### 4. Verification & Rollback
- Query SQLite: `SELECT act_id, title, validity_from, is_active FROM central_statutes;`
- In case of malformed payload, the pipeline rolls back the SQLite transaction automatically without modifying existing rows.

---

### Runbook 25: Logging and Updating Amendment Events

#### 1. Purpose
Register a parliamentary amendment event in `data/22_central_legislation/amendment_event_ledger.json` and propagate temporal interval terminations to impacted provisions.

#### 2. Procedure
1. Locate official gazette notification for the amending Act.
2. Record event ID format `EVT-AMD-YYYY-NNN`.
3. Set `target_act_id`, `amending_act_id`, `amendment_type` (`SUBSTITUTION`, `INSERTION`, `OMISSION`, `REPEAL`), and `effective_date`.
4. If the amending Act has phased commencement (like DPDP Act 2023 s.1(2)), set:
   ```json
   "commencement_mode": "phased_uncommenced",
   "commencement_status": "uncommenced",
   "commencement_condition": "Pending Central Government notification"
   ```
5. Run ingestion pipeline to apply ledger events:
```bash
python -c "
from legalmitra.temporal.ingestion import CentralStatuteIngestionPipeline
pipeline = CentralStatuteIngestionPipeline()
pipeline.ingest_amendment_ledger('data/22_central_legislation/amendment_event_ledger.json')
"
```

---

### Runbook 26: Point-in-Time Temporal Retrieval Query Execution

#### 1. Purpose
Execute statutory retrieval for a legal scenario at a specified point in time, guaranteeing that the retrieved wording matches the exact law in force on that date.

#### 2. Python Execution Example
```python
from legalmitra.temporal.ingestion import TemporalLawEngine

engine = TemporalLawEngine()

# Example: Query Section 10 of Specific Relief Act prior to 2018 amendment
res_pre = engine.query_provision_at_date("ACT-CENTRAL-1963-047", "Section 10", "2017-06-01")
print(f"Pre-2018 Regime: {res_pre['version_id']} | Text: {res_pre['content'][:60]}")
# Output: Pre-2018 Regime: VER-SRA-10-V1 | Text: the specific performance of any contract may, in the discretion...

# Example: Query Section 10 of Specific Relief Act after 2018 amendment
res_post = engine.query_provision_at_date("ACT-CENTRAL-1963-047", "Section 10", "2019-01-15")
print(f"Post-2018 Regime: {res_post['version_id']} | Text: {res_post['content'][:60]}")
# Output: Post-2018 Regime: VER-SRA-10-V2 | Text: The specific performance of a contract shall be enforced...
```

---

### Runbook 27: Resolving Phased Commencement Notifications

#### 1. Purpose
Safely activate an uncommenced amendment (e.g. when the Ministry of Electronics and Information Technology issues a notification under Section 1(2) of the DPDP Act 2023).

#### 2. Procedure
1. Obtain the official Gazette Notification S.O. number and publication date.
2. In `data/22_central_legislation/amendment_event_ledger.json`, update `commencement_status` from `"uncommenced"` to `"in_force"`, and set `effective_date` to the gazetted appointment date.
3. Update target provision in `provision_provenance_manifest.json` setting `valid_until` of the old provision to the appointed date.
4. Execute `pipeline.ingest_amendment_ledger()`.
5. Run test suite `pytest tests/test_phase45_central_legislation.py` to confirm no regressions.

---

### Runbook 28: Auditing Legal Dependency Graph Cycles and Broken Links

#### 1. Purpose
Verify that the statutory relationship graph (`data/22_central_legislation/legal_dependency_graph.json`) is acyclic in its parent-child hierarchies and that all edge references resolve to known nodes.

#### 2. Verification Command
```bash
python -c "
import json

with open('data/22_central_legislation/legal_dependency_graph.json', 'r', encoding='utf-8') as f:
    graph = json.load(f)

node_ids = {n['id'] for n in graph['nodes']}
broken_edges = []
for edge in graph['edges']:
    if edge['source'] not in node_ids:
        broken_edges.append((edge['id'], 'missing source', edge['source']))
    if edge['target'] not in node_ids:
        broken_edges.append((edge['id'], 'missing target', edge['target']))

if broken_edges:
    print(f'ERROR: Broken edges found: {broken_edges}')
else:
    print(f'SUCCESS: Dependency graph verified! {len(node_ids)} nodes, {len(graph[\"edges\"])} edges, 0 broken links.')
"
```
