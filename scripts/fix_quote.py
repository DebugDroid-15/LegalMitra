from pathlib import Path

p = Path("legalmitra/orchestration/evidence_matrix.py")
content = p.read_text(encoding="utf-8")
content = content.replace(
    'rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022).\n',
    'rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022)."\n'
)
content = content.replace(
    'rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022).\r\n',
    'rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022)."\r\n'
)
p.write_text(content, encoding="utf-8")
print("Quote replaced successfully.")
