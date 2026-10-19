# LEGALMITRA — PHASE 46
## Operations Runbook: Commercial, Corporate, and Temporal Retrieval (Runbooks 29–33)

**Project:** LegalMitra  
**Document ID:** `LM-P46-REP-015-OPS-RUNBOOK`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** 2026-10-19  
**Status:** ACTIVE OPERATIONAL RUNBOOK

---

### Runbook 29: Ingesting Central Legislation Batch 2 and Verifying Spec V2 Hashes

#### 1. Purpose
Idempotently ingest Central Legislation Batch 2 manifests into `data/legalmitra_kb.db`, verifying source gazette URLs, SHA-256 hashes, and provision hierarchy before persisting.

#### 2. Execution Command
```bash
python -c "
from legalmitra.temporal.ingestion import CentralStatuteIngestionPipeline
import json

with open('data/22_central_legislation/source_provenance_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

pipeline = CentralStatuteIngestionPipeline()
for src in manifest['sources']:
    res = pipeline.ingest_instrument(src, [])
    print(f'Instrument: {res.instrument_id} | Status: {res.status.value} | SHA256: {res.sha256_hash[:12]}...')
"
```

#### 3. Verification
Query database to ensure 14 registered sources:
```bash
python scripts/audit_database.py
```

---

### Runbook 30: Querying Corporate CSR Regimes Across the 2021 Decriminalization Boundary

#### 1. Purpose
Resolve whether a corporate CSR non-compliance issue falls under the pre-2021 "comply or explain" regime (with Section 450 general criminal penalties) or the post-2021 mandatory unspent fund transfer and civil administrative penalty regime under Section 135(7).

#### 2. Python Query Execution
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()

# Example A: Query default for FY 2018-19 (Pre-amendment)
res_a = engine.resolve_companies_act_csr_regime("2019-05-15")
print(f"Pre-2021 Regime: {res_a['regime']}")
print(f"  Character: {res_a['csr_character']}")
print(f"  Penalty: {res_a['penalty_type']}")

# Example B: Query default for FY 2022-23 (Post-amendment)
res_b = engine.resolve_companies_act_csr_regime("2023-04-10")
print(f"Post-2021 Regime: {res_b['regime']}")
print(f"  Character: {res_b['csr_character']}")
print(f"  Penalty: {res_b['penalty_type']}")
print(f"  Notification: {res_b['notification_ref']}")
```

---

### Runbook 31: Querying IBC Clean-Slate Immunity and Section 29A Disqualification

#### 1. Purpose
Resolve whether a corporate debtor or successful resolution applicant is entitled to statutory clean-slate immunity under Section 32A of the Insolvency and Bankruptcy Code, 2016, and verify promoter eligibility under Section 29A.

#### 2. Python Query Execution
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()

# Query Clean-Slate Immunity post-approval in 2021
res = engine.resolve_ibc_clean_slate_regime("2021-06-15")
print(f"IBC Clean-Slate Active: {res['clean_slate_statutory_immunity']}")
print(f"Asset Attachment Bar: {res['asset_attachment_bar']}")
print(f"Governing Rule: {res['governing_rule']}")
```

---

### Runbook 32: Resolving Commercial Courts Act vs CPC Order VIII Rule 1 Deadlines

#### 1. Purpose
Determine whether a defendant's written statement filed beyond 90 days but within 120 days from summons service can be accepted by the court, distinguishing ordinary civil suits from commercial disputes of Specified Value.

#### 2. Python Query Execution
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()

# Case 1: Ordinary Civil Suit at Day 105
res_ord = engine.resolve_cpc_commercial_timeline(is_commercial_dispute=False, days_elapsed=105)
print(f"Ordinary Suit Day 105: Condonable={res_ord['delay_condonable']}, Forfeited={res_ord['right_to_file_forfeited']}")
# Expected: Condonable=True, Forfeited=False (Kailash v. Nanhku)

# Case 2: Commercial Dispute at Day 105
res_comm_105 = engine.resolve_cpc_commercial_timeline(is_commercial_dispute=True, days_elapsed=105)
print(f"Commercial Suit Day 105: Condonable={res_comm_105['delay_condonable']}, Forfeited={res_comm_105['right_to_file_forfeited']}")
# Expected: Condonable=True (on costs), Forfeited=False

# Case 3: Commercial Dispute at Day 125
res_comm_125 = engine.resolve_cpc_commercial_timeline(is_commercial_dispute=True, days_elapsed=125)
print(f"Commercial Suit Day 125: Condonable={res_comm_125['delay_condonable']}, Forfeited={res_comm_125['right_to_file_forfeited']}")
# Expected: Condonable=False, Forfeited=True (SCG Contracts)
```

---

### Runbook 33: Executing Point-in-Time Temporal Benchmark Suite V2 (PIT-V2)

#### 1. Purpose
Execute the full 20-scenario Point-in-Time Temporal Retrieval Benchmark Suite (`data/22_central_legislation/temporal_benchmark_manifest.json`) and verify 100% temporal precision.

#### 2. Execution Command
```bash
pytest tests/test_phase46_central_legislation_batch2.py -v
```

#### 3. Expected Output
All 20 test cases passing with zero temporal hallucinations, zero broken citations, and clean boundary date transitions.
