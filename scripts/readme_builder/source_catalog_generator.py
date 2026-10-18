"""
Source Catalog Generator for LegalMitra README Part XI.
Loads all 111 sources from unified_source_registry.json and outputs an exhaustive reference catalog.
"""

import json
from pathlib import Path

def generate_source_catalog_markdown() -> str:
    path = Path("data/09_national_corpus/unified_source_registry.json")
    if not path.exists():
        return "\n<!-- unified_source_registry.json not found -->\n"
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    sources = data.get("sources", [])
    
    lines = [
        "### 11.6 Complete National Legal Sources Master Catalog (111 Tracked Sources)\n",
        "The following master reference catalog documents all 111 authoritative legal instruments tracked by the LegalMitra National Legal Registry, including statutory status, official jurisdiction, publication dates, and Section 52(1)(q) copyright clearance bases:\n"
    ]
    
    for idx, s in enumerate(sources, 1):
        sid = s.get("source_id", "UNKNOWN")
        title = s.get("official_title", "Unknown Title")
        authority = s.get("issuing_authority", "Government of India")
        jurisdiction = s.get("jurisdiction", "IN")
        stype = s.get("source_type", "statute")
        state = s.get("current_state", "DISCOVERED")
        url = s.get("source_url", "https://www.indiacode.nic.in")
        pub_date = s.get("publication_date") or s.get("commencement_date") or "Official Gazette"
        rights = s.get("rights_basis", "Section 52(1)(q) Copyright Act 1957")
        passages = s.get("derived_passages_count", 0)
        eligible = "Yes (Pretraining Manifest v4)" if s.get("pretraining_eligible") else "No (Catalog / Backlog / Quarantined)"
        
        lines.append(f"#### Source {idx:03d}: `{sid}` — {title}")
        lines.append(f"- **Issuing Authority**: {authority}")
        lines.append(f"- **Jurisdiction**: `{jurisdiction}` | **Document Class**: `{stype}` | **Publication / Enactment**: `{pub_date}`")
        lines.append(f"- **Lifecycle State**: `{state}` | **Pretraining Eligible**: {eligible}")
        lines.append(f"- **Statutory Rights Basis**: {rights}")
        lines.append(f"- **Official Repository URL**: [{url}]({url})")
        lines.append(f"- **Derived Knowledge Chunks**: {passages} chunks indexed in `data/legalmitra_kb.db`")
        lines.append("")
    
    return "\n".join(lines)
