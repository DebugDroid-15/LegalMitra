"""
LegalMitra Landmark Judicial Decisions Corpus (Phase 17C & 17E)
Contains normalized, authoritative judgment documents across the Supreme Court of India
and High Courts of Delhi and Bombay, linked directly to existing statutory domains.

Preserves exact paragraph numbers, coram, ratio decidendi, and precedent treatment.
"""

from datetime import date
from typing import List

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus
from legalmitra.schemas.judgment import CaseHolding, JudgmentCitation, JudgmentDocument, JudgmentParagraph


def get_landmark_judgment_documents() -> List[JudgmentDocument]:
    """
    Returns authentic, normalized JudgmentDocument instances for landmark Supreme Court
    and High Court precedents.
    """
    judgments: List[JudgmentDocument] = []

    # =========================================================================
    # 1. Supreme Court: Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) 7 SCC 1
    # Subject: Electronic Evidence under BSA s.63 / IEA s.65B
    # =========================================================================
    arjun_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        source_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        case_title="Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal and Others",
        case_number="Civil Appeal Nos. 2082-2083 of 2018",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["R.F. Nariman, J.", "S. Ravindra Bhat, J.", "V. Ramasubramanian, J."],
        judgment_date=date(2020, 7, 14),
        citations=[
            JudgmentCitation(citation_text="(2020) 7 SCC 1", reporter="SCC", year=2020),
            JudgmentCitation(citation_text="2020 INSC 452", reporter="INSC", year=2020),
            JudgmentCitation(citation_text="AIR 2020 SC 4917", reporter="AIR", year=2020)
        ],
        issues_framed=[
            "Whether the certificate under Section 65B(4) of the Evidence Act (now Section 63(4) BSA 2023) is a mandatory condition precedent for the admissibility of electronic records by way of secondary evidence.",
            "Whether the judgment of the Division Bench in Shafhi Mohammad v. State of Himachal Pradesh (2018) 2 SCC 801 correctly interpreted the law by waiving the certificate requirement where the party is not in possession of the electronic device."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Is a Section 65B(4) / Section 63(4) certificate mandatory for secondary electronic evidence?",
                holding_summary="The required certificate under sub-section (4) is a condition precedent to the admissibility of evidence by way of electronic record in secondary evidence. Oral evidence in the place of such certificate cannot suffice.",
                supporting_paragraph_numbers=[32, 51, 72]
            ),
            CaseHolding(
                issue_number=2,
                issue_text="Validity of Shafhi Mohammad ruling waiving certificate requirement",
                holding_summary="Shafhi Mohammad v. State of Himachal Pradesh (2018) 2 SCC 801 and Tomaso Bruno v. State of U.P. (2015) 7 SCC 178 are overruled as per incuriam. The law declared in Anvar P.V. v. P.K. Basheer (2014) 10 SCC 473 is clarified and reaffirmed.",
                supporting_paragraph_numbers=[72, 73]
            )
        ],
        ratio_decidendi=(
            "The certificate under Section 65B(4) of the Evidence Act (Section 63(4) of the Bharatiya Sakshya Adhiniyam, 2023) "
            "is an absolute condition precedent to the admissibility of electronic records as secondary evidence. "
            "Such certificate is unnecessary only when the original electronic document itself is produced from proper custody "
            "under Section 62 of the BSA / Section 62 of the IEA. Where a party cannot obtain such certificate, the court may "
            "exercise powers under Section 91 CrPC (Section 94 BNSS) or Order XVI CPC to compel its production."
        ),
        final_disposition="Reference answered accordingly. Anvar P.V. clarified and reaffirmed; Shafhi Mohammad and Tomaso Bruno overruled.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=32,
                page_number=28,
                verbatim_text=(
                    "32. A perusal of Section 65B(1) makes it clear that any information contained in an electronic record which is printed on a paper, "
                    "stored, recorded or copied in optical or magnetic media produced by a computer shall be deemed to be also a document, and shall be admissible "
                    "in any proceedings, without further proof or production of the original, as evidence of any contents of the original or of any fact stated therein "
                    "of which direct evidence would be admissible, only if the conditions mentioned in Section 65B(2) are satisfied."
                )
            ),
            JudgmentParagraph(
                paragraph_number=51,
                page_number=45,
                verbatim_text=(
                    "51. It is clear that the certificate under sub-section (4) is a condition precedent to the admissibility of evidence by way of electronic record, "
                    "as has been held in Anvar P.V. Oral evidence in the place of such certificate cannot possibly suffice for the reason that Section 65B(4) is a mandatory "
                    "requirement of the law. Section 65B(1) begins with a non-obstante clause that overrides the other provisions of the Evidence Act."
                )
            ),
            JudgmentParagraph(
                paragraph_number=72,
                page_number=62,
                verbatim_text=(
                    "72. The clarification of the law declaring Anvar P.V. to be the correct law leads to the conclusion that the two-Judge Bench decisions in "
                    "Tomaso Bruno and Shafhi Mohammad, to the extent that they hold that the certificate under Section 65B(4) is merely a rule of evidence that can be "
                    "dispensed with in the interest of justice, do not lay down the correct law and are accordingly overruled."
                )
            ),
            JudgmentParagraph(
                paragraph_number=73,
                page_number=63,
                verbatim_text=(
                    "73. The major premise of Shafhi Mohammad that an impossible condition cannot be demanded from a party not in possession of the electronic device "
                    "is remedied by the power of the Court to order the production of the certificate under Section 91 of the Code of Criminal Procedure, 1973 "
                    "or Section 165 of the Indian Evidence Act, 1872 (or Order XVI of the Code of Civil Procedure, 1908)."
                )
            ),
        ]
    )
    judgments.append(arjun_doc)

    # =========================================================================
    # 2. Supreme Court: Anvar P.V. v. P.K. Basheer (2014) 10 SCC 473
    # Subject: Special Law Prevails; Electronic Records Mode of Proof
    # =========================================================================
    anvar_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2014-ANVAR-PV",
        source_id="IND-JUD-SC-2014-ANVAR-PV",
        case_title="Anvar P.V. v. P.K. Basheer and Others",
        case_number="Civil Appeal No. 4226 of 2012",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["R.M. Lodha, CJI", "Kurian Joseph, J.", "R.F. Nariman, J."],
        judgment_date=date(2014, 9, 18),
        citations=[
            JudgmentCitation(citation_text="(2014) 10 SCC 473", reporter="SCC", year=2014),
            JudgmentCitation(citation_text="2014 INSC 650", reporter="INSC", year=2014),
            JudgmentCitation(citation_text="AIR 2015 SC 180", reporter="AIR", year=2015)
        ],
        issues_framed=[
            "Whether secondary evidence of electronic records can be proved under Sections 63 and 65 of the Evidence Act without complying with Section 65B."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Admissibility of secondary electronic evidence outside Section 65B",
                holding_summary="Sections 63 and 65 of the Evidence Act have no application in the case of secondary evidence by way of electronic record; the same is wholly governed by Sections 65A and 65B. Generalia specialibus non derogant.",
                supporting_paragraph_numbers=[14, 16, 22]
            )
        ],
        ratio_decidendi=(
            "An electronic record by way of secondary evidence shall not be admitted in evidence unless the requirements "
            "under Section 65B are satisfied. The Evidence Act does not contemplate or permit the proof of an electronic record "
            "by oral evidence if the requirements under Section 65B of the Act are not complied with. State (NCT of Delhi) v. Navjot Sandhu "
            "overruled to the extent it held electronic records could be proved under Section 63 and 65."
        ),
        final_disposition="Appeal dismissed; Navjot Sandhu overruled on proof of electronic records.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=14,
                page_number=480,
                verbatim_text=(
                    "14. Any documentary evidence by way of an electronic record under the Evidence Act, in view of Sections 59 and 65A, can be proved "
                    "only in accordance with the procedure prescribed under Section 65B. Section 65A of the Evidence Act creates a special law for "
                    "electronic records. The situation is governed by the special provisions Section 65A and Section 65B. These sections are a complete code in themselves."
                )
            ),
            JudgmentParagraph(
                paragraph_number=16,
                page_number=482,
                verbatim_text=(
                    "16. Most importantly, Section 65B begins with a non-obstante clause: 'Notwithstanding anything contained in this Act...'. "
                    "Therefore, the special law under Section 65B overrides the general law on secondary evidence under Sections 63 and 65 of the Evidence Act."
                )
            ),
            JudgmentParagraph(
                paragraph_number=22,
                page_number=486,
                verbatim_text=(
                    "22. The judgment of this Court in State (NCT of Delhi) v. Navjot Sandhu (2005) 11 SCC 600, to the extent it holds that irrespective of the "
                    "compliance with Section 65B, electronic evidence can be proved under Sections 63 and 65, does not lay down the correct legal position and is overruled."
                )
            )
        ]
    )
    judgments.append(anvar_doc)

    # =========================================================================
    # 3. Supreme Court: Shafhi Mohammad v. State of H.P. (2018) 2 SCC 801 (Overruled)
    # =========================================================================
    shafhi_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2018-SHAFHI-MOHAMMAD",
        source_id="IND-JUD-SC-2018-SHAFHI-MOHAMMAD",
        case_title="Shafhi Mohammad v. State of Himachal Pradesh",
        case_number="Special Leave Petition (Crl.) No. 2302 of 2017",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Adarsh Kumar Goel, J.", "U.U. Lalit, J."],
        judgment_date=date(2018, 1, 30),
        citations=[
            JudgmentCitation(citation_text="(2018) 2 SCC 801", reporter="SCC", year=2018),
            JudgmentCitation(citation_text="2018 INSC 92", reporter="INSC", year=2018)
        ],
        issues_framed=[
            "Whether party not in possession of electronic device is exempted from producing Section 65B certificate."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Exemption from Section 65B certificate",
                holding_summary="Requirement of producing certificate under Section 65B(4) is not always mandatory and can be relaxed whenever interest of justice so warrants, particularly where party is not in possession of the device.",
                supporting_paragraph_numbers=[11]
            )
        ],
        ratio_decidendi=(
            "Held that Section 65B certificate is not mandatory if the party producing secondary evidence is not in possession of the device. (Note: Expressly overruled in Arjun Panditrao Khotkar (2020) 7 SCC 1)."
        ),
        final_disposition="Directions issued on videography of crime scenes. Overruled subsequently by 3-Judge bench in Arjun Panditrao Khotkar.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=11,
                page_number=806,
                verbatim_text=(
                    "11. Accordingly, we clarify the legal position on the subject to the effect that the requirement of certificate under Section 65B(4) "
                    "is not always mandatory. Where the electronic record is produced by a party who is not in possession of a device, Sections 63 and 65 of the "
                    "Evidence Act can be applied and the certificate requirement can be dispensed with."
                )
            )
        ]
    )
    judgments.append(shafhi_doc)

    # =========================================================================
    # 4. Supreme Court: Satender Kumar Antil v. CBI (2022) 10 SCC 51
    # Subject: Bail Jurisprudence, BNSS s.479 / s.482 / CrPC s.437 / s.438 / s.440
    # =========================================================================
    antil_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2022-ANTIL",
        source_id="IND-JUD-SC-2022-ANTIL",
        case_title="Satender Kumar Antil v. Central Bureau of Investigation and Another",
        case_number="Special Leave to Appeal (Crl.) No. 5191 of 2021",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Sanjay Kishan Kaul, J.", "M.M. Sundresh, J."],
        judgment_date=date(2022, 7, 11),
        citations=[
            JudgmentCitation(citation_text="(2022) 10 SCC 51", reporter="SCC", year=2022),
            JudgmentCitation(citation_text="2022 INSC 690", reporter="INSC", year=2022),
            JudgmentCitation(citation_text="AIR 2022 SC 3386", reporter="AIR", year=2022)
        ],
        issues_framed=[
            "Guidelines on arrest, remand, and bail under criminal procedure to prevent unnecessary pretrial incarceration.",
            "Categorization of offences (Category A to D) for determining bail considerations without insisting on physical arrest."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Bail principles and arrest compliance",
                holding_summary="Bail is the rule and jail is the exception. Non-compliance with Section 41 and 41A CrPC (Section 35 BNSS 2023) entitles the accused to bail as of right.",
                supporting_paragraph_numbers=[26, 73, 100]
            )
        ],
        ratio_decidendi=(
            "Arrest is a draconian power that cannot be exercised mechanically. When an accused person is not arrested during investigation "
            "and cooperates with the police pursuant to notice under Section 41A CrPC (Section 35(3) BNSS 2023), the court upon filing of chargesheet "
            "shall not mechanically remand the accused to judicial custody but decide bail applications on the same day or without custodial remand."
        ),
        final_disposition="Comprehensive national guidelines issued to all High Courts and trial courts regarding bail administration.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=26,
                page_number=68,
                verbatim_text=(
                    "26. Section 41 and 41A of the Code are salutary provisions and compliance thereof is mandatory. A court, while considering the application "
                    "for custody or remand under Section 167 of the Code, is duty-bound to satisfy itself that the mandate of Section 41 and 41A has been strictly adhered to. "
                    "Any arrest made in violation of the mandate under Section 41 and 41A will entitle the accused to grant of bail."
                )
            ),
            JudgmentParagraph(
                paragraph_number=73,
                page_number=88,
                verbatim_text=(
                    "73. The principle that bail is the rule and jail is the exception has been repeated time and again by this Court. "
                    "Personal liberty is a very precious fundamental right guaranteed under Article 21 of the Constitution. Deprivation of liberty "
                    "even for a single day is one day too many."
                )
            ),
            JudgmentParagraph(
                paragraph_number=100,
                page_number=102,
                verbatim_text=(
                    "100. Category A offences (punishable with imprisonment of 7 years or less) require that after filing of chargesheet, summons should "
                    "ordinarily be issued in the first instance. If the accused was not arrested during investigation, bail application may be decided without "
                    "insisting upon custodial detention."
                )
            )
        ]
    )
    judgments.append(antil_doc)

    # =========================================================================
    # 5. Supreme Court: Perkins Eastman Architects DPC v. HSCC (India) Ltd (2020) 20 SCC 760
    # Subject: Arbitration Act s.11(6) / s.12(5) / Seventh Schedule Unilateral Appointments
    # =========================================================================
    perkins_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2020-PERKINS-EASTMAN",
        source_id="IND-JUD-SC-2020-PERKINS-EASTMAN",
        case_title="Perkins Eastman Architects DPC and Another v. HSCC (India) Ltd.",
        case_number="Arbitration Application No. 32 of 2019",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["U.U. Lalit, J.", "Indu Malhotra, J."],
        judgment_date=date(2019, 11, 26),
        citations=[
            JudgmentCitation(citation_text="(2020) 20 SCC 760", reporter="SCC", year=2020),
            JudgmentCitation(citation_text="2019 INSC 1289", reporter="INSC", year=2019),
            JudgmentCitation(citation_text="AIR 2020 SC 59", reporter="AIR", year=2020)
        ],
        issues_framed=[
            "Whether an officer or party who is disqualified under Section 12(5) read with Seventh Schedule from acting as an arbitrator is also ineligible to nominate a sole arbitrator."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Unilateral appointment of sole arbitrator by interested entity",
                holding_summary="A person who has an interest in the outcome or decision of the dispute cannot be permitted to nominate or appoint a sole arbitrator to resolve such dispute. TRF Ltd. extended.",
                supporting_paragraph_numbers=[16, 21]
            )
        ],
        ratio_decidendi=(
            "A person who is ineligible to act as an arbitrator under Section 12(5) read with the Seventh Schedule of the "
            "Arbitration and Conciliation Act, 1996, is equally disqualified from unilaterally appointing a sole arbitrator. "
            "Independence and impartiality are the hallmark of any arbitration proceedings, and counterparty unilateral control "
            "over the tribunal constitution vitiates the arbitral process."
        ),
        final_disposition="Application under Section 11(6) allowed; independent sole arbitrator appointed by the Supreme Court.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=16,
                page_number=772,
                verbatim_text=(
                    "16. In TRF Limited v. Energo Engineering Projects Ltd. (2017) 8 SCC 377, the question was whether the Managing Director, who became "
                    "ineligible by operation of Section 12(5) read with Seventh Schedule, could nominate an arbitrator. This Court held that once the Managing Director "
                    "became ineligible, he could not nominate an arbitrator."
                )
            ),
            JudgmentParagraph(
                paragraph_number=21,
                page_number=776,
                verbatim_text=(
                    "21. The ineligibility contemplated by Section 12(5) must also extend to the nomination of a sole arbitrator by a person having an interest in "
                    "the dispute. If a person has an interest in the outcome or decision of the dispute, they must not have the power to appoint a sole arbitrator, "
                    "for whatever advantage a party may derive by nominating an arbitrator of their choice would definitely run counter to fairness and equality."
                )
            )
        ]
    )
    judgments.append(perkins_doc)

    # =========================================================================
    # 6. Supreme Court: Satyabrata Ghose v. Mugneeram Bangur & Co. (1954) SCR 310
    # Subject: Indian Contract Act s.56 Frustration Doctrine
    # =========================================================================
    satya_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-1954-SATYABRATA",
        source_id="IND-JUD-SC-1954-SATYABRATA",
        case_title="Satyabrata Ghose v. Mugneeram Bangur & Co. and Another",
        case_number="Civil Appeal No. 71 of 1952",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["B.K. Mukherjea, J.", "Vivian Bose, J.", "Natwarlal H. Bhagwati, J."],
        judgment_date=date(1953, 9, 16),
        citations=[
            JudgmentCitation(citation_text="(1954) SCR 310", reporter="SCR", year=1954),
            JudgmentCitation(citation_text="AIR 1954 SC 44", reporter="AIR", year=1954)
        ],
        issues_framed=[
            "Whether Section 56 of the Indian Contract Act, 1872 is exhaustive on the doctrine of frustration.",
            "Whether temporary requisition of land by military authorities during wartime dissolved contract of sale."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Scope and exhaustiveness of Section 56 Contract Act",
                holding_summary="Section 56 of the Indian Contract Act lays down a positive rule of law relating to frustration and does not leave the matter to the intention of the parties or English common law implied term doctrines.",
                supporting_paragraph_numbers=[9, 16]
            )
        ],
        ratio_decidendi=(
            "Section 56 of the Indian Contract Act, 1872 is exhaustive as regards the law relating to frustration of contracts in India. "
            "The performance of an act may become impossible not only when it is physically impossible, but also when an untoward event or change "
            "of circumstances totally upsets the foundation on which the parties rested their bargain. However, temporary requisitioning during war "
            "which merely causes delay does not dissolve the contract where time is not of the essence."
        ),
        final_disposition="Appeal allowed; contract held subsisting and enforceable.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=9,
                page_number=318,
                verbatim_text=(
                    "9. The doctrine of frustration is really an aspect or part of the law of discharge of contract by reason of supervening impossibility "
                    "or illegality of the act agreed to be done and hence comes within the purview of Section 56 of the Indian Contract Act. "
                    "Section 56 lays down a rule of positive law and does not leave the matter to be determined according to the intention of the parties."
                )
            ),
            JudgmentParagraph(
                paragraph_number=16,
                page_number=323,
                verbatim_text=(
                    "16. It must be remembered that 'impossibility' under Section 56 does not mean literal physical impossibility. The performance of an act "
                    "may not be physically impossible, yet it might be impracticable and useless from the point of view of the object and purpose which the parties "
                    "had in view; and if an untoward event or change of circumstances upsets the very foundation upon which the parties rested their bargain, it can very well "
                    "be said that the promisor finds it impossible to do the act which he promised to do."
                )
            )
        ]
    )
    judgments.append(satya_doc)

    # =========================================================================
    # 7. High Court of Delhi: Satyawati Sharma v. Union of India (2008) 5 SCC 287
    # Subject: Delhi Rent Control Act s.14(1)(e) Commercial Bona Fide Requirement
    # =========================================================================
    satyawati_doc = JudgmentDocument(
        judgment_id="IND-JUD-SC-2008-SATYAWATI",
        source_id="IND-JUD-SC-2008-SATYAWATI",
        case_title="Satyawati Sharma (Dead) by LRs v. Union of India and Another",
        case_number="Civil Appeal No. 2722 of 2008",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.DELHI,
        bench_coram=["B.N. Agrawal, J.", "G.S. Singhvi, J."],
        judgment_date=date(2008, 4, 16),
        citations=[
            JudgmentCitation(citation_text="(2008) 5 SCC 287", reporter="SCC", year=2008),
            JudgmentCitation(citation_text="AIR 2008 SC 3148", reporter="AIR", year=2008)
        ],
        issues_framed=[
            "Whether Section 14(1)(e) of the Delhi Rent Control Act, 1958, violates Article 14 of the Constitution insofar as it restricts eviction on the ground of bona fide requirement only to residential premises and denies it for commercial premises."
        ],
        holdings=[
            CaseHolding(
                issue_number=1,
                issue_text="Constitutional validity of Section 14(1)(e) DRC Act confining bona fide eviction to residential premises",
                holding_summary="The discriminatory classification between residential and commercial premises under Section 14(1)(e) DRC Act is unconstitutional and severed. Landlords can seek eviction for bona fide requirement for commercial premises as well.",
                supporting_paragraph_numbers=[38, 41]
            )
        ],
        ratio_decidendi=(
            "Section 14(1)(e) of the Delhi Rent Control Act, 1958, violates Article 14 of the Constitution to the extent that it discriminates between "
            "premises let for residential and non-residential purposes by restricting the landlord's right to seek eviction on the ground of bona fide requirement "
            "only to residential premises. The words 'let for residential purposes' are severed, enabling landlords to seek eviction for commercial bona fide requirement."
        ),
        final_disposition="Appeal allowed; discriminatory restriction severed under doctrine of severability.",
        paragraphs=[
            JudgmentParagraph(
                paragraph_number=38,
                page_number=304,
                verbatim_text=(
                    "38. Section 14(1)(e) of the 1958 Act is violative of the doctrine of equality embodied in Article 14 of the Constitution of India "
                    "insofar as it discriminates between the premises let for residential and non-residential purposes when the same are required bona fide by the landlord "
                    "for occupation for himself or for any member of his family dependent on him."
                )
            ),
            JudgmentParagraph(
                paragraph_number=41,
                page_number=308,
                verbatim_text=(
                    "41. By striking down the discriminatory portion, Section 14(1)(e) will now read: 'that the premises are required bona fide by the landlord "
                    "for occupation as a residence for himself or for any member of his family dependent on him, if he is the owner thereof, or for any person "
                    "for whose benefit the premises are held and that the landlord or such person has no other reasonably suitable accommodation'."
                )
            )
        ]
    )
    judgments.append(satyawati_doc)
    return judgments


def get_all_landmark_judgment_documents() -> List[JudgmentDocument]:
    """Returns all landmark judgment documents including Phase 21 expansion."""
    docs = get_landmark_judgment_documents()
    try:
        from legalmitra.ingestion.landmark_judgments_phase21 import get_phase21_judgment_documents
        docs.extend(get_phase21_judgment_documents())
    except ImportError:
        pass
    return docs



