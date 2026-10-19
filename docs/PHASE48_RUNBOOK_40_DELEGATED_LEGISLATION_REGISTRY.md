# LEGALMITRA — PHASE 48 RUNBOOK 40
## Operational Runbook: Delegated Legislation Registry Query

**Runbook ID:** `LM-RUNBOOK-48-040`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Retrieve Central Delegated Rules made under specific Central Acts and enabling sections.

### 2. Operational Procedure
```python
from legalmitra.temporal.engine import build_default_temporal_engine

engine = build_default_temporal_engine()
rules = engine.resolve_delegated_rule_for_statute("IND-STAT-COPYRIGHT-1957", section="78")
for r in rules:
    print(f"Instrument: {r['official_title']} | Gazette: {r['gazette_notification_number']} | Commenced: {r['commencement_date']}")
```

### 3. Expected Output
Returns Copyright Rules, 2013 (G.S.R. 172(E)) w.e.f. 14 March 2013.
