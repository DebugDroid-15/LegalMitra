"""
Comprehensive updater for historical test assertions across Phases 51-55 for Phase 57.
"""

# Phase 51
p51 = "tests/test_phase51_evaluation_framework.py"
with open(p51, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert split_counts["development"] in (50, 60, 70, 78, 88)',
    'assert split_counts["development"] in (50, 60, 70, 78, 88, 100)'
)
c = c.replace(
    'assert split_counts["validation"] in (20, 25, 30, 35, 40)',
    'assert split_counts["validation"] in (20, 25, 30, 35, 40, 46)'
)
c = c.replace(
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84)',
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84, 94)'
)
c = c.replace(
    'assert report.split_counts["development"] in (50, 60, 70, 78, 88)',
    'assert report.split_counts["development"] in (50, 60, 70, 78, 88, 100)'
)
c = c.replace(
    'assert report.split_counts["validation"] in (20, 25, 30, 35, 40)',
    'assert report.split_counts["validation"] in (20, 25, 30, 35, 40, 46)'
)
c = c.replace(
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84)',
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84, 94)'
)
c = c.replace(
    'assert len(held_out) in (30, 50, 55, 64, 75, 84)',
    'assert len(held_out) in (30, 50, 55, 64, 75, 84, 94)'
)
c = c.replace(
    'assert summary.total_gates in (11, 15)',
    'assert summary.total_gates in (11, 15, 20)'
)
c = c.replace(
    'assert summary.passed_gates in (10, 14)',
    'assert summary.passed_gates in (10, 14, 19)'
)
c = c.replace(
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56")',
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    'assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0")',
    'assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0")'
)
with open(p51, "w", encoding="utf-8") as f:
    f.write(c)

# Phase 52
p52 = "tests/test_phase52_source_integrity.py"
with open(p52, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert summary.total_gates in (11, 15)',
    'assert summary.total_gates in (11, 15, 20)'
)
c = c.replace(
    'assert summary.passed_gates in (10, 14)',
    'assert summary.passed_gates in (10, 14, 19)'
)
with open(p52, "w", encoding="utf-8") as f:
    f.write(c)

# Phase 53
p53 = "tests/test_phase53_evidence_reliability.py"
with open(p53, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13")'
)
c = c.replace(
    'assert summary.total_gates in (11, 15)',
    'assert summary.total_gates in (11, 15, 20)'
)
c = c.replace(
    'assert summary.passed_gates in (10, 14)',
    'assert summary.passed_gates in (10, 14, 19)'
)
with open(p53, "w", encoding="utf-8") as f:
    f.write(c)

# Phase 54
p54 = "tests/test_phase54_authority_graph.py"
with open(p54, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13")'
)
c = c.replace(
    'assert summary.total_gates in (11, 15)',
    'assert summary.total_gates in (11, 15, 20)'
)
c = c.replace(
    'assert summary.passed_gates in (10, 14)',
    'assert summary.passed_gates in (10, 14, 19)'
)
with open(p54, "w", encoding="utf-8") as f:
    f.write(c)

# Phase 55
p55 = "tests/test_phase55_temporal_authority_trace.py"
with open(p55, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13")'
)
c = c.replace(
    'assert summary.total_gates in (11, 15)',
    'assert summary.total_gates in (11, 15, 20)'
)
c = c.replace(
    'assert summary.passed_gates in (10, 14)',
    'assert summary.passed_gates in (10, 14, 19)'
)
with open(p55, "w", encoding="utf-8") as f:
    f.write(c)

print("Historical assertions in Phase 51-55 updated successfully!")
