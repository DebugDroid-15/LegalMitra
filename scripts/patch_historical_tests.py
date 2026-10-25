from pathlib import Path

# 1. tests/test_phase51_evaluation_framework.py
p51 = Path("tests/test_phase51_evaluation_framework.py")
t51 = p51.read_text(encoding="utf-8")
t51 = t51.replace(
    'assert data.get("version") in ("7.0.0", "8.0.0", "9.0.0", "10.0.0")',
    'assert data.get("version") in ("7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0")'
)
t51 = t51.replace(
    'assert report.total_cases_audited in (100, 120, 140, 164)',
    'assert report.total_cases_audited in (100, 120, 140, 164, 188)'
)
t51 = t51.replace(
    'assert len(held_out) in (30, 50, 55, 64)',
    'assert len(held_out) in (30, 50, 55, 64, 75)'
)
p51.write_text(t51, encoding="utf-8")
print("Updated test_phase51_evaluation_framework.py")

# 2. tests/test_phase52_source_integrity.py
p52 = Path("tests/test_phase52_source_integrity.py")
t52 = p52.read_text(encoding="utf-8")
t52 = t52.replace(
    'assert data["total_test_cases"] in (120, 140, 164)',
    'assert data["total_test_cases"] in (120, 140, 164, 188)'
)
t52 = t52.replace(
    'assert summary.target_version in ("0.52.0", "0.53.0", "0.54.0")',
    'assert summary.target_version in ("0.52.0", "0.53.0", "0.54.0", "0.55.0")'
)
p52.write_text(t52, encoding="utf-8")
print("Updated test_phase52_source_integrity.py")

# 3. tests/test_phase53_evidence_reliability.py
p53 = Path("tests/test_phase53_evidence_reliability.py")
t53 = p53.read_text(encoding="utf-8")
t53 = t53.replace(
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10")',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11")'
)
t53 = t53.replace(
    'assert summary.target_version in ("0.53.0", "0.54.0")',
    'assert summary.target_version in ("0.53.0", "0.54.0", "0.55.0")'
)
p53.write_text(t53, encoding="utf-8")
print("Updated test_phase53_evidence_reliability.py")

