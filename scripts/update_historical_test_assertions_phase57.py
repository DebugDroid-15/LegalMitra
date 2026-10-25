"""
Update historical test assertions for Phase 57.
Accommodates 240 cases, version 13.0.0, release LEGALMITRA-RELEASE-PHASE57, and version 0.57.0.
"""

# 1. Update test_phase51_evaluation_framework.py
p51 = "tests/test_phase51_evaluation_framework.py"
with open(p51, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '("7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0", "12.0.0")',
    '("7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0", "12.0.0", "13.0.0")'
)
c = c.replace(
    '(100, 120, 140, 164, 188, 212)',
    '(100, 120, 140, 164, 188, 212, 240)'
)
c = c.replace(
    '100, 120, 140, 164, 188, or 212 test cases',
    '100, 120, 140, 164, 188, 212, or 240 test cases'
)
with open(p51, "w", encoding="utf-8") as f:
    f.write(c)

# 2. Update test_phase52_source_integrity.py
p52 = "tests/test_phase52_source_integrity.py"
with open(p52, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '(120, 140, 164, 188, 212)',
    '(120, 140, 164, 188, 212, 240)'
)
c = c.replace(
    '("LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56")',
    '("LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    '("0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0")',
    '("0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0")'
)
with open(p52, "w", encoding="utf-8") as f:
    f.write(c)

# 3. Update test_phase53_evidence_reliability.py
p53 = "tests/test_phase53_evidence_reliability.py"
with open(p53, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '("9.0.0", "10.0.0", "11.0.0", "12.0.0")',
    '("9.0.0", "10.0.0", "11.0.0", "12.0.0", "13.0.0")'
)
c = c.replace(
    '(140, 164, 188, 212)',
    '(140, 164, 188, 212, 240)'
)
c = c.replace(
    '("LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56")',
    '("LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    '("0.53.0", "0.54.0", "0.55.0", "0.56.0")',
    '("0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0")'
)
with open(p53, "w", encoding="utf-8") as f:
    f.write(c)

# 4. Update test_phase54_authority_graph.py
p54 = "tests/test_phase54_authority_graph.py"
with open(p54, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '("10.0.0", "11.0.0", "12.0.0")',
    '("10.0.0", "11.0.0", "12.0.0", "13.0.0")'
)
c = c.replace(
    '("LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56")',
    '("LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    '("0.54.0", "0.55.0", "0.56.0")',
    '("0.54.0", "0.55.0", "0.56.0", "0.57.0")'
)
with open(p54, "w", encoding="utf-8") as f:
    f.write(c)

# 5. Update test_phase55_temporal_authority_trace.py
p55 = "tests/test_phase55_temporal_authority_trace.py"
with open(p55, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '("11.0.0", "12.0.0")',
    '("11.0.0", "12.0.0", "13.0.0")'
)
c = c.replace(
    '(188, 212)',
    '(188, 212, 240)'
)
c = c.replace(
    '("LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56")',
    '("LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    '("0.55.0", "0.56.0")',
    '("0.55.0", "0.56.0", "0.57.0")'
)
with open(p55, "w", encoding="utf-8") as f:
    f.write(c)

# 6. Update test_phase56_multi_authority_synthesis.py
p56 = "tests/test_phase56_multi_authority_synthesis.py"
with open(p56, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    'assert data["benchmark_suite_id"] == "LEGALMITRA-BENCHMARK-PIT-V12"',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13")'
)
c = c.replace(
    'assert data["version"] == "12.0.0"',
    'assert data["version"] in ("12.0.0", "13.0.0")'
)
c = c.replace(
    'assert len(data["test_cases"]) == 212',
    'assert len(data["test_cases"]) in (212, 240)'
)
c = c.replace(
    'assert data["split_counts"]["development"] == 88',
    'assert data["split_counts"]["development"] in (88, 100)'
)
c = c.replace(
    'assert data["split_counts"]["validation"] == 40',
    'assert data["split_counts"]["validation"] in (40, 46)'
)
c = c.replace(
    'assert data["split_counts"]["held_out_evaluation"] == 84',
    'assert data["split_counts"]["held_out_evaluation"] in (84, 94)'
)
c = c.replace(
    'assert summary.release_id == "LEGALMITRA-RELEASE-PHASE56"',
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57")'
)
c = c.replace(
    'assert summary.target_version == "0.56.0"',
    'assert summary.target_version in ("0.56.0", "0.57.0")'
)
c = c.replace(
    'assert summary.total_gates == 15',
    'assert summary.total_gates in (15, 20)'
)
c = c.replace(
    'assert summary.passed_gates == 14',
    'assert summary.passed_gates in (14, 19)'
)
with open(p56, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated historical test assertions successfully!")

