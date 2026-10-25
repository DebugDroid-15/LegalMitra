"""
Inspect all 20 release gates in release_gates.py to analyze evidence sources, predicates, and potential bypasses.
"""

from legalmitra.evaluation.release_gates import ReleaseGateEvaluator, GateStatus

rge = ReleaseGateEvaluator()
summary = rge.evaluate_all_gates()

print(f"Total gates: {summary.total_gates}, Passed: {summary.passed_gates}, Failed: {summary.failed_gates}, Pending: {summary.pending_gates}")
print(f"Overall Decision: {summary.overall_decision}")
print("-" * 80)

for g in summary.gates:
    print(f"[{g.gate_id}] {g.name}")
    print(f"  Category: {g.category} | Status: {g.status.value}")
    print(f"  Threshold: {g.threshold}")
    print(f"  Actual: {g.actual_value}")
    print(f"  Evidence Keys: {list(g.evidence.keys())}")
    print("-" * 80)
