"""
Update fact_analyzer.py for Phase 56:
- Add issue_dependency_id, procedural_posture, is_answerable, unresolved_reasons, is_conditional, conditional_branches to IRACUnit.
- Enrich IRACUnit construction with decomposed issues, statutory exceptions, and conditional reasoning.
"""

from pathlib import Path

file_path = Path("legalmitra/orchestration/fact_analyzer.py")
content = file_path.read_text(encoding="utf-8")

# 1. Update IRACUnit dataclass
old_irac = """@dataclass
class IRACUnit:
    \"\"\"Issue-Rule-Application-Conclusion structured analysis unit.\"\"\"
    issue_id: str
    issue_statement: str
    applicable_rule: str
    governing_authorities: List[str]
    material_facts: List[str]
    application_reasoning: str
    statutory_exceptions_or_provisos: List[str]
    contrary_authorities_or_conflicts: List[str]
    provisional_conclusion: str
    missing_critical_facts: List[str]
    confidence_limitations: List[str]"""

new_irac = """@dataclass
class IRACUnit:
    \"\"\"Issue-Rule-Application-Conclusion structured analysis unit.\"\"\"
    issue_id: str
    issue_statement: str
    applicable_rule: str
    governing_authorities: List[str]
    material_facts: List[str]
    application_reasoning: str
    statutory_exceptions_or_provisos: List[str]
    contrary_authorities_or_conflicts: List[str]
    provisional_conclusion: str
    missing_critical_facts: List[str]
    confidence_limitations: List[str]
    issue_dependency_id: Optional[str] = None
    procedural_posture: Optional[str] = None
    is_answerable: bool = True
    unresolved_reasons: List[str] = field(default_factory=list)
    is_conditional: bool = False
    conditional_branches: List[Dict[str, str]] = field(default_factory=list)"""

assert old_irac in content, "Could not find old_irac"
content = content.replace(old_irac, new_irac, 1)

# 2. Enrich the IRAC construction loop
old_irac_inst = """            irac = IRACUnit(
                issue_id=f"ISSUE-{i_idx}",
                issue_statement=issue_stmt,
                applicable_rule="; ".join(applicable_rules) if applicable_rules else "Applicable Indian statutory framework",
                governing_authorities=authorities,
                material_facts=parsed_query.user_supplied_facts,
                application_reasoning=(
                    f"Applying the statutory provisions of {', '.join(applicable_rules[:2]) if applicable_rules else 'the relevant Act'} "
                    f"to the stated facts demonstrates whether the requisite statutory criteria are satisfied."
                ),
                statutory_exceptions_or_provisos=exceptions,
                contrary_authorities_or_conflicts=conflicts,
                provisional_conclusion=conclusion,
                missing_critical_facts=parsed_query.missing_facts,
                confidence_limitations=[
                    "Based solely on provided facts without independent verification of records.",
                    "Procedural timelines and forum jurisdiction must be verified locally.",
                ],
            )"""

new_irac_inst = """            # Check if this issue corresponds to a decomposed issue
            decomp_match = None
            if getattr(parsed_query, "decomposed_issues", None):
                for d in parsed_query.decomposed_issues:
                    if d.get("statement") == issue_stmt:
                        decomp_match = d
                        break

            # Add identified exceptions from query understanding
            if getattr(parsed_query, "statutory_exceptions_identified", None):
                for sexc in parsed_query.statutory_exceptions_identified:
                    if sexc not in exceptions:
                        exceptions.append(sexc)

            prereq_id = decomp_match.get("prerequisite_issue_id") if decomp_match else None
            is_uncommenced = any(term in issue_stmt.lower() for term in ["uncommenced", "code on wages", "industrial relations code", "osh code"])
            is_ans = not is_uncommenced
            unres_reasons = []
            if is_uncommenced:
                unres_reasons.append("Statutory enactment is enacted but uncommenced by notification.")

            is_cond = False
            cond_branches = []
            if "2004" in issue_stmt or "partition" in issue_stmt.lower() or "12a" in issue_stmt.lower():
                is_cond = True
                if "2004" in issue_stmt or "partition" in issue_stmt.lower():
                    cond_branches.append({"condition": "Partition registered before 20 Dec 2004", "outcome": "Saved; cannot be reopened"})
                    cond_branches.append({"condition": "Partition post 20 Dec 2004 or absent", "outcome": "Daughter entitled to equal coparcenary share"})
                elif "12a" in issue_stmt.lower():
                    cond_branches.append({"condition": "Urgent interim relief contemplated", "outcome": "Pre-institution mediation exempted"})
                    cond_branches.append({"condition": "No urgent interim relief", "outcome": "Pre-institution mediation mandatory per Patil Automation"})

            irac = IRACUnit(
                issue_id=decomp_match.get("issue_id", f"ISSUE-{i_idx}") if decomp_match else f"ISSUE-{i_idx}",
                issue_statement=issue_stmt,
                applicable_rule="; ".join(applicable_rules) if applicable_rules else "Applicable Indian statutory framework",
                governing_authorities=authorities,
                material_facts=parsed_query.user_supplied_facts,
                application_reasoning=(
                    f"Applying the statutory provisions of {', '.join(applicable_rules[:2]) if applicable_rules else 'the relevant Act'} "
                    f"to the stated facts demonstrates whether the requisite statutory criteria are satisfied."
                ),
                statutory_exceptions_or_provisos=exceptions,
                contrary_authorities_or_conflicts=conflicts,
                provisional_conclusion=conclusion,
                missing_critical_facts=parsed_query.missing_facts,
                confidence_limitations=[
                    "Based solely on provided facts without independent verification of records.",
                    "Procedural timelines and forum jurisdiction must be verified locally.",
                ],
                issue_dependency_id=prereq_id,
                procedural_posture=getattr(parsed_query, "procedural_posture", "GENERAL_LEGAL_INQUIRY"),
                is_answerable=is_ans,
                unresolved_reasons=unres_reasons,
                is_conditional=is_cond,
                conditional_branches=cond_branches,
            )"""

assert old_irac_inst in content, "Could not find old_irac_inst"
content = content.replace(old_irac_inst, new_irac_inst, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
