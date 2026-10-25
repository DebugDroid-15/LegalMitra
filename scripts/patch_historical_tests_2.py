from pathlib import Path

# 1. tests/test_phase51_evaluation_framework.py
p51 = Path("tests/test_phase51_evaluation_framework.py")
t51 = p51.read_text(encoding="utf-8")
t51 = t51.replace(
    'assert len(test_cases) in (100, 120, 140, 164)',
    'assert len(test_cases) in (100, 120, 140, 164, 188)'
)
t51 = t51.replace(
    'assert split_counts["development"] in (50, 60, 70)',
    'assert split_counts["development"] in (50, 60, 70, 78)'
)
t51 = t51.replace(
    'assert split_counts["validation"] in (20, 25, 30)',
    'assert split_counts["validation"] in (20, 25, 30, 35)'
)
t51 = t51.replace(
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64)',
    'assert split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75)'
)
t51 = t51.replace(
    'assert report.split_counts["development"] in (50, 60, 70)',
    'assert report.split_counts["development"] in (50, 60, 70, 78)'
)
t51 = t51.replace(
    'assert report.split_counts["validation"] in (20, 25, 30)',
    'assert report.split_counts["validation"] in (20, 25, 30, 35)'
)
t51 = t51.replace(
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64)',
    'assert report.split_counts["held_out_evaluation"] in (30, 50, 55, 64, 75)'
)
p51.write_text(t51, encoding="utf-8")
print("Updated test_phase51_evaluation_framework.py")

# 2. tests/test_phase52_source_integrity.py
p52 = Path("tests/test_phase52_source_integrity.py")
t52 = p52.read_text(encoding="utf-8")
t52 = t52.replace(
    'assert report.total_cases_audited in (120, 140, 164)',
    'assert report.total_cases_audited in (120, 140, 164, 188)'
)
p52.write_text(t52, encoding="utf-8")
print("Updated test_phase52_source_integrity.py")

# 3. tests/test_phase53_evidence_reliability.py
p53 = Path("tests/test_phase53_evidence_reliability.py")
t53 = p53.read_text(encoding="utf-8")
t53 = t53.replace(
    'assert data["version"] in ("9.0.0", "10.0.0")',
    'assert data["version"] in ("9.0.0", "10.0.0", "11.0.0")'
)
t53 = t53.replace(
    'assert data["total_test_cases"] in (140, 164)',
    'assert data["total_test_cases"] in (140, 164, 188)'
)
t53 = t53.replace(
    'assert data["split_counts"]["development"] in (60, 70)',
    'assert data["split_counts"]["development"] in (60, 70, 78)'
)
t53 = t53.replace(
    'assert data["split_counts"]["validation"] in (25, 30)',
    'assert data["split_counts"]["validation"] in (25, 30, 35)'
)
t53 = t53.replace(
    'assert data["split_counts"]["held_out_evaluation"] in (55, 64)',
    'assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75)'
)
p53.write_text(t53, encoding="utf-8")
print("Updated test_phase53_evidence_reliability.py")

