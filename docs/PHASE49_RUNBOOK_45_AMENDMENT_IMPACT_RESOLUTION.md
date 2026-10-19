# LEGALMITRA — PHASE 49 RUNBOOK 45
## Operational Runbook: Amendment Impact on Precedent Resolution

**Runbook ID:** `LM-RUNBOOK-49-045`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Determine if a precedent interpreting a statutory provision is operative on a specific transaction date or superseded by an amendment.

### 2. Operational Procedure
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()
res = engine.resolve_amendment_impact_on_precedent(
    "CASE-VULCAN", "IND-STAT-ICA-1872", "Section 28", "2005-09-15"
)
print("Applicable:", res["is_applicable"])
print("Status:", res["status"])
print("Rationale:", res["rationale"])
```

### 3. Expected Output
`is_applicable: False` | Status: `SUPERSEDED_BY_LEGISLATIVE_AMENDMENT` | Rationale: Act 1 of 1997 inserted Section 28(b).
