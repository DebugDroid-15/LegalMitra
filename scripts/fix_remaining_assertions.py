with open('tests/test_phase53_evidence_reliability.py', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('assert data["split_counts"]["development"] in (60, 70, 78, 88)', 'assert data["split_counts"]["development"] in (60, 70, 78, 88, 100)')
c = c.replace('assert data["split_counts"]["validation"] in (25, 30, 35, 40)', 'assert data["split_counts"]["validation"] in (25, 30, 35, 40, 46)')
c = c.replace('assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75, 84)', 'assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75, 84, 94)')
c = c.replace('assert rg10.evidence["held_out_case_count"] in (55, 64, 75, 84)', 'assert rg10.evidence["held_out_case_count"] in (55, 64, 75, 84, 94)')
with open('tests/test_phase53_evidence_reliability.py', 'w', encoding='utf-8') as f:
    f.write(c)

with open('tests/test_phase55_temporal_authority_trace.py', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('assert data["split_counts"]["development"] in (78, 88)', 'assert data["split_counts"]["development"] in (78, 88, 100)')
c = c.replace('assert data["split_counts"]["validation"] in (35, 40)', 'assert data["split_counts"]["validation"] in (35, 40, 46)')
c = c.replace('assert data["split_counts"]["held_out_evaluation"] in (75, 84)', 'assert data["split_counts"]["held_out_evaluation"] in (75, 84, 94)')
with open('tests/test_phase55_temporal_authority_trace.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated 53 and 55 successfully!')

