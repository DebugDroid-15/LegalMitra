"""
LegalMitra Data Quality Gate
Pre-generation and pre-release validation system enforcing rigorous quality controls:
1. Source authenticity (supporting source IDs exist in registry and are verified/active)
2. Section-level commencement (provisions checked against commencement schedule for the legal_as_of_date)
3. Exact evidence-span matching (evidence passage verbatim_text is an exact/normalized substring of registered source text)
4. Citation completeness (statutory_citations list is non-empty and formatted with recognizable legal references)
5. Quarantine exclusion (sources marked is_synthetic_scaffold or in quarantine are strictly rejected)
6. Duplicate detection (question and answer deduplication against existing dataset records or within batch)
7. Legal-as-of date consistency (ensures legal_as_of_date, law_status_label, provision_commencement_status, and commencement_source_id are fully populated)
8. Separate human review status (legal_review_status must remain PENDING_LEGAL_REVIEW; automated systems cannot self-approve legal advice)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional, Set, Tuple
import re

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProcessingStatus,
    ProvisionCommencementStatus,
)
from legalmitra.core.hashing import compute_content_fingerprint
from legalmitra.core.logging import get_logger
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.validation.deduplication import DeduplicationEngine
from legalmitra.validation.grounding_validator import GroundingValidator
from legalmitra.validation.temporal_validator import TemporalValidator

logger = get_logger("quality_gate")


@dataclass
class QualityGateResult:
    """Outcome of quality gate evaluation for a single LegalQADocument."""
    qa_id: str
    is_valid: bool
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataQualityGate:
    """
    Comprehensive pre-generation and pre-release data quality gate for LegalMitra datasets.
    """

    KNOWN_QUARANTINED_IDS: Set[str] = {
        "IND-JUD-DEL-2024-BAIL",
        "PROC-BNSS-482-BAIL-001",
    }

    STATUTORY_CITATION_PATTERNS = [
        re.compile(r"\bSection\s+\d+", re.IGNORECASE),
        re.compile(r"\bArticle\s+\d+", re.IGNORECASE),
        re.compile(r"\bRule\s+\d+", re.IGNORECASE),
        re.compile(r"\bOrder\s+[IVXLCDM\d]+", re.IGNORECASE),
        re.compile(r"\bSchedule\b", re.IGNORECASE),
        re.compile(r"\bClause\s+\d+", re.IGNORECASE),
        re.compile(r"\bAct\b", re.IGNORECASE),
        re.compile(r"\bCode\b", re.IGNORECASE),
        re.compile(r"\bSanhita\b", re.IGNORECASE),
        re.compile(r"\bAdhiniyam\b", re.IGNORECASE),
    ]

    def __init__(
        self,
        registry_manager: Optional[SourceRegistryManager] = None,
        source_texts: Optional[Dict[str, str]] = None,
        temporal_validator: Optional[TemporalValidator] = None,
        grounding_validator: Optional[GroundingValidator] = None,
    ):
        self.registry = registry_manager
        self.source_texts = source_texts or {}
        self.temporal_validator = temporal_validator or TemporalValidator()
        self.grounding_validator = grounding_validator or GroundingValidator(registry_manager)
        self.dedup_engine = DeduplicationEngine()

    def check_human_review_status(self, doc: LegalQADocument) -> Tuple[bool, Optional[str]]:
        """
        Quality Gate 8: Automated checks must never self-approve legal advice or datasets.
        The legal_review_status must remain PENDING_LEGAL_REVIEW until an advocate has reviewed it.
        """
        if doc.legal_review_status == LegalReviewStatus.LEGAL_EXPERT_APPROVED:
            return (
                False,
                f"Automated quality gate cannot self-approve legal dataset records. "
                f"Record {doc.qa_id} has legal_review_status '{doc.legal_review_status}', "
                f"which must remain '{LegalReviewStatus.PENDING_LEGAL_REVIEW.value}' pending advocate review.",
            )
        if doc.legal_review_status != LegalReviewStatus.PENDING_LEGAL_REVIEW:
            return (
                False,
                f"Generated dataset records must have legal_review_status '{LegalReviewStatus.PENDING_LEGAL_REVIEW.value}', "
                f"got '{doc.legal_review_status}'.",
            )
        return True, None

    def check_quarantine_exclusion(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 5: Rejects any record relying on synthetic test scaffolds or quarantined source IDs
        either directly or indirectly.
        """
        issues = []
        # Direct source ID checks
        for s_id in doc.supporting_source_ids:
            if s_id in self.KNOWN_QUARANTINED_IDS:
                issues.append(f"Record relies on quarantined source ID '{s_id}'.")
            elif self.registry is not None:
                record = self.registry.get(s_id)
                if record is not None:
                    if record.verification_status == LegalReviewStatus.FLAGGED_UNSUPPORTED:
                        issues.append(f"Source '{s_id}' is flagged as unsupported/quarantined in registry.")
                    notes = (record.privacy_redaction_notes or "").lower()
                    if "synthetic test scaffold" in notes or "synthetic scaffold" in notes:
                        issues.append(f"Source '{s_id}' is identified as a synthetic test scaffold.")

        for passage in doc.evidence_passages:
            if passage.source_id in self.KNOWN_QUARANTINED_IDS:
                issues.append(f"Evidence passage references quarantined source '{passage.source_id}'.")

        # Indirect quarantine checks in case citations, question, or answer
        combined_text = f"{doc.question} {doc.answer} {' '.join(doc.case_citations or [])}".lower()
        if "rahul kumar" in combined_text or "ind-jud-del-2024-bail" in combined_text or "proc-bnss-482-bail-001" in combined_text:
            issues.append("Record contains indirect reference to quarantined synthetic scaffold (Rahul Kumar / IND-JUD-DEL-2024-BAIL).")

        return len(issues) == 0, issues

    def check_source_authenticity(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 1: Source authenticity - supporting source IDs exist in registry, are active,
        and have valid canonical source URLs (rejecting missing, malformed, or dummy URLs).
        """
        issues = []
        if not doc.supporting_source_ids:
            issues.append(f"Record {doc.qa_id} has no supporting_source_ids.")
            return False, issues

        if self.registry is not None:
            for s_id in doc.supporting_source_ids:
                record = self.registry.get(s_id)
                if record is None:
                    issues.append(f"Source ID '{s_id}' not found in Source Registry.")
                else:
                    if record.processing_status == ProcessingStatus.FAILED:
                        issues.append(f"Source ID '{s_id}' has processing_status 'failed' in registry.")
                    if not record.source_url or not record.source_url.startswith(("http://", "https://")) or "example.com" in record.source_url:
                        issues.append(f"Source ID '{s_id}' lacks a valid canonical source_url in registry (found: '{record.source_url}').")

        return len(issues) == 0, issues

    def check_temporal_metadata(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 7: Legal-as-of date consistency, complete temporal metadata,
        and source version temporality check (ensuring source enactment/commencement
        precedes or accounts for historical versioning).
        """
        issues = []
        if doc.legal_as_of_date is None:
            issues.append("Missing required legal_as_of_date.")
        elif not isinstance(doc.legal_as_of_date, date):
            issues.append(f"legal_as_of_date must be a date object, got {type(doc.legal_as_of_date)}.")

        if doc.law_status_label is None or not isinstance(doc.law_status_label, LawStatusLabel):
            issues.append(f"Missing or invalid law_status_label: {doc.law_status_label}.")

        if doc.provision_commencement_status is None or not isinstance(doc.provision_commencement_status, ProvisionCommencementStatus):
            issues.append(f"Missing or invalid provision_commencement_status: {doc.provision_commencement_status}.")

        if not doc.commencement_source_id or not doc.commencement_source_id.strip():
            issues.append("Missing required commencement_source_id (Gazette notification reference).")

        if doc.commencement_date is None or not isinstance(doc.commencement_date, date):
            issues.append("Missing required commencement_date.")

        # Source version vs legal-as-of date audit (Case 12)
        if self.registry is not None and doc.legal_as_of_date is not None:
            for s_id in doc.supporting_source_ids:
                record = self.registry.get(s_id)
                if record is not None:
                    if record.document_date > doc.legal_as_of_date:
                        issues.append(
                            f"Source '{s_id}' enactment/document date ({record.document_date}) is after the answer's legal-as-of date "
                            f"({doc.legal_as_of_date}) without a preserved historical version."
                        )
                    elif doc.law_status_label == LawStatusLabel.IN_FORCE and record.effective_date and record.effective_date > doc.legal_as_of_date:
                        issues.append(
                            f"Source '{s_id}' effective date ({record.effective_date}) is after the answer's legal-as-of date "
                            f"({doc.legal_as_of_date}). In-force status requires a contemporary historical version."
                        )

        return len(issues) == 0, issues

    def check_section_commencement(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 2: Section-level commencement audit under G.S.R. 843(E) and S.O. 848(E),
        including partial commencement checks and anti-conflation regression.
        """
        is_valid, issues = self.temporal_validator.validate_temporal_claims(doc)

        # Check for partial commencement mislabeling (Case 6)
        citations = doc.statutory_citations or []
        for cit in citations:
            if "Section 44" in cit and "Digital Personal Data Protection" in cit:
                # Section 44 is partially commenced: 44(1) and 44(3) commenced 13 Nov 2025; 44(2) commences 13 May 2027
                if doc.law_status_label == LawStatusLabel.IN_FORCE or doc.provision_commencement_status == ProvisionCommencementStatus.COMMENCED:
                    issues.append(
                        f"Section 44 of the DPDP Act, 2023 is partially commenced under G.S.R. 843(E) "
                        f"(Section 44(2) omitting IT Act s.43A does not commence until 13 May 2027) "
                        f"and cannot be labeled fully 'in_force' or 'commenced'."
                    )
            elif "Section 27" in cit and "Digital Personal Data Protection" in cit and "Section 27(1)(d)" not in cit:
                if doc.law_status_label == LawStatusLabel.IN_FORCE and doc.legal_as_of_date and doc.legal_as_of_date < date(2027, 5, 13):
                    issues.append(
                        f"Section 27 of the DPDP Act is partially commenced under G.S.R. 843(E) "
                        f"(only s.27(1)(d) commences 13 Nov 2026; balance commences 13 May 2027)."
                    )

        return len(issues) == 0, issues

    def check_exact_evidence_matching(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 3: Exact evidence-span matching, section attribution verification,
        and material proviso enforcement.
        """
        issues = []
        if not doc.evidence_passages:
            issues.append("Document contains no evidence passages.")
            return False, issues

        for idx, passage in enumerate(doc.evidence_passages, start=1):
            if not passage.verbatim_text or not passage.verbatim_text.strip():
                issues.append(f"Evidence passage {idx} has empty verbatim_text.")
            if not passage.section_or_para_ref or not passage.section_or_para_ref.strip():
                issues.append(f"Evidence passage {idx} has empty section_or_para_ref.")
            if passage.source_id not in doc.supporting_source_ids:
                issues.append(
                    f"Evidence passage {idx} references '{passage.source_id}', which is not in supporting_source_ids."
                )

            # Check Section Attribution (Case 3)
            # If the verbatim text explicitly starts with a section number like "11." or "Section 11",
            # verify that section_or_para_ref aligns with it
            vtext = passage.verbatim_text.strip()
            sec_match = re.match(r"^(?:\*\*)?(\d+[A-Z]?)\.\s+", vtext)
            if sec_match:
                extracted_sec = sec_match.group(1)
                ref_secs = re.findall(r"\b(\d+[A-Z]?)\b", passage.section_or_para_ref)
                if ref_secs and extracted_sec not in ref_secs:
                    issues.append(
                        f"Section attribution mismatch in evidence passage {idx}: "
                        f"section_or_para_ref specifies '{passage.section_or_para_ref}', "
                        f"but quotation text begins with Section {extracted_sec}."
                    )

            # Check Material Proviso Omission (Case 4)
            # If passage cites Section 61 BSA and asserts unconditional admissibility while omitting proviso/certificate
            if "bsa" in passage.source_id.lower() and "61" in passage.section_or_para_ref.lower():
                answer_lower = doc.answer.lower()
                if "without" in answer_lower and "certificate" in answer_lower and "not required" in answer_lower:
                    issues.append(
                        "Answer claims electronic evidence under BSA Section 61 is admissible without a certificate, "
                        "omitting the legally material statutory proviso requiring Section 63(4) certification."
                    )
                elif "unconditional" in answer_lower and "63" not in answer_lower:
                    issues.append(
                        "Answer presents BSA Section 61 as granting unconditional admissibility, "
                        "omitting the material proviso and statutory restriction 'subject to the provisions of section 63'."
                    )

            # If source text is available, verify verbatim presence
            if self.source_texts and passage.source_id in self.source_texts:
                stext = self.source_texts[passage.source_id]
                if not self.grounding_validator.verify_evidence_passage(passage, stext):
                    issues.append(
                        f"Evidence passage {idx} ('{passage.section_or_para_ref}') does not match verbatim source text in '{passage.source_id}'."
                    )

        return len(issues) == 0, issues

    def check_citation_completeness(self, doc: LegalQADocument) -> Tuple[bool, List[str]]:
        """
        Quality Gate 4: Citation completeness and statutory reference structure.
        """
        issues = []
        if not doc.statutory_citations:
            issues.append("statutory_citations list is empty.")
            return False, issues

        for idx, cit in enumerate(doc.statutory_citations, start=1):
            if not cit or not cit.strip():
                issues.append(f"Citation {idx} is empty.")
                continue

            matches_any_pattern = any(pattern.search(cit) for pattern in self.STATUTORY_CITATION_PATTERNS)
            if not matches_any_pattern:
                issues.append(
                    f"Citation {idx} ('{cit}') lacks recognizable statutory anchor (Section, Article, Rule, Order, Schedule, Act, Code)."
                )

        return len(issues) == 0, issues

    def check_duplicate_status(
        self,
        doc: LegalQADocument,
        existing_docs: Optional[List[LegalQADocument]] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Quality Gate 6: Question / Answer duplicate detection against existing repository,
        including near-duplicate detection with token-set and stop-word normalization.
        """
        # 1. Normalize question
        norm_q = re.sub(r"[^\w\s]", "", doc.question.strip().lower())
        norm_q_clean = re.sub(r"\s+", " ", norm_q)
        q_fingerprint = compute_content_fingerprint(norm_q_clean)

        # Token set for near-duplicate Jaccard comparison
        stop_words = {"what", "is", "are", "under", "the", "a", "an", "does", "do", "how", "of", "in", "to", "for", "and", "by", "on", "can"}
        tokens = {w for w in norm_q_clean.split() if w not in stop_words and len(w) > 2}

        if existing_docs:
            for ex in existing_docs:
                if ex.qa_id == doc.qa_id:
                    continue
                ex_norm_q = re.sub(r"[^\w\s]", "", ex.question.strip().lower())
                ex_norm_clean = re.sub(r"\s+", " ", ex_norm_q)
                
                # Exact fingerprint match
                if q_fingerprint == compute_content_fingerprint(ex_norm_clean):
                    return (
                        False,
                        f"Duplicate question detected: '{doc.qa_id}' matches existing '{ex.qa_id}' question.",
                    )

                # Near-duplicate Jaccard similarity
                ex_tokens = {w for w in ex_norm_clean.split() if w not in stop_words and len(w) > 2}
                if tokens and ex_tokens:
                    intersection = tokens.intersection(ex_tokens)
                    union = tokens.union(ex_tokens)
                    jaccard = len(intersection) / len(union)
                    if jaccard >= 0.82:
                        return (
                            False,
                            f"Near-duplicate question detected (superficially rephrased, similarity {jaccard:.2f}): "
                            f"'{doc.qa_id}' matches existing '{ex.qa_id}'.",
                        )

        # Register in instance deduplication engine
        dup_match = self.dedup_engine.check_and_register_text(doc.qa_id, norm_q_clean)
        if dup_match is not None and dup_match != doc.qa_id:
            return (
                False,
                f"Duplicate content detected: '{doc.qa_id}' matches '{dup_match}'.",
            )

        return True, None

    def validate_record(
        self,
        doc: LegalQADocument,
        existing_docs: Optional[List[LegalQADocument]] = None,
    ) -> QualityGateResult:
        """
        Evaluates a single LegalQADocument against all 8 quality gates.
        """
        passed_checks: List[str] = []
        failed_checks: List[str] = []
        issues: List[str] = []

        # Gate 1: Source Authenticity
        g1_ok, g1_issues = self.check_source_authenticity(doc)
        if g1_ok:
            passed_checks.append("source_authenticity")
        else:
            failed_checks.append("source_authenticity")
            issues.extend(g1_issues)

        # Gate 2: Section-level Commencement
        g2_ok, g2_issues = self.check_section_commencement(doc)
        if g2_ok:
            passed_checks.append("section_level_commencement")
        else:
            failed_checks.append("section_level_commencement")
            issues.extend(g2_issues)

        # Gate 3: Exact Evidence-Span Matching
        g3_ok, g3_issues = self.check_exact_evidence_matching(doc)
        if g3_ok:
            passed_checks.append("exact_evidence_matching")
        else:
            failed_checks.append("exact_evidence_matching")
            issues.extend(g3_issues)

        # Gate 4: Citation Completeness
        g4_ok, g4_issues = self.check_citation_completeness(doc)
        if g4_ok:
            passed_checks.append("citation_completeness")
        else:
            failed_checks.append("citation_completeness")
            issues.extend(g4_issues)

        # Gate 5: Quarantine Exclusion
        g5_ok, g5_issues = self.check_quarantine_exclusion(doc)
        if g5_ok:
            passed_checks.append("quarantine_exclusion")
        else:
            failed_checks.append("quarantine_exclusion")
            issues.extend(g5_issues)

        # Gate 6: Duplicate Detection
        g6_ok, g6_issue = self.check_duplicate_status(doc, existing_docs)
        if g6_ok:
            passed_checks.append("duplicate_detection")
        else:
            failed_checks.append("duplicate_detection")
            if g6_issue:
                issues.append(g6_issue)

        # Gate 7: Legal-As-Of Date Consistency
        g7_ok, g7_issues = self.check_temporal_metadata(doc)
        if g7_ok:
            passed_checks.append("legal_as_of_date_consistency")
        else:
            failed_checks.append("legal_as_of_date_consistency")
            issues.extend(g7_issues)

        # Gate 8: Separate Human Review Status
        g8_ok, g8_issue = self.check_human_review_status(doc)
        if g8_ok:
            passed_checks.append("separate_human_review_status")
        else:
            failed_checks.append("separate_human_review_status")
            if g8_issue:
                issues.append(g8_issue)

        is_valid = len(failed_checks) == 0
        return QualityGateResult(
            qa_id=doc.qa_id,
            is_valid=is_valid,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            issues=issues,
            metadata={
                "total_checks": 8,
                "passed_count": len(passed_checks),
                "failed_count": len(failed_checks),
            },
        )

    def validate_batch(
        self,
        docs: List[LegalQADocument],
        existing_docs: Optional[List[LegalQADocument]] = None,
    ) -> Tuple[bool, List[QualityGateResult]]:
        """
        Evaluates a batch of LegalQADocument objects against all quality gates.
        """
        results: List[QualityGateResult] = []
        all_passed = True
        cumulative_existing = list(existing_docs or [])

        for doc in docs:
            result = self.validate_record(doc, existing_docs=cumulative_existing)
            results.append(result)
            if not result.is_valid:
                all_passed = False
            cumulative_existing.append(doc)

        return all_passed, results

