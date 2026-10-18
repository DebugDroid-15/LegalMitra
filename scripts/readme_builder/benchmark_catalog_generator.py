"""
Benchmark Catalog Generator for LegalMitra README Part XV.
Loads all 96 evaluation cases from data/20_evaluation/evaluation_cases_v9.json and outputs an exhaustive reference catalog.
"""

import json
from pathlib import Path

def generate_benchmark_catalog_markdown() -> str:
    path = Path("data/20_evaluation/evaluation_cases_v9.json")
    if not path.exists():
        return "\n<!-- evaluation_cases_v9.json not found -->\n"
    
    with open(path, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    lines = [
        "### 15.6 Complete Benchmark v9 Case Catalog (All 96 Evaluation Cases)\n",
        "The following catalog provides the complete specification for all 96 test cases in the authoritative LegalMitra Benchmark v9 suite. Each case represents an adversarial or real-world legal challenge evaluated under strict metric contracts:\n"
    ]
    
    for idx, c in enumerate(cases, 1):
        eid = c.get("eval_id", f"V9-{idx:03d}")
        cat = c.get("category", "general")
        q = c.get("question", "").strip()
        etype = c.get("expected_type", "affirmative_statute")
        target_act = c.get("target_act_or_case", "Universal Legal Corpus")
        sections = ", ".join(c.get("target_sections_or_paras", [])) or "General Principles"
        golden = ", ".join(f"`{g}`" for g in c.get("golden_citations", [])) or "None specified"
        forbidden = ", ".join(f"`{f}`" for f in c.get("forbidden_terms", [])) or "None"
        abstain = "Yes (Must Abstain)" if c.get("should_abstain") else "No (Affirmative Grounding Required)"
        rationale = c.get("rationale", "Primary legal grounding.")
        
        lines.append(f"#### Case {idx:02d}: `{eid}` — [{cat.upper()}]")
        lines.append(f"- **Evaluated Question**: \"{q}\"")
        lines.append(f"- **Target Legal Authority**: {target_act}")
        lines.append(f"- **Target Provisions / Paras**: {sections}")
        lines.append(f"- **Expected Response Type**: `{etype}` | **Abstention Required**: {abstain}")
        lines.append(f"- **Golden Citations Required**: {golden}")
        lines.append(f"- **Forbidden Terms**: {forbidden}")
        lines.append(f"- **Jurisprudential Rationale**: {rationale}")
        lines.append("")
    
    return "\n".join(lines)
