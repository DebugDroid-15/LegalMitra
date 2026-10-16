"""
Batch 1 Candidate Generation Script
Generates 20 authentic, grounded candidate examples across verified legal sources:
- DPDP Act 2023 (uncommenced provisions with explicit temporal qualifications)
- BNSS 2023 (in-force criminal procedure provisions)
- BSA 2023 (in-force electronic evidence provisions)
- POCSO Act 2012 (in-force child protection provisions)
- IT Act 2000 (in-force cyber offenses provisions)
- Puttaswamy (2017) (authoritative constitutional privacy precedent)

All candidates are marked strictly pending_legal_review.
Outputs:
- data/07_batches/batch_01_candidates/batch_01_examples.jsonl
- data/07_batches/batch_01_candidates/batch_01_manifest.json
- data/07_batches/review/batch_01_review_sheet.csv
"""

import csv
import json
from datetime import date, datetime
from pathlib import Path

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
    TemporalValidationStatus,
)
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.generation.orchestrator import GenerationOrchestrator
from legalmitra.generation.schemas import GenerationConfig
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.validation.quality_gate import DataQualityGate


def build_candidates() -> list[LegalQADocument]:
    examples = [
        # --- DPDP ACT 2023 (5 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-001",
            question="Under the enacted provisions of Section 4(1) of the Digital Personal Data Protection Act, 2023 (scheduled to commence on 13 May 2027 under G.S.R. 843(E)), under what grounds may personal data be processed?",
            answer="Under Section 4(1) of the Digital Personal Data Protection Act, 2023 (enacted and scheduled to commence on 13 May 2027 under Notification G.S.R. 843(E), and not yet in force as of 16 October 2026), a person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose: (a) for which the Data Principal has given her consent; or (b) for certain legitimate uses.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 4(1)",
                    verbatim_text="4. Grounds for processing personal data.-(1) A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose,-\n\n(a) for which the Data Principal has given her consent; or\n\n- (b) for certain legitimate uses.",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 4(1), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-002",
            question="What statutory notice requirements are mandated under the enacted text of Section 5(1) of the DPDP Act, 2023 when requesting consent from a Data Principal once commenced?",
            answer="Under Section 5(1) of the Digital Personal Data Protection Act, 2023 (enacted and appointed to commence on 13 May 2027 under G.S.R. 843(E), hence uncommenced as of 16 October 2026), every request made to a Data Principal under Section 6 for consent shall be accompanied or preceded by a notice informing her: (i) the personal data and the purpose for which the same is proposed to be processed; (ii) the manner in which she may exercise her rights under Section 6(4) and Section 13; and (iii) the manner in which she may make a complaint to the Board.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 5(1)",
                    verbatim_text="5. Notice.-(1) Every request made to a Data Principal under section 6 for consent shall be accompanied or preceded by a notice given by the Data Fiduciary to the Data Principal, informing her,-\n\n(i) the personal data and the purpose for which the same is proposed to be processed;\n\n(ii) the manner in which she may exercise her rights under sub-section (4) of section 6 and section 13; and",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 5(1), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-003",
            question="When may personal data be processed for legitimate uses under the enacted scheme of Section 7(a) of the Digital Personal Data Protection Act, 2023 upon its scheduled commencement?",
            answer="Under Section 7(a) of the Digital Personal Data Protection Act, 2023 (enacted and scheduled to commence on 13 May 2027 under G.S.R. 843(E) and not yet in force as of 16 October 2026), a Data Fiduciary may process personal data of a Data Principal for the specified purpose for which the Data Principal has voluntarily provided her personal data to the Data Fiduciary, and in respect of which she has not indicated to the Data Fiduciary that she does not consent to the use of her personal data.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 7(a)",
                    verbatim_text="7. Certain legitimate uses.-A Data Fiduciary may process personal data of a Data Principal for any of following uses, namely:-\n\n(a) for the specified purpose for which the Data Principal has voluntarily provided her personal data to the Data Fiduciary, and in respect of which she has not indicated to the Data Fiduciary that she does not consent to the use of her personal data.",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 7(a), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-004",
            question="What statutory consent requirement applies to processing personal data of children under the enacted Section 9(1) of the DPDP Act, 2023 when it takes effect?",
            answer="Under Section 9(1) of the Digital Personal Data Protection Act, 2023 (scheduled to commence on 13 May 2027 under Notification G.S.R. 843(E) and uncommenced as of 16 October 2026), the Data Fiduciary shall, before processing any personal data of a child or a person with disability who has a lawful guardian, obtain verifiable consent of the parent of such child or the lawful guardian, as the case may be, in such manner as may be prescribed.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 9(1)",
                    verbatim_text="9. Processing of personal data of children.-(1) The Data Fiduciary shall, before processing any personal data of a child or a person with disability who has a lawful guardian obtain verifiable consent of the parent of such child or the lawful guardian, as the case may be, in such manner as may be prescribed.",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 9(1), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-005",
            question="What assessment factors guide the Central Government in notifying a Significant Data Fiduciary under the enacted Section 10(1) of the DPDP Act, 2023?",
            answer="Under Section 10(1) of the Digital Personal Data Protection Act, 2023 (enacted and scheduled to commence on 13 May 2027 under G.S.R. 843(E), not yet in force as of 16 October 2026), the Central Government may notify any Data Fiduciary or class of Data Fiduciaries as Significant Data Fiduciary based on assessment of factors including: (a) the volume and sensitivity of personal data processed; (b) risk to the rights of Data Principal; and (c) potential impact on the sovereignty and integrity of India.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 10(1)",
                    verbatim_text="10. Additional obligations of Significant Data Fiduciary.-(1) The Central Government may notify any Data Fiduciary or class of Data Fiduciaries as Significant Data Fiduciary, on the basis of an assessment of such relevant factors as it may determine, including-\n\n(a) the volume and sensitivity of personal data processed;\n\n(b) risk to the rights of Data Principal;",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 10(1), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),

        # --- BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (5 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-006",
            question="Under what circumstances may a police officer arrest a person without a warrant under Section 35(1)(a) of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer="Under Section 35(1)(a) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 pursuant to Notification S.O. 848(E)), any police officer may, without an order from a Magistrate and without a warrant, arrest any person who commits, in the presence of a police officer, a cognizable offence.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 35(1)(a)",
                    verbatim_text="(a) who commits, in the presence of a police officer, a cognizable offence; or",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 35(1)(a), Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-007",
            question="How may information relating to the commission of a cognizable offence be given to a police station under Section 173(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer="Under Section 173(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under Notification S.O. 848(E)), every information relating to the commission of a cognizable offence, irrespective of the area where the offence is committed, may be given orally or by electronic communication to an officer in charge of a police station.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 173(1)",
                    verbatim_text="Every information relating to the commission of a cognizable offence, irrespective of the area where the offence is committed, may be given orally or by electronic communication to an officer in charge of a police station, and if given",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 173(1), Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-008",
            question="What statutory right to bail is provided to an under-trial prisoner who has undergone detention extending up to one-half of the maximum sentence under Section 479(1) of the BNSS 2023?",
            answer="Under Section 479(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under Notification S.O. 848(E)), where a person has, during the period of investigation, inquiry, or trial of an offence (not being an offence punishable with death or life imprisonment) undergone detention extending up to one-half of the maximum period of imprisonment specified for that offence, he shall be released by the Court on bail.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 479(1)",
                    verbatim_text="Where a person has, during the period of investigation, inquiry or trial under this Sanhita of an offence under any law (not being an offence for which the punishment of death or life imprisonment has been specified as one of the punishments under that law) undergone detention for a period extending up to one-half of the maximum period of imprisonment specified for that offence under that law, he shall be released by the Court on bail:",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 479(1), Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-009",
            question="What is the scope of inherent powers preserved for the High Court under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer="Under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under S.O. 848(E)), nothing in the Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Sanhita, or to prevent abuse of the process of any court or otherwise to secure the ends of justice.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 528",
                    verbatim_text="Nothing in this Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Sanhita, or to prevent abuse of the process of any court or otherwise to secure the ends of justice.",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 528, Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-010",
            question="What repeal and savings effect does Section 531(1) and 531(2)(a) of the BNSS 2023 have on proceedings instituted under the CrPC 1973 prior to 1 July 2024?",
            answer="Under Section 531(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 (in force since 1 July 2024 under S.O. 848(E)), the Code of Criminal Procedure, 1973 is repealed. However, by virtue of Section 531(2)(a), any appeal, application, trial, inquiry, or investigation pending immediately before 1 July 2024 shall be disposed of, continued, held, or made in accordance with the provisions of the Code of Criminal Procedure, 1973 as if the BNSS had not come into force.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 531(1) and (2)(a)",
                    verbatim_text="(1) The Code of Criminal Procedure, 1973 (2 of 1974) is hereby repealed.\n \n(2) Notwithstanding such repeal---\n \n(a) if, immediately before the date on which this Sanhita comes into force, there is any appeal, application, trial, inquiry or investigation pending, then, such appeal, application, trial, inquiry or investigation shall be disposed of, continued, held or made, as the case may be, in accordance with the provisions of the Code of Criminal Procedure, 1973 (2 of 1974), as in force immediately before such commencement (hereinafter referred to as the said Code), as if this Sanhita had not come into force;",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 531, Bharatiya Nagarik Suraksha Sanhita, 2023", "Code of Criminal Procedure, 1973"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_HISTORICAL_SAVINGS,
            repealed_statute_context="Code of Criminal Procedure, 1973 is repealed with savings under BNSS s. 531(2)(a)",
            repealed_statute_status=LawStatusLabel.REPEALED_WITH_SAVINGS,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),

        # --- BHARATIYA SAKSHYA ADHINIYAM, 2023 (3 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-011",
            question="What statutory rule of admissibility is established for electronic or digital records under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023?",
            answer="Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under Notification S.O. 849(E)), nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of Section 63.",
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Section 61",
                    verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of section 63.",
                )
            ],
            legal_domain="Evidence Law",
            statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023", "Section 63, Bharatiya Sakshya Adhiniyam, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-012",
            question="What statutory definition of electronic or digital record is incorporated in the Explanation to Section 61 of the Bharatiya Sakshya Adhiniyam, 2023?",
            answer="Under the Explanation to Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under S.O. 849(E)), an electronic or digital record includes records stored, generated, received or sent in an electronic form or micro-films, computer-generated fiche and any other form as defined in clause (t) of sub-section (1) of Section 2 of the Information Technology Act, 2000.",
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Explanation to Section 61",
                    verbatim_text="For the purposes of this section, an electronic or digital record includes records stored, generated, received or sent in an electronic form or micro-films, computer-generated fiche and any other form as defined in clause (t) of sub-section (1) of section 2 of the Information Technology Act, 2000.",
                )
            ],
            legal_domain="Evidence Law",
            statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023", "Section 2(1)(t), Information Technology Act, 2000"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-013",
            question="When is electronic information stored in magnetic media deemed to be a document under Section 63(1) of the Bharatiya Sakshya Adhiniyam, 2023?",
            answer="Under Section 63(1) of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under Notification S.O. 849(E)), notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media shall be deemed to be also a document.",
            supporting_source_ids=["IND-STAT-BSA-2023-SEC63"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC63",
                    section_or_para_ref="Section 63(1)",
                    verbatim_text="**63.** (1) Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media shall be deemed to be also a document.",
                )
            ],
            legal_domain="Evidence Law",
            statutory_citations=["Section 63(1), Bharatiya Sakshya Adhiniyam, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),

        # --- POCSO ACT 2012 (3 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-014",
            question="What minimum and maximum punishment is prescribed for penetrative sexual assault under Section 4(1) of the Protection of Children from Sexual Offences Act, 2012?",
            answer="Under Section 4(1) of the Protection of Children from Sexual Offences Act, 2012 (in force since 14 November 2012 pursuant to S.O. 2642(E)), whoever commits penetrative sexual assault shall be punished with imprisonment of either description for a term which shall not be less than ten years but which may extend to imprisonment for life, and shall also be liable to fine.",
            supporting_source_ids=["IND-STAT-POCSO-2012-SEC4"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-POCSO-2012-SEC4",
                    section_or_para_ref="Section 4(1)",
                    verbatim_text="4. Punishment for penetrative sexual assault.—(1) Whoever commits penetrative sexual assault shall be punished with imprisonment of either description for a term which shall not be less than ten years but which may extend to imprisonment for life, and shall also be liable to fine.",
                )
            ],
            legal_domain="Child Protection Law",
            statutory_citations=["Section 4(1), Protection of Children from Sexual Offences Act, 2012"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-WCD-SO-2642E-2012",
            commencement_date=date(2012, 11, 14),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-015",
            question="What enhanced punishment applies under the first proviso to Section 4 of the POCSO Act, 2012 where the child is below sixteen years of age?",
            answer="Under the first proviso to Section 4 of the Protection of Children from Sexual Offences Act, 2012 (in force since 14 November 2012), whoever commits penetrative sexual assault on a child below sixteen years of age shall be punished with rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of natural life of that person, and shall also be liable to fine.",
            supporting_source_ids=["IND-STAT-POCSO-2012-SEC4"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-POCSO-2012-SEC4",
                    section_or_para_ref="Section 4 First Proviso",
                    verbatim_text="Provided that whoever commits penetrative sexual assault on a child below sixteen years of age shall be punished with rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of natural life of that person, and shall also be liable to fine:",
                )
            ],
            legal_domain="Child Protection Law",
            statutory_citations=["Section 4, Protection of Children from Sexual Offences Act, 2012"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-WCD-SO-2642E-2012",
            commencement_date=date(2012, 11, 14),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-016",
            question="What statutory purpose must fine serve under the second proviso to Section 4 of the POCSO Act, 2012?",
            answer="Under the second proviso to Section 4 of the Protection of Children from Sexual Offences Act, 2012 (in force since 14 November 2012), it is provided further that such fine imposed shall be just and reasonable to meet the medical expenses and rehabilitation of the victim.",
            supporting_source_ids=["IND-STAT-POCSO-2012-SEC4"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-POCSO-2012-SEC4",
                    section_or_para_ref="Section 4 Second Proviso",
                    verbatim_text="Provided further that such fine shall be just and reasonable to meet the medical expenses and rehabilitation of the victim.",
                )
            ],
            legal_domain="Child Protection Law",
            statutory_citations=["Section 4, Protection of Children from Sexual Offences Act, 2012"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-WCD-SO-2642E-2012",
            commencement_date=date(2012, 11, 14),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),

        # --- IT ACT 2000 (2 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-017",
            question="What constitutes unauthorized access to a computer system under Section 43(a) of the Information Technology Act, 2000?",
            answer="Under Section 43(a) of the Information Technology Act, 2000 (in force w.e.f. 17 October 2000), if any person without permission of the owner or any other person who is in charge of a computer, computer system or computer network accesses or secures access to such computer, computer system or computer network, he shall be liable to pay damages by way of compensation to the person so affected.",
            supporting_source_ids=["IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 43(a)",
                    verbatim_text="43. 6 [Penalty and compensation] for damage to computer, computer system, etc.-If any person without permission of the owner or any other person who is in charge of a computer, computer system or computer network,-\n\n(a) accesses or secures access to such computer, computer system or computer network",
                )
            ],
            legal_domain="Cyber Law",
            statutory_citations=["Section 43(a), Information Technology Act, 2000"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-STAT-IT-2000",
            commencement_date=date(2000, 10, 17),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-018",
            question="What punishment is prescribed for intentionally capturing or publishing images of a private area under Section 66E of the Information Technology Act, 2000?",
            answer="Under Section 66E of the Information Technology Act, 2000 (in force w.e.f. 27 October 2009 pursuant to Act 10 of 2009), whoever, intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, under circumstances violating the privacy of that person, shall be punished with imprisonment which may extend to three years or with fine not exceeding two lakh rupees, or with both.",
            supporting_source_ids=["IND-STAT-IT-2000"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-IT-2000",
                    section_or_para_ref="Section 66E",
                    verbatim_text="66E. Punishment for violation of privacy.-Whoever, intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, under circumstances violating the privacy of that person, shall be punished with imprisonment which may extend to three years or with fine not exceeding two lakh rupees, or with both.",
                )
            ],
            legal_domain="Cyber Law",
            statutory_citations=["Section 66E, Information Technology Act, 2000"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-STAT-IT-2000",
            commencement_date=date(2009, 10, 27),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),

        # --- PUTTASWAMY CONSTITUTIONAL PRECEDENT (2 Examples) ---
        LegalQADocument(
            qa_id="QA-BATCH1-019",
            question="What is the constitutional ratio decidendi regarding the right to privacy established in Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1?",
            answer="In Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1, the nine-judge Constitution Bench held that the right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
            supporting_source_ids=["IND-JUD-SC-2017-PUTTASWAMY"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-JUD-SC-2017-PUTTASWAMY",
                    section_or_para_ref="Ratio Decidendi",
                    verbatim_text="RATIO DECIDENDI: The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
                )
            ],
            legal_domain="Constitutional Law",
            statutory_citations=["Article 21, Constitution of India"],
            case_citations=["Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-JUD-SC-2017-PUTTASWAMY",
            commencement_date=date(2017, 8, 24),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH1-020",
            question="Which earlier Supreme Court decisions holding that privacy is not a fundamental right were overruled by the 9-Judge Bench in Puttaswamy (2017) 10 SCC 1?",
            answer="In Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1, the nine-judge Constitution Bench expressly overruled the earlier decisions in M.P. Sharma v. Satish Chandra (1954) SCR 1077 and Kharak Singh v. State of U.P. (1964) 1 SCR 332 to the extent that they had held privacy is not a fundamental right under the Constitution.",
            supporting_source_ids=["IND-JUD-SC-2017-PUTTASWAMY"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-JUD-SC-2017-PUTTASWAMY",
                    section_or_para_ref="Paragraph 25",
                    verbatim_text="The decisions in M.P. Sharma and Kharak Singh to the extent they hold that privacy is not a fundamental right stand overruled.",
                )
            ],
            legal_domain="Constitutional Law",
            statutory_citations=["Article 21, Constitution of India"],
            case_citations=[
                "Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1",
                "M.P. Sharma v. Satish Chandra (1954) SCR 1077",
                "Kharak Singh v. State of U.P. (1964) 1 SCR 332",
            ],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-JUD-SC-2017-PUTTASWAMY",
            commencement_date=date(2017, 8, 24),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
    ]
    return examples


def generate_batch_01() -> bool:
    print("=== Generating Batch 1 Candidate Dataset ===")
    reg = SourceRegistryManager("registry/source_registry.jsonl")
    orch = GenerationOrchestrator(GenerationConfig(dry_run=True), reg)

    source_ids = [
        "IND-STAT-DPDP-2023",
        "IND-STAT-IT-2000",
        "IND-STAT-BSA-2023-SEC61",
        "IND-STAT-BSA-2023-SEC63",
        "IND-STAT-BNSS-2023",
        "IND-STAT-POCSO-2012-SEC4",
        "IND-JUD-SC-2017-PUTTASWAMY",
    ]
    source_texts = {sid: orch.load_source_text(sid) for sid in source_ids}

    # Load existing pilot 20 examples to test deduplication against pilot
    pilot_file = Path("data/03_generated/pilot_20_examples.jsonl")
    pilot_docs = []
    if pilot_file.exists():
        with open(pilot_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    pilot_docs.append(LegalQADocument(**json.loads(line)))

    examples = build_candidates()
    print(f"Loaded {len(examples)} candidate definitions.")

    # Run DataQualityGate
    gate = DataQualityGate(registry_manager=reg, source_texts=source_texts)
    all_passed, results = gate.validate_batch(examples, existing_docs=pilot_docs)
    if not all_passed:
        print("[FAIL] Quality gate rejected candidates:")
        for r in results:
            if not r.is_valid:
                print(f"  {r.qa_id}: {r.issues}")
        return False
    print(f"[OK] All {len(examples)} candidates passed all 8 DataQualityGate checks!")

    # Write examples JSONL
    out_dir = Path("data/07_batches/batch_01_candidates")
    out_dir.mkdir(parents=True, exist_ok=True)
    batch_file = out_dir / "batch_01_examples.jsonl"
    with open(batch_file, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(ex.model_dump_json() + "\n")
    print(f"[OK] Wrote {len(examples)} records to {batch_file}")

    # Write Candidate Manifest
    manifest_file = out_dir / "batch_01_manifest.json"
    manifest_data = {
        "batch_id": "BATCH-01",
        "description": "Controlled expansion candidate dataset (Batch 1) covering BNSS, BSA, DPDP, POCSO, IT Act, and Puttaswamy.",
        "created_at": datetime.now().isoformat(),
        "total_records": len(examples),
        "source_coverage": {
            "IND-STAT-DPDP-2023": 5,
            "IND-STAT-BNSS-2023": 5,
            "IND-STAT-BSA-2023-SEC61": 2,
            "IND-STAT-BSA-2023-SEC63": 1,
            "IND-STAT-POCSO-2012-SEC4": 3,
            "IND-STAT-IT-2000": 2,
            "IND-JUD-SC-2017-PUTTASWAMY": 2,
        },
        "legal_review_status_summary": {
            "pending_legal_review": len(examples),
            "approved": 0,
            "rejected": 0,
        },
        "quarantine_compliance": {
            "IND-JUD-DEL-2024-BAIL_excluded": True,
            "synthetic_scaffolds_excluded": True,
        },
        "sha256": compute_file_sha256(batch_file),
    }
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"[OK] Wrote candidate manifest to {manifest_file}")

    # Write blank review sheet CSV
    review_dir = Path("data/07_batches/review")
    review_dir.mkdir(parents=True, exist_ok=True)
    csv_file = review_dir / "batch_01_review_sheet.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "record_id",
            "legal_domain",
            "statutory_citations",
            "question",
            "answer",
            "review_decision",
            "legal_accuracy_score_1_to_5",
            "temporal_accuracy_score_1_to_5",
            "grounding_accuracy_score_1_to_5",
            "reviewer_comments",
            "reviewer_name_initials",
            "review_date",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ex in examples:
            writer.writerow({
                "record_id": ex.qa_id,
                "legal_domain": ex.legal_domain,
                "statutory_citations": "; ".join(ex.statutory_citations),
                "question": ex.question,
                "answer": ex.answer,
                "review_decision": "",
                "legal_accuracy_score_1_to_5": "",
                "temporal_accuracy_score_1_to_5": "",
                "grounding_accuracy_score_1_to_5": "",
                "reviewer_comments": "",
                "reviewer_name_initials": "",
                "review_date": "",
            })
    print(f"[OK] Wrote blank review sheet to {csv_file}")
    print("=== Batch 1 Candidate Generation Complete ===")
    return True


if __name__ == "__main__":
    generate_batch_01()
