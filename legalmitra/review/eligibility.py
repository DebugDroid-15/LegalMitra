"""
LegalMitra Dataset Eligibility & Boundary Protection Subsystem
Enforces strict boundary controls ensuring that:
1. Only genuine advocate-approved records with complete reviewer attribution can be exported for training.
2. Holdout evaluation benchmarks (including the frozen Phase 9 pilot) can never leak into training splits.
3. Quarantined synthetic scaffolds (IND-JUD-DEL-2024-BAIL) are 100% excluded.
4. Pending, rejected, revision-required, and unverified records are barred from training exports.
"""

from typing import Any, Dict, List, Optional, Set, Tuple

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.schemas.legal_qa import LegalQADocument


class DatasetEligibilityFilter:
    """
    Enforces training-eligibility policies and prevents partition leakage.
    """

    KNOWN_QUARANTINED_IDS: Set[str] = {
        "IND-JUD-DEL-2024-BAIL",
        "PROC-BNSS-482-BAIL-001",
    }

    # Pilot 20 records are permanently designated as the primary blind holdout evaluation benchmark
    FROZEN_PILOT_HOLDOUT_IDS: Set[str] = {
        f"QA-PILOT-DPDP-{i:03d}" for i in range(1, 11)
    } | {
        f"QA-PILOT-CROSS-{i:03d}" for i in range(1, 11)
    }

    def __init__(self, additional_holdout_ids: Optional[Set[str]] = None):
        self.holdout_ids = set(self.FROZEN_PILOT_HOLDOUT_IDS)
        if additional_holdout_ids:
            self.holdout_ids.update(additional_holdout_ids)

    def evaluate_record_eligibility(
        self,
        doc: LegalQADocument,
    ) -> Tuple[bool, List[str]]:
        """
        Evaluates a single LegalQADocument for training partition eligibility.
        Returns: (is_eligible, list_of_ineligibility_reasons)
        """
        reasons: List[str] = []

        # 1. Review Status Check: Must be strictly LEGAL_EXPERT_APPROVED
        if doc.legal_review_status != LegalReviewStatus.LEGAL_EXPERT_APPROVED:
            reasons.append(
                f"Record has review status '{doc.legal_review_status.value}'; "
                f"only '{LegalReviewStatus.LEGAL_EXPERT_APPROVED.value}' records are eligible for model training."
            )

        # 2. Holdout Evaluation Partition Leakage Protection
        if doc.qa_id in self.holdout_ids:
            reasons.append(
                f"Record '{doc.qa_id}' belongs to the permanent blind holdout evaluation partition "
                f"and cannot be exported into any training split (strict leakage protection)."
            )

        # 3. Quarantine Exclusion Check
        for s_id in doc.supporting_source_ids:
            if s_id in self.KNOWN_QUARANTINED_IDS:
                reasons.append(f"Record relies on quarantined source ID '{s_id}'.")

        for passage in doc.evidence_passages:
            if passage.source_id in self.KNOWN_QUARANTINED_IDS:
                reasons.append(f"Evidence passage references quarantined source '{passage.source_id}'.")

        combined_text = f"{doc.question} {doc.answer}".lower()
        if "rahul kumar" in combined_text or "ind-jud-del-2024-bail" in combined_text:
            reasons.append("Record contains references to quarantined synthetic scaffold (Rahul Kumar / IND-JUD-DEL-2024-BAIL).")

        # 4. Reviewer Attribution Check
        if doc.legal_review_status == LegalReviewStatus.LEGAL_EXPERT_APPROVED:
            if not doc.reviewer_name_initials or not doc.reviewer_name_initials.strip():
                reasons.append("Approved record lacks mandatory reviewer name/initials attribution.")
            if not doc.review_date:
                reasons.append("Approved record lacks mandatory review date attribution.")

        # 5. Evidence & Citations Completeness
        if not doc.evidence_passages:
            reasons.append("Record contains no evidence passages.")
        if not doc.statutory_citations:
            reasons.append("Record contains no statutory citations.")

        is_eligible = len(reasons) == 0
        return is_eligible, reasons

    def filter_training_dataset(
        self,
        docs: List[LegalQADocument],
    ) -> Tuple[List[LegalQADocument], Dict[str, Any]]:
        """
        Filters a collection of LegalQADocument objects, returning only training-eligible records
        and a detailed audit breakdown of rejected items.
        """
        eligible_records: List[LegalQADocument] = []
        ineligible_reasons: Dict[str, List[str]] = {}

        for doc in docs:
            is_eligible, reasons = self.evaluate_record_eligibility(doc)
            if is_eligible:
                eligible_records.append(doc)
            else:
                ineligible_reasons[doc.qa_id] = reasons

        summary = {
            "total_evaluated": len(docs),
            "eligible_for_training_count": len(eligible_records),
            "ineligible_count": len(ineligible_reasons),
            "reasons_by_record": ineligible_reasons,
        }

        return eligible_records, summary

