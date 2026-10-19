# LEGALMITRA — PHASE 50
## Operations Runbook 49: Fact-Sensitive Analysis & IRAC Generation

**Document ID:** `LM-RUNBOOK-49-FACT-ANALYSIS-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  

---

### 1. Purpose

Runbook for inspecting epistemic fact classifications and structured IRAC units.

### 2. Inspection Workflow

```python
from legalmitra.orchestration.query_understanding import LegalQueryAnalyzer
from legalmitra.orchestration.evidence_orchestrator import UnifiedEvidenceOrchestrator
from legalmitra.orchestration.fact_analyzer import FactSensitiveAnalyzer

analyzer = LegalQueryAnalyzer()
parsed = analyzer.parse_query("Tenant claims rent is INR 15,000 in Delhi under DRC Act.")
orchestrator = UnifiedEvidenceOrchestrator()
evidence = orchestrator.orchestrate_evidence(parsed)
fact_report = FactSensitiveAnalyzer().analyze(parsed, evidence)

for unit in fact_report.irac_units:
    print("Issue:", unit.issue)
    print("Rule:", unit.rule)
    print("Application:", unit.application)
    print("Conclusion:", unit.conclusion)
```
