# LEGALMITRA PHASE 60 — NEGATIVE CONTROL RESULTS

**Project:** LegalMitra  
**Phase Identifier:** `LEGALMITRA-PHASE60`  
**Execution Date:** 2026-10-25  

---

## 1. 14 Fail-Closed Negative Controls Summary

| Control ID | Condition Tested | Injected Fault | Expected Gate Outcome | Result |
|:---|:---|:---|:---:|:---:|
| **NC-01** | Review Freeze Mismatch | Modified SHA-256 in freeze file | RG-09 FAILED | **PASS** |
| **NC-02** | Missing Corpus Database | Invalid path to `legalmitra_kb.db` | RG-01 FAILED | **PASS** |
| **NC-03** | Fabricated Citation | Mocked citation returning False | RG-06 FAILED | **PASS** |
| **NC-04** | Unindexed Authority | Nonexistent reporter volume | Citation labeled UNINDEXED/FABRICATED | **PASS** |
| **NC-05** | Unsupported Proposition | Enforces grounding threshold >= 85% | RG-04 Enforced | **PASS** |
| **NC-06** | Unresolved Temporal Applicability | Boundary date shift | RG-02 Enforced | **PASS** |
| **NC-07** | Precedent Conflict | Bench strength reversal | RG-03 Enforced | **PASS** |
| **NC-08** | Missing Statutory Exception | Omission of Section 20A SRA bar | RG-13 Enforced | **PASS** |
| **NC-09** | Broken Premise Dependency | Unregistered TPA 53A agreement | RG-14 Enforced | **PASS** |
| **NC-10** | Scaffold Inclusion | Query citing `IND-JUD-DEL-2024-BAIL` | RG-01/08 FAILED | **PASS** |
| **NC-11** | Conversation DB Leak | Shared DB path between KB and sessions | RG-08 FAILED | **PASS** |
| **NC-12** | Hidden Regression | Candidate case with safety violation | RG-20 FAILED | **PASS** |
| **NC-13** | Missing Legal Review | Unsigned advocate review register | RG-11 PENDING | **PASS** |
| **NC-14** | Stale Benchmark Manifest | Missing manifest JSON file | RG-19 FAILED | **PASS** |

All 14 negative controls verified fail-closed behavior under isolated test conditions.
