"""
LegalMitra Fact-Sensitive Legal Analysis Engine (Phase 50)
Separates user facts, source facts, inferences, and unknown facts.
Constructs structured Issue-Rule-Application-Conclusion (IRAC) representations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.orchestration.evidence_orchestrator import EvidenceItem, OrchestratedEvidenceSet
from legalmitra.orchestration.query_understanding import ParsedLegalQuery


class FactClassification(str, Enum):
    USER_PROVIDED_FACT = "USER_PROVIDED_FACT"
    SOURCE_ESTABLISHED_FACT = "SOURCE_ESTABLISHED_FACT"
    ANALYTICAL_INFERENCE = "ANALYTICAL_INFERENCE"
    UNKNOWN_OR_DISPUTED_FACT = "UNKNOWN_OR_DISPUTED_FACT"


@dataclass
class FactNode:
    """Represents a single fact with explicit epistemic status."""
    fact_id: str
    statement: str
    classification: FactClassification
    source_reference: Optional[str] = None
    verification_notes: Optional[str] = None


@dataclass
class IRACUnit:
    """Issue-Rule-Application-Conclusion structured analysis unit."""
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
    conditional_branches: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class FactAnalysisReport:
    """Comprehensive epistemically separated fact analysis report."""
    facts: List[FactNode] = field(default_factory=list)
    irac_units: List[IRACUnit] = field(default_factory=list)
    unresolved_factual_dependencies: List[str] = field(default_factory=list)
    competing_interpretations_present: bool = False
    competing_notes: Optional[str] = None


class FactSensitiveAnalyzer:
    """
    Performs rigorous fact-to-rule mapping without allowing unverified user allegations
    to morph into source-established legal facts.
    """

    def analyze(
        self,
        parsed_query: ParsedLegalQuery,
        evidence_set: OrchestratedEvidenceSet,
    ) -> FactAnalysisReport:
        report = FactAnalysisReport()

        # 1. Populate User-Provided Facts (never verified by default)
        idx = 1
        for uf in parsed_query.user_supplied_facts:
            report.facts.append(FactNode(
                fact_id=f"FACT-USR-{idx}",
                statement=uf,
                classification=FactClassification.USER_PROVIDED_FACT,
                source_reference="User Prompt",
                verification_notes="Supplied by inquirer; not independently verified by official record.",
            ))
            idx += 1

        # 2. Populate Alleged Facts (Unverified assertions)
        for af in parsed_query.alleged_facts_unverified:
            report.facts.append(FactNode(
                fact_id=f"FACT-ALG-{idx}",
                statement=af,
                classification=FactClassification.USER_PROVIDED_FACT,
                source_reference="User Allegation",
                verification_notes="Unsubstantiated allegation; cannot be treated as proven fact.",
            ))
            idx += 1

        # 3. Populate Source-Established Facts from primary statutes / precedents
        src_idx = 1
        for st in evidence_set.primary_statutes[:3]:
            report.facts.append(FactNode(
                fact_id=f"FACT-SRC-{src_idx}",
                statement=f"Statutory Provision: {st.title} {st.provision_or_para_ref} in force with text: '{st.passage_text[:120]}...'",
                classification=FactClassification.SOURCE_ESTABLISHED_FACT,
                source_reference=f"{st.source_id}:{st.provision_or_para_ref}",
                verification_notes="Extracted from authoritative Gazette / statute repository.",
            ))
            src_idx += 1

        for cb in evidence_set.constitution_benches[:2]:
            report.facts.append(FactNode(
                fact_id=f"FACT-SRC-{src_idx}",
                statement=f"Constitution Bench Ratio: {cb.title} held: '{cb.passage_text[:120]}...'",
                classification=FactClassification.SOURCE_ESTABLISHED_FACT,
                source_reference=cb.source_id,
                verification_notes="Extracted from Supreme Court Reports / official reporter.",
            ))
            src_idx += 1

        # 4. Unknown or Disputed Facts
        for mf in parsed_query.missing_facts:
            report.facts.append(FactNode(
                fact_id=f"FACT-UNK-{idx}",
                statement=f"Missing Fact: {mf}",
                classification=FactClassification.UNKNOWN_OR_DISPUTED_FACT,
                verification_notes="Fact not supplied by user; outcome contingent upon its resolution.",
            ))
            idx += 1
            report.unresolved_factual_dependencies.append(mf)

        # 5. Build IRAC Units for each candidate issue
        for i_idx, issue_stmt in enumerate(parsed_query.candidate_issues, start=1):
            # Gather relevant rules
            applicable_rules = []
            authorities = []
            exceptions = []
            conflicts = []

            for st in evidence_set.primary_statutes:
                applicable_rules.append(f"{st.title} ({st.provision_or_para_ref})")
                authorities.append(st.source_id)

            for cb in evidence_set.constitution_benches:
                applicable_rules.append(f"{cb.title}")
                authorities.append(cb.source_id)

            for dr in evidence_set.delegated_rules:
                applicable_rules.append(f"{dr.title} ({dr.provision_or_para_ref})")
                authorities.append(dr.source_id)

            for ca in evidence_set.contrary_authorities:
                if ca.is_stayed_or_referred:
                    conflicts.append(f"{ca.title}: {ca.conflict_notes}")
                elif ca.is_contrary_authority:
                    exceptions.append(f"{ca.title}: {ca.passage_text}")

            for uc in evidence_set.unresolved_conflicts:
                conflicts.append(f"{uc.get('nature')}: {uc.get('territorial_bindingness')}")

            # Check if competing interpretations exist
            competing = len(conflicts) > 0 or len(evidence_set.contrary_authorities) > 0

            # Formulate provisional conclusion
            conclusion = "Subject to the statutory provisions and authoritative precedents cited."
            if parsed_query.missing_facts:
                conclusion = "Provisional analysis only: definitive outcome cannot be determined without clarification of missing material facts."

            # Check if this issue corresponds to a decomposed issue
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
            )
            report.irac_units.append(irac)

        report.competing_interpretations_present = len(evidence_set.contrary_authorities) > 0 or len(evidence_set.unresolved_conflicts) > 0
        if report.competing_interpretations_present:
            report.competing_notes = "Authorities or statutory versions present competing legal positions; qualifications applied."

        return report

