# LEGALMITRA — PHASE 48 RUNBOOK 41
## Operational Runbook: Cross-Statute Definition Lookup & Conflation Guard

**Runbook ID:** `LM-RUNBOOK-48-041`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Resolve statutory terms across enactments and identify semantic divergence warnings.

### 2. Operational Procedure
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()
comp = engine.compare_cross_statute_definitions("goods")
print("Warning:", comp["doctrinal_warning"])
for statute, d in comp["definitions"].items():
    print(f"[{statute}] Section {d['section']}: {d['verbatim_excerpt'][:80]}...")
```

### 3. Expected Output
Identifies that shares are goods under SOGA s.2(7) but strictly excluded under CGST s.2(52).
