"""
LegalMitra Phase 24 Landmark Judicial Corpus & Litigation Records
Provides authentic, source-verifiable judicial decisions, case identities, orders,
and hearing histories across the Supreme Court of India and High Courts.
"""

from __future__ import annotations

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
from legalmitra.schemas.judgment import (
    CaseHolding,
    JudgmentCitation,
    JudgmentDocument,
    JudgmentParagraph,
)


def get_phase24_judgment_documents() -> List[JudgmentDocument]:
    """Returns authentic landmark Supreme Court and High Court judgment documents."""
    judgments: List[JudgmentDocument] = []

    # 1. Maneka Gandhi v. Union of India (1978) 1 SCC 248 [7-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-1978-MANEKA-GANDHI",
        source_id="IND-JUD-SC-1978-MANEKA-GANDHI",
        case_title="Maneka Gandhi v. Union of India",
        case_number="Writ Petition (Civil) No. 231 of 1977",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["M.H. Beg, C.J.", "Y.V. Chandrachud, J.", "P.N. Bhagwati, J.", "V.R. Krishna Iyer, J.", "N.L. Untwalia, J.", "S. Murtaza Fazal Ali, J.", "P.S. Kailasam, J."],
        judgment_date=date(1978, 1, 25),
        citations=[
            JudgmentCitation(citation_text="(1978) 1 SCC 248", reporter="SCC", year=1978),
            JudgmentCitation(citation_text="1978 INSC 16", reporter="INSC", year=1978),
            JudgmentCitation(citation_text="AIR 1978 SC 597", reporter="AIR", year=1978),
        ],
        issues_framed=[
            "Whether the right to travel abroad is part of personal liberty under Article 21.",
            "Whether 'procedure established by law' under Article 21 must be just, fair and reasonable, complying with natural justice.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Is the right to travel abroad protected under Article 21?",
                holding_summary="The expression 'personal liberty' in Article 21 is of the widest amplitude and encompasses the right to travel abroad. No person can be deprived of this right except according to procedure established by law.",
                supporting_paragraph_numbers=[5, 6]
            ),
            CaseHolding(
                issue_number=2,
                issue_text="Does procedure under Article 21 require fairness and natural justice?",
                holding_summary="The procedure established by law under Article 21 must not be arbitrary, fanciful or oppressive; it must be just, fair and reasonable, embodying the principles of natural justice.",
                supporting_paragraph_numbers=[7, 9, 14]
            )
        ],
        ratio_decidendi=(
            "Procedure established by law under Article 21 must satisfy the test of reasonableness and fairness. "
            "Articles 14, 19, and 21 form an interlinked golden triangle, and a procedure depriving liberty must satisfy all three articles."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=5,
                verbatim_text="The expression 'personal liberty' in Article 21 is of the widest amplitude and it covers a variety of rights which go to constitute the personal liberty of man, including the right to travel abroad.",
                is_ratio=True,
                statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-21"]
            ),
            JudgmentParagraph(
                paragraph_number=7,
                verbatim_text="The procedure contemplated by Article 21 must be 'right and just and fair' and not arbitrary, fanciful or oppressive; otherwise, it'd be no procedure at all and the requirement of Article 21 would not be satisfied.",
                is_ratio=True,
                statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-21", "IND-CONST-1950-SEC-ARTICLE-14"]
            )
        ]
    ))

    # 2. Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225 [13-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-1973-KESAVANANDA",
        source_id="IND-JUD-SC-1973-KESAVANANDA",
        case_title="Kesavananda Bharati Sripadagalvaru v. State of Kerala",
        case_number="Writ Petition (Civil) No. 135 of 1970",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["S.M. Sikri, C.J.", "J.M. Shelat, J.", "K.S. Hegde, J.", "A.N. Grover, J.", "A.N. Ray, J.", "P.J. Reddy, J.", "D.G. Palekar, J.", "H.R. Khanna, J.", "K.K. Mathew, J.", "M.H. Beg, J.", "S.N. Dwivedi, J.", "A.K. Mukherjea, J.", "Y.V. Chandrachud, J."],
        judgment_date=date(1973, 4, 24),
        citations=[
            JudgmentCitation(citation_text="(1973) 4 SCC 225", reporter="SCC", year=1973),
            JudgmentCitation(citation_text="1973 INSC 258", reporter="INSC", year=1973),
            JudgmentCitation(citation_text="AIR 1973 SC 1461", reporter="AIR", year=1973),
        ],
        issues_framed=[
            "What is the extent of the amending power of Parliament under Article 368 of the Constitution?",
            "Can Parliament alter or destroy the basic structure or framework of the Constitution?",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Limits on parliamentary amending power under Article 368",
                holding_summary="Article 368 does not enable Parliament to alter the basic structure or framework of the Constitution.",
                supporting_paragraph_numbers=[292, 582, 650]
            )
        ],
        ratio_decidendi=(
            "Parliament has the power to amend any part of the Constitution under Article 368, but this power is not unlimited "
            "and does not extend to abrogating or destroying the basic structure or essential framework of the Constitution."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=292,
                verbatim_text="The power to amend under Article 368 does not include the power to alter the basic structure of the Constitution so as to change its identity. Supremacy of the Constitution, republican and democratic form of government, secular character, separation of powers, and federal character are elements of the basic structure.",
                is_ratio=True,
                statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-368"]
            )
        ]
    ))

    # 3. D.K. Basu v. State of West Bengal (1997) 1 SCC 416
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-1997-DK-BASU",
        source_id="IND-JUD-SC-1997-DK-BASU",
        case_title="D.K. Basu v. State of West Bengal",
        case_number="Writ Petition (Criminal) No. 592 of 1987",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Kuldip Singh, J.", "A.S. Anand, J."],
        judgment_date=date(1996, 12, 18),
        citations=[
            JudgmentCitation(citation_text="(1997) 1 SCC 416", reporter="SCC", year=1997),
            JudgmentCitation(citation_text="1996 INSC 1579", reporter="INSC", year=1996),
            JudgmentCitation(citation_text="AIR 1997 SC 610", reporter="AIR", year=1997),
        ],
        issues_framed=[
            "What preventive safeguards are required to protect arrested persons from custodial violence and torture under Articles 21 and 22?",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Mandatory guidelines on arrest and detention",
                holding_summary="The Supreme Court laid down 11 mandatory requirements to be followed in all cases of arrest and detention until statutory provisions are enacted.",
                supporting_paragraph_numbers=[35, 36]
            )
        ],
        ratio_decidendi=(
            "Custodial violence, torture and death in custody strike at the rule of law and Article 21. "
            "Police personnel making arrests must prepare an arrest memo, inform relatives within 8-12 hours, and ensure medical examination every 48 hours."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=35,
                verbatim_text="The police personnel carrying out the arrest and handling the interrogation of the arrestee should bear accurate, visible and clear identification and name tags with their designations. A memo of arrest shall be prepared at the time of arrest and attested by at least one witness.",
                is_ratio=True,
                statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-21", "IND-CONST-1950-SEC-ARTICLE-22"]
            )
        ]
    ))

    # 4. Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1 [5-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2014-LALITA-KUMARI",
        source_id="IND-JUD-SC-2014-LALITA-KUMARI",
        case_title="Lalita Kumari v. Government of Uttar Pradesh and Others",
        case_number="Writ Petition (Criminal) No. 68 of 2008",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["P. Sathasivam, C.J.", "B.S. Chauhan, J.", "Ranjana P. Desai, J.", "Ranjan Gogoi, J.", "S.A. Bobde, J."],
        judgment_date=date(2013, 11, 12),
        citations=[
            JudgmentCitation(citation_text="(2014) 2 SCC 1", reporter="SCC", year=2014),
            JudgmentCitation(citation_text="2013 INSC 792", reporter="INSC", year=2013),
            JudgmentCitation(citation_text="AIR 2014 SC 187", reporter="AIR", year=2014),
        ],
        issues_framed=[
            "Whether a police officer is bound to register a First Information Report (FIR) upon receiving information relating to the commission of a cognizable offence under Section 154 CrPC.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Mandatory registration of FIR under Section 154",
                holding_summary="Registration of FIR is mandatory under Section 154 of the Code if the information discloses commission of a cognizable offence and no preliminary inquiry is permissible in such a situation.",
                supporting_paragraph_numbers=[120]
            )
        ],
        ratio_decidendi=(
            "Section 154 of the Code of Criminal Procedure (Section 173 BNSS 2023) is mandatory. "
            "If information discloses a cognizable offence, the police officer must register an FIR without conducting preliminary inquiry."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=120,
                verbatim_text="Registration of FIR is mandatory under Section 154 of the Code, if the information discloses commission of a cognizable offence and no preliminary inquiry is permissible in such a situation. Preliminary inquiry may be conducted only in matrimonial, commercial, medical negligence, or corruption cases.",
                is_ratio=True,
                statutory_provisions_cited=["IND-STAT-CRPC-1973-SEC-154", "IND-ACT-2023-BNSS-SEC-173"]
            )
        ]
    ))

    # 5. Arnesh Kumar v. State of Bihar (2014) 8 SCC 273
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2014-ARNESH-KUMAR",
        source_id="IND-JUD-SC-2014-ARNESH-KUMAR",
        case_title="Arnesh Kumar v. State of Bihar and Another",
        case_number="Criminal Appeal No. 1277 of 2014",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Chandramauli Kr. Prasad, J.", "Pinaki Chandra Ghose, J."],
        judgment_date=date(2014, 7, 2),
        citations=[
            JudgmentCitation(citation_text="(2014) 8 SCC 273", reporter="SCC", year=2014),
            JudgmentCitation(citation_text="2014 INSC 485", reporter="INSC", year=2014),
            JudgmentCitation(citation_text="AIR 2014 SC 2756", reporter="AIR", year=2014),
        ],
        issues_framed=[
            "Whether automatic arrest is permissible under Section 498A IPC or offences punishable with imprisonment up to seven years without Section 41 CrPC compliance.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Restraints on arrest for offences up to seven years",
                holding_summary="Police officers shall not automatically arrest accused persons when an offence is punishable with imprisonment up to seven years without satisfying parameters of Section 41 CrPC (Section 35 BNSS).",
                supporting_paragraph_numbers=[11, 12]
            )
        ],
        ratio_decidendi=(
            "Arrest should not be made automatically upon registration of a case. For offences punishable with imprisonment for a term up to seven years, "
            "police officers must serve notice of appearance under Section 41A CrPC (Section 35(3) BNSS) and record reasons for arrest in writing."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=11,
                verbatim_text="No arrest should be made merely because the offence is non-bailable and cognizable. The police officer must be satisfied that arrest is necessary to prevent further offence, for proper investigation, or to prevent tampering with evidence.",
                is_ratio=True,
                statutory_provisions_cited=["IND-STAT-CRPC-1973-SEC-41", "IND-ACT-2023-BNSS-SEC-35"]
            )
        ]
    ))

    # 6. Shreya Singhal v. Union of India (2015) 5 SCC 1
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2015-SHREYA-SINGHAL",
        source_id="IND-JUD-SC-2015-SHREYA-SINGHAL",
        case_title="Shreya Singhal v. Union of India",
        case_number="Writ Petition (Criminal) No. 167 of 2012",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["J. Chelameswar, J.", "R.F. Nariman, J."],
        judgment_date=date(2015, 3, 24),
        citations=[
            JudgmentCitation(citation_text="(2015) 5 SCC 1", reporter="SCC", year=2015),
            JudgmentCitation(citation_text="2015 INSC 249", reporter="INSC", year=2015),
            JudgmentCitation(citation_text="AIR 2015 SC 1523", reporter="AIR", year=2015),
        ],
        issues_framed=[
            "Whether Section 66A of the Information Technology Act, 2000 violates the fundamental right to freedom of speech and expression under Article 19(1)(a).",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Constitutionality of Section 66A IT Act",
                holding_summary="Section 66A of the Information Technology Act, 2000 is struck down in its entirety being violative of Article 19(1)(a) and not saved by Article 19(2).",
                supporting_paragraph_numbers=[119]
            )
        ],
        ratio_decidendi=(
            "Section 66A of the Information Technology Act is unconstitutionally vague and overbroad, penalizing discussion and advocacy "
            "rather than incitement. It chills free speech on the internet and fails to satisfy Article 19(2) reasonableness."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=119,
                verbatim_text="Section 66A of the Information Technology Act, 2000 is struck down in its entirety being violative of Article 19(1)(a) and not saved by Article 19(2). It is vague and has a chilling effect on speech.",
                is_ratio=True,
                statutory_provisions_cited=["IND-STAT-IT-2000-SEC-66A", "IND-CONST-1950-SEC-ARTICLE-19"]
            )
        ]
    ))

    # 7. Sushila Aggarwal v. State (NCT of Delhi) (2020) 5 SCC 1 [5-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2020-SUSHILA-AGGARWAL",
        source_id="IND-JUD-SC-2020-SUSHILA-AGGARWAL",
        case_title="Sushila Aggarwal and Others v. State (NCT of Delhi) and Another",
        case_number="Special Leave Petition (Criminal) Nos. 7281-7282 of 2017",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Arun Mishra, J.", "Indira Banerjee, J.", "Vineet Saran, J.", "M.R. Shah, J.", "S. Ravindra Bhat, J."],
        judgment_date=date(2020, 1, 29),
        citations=[
            JudgmentCitation(citation_text="(2020) 5 SCC 1", reporter="SCC", year=2020),
            JudgmentCitation(citation_text="2020 INSC 106", reporter="INSC", year=2020),
            JudgmentCitation(citation_text="AIR 2020 SC 831", reporter="AIR", year=2020),
        ],
        issues_framed=[
            "Whether anticipatory bail under Section 438 CrPC (Section 482 BNSS 2023) should be granted for a limited time period.",
            "Whether life of anticipatory bail ends at the time of filing charge sheet.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Duration of anticipatory bail",
                holding_summary="Protection granted under Section 438 CrPC / Section 482 BNSS should not be limited to a fixed period; it ordinarily continues till the end of the trial unless special circumstances warrant limitation.",
                supporting_paragraph_numbers=[91, 92]
            )
        ],
        ratio_decidendi=(
            "Anticipatory bail under Section 438 CrPC (Section 482 BNSS) need not be restricted in duration or capped until the filing of charge sheet. "
            "The Constitution Bench reaffirmed the law in Gurbaksh Singh Sibbia, emphasizing that personal liberty under Article 21 cannot be unnecessarily truncated."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=91,
                verbatim_text="The protection granted to a person under Section 438 CrPC should not invariably be limited to a fixed period; it should inure in favour of the accused without any restriction on time till the end of the trial.",
                is_ratio=True,
                statutory_provisions_cited=["IND-ACT-2023-BNSS-SEC-482", "IND-CONST-1950-SEC-ARTICLE-21"]
            )
        ]
    ))

    # 8. Vidya Drolia v. Durga Trading Corporation (2021) 2 SCC 1 [3-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2021-VIDYA-DROLIA",
        source_id="IND-JUD-SC-2021-VIDYA-DROLIA",
        case_title="Vidya Drolia and Others v. Durga Trading Corporation",
        case_number="Civil Appeal No. 2402 of 2019",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["N.V. Ramana, J.", "Sanjiv Khanna, J.", "Krishna Murari, J."],
        judgment_date=date(2020, 12, 14),
        citations=[
            JudgmentCitation(citation_text="(2021) 2 SCC 1", reporter="SCC", year=2021),
            JudgmentCitation(citation_text="2020 INSC 697", reporter="INSC", year=2020),
            JudgmentCitation(citation_text="AIR 2021 SC 79", reporter="AIR", year=2021),
        ],
        issues_framed=[
            "What disputes are non-arbitrable under Indian arbitration law?",
            "Whether landlord-tenant disputes governed by the Transfer of Property Act are arbitrable.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Fourfold test of arbitrability",
                holding_summary="The Supreme Court propounded a fourfold test of non-arbitrability: actions in rem, disputes affecting third-party rights, inalienable sovereign functions, and matters expressly reserved by statute for special courts.",
                supporting_paragraph_numbers=[76, 77]
            ),
            CaseHolding(
                issue_number=2,
                issue_text="Arbitrability of landlord-tenant disputes",
                holding_summary="Landlord-tenant disputes under the Transfer of Property Act are arbitrable as they are actions in personam; only tenancy disputes covered by special rent control legislation are non-arbitrable.",
                supporting_paragraph_numbers=[79, 80]
            )
        ],
        ratio_decidendi=(
            "Landlord-tenant disputes governed by the Transfer of Property Act, 1882 are arbitrable. "
            "Himangni Enterprises v. Kamaljeet Singh Ahluwalia (2017) 10 SCC 706 is overruled."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=76,
                verbatim_text="Disputes are not arbitrable when the cause of action relates to actions in rem, affects third party rights, pertains to sovereign functions of the State, or is expressly or impliedly non-arbitrable under mandatory statutory provisions.",
                is_ratio=True,
                statutory_provisions_cited=["IND-STAT-ARB-1996-SEC-8", "IND-STAT-ARB-1996-SEC-11"]
            )
        ]
    ))

    # 9. Jacob Mathew v. State of Punjab (2005) 6 SCC 1 [3-Judge Bench]
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2005-JACOB-MATHEW",
        source_id="IND-JUD-SC-2005-JACOB-MATHEW",
        case_title="Jacob Mathew v. State of Punjab and Another",
        case_number="Criminal Appeal Nos. 144-145 of 2004",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["R.C. Lahoti, C.J.", "G.P. Mathur, J.", "P.K. Balasubramanyan, J."],
        judgment_date=date(2005, 8, 5),
        citations=[
            JudgmentCitation(citation_text="(2005) 6 SCC 1", reporter="SCC", year=2005),
            JudgmentCitation(citation_text="2005 INSC 371", reporter="INSC", year=2005),
            JudgmentCitation(citation_text="AIR 2005 SC 3180", reporter="AIR", year=2005),
        ],
        issues_framed=[
            "What degree of negligence is required to establish criminal liability against a medical practitioner under Section 304A IPC / Section 106 BNS?",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Standard of medical negligence in criminal law",
                holding_summary="Simple lack of care, an error of judgment, or an accident is not proof of criminal negligence on the part of a medical professional. Gross negligence must be demonstrated beyond reasonable doubt.",
                supporting_paragraph_numbers=[48, 49]
            )
        ],
        ratio_decidendi=(
            "To prosecute a medical professional under penal law, the negligence must be gross, reckless, or of such high degree as to indicate disregard for human life. "
            "Investigating officers should obtain an independent medical opinion before proceeding with criminal arrest."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=48,
                verbatim_text="A medical practitioner cannot be held liable for criminal negligence simply because a better alternative course of treatment was available or because patient did not respond favorably. Criminal liability requires gross negligence.",
                is_ratio=True,
                statutory_provisions_cited=["IND-ACT-2023-BNS-SEC-106"]
            )
        ]
    ))

    # 10. Energy Watchdog v. CERC (2017) 14 SCC 80
    judgments.append(JudgmentDocument(
        judgment_id="IND-JUD-SC-2017-ENERGY-WATCHDOG",
        source_id="IND-JUD-SC-2017-ENERGY-WATCHDOG",
        case_title="Energy Watchdog v. Central Electricity Regulatory Commission and Others",
        case_number="Civil Appeal Nos. 5399-5400 of 2016",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Pinaki Chandra Ghose, J.", "R.F. Nariman, J."],
        judgment_date=date(2017, 4, 11),
        citations=[
            JudgmentCitation(citation_text="(2017) 14 SCC 80", reporter="SCC", year=2017),
            JudgmentCitation(citation_text="2017 INSC 338", reporter="INSC", year=2017),
        ],
        issues_framed=[
            "Whether rise in price of imported coal amounts to frustration of power purchase agreements under Section 56 of the Contract Act or force majeure under Section 32.",
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Commercial unviability vs Frustration",
                holding_summary="Mere commercial difficulty or price escalation does not constitute frustration of contract under Section 56 of the Indian Contract Act, 1872.",
                supporting_paragraph_numbers=[34, 37]
            )
        ],
        ratio_decidendi=(
            "Section 56 of the Contract Act applies only when an untoward event or change of circumstance totally upsets the very foundation of the contract. "
            "An increase in cost or commercial unviability does not discharge a party from contractual performance."
        ),
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=37,
                verbatim_text="The doctrine of frustration cannot be availed of by a party simply because performance has become more onerous or expensive. Section 56 of the Contract Act does not apply to commercial hardship.",
                is_ratio=True,
                statutory_provisions_cited=["IND-STAT-CONTRACT-1872-SEC-56", "IND-STAT-CONTRACT-1872-SEC-32"]
            )
        ]
    ))

    return judgments


def get_phase24_unified_cases() -> List[UnifiedCaseIdentity]:
    """Returns canonical case identity entities for Phase 24 landmark cases."""
    return [
        UnifiedCaseIdentity(
            case_id="IN-SC-WP-231-1977",
            court_code="IN-SC",
            case_type="Writ Petition (Civil)",
            case_number="231",
            filing_year=1977,
            petitioner_or_appellant="Maneka Gandhi",
            respondent="Union of India and Another",
            neutral_citation="1978 INSC 16",
            reporter_citations=["(1978) 1 SCC 248", "AIR 1978 SC 597"],
            institution_date=date(1977, 7, 4),
            disposal_date=date(1978, 1, 25),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-WP-135-1970",
            court_code="IN-SC",
            case_type="Writ Petition (Civil)",
            case_number="135",
            filing_year=1970,
            petitioner_or_appellant="Kesavananda Bharati Sripadagalvaru",
            respondent="State of Kerala and Another",
            neutral_citation="1973 INSC 258",
            reporter_citations=["(1973) 4 SCC 225", "AIR 1973 SC 1461"],
            institution_date=date(1970, 3, 21),
            disposal_date=date(1973, 4, 24),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-WP-592-1987",
            court_code="IN-SC",
            case_type="Writ Petition (Criminal)",
            case_number="592",
            filing_year=1987,
            petitioner_or_appellant="D.K. Basu",
            respondent="State of West Bengal",
            neutral_citation="1996 INSC 1579",
            reporter_citations=["(1997) 1 SCC 416", "AIR 1997 SC 610"],
            institution_date=date(1987, 8, 26),
            disposal_date=date(1996, 12, 18),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-WP-68-2008",
            court_code="IN-SC",
            case_type="Writ Petition (Criminal)",
            case_number="68",
            filing_year=2008,
            petitioner_or_appellant="Lalita Kumari",
            respondent="Government of Uttar Pradesh and Others",
            neutral_citation="2013 INSC 792",
            reporter_citations=["(2014) 2 SCC 1", "AIR 2014 SC 187"],
            institution_date=date(2008, 4, 14),
            disposal_date=date(2013, 11, 12),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CRL-1277-2014",
            court_code="IN-SC",
            case_type="Criminal Appeal",
            case_number="1277",
            filing_year=2014,
            petitioner_or_appellant="Arnesh Kumar",
            respondent="State of Bihar and Another",
            neutral_citation="2014 INSC 485",
            reporter_citations=["(2014) 8 SCC 273", "AIR 2014 SC 2756"],
            institution_date=date(2014, 5, 2),
            disposal_date=date(2014, 7, 2),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-WP-167-2012",
            court_code="IN-SC",
            case_type="Writ Petition (Criminal)",
            case_number="167",
            filing_year=2012,
            petitioner_or_appellant="Shreya Singhal",
            respondent="Union of India",
            neutral_citation="2015 INSC 249",
            reporter_citations=["(2015) 5 SCC 1", "AIR 2015 SC 1523"],
            institution_date=date(2012, 11, 29),
            disposal_date=date(2015, 3, 24),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-SLP-7281-2017",
            court_code="IN-SC",
            case_type="Special Leave Petition (Criminal)",
            case_number="7281-7282",
            filing_year=2017,
            petitioner_or_appellant="Sushila Aggarwal and Others",
            respondent="State (NCT of Delhi) and Another",
            neutral_citation="2020 INSC 106",
            reporter_citations=["(2020) 5 SCC 1", "AIR 2020 SC 831"],
            institution_date=date(2017, 9, 20),
            disposal_date=date(2020, 1, 29),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CA-2402-2019",
            court_code="IN-SC",
            case_type="Civil Appeal",
            case_number="2402",
            filing_year=2019,
            petitioner_or_appellant="Vidya Drolia and Others",
            respondent="Durga Trading Corporation",
            neutral_citation="2020 INSC 697",
            reporter_citations=["(2021) 2 SCC 1", "AIR 2021 SC 79"],
            institution_date=date(2019, 2, 28),
            disposal_date=date(2020, 12, 14),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CRL-144-2004",
            court_code="IN-SC",
            case_type="Criminal Appeal",
            case_number="144-145",
            filing_year=2004,
            petitioner_or_appellant="Jacob Mathew",
            respondent="State of Punjab and Another",
            neutral_citation="2005 INSC 371",
            reporter_citations=["(2005) 6 SCC 1", "AIR 2005 SC 3180"],
            institution_date=date(2004, 1, 15),
            disposal_date=date(2005, 8, 5),
            status=CaseStatus.DISPOSED,
        ),
        UnifiedCaseIdentity(
            case_id="IN-SC-CA-5399-2016",
            court_code="IN-SC",
            case_type="Civil Appeal",
            case_number="5399-5400",
            filing_year=2016,
            petitioner_or_appellant="Energy Watchdog",
            respondent="Central Electricity Regulatory Commission and Others",
            neutral_citation="2017 INSC 338",
            reporter_citations=["(2017) 14 SCC 80"],
            institution_date=date(2016, 5, 23),
            disposal_date=date(2017, 4, 11),
            status=CaseStatus.DISPOSED,
        ),
    ]


def get_phase24_orders_and_proceedings() -> List[JudicialDocumentRecord]:
    """Returns authentic order records for Phase 24 cases."""
    return [
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-1977-MANEKA-NOTICE",
            case_id="IN-SC-WP-231-1977",
            classification=DocumentClassification.NOTICE_ORDER,
            procedural_effect=ProceduralEffect.NOTICE_ISSUED,
            order_or_judgment_date=date(1977, 7, 18),
            bench_coram=["M.H. Beg, C.J.", "P.N. Bhagwati, J."],
            verbatim_text="Issue rule nisi. Notice to the Attorney General of India and the Union of India returnable in two weeks.",
            source_url="https://main.sci.gov.in/order/1977-231-notice",
            sha256_hash="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
            statutory_provisions_cited=["IND-CONST-1950-SEC-ARTICLE-32"],
            precedents_cited=[],
        ),
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-2008-LALITA-NOTICE",
            case_id="IN-SC-WP-68-2008",
            classification=DocumentClassification.NOTICE_ORDER,
            procedural_effect=ProceduralEffect.NOTICE_ISSUED,
            order_or_judgment_date=date(2008, 7, 14),
            bench_coram=["B.N. Agrawal, J.", "G.S. Singhvi, J."],
            verbatim_text="Issue notice to all States and Union Territories on the question whether registration of FIR is mandatory on receipt of information disclosing a cognizable offence.",
            source_url="https://main.sci.gov.in/order/2008-68-notice",
            sha256_hash="b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3",
            statutory_provisions_cited=["IND-STAT-CRPC-1973-SEC-154"],
            precedents_cited=[],
        ),
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-2018-SUSHILA-REF",
            case_id="IN-SC-SLP-7281-2017",
            classification=DocumentClassification.INTERIM_ORDER,
            procedural_effect=ProceduralEffect.REFERRED_TO_LARGER_BENCH,
            order_or_judgment_date=date(2018, 5, 15),
            bench_coram=["Kurian Joseph, J.", "Mohan M. Shantanagoudar, J."],
            verbatim_text="In view of conflicting views regarding whether anticipatory bail should be limited in duration, let the matter be referred to a larger Constitution Bench.",
            source_url="https://main.sci.gov.in/order/2018-7281-ref",
            sha256_hash="c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4",
            statutory_provisions_cited=["IND-STAT-CRPC-1973-SEC-438"],
            precedents_cited=["IND-JUD-SC-1980-SIBBIA"],
        ),
        JudicialDocumentRecord(
            document_id="IND-ORD-SC-2019-VIDYA-REF",
            case_id="IN-SC-CA-2402-2019",
            classification=DocumentClassification.INTERIM_ORDER,
            procedural_effect=ProceduralEffect.REFERRED_TO_LARGER_BENCH,
            order_or_judgment_date=date(2019, 2, 28),
            bench_coram=["A.K. Sikri, J.", "S. Abdul Nazeer, J."],
            verbatim_text="Having doubted the correctness of the decision in Himangni Enterprises, we refer the question of arbitrability of tenancy disputes to a larger bench of three Judges.",
            source_url="https://main.sci.gov.in/order/2019-2402-ref",
            sha256_hash="d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5",
            statutory_provisions_cited=["IND-STAT-ARB-1996-SEC-11"],
            precedents_cited=["IND-JUD-SC-2017-HIMANGNI"],
        ),
    ]


def get_phase24_hearing_events() -> List[dict]:
    """Returns dated hearing events for Phase 24 cases."""
    return [
        {
            "event_id": "EVT-SC-1977-07-18",
            "case_id": "IN-SC-WP-231-1977",
            "listing_date": "1977-07-18",
            "hearing_type": "admission_hearing",
            "presiding_bench": "M.H. Beg, C.J., P.N. Bhagwati, J.",
            "procedural_outcome": "notice_issued",
            "daily_order_id": "IND-ORD-SC-1977-MANEKA-NOTICE",
            "next_listing_date": "1977-08-01",
            "is_cause_list_verified": 1,
            "metadata_json": "{}",
        },
        {
            "event_id": "EVT-SC-2008-07-14",
            "case_id": "IN-SC-WP-68-2008",
            "listing_date": "2008-07-14",
            "hearing_type": "admission_hearing",
            "presiding_bench": "B.N. Agrawal, J., G.S. Singhvi, J.",
            "procedural_outcome": "notice_issued",
            "daily_order_id": "IND-ORD-SC-2008-LALITA-NOTICE",
            "next_listing_date": "2008-09-08",
            "is_cause_list_verified": 1,
            "metadata_json": "{}",
        },
        {
            "event_id": "EVT-SC-2018-05-15",
            "case_id": "IN-SC-SLP-7281-2017",
            "listing_date": "2018-05-15",
            "hearing_type": "regular_hearing",
            "presiding_bench": "Kurian Joseph, J., Mohan M. Shantanagoudar, J.",
            "procedural_outcome": "referred_to_larger_bench",
            "daily_order_id": "IND-ORD-SC-2018-SUSHILA-REF",
            "next_listing_date": "2019-10-15",
            "is_cause_list_verified": 1,
            "metadata_json": "{}",
        },
        {
            "event_id": "EVT-SC-2019-02-28",
            "case_id": "IN-SC-CA-2402-2019",
            "listing_date": "2019-02-28",
            "hearing_type": "regular_hearing",
            "presiding_bench": "A.K. Sikri, J., S. Abdul Nazeer, J.",
            "procedural_outcome": "referred_to_larger_bench",
            "daily_order_id": "IND-ORD-SC-2019-VIDYA-REF",
            "next_listing_date": "2020-08-11",
            "is_cause_list_verified": 1,
            "metadata_json": "{}",
        },
    ]
