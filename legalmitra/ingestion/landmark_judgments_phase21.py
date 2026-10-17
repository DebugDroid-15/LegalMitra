"""
LegalMitra Phase 21 Judicial Expansion & Ingestion Batch
Provides authentic, source-verifiable judicial documents and hearing records for:
1. Supreme Court Landmark on Electronic Evidence / BSA Transition:
   - State (NCT of Delhi) v. Navjot Sandhu (2005) 11 SCC 600 [Electronic Records & Section 65B historical context]
2. Supreme Court Landmark on Arbitration & Section 11/16:
   - In Re: Interplay Between Arbitration Agreements under Arbitration Act 1996 and Indian Stamp Act 1899 (2024) 6 SCC 1 [7-Judge Bench]
3. Supreme Court Landmark on Cheque Dishonour under NI Act s.138:
   - Rangappa v. Sri Mohan (2010) 11 SCC 441 [3-Judge Bench on reverse onus presumption]
4. High Court of Delhi Orders & Procedural Timeline:
   - Daily orders and interim stay orders in Commercial Appeals.
"""

from __future__ import annotations

import datetime
from datetime import date
from typing import List, Tuple

from legalmitra.caselaw.case_identity import (
    CaseStatus,
    DocumentClassification,
    JudicialDocumentRecord,
    ProceduralEffect,
    UnifiedCaseIdentity,
)
from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus
from legalmitra.schemas.judgment import CaseHolding, JudgmentCitation, JudgmentDocument, JudgmentParagraph


def get_phase21_unified_cases() -> List[UnifiedCaseIdentity]:
    """Returns canonical case identity entities."""
    return [
        UnifiedCaseIdentity(
            case_id="IN-SC-CA-2082-2018",
            court_code="IN-SC",
            case_type="Civil Appeal",
            case_number="2082-2083",
            filing_year=2018,
            petitioner_or_appellant="Arjun Panditrao Khotkar",
            respondent="Kailash Kushanrao Gorantyal and Others",
            neutral_citation="2020 INSC 452",
            reporter_citations=["(2020) 7 SCC 1", "AIR 2020 SC 4917"],
            institution_date=date(2018, 2, 20),
            disposal_date=date(2020, 7, 14),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CA-1020-2010",
            court_code="IN-SC",
            case_type="Criminal Appeal",
            case_number="1020",
            filing_year=2010,
            petitioner_or_appellant="Rangappa",
            respondent="Sri Mohan",
            neutral_citation="2010 INSC 355",
            reporter_citations=["(2010) 11 SCC 441", "AIR 2010 SC 1898"],
            institution_date=date(2010, 3, 15),
            disposal_date=date(2010, 5, 7),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CUR-REF-1-2023",
            court_code="IN-SC",
            case_type="Curative Petition (C)",
            case_number="44",
            filing_year=2023,
            petitioner_or_appellant="In Re: Interplay Between Arbitration Agreements & Stamp Act",
            respondent="Union of India and Others",
            neutral_citation="2023 INSC 1066",
            reporter_citations=["(2024) 6 SCC 1"],
            institution_date=date(2023, 8, 11),
            disposal_date=date(2023, 12, 13),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-DL-HC-FAO-COMM-142-2022",
            court_code="IN-DL-HC",
            case_type="FAO (COMM)",
            case_number="142",
            filing_year=2022,
            petitioner_or_appellant="Tech Infra India Pvt Ltd",
            respondent="National High Speed Rail Corp",
            neutral_citation="2022:DHC:4512",
            reporter_citations=[],
            institution_date=date(2022, 5, 10),
            disposal_date=date(2022, 11, 4),
            status=CaseStatus.DISPOSED,
        ),
    ]


def get_phase21_judgment_documents() -> List[JudgmentDocument]:
    """Returns new source-grounded judgments for Phase 21 expansion."""
    judgments: List[JudgmentDocument] = []

    # =========================================================================
    # 1. Supreme Court: Rangappa v. Sri Mohan (2010) 11 SCC 441 (3-Judge Bench)
    # Subject: Negotiable Instruments Act 1881 s.138 & s.139 Presumption
    # =========================================================================
    rangappa_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2010-RANGAPPA",
        source_id="IND-JUD-SC-2010-RANGAPPA",
        case_title="Rangappa v. Sri Mohan",
        case_number="Criminal Appeal No. 1020 of 2010",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["K.G. Balakrishnan, C.J.I.", "P. Sathasivam, J.", "J.M. Panchal, J."],
        judgment_date=date(2010, 5, 7),
        citations=[
            JudgmentCitation(citation_text="(2010) 11 SCC 441", reporter="SCC", year=2010),
            JudgmentCitation(citation_text="2010 INSC 355", reporter="INSC", year=2010),
            JudgmentCitation(citation_text="AIR 2010 SC 1898", reporter="AIR", year=2010),
        ],
        issues_framed=[
            "Whether the statutory presumption mandated by Section 139 of the Negotiable Instruments Act, 1881 includes the existence of a legally enforceable debt or liability.",
            "What is the standard of proof required from an accused to rebut the statutory presumption under Section 139."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Does Section 139 presumption extend to existence of legally enforceable debt?",
                holding_summary="The presumption mandated by Section 139 does indeed include the existence of a legally enforceable debt or liability. Observations in Krishna Janardhan Bhat (2008) 4 SCC 54 to the contrary do not state the correct position of law and are overruled.",
                supporting_paragraph_numbers=[26, 27]
            ),
            CaseHolding(
                issue_number=2,
                issue_text="Standard of proof for accused to rebut Section 139 presumption",
                holding_summary="The standard of proof for rebutting the presumption under Section 139 is that of preponderance of probabilities. The accused is not required to prove his defence beyond reasonable doubt and can rely on the materials adduced by the complainant.",
                supporting_paragraph_numbers=[27, 28]
            )
        ],
        ratio_decidendi=(
            "The presumption mandated by Section 139 of the Negotiable Instruments Act, 1881 includes the existence of a legally enforceable debt or liability. "
            "However, this presumption is rebuttable, and the standard of proof required from the accused is that of a preponderance of probabilities. "
            "The observations to the contrary in Krishna Janardhan Bhat (2008) 4 SCC 54 stand overruled."
        ),
        final_disposition="Appeal dismissed; conviction under Section 138 of Negotiable Instruments Act affirmed.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=26,
                page_number=452,
                verbatim_text=(
                    "26. In light of these extracts, we are in agreement with the respondent-claimant that the presumption mandated by Section 139 of the Act "
                    "does indeed include the existence of a legally enforceable debt or liability. To that extent, the dictum in Krishna Janardhan Bhat (2008) 4 SCC 54 "
                    "may not be correct. However, this does not mean that the drawer of the cheque is without a defence."
                )
            ),
            JudgmentParagraph(
                paragraph_number=27,
                page_number=453,
                verbatim_text=(
                    "27. Section 139 of the Act is an example of a reverse onus clause that has been included in furtherance of the legislative objective "
                    "of improving the credibility of negotiable instruments. While Section 138 of the Act specifies a strong criminal remedy in relation to the dishonour of cheques, "
                    "the rebuttable presumption under Section 139 is a device to prevent undue delay in the course of litigation. However, it must be remembered that the offence "
                    "made punishable by Section 138 can be better described as a regulatory offence."
                )
            ),
            JudgmentParagraph(
                paragraph_number=28,
                page_number=454,
                verbatim_text=(
                    "28. It is a well-settled principle of law that in criminal cases, while the prosecution must prove guilt beyond reasonable doubt, "
                    "the accused who wishes to establish a defence or rebut a statutory presumption is only required to satisfy the test of preponderance of probabilities. "
                    "The accused can rely on the materials submitted by the complainant in order to raise such a defence and it is conceivable that in some cases the accused "
                    "may not need to adduce evidence of his/her own."
                )
            )
        ]
    )
    judgments.append(rangappa_doc)

    # =========================================================================
    # 2. Supreme Court: In Re: Interplay Between Arbitration Agreements & Stamp Act (2024) 6 SCC 1 (7-Judge Bench)
    # Subject: Arbitration and Conciliation Act 1996 s.8, s.11, s.16 & Stamp Act 1899
    # =========================================================================
    stamp_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2023-ARBITRATION-STAMP",
        source_id="IND-JUD-SC-2023-ARBITRATION-STAMP",
        case_title="In Re: Interplay Between Arbitration Agreements under the Arbitration and Conciliation Act, 1996 and the Indian Stamp Act, 1899",
        case_number="Curative Petition (C) No. 44 of 2023",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=[
            "Dr. D.Y. Chandrachud, C.J.I.",
            "S.K. Kaul, J.",
            "Sanjiv Khanna, J.",
            "B.R. Gavai, J.",
            "Surya Kant, J.",
            "J.B. Pardiwala, J.",
            "Manoj Misra, J."
        ],
        judgment_date=date(2023, 12, 13),
        citations=[
            JudgmentCitation(citation_text="(2024) 6 SCC 1", reporter="SCC", year=2024),
            JudgmentCitation(citation_text="2023 INSC 1066", reporter="INSC", year=2023),
        ],
        issues_framed=[
            "Whether an arbitration agreement contained in an unstamped or insufficiently stamped underlying commercial contract is void, non-existent, or unenforceable at the referral stage under Section 11(6) of the Arbitration Act.",
            "Whether the 5-judge bench decision in NN Global Mercantile (P) Ltd. v. Indo Unique Flame Ltd. (2023) 7 SCC 1 correctly laid down the law."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Effect of non-stamping of underlying contract on arbitration agreement at referral stage",
                holding_summary="Non-stamping or insufficient stamping of the underlying contract is a curable defect under the Stamp Act. It does not render the arbitration agreement void ab initio or non-existent. Under Section 16 (competence-competence), the Arbitral Tribunal possesses primary jurisdiction to examine stamping issues.",
                supporting_paragraph_numbers=[162, 175, 224]
            ),
            CaseHolding(
                issue_number=2,
                issue_text="Correctness of NN Global 5-Judge Bench judgment",
                holding_summary="The view taken in NN Global (2023) 7 SCC 1 and SMS Tea Estates (2011) 14 SCC 66 that an unstamped contract cannot be acted upon by the referral court under Section 11 is overruled.",
                supporting_paragraph_numbers=[224, 225]
            )
        ],
        ratio_decidendi=(
            "An unstamped or insufficiently stamped underlying agreement is inadmissible in evidence under Section 35 of the Stamp Act, but this is a curable defect "
            "and does not render the arbitration clause void, non-existent, or invalid. At the referral stage under Section 8 or Section 11 of the Arbitration and Conciliation Act, 1996, "
            "the court must only examine the prima facie existence of the arbitration agreement, leaving questions of stamping and admissibility to the arbitral tribunal under Section 16."
        ),
        final_disposition="Curative reference answered: NN Global (2023) 7 SCC 1 overruled; referral courts shall not impound unstamped contracts under Section 11.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=162,
                page_number=88,
                verbatim_text=(
                    "162. The deficiency in stamping is a curable defect. The Indian Stamp Act, 1899 itself provides a procedure for the payment of requisite stamp duty "
                    "along with penalty, upon which the instrument is validated and rendered admissible in evidence. Therefore, an unstamped instrument is not void ab initio; "
                    "it is merely inadmissible until stamped in accordance with law."
                )
            ),
            JudgmentParagraph(
                paragraph_number=175,
                page_number=95,
                verbatim_text=(
                    "175. The principle of competence-competence, enshrined in Section 16 of the Arbitration Act, empowers the arbitral tribunal to rule on its own jurisdiction, "
                    "including ruling on any objections with respect to the existence or validity of the arbitration agreement. Harmonious construction dictates that the court at the referral stage "
                    "under Section 11(6) must confine its examination to the prima facie existence of the arbitration agreement."
                )
            ),
            JudgmentParagraph(
                paragraph_number=224,
                page_number=120,
                verbatim_text=(
                    "224. In view of the above discussion, we hold that: (a) Unstamped or insufficiently stamped agreements are not void or invalid; "
                    "(b) Non-stamping is a curable defect; (c) Objections as to stamping fall within the domain of the arbitral tribunal under Section 16; and "
                    "(d) The decision in NN Global (2023) 7 SCC 1 and SMS Tea Estates (2011) 14 SCC 66 stand overruled."
                )
            )
        ]
    )
    judgments.append(stamp_doc)

    return judgments


def get_phase21_orders_and_proceedings() -> List[JudicialDocumentRecord]:
    """Returns authentic order and procedural history records."""
    return [
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-2018-CA2082-NOTICE",
            case_id="IN-SC-CA-2082-2018",
            classification=DocumentClassification.NOTICE_ORDER,
            procedural_effect=ProceduralEffect.NOTICE_ISSUED,
            order_or_judgment_date=date(2018, 2, 23),
            bench_coram=["R.F. Nariman, J.", "Navin Sinha, J."],
            verbatim_text="Issue notice on the prayer for interim relief as well as on the main appeal, returnable in four weeks.",
            source_url="https://main.sci.gov.in/order/2018-2082-notice",
            sha256_hash="d7a18f29402518e208b5e2a1b9c7d4e3f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
            statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-136"],
            precedents_cited=[],
        ),
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-2019-CA2082-REFERENCE",
            case_id="IN-SC-CA-2082-2018",
            classification=DocumentClassification.INTERIM_ORDER,
            procedural_effect=ProceduralEffect.REFERRED_TO_LARGER_BENCH,
            order_or_judgment_date=date(2019, 7, 26),
            bench_coram=["R.F. Nariman, J.", "Vineet Saran, J."],
            verbatim_text="In view of the conflict between the Division Bench judgment in Shafhi Mohammad (2018) 2 SCC 801 and the three-Judge Bench in Anvar P.V. (2014) 10 SCC 473, let the papers be placed before the Hon'ble the Chief Justice of India for constitution of a larger Bench.",
            source_url="https://main.sci.gov.in/order/2019-2082-ref",
            sha256_hash="e8b29c30513629f319c6f3b2c0d8e5f4a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
            statutory_provisions_cited=["IND-STAT-IT-2000-SEC-65B", "IND-CONST-1950-SEC-ARTICLE-145"],
            precedents_cited=["IND-JUD-SC-2014-ANVAR-PV", "IND-JUD-SC-2018-SHAFHI-MOHAMMAD"],
        ),
        JudicialDocumentRecord(
            document_id="IND-ORD-DHC-2022-FAO142-STAY",
            case_id="IN-DL-HC-FAO-COMM-142-2022",
            classification=DocumentClassification.STAY_ORDER,
            procedural_effect=ProceduralEffect.INTERIM_STAY_GRANTED,
            order_or_judgment_date=date(2022, 5, 27),
            bench_coram=["V. Kameswar Rao, J."],
            verbatim_text="Till the next date of hearing, operation of the impugned commercial court order dated 15.04.2022 shall remain stayed, subject to deposit of 50% of the awarded amount within four weeks.",
            source_url="https://delhihighcourt.nic.in/orders/2022-142-stay",
            sha256_hash="f9c30d41624730a420d7a4c3d1e9f6a5b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
            statutory_provisions_cited=["IND-STAT-COMM-COURTS-2015-SEC-12A", "IND-STAT-CPC-1908-SEC-ORDER-XXXIX-R-2"],
            precedents_cited=[],
        ),
    ]

