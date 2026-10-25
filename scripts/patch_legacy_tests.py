from pathlib import Path

# 1. tests/test_phase52_source_integrity.py
p52 = Path("tests/test_phase52_source_integrity.py")
t52 = p52.read_text(encoding="utf-8")
t52 = t52.replace(
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54")',
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55")'
)
t52 = t52.replace(
    'assert rg10.evidence["held_out_case_count"] in (50, 55, 64)',
    'assert rg10.evidence["held_out_case_count"] in (50, 55, 64, 75)'
)
p52.write_text(t52, encoding="utf-8")
print("Updated test_phase52_source_integrity.py")

# 2. tests/test_phase53_evidence_reliability.py
p53 = Path("tests/test_phase53_evidence_reliability.py")
t53 = p53.read_text(encoding="utf-8")
t53 = t53.replace(
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54")',
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55")'
)
t53 = t53.replace(
    'assert rg10.evidence["held_out_case_count"] in (55, 64)',
    'assert rg10.evidence["held_out_case_count"] in (55, 64, 75)'
)
p53.write_text(t53, encoding="utf-8")
print("Updated test_phase53_evidence_reliability.py")

# 3. tests/test_phase54_authority_graph.py
p54 = Path("tests/test_phase54_authority_graph.py")
t54 = p54.read_text(encoding="utf-8")
t54 = t54.replace(
    'assert data["benchmark_suite_id"] == "LEGALMITRA-BENCHMARK-PIT-V10"',
    'assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11")'
)
t54 = t54.replace(
    'assert data["version"] == "10.0.0"',
    'assert data["version"] in ("10.0.0", "11.0.0")'
)
t54 = t54.replace(
    'assert summary.release_id == "LEGALMITRA-RELEASE-PHASE54"',
    'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55")'
)
t54 = t54.replace(
    'assert summary.target_version == "0.54.0"',
    'assert summary.target_version in ("0.54.0", "0.55.0")'
)
p54.write_text(t54, encoding="utf-8")
print("Updated test_phase54_authority_graph.py")

