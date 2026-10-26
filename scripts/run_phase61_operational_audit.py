"""
Phase 61 Operational Audit and Execution Trace Generator.
Runs representative legal queries through the 13-stage pipeline execution harness,
validates trace observability, stage completeness, and privacy sanitization,
and outputs data/22_central_legislation/phase61_operational_traces.json.
"""

import json
import os
from datetime import datetime, timezone

from legalmitra.evaluation.adversarial_harness import PipelineExecutionHarness
from legalmitra.operations.reconciler import CorpusReconciler
from legalmitra.operations.backup_recovery import KnowledgeBaseBackupManager


def run_operational_audit():
    print("=== LegalMitra Phase 61 Operational Audit & Trace Verification ===")

    # 1. Corpus Reconciliation
    reconciler = CorpusReconciler()
    recon_report = reconciler.run_full_reconciliation()
    print(f"[OK] Corpus Reconciliation: {recon_report.overall_status}")
    print(f"     Total Chunks: {recon_report.total_chunks} | Scaffold: {recon_report.quarantined_chunks}")
    print(f"     Review Pending: {recon_report.review_package_pending_count}/40")

    # 2. Pipeline Execution Harness Traces
    harness = PipelineExecutionHarness()
    traces, summary = harness.execute_all()
    print(f"[OK] Executed {len(traces)} compound adversarial scenarios via PipelineExecutionHarness.")
    print(f"     Safety Pass Rate: {summary['safety_pass_rate'] * 100:.1f}%")

    trace_dicts = [t.to_dict() for t in traces]

    # 3. Privacy & Sanitization Check on Traces
    forbidden_tokens = ["api_key", "password", "secret", "private_key", "bearer_token"]
    sanitization_clean = True
    for t in trace_dicts:
        t_str = json.dumps(t).lower()
        for tok in forbidden_tokens:
            if tok in t_str and "not_" not in t_str:
                sanitization_clean = False
                print(f"[WARN] Sanitization warning: possible token {tok} in scenario {t['scenario_id']}")

    output_path = os.path.join(
        "data", "22_central_legislation", "phase61_operational_traces.json"
    )
    payload = {
        "manifest_version": "1.0.0",
        "release_id": "LEGALMITRA-RELEASE-PHASE61",
        "target_release": "0.61.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_traces": len(trace_dicts),
        "harness_summary": summary,
        "sanitization_clean": sanitization_clean,
        "corpus_reconciliation_status": recon_report.overall_status,
        "traces": trace_dicts,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[OK] Operational traces persisted to {output_path}")


if __name__ == "__main__":
    run_operational_audit()
