"""
LegalMitra Temporal Law Validator
Validates legal commencement status, temporal consistency, and date-dependent claims
against authoritative Gazette notifications (e.g. G.S.R. 843(E), S.O. 848(E), S.O. 849(E)).
"""

from datetime import date
import re
from typing import List, Optional, Tuple

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
    TemporalValidationStatus,
)
from legalmitra.schemas.legal_qa import LegalQADocument


class TemporalValidator:
    """
    Audits and validates that legal assertions in question-answer pairs
    accurately reflect the commencement and operational status of cited statutes
    as of a designated legal-as-of date.
    """

    # DPDP Act Phased Commencement Dates under G.S.R. 843(E) dt. 13 November 2025
    DPDP_GROUP_1_DATE = date(2025, 11, 13)
    DPDP_GROUP_2_DATE = date(2026, 11, 13)  # One year from 13 Nov 2025
    DPDP_GROUP_3_DATE = date(2027, 5, 13)   # 18 months from 13 Nov 2025 (s.9 General Clauses Act)

    # Criminal Laws Appointed Date under S.O. 848(E), S.O. 849(E), S.O. 850(E) dt. 24 Feb 2024
    NEW_CRIMINAL_LAWS_DATE = date(2024, 7, 1)

    # IT Act Commencement Date
    IT_ACT_COMMENCEMENT_DATE = date(2000, 10, 17)
    IT_ACT_SEC43A_INSERTION_DATE = date(2009, 10, 27)

    @classmethod
    def get_dpdp_commencement_date(cls, section_str: str) -> Tuple[date, str]:
        """
        Returns (commencement_date, grouping_description) for a specific DPDP provision
        pursuant to Notification G.S.R. 843(E) dated 13 November 2025.
        """
        sec = section_str.strip().lower()

        # Group 2: s. 6(9) and s. 27(1)(d)
        if "6(9)" in sec or "section 6(9)" in sec:
            return cls.DPDP_GROUP_2_DATE, "Group 2: 1 year from publication (13 Nov 2026) under G.S.R. 843(E)"
        if "27(1)(d)" in sec or "27(1)(d)" in sec:
            return cls.DPDP_GROUP_2_DATE, "Group 2: 1 year from publication (13 Nov 2026) under G.S.R. 843(E)"

        # Group 1: ss. 2, 18-26, 35-43, 44(1), 44(3)
        if "44(1)" in sec or "44(3)" in sec:
            return cls.DPDP_GROUP_1_DATE, "Group 1: Date of publication (13 Nov 2025) under G.S.R. 843(E)"
        if "44(2)" in sec:
            return cls.DPDP_GROUP_3_DATE, "Group 3: 18 months from publication (13 May 2027) under G.S.R. 843(E)"

        match = re.search(r"\b(?:section\s+|s\.\s*)?(\d+)", sec)
        if match:
            num = int(match.group(1))
            if num in (36, 37):
                return cls.DPDP_GROUP_3_DATE, "Group 3: 18 months from publication (13 May 2027) under G.S.R. 843(E)"
            if num == 2 or (18 <= num <= 26) or (35 <= num <= 43):
                return cls.DPDP_GROUP_1_DATE, "Group 1: Date of publication (13 Nov 2025) under G.S.R. 843(E)"
            if (3 <= num <= 17) or num == 27 or (28 <= num <= 34):
                return cls.DPDP_GROUP_3_DATE, "Group 3: 18 months from publication (13 May 2027) under G.S.R. 843(E)"

        # Schedule follows Section 33 penalties (Group 3)
        if "schedule" in sec:
            return cls.DPDP_GROUP_3_DATE, "Group 3: 18 months from publication (13 May 2027) under G.S.R. 843(E)"

        # Default to Group 3 for substantive data fiduciary/principal provisions
        return cls.DPDP_GROUP_3_DATE, "Group 3: 18 months from publication (13 May 2027) under G.S.R. 843(E)"

    def validate_temporal_claims(
        self,
        qa_doc: LegalQADocument,
        default_as_of_date: Optional[date] = None,
    ) -> Tuple[bool, List[str]]:
        """
        Validates the temporal consistency of a LegalQADocument.
        Ensures uncommenced provisions are never presented as currently operative rights or duties.
        """
        issues = []
        as_of_date = qa_doc.legal_as_of_date or default_as_of_date or date(2026, 10, 16)

        # Check DPDP Act provisions
        if any("DPDP" in s_id for s_id in qa_doc.supporting_source_ids):
            # Identify which sections are cited
            citations = qa_doc.statutory_citations or []
            combined_text = (qa_doc.question + " " + qa_doc.answer).lower()

            for cit in citations:
                if "digital personal data protection" in cit.lower() or "dpdp" in cit.lower():
                    comm_date, group_desc = self.get_dpdp_commencement_date(cit)

                    # Check if evaluation date precedes commencement
                    if as_of_date < comm_date:
                        # Provision is not yet in force on as_of_date
                        if qa_doc.law_status_label == LawStatusLabel.IN_FORCE:
                            issues.append(
                                f"Provision in '{cit}' is labeled 'in_force', but its commencement date is "
                                f"{comm_date.isoformat()} ({group_desc}), which is after legal_as_of_date {as_of_date.isoformat()}."
                            )

                        if qa_doc.provision_commencement_status == ProvisionCommencementStatus.COMMENCED:
                            issues.append(
                                f"Provision '{cit}' has commencement status 'commenced', but does not commence until {comm_date.isoformat()}."
                            )

                        # Check answer text: Must acknowledge uncommenced / future commencement status
                        # Reject answers that state it is currently in force or currently operative
                        has_commencement_notice = (
                            "commence" in combined_text
                            or "13 may 2027" in combined_text
                            or "not yet in force" in combined_text
                            or "enacted" in combined_text
                            or "uncommenced" in combined_text
                            or "scheduled" in combined_text
                            or "g.s.r. 843(e)" in combined_text
                        )
                        if not has_commencement_notice:
                            issues.append(
                                f"Answer presents uncommenced provision '{cit}' (effective {comm_date.isoformat()}) "
                                f"without noting its enacted/future-commencement status as of {as_of_date.isoformat()}."
                            )

        # Check Section 43A Information Technology Act, 2000
        if any("IT-2000" in s_id for s_id in qa_doc.supporting_source_ids) and "43a" in (qa_doc.question + qa_doc.answer).lower():
            if as_of_date < self.DPDP_GROUP_3_DATE:
                # Prior to 13 May 2027, Section 43A is operative
                if "repealed" in qa_doc.answer.lower() and "not yet" not in qa_doc.answer.lower() and "until" not in qa_doc.answer.lower():
                    issues.append(
                        f"Answer claims IT Act Section 43A is repealed/omitted as of {as_of_date.isoformat()}, "
                        f"but DPDP Act Section 44(2) does not take effect until {self.DPDP_GROUP_3_DATE.isoformat()}."
                    )

        # Check BNSS 2023 provisions
        if any("BNSS" in s_id for s_id in qa_doc.supporting_source_ids):
            if as_of_date < self.NEW_CRIMINAL_LAWS_DATE:
                if qa_doc.law_status_label == LawStatusLabel.IN_FORCE:
                    issues.append(
                        f"BNSS provisions cited as in_force as of {as_of_date.isoformat()}, "
                        f"but BNSS commenced on {self.NEW_CRIMINAL_LAWS_DATE.isoformat()} under S.O. 848(E)."
                    )
            else:
                # BNSS 2023 commenced on 1 July 2024. A provision of BNSS (such as Section 531) is an in-force provision
                # of a contemporary statute. Its own provision status cannot be marked REPEALED or REPEALED_WITH_SAVINGS.
                if qa_doc.law_status_label in (LawStatusLabel.REPEALED, LawStatusLabel.REPEALED_WITH_SAVINGS) or qa_doc.provision_commencement_status == ProvisionCommencementStatus.REPEALED:
                    issues.append(
                        f"Provision of BNSS 2023 cannot be labeled 'repealed' or 'repealed_with_savings'. "
                        f"BNSS 2023 is in force; the repeal-with-savings status belongs to the prior enactment (CrPC 1973), "
                        f"which should be designated in 'repealed_statute_status'."
                    )

        is_valid = len(issues) == 0
        if not is_valid:
            qa_doc.temporal_validation_status = TemporalValidationStatus.TEMPORAL_MISMATCH_DETECTED
        else:
            if qa_doc.law_status_label == LawStatusLabel.ENACTED_NOT_YET_IN_FORCE:
                qa_doc.temporal_validation_status = TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT
            elif qa_doc.repealed_statute_status == LawStatusLabel.REPEALED_WITH_SAVINGS or "savings" in (qa_doc.question + qa_doc.answer).lower():
                qa_doc.temporal_validation_status = TemporalValidationStatus.VERIFIED_HISTORICAL_SAVINGS
            else:
                qa_doc.temporal_validation_status = TemporalValidationStatus.VERIFIED_CURRENT

        return is_valid, issues
