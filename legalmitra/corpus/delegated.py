"""
LegalMitra Delegated Legislation Models & Subordinate Legal Instruments
Defines subordinate instruments (Rules, Regulations, Commencement Notifications)
promulgated under central or state parent statutes.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.schemas.statute import StatuteDocument, StatuteSection


class DelegatedInstrumentMetadata(BaseModel):
    """
    Subordinate instrument metadata linking rules/notifications to parent statutes.
    """
    document_id: str = Field(..., description="Unique instrument ID, e.g. 'IND-RULE-IT-SPDI-2011'")
    title: str = Field(..., description="Official title of the rules, regulations, or notification")
    instrument_type: SourceType = Field(default=SourceType.RULES_REGULATION)
    parent_act_id: str = Field(..., description="Document ID of parent Act, e.g. 'IND-STAT-IT-2000'")
    parent_act_title: str = Field(..., description="Short title of parent Act")
    enabling_section: str = Field(..., description="Section of parent Act conferring rule-making power (e.g. 'Section 43A read with Section 87')")
    gazette_notification_number: str = Field(..., description="e.g. 'G.S.R. 313(E)' or 'S.O. 848(E)'")
    ministry_or_authority: str = Field(..., description="Issuing Ministry, Department, or Regulatory Authority")
    notification_date: date = Field(..., description="Date of notification in the Gazette of India")
    commencement_date: Optional[date] = Field(default=None, description="Date of entry into force")
    source_url: str = Field(..., description="Authoritative portal URL (egazette.gov.in / indiacode.nic.in)")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    is_commencement_notification: bool = Field(default=False)
    target_enactment_ids: List[str] = Field(default_factory=list, description="Target Act IDs commenced by this notification")


def get_delegated_instruments() -> List[StatuteDocument]:
    """
    Builds normalized StatuteDocuments for high-priority Central subordinate rules
    and key commencement notifications.
    """
    instruments: List[StatuteDocument] = []

    # 1. SPDI Rules 2011 under IT Act 2000
    spdi_doc = StatuteDocument(
        source_id="IND-RULE-IT-SPDI-2011",
        act_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
        act_number="G.S.R. 313(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2011, 4, 11),
        effective_date=date(2011, 4, 11),
        preamble="Rules framed by the Central Government in exercise of powers conferred by clause (ob) of sub-section (2) of section 87 read with section 43A of the Information Technology Act, 2000.",
        sections=[
            StatuteSection(
                section_id="IND-RULE-IT-SPDI-2011:RULE:3",
                source_id="IND-RULE-IT-SPDI-2011",
                act_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
                section_number="Rule 3",
                section_title="Sensitive personal data or information",
                full_verbatim_text=(
                    "Rule 3. Sensitive personal data or information.—Sensitive personal data or information of a person means "
                    "such personal information which consists of information relating to;—\n"
                    "(i) password;\n"
                    "(ii) financial information such as Bank account or credit card or debit card or other payment instrument details;\n"
                    "(iii) physical, physiological and mental health condition;\n"
                    "(iv) sexual orientation;\n"
                    "(v) medical records and history;\n"
                    "(vi) Biometric information;\n"
                    "(vii) any detail relating to the above clauses as provided to body corporate for providing service; and\n"
                    "(viii) any of the information received under above clauses by body corporate for processing, stored or processed under lawful contract or otherwise:\n"
                    "Provided that, any information that is freely available or accessible in public domain or furnished under the Right to Information Act, 2005 "
                    "or any other law for the time being in force shall not be regarded as sensitive personal data or information for the purposes of these rules."
                ),
            ),
            StatuteSection(
                section_id="IND-RULE-IT-SPDI-2011:RULE:4",
                source_id="IND-RULE-IT-SPDI-2011",
                act_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
                section_number="Rule 4",
                section_title="Privacy policy and disclosure of information",
                full_verbatim_text=(
                    "Rule 4. Body corporate to provide privacy policy.—(1) The body corporate or any person who on its behalf collects, receives, possesses, "
                    "stores, deals or handle information of provider of information, shall provide a privacy policy for handling of or dealing in personal information "
                    "including sensitive personal data or information and ensure that the same are available for view by such providers of information who has provided "
                    "such information under lawful contract. Such policy shall be published on website of body corporate or any person on its behalf and shall provide "
                    "for—\n"
                    "(i) Clear and easily accessible statements of its practices and policies;\n"
                    "(ii) Type of personal or sensitive personal data or information collected;\n"
                    "(iii) Purpose of collection and usage of such information;\n"
                    "(iv) Disclosure of information including sensitive personal data or information as provided in rule 6;\n"
                    "(v) Reasonable security practices and procedures as provided under rule 8."
                ),
            ),
            StatuteSection(
                section_id="IND-RULE-IT-SPDI-2011:RULE:5",
                source_id="IND-RULE-IT-SPDI-2011",
                act_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
                section_number="Rule 5",
                section_title="Collection of information",
                full_verbatim_text=(
                    "Rule 5. Consent and collection standards.—(1) Body corporate or any person on its behalf shall obtain consent, whether in writing or through "
                    "electronic means, from the provider of the sensitive personal data or information regarding purpose of usage before collection of such information.\n"
                    "(2) Body corporate or any person on its behalf shall not collect sensitive personal data or information unless the information is collected for a lawful "
                    "purpose connected with a function or activity of the body corporate or any person on its behalf, and the collection of the sensitive personal data or "
                    "information is considered necessary for that purpose.\n"
                    "(3) While collecting information directly from the person concerned, the body corporate or any person on its behalf shall take such steps as are, in the "
                    "circumstances, reasonable to ensure that the person concerned is having the knowledge of the fact that the information is being collected, the purpose "
                    "for which the information is being collected, and the intended recipients of the information."
                ),
            ),
            StatuteSection(
                section_id="IND-RULE-IT-SPDI-2011:RULE:8",
                source_id="IND-RULE-IT-SPDI-2011",
                act_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
                section_number="Rule 8",
                section_title="Reasonable security practices and procedures",
                full_verbatim_text=(
                    "Rule 8. Reasonable security practices and procedures.—(1) A body corporate or a person on its behalf shall be considered to have complied with reasonable "
                    "security practices and procedures, if they have implemented such security practices and standards and have a comprehensive documented information security "
                    "programme and information security policies that contain managerial, technical, operational and physical security control measures that are commensurate "
                    "with the information assets being protected with the nature of business.\n"
                    "(2) The international Standard IS/ISO/IEC 27001 on 'Information Technology - Security Techniques - Information Security Management System - Requirements' "
                    "is one such standard referred to in sub-rule (1).\n"
                    "(3) Any industry association or entity may follow codes of best practices approved and notified by the Central Government."
                ),
            ),
        ]
    )
    instruments.append(spdi_doc)

    # 2. IT Intermediary Rules 2021
    intermediary_doc = StatuteDocument(
        source_id="IND-RULE-IT-INTERMEDIARY-2021",
        act_title="Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
        act_number="G.S.R. 139(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2021, 2, 25),
        effective_date=date(2021, 2, 25),
        preamble="Rules framed under sub-section (1) and clauses (z) and (zg) of sub-section (2) of section 87 of the Information Technology Act, 2000, superseding the 2011 Intermediary Guidelines.",
        sections=[
            StatuteSection(
                section_id="IND-RULE-IT-INTERMEDIARY-2021:RULE:3",
                source_id="IND-RULE-IT-INTERMEDIARY-2021",
                act_title="Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
                section_number="Rule 3",
                section_title="Due diligence by an intermediary",
                full_verbatim_text=(
                    "Rule 3. Due diligence by an intermediary.—(1) The intermediary shall observe due diligence while discharging its duties, including:\n"
                    "(a) The intermediary shall prominently publish on its website, mobile based application or both, the rules and regulations, privacy policy and "
                    "user agreement for access or usage of its computer resource by any person;\n"
                    "(b) The intermediary shall inform its rules and regulations, privacy policy to user and shall cause user not to host, display, upload, modify, publish, "
                    "transmit, store, update or share any information that belongs to another person and to which the user does not have any right, or is grossly harmful, "
                    "harassing, blasphemous, defamatory, obscene, pornographic, pedophilic, invasive of another's privacy, or violates any law for the time being in force;\n"
                    "(c) An intermediary shall take all reasonable measures to secure its computer resource and information contained therein;\n"
                    "(d) The intermediary shall remove or disable access to unlawful content within 36 hours of receipt of actual knowledge in the form of a court order "
                    "or notification by the Appropriate Government under section 79(3)(b) of the Act."
                ),
            ),
            StatuteSection(
                section_id="IND-RULE-IT-INTERMEDIARY-2021:RULE:4",
                source_id="IND-RULE-IT-INTERMEDIARY-2021",
                act_title="Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
                section_number="Rule 4",
                section_title="Additional due diligence observed by significant social media intermediary",
                full_verbatim_text=(
                    "Rule 4. Additional due diligence observed by significant social media intermediary.—(1) A significant social media intermediary shall appoint a Chief "
                    "Compliance Officer who shall be responsible for ensuring that the intermediary is in compliance with the Act and these rules.\n"
                    "(2) A significant social media intermediary shall appoint a nodal contact person for 24x7 coordination with law enforcement agencies and officers.\n"
                    "(3) A significant social media intermediary shall appoint a Resident Grievance Officer, who shall be an employee and a resident of India.\n"
                    "(4) A significant social media intermediary providing services primarily in the nature of messaging shall enable the identification of the first originator "
                    "of the information on its computer resource as may be required by a judicial order passed by a court of competent jurisdiction or an order under section 69 "
                    "by the Competent Authority."
                ),
            ),
        ]
    )
    instruments.append(intermediary_doc)

    # 3. Consumer Protection (E-Commerce) Rules, 2020
    ecommerce_doc = StatuteDocument(
        source_id="IND-RULE-CPA-ECOMMERCE-2020",
        act_title="Consumer Protection (E-Commerce) Rules, 2020",
        act_number="G.S.R. 462(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2020, 7, 23),
        effective_date=date(2020, 7, 23),
        preamble="Rules framed by the Central Government under sub-clause (zg) of sub-section (2) of section 101 read with section 94 of the Consumer Protection Act, 2019 for prevention of unfair trade practices in e-commerce.",
        sections=[
            StatuteSection(
                section_id="IND-RULE-CPA-ECOMMERCE-2020:RULE:4",
                source_id="IND-RULE-CPA-ECOMMERCE-2020",
                act_title="Consumer Protection (E-Commerce) Rules, 2020",
                section_number="Rule 4",
                section_title="Mandatory duties of e-commerce entities",
                full_verbatim_text=(
                    "Rule 4. Duties of e-commerce entities.—(1) An e-commerce entity shall be a company incorporated under the Companies Act, 1956 or the Companies Act, 2013 "
                    "or a foreign company or an office, branch or agency outside India owned or controlled by a person resident in India.\n"
                    "(2) Appoint a nodal person of contact or an alternate senior designated functionary who is resident in India, to ensure compliance with the provisions of "
                    "the Act or the rules made thereunder.\n"
                    "(3) Every e-commerce entity shall provide in a clear and accessible manner on its platform the legal name of the entity, principal geographic address of its "
                    "headquarters and all branches, name and details of its website, and contact details including email address, fax, and telephone numbers.\n"
                    "(4) Every e-commerce entity shall establish an adequate grievance redressal mechanism and appoint a grievance officer for consumer grievance redressal, "
                    "and display prominently on its platform the name, designation and contact details of such officer.\n"
                    "(5) The grievance officer shall acknowledge receipt of any consumer complaint within forty-eight hours and redress the complaint within one month from the "
                    "date of receipt of the complaint."
                ),
            ),
            StatuteSection(
                section_id="IND-RULE-CPA-ECOMMERCE-2020:RULE:5",
                source_id="IND-RULE-CPA-ECOMMERCE-2020",
                act_title="Consumer Protection (E-Commerce) Rules, 2020",
                section_number="Rule 5",
                section_title="Liabilities of marketplace e-commerce entities",
                full_verbatim_text=(
                    "Rule 5. Marketplace e-commerce entities.—(1) A marketplace e-commerce entity shall require sellers through an undertaking to ensure that descriptions, "
                    "images, and other content pertaining to goods or services on their platform are accurate and correspond directly with the appearance, nature, quality, "
                    "purpose and other general features of such good or service.\n"
                    "(2) Every marketplace e-commerce entity shall display prominently to its users: details about the sellers offering goods and services, including the name "
                    "of their business, whether registered or not, their geographic address, customer care number, rating or feedback, and any other information necessary "
                    "for enabling consumers to make informed decisions at the pre-purchase stage.\n"
                    "(3) No marketplace e-commerce entity shall manipulate the search results or listings in a manner that favors a particular seller or group of sellers."
                ),
            ),
        ]
    )
    instruments.append(ecommerce_doc)

    # 4. Commencement Notifications: Criminal Laws (BNS, BNSS, BSA) & SRA & CPA
    commence_bnss = StatuteDocument(
        source_id="IND-NOTIF-COMMENCE-BNSS-2024",
        act_title="Commencement Notification for Bharatiya Nagarik Suraksha Sanhita, 2023 (S.O. 848(E))",
        act_number="S.O. 848(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2024, 2, 23),
        effective_date=date(2024, 7, 1),
        preamble="Notification issued by Ministry of Home Affairs bringing Bharatiya Nagarik Suraksha Sanhita, 2023 into force.",
        sections=[
            StatuteSection(
                section_id="IND-NOTIF-COMMENCE-BNSS-2024:SEC:1",
                source_id="IND-NOTIF-COMMENCE-BNSS-2024",
                act_title="Commencement Notification for Bharatiya Nagarik Suraksha Sanhita, 2023",
                section_number="Notification S.O. 848(E)",
                section_title="Commencement of BNSS 2023",
                full_verbatim_text=(
                    "MINISTRY OF HOME AFFAIRS NOTIFICATION, New Delhi, the 23rd February, 2024.\n"
                    "S.O. 848(E).—In exercise of the powers conferred by sub-section (3) of section 1 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (46 of 2023), "
                    "the Central Government hereby appoints the 1st day of July, 2024 as the date on which the provisions of the said Sanhita, except the provisions of "
                    "the entry relating to section 106(2) of the Bharatiya Nyaya Sanhita, 2023 in the First Schedule, shall come into force."
                ),
            )
        ]
    )
    instruments.append(commence_bnss)

    commence_bns = StatuteDocument(
        source_id="IND-NOTIF-COMMENCE-BNS-2024",
        act_title="Commencement Notification for Bharatiya Nyaya Sanhita, 2023 (S.O. 849(E))",
        act_number="S.O. 849(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2024, 2, 23),
        effective_date=date(2024, 7, 1),
        preamble="Notification issued by Ministry of Home Affairs appointing 1st July 2024 for BNS 2023 enforcement.",
        sections=[
            StatuteSection(
                section_id="IND-NOTIF-COMMENCE-BNS-2024:SEC:1",
                source_id="IND-NOTIF-COMMENCE-BNS-2024",
                act_title="Commencement Notification for Bharatiya Nyaya Sanhita, 2023",
                section_number="Notification S.O. 849(E)",
                section_title="Commencement of BNS 2023",
                full_verbatim_text=(
                    "MINISTRY OF HOME AFFAIRS NOTIFICATION, New Delhi, the 23rd February, 2024.\n"
                    "S.O. 849(E).—In exercise of the powers conferred by sub-section (2) of section 1 of the Bharatiya Nyaya Sanhita, 2023 (45 of 2023), "
                    "the Central Government hereby appoints the 1st day of July, 2024 as the date on which the provisions of the said Sanhita, except the provisions "
                    "of sub-section (2) of section 106, shall come into force."
                ),
            )
        ]
    )
    instruments.append(commence_bns)

    commence_bsa = StatuteDocument(
        source_id="IND-NOTIF-COMMENCE-BSA-2024",
        act_title="Commencement Notification for Bharatiya Sakshya Adhiniyam, 2023 (S.O. 850(E))",
        act_number="S.O. 850(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2024, 2, 23),
        effective_date=date(2024, 7, 1),
        preamble="Notification issued by Ministry of Home Affairs appointing 1st July 2024 for BSA 2023 enforcement.",
        sections=[
            StatuteSection(
                section_id="IND-NOTIF-COMMENCE-BSA-2024:SEC:1",
                source_id="IND-NOTIF-COMMENCE-BSA-2024",
                act_title="Commencement Notification for Bharatiya Sakshya Adhiniyam, 2023",
                section_number="Notification S.O. 850(E)",
                section_title="Commencement of BSA 2023",
                full_verbatim_text=(
                    "MINISTRY OF HOME AFFAIRS NOTIFICATION, New Delhi, the 23rd February, 2024.\n"
                    "S.O. 850(E).—In exercise of the powers conferred by sub-section (3) of section 1 of the Bharatiya Sakshya Adhiniyam, 2023 (47 of 2023), "
                    "the Central Government hereby appoints the 1st day of July, 2024 as the date on which the provisions of the said Adhiniyam shall come into force."
                ),
            )
        ]
    )
    instruments.append(commence_bsa)

    commence_sra = StatuteDocument(
        source_id="IND-NOTIF-COMMENCE-SRA-2018",
        act_title="Commencement Notification for Specific Relief (Amendment) Act, 2018 (S.O. 4888(E))",
        act_number="S.O. 4888(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2018, 9, 19),
        effective_date=date(2018, 10, 1),
        preamble="Notification bringing the Specific Relief (Amendment) Act, 2018 into force on 1st October 2018.",
        sections=[
            StatuteSection(
                section_id="IND-NOTIF-COMMENCE-SRA-2018:SEC:1",
                source_id="IND-NOTIF-COMMENCE-SRA-2018",
                act_title="Commencement Notification for Specific Relief (Amendment) Act, 2018",
                section_number="Notification S.O. 4888(E)",
                section_title="Commencement of SRA Amendment 2018",
                full_verbatim_text=(
                    "MINISTRY OF LAW AND JUSTICE (Legislative Department) NOTIFICATION, New Delhi, the 19th September, 2018.\n"
                    "S.O. 4888(E).—In exercise of the powers conferred by sub-section (2) of section 1 of the Specific Relief (Amendment) Act, 2018 (18 of 2018), "
                    "the Central Government hereby appoints the 1st day of October, 2018, as the date on which the provisions of the said Act shall come into force."
                ),
            )
        ]
    )
    instruments.append(commence_sra)

    commence_cpa = StatuteDocument(
        source_id="IND-NOTIF-COMMENCE-CPA-2020",
        act_title="Commencement Notification for Consumer Protection Act, 2019 (S.O. 2351(E))",
        act_number="S.O. 2351(E)",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2020, 7, 15),
        effective_date=date(2020, 7, 20),
        preamble="Notification bringing the Consumer Protection Act, 2019 into force on 20th July 2020.",
        sections=[
            StatuteSection(
                section_id="IND-NOTIF-COMMENCE-CPA-2020:SEC:1",
                source_id="IND-NOTIF-COMMENCE-CPA-2020",
                act_title="Commencement Notification for Consumer Protection Act, 2019",
                section_number="Notification S.O. 2351(E)",
                section_title="Commencement of CPA 2019",
                full_verbatim_text=(
                    "MINISTRY OF CONSUMER AFFAIRS, FOOD AND PUBLIC DISTRIBUTION NOTIFICATION, New Delhi, the 15th July, 2020.\n"
                    "S.O. 2351(E).—In exercise of the powers conferred by sub-section (3) of section 1 of the Consumer Protection Act, 2019 (35 of 2019), "
                    "the Central Government hereby appoints the 20th day of July, 2020 as the date on which the following provisions of the said Act shall come into force, "
                    "namely: Chapter I, Chapter II (except clauses (l), (m), (n) of section 2), Chapter III, Chapter IV (except sections 44, 50, 58), Chapter V and Chapter VI."
                ),
            )
        ]
    )
    instruments.append(commence_cpa)

    return instruments

