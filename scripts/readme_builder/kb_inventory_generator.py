"""
Knowledge Base Chunk Inventory Generator for LegalMitra README Part XI.
Extracts all 1,505 stored chunks from data/legalmitra_kb.db,
grouping them by primary legal source and generating an exhaustive provision inventory.
"""

import sqlite3
from collections import defaultdict
from pathlib import Path

def generate_kb_inventory_markdown() -> str:
    db_path = Path("data/legalmitra_kb.db")
    if not db_path.exists():
        return "\n<!-- legalmitra_kb.db not found -->\n"
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT chunk_id, source_id, act_or_case_title, provision_or_para_ref, authority_level, content, is_synthetic_scaffold
        FROM legal_chunks
        ORDER BY act_or_case_title, provision_or_para_ref
    """)
    rows = c.fetchall()
    conn.close()
    
    # Group by act_or_case_title
    by_source = defaultdict(list)
    for r in rows:
        by_source[r[2]].append(r)
        
    lines = [
        "### 11.7 Comprehensive Knowledge Base Chunks Inventory (1,505 Stored Chunks)\n",
        f"The LegalMitra Knowledge Base (`data/legalmitra_kb.db`) contains **{len(rows)} stored chunks** across **{len(by_source)} primary legal sources**. The following inventory provides an exhaustive reference table for every stored statutory provision, ratio decidendi, and procedural chunk:\n"
    ]
    
    for act_title, chunks in sorted(by_source.items()):
        total_chunks = len(chunks)
        sample_auth = chunks[0][4]
        scaffold_flag = any(chk[6] == 1 for chk in chunks)
        scaffold_note = " **[STRICTLY QUARANTINED TEST SCAFFOLD]**" if scaffold_flag else ""
        
        lines.append(f"#### Source: {act_title} ({total_chunks} Chunks){scaffold_note}")
        lines.append(f"- **Authority Level**: `{sample_auth}` | **Indexed Chunks**: {total_chunks}")
        lines.append("")
        lines.append("| Chunk Identifier | Provision / Para Reference | Authority Level | Verbatim Content Snippet |")
        lines.append("|:---|:---|:---:|:---|")
        
        for chk in chunks:
            cid = chk[0]
            pref = chk[3]
            auth = chk[4]
            # Clean snippet for markdown table
            raw_snippet = chk[5].replace("\n", " ").replace("|", "\\|").strip()
            snippet = (raw_snippet[:80] + "...") if len(raw_snippet) > 80 else raw_snippet
            lines.append(f"| `{cid}` | {pref} | `{auth}` | {snippet} |")
        
        lines.append("")
        
    return "\n".join(lines)
