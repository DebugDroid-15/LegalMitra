# LEGALMITRA — PHASE 48 RUNBOOK 39
## Operational Runbook: Constitution Bench Jurisprudence Lookup

**Runbook ID:** `LM-RUNBOOK-48-039`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Query Supreme Court Constitution Bench landmark decisions linked to constitutional articles.

### 2. Operational Procedure
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()
precedents = engine.resolve_constitution_bench_precedent("Article 368")
for p in precedents:
    print(f"Case: {p['case_title']} | Bench: {p['bench_strength']} Judges | Citation: {p['canonical_citation']}")
```

### 3. Expected Output
Returns Kesavananda Bharati (13 judges) and Minerva Mills (5 judges) with majority breakdown and holding summary.
