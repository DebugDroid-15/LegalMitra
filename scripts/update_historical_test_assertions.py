"""
Update historical test assertions across tests/test_phase51_*.py through test_phase55_*.py
to support Version 12.0.0, 212 test cases, 84 held-out cases, and Release 0.56.0.
"""

from pathlib import Path

# 1. Update test_phase51_evaluation_framework.py
p51 = Path("tests/test_phase51_evaluation_framework.py")
content = p51.read_text(encoding="utf-8")
content = content.replace(
    'assert data.get("version") in ("7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0")',
    'assert data.get("version") in ("7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0", "12.0.0")'
)
content = content.replace(
    'assert len(test_cases) in (100, 120, 140, 164, 188), f"Expected 100, 120, 140, or 164 test cases, found {len(test_cases)}"',
    'assert len(test_cases) in (100, 120, 140, 164, 188, 212), f"Expected 100, 120, 140, 164, 188, or 212 test cases, found {len(test_cases)}"'
)
content = content.replace(
    'assert split_counts["development"] in (50, 60, 70, 78)',
    'assert split_counts["development"] in (50, 60, 70, 78, 88)'
)
content = content.replace(
    'assert split_counts["validation"] in (20, 25, 30, 35)',
    'assert split_counts["validation"] in (20, 25, 30, 35, 40)'
)
content = content.replace(
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75)',
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84)'
)
content = content.replace(
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75)',
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75, 84)'
)
content = content.replace(
    'assert len(held_out) in (30, 50, 55, 64, 75)',
    'assert len(held_out) in (30, 50, 55, 64, 75, 84)'
)
content = content.replace(
    'assert summary.total_gates == 11',
    'assert summary.total_gates in (11, 15)'
)
content = content.replace(
    'assert summary.passed_gates == 10',
    'assert summary.passed_gates in (10, 14)'
)
content = content.replace(
    'assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0")',
    'assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0")'
)
p51.write_text(content, encoding="utf-8")
print("Updated test_phase51_evaluation_framework.py")

# 2. Update test_phase52_source_integrity.py
p52 = Path("tests/test_phase52_source_integrity.py")
content = p52.read_text(encoding="utf-8")
content = content.replace(
    'assert data["total_test_cases"] in (120, 140, 164, 188)',
    'assert data["total_test_cases"] in (120, 140, 164, 188, 212)'
)
content = content.replace(
    'assert summary.target_version in ("0.52.0", "0.53.0", "0.54.0", "0.55.0")',
    'assert summary.target_version in ("0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0")'
)
content = content.replace(
    'assert summary.total_gates == 11',
    'assert summary.total_gates in (11, 15)'
)
content = content.replace(
    'assert summary.passed_gates == 10',
    'assert summary.passed_gates in (10, 14)'
)
content = content.replace(
    'assert rg10.evidence["held_out_case_count"] in (50, 55, 64, 75)',
    'assert rg10.evidence["held_out_case_count"] in (50, 55, 64, 75, 84)'
)
p52.write_text(content, encoding="utf-8")
print("Updated test_phase52_source_integrity.py")

# 3. Update test_phase53_evidence_reliability.py
p53 = Path("tests/test_phase53_evidence_reliability.py")
content = p53.read_text(encoding="utf-8")
content = content.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")'
)
content = content.replace(
    'assert data["version"] in ("9.0.0", "10.0.0", "11.0.0")',
    'assert data["version"] in ("9.0.0", "10.0.0", "11.0.0", "12.0.0")'
)
content = content.replace(
    'assert data["total_test_cases"] in (140, 164, 188)',
    'assert data["total_test_cases"] in (140, 164, 188, 212)'
)
content = content.replace(
    'assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75)',
    'assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75, 84)'
)
content = content.replace(
    'assert summary.target_version in ("0.53.0", "0.54.0", "0.55.0")',
    'assert summary.target_version in ("0.53.0", "0.54.0", "0.55.0", "0.56.0")'
)
content = content.replace(
    'assert summary.total_gates == 11',
    'assert summary.total_gates in (11, 15)'
)
content = content.replace(
    'assert summary.passed_gates == 10',
    'assert summary.passed_gates in (10, 14)'
)
content = content.replace(
    'assert rg10.evidence["held_out_case_count"] in (55, 64, 75)',
    'assert rg10.evidence["held_out_case_count"] in (55, 64, 75, 84)'
)
p53.write_text(content, encoding="utf-8")
print("Updated test_phase53_evidence_reliability.py")

# 4. Update test_phase54_authority_graph.py
p54 = Path("tests/test_phase54_authority_graph.py")
content = p54.read_text(encoding="utf-8")
content = content.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")'
)
content = content.replace(
    'assert data["version"] in ("10.0.0", "11.0.0")',
    'assert data["version"] in ("10.0.0", "11.0.0", "12.0.0")'
)
content = content.replace(
    'assert summary.target_version in ("0.54.0", "0.55.0")',
    'assert summary.target_version in ("0.54.0", "0.55.0", "0.56.0")'
)
content = content.replace(
    'assert summary.total_gates == 11',
    'assert summary.total_gates in (11, 15)'
)
content = content.replace(
    'assert summary.passed_gates == 10',
    'assert summary.passed_gates in (10, 14)'
)
p54.write_text(content, encoding="utf-8")
print("Updated test_phase54_authority_graph.py")

# 5. Update test_phase55_temporal_authority_trace.py
p55 = Path("tests/test_phase55_temporal_authority_trace.py")
content = p55.read_text(encoding="utf-8")
content = content.replace(
    'assert data["benchmark_suite_id"] == "LEGALMITRA-BENCHMARK-PIT-V11"',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12")'
)
content = content.replace(
    'assert data["version"] == "11.0.0"',
    'assert data["version"] in ("11.0.0", "12.0.0")'
)
content = content.replace(
    'assert len(data["test_cases"]) == 188',
    'assert len(data["test_cases"]) in (188, 212)'
)
content = content.replace(
    'assert data["split_counts"]["held_out_evaluation"] == 75',
    'assert data["split_counts"]["held_out_evaluation"] in (75, 84)'
)
content = content.replace(
    'assert summary.target_version == "0.55.0"',
    'assert summary.target_version in ("0.55.0", "0.56.0")'
)
content = content.replace(
    'assert summary.total_gates == 11',
    'assert summary.total_gates in (11, 15)'
)
content = content.replace(
    'assert summary.passed_gates == 10',
    'assert summary.passed_gates in (10, 14)'
)
p55.write_text(content, encoding="utf-8")
print("Updated test_phase55_temporal_authority_trace.py")
