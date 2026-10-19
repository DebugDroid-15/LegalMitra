# LEGALMITRA — PHASE 49 RUNBOOK 44
## Operational Runbook: Precedent Conflict & Status Evaluation

**Runbook ID:** `LM-RUNBOOK-49-044`  
**Author:** Shatrujeet Legal Engineering Team  

### 1. Purpose
Evaluate the comprehensive precedential status of a case, distinguishing active law, partial overruling, stays, referrals, and legislative supersession.

### 2. Operational Procedure
```python
from legalmitra.caselaw.knowledge_graph import build_national_judicial_knowledge_graph

graph = build_national_judicial_knowledge_graph()
status = graph.evaluate_precedent_status("CASE-SC-VODAFONE-2012")
print("Status:", status["status"])
print("Good Law:", status["is_good_law"])
print("Superseded by Legislation:", status["superseded_by_legislation"])
```

### 3. Expected Output
Status: `statutory_basis_superseded` | Details show Finance Act 2012 retrospective amendments.
