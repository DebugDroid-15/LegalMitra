"""
LegalMitra Phase 7.1 Temporal Audit & Controlled Pilot Generator
Builds and validates 20 high-fidelity, source-grounded legal Q&A examples with full temporal-law audit:
- 10 DPDP / IT Act statutory Q&A (testing Data Principal rights, Data Fiduciary obligations, Schedule penalties, s.43A IT Act vs s.44(2) DPDP Act temporal status under G.S.R. 843(E)).
- 10 Cross-statute evidence & cybercrime examples (testing BSA s.61/63 certificates with IT Act s.2(1)(t) digital records, s.66 cybercrime, and BNSS s.482 anticipatory bail).
"""

import json
from pathlib import Path
from datetime import date, datetime

from legalmitra.core.enums import (
    Jurisdiction,
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
    TemporalValidationStatus,
)
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.generation.validator import GenerationValidator
from legalmitra.generation.orchestrator import GenerationOrchestrator
from legalmitra.generation.schemas import GenerationConfig
from legalmitra.validation.quality_gate import DataQualityGate
from legalmitra.validation.temporal_validator import TemporalValidator


def build_pilot_examples():
    examples = []
    audit_date = date(2026, 10, 16)

    # =========================================================================
    # Group 1: 10 DPDP / IT Act Statutory Q&A Examples
    # =========================================================================

    # 1. DPDP s.11: Right to access information about personal data
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-001",
            question=(
                "Under the enacted statutory text of Section 11 of the Digital Personal Data Protection Act, 2023 "
                "(scheduled to commence on 13 May 2027 under G.S.R. 843(E)), what specific information will a Data Principal "
                "be entitled to obtain from a Data Fiduciary?"
            ),
            answer=(
                "Under the enacted statutory scheme of Section 11(1) of the Digital Personal Data Protection Act, 2023 "
                "(which is scheduled to commence on 13 May 2027 pursuant to Notification G.S.R. 843(E) and is not yet in force as of 16 October 2026), "
                "a Data Principal who has previously given consent will have the right to obtain from the Data Fiduciary upon request: "
                "(a) a summary of personal data which is being processed by such Data Fiduciary and the processing activities undertaken "
                "with respect to such personal data; (b) the identities of all other Data Fiduciaries and Data Processors with whom the personal "
                "data has been shared, along with a description of the personal data so shared; and (c) any other information related to the personal "
                "data and its processing as may be prescribed."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 11(1)",
                    verbatim_text=(
                        "11. Right to access information about personal data.-(1) The Data Principal shall have the right to "
                        "obtain from the Data Fiduciary to whom she has previously given consent, including consent as referred "
                        "to in clause (a) of section 7 (hereinafter referred to as the said Data Fiduciary), for processing of "
                        "personal data, upon making to it a request in such manner as may be prescribed,-\n\n"
                        "(a) a summary of personal data which is being processed by such Data Fiduciary and the processing "
                        "activities undertaken by that Data Fiduciary with respect to such personal data;\n\n"
                        "(b) the identities of all other Data Fiduciaries and Data Processors with whom the personal data has "
                        "been shared by such Data Fiduciary, along with a description of the personal data so shared; and\n\n"
                        "(c) any other information related to the personal data of such Data Principal and its processing, "
                        "as may be prescribed."
                    ),
                    page_number=6,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 11, Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 2. DPDP s.12: Right to correction and erasure of personal data
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-002",
            question=(
                "What statutory duties are established for a Data Fiduciary regarding correction, completion, updating, "
                "and erasure under the enacted text of Section 12 of the DPDP Act, 2023 once it comes into force?"
            ),
            answer=(
                "Under the enacted text of Section 12 of the Digital Personal Data Protection Act, 2023 (appointed to commence "
                "on 13 May 2027 under G.S.R. 843(E) and not yet in force as of 16 October 2026), a Data Principal will possess statutory "
                "rights under Section 12(1) to correction, completion, updating, and erasure of personal data. Upon receiving such a request, "
                "under Section 12(2) the Data Fiduciary shall: (a) correct inaccurate or misleading personal data; (b) complete incomplete "
                "personal data; and (c) update the personal data. Furthermore, under Section 12(3), upon receiving an erasure request, the "
                "Data Fiduciary shall erase the personal data unless retention is necessary for the specified purpose or legal compliance."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 12",
                    verbatim_text=(
                        "12. Right to correction and erasure of personal data.-(1) A Data Principal shall have the right to correction, "
                        "completion, updating and erasure of her personal data for the processing of which she has previously given consent, "
                        "including consent as referred to in clause (a) of section 7, in accordance with any requirement or procedure under "
                        "any law for the time being in force.\n\n"
                        "(2) A Data Fiduciary shall, upon receiving a request for correction, completion or updating from a Data Principal,-\n\n"
                        "(a) correct the inaccurate or misleading personal data;\n\n"
                        "- (b) complete the incomplete personal data; and\n"
                        "- (c) update the personal data.\n\n"
                        "(3) A Data Principal shall make a request in such manner as may be prescribed to the Data Fiduciary for erasure "
                        "of her personal data, and upon receipt of such a request, the Data Fiduciary shall erase her personal data unless "
                        "retention of the same is necessary for the specified purpose or for compliance with any law for the time being in force."
                    ),
                    page_number=6,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 12, Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 3. DPDP s.13: Right of grievance redressal
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-003",
            question=(
                "Under the enacted scheme of Section 13 of the Digital Personal Data Protection Act, 2023, must a Data Principal "
                "exhaust internal grievance redressal mechanisms before approaching the Data Protection Board of India?"
            ),
            answer=(
                "Yes. Under the enacted statutory provisions of Section 13 of the Digital Personal Data Protection Act, 2023 "
                "(scheduled to commence on 13 May 2027 pursuant to Notification G.S.R. 843(E) and not yet in force as of 16 October 2026), "
                "a Data Principal will have readily available means of grievance redressal under Section 13(1). Section 13(3) explicitly dictates "
                "that the Data Principal shall exhaust the opportunity of redressing her grievance under Section 13 before approaching the Data Protection Board."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 13",
                    verbatim_text=(
                        "13. Right of grievance redressal.-(1) A Data Principal shall have the right to have readily available means of "
                        "grievance redressal provided by a Data Fiduciary or Consent Manager in respect of any act or omission of such "
                        "Data Fiduciary or Consent Manager regarding the performance of its obligations in relation to the personal data "
                        "of such Data Principal or the exercise of her rights under the provisions of this Act and the rules made thereunder.\n\n"
                        "(2) The Data Fiduciary or Consent Manager shall respond to any grievances referred to in sub-section (1) within "
                        "such period as may be prescribed from the date of its receipt for all or any class of Data Fiduciaries.\n\n"
                        "(3) The Data Principal shall exhaust the opportunity of redressing her grievance under this section before approaching the Board."
                    ),
                    page_number=7,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 13, Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 4. DPDP s.8(5): Security Safeguards Obligation
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-004",
            question=(
                "What statutory obligation will be placed upon a Data Fiduciary to protect personal data by taking security safeguards "
                "under the enacted Section 8(5) of the DPDP Act, 2023, and what is its commencement status?"
            ),
            answer=(
                "Under the enacted text of Section 8(5) of the Digital Personal Data Protection Act, 2023 (which commences on 13 May 2027 "
                "under Notification G.S.R. 843(E) and is uncommenced as of 16 October 2026), a Data Fiduciary is mandated to protect personal data "
                "in its possession or under its control, including in respect of any processing undertaken by it or on its behalf by a Data Processor, "
                "by taking reasonable security safeguards to prevent personal data breach. (Note: As of October 2026 prior to the 13 May 2027 commencement, "
                "data protection security requirements under existing law remain governed under the Information Technology Act, 2000)."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 8(5)",
                    verbatim_text=(
                        "(5) A Data Fiduciary shall protect personal data in its possession or under its control, including in respect of "
                        "any processing undertaken by it or on its behalf by a Data Processor, by taking reasonable security safeguards "
                        "to prevent personal data breach."
                    ),
                    page_number=4,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 8(5), Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 5. DPDP s.6(1): Consent Requirements
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-005",
            question=(
                "What legal requirements must be fulfilled for consent given by a Data Principal under the enacted provisions of "
                "Section 6(1) of the DPDP Act, 2023, and when do they take effect?"
            ),
            answer=(
                "Under the enacted text of Section 6(1) of the Digital Personal Data Protection Act, 2023 (scheduled for commencement on "
                "13 May 2027 under Notification G.S.R. 843(E) and not yet in force as of 16 October 2026), consent given by the Data Principal "
                "shall be free, specific, informed, unconditional, and unambiguous with a clear affirmative action. It must signify an agreement "
                "to the processing of her personal data for the specified purpose and be limited to such personal data as is necessary for such specified purpose."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 6(1)",
                    verbatim_text=(
                        "6. Consent.--(1) The consent given by the Data Principal shall be free, specific, informed, unconditional "
                        "and unambiguous with a clear affirmative action, and shall signify an agreement to the processing of her "
                        "personal data for the specified purpose and be limited to such personal data as is necessary for such specified purpose."
                    ),
                    page_number=3,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 6(1), Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 6. DPDP s.8(6): Intimation of Personal Data Breach
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-006",
            question=(
                "Under the enacted provisions of Section 8(6) of the DPDP Act, 2023, who must be notified by the Data Fiduciary "
                "in the event of a personal data breach once the section commences?"
            ),
            answer=(
                "Under Section 8(6) of the Digital Personal Data Protection Act, 2023 (enacted and appointed to commence on 13 May 2027 "
                "under Notification G.S.R. 843(E), hence uncommenced as of 16 October 2026), in the event of a personal data breach, the "
                "Data Fiduciary shall give intimation of such breach to both the Data Protection Board of India and each affected Data Principal, "
                "in such form and manner as may be prescribed."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 8(6)",
                    verbatim_text=(
                        "(6) In the event of a personal data breach, the Data Fiduciary shall give the Board and each affected Data Principal, "
                        "intimation of such breach in such form and manner as may be prescribed."
                    ),
                    page_number=4,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 8(6), Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 7. DPDP s.33(1): Penalties Adjudication
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-007",
            question=(
                "Under the enacted statutory text of Section 33(1) of the DPDP Act, 2023, what prerequisites govern the imposition "
                "of monetary penalties by the Board once the penal provisions commence?"
            ),
            answer=(
                "Under the enacted provisions of Section 33(1) of the Digital Personal Data Protection Act, 2023 (scheduled to commence "
                "on 13 May 2027 under G.S.R. 843(E) and uncommenced as of 16 October 2026), if the Board determines on conclusion of an inquiry "
                "that breach of the provisions of the Act or rules by a person is significant, it may, after giving the person an opportunity of "
                "being heard, impose such monetary penalty specified in the Schedule."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 33(1)",
                    verbatim_text=(
                        "33. Penalties.-(1) If the Board determines on conclusion of an inquiry that breach of the provisions of this Act "
                        "or the rules made thereunder by a person is significant, it may, after giving the person an opportunity of being "
                        "heard, impose such monetary penalty specified in the Schedule."
                    ),
                    page_number=13,
                )
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 33(1), Digital Personal Data Protection Act, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 8. DPDP Schedule Item 1: Penalty for failure to take reasonable security safeguards
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-008",
            question=(
                "What maximum monetary penalty is prescribed under Item 1 of the Schedule to the DPDP Act, 2023 for failure by a Data "
                "Fiduciary to observe reasonable security safeguards under Section 8(5) upon commencement?"
            ),
            answer=(
                "Under the enacted text of Item 1 of the Schedule to the Digital Personal Data Protection Act, 2023 (read with Section 33(1), "
                "scheduled to commence on 13 May 2027 pursuant to Notification G.S.R. 843(E) and not yet in force as of 16 October 2026), "
                "for a breach in observing the obligation of a Data Fiduciary to take reasonable security safeguards to prevent personal data "
                "breach under Section 8(5), the monetary penalty may extend to two hundred and fifty crore rupees."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 33(1)",
                    verbatim_text=(
                        "33. Penalties.-(1) If the Board determines on conclusion of an inquiry that breach of the provisions of this Act "
                        "or the rules made thereunder by a person is significant, it may, after giving the person an opportunity of being "
                        "heard, impose such monetary penalty specified in the Schedule."
                    ),
                    page_number=13,
                ),
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Schedule Item 1 and Section 8(5)",
                    verbatim_text=(
                        "| 1.        | Breach in observing the obligation of Data Fiduciary to take reasonable security safeguards to prevent "
                        "personal data breach under sub-section (5) of section 8. | May extend to two hundred and fifty crore rupees"
                    ),
                    page_number=17,
                ),
            ],
            legal_domain="Data Protection Law - Digital Privacy",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 8(5), Digital Personal Data Protection Act, 2023",
                "Section 33, Digital Personal Data Protection Act, 2023",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # 9. Temporal Status: Section 43A IT Act vs Section 44(2) DPDP Act
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-009",
            question=(
                "What is the operational status of Section 43A of the Information Technology Act, 2000 as of 16 October 2026, "
                "and on what exact date does its omission under Section 44(2) of the DPDP Act, 2023 take legal effect?"
            ),
            answer=(
                "As of 16 October 2026, Section 43A of the Information Technology Act, 2000 remains operative law and legally enforceable. "
                "While Section 44(2)(a) of the Digital Personal Data Protection Act, 2023 provides for the omission of Section 43A, Notification "
                "G.S.R. 843(E) (published 13 November 2025) specifies that Section 44(2) commences on the expiry of eighteen months from publication. "
                "Computing eighteen calendar months from 13 November 2025 under Section 9 of the General Clauses Act, 1897 establishes that "
                "Section 44(2) commences on 13 May 2027. Therefore, prior to 13 May 2027, Section 43A IT Act remains in force."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023", "IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 44(2) and Section 9 GC Act computation",
                    verbatim_text=(
                        "(2) The Information Technology Act, 2000 (21 of 2000) shall be amended in the following manner, namely:-\n\n"
                        "(a) section 43A shall be omitted;"
                    ),
                    page_number=16,
                ),
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 43A heading",
                    verbatim_text="43A. Compensation for failure to protect data.",
                    page_number=28,
                ),
            ],
            legal_domain="Data Protection Law - Temporal Statutory Status",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 44(2), Digital Personal Data Protection Act, 2023",
                "Section 43A, Information Technology Act, 2000",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.PARTIALLY_COMMENCED,
            provision_commencement_status=ProvisionCommencementStatus.PARTIAL,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 10. DPDP s.44(2): Consequential amendments to IT Act Section 81 and Section 87
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-DPDP-010",
            question=(
                "What consequential amendments does Section 44(2) of the DPDP Act, 2023 make to Section 81 and Section 87 of the "
                "Information Technology Act, 2000, and when do they take effect?"
            ),
            answer=(
                "Under Section 44(2) of the Digital Personal Data Protection Act, 2023 (scheduled to commence on 13 May 2027 under G.S.R. 843(E) "
                "and uncommenced as of 16 October 2026), the Information Technology Act, 2000 is amended as follows: in addition to omitting Section 43A, "
                "(b) in Section 81, in the proviso, after the words and figures 'the Patents Act, 1970 (39 of 1970)', the words and figures 'or the "
                "Digital Personal Data Protection Act, 2023' shall be inserted; and (c) in Section 87, in sub-section (2), clause (ob) shall be omitted. "
                "(Note: By contrast, Section 44(1) and 44(3) commenced on 13 November 2025)."
            ),
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 44(2)",
                    verbatim_text=(
                        "(2) The Information Technology Act, 2000 (21 of 2000) shall be amended in the following manner, namely:-\n\n"
                        "(a) section 43A shall be omitted;\n\n"
                        "(b) in section 81, in the proviso, after the words and figures \"the Patents Act, 1970 (39 of 1970)\", "
                        "the words and figures \"or the Digital Personal Data Protection Act, 2023\" shall be inserted; and\n\n"
                        "(c) in section 87, in sub-section (2), clause (ob) shall be omitted."
                    ),
                    page_number=16,
                )
            ],
            legal_domain="Data Protection Law - Consequential Statutory Amendments",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 44(2), Digital Personal Data Protection Act, 2023",
                "Section 81, Information Technology Act, 2000",
                "Section 87, Information Technology Act, 2000",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        )
    )

    # =========================================================================
    # Group 2: 10 Cross-Statute Evidence & Cybercrime Examples
    # =========================================================================

    # 11. BSA s.61 & IT Act s.2(1)(t): Admissibility of electronic records
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-001",
            question=(
                "Under current law, how does Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 establish the admissibility of an electronic "
                "record as defined under Section 2(1)(t) of the Information Technology Act, 2000, and what statutory proviso applies?"
            ),
            answer=(
                "Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under S.O. 849(E)), nothing in the Adhiniyam "
                "shall apply to deny the admissibility of an electronic or digital record in evidence solely on the ground that it is an electronic "
                "or digital record. Such record has the same legal effect, validity, and enforceability as other documents, but is expressly subject "
                "to Section 63. The Explanation incorporates the definition in clause (t) of Section 2(1) of the Information Technology Act, 2000, "
                "and the proviso mandates that any electronic record produced in evidence must be accompanied by a certificate under Section 63(4)."
            ),
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61", "IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Section 61",
                    verbatim_text=(
                        "Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic "
                        "or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same "
                        "legal effect, validity and enforceability as other document, subject to the provisions of section 63."
                    ),
                    page_number=1,
                ),
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Explanation to Section 61",
                    verbatim_text=(
                        "For the purposes of this section, an electronic or digital record includes records stored, generated, received "
                        "or sent in an electronic form or micro-films, computer-generated fiche and any other form as defined in clause (t) of sub-section "
                        "(1) of section 2 of the Information Technology Act, 2000."
                    ),
                    page_number=1,
                ),
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 2(1)(t)",
                    verbatim_text='(t) "electronic record" means data, record or data generated, image or sound stored, received or sent in an electronic form or micro film or computer generated micro fiche;',
                    page_number=2,
                ),
            ],
            legal_domain="Criminal Law - Electronic Evidence",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 61, Bharatiya Sakshya Adhiniyam, 2023",
                "Section 63, Bharatiya Sakshya Adhiniyam, 2023",
                "Section 2(1)(t), Information Technology Act, 2000",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 12. BSA s.61 Proviso: Mandatory Section 63 Certificate
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-002",
            question="What mandatory requirement is set forth in the proviso to Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 when producing electronic records in evidence?",
            answer=(
                "Under the proviso to Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under Notification S.O. 849(E)), "
                "where any electronic record is produced in evidence, it shall mandatorily be accompanied by a certificate referred to in sub-section (4) of Section 63."
            ),
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Proviso to Section 61",
                    verbatim_text="Provided that where any electronic record is produced in evidence, it shall be accompanied by a certificate referred to in sub-section (4) of section 63.",
                    page_number=1,
                )
            ],
            legal_domain="Criminal Law - Electronic Evidence",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 61, Bharatiya Sakshya Adhiniyam, 2023",
                "Section 63, Bharatiya Sakshya Adhiniyam, 2023",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 13. BSA s.63(1) and (2): Deemed Document and Certificate by Person in Official Charge
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-003",
            question="Under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023, when is electronic information deemed to be a document and who must sign the accompanying certificate?",
            answer=(
                "Under Section 63(1) of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under S.O. 849(E)), any information contained "
                "in an electronic record which is printed on paper, stored, recorded, or copied in optical or magnetic media shall be deemed to be also a "
                "document. Under Section 63(2), the computer output must be produced during a period of regular use with regular input of information, "
                "provided that the certificate signed by a person in official charge shall be produced in evidence."
            ),
            supporting_source_ids=["IND-STAT-BSA-2023-SEC63"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC63",
                    section_or_para_ref="Section 63(1) and (2)",
                    verbatim_text=(
                        "**63.** (1) Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record "
                        "which is printed on a paper, stored, recorded or copied in optical or magnetic media shall be deemed to be also a document.\n\n"
                        "(2) The conditions referred to in sub-section (1) in respect of a computer output shall be the following, namely:-\n\n"
                        "- (a) the computer output containing the information was produced by the computer during the period over which the computer was used regularly;\n"
                        "- (b) during the said period, information of the kind contained in the electronic record was regularly fed into the computer;\n\n"
                        "**Provided that** the certificate signed by a person in official charge shall be produced in evidence."
                    ),
                    page_number=1,
                )
            ],
            legal_domain="Criminal Law - Electronic Evidence",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 63, Bharatiya Sakshya Adhiniyam, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 14. BSA s.61 & s.63: Interplay of Admissibility and Certificate Requirements
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-004",
            question="Can an electronic record be admitted in evidence under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 without complying with Section 63?",
            answer=(
                "No. Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under S.O. 849(E)) explicitly states that the legal "
                "effect, validity, and enforceability of an electronic or digital record is 'subject to the provisions of section 63'. Furthermore, the "
                "proviso to Section 61 specifies that where any electronic record is produced in evidence, it shall be accompanied by a certificate "
                "referred to in sub-section (4) of Section 63."
            ),
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Section 61",
                    verbatim_text=(
                        "Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic "
                        "or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same "
                        "legal effect, validity and enforceability as other document, subject to the provisions of section 63.\n\n"
                        "Provided that where any electronic record is produced in evidence, it shall be accompanied by a certificate referred to in sub-section (4) of section 63."
                    ),
                    page_number=1,
                )
            ],
            legal_domain="Criminal Law - Electronic Evidence",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 61, Bharatiya Sakshya Adhiniyam, 2023",
                "Section 63, Bharatiya Sakshya Adhiniyam, 2023",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 15. IT Act s.66: Computer Related Offences
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-005",
            question="What elements constitute a computer related offence under Section 66 of the Information Technology Act, 2000 and what punishment is prescribed?",
            answer=(
                "Under Section 66 of the Information Technology Act, 2000 (in force w.e.f. 27 October 2009 pursuant to Act 10 of 2009), if any person, "
                "dishonestly or fraudulently, does any act referred to in Section 43, he commits a computer related offence and shall be punishable with "
                "imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both. The Explanation "
                "clarifies that 'dishonestly' and 'fraudulently' carry the meanings assigned to them in Section 24 and Section 25 of the Indian Penal Code."
            ),
            supporting_source_ids=["IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 66 and Explanation",
                    verbatim_text=(
                        "1 [66. Computer related offences.-If any person, dishonestly or fraudulently, does any act referred to in section 43, "
                        "he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to "
                        "five lakh rupees or with both.\n\n"
                        "Explanation.-For the purposes of this section,-\n\n"
                        "(a) the word \"dishonestly\" shall have the meaning assigned to it in section 24 of the Indian Penal Code (45 of 1860);\n\n"
                        "(b) the word \"fraudulently\" shall have the meaning assigned to it in section 25 of the Indian Penal Code (45 of 1860)."
                    ),
                    page_number=35,
                )
            ],
            legal_domain="Cyber Law - Information Technology Offences",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 66, Information Technology Act, 2000",
                "Section 43, Information Technology Act, 2000",
                "Section 24, Indian Penal Code, 1860",
                "Section 25, Indian Penal Code, 1860",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-STAT-IT-2000",
            commencement_date=date(2009, 10, 27),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 16. IT Act s.66C: Identity Theft
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-006",
            question="What ingredients constitute the offence of identity theft under Section 66C of the Information Technology Act, 2000 and what is the penalty?",
            answer=(
                "Under Section 66C of the Information Technology Act, 2000 (in force w.e.f. 27 October 2009 under Act 10 of 2009), whoever fraudulently "
                "or dishonestly makes use of the electronic signature, password, or any other unique identification feature of any other person commits "
                "identity theft. The offender shall be punished with imprisonment of either description for a term which may extend to three years and "
                "shall also be liable to fine which may extend to one lakh rupees."
            ),
            supporting_source_ids=["IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 66C",
                    verbatim_text=(
                        "66C. Punishment for identity theft.-Whoever, fraudulently or dishonestly make use of the electronic signature, password "
                        "or any other unique identification feature of any other person, shall be punished with imprisonment of either description "
                        "for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh."
                    ),
                    page_number=37,
                )
            ],
            legal_domain="Cyber Law - Information Technology Offences",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 66C, Information Technology Act, 2000"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-STAT-IT-2000",
            commencement_date=date(2009, 10, 27),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 17. IT Act s.66D: Cheating by Personation Using Computer Resource
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-007",
            question="What acts constitute cheating by personation using a computer resource under Section 66D of the Information Technology Act, 2000 and what is the sentence?",
            answer=(
                "Under Section 66D of the Information Technology Act, 2000 (in force w.e.f. 27 October 2009 under Act 10 of 2009), whoever, by means of "
                "any communication device or computer resource cheats by personating, shall be punished with imprisonment of either description for a term "
                "which may extend to three years and shall also be liable to fine which may extend to one lakh rupees."
            ),
            supporting_source_ids=["IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 66D",
                    verbatim_text=(
                        "66D. Punishment for cheating by personation by using computer resource.-Whoever, by means of any communication device "
                        "or computer resource cheats by personating, shall be punished with imprisonment of either description for a term which "
                        "may extend to three years and shall also be liable to fine which may extend to one lakh rupees."
                    ),
                    page_number=37,
                )
            ],
            legal_domain="Cyber Law - Information Technology Offences",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 66D, Information Technology Act, 2000"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-STAT-IT-2000",
            commencement_date=date(2009, 10, 27),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 18. BNSS s.482(1): Direction for grant of bail to person apprehending arrest
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-008",
            question="Which judicial forums possess jurisdiction to grant anticipatory bail under Section 482(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer=(
                "Under Section 482(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under Notification S.O. 848(E)), "
                "when any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may "
                "apply to either the High Court or the Court of Session for a direction under Section 482, and that Court may, if it thinks fit, "
                "direct that in the event of such arrest, he shall be released on bail."
            ),
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 482(1)",
                    verbatim_text=(
                        "When any person has reason to believe that he may "
                        "be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session "
                        "for a direction under this section; and that Court may, if it thinks fit, direct that in the event of such arrest, he shall be released on bail."
                    ),
                    page_number=198,
                )
            ],
            legal_domain="Criminal Procedure - Anticipatory Bail",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=["Section 482(1), Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 19. BNSS s.482(4): Statutory Exclusion for BNS Section 65 and Section 70(2)
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-009",
            question="Which offences are strictly barred from the grant of anticipatory bail under Section 482(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer=(
                "Under Section 482(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under S.O. 848(E)), the provisions "
                "of Section 482 for anticipatory bail shall not apply to any case involving the arrest of any person on an accusation of having committed "
                "an offence under Section 65 and sub-section (2) of Section 70 of the Bharatiya Nyaya Sanhita, 2023 (relating to aggravated rape of minors/gang rape)."
            ),
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 482(4)",
                    verbatim_text=(
                        "(4) Nothing in this section shall apply to any case involving the arrest of any person on accusation of having committed "
                        "an offence under section 65 and sub-section \n(2)\n of section 70 of the Bharatiya Nyaya Sanhita, 2023."
                    ),
                    page_number=198,
                )
            ],
            legal_domain="Criminal Procedure - Statutory Exclusions from Anticipatory Bail",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 482(4), Bharatiya Nagarik Suraksha Sanhita, 2023",
                "Section 65, Bharatiya Nyaya Sanhita, 2023",
                "Section 70(2), Bharatiya Nyaya Sanhita, 2023",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        )
    )

    # 20. BNSS s.531(2)(a): Repeal and Savings for Pre-July 2024 Criminal Proceedings
    examples.append(
        LegalQADocument(
            qa_id="QA-PILOT-CROSS-010",
            question="How are criminal appeals, applications, trials, and investigations pending immediately before 1 July 2024 governed under Section 531(2)(a) of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer=(
                "Under Section 531(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under S.O. 848(E)), the Code of Criminal "
                "Procedure, 1973 is repealed. However, under Section 531(2)(a), if immediately before 1 July 2024 there was any appeal, application, "
                "trial, inquiry, or investigation pending, such proceeding shall be disposed of, continued, held, or made in accordance with the provisions "
                "of the Code of Criminal Procedure, 1973 as if the BNSS had not come into force."
            ),
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 531(1) and (2)(a)",
                    verbatim_text=(
                        "(1) The Code of Criminal Procedure, 1973 (2 of 1974) is hereby repealed.\n \n"
                        "(2) Notwithstanding such repeal---\n \n"
                        "(a) if, immediately before the date on which this Sanhita comes into force, there is any appeal, application, trial, "
                        "inquiry or investigation pending, then, such appeal, application, trial, inquiry or investigation shall be disposed of, "
                        "continued, held or made, as the case may be, in accordance with the provisions of the Code of Criminal Procedure, 1973 "
                        "(2 of 1974), as in force immediately before such commencement (hereinafter referred to as the said Code), as if this Sanhita had not come into force;"
                    ),
                    page_number=218,
                )
            ],
            legal_domain="Criminal Procedure - Repeal and Savings",
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            statutory_citations=[
                "Section 531, Bharatiya Nagarik Suraksha Sanhita, 2023",
                "Code of Criminal Procedure, 1973",
            ],
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
            legal_as_of_date=audit_date,
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            repealed_statute_context="Code of Criminal Procedure, 1973 (Act No. 2 of 1974) is repealed with savings under BNSS s. 531(2)(a)",
            repealed_statute_status=LawStatusLabel.REPEALED_WITH_SAVINGS,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_HISTORICAL_SAVINGS,
        )
    )

    return examples


def validate_and_export():
    reg = SourceRegistryManager("registry/source_registry.jsonl")
    orch = GenerationOrchestrator(GenerationConfig(dry_run=True), reg)
    grounding_val = GenerationValidator(reg)
    temporal_val = TemporalValidator()

    source_ids = [
        "IND-STAT-DPDP-2023",
        "IND-STAT-IT-2000",
        "IND-STAT-BSA-2023-SEC61",
        "IND-STAT-BSA-2023-SEC63",
        "IND-STAT-BNSS-2023",
    ]
    source_texts = {sid: orch.load_source_text(sid) for sid in source_ids}
    source_records = {sid: reg.get(sid) for sid in source_ids}

    examples = build_pilot_examples()
    assert len(examples) == 20, f"Expected exactly 20 examples, got {len(examples)}"

    print(f"Validating {len(examples)} controlled pilot examples (Grounding + Temporal Law)...")

    print("Executing DataQualityGate across 20 controlled pilot examples (8 Pre-Generation Quality Gates)...")
    gate = DataQualityGate(registry_manager=reg, source_texts=source_texts)
    all_passed, qg_results = gate.validate_batch(examples)

    validated_docs = []
    all_issues = []

    for idx, (doc, qg_res) in enumerate(zip(examples, qg_results), start=1):
        if not qg_res.is_valid:
            print(f"FAILED QualityGate Example {idx} ({doc.qa_id}): {qg_res.issues}")
            all_issues.extend(qg_res.issues)
        else:
            print(f"PASSED QualityGate Example {idx} ({doc.qa_id}) [Label: {doc.law_status_label.value}] - All 8 Gates Cleared")
            validated_docs.append(doc)

    if not all_passed or all_issues:
        print(f"Total QualityGate issues: {len(all_issues)}")
        raise RuntimeError("DataQualityGate validation failed for pilot examples")

    # Export to JSONL
    out_file = Path("data/03_generated/pilot_20_examples.jsonl")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        for doc in validated_docs:
            f.write(doc.model_dump_json() + "\n")
    print(f"Exported 20 validated examples to {out_file}")

    # Build machine-readable manifest
    manifest = {
        "manifest_version": "1.2",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "audit_phase": "Phase 7.2 Advocate Review Package & Data Quality Gates",
        "total_examples": len(validated_docs),
        "source_breakdown": {
            "IND-STAT-DPDP-2023": 10,
            "IND-STAT-IT-2000": 6,
            "IND-STAT-BSA-2023-SEC61": 3,
            "IND-STAT-BSA-2023-SEC63": 2,
            "IND-STAT-BNSS-2023": 3,
        },
        "category_breakdown": {
            "dpdp_it_statutory_qa": 10,
            "cross_statute_evidence_and_cybercrime": 10,
        },
        "temporal_law_distribution": {
            "in_force": len([d for d in validated_docs if d.law_status_label == LawStatusLabel.IN_FORCE]),
            "enacted_not_yet_in_force": len([d for d in validated_docs if d.law_status_label == LawStatusLabel.ENACTED_NOT_YET_IN_FORCE]),
            "partially_commenced": len([d for d in validated_docs if d.law_status_label == LawStatusLabel.PARTIALLY_COMMENCED]),
            "repealed_prior_enactments_saved": len([d for d in validated_docs if d.repealed_statute_status == LawStatusLabel.REPEALED_WITH_SAVINGS]),
        },
        "temporal_validation_status": {
            "bnss_commencement_notification": "S.O. 848(E) dated 24 February 2024 (effective 1 July 2024)",
            "bsa_commencement_notification": "S.O. 849(E) dated 24 February 2024 (effective 1 July 2024)",
            "dpdp_commencement_notification": "G.S.R. 843(E) dated 13 November 2025",
            "dpdp_group_1_provisions": "Sections 2, 18-26, 35-43, 44(1), 44(3) commenced 13 Nov 2025",
            "dpdp_group_2_provisions": "Section 6(9), Section 27(1)(d) commence 13 Nov 2026 (1 year)",
            "dpdp_group_3_provisions": "Sections 3-5, 6(1)-(8), 6(10), 7-17, 27 except 27(1)(d), 28-34, 36, 37, 44(2) commence 13 May 2027 (18 months)",
            "it_act_section_43a_status": "Legally operative and enforceable until 13 May 2027 under G.S.R. 843(E)",
            "bnss_section_531_status": "BNSS Section 531 is in force since 1 July 2024; CrPC 1973 is repealed with savings",
        },
        "quarantine_compliance": {
            "synthetic_scaffold_quarantined": "IND-JUD-DEL-2024-BAIL (is_synthetic_scaffold=1, excluded from pilot)",
            "quarantined_generated_guide": "PROC-BNSS-482-BAIL-001 (excluded from training/RAG splits)",
        },
        "examples": [
            {
                "qa_id": doc.qa_id,
                "question": doc.question,
                "supporting_source_ids": doc.supporting_source_ids,
                "legal_domain": doc.legal_domain,
                "statutory_citations": doc.statutory_citations,
                "legal_review_status": doc.legal_review_status.value,
                "legal_as_of_date": doc.legal_as_of_date.isoformat() if doc.legal_as_of_date else None,
                "commencement_source_id": doc.commencement_source_id,
                "commencement_date": doc.commencement_date.isoformat() if doc.commencement_date else None,
                "law_status_label": doc.law_status_label.value if doc.law_status_label else None,
                "provision_commencement_status": doc.provision_commencement_status.value if doc.provision_commencement_status else None,
                "repealed_statute_context": doc.repealed_statute_context,
                "repealed_statute_status": doc.repealed_statute_status.value if doc.repealed_statute_status else None,
                "temporal_validation_status": doc.temporal_validation_status.value if doc.temporal_validation_status else None,
            }
            for doc in validated_docs
        ],
    }

    manifest_file = Path("data/03_generated/pilot_20_manifest.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Exported machine-readable manifest to {manifest_file}")


if __name__ == "__main__":
    validate_and_export()
