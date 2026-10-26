"""
Comprehensive Documentation Generator for LegalMitra Phase 62.
Target: ~5,000 lines of highly technical, concrete, non-repetitive engineering documentation
across 20 dedicated markdown reports in docs/.
"""

import os
from pathlib import Path

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

def write_doc(filename: str, content: str):
    path = DOCS_DIR / filename
    cleaned = content.strip() + "\n"
    path.write_text(cleaned, encoding="utf-8")
    lines = len(cleaned.splitlines())
    print(f"Wrote {filename}: {lines} lines")
    return lines

total_lines = 0
