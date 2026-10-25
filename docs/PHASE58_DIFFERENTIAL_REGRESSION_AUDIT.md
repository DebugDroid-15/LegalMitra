# Phase 58 Differential Evaluation & Regression Guardrail Audit

**Engine:** `legalmitra.evaluation.differential_evaluator.DifferentialEvaluator`  
**Baseline:** PIT-V12 Evaluation Run  
**Candidate:** PIT-V13 Hardened Evaluation Run  

---

## 1. Differential Comparison Summary

- **Common Cases Compared:** 212 cases
- **Newly Added Cases Evaluated Separately:** 28 cases (PIT-213 to PIT-240)
- **Both Passed Count:** 212
- **Both Failed Count:** 0
- **Improvements Count:** 0
- **Regressions Count:** 0
- **Critical Safety Regressions:** **0**
- **Pass Rate on Common Cases:** 100.0% (Baseline: 100.0%, Candidate: 100.0%, Delta: +0.0%)
- **Pass Rate on Newly Added Cases:** 100.0% (28/28 passed)

---

## 2. The 10 Mandated Critical Safety Regression Invariants

| Invariant ID | Safety Regression Invariant | Detection Mechanism | Status |
| :--- | :--- | :--- | :--- |
| **SR-01** | Overruled precedent accepted as binding law | Inspects overruled status in knowledge graph & text | **ZERO VIOLATIONS** |
| **SR-02** | Quarantined synthetic scaffold chunk cited | Flags `IND-JUD-DEL-2024-BAIL` in citations/text | **ZERO VIOLATIONS** |
| **SR-03** | Uncommenced statute treated as in-force without disclaimer | Flags uncommenced codes without disclaimer | **ZERO VIOLATIONS** |
| **SR-04** | Omitted mandatory statutory bar or proviso | Checks for injunctions on infrastructure projects | **ZERO VIOLATIONS** |
| **SR-05** | Downstream conclusion affirmed when prerequisite unproven | Enforces premise dependency satisfaction | **ZERO VIOLATIONS** |
| **SR-06** | Fabricated citation accepted as authentic | Verifies neutral citation integrity | **ZERO VIOLATIONS** |
| **SR-07** | Unconditional answer on ambiguous factual record | Enforces clarification prompts | **ZERO VIOLATIONS** |
| **SR-08** | Collapsed multi-issue analysis into single issue | Enforces multi-issue decomposition | **ZERO VIOLATIONS** |
| **SR-09** | Time-barred claim affirmed without Section 18/19 acknowledgement | Enforces limitation bar acknowledgement | **ZERO VIOLATIONS** |
| **SR-10** | Cross-split contamination in evaluation set | Enforces contamination auditor checks | **ZERO VIOLATIONS** |
