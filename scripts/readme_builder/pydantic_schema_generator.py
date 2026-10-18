"""
Pydantic Schema Dictionary Generator for LegalMitra README Part IV & XXIII.
Inspects all 31 core Pydantic domain models and generates comprehensive field reference tables.
"""

import inspect
from pathlib import Path
from typing import Any, Dict, List

import legalmitra.schemas.statute as s1
import legalmitra.schemas.judgment as s2
import legalmitra.schemas.legal_qa as s3
import legalmitra.schemas.case_analysis as s4
import legalmitra.schemas.procedural_guide as s5
import legalmitra.schemas.registry as s6
import legalmitra.schemas.evaluation as s7
import legalmitra.web.schemas as s8
import legalmitra.knowledge.models as s9
import legalmitra.rag.schemas as s10

def generate_pydantic_schema_markdown() -> str:
    modules = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    
    lines = [
        "### 4.26 Comprehensive Pydantic Data Contracts & Field Reference (31 Models)\n",
        "Every domain entity, API request, and storage record in LegalMitra is governed by strict Pydantic V2 models. The following dictionary details all 31 models, their field types, constraints, and descriptions:\n"
    ]
    
    for m in modules:
        mod_name = m.__name__
        for name, obj in inspect.getmembers(m, inspect.isclass):
            if hasattr(obj, "model_fields") and obj.__module__ == mod_name:
                doc = inspect.getdoc(obj) or "Domain entity contract."
                lines.append(f"#### Model: `{name}` (`{mod_name}.{name}`)")
                lines.append(f"- **Contract Description**: {doc.splitlines()[0]}")
                lines.append("")
                lines.append("| Field Name | Type Annotation | Default / Required | Description & Constraints |")
                lines.append("|:---|:---|:---:|:---|")
                
                fields = obj.model_fields
                for fname, fval in fields.items():
                    ftype = str(fval.annotation).replace("typing.", "").replace("NoneType", "None").replace("|", "\\|")
                    fdesc = (fval.description or "Domain attribute.").replace("|", "\\|").replace("\n", " ")
                    is_req = "Required" if fval.is_required() else f"`{fval.default}`"
                    lines.append(f"| `{fname}` | `{ftype}` | {is_req} | {fdesc} |")
                
                lines.append("")
                
    return "\n".join(lines)
