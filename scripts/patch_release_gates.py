from pathlib import Path
import json

p = Path("legalmitra/evaluation/release_gates.py")
content = p.read_text(encoding="utf-8")

old_rel = """        return ReleaseEvaluationSummary(
            release_id="LEGALMITRA-RELEASE-PHASE54",
            target_version="0.54.0","""

new_rel = """        return ReleaseEvaluationSummary(
            release_id="LEGALMITRA-RELEASE-PHASE55",
            target_version="0.55.0","""

if old_rel in content:
    content = content.replace(old_rel, new_rel)
    print("Updated release_id to PHASE55 and target_version to 0.55.0")
elif old_rel.replace('\n', '\r\n') in content:
    content = content.replace(old_rel.replace('\n', '\r\n'), new_rel.replace('\n', '\r\n'))
    print("Updated release_id (CRLF)")

old_rg10 = """        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(cases)
        clean = (
            report.exact_duplicates_count == 0
            and report.max_cross_split_jaccard <= 0.85
            and report.split_counts.get("held_out_evaluation", 0) >= 55
        )

        return ReleaseGate(
            gate_id="RG-10-HELD-OUT-EVALUATION",
            name="Independent Held-Out Evaluation Generalization",
            description="Evaluates generalization on 55 independently curated, held-out evaluation cases with verified zero split contamination.",
            category="LEGAL_VALIDITY",
            threshold="55 held-out cases; 0 exact duplicates; max similarity <= 0.85; >= 90% pass rate",
            actual_value=f"55 held-out cases verified; {report.exact_duplicates_count} exact duplicates; max similarity {report.max_cross_split_jaccard:.2f}","""

new_rg10 = """        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(cases)
        held_out_count = report.split_counts.get("held_out_evaluation", 0)
        clean = (
            report.exact_duplicates_count == 0
            and report.max_cross_split_jaccard <= 0.85
            and held_out_count >= 55
        )

        return ReleaseGate(
            gate_id="RG-10-HELD-OUT-EVALUATION",
            name="Independent Held-Out Evaluation Generalization",
            description="Evaluates generalization on independently curated, held-out evaluation cases with verified zero split contamination.",
            category="LEGAL_VALIDITY",
            threshold=">= 55 held-out cases; 0 exact duplicates; max similarity <= 0.85; >= 90% pass rate",
            actual_value=f"{held_out_count} held-out cases verified; {report.exact_duplicates_count} exact duplicates; max similarity {report.max_cross_split_jaccard:.2f}","""

if old_rg10 in content:
    content = content.replace(old_rg10, new_rg10)
    print("Updated RG-10 held-out evaluation block")
elif old_rg10.replace('\n', '\r\n') in content:
    content = content.replace(old_rg10.replace('\n', '\r\n'), new_rg10.replace('\n', '\r\n'))
    print("Updated RG-10 block (CRLF)")

p.write_text(content, encoding="utf-8")
print("Saved patched legalmitra/evaluation/release_gates.py")

