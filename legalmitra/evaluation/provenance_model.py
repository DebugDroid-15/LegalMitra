"""
End-to-End Legal Authority Verification & Proposition Provenance Model (Phase 59)

Establishes an auditable, uncompromised provenance chain linking every material legal proposition
from the final answer back to its primary statutory or judicial authority.
Explicitly models the 12 distinct evidence lifecycle states, preventing their collapse into a single Boolean.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import os
import re
import sqlite3
from typing import Any, Dict, List, Optional, Set, Tuple


class EvidenceLifecycleState(str, Enum):
    """The 12 distinct, non-collapsible evidence lifecycle states."""
    SOURCE_REGISTERED = "SOURCE_REGISTERED"
    SOURCE_ACQUIRED = "SOURCE_ACQUIRED"
    SOURCE_PARSED = "SOURCE_PARSED"
    SOURCE_STRUCTURE_VALIDATED = "SOURCE_STRUCTURE_VALIDATED"
    SOURCE_AUTHENTICITY_VERIFIED = "SOURCE_AUTHENTICITY_VERIFIED"
    SOURCE_INDEXED = "SOURCE_INDEXED"
    PASSAGE_RETRIEVABLE = "PASSAGE_RETRIEVABLE"
    TEMPORALLY_APPLICABLE = "TEMPORALLY_APPLICABLE"
    JURISDICTIONALLY_APPLICABLE = "JURISDICTIONALLY_APPLICABLE"
    SUBSTANTIVELY_SUPPORTS = "SUBSTANTIVELY_SUPPORTS"
    RIGHTS_CLEARED = "RIGHTS_CLEARED"
    ADVOCATE_REVIEWED = "ADVOCATE_REVIEWED"


class SubstantiveRelation(str, Enum):
    """Substantive relationship between primary authority passage and proposition."""
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    QUALIFIES = "QUALIFIES"
    DOES_NOT_RESOLVE = "DOES_NOT_RESOLVE"


class AuthorityLevel(str, Enum):
    """Precedent hierarchy and constitutional/statutory authority levels."""
    CONSTITUTIONAL_PROVISION = "CONSTITUTIONAL_PROVISION"
    CENTRAL_STATUTE = "CENTRAL_STATUTE"
    STATE_STATUTE = "STATE_STATUTE"
    DELEGATED_LEGISLATION = "DELEGATED_LEGISLATION"
    BINDING_CONSTITUTION_BENCH = "BINDING_CONSTITUTION_BENCH"
    BINDING_COORDINATE_BENCH = "BINDING_COORDINATE_BENCH"
    PERSUASIVE_HIGH_COURT = "PERSUASIVE_HIGH_COURT"
    OVERRULED_HISTORICAL = "OVERRULED_HISTORICAL"
    REFERRED_SUB_JUDICE = "REFERRED_SUB_JUDICE"
    STAYED_INTERIM = "STAYED_INTERIM"
    DISTINGUISHED = "DISTINGUISHED"


class AuthenticityStatus(str, Enum):
    """Authenticity verification status of source document."""
    AUTHENTIC_GAZETTE = "AUTHENTIC_GAZETTE"
    OFFICIAL_PORTAL = "OFFICIAL_PORTAL"
    REPORTER_VERIFIED = "REPORTER_VERIFIED"
    UNVERIFIED_SOURCE = "UNVERIFIED_SOURCE"
    SYNTHETIC_QUARANTINED = "SYNTHETIC_QUARANTINED"
    FABRICATED = "FABRICATED"


class RightsStatus(str, Enum):
    """Rights clearance status under Indian copyright and repository rules."""
    PUBLIC_DOMAIN_STATUTE = "PUBLIC_DOMAIN_STATUTE"  # Section 52(1)(q) Copyright Act, 1957
    FAIR_DEALING_LEGAL = "FAIR_DEALING_LEGAL"
    RESTRICTED_REUSE = "RESTRICTED_REUSE"


@dataclass
class LegalPropositionProvenance:
    """
    Complete, end-to-end auditable provenance chain for a material legal proposition.
    """
    proposition_id: str
    issue_id: str
    user_query: str
    proposition_text: str
    source_id: str
    source_type: str  # CENTRAL_ACT, STATE_ACT, DELEGATED_RULES, JUDICIAL_PRECEDENT, CONSTITUTIONAL_PROVISION
    authority_title: str
    pinpoint_reference: str  # e.g., "Section 20A(1)", "Paragraph 42", "Article 226"
    evidence_states: List[EvidenceLifecycleState] = field(default_factory=list)
    highest_verified_state: EvidenceLifecycleState = EvidenceLifecycleState.SOURCE_REGISTERED
    authenticity_status: AuthenticityStatus = AuthenticityStatus.OFFICIAL_PORTAL
    passage_locator: str = ""  # Chunk hash or database primary key
    verbatim_passage: str = ""
    jurisdiction: str = "NATIONAL"  # "NATIONAL", "IN-DL", "IN-MH", etc.
    effective_from: Optional[str] = None
    effective_until: Optional[str] = None
    evaluation_date: Optional[str] = None
    temporal_applicability: bool = True
    legislative_status: str = "IN_FORCE"  # IN_FORCE, AMENDED, REPEALED_WITH_SAVINGS, UNCOMMENCED
    precedent_status: AuthorityLevel = AuthorityLevel.CENTRAL_STATUTE
    substantive_relation: SubstantiveRelation = SubstantiveRelation.SUPPORTS
    material_exceptions: List[str] = field(default_factory=list)
    prerequisite_dependencies: List[str] = field(default_factory=list)
    dependencies_satisfied: bool = True
    rights_status: RightsStatus = RightsStatus.PUBLIC_DOMAIN_STATUTE
    human_review_required: bool = False
    review_notes: str = ""
    audit_hash: str = ""

    def compute_canonical_audit_hash(self) -> str:
        """
        Computes a deterministic canonical SHA-256 audit digest binding the proposition
        to its exact source identifier, pinpoint reference, and proposition text.
        """
        raw = f"{self.proposition_id}:{self.source_id}:{self.pinpoint_reference}:{self.proposition_text}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def verify_hash_integrity(self) -> tuple:
        """
        Recomputes the canonical audit hash and verifies that content or metadata
        has not been altered post-creation.
        """
        if not self.audit_hash:
            return False, "Missing audit hash: proposition was not cryptographically bound."
        expected = self.compute_canonical_audit_hash()
        if self.audit_hash != expected:
            return False, f"Cryptographic tamper detected: audit hash '{self.audit_hash}' does not match expected '{expected}'."
        return True, "Hash verified"

    def __post_init__(self):
        if not self.audit_hash:
            self.audit_hash = self.compute_canonical_audit_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposition_id": self.proposition_id,
            "issue_id": self.issue_id,
            "user_query": self.user_query,
            "proposition_text": self.proposition_text,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "authority_title": self.authority_title,
            "pinpoint_reference": self.pinpoint_reference,
            "evidence_states": [s.value for s in self.evidence_states],
            "highest_verified_state": self.highest_verified_state.value,
            "authenticity_status": self.authenticity_status.value,
            "passage_locator": self.passage_locator,
            "verbatim_passage": self.verbatim_passage,
            "jurisdiction": self.jurisdiction,
            "effective_from": self.effective_from,
            "effective_until": self.effective_until,
            "evaluation_date": self.evaluation_date,
            "temporal_applicability": self.temporal_applicability,
            "legislative_status": self.legislative_status,
            "precedent_status": self.precedent_status.value,
            "substantive_relation": self.substantive_relation.value,
            "material_exceptions": self.material_exceptions,
            "prerequisite_dependencies": self.prerequisite_dependencies,
            "dependencies_satisfied": self.dependencies_satisfied,
            "rights_status": self.rights_status.value,
            "human_review_required": self.human_review_required,
            "review_notes": self.review_notes,
            "audit_hash": self.audit_hash,
        }


@dataclass
class ProvenanceAuditReport:
    """Comprehensive machine-readable provenance audit report."""
    audit_id: str
    total_propositions: int
    fully_provenanced_propositions: int
    unprovenanced_propositions: int
    state_distribution: Dict[str, int]
    substantive_relation_distribution: Dict[str, int]
    authenticity_distribution: Dict[str, int]
    missing_provenance_count: int
    contradicted_count: int
    temporal_mismatch_count: int
    unsupported_dependencies_count: int
    quarantined_scaffold_count: int
    is_audit_passed: bool
    diagnostic_details: List[str] = field(default_factory=list)
    propositions: List[LegalPropositionProvenance] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "total_propositions": self.total_propositions,
            "fully_provenanced_propositions": self.fully_provenanced_propositions,
            "unprovenanced_propositions": self.unprovenanced_propositions,
            "state_distribution": self.state_distribution,
            "substantive_relation_distribution": self.substantive_relation_distribution,
            "authenticity_distribution": self.authenticity_distribution,
            "missing_provenance_count": self.missing_provenance_count,
            "contradicted_count": self.contradicted_count,
            "temporal_mismatch_count": self.temporal_mismatch_count,
            "unsupported_dependencies_count": self.unsupported_dependencies_count,
            "quarantined_scaffold_count": self.quarantined_scaffold_count,
            "is_audit_passed": self.is_audit_passed,
            "diagnostic_details": self.diagnostic_details,
            "propositions": [p.to_dict() for p in self.propositions],
        }


class PropositionProvenanceAuditor:
    """
    Audits propositions to ensure complete, auditable provenance across all 12 evidence states.
    Prevents Boolean collapse and validates evidence consistency.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.getcwd(), "data", "legalmitra_kb.db")

    def audit_proposition(self, prop: LegalPropositionProvenance) -> Tuple[bool, List[str]]:
        """
        Validates internal consistency and sequential prerequisite satisfaction across evidence states.
        """
        issues: List[str] = []

        # 0. Cryptographic Integrity Check
        if hasattr(prop, "verify_hash_integrity"):
            hash_valid, hash_msg = prop.verify_hash_integrity()
            if not hash_valid:
                issues.append(f"Proposition {prop.proposition_id}: {hash_msg}")

        # 0. Cryptographic Integrity Check
        if hasattr(prop, "verify_hash_integrity"):
            hash_valid, hash_msg = prop.verify_hash_integrity()
            if not hash_valid:
                issues.append(f"Proposition {prop.proposition_id}: {hash_msg}")

        # 1. Quarantined Scaffold Check
        if (
            "IND-JUD-DEL-2024-BAIL" in prop.source_id
            or "IND-JUD-DEL-2024-BAIL" in prop.authority_title
            or "synthetic" in prop.source_id.lower()
        ):
            prop.authenticity_status = AuthenticityStatus.SYNTHETIC_QUARANTINED
            issues.append(f"Proposition {prop.proposition_id}: Illegally derives from quarantined synthetic scaffold.")

        # 1b. Unauthorized Promotion to ADVOCATE_REVIEWED
        if (
            EvidenceLifecycleState.ADVOCATE_REVIEWED in prop.evidence_states
            or prop.highest_verified_state == EvidenceLifecycleState.ADVOCATE_REVIEWED
        ):
            # Must have verifiable advocate enrollment record
            has_adv_notes = bool(prop.review_notes and any(k in prop.review_notes.lower() for k in ["advocate", "enrollment", "bar council", "adv-"]))
            if not has_adv_notes:
                issues.append(
                    f"Proposition {prop.proposition_id}: Unauthorized promotion to ADVOCATE_REVIEWED without recorded advocate credentials."
                )

        # 1b. Unauthorized Promotion to ADVOCATE_REVIEWED
        if (
            EvidenceLifecycleState.ADVOCATE_REVIEWED in prop.evidence_states
            or prop.highest_verified_state == EvidenceLifecycleState.ADVOCATE_REVIEWED
        ):
            # Must have verifiable advocate enrollment record
            has_adv_notes = bool(prop.review_notes and any(k in prop.review_notes.lower() for k in ["advocate", "enrollment", "bar council", "adv-"]))
            if not has_adv_notes:
                issues.append(
                    f"Proposition {prop.proposition_id}: Unauthorized promotion to ADVOCATE_REVIEWED without recorded advocate credentials."
                )

        # 2. Sequential Evidence State Satisfaction Check
        # To reach SUBSTANTIVELY_SUPPORTS, must have PASSAGE_RETRIEVABLE and SOURCE_AUTHENTICITY_VERIFIED
        has_passage = EvidenceLifecycleState.PASSAGE_RETRIEVABLE in prop.evidence_states
        has_auth = EvidenceLifecycleState.SOURCE_AUTHENTICITY_VERIFIED in prop.evidence_states
        has_temp = EvidenceLifecycleState.TEMPORALLY_APPLICABLE in prop.evidence_states
        has_support = EvidenceLifecycleState.SUBSTANTIVELY_SUPPORTS in prop.evidence_states

        if has_support and not (has_passage and has_auth):
            issues.append(f"Proposition {prop.proposition_id}: Claims substantive support without verified passage retrieval or authenticity.")

        if has_support and not has_temp:
            issues.append(f"Proposition {prop.proposition_id}: Claims substantive support while temporally inapplicable.")

        # 3. Contradiction Alignment
        if prop.substantive_relation == SubstantiveRelation.CONTRADICTS and has_support:
            issues.append(f"Proposition {prop.proposition_id}: States contradictory substantive relation yet claims SUBSTANTIVELY_SUPPORTS.")

        # 4. Pinpoint reference presence
        if not prop.pinpoint_reference or prop.pinpoint_reference.strip() == "":
            issues.append(f"Proposition {prop.proposition_id}: Missing pinpoint provision/paragraph reference.")

        # 5. Dependency check
        if prop.prerequisite_dependencies and not prop.dependencies_satisfied:
            if prop.substantive_relation == SubstantiveRelation.SUPPORTS:
                issues.append(f"Proposition {prop.proposition_id}: Downstream proposition affirmed unconditionally despite failed prerequisites.")

        is_valid = len(issues) == 0
        return is_valid, issues

    def audit_propositions(self, propositions: List[LegalPropositionProvenance]) -> ProvenanceAuditReport:
        """Audits a batch of propositions and returns a comprehensive report."""
        audit_id = f"PROV-AUDIT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        state_dist: Dict[str, int] = {s.value: 0 for s in EvidenceLifecycleState}
        sub_dist: Dict[str, int] = {r.value: 0 for r in SubstantiveRelation}
        auth_dist: Dict[str, int] = {a.value: 0 for a in AuthenticityStatus}

        missing_prov = 0
        contradicted = 0
        temporal_mismatch = 0
        unsupported_deps = 0
        quarantined = 0
        all_diagnostics: List[str] = []

        for p in propositions:
            # Update distributions
            for s in p.evidence_states:
                state_dist[s.value] = state_dist.get(s.value, 0) + 1
            sub_dist[p.substantive_relation.value] = sub_dist.get(p.substantive_relation.value, 0) + 1
            auth_dist[p.authenticity_status.value] = auth_dist.get(p.authenticity_status.value, 0) + 1

            valid, issues = self.audit_proposition(p)
            all_diagnostics.extend(issues)

            if not valid:
                missing_prov += 1
            if p.substantive_relation == SubstantiveRelation.CONTRADICTS:
                contradicted += 1
            if not p.temporal_applicability:
                temporal_mismatch += 1
            if p.prerequisite_dependencies and not p.dependencies_satisfied:
                unsupported_deps += 1
            if p.authenticity_status == AuthenticityStatus.SYNTHETIC_QUARANTINED:
                quarantined += 1

        total = len(propositions)
        passed = (missing_prov == 0 and quarantined == 0)

        return ProvenanceAuditReport(
            audit_id=audit_id,
            total_propositions=total,
            fully_provenanced_propositions=total - missing_prov,
            unprovenanced_propositions=missing_prov,
            state_distribution=state_dist,
            substantive_relation_distribution=sub_dist,
            authenticity_distribution=auth_dist,
            missing_provenance_count=missing_prov,
            contradicted_count=contradicted,
            temporal_mismatch_count=temporal_mismatch,
            unsupported_dependencies_count=unsupported_deps,
            quarantined_scaffold_count=quarantined,
            is_audit_passed=passed,
            diagnostic_details=all_diagnostics,
            propositions=propositions,
        )
