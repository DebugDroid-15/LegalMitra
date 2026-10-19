# PHASE 47: OPERATIONS RUNBOOK (RUNBOOKS 34–38)

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 19, 2026  

---

## Runbook 34: Ingesting Intellectual Property Statutes & Verifying 2012/2005 Hashes
1. Load `data/22_central_legislation/source_provenance_manifest.json`.
2. Verify SHA-256 hashes for Copyright Act 1957, Patents Act 1970, and Trade Marks Act 1999.
3. Validate presence of `AMEND-EVT-021` (Copyright 2012) and `AMEND-EVT-022` (Patents 2005) in `amendment_event_ledger.json`.

---

## Runbook 35: Querying Labour Code Enactment vs Commencement Status
```python
from legalmitra.temporal.engine import build_default_temporal_engine
engine = build_default_temporal_engine()

# Query Industrial Relations Code 2020 status
status = engine.resolve_labour_code_commencement_status("IND-STAT-IRCODE-2020")
print(status["status"])  # Output: ENACTED_UNCOMMENCED
print(status["operative_predecessors"])  # Output: ['Industrial Disputes Act, 1947', ...]
```

---

## Runbook 36: Resolving Patent Section 3(d) Therapeutic Efficacy
```python
from legalmitra.temporal.engine import build_default_temporal_engine
engine = build_default_temporal_engine()

# Query polymorphic form patent eligibility in 2014
res = engine.resolve_patent_section3d_regime("2014-05-12")
assert res["therapeutic_efficacy_mandate"] is True
assert "Novartis AG" in res["landmark_precedent"]
```

---

## Runbook 37: Traversing Precedent-to-Statute Links with Passage Anchors
```python
from legalmitra.temporal.engine import build_default_temporal_engine
engine = build_default_temporal_engine()

# Retrieve precedent anchors for Patents Act Section 3(d)
links = engine.resolve_precedent_for_provision("IND-STAT-PATENTS-1970", "3(d)")
for l in links:
    print(l["case_title"], "->", l["paragraph_anchor"])
```

---

## Runbook 38: Executing Point-in-Time Benchmark Suite V3 (PIT-V3)
```powershell
pytest tests/test_phase47_ip_labour_precedents.py -v
```
