import re
"""
LegalMitra Issue-Level Evidence Matrix & Claim Dependency Validation Engine (Phase 56)
Constructs a structured audit matrix linking decomposed legal issues to material facts,
candidate rules, statutory exceptions/provisos, selected evidence IDs, temporal validity,
precedent status, and claim validation outcomes.
Validates dependencies to ensure downstream conclusions never rest on unsupported intermediate claims.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.orchestration.evidence_orchestrator import EvidenceItem, OrchestratedEvidenceSet
from legalmitra.orchestration.fact_analyzer import FactAnalysisReport
from legalmitra.orchestration.query_understanding import ParsedLegalQuery


class IssueDisposition(str, Enum):
    DIRECT_ANSWER = "DIRECT_ANSWER"
    QUALIFIED_ANSWER = "QUALIFIED_ANSWER"
    CONDITIONAL_ANSWER = "CONDITIONAL_ANSWER"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    ABSTAIN_UNCOMMENCED = "ABSTAIN_UNCOMMENCED"
    ABSTAIN_INSUFFICIENT = "ABSTAIN_INSUFFICIENT"
    ABSTAIN_CONFLICT = "ABSTAIN_CONFLICT"


@dataclass
class IssueEvidenceRecord:
    """Detailed record linking a specific legal issue to its evidentiary basis and disposition."""
    issue_id: str
    issue_statement: str
    material_facts: List[str] = field(default_factory=list)
    unresolved_assumptions: List[str] = field(default_factory=list)
    candidate_rules: List[str] = field(default_factory=list)
    applicable_exceptions: List[str] = field(default_factory=list)
    selected_evidence_ids: List[str] = field(default_factory=list)
    temporal_status: str = "IN_FORCE"
    precedent_status: str = "BINDING_RATIO"
    claim_validation_outcome: str = "FULLY_SUPPORTED"  # FULLY_SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED, TEMPORALLY_UNCERTAIN, INSUFFICIENT_EVIDENCE
    missing_evidence: List[str] = field(default_factory=list)
    issue_disposition: IssueDisposition = IssueDisposition.DIRECT_ANSWER
    prerequisite_issue_id: Optional[str] = None
    dependency_satisfied: bool = True
    conditional_reasoning: Optional[str] = None
    disposition_rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "issue_statement": self.issue_statement,
            "material_facts": self.material_facts,
            "unresolved_assumptions": self.unresolved_assumptions,
            "candidate_rules": self.candidate_rules,
            "applicable_exceptions": self.applicable_exceptions,
            "selected_evidence_ids": self.selected_evidence_ids,
            "temporal_status": self.temporal_status,
            "precedent_status": self.precedent_status,
            "claim_validation_outcome": self.claim_validation_outcome,
            "missing_evidence": self.missing_evidence,
            "issue_disposition": self.issue_disposition.value,
            "prerequisite_issue_id": self.prerequisite_issue_id,
            "dependency_satisfied": self.dependency_satisfied,
            "conditional_reasoning": self.conditional_reasoning,
            "disposition_rationale": self.disposition_rationale,
        }


@dataclass
class IssueEvidenceMatrix:
    """Comprehensive matrix of issue-level evidence records with dependency validation."""
    records: List[IssueEvidenceRecord] = field(default_factory=list)
    has_unsupported_dependencies: bool = False
    dependency_failure_notes: List[str] = field(default_factory=list)
    cross_issue_contradictions: List[str] = field(default_factory=list)
    has_partial_support: bool = False
    is_conditional: bool = False
    fully_supported_count: int = 0
    qualified_count: int = 0
    unresolved_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "records": [r.to_dict() for r in self.records],
            "has_unsupported_dependencies": self.has_unsupported_dependencies,
            "dependency_failure_notes": self.dependency_failure_notes,
            "cross_issue_contradictions": self.cross_issue_contradictions,
            "has_partial_support": self.has_partial_support,
            "is_conditional": self.is_conditional,
            "fully_supported_count": self.fully_supported_count,
            "qualified_count": self.qualified_count,
            "unresolved_count": self.unresolved_count,
        }

    def format_markdown_table(self) -> str:
        lines = [
            "| Issue ID | Legal Issue | Candidate Rules | Temporal / Authority Status | Validation Outcome | Disposition |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for r in self.records:
            rules_str = ", ".join(r.candidate_rules[:2]) if r.candidate_rules else "General Law"
            lines.append(
                f"| `{r.issue_id}` | {r.issue_statement[:45]}... | {rules_str} | {r.temporal_status} / {r.precedent_status} | `{r.claim_validation_outcome}` | `{r.issue_disposition.value}` |"
            )
        return "\n".join(lines)


class ClaimDependencyValidator:
    """
    Constructs and audits the IssueEvidenceMatrix from parsed query, evidence set, and facts.
    Enforces that intermediate unsupported premises halt unconditional downstream conclusions.
    """

    def build_matrix(
        self,
        parsed_query: ParsedLegalQuery,
        evidence_set: OrchestratedEvidenceSet,
        fact_report: FactAnalysisReport,
    ) -> IssueEvidenceMatrix:
        matrix = IssueEvidenceMatrix()

        # If decomposed issues are available in parsed_query, use them; otherwise use IRAC units
        issue_sources = []
        if getattr(parsed_query, "decomposed_issues", None):
            for d in parsed_query.decomposed_issues:
                issue_sources.append({
                    "issue_id": d.get("issue_id", "ISSUE-1"),
                    "statement": d.get("statement", ""),
                    "governing_statute": d.get("governing_statute", ""),
                    "relationship_type": d.get("relationship_type", "PRIMARY_RULE"),
                    "prerequisite_issue_id": d.get("prerequisite_issue_id"),
                    "conditional_rule": d.get("conditional_rule"),
                })
        else:
            for idx, irac in enumerate(fact_report.irac_units, start=1):
                issue_sources.append({
                    "issue_id": irac.issue_id or f"ISSUE-{idx}",
                    "statement": irac.issue_statement,
                    "governing_statute": irac.applicable_rule,
                    "relationship_type": "PRIMARY_RULE",
                    "prerequisite_issue_id": getattr(irac, "issue_dependency_id", None),
                    "conditional_rule": None,
                })

        # Build records
        for isrc in issue_sources:
            issue_id = isrc["issue_id"]
            stmt = isrc["statement"]
            prereq_id = isrc.get("prerequisite_issue_id")

            # Determine candidate rules and exceptions
            cand_rules = []
            exceptions = []
            ev_ids = []
            temp_status = "IN_FORCE"
            prec_status = "BINDING_RATIO"
            outcome = "FULLY_SUPPORTED"
            missing_ev = []
            disposition = IssueDisposition.DIRECT_ANSWER
            conditional_reasoning = None
            rationale = "Grounded in primary legislation and binding authority."

            # Check if this issue is specifically about uncommenced enactment
            q_low = (parsed_query.original_query + " " + stmt).lower()
            if any(term in stmt.lower() for term in ["uncommenced", "code on wages", "industrial relations code", "osh code"]):
                temp_status = "ENACTED_UNCOMMENCED"
                outcome = "TEMPORALLY_UNCERTAIN"
                disposition = IssueDisposition.ABSTAIN_UNCOMMENCED
                missing_ev.append("Official Gazette commencement notification under enabling section")
                rationale = "Enactment has received Presidential assent but remains uncommenced by executive notification."

            # Check if this issue is specifically about infrastructure bar / SRA Section 20A
            elif "20a" in stmt.lower() or "infrastructure" in stmt.lower():
                cand_rules.append("Specific Relief Act, 1963 Section 20A")
                exceptions.append("Section 20A(1) bar on injunctions in infrastructure projects specified in Schedule")
                for st in evidence_set.primary_statutes:
                    if "SRA" in st.source_id or "SPECIFIC_RELIEF" in st.source_id:
                        ev_ids.append(st.item_id)
                outcome = "FULLY_SUPPORTED"
                disposition = IssueDisposition.QUALIFIED_ANSWER
                rationale = "Section 20A operates as a statutory bar prohibiting injunctions that cause impediment/delay in infrastructure projects."

            # Check if this issue is about Hindu Succession daughter's coparcenary and pre-2004 partition proviso
            elif ("hindu succession" in stmt.lower() or "coparcen" in stmt.lower() or "hsa" in stmt.lower()) and (bool(re.search(r"\bsection\s*6\b(?![a-zA-Z0-9])", stmt, re.I)) or "coparcen" in stmt.lower() or "partition" in stmt.lower()):
                cand_rules.append("Hindu Succession Act, 1956 Section 6(1)")
                exceptions.append("Section 6(1) Proviso: Savings of registered partitions executed prior to 20 December 2004")
                if "proviso" in stmt.lower() or "2004" in stmt.lower() or "partition" in q_low:
                    conditional_reasoning = (
                        "Branch A (Partition prior to 20 Dec 2004): If registered partition was executed before 20 December 2004, "
                        "it remains protected by Section 6(1) proviso, and the daughter cannot reopen the coparcenary partition.\n"
                        "Branch B (No partition before 20 Dec 2004): Daughter holds coparcenary rights by birth on equal footing with sons."
                    )
                    disposition = IssueDisposition.CONDITIONAL_ANSWER
                    matrix.is_conditional = True
                    rationale = "Governed by statutory proviso in Section 6(1) as interpreted in Vineeta Sharma (2020)."
                else:
                    disposition = IssueDisposition.QUALIFIED_ANSWER

            # Check if this issue is about Commercial Courts Act Section 12A mediation
            elif "12a" in stmt.lower() or "mediation" in stmt.lower():
                cand_rules.append("Commercial Courts Act, 2015 Section 12A")
                for st in evidence_set.primary_statutes:
                    if "COMMERCIAL" in st.source_id:
                        ev_ids.append(st.item_id)
                if "urgent" in q_low or "interim" in q_low or "except" in q_low:
                    exceptions.append("Section 12A(1) exemption where suit contemplates urgent interim relief")
                    conditional_reasoning = (
                        "Branch A (Urgent interim relief contemplated): Pre-institution mediation under Section 12A is not mandatory.\n"
                        "Branch B (No urgent interim relief sought): Pre-institution mediation is mandatory per Patil Automation (2022); non-compliance results in rejection of plaint under Order VII Rule 11 CPC."
                    )
                    disposition = IssueDisposition.CONDITIONAL_ANSWER
                    matrix.is_conditional = True
                    rationale = "Supreme Court in Patil Automation (2022) declared Section 12A mandatory, subject to urgent interim relief exception."
                else:
                    disposition = IssueDisposition.DIRECT_ANSWER
                    rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022)."

            # Check if this issue is about NI Act Section 138 demand notice & Section 142 limitation
            elif "138" in stmt.lower() or "142" in stmt.lower() or "cheque" in q_low:
                cand_rules.append("Negotiable Instruments Act, 1881 Section 138")
                cand_rules.append("Negotiable Instruments Act, 1881 Section 142(1)(b)")
                exceptions.append("Section 142(1)(b) proviso allowing condonation of delay upon sufficient cause")
                disposition = IssueDisposition.DIRECT_ANSWER
                rationale = "Statutory notice within 30 days is a condition precedent under Section 138(b); complaint must be filed within 1 month under Section 142(1)(b)."

            # Check if this issue is about Part Performance & Registration
            elif "53a" in stmt.lower() or "part performance" in stmt.lower() or "registration" in stmt.lower():
                cand_rules.append("Transfer of Property Act, 1882 Section 53A")
                cand_rules.append("Registration Act, 1908 Section 17(1A)")
                exceptions.append("Post-2001 amendment: Section 53A protection unavailable unless agreement to sell is registered")
                disposition = IssueDisposition.QUALIFIED_ANSWER
                rationale = "Section 17(1A) of Registration Act mandates registration of contracts to transfer immovable property for Section 53A protection."

            # Check if query has empty evidence -> INSUFFICIENT_EVIDENCE
            elif evidence_set.total_items_retrieved == 0:
                outcome = "INSUFFICIENT_EVIDENCE"
                disposition = IssueDisposition.ABSTAIN_INSUFFICIENT
                missing_ev.append("Verified primary statute / gazette entry in knowledge base")
                rationale = "No verified source chunks in knowledge base matching this issue."

            # Check if query has unresolved coordinate conflict with missing jurisdiction
            elif evidence_set.unresolved_conflicts and not parsed_query.jurisdiction:
                outcome = "CONTRADICTED"
                disposition = IssueDisposition.ABSTAIN_CONFLICT
                missing_ev.append("Territorial High Court Jurisdiction")
                rationale = "Coordinate High Courts have delivered conflicting decisions; territorial jurisdiction required."

            # Check if clarification is required
            elif parsed_query.clarification_necessary and parsed_query.missing_facts:
                outcome = "PARTIALLY_SUPPORTED"
                disposition = IssueDisposition.CLARIFICATION_REQUIRED
                rationale = f"Missing material facts: {'; '.join(parsed_query.missing_facts)}"

            # Default rule linking from primary statutes and precedents
            else:
                for st in evidence_set.primary_statutes[:2]:
                    cand_rules.append(f"{st.title} {st.provision_or_para_ref}")
                    ev_ids.append(st.item_id)
                for cb in evidence_set.constitution_benches[:1]:
                    cand_rules.append(f"{cb.title} [Constitution Bench]")
                    ev_ids.append(cb.item_id)
                for ca in evidence_set.contrary_authorities:
                    exceptions.append(f"{ca.title}: {ca.conflict_notes or ca.passage_text[:100]}")
                if evidence_set.contrary_authorities:
                    disposition = IssueDisposition.QUALIFIED_ANSWER
                else:
                    disposition = IssueDisposition.DIRECT_ANSWER

            # Build record
            rec = IssueEvidenceRecord(
                issue_id=issue_id,
                issue_statement=stmt,
                material_facts=parsed_query.user_supplied_facts,
                unresolved_assumptions=parsed_query.implicit_assumptions,
                candidate_rules=cand_rules,
                applicable_exceptions=exceptions,
                selected_evidence_ids=ev_ids,
                temporal_status=temp_status,
                precedent_status=prec_status,
                claim_validation_outcome=outcome,
                missing_evidence=missing_ev,
                issue_disposition=disposition,
                prerequisite_issue_id=prereq_id,
                dependency_satisfied=True,
                conditional_reasoning=conditional_reasoning,
                disposition_rationale=rationale,
            )
            matrix.records.append(rec)

        # Enforce Claim Dependency Validation
        record_map = {r.issue_id: r for r in matrix.records}
        for rec in matrix.records:
            if rec.prerequisite_issue_id and rec.prerequisite_issue_id in record_map:
                prereq = record_map[rec.prerequisite_issue_id]
                # If prerequisite is not fully or qualifiedly supported, dependent issue cannot be directly affirmed
                if prereq.claim_validation_outcome in ("UNSUPPORTED", "CONTRADICTED", "TEMPORALLY_UNCERTAIN", "INSUFFICIENT_EVIDENCE"):
                    rec.dependency_satisfied = False
                    rec.claim_validation_outcome = "PARTIALLY_SUPPORTED"
                    rec.issue_disposition = IssueDisposition.QUALIFIED_ANSWER
                    matrix.has_unsupported_dependencies = True
                    note = (
                        f"Downstream issue '{rec.issue_id}' depends on prerequisite '{prereq.issue_id}', "
                        f"which has unresolved outcome '{prereq.claim_validation_outcome}'. Unconditional affirmation suppressed."
                    )
                    matrix.dependency_failure_notes.append(note)
                    rec.disposition_rationale += f" [Prerequisite '{prereq.issue_id}' unsatisfied: {note}]"

        # Check for multi-issue partial support
        has_answerable = any(
            r.issue_disposition in (IssueDisposition.DIRECT_ANSWER, IssueDisposition.QUALIFIED_ANSWER, IssueDisposition.CONDITIONAL_ANSWER)
            for r in matrix.records
        )
        has_unanswerable = any(
            r.issue_disposition in (IssueDisposition.ABSTAIN_UNCOMMENCED, IssueDisposition.ABSTAIN_INSUFFICIENT, IssueDisposition.ABSTAIN_CONFLICT, IssueDisposition.CLARIFICATION_REQUIRED)
            for r in matrix.records
        )
        if len(matrix.records) > 1 and has_answerable and has_unanswerable:
            matrix.has_partial_support = True

        # Summarize counts
        matrix.fully_supported_count = sum(1 for r in matrix.records if r.claim_validation_outcome == "FULLY_SUPPORTED")
        matrix.qualified_count = sum(1 for r in matrix.records if r.issue_disposition == IssueDisposition.QUALIFIED_ANSWER)
        matrix.unresolved_count = sum(
            1 for r in matrix.records
            if r.issue_disposition in (IssueDisposition.ABSTAIN_UNCOMMENCED, IssueDisposition.ABSTAIN_INSUFFICIENT, IssueDisposition.ABSTAIN_CONFLICT, IssueDisposition.CLARIFICATION_REQUIRED)
        )

        return matrix
