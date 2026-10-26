"""
Updates release_gates.py and historical test assertions for Phase 61.
"""

import glob
import re

def update_release_gates():
    rg_path = "legalmitra/evaluation/release_gates.py"
    with open(rg_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace('"LEGALMITRA-RELEASE-PHASE60"', '"LEGALMITRA-RELEASE-PHASE61"')
    content = content.replace('"0.60.0"', '"0.61.0"')

    with open(rg_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated {rg_path}")

def update_historical_tests():
    # Update test_phase52 through test_phase59 to include PHASE61 in the allowed tuple
    pattern = r'assert summary\.release_id in \(("LEGALMITRA-RELEASE-PHASE51"[^)]+)\)'
    for tf in glob.glob("tests/test_phase5*.py"):
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "LEGALMITRA-RELEASE-PHASE60" in content and "LEGALMITRA-RELEASE-PHASE61" not in content:
            content = content.replace(
                '"LEGALMITRA-RELEASE-PHASE60"',
                '"LEGALMITRA-RELEASE-PHASE60", "LEGALMITRA-RELEASE-PHASE61"'
            )
        if '"0.60.0"' in content and '"0.61.0"' not in content:
            content = content.replace(
                '"0.60.0"',
                '"0.60.0", "0.61.0"'
            )
        with open(tf, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Updated historical assertion in {tf}")

    # Update test_phase60_adversarial_validation.py
    p60_test = "tests/test_phase60_adversarial_validation.py"
    with open(p60_test, "r", encoding="utf-8") as f:
        content = f.read()
    if 'assert summary.release_id == "LEGALMITRA-RELEASE-PHASE60"' in content:
        content = content.replace(
            'assert summary.release_id == "LEGALMITRA-RELEASE-PHASE60"',
            'assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE60", "LEGALMITRA-RELEASE-PHASE61")'
        )
    if 'assert summary.target_version == "0.60.0"' in content:
        content = content.replace(
            'assert summary.target_version == "0.60.0"',
            'assert summary.target_version in ("0.60.0", "0.61.0")'
        )
    with open(p60_test, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated release assertion in {p60_test}")

def generate_release_manifest():
    from legalmitra.evaluation.release_gates import ReleaseGateEvaluator
    import json
    evaluator = ReleaseGateEvaluator()
    summary = evaluator.evaluate_all_gates()
    out_path = "data/22_central_legislation/release_gates_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary.to_dict(), f, indent=2)
    print(f"[OK] Generated {out_path} (release_id: {summary.release_id}, decision: {summary.overall_decision})")

if __name__ == "__main__":
    update_release_gates()
    update_historical_tests()
    generate_release_manifest()
