# Phase 57 Operations Runbook & CLI Procedures

**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Release:** `LEGALMITRA-RELEASE-PHASE57`  

---

## 1. Independent Evaluation CLI Procedures

To evaluate an answer independently post-generation:
```python
from legalmitra.evaluation import IndependentClaimEvaluator, AnswerCompletenessAuditor, RootCauseAttributor

# 1. Independent Claim Evaluation
evaluator = IndependentClaimEvaluator()
eval_report = evaluator.evaluate_response(
    query="Can a contractor get an injunction against a national highway project under Section 20A SRA?",
    answer_text="Under Section 20A SRA, no injunction shall be granted for infrastructure projects.",
    citations=["Specific Relief Act, 1963 Section 20A"],
    production_response_state="ANSWER_SUPPORTED"
)
print("Trustworthiness Score:", eval_report.trustworthiness_score)
print("Substantive Support Rate:", eval_report.substantive_support_rate)

# 2. 4D Answer Completeness Audit
auditor = AnswerCompletenessAuditor()
audit_report = auditor.audit(
    query="Does a daughter inherit coparcenary property if partition was registered in 2003?",
    answer_text="Under Section 6(1) proviso, partitions registered before 20 Dec 2004 are saved.",
    citations=["Hindu Succession Act Section 6(1) Proviso"],
    response_state="ANSWER_QUALIFIED"
)
print("Completeness Score:", audit_report.overall_completeness_score)
print("Calibration Verdict:", audit_report.calibration_verdict.value)
```

---

## 2. Release Gate Assessment Execution

To evaluate all 20 release quality gates:
```bash
python -c "from legalmitra.evaluation.release_gates import ReleaseGateEvaluator; rge = ReleaseGateEvaluator(); summary = rge.evaluate_all_gates(); print(f'Passed: {summary.passed_gates}/{summary.total_gates}'); rge.generate_manifest()"
```
