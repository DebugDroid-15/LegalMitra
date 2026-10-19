# LEGALMITRA — PHASE 50
## Operations Runbook 48: Query Orchestration Pipeline Execution

**Document ID:** `LM-RUNBOOK-48-ORCHESTRATION-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  

---

### 1. Purpose

Guide operators on executing and monitoring the 14-step deterministic legal query orchestration pipeline.

### 2. Execution Commands

```python
from legalmitra.orchestration.pipeline import LegalQueryPipeline

pipeline = LegalQueryPipeline()
response = pipeline.execute(
    query="Can a workman claim overtime for 54 weekly hours under the Factories Act?",
    context_date="2024-05-01"
)

print("State:", response.response_state)
print("Answer:", response.answer_text)
print("Governing Provisions:", response.governing_provisions)
```

### 3. Verification

Inspect `response.telemetry` for execution timings across each phase.
