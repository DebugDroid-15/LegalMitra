"""
Master Assembler for LegalMitra README.md.
Combines all parts, validates line counts, checks formatting, and writes to root README.md.
"""

import sys
from pathlib import Path

# Add project root to sys.path
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from scripts.readme_builder.part_01_to_03 import (
    generate_header,
    generate_table_of_contents,
    generate_part_01,
    generate_part_02,
    generate_part_03,
)
from scripts.readme_builder.part_04_repository import generate_part_04
from scripts.readme_builder.module_doc_generator import (
    generate_subpackage_reference,
    generate_scripts_reference,
    generate_tests_reference,
)
from scripts.readme_builder.pydantic_schema_generator import generate_pydantic_schema_markdown
from scripts.readme_builder.part_05_to_08 import generate_part_05_to_08
from scripts.readme_builder.part_09_to_11 import generate_part_09_to_11
from scripts.readme_builder.source_catalog_generator import generate_source_catalog_markdown
from scripts.readme_builder.kb_inventory_generator import generate_kb_inventory_markdown
from scripts.readme_builder.part_12_to_15 import generate_part_12_to_15
from scripts.readme_builder.benchmark_catalog_generator import generate_benchmark_catalog_markdown
from scripts.readme_builder.part_16_to_18 import generate_part_16_to_18
from scripts.readme_builder.part_19_troubleshooting import generate_part_19
from scripts.readme_builder.part_20_milestones import generate_part_20
from scripts.readme_builder.phase_history_generator import generate_detailed_phase_history
from scripts.readme_builder.part_21_to_25 import (
    generate_part_21_governance,
    generate_part_22_deployment,
    generate_part_23_appendices_intro,
    generate_part_24_contribution,
    generate_part_25_ownership_and_roadmap,
)
from scripts.readme_builder.cli_reference_generator import generate_detailed_cli_reference
from scripts.readme_builder.glossary_and_schemas_generator import generate_expanded_legal_glossary

def assemble_readme() -> str:
    parts = [
        generate_header(),
        generate_table_of_contents(),
        generate_part_01(),
        generate_part_02(),
        generate_part_03(),
        generate_part_04(),
        generate_subpackage_reference(),
        generate_scripts_reference(),
        generate_tests_reference(),
        generate_pydantic_schema_markdown(),
        generate_part_05_to_08(),
        generate_part_09_to_11(),
        generate_source_catalog_markdown(),
        generate_kb_inventory_markdown(),
        generate_part_12_to_15(),
        generate_benchmark_catalog_markdown(),
        generate_part_16_to_18(),
        generate_part_19(),
        generate_part_20(),
        generate_detailed_phase_history(),
        generate_part_21_governance(),
        generate_part_22_deployment(),
        generate_part_23_appendices_intro(),
        generate_detailed_cli_reference(),
        generate_expanded_legal_glossary(),
        generate_part_24_contribution(),
        generate_part_25_ownership_and_roadmap(),
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    content = assemble_readme()
    lines = content.splitlines()
    non_empty = [l for l in lines if l.strip()]
    print(f"Total Physical Lines: {len(lines)}")
    print(f"Non-Empty Lines:      {len(non_empty)}")
    
    if len(lines) >= 10000 and len(non_empty) >= 8500:
        readme_path = _root / "README.md"
        readme_path.write_text(content, encoding="utf-8")
        print(f"SUCCESS: Successfully generated README.md ({len(lines)} lines, {len(non_empty)} non-empty lines) at {readme_path}")
    else:
        print(f"NOTICE: Current count is {len(lines)} lines. Needs expansion to reach >= 10,000 physical lines.")
