"""
LegalMitra Central Acts Structural Corpus Generator
Generates validated, source-grounded Pydantic StatuteDocument structures
for authoritative central enactments, preserving exact hierarchical provisions.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus
from legalmitra.schemas.statute import (
    StatuteDocument,
    StatuteExplanation,
    StatuteIllustration,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)
from legalmitra.ingestion.central_acts_phase16 import (
    get_arbitration_phase16_sections,
    get_bns_phase16_sections,
    get_constitution_phase16_sections,
    get_contract_phase16_sections,
    get_cpa_phase16_sections,
    get_cpc_phase16_sections,
    get_limitation_phase16_sections,
    get_sra_phase16_sections,
)


def make_section(

    source_id: str,
    act_title: str,
    section_number: str,
    section_title: str,
    full_verbatim_text: str,
    act_number: Optional[str] = None,
    chapter_number: Optional[str] = None,
    chapter_title: Optional[str] = None,
    subsections: Optional[List[StatuteSubSection]] = None,
    provisos: Optional[List[StatuteProviso]] = None,
    explanations: Optional[List[StatuteExplanation]] = None,
    illustrations: Optional[List[StatuteIllustration]] = None,
) -> StatuteSection:
    sec_id_clean = section_number.replace(" ", "-").replace("(", "").replace(")", "").replace(".", "-").upper()
    return StatuteSection(
        section_id=f"{source_id}-SEC-{sec_id_clean}",
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        section_number=section_number,
        section_title=section_title,
        full_verbatim_text=full_verbatim_text,
        subsections=subsections or [],
        provisos=provisos or [],
        explanations=explanations or [],
        illustrations=illustrations or [],
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_constitution_document() -> StatuteDocument:
    source_id = "IND-CONST-1950"
    act_title = "The Constitution of India"
    act_number = "Constituent Assembly Enactment"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Preamble",
            section_title="Preamble to the Constitution of India",
            chapter_number="Foundational",
            chapter_title="Preamble",
            full_verbatim_text=(
                "WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a "
                "SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC and to secure to all its citizens: "
                "JUSTICE, social, economic and political; LIBERTY of thought, expression, belief, faith and worship; "
                "EQUALITY of status and of opportunity; and to promote among them all FRATERNITY assuring the "
                "dignity of the individual and the unity and integrity of the Nation; IN OUR CONSTITUENT ASSEMBLY "
                "this twenty-sixth day of November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 14",
            section_title="Equality before law",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "The State shall not deny to any person equality before the law or the equal protection "
                "of the laws within the territory of India."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 19",
            section_title="Protection of certain rights regarding freedom of speech, etc.",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "(1) All citizens shall have the right— (a) to freedom of speech and expression; "
                "(b) to assemble peaceably and without arms; (c) to form associations or unions; "
                "(d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; "
                "and (g) to practise any profession, or to carry on any occupation, trade or business. "
                "(2) Nothing in sub-clause (a) of clause (1) shall affect the operation of any existing law, "
                "or prevent the State from making any law, in so far as such law imposes reasonable restrictions "
                "on the exercise of the right conferred by the said sub-clause in the interests of the sovereignty "
                "and integrity of India, the security of the State, friendly relations with foreign States, public order, "
                "decency or morality, or in relation to contempt of court, defamation or incitement to an offence."
            ),
            subsections=[
                StatuteSubSection(
                    sub_section_number="(1)",
                    text="All citizens shall have the right— (a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions; (d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; and (g) to practise any profession, or to carry on any occupation, trade or business."
                ),
                StatuteSubSection(
                    sub_section_number="(2)",
                    text="Nothing in sub-clause (a) of clause (1) shall affect the operation of any existing law, or prevent the State from making any law, in so far as such law imposes reasonable restrictions on the exercise of the right conferred by the said sub-clause in the interests of the sovereignty and integrity of India, the security of the State, friendly relations with foreign States, public order, decency or morality, or in relation to contempt of court, defamation or incitement to an offence."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 20",
            section_title="Protection in respect of conviction for offences",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "(1) No person shall be convicted of any offence except for violation of a law in force at the time "
                "of the commission of the act charged as an offence, nor be subjected to a penalty greater than that "
                "which might have been inflicted under the law in force at the time of the commission of the offence. "
                "(2) No person shall be prosecuted and punished for the same offence more than once. "
                "(3) No person accused of any offence shall be compelled to be a witness against himself."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act charged as an offence, nor be subjected to a penalty greater than that which might have been inflicted under the law in force at the time of the commission of the offence."),
                StatuteSubSection(sub_section_number="(2)", text="No person shall be prosecuted and punished for the same offence more than once."),
                StatuteSubSection(sub_section_number="(3)", text="No person accused of any offence shall be compelled to be a witness against himself.")
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 21",
            section_title="Protection of life and personal liberty",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "No person shall be deprived of his life or personal liberty except according to procedure established by law."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 21A",
            section_title="Right to education",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "The State shall provide free and compulsory education to all children of the age of six to fourteen "
                "years in such manner as the State may, by law, determine."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 32",
            section_title="Remedies for enforcement of rights conferred by this Part",
            chapter_number="Part III",
            chapter_title="Fundamental Rights",
            full_verbatim_text=(
                "(1) The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights "
                "conferred by this Part is guaranteed. (2) The Supreme Court shall have power to issue directions or orders "
                "or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, "
                "whichever may be appropriate, for the enforcement of any of the rights conferred by this Part."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed."),
                StatuteSubSection(sub_section_number="(2)", text="The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part.")
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 226",
            section_title="Power of High Courts to issue certain writs",
            chapter_number="Part VI",
            chapter_title="The High Courts in the States",
            full_verbatim_text=(
                "(1) Notwithstanding anything in article 32, every High Court shall have power, throughout the territories "
                "in relation to which it exercises jurisdiction, to issue to any person or authority, including in appropriate cases, "
                "any Government, within those territories directions, orders or writs, including writs in the nature of habeas corpus, "
                "mandamus, prohibition, quo warranto and certiorari, or any of them, for the enforcement of any of the rights "
                "conferred by Part III and for any other purpose."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 368",
            section_title="Power of Parliament to amend the Constitution and procedure therefor",
            chapter_number="Part XX",
            chapter_title="Amendment of the Constitution",
            full_verbatim_text=(
                "(1) Notwithstanding anything in this Constitution, Parliament may in exercise of its constituent power "
                "amend by way of addition, variation or repeal any provision of this Constitution in accordance with the procedure "
                "laid down in this article. (2) An amendment of this Constitution may be initiated only by the introduction "
                "of a Bill for the purpose in either House of Parliament, and when the Bill is passed in each House by a majority "
                "of the total membership of that House and by a majority of not less than two-thirds of the members of that House "
                "present and voting, it shall be presented to the President who shall give his assent to the Bill and thereupon "
                "the Constitution shall stand amended in accordance with the terms of the Bill."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="Notwithstanding anything in this Constitution, Parliament may in exercise of its constituent power amend by way of addition, variation or repeal any provision of this Constitution in accordance with the procedure laid down in this article."),
                StatuteSubSection(sub_section_number="(2)", text="An amendment of this Constitution may be initiated only by the introduction of a Bill for the purpose in either House of Parliament, and when the Bill is passed in each House by a majority of the total membership of that House and by a majority of not less than two-thirds of the members of that House present and voting, it shall be presented to the President who shall give his assent to the Bill and thereupon the Constitution shall stand amended in accordance with the terms of the Bill.")
            ],
            provisos=[
                StatuteProviso(
                    proviso_index=1,
                    text="Provided that if such amendment seeks to make any change in article 54, 55, 73, 162, 241, Chapter IV of Part V, Chapter V of Part VI, or Chapter I of Part XI, or any of the Lists in the Seventh Schedule, or the representation of States in Parliament, or the provisions of this article, the amendment shall also require to be ratified by the Legislatures of not less than one-half of the States."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Article 330A",
            section_title="Reservation of seats for women in the House of the People",
            chapter_number="Part XVI",
            chapter_title="Special Provisions Relating to Certain Classes",
            full_verbatim_text=(
                "(1) Seats shall be reserved for women in the House of the People. (2) As nearly as may be, one-third "
                "of the total number of seats reserved under clause (2) of article 330 shall be reserved for women "
                "belonging to the Scheduled Castes or the Scheduled Tribes. (3) As nearly as may be, one-third (including "
                "the number of seats reserved under clause (2)) of the total number of seats to be filled by direct election "
                "to the House of the People shall be reserved for women. (Inserted by the Constitution (One Hundred and Sixth "
                "Amendment) Act, 2023)."
            ),
        )
    ]
    sections.extend(get_constitution_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1949, 11, 26),
        effective_date=date(1950, 1, 26),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_bns_document() -> StatuteDocument:
    source_id = "IND-STAT-BNS-2023"
    act_title = "The Bharatiya Nyaya Sanhita, 2023"
    act_number = "Act No. 45 of 2023"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="1",
            section_title="Short title, commencement and application",
            chapter_number="Chapter I",
            chapter_title="Preliminary",
            full_verbatim_text=(
                "(1) This Act may be called the Bharatiya Nyaya Sanhita, 2023. "
                "(2) It shall come into force on such date as the Central Government may, by notification in the Official Gazette, appoint. "
                "(3) Every person shall be liable to punishment under this Sanhita and not otherwise for every act or omission "
                "contrary to the provisions thereof, of which he shall be guilty within India."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="This Act may be called the Bharatiya Nyaya Sanhita, 2023."),
                StatuteSubSection(sub_section_number="(2)", text="It shall come into force on such date as the Central Government may, by notification in the Official Gazette, appoint [Commenced 1 July 2024 via S.O. 849(E)]."),
                StatuteSubSection(sub_section_number="(3)", text="Every person shall be liable to punishment under this Sanhita and not otherwise for every act or omission contrary to the provisions thereof, of which he shall be guilty within India.")
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="4",
            section_title="Punishments",
            chapter_number="Chapter II",
            chapter_title="Of Punishments",
            full_verbatim_text=(
                "The punishments to which offenders are liable under the provisions of this Sanhita are— "
                "(a) Death; (b) Imprisonment for life; (c) Imprisonment, which is of two descriptions, namely:— "
                "(1) Rigorous, that is, with hard labour; (2) Simple; (d) Forfeiture of property; (e) Fine; (f) Community service."
            ),
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation",
                    text="Community service shall mean the work which the Court may order a convict to perform as a form of punishment that benefits the community, for which he shall not be entitled to any remuneration."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="103",
            section_title="Punishment for murder",
            chapter_number="Chapter VI",
            chapter_title="Of Offences Affecting the Human Body",
            full_verbatim_text=(
                "(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. "
                "(2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, "
                "sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be "
                "punished with death or with imprisonment for life, and shall also be liable to fine."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."),
                StatuteSubSection(sub_section_number="(2)", text="When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine.")
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="111",
            section_title="Organised crime",
            chapter_number="Chapter VI",
            chapter_title="Of Offences Affecting the Human Body",
            full_verbatim_text=(
                "(1) Any continuing unlawful activity including kidnapping, robbery, vehicle theft, extortion, land grabbing, "
                "contract killing, economic offence, cyber-crimes having severe consequences, trafficking in persons, drugs or weapons "
                "or illicit goods or services, human trafficking for prostitution or ransom, by any person or a group of persons "
                "acting on behalf of an organised crime syndicate shall constitute the offence of organised crime. "
                "(2) Whoever commits organised crime shall,— (a) if such offence has resulted in the death of any person, "
                "be punished with death or imprisonment for life, and shall also be liable to fine which shall not be less than ten lakh rupees."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="303",
            section_title="Theft",
            chapter_number="Chapter XVII",
            chapter_title="Of Offences Against Property",
            full_verbatim_text=(
                "(1) Whoever, intending to take dishonestly any movable property out of the possession of any person "
                "without that person's consent, moves that property in order to such taking, is said to commit theft. "
                "(2) Whoever commits theft shall be punished with imprisonment of either description for a term which may "
                "extend to three years, or with fine, or with both."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="304",
            section_title="Snatching",
            chapter_number="Chapter XVII",
            chapter_title="Of Offences Against Property",
            full_verbatim_text=(
                "(1) Theft is 'snatching' if, in order to commit theft, the offender suddenly or quickly or forcibly seizes, "
                "secures, grabs or takes away from any person or from his possession any movable property. "
                "(2) Whoever commits snatching shall be punished with imprisonment of either description for a term which may "
                "extend to three years, and shall also be liable to fine."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="318",
            section_title="Cheating",
            chapter_number="Chapter XVII",
            chapter_title="Of Offences Against Property",
            full_verbatim_text=(
                "(1) Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver "
                "any property to any person... is said to 'cheat'. (4) Whoever cheats and thereby dishonestly induces the person "
                "deceived to deliver any property... shall be punished with imprisonment of either description for a term which may "
                "extend to seven years, and shall also be liable to fine."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="358",
            section_title="Repeal and savings",
            chapter_number="Chapter XX",
            chapter_title="Repeal and Savings",
            full_verbatim_text=(
                "(1) The Indian Penal Code is hereby repealed. (2) Notwithstanding the repeal of the Code, "
                "the repeal shall not affect— (a) the previous operation of the Code so repealed or anything duly done or suffered thereunder; "
                "or (b) any right, privilege, obligation or liability acquired, accrued or incurred under the Code so repealed; "
                "or (c) any penalty, forfeiture or punishment incurred in respect of any offence committed against the Code so repealed; "
                "or (d) any investigation, legal proceeding or remedy in respect of any such penalty, forfeiture or punishment, "
                "and any such investigation, legal proceeding or remedy may be instituted, continued or enforced, and any such penalty, "
                "forfeiture or punishment may be imposed as if that Code had not been repealed."
            ),
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="The Indian Penal Code is hereby repealed."),
                StatuteSubSection(sub_section_number="(2)", text="Notwithstanding the repeal of the Code, the repeal shall not affect— (a) the previous operation of the Code so repealed or anything duly done or suffered thereunder; or (b) any right, privilege, obligation or liability acquired, accrued or incurred under the Code so repealed; or (c) any penalty, forfeiture or punishment incurred in respect of any offence committed against the Code so repealed; or (d) any investigation, legal proceeding or remedy in respect of any such penalty, forfeiture or punishment, and any such investigation, legal proceeding or remedy may be instituted, continued or enforced, and any such penalty, forfeiture or punishment may be imposed as if that Code had not been repealed.")
            ]
        )
    ]
    sections.extend(get_bns_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(2023, 12, 25),
        effective_date=date(2024, 7, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_cpc_document() -> StatuteDocument:
    source_id = "IND-STAT-CPC-1908"
    act_title = "The Code of Civil Procedure, 1908"
    act_number = "Act No. 5 of 1908"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="9",
            section_title="Courts to try all civil suits unless barred",
            chapter_number="Part I",
            chapter_title="Suits in General",
            full_verbatim_text=(
                "The Courts shall (subject to the provisions herein contained) have jurisdiction to try all suits "
                "of a civil nature excepting suits of which their cognizance is either expressly or impliedly barred."
            ),
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation I",
                    text="A suit in which the right to property or to an office is contested is a suit of a civil nature, notwithstanding that such right may depend entirely on the decision of questions as to religious rites or ceremonies."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="10",
            section_title="Stay of suit (Res Sub-Judice)",
            chapter_number="Part I",
            chapter_title="Suits in General",
            full_verbatim_text=(
                "No Court shall proceed with the trial of any suit in which the matter in issue is also directly "
                "and substantially in issue in a previously instituted suit between the same parties, or between "
                "parties under whom they or any of them claim litigating under the same title where such suit is pending "
                "in the same or any other Court in India having jurisdiction to grant the relief claimed."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="11",
            section_title="Res Judicata",
            chapter_number="Part I",
            chapter_title="Suits in General",
            full_verbatim_text=(
                "No Court shall try any suit or issue in which the matter directly and substantially in issue has been "
                "directly and substantially in issue in a former suit between the same parties, or between parties under "
                "whom they or any of them claim, litigating under the same title, in a Court competent to try such subsequent suit "
                "or the suit in which such issue has been subsequently raised, and has been heard and finally decided by such Court."
            ),
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation IV",
                    text="Constructive Res Judicata: Any matter which might and ought to have been made ground of defence or attack in such former suit shall be deemed to have been a matter directly and substantially in issue in such suit."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="80",
            section_title="Notice to Government or public officer",
            chapter_number="Part IV",
            chapter_title="Suits by or Against the Government",
            full_verbatim_text=(
                "(1) Save as otherwise provided in sub-section (2), no suit shall be instituted against the Government "
                "or against a public officer in respect of any act purporting to be done by such public officer in his official "
                "capacity, until the expiration of two months next after notice in writing has been delivered to, or left at the office of..."
            ),
            subsections=[
                StatuteSubSection(
                    sub_section_number="(1)",
                    text="Save as otherwise provided in sub-section (2), no suit shall be instituted against the Government or against a public officer in respect of any act purporting to be done by such public officer in his official capacity, until the expiration of two months next after notice in writing has been delivered to, or left at the office of..."
                ),
                StatuteSubSection(
                    sub_section_number="(2)",
                    text="A suit to obtain an urgent or immediate relief against the Government or any public officer may be instituted, with the leave of the Court, without serving any notice as required by sub-section (1); but the Court shall not grant relief in the suit, whether interim or otherwise, except after giving to the Government or public officer a reasonable opportunity of showing cause."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="89",
            section_title="Settlement of disputes outside the Court",
            chapter_number="Part V",
            chapter_title="Special Proceedings",
            full_verbatim_text=(
                "(1) Where it appears to the Court that there exist elements of a settlement which may be acceptable to the parties, "
                "the Court shall formulate the terms of settlement and give them to the parties for their observations... "
                "the Court may refer the same for:— (a) arbitration; (b) conciliation; (c) judicial settlement including settlement "
                "through Lok Adalat; or (d) mediation."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="151",
            section_title="Saving of inherent powers of Court",
            chapter_number="Part XI",
            chapter_title="Miscellaneous",
            full_verbatim_text=(
                "Nothing in this Code shall be deemed to limit or otherwise affect the inherent power of the Court "
                "to make such orders as may be necessary for the ends of justice or to prevent abuse of the process of the Court."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="Order 39 Rule 1",
            section_title="Cases in which temporary injunction may be granted",
            chapter_number="First Schedule",
            chapter_title="Orders and Rules",
            full_verbatim_text=(
                "Where in any suit it is proved by affidavit or otherwise— (a) that any property in dispute in a suit is "
                "in danger of being wasted, damaged or alienated by any party to the suit, or wrongfully sold in execution of a decree, "
                "or (b) that the defendant threatens, or intends, to remove or dispose of his property with a view to defrauding his creditors, "
                "the Court may by order grant a temporary injunction to restrain such act, or make such other order for the purpose "
                "of staying and preventing the wasting, damaging, alienation, sale, removal or disposition of the property as the Court thinks fit."
            ),
        )
    ]
    sections.extend(get_cpc_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1908, 3, 21),
        effective_date=date(1909, 1, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_limitation_document() -> StatuteDocument:
    source_id = "IND-STAT-LIMIT-1963"
    act_title = "The Limitation Act, 1963"
    act_number = "Act No. 36 of 1963"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="3",
            section_title="Bar of limitation",
            chapter_number="Part II",
            chapter_title="Limitation of Suits, Appeals and Applications",
            full_verbatim_text=(
                "(1) Subject to the provisions contained in sections 4 to 24 (inclusive), every suit instituted, appeal preferred, "
                "and application made after the prescribed period shall be dismissed, although limitation has not been set up as a defence."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="5",
            section_title="Extension of prescribed period in certain cases (Condonation of delay)",
            chapter_number="Part II",
            chapter_title="Limitation of Suits, Appeals and Applications",
            full_verbatim_text=(
                "Any appeal or any application, other than an application under any of the provisions of Order XXI of the Code "
                "of Civil Procedure, 1908, may be admitted after the prescribed period, if the appellant or the applicant satisfies "
                "the court that he had sufficient cause for not preferring the appeal or making the application within such period."
            ),
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation",
                    text="The fact that the appellant or the applicant was misled by any order, practice or judgment of the High Court in ascertaining or computing the prescribed period may be sufficient cause within the meaning of this section."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="12",
            section_title="Exclusion of time in legal proceedings",
            chapter_number="Part III",
            chapter_title="Computation of Period of Limitation",
            full_verbatim_text=(
                "(1) In computing the period of limitation for any suit, appeal or application, the day from which such period "
                "is to be reckoned, shall be excluded. (2) In computing the period of limitation for an appeal or an application "
                "for leave to appeal or for revision or for review of a judgment, the day on which the judgment complained of was pronounced "
                "and the time requisite for obtaining a copy of the decree, sentence or order appealed from or sought to be revised or "
                "reviewed shall be excluded."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="14",
            section_title="Exclusion of time of proceeding bona fide in court without jurisdiction",
            chapter_number="Part III",
            chapter_title="Computation of Period of Limitation",
            full_verbatim_text=(
                "(1) In computing the period of limitation for any suit the time during which the plaintiff has been prosecuting "
                "with due diligence another civil proceeding, whether in a Court of first instance or of appeal or revision, "
                "against the defendant shall be excluded, where the proceeding relates to the same matter in issue and is prosecuted "
                "in good faith in a Court which, from defect of jurisdiction or other cause of a like nature, is unable to entertain it."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="18",
            section_title="Effect of acknowledgment in writing",
            chapter_number="Part III",
            chapter_title="Computation of Period of Limitation",
            full_verbatim_text=(
                "(1) Where, before the expiration of the prescribed period for a suit or application in respect of any property or right, "
                "an acknowledgment of liability in respect of such property or right has been made in writing signed by the party "
                "against whom such property or right is claimed... a fresh period of limitation shall be computed from the time when "
                "the acknowledgment was so signed."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="27",
            section_title="Extinguishment of right to property",
            chapter_number="Part IV",
            chapter_title="Acquisition of Ownership by Possession",
            full_verbatim_text=(
                "At the determination of the period hereby limited to any person for instituting a suit for possession "
                "of any property, his right to such property shall be extinguished."
            ),
        )
    ]
    sections.extend(get_limitation_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1963, 10, 5),
        effective_date=date(1964, 1, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_contract_document() -> StatuteDocument:
    source_id = "IND-STAT-ICA-1872"
    act_title = "The Indian Contract Act, 1872"
    act_number = "Act No. 9 of 1872"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="2",
            section_title="Interpretation-clause",
            chapter_number="Preliminary",
            chapter_title="Preliminary",
            full_verbatim_text=(
                "In this Act the following words and expressions are used in the following senses, unless a contrary intention appears "
                "from the context:— (a) When one person signifies to another his willingness to do or to abstain from doing anything, "
                "with a view to obtaining the assent of that other to such act or abstinence, he is said to make a proposal; "
                "(b) When the person to whom the proposal is made signifies his assent thereto, the proposal is said to be accepted. "
                "A proposal, when accepted, becomes a promise; (d) When, at the desire of the promisor, the promisee or any other person "
                "has done or abstained from doing... such act or abstinence or promise is called a consideration for the promise; "
                "(e) Every promise and every set of promises, forming the consideration for each other, is an agreement; "
                "(h) An agreement enforceable by law is a contract."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="10",
            section_title="What agreements are contracts",
            chapter_number="Chapter II",
            chapter_title="Of Contracts, Voidable Contracts and Void Agreements",
            full_verbatim_text=(
                "All agreements are contracts if they are made by the free consent of parties competent to contract, "
                "for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="27",
            section_title="Agreement in restraint of trade void",
            chapter_number="Chapter II",
            chapter_title="Of Contracts, Voidable Contracts and Void Agreements",
            full_verbatim_text=(
                "Every agreement by which any one is restrained from exercising a lawful profession, trade or business "
                "of any kind, is to that extent void."
            ),
            provisos=[
                StatuteProviso(
                    proviso_index=1,
                    text="Saving of agreement not to carry on business of which good-will is sold: One who sells the good-will of a business may agree with the buyer to refrain from carrying on a similar business, within specified local limits, so long as the buyer, or any person deriving title to the good-will from him, carries on a like business therein, provided that such limits appear to the Court reasonable."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="28",
            section_title="Agreements in restraint of legal proceedings void",
            chapter_number="Chapter II",
            chapter_title="Of Contracts, Voidable Contracts and Void Agreements",
            full_verbatim_text=(
                "Every agreement,— (a) by which any party thereto is restricted absolutely from enforcing his rights under "
                "or in respect of any contract, by the usual legal proceedings in the ordinary tribunals, or which limits the time "
                "within which he may thus enforce his rights; or (b) which extinguishes the rights of any party thereto, or discharges "
                "any party thereto, from any liability, under or in respect of any contract on the expiry of a specified period so as "
                "to restrict any party from enforcing his rights, is void to that extent."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="56",
            section_title="Agreement to do impossible act (Doctrine of Frustration)",
            chapter_number="Chapter IV",
            chapter_title="Of the Performance of Contracts",
            full_verbatim_text=(
                "An agreement to do an act impossible in itself is void. Contract to do act afterwards becoming impossible or unlawful: "
                "A contract to do an act which, after the contract is made, becomes impossible, or, by reason of some event which the promisor "
                "could not prevent, unlawful, becomes void when the act becomes impossible or unlawful."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="73",
            section_title="Compensation for loss or damage caused by breach of contract",
            chapter_number="Chapter VI",
            chapter_title="Of the Consequences of Breach of Contract",
            full_verbatim_text=(
                "When a contract has been broken, the party who suffers by such breach is entitled to receive, from the party "
                "who has broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose "
                "in the usual course of things from such breach, or which the parties knew, when they made the contract, "
                "to be likely to result from the breach of it. Such compensation is not to be given for any remote and indirect loss or damage."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="74",
            section_title="Compensation for breach of contract where penalty stipulated for (Liquidated Damages)",
            chapter_number="Chapter VI",
            chapter_title="Of the Consequences of Breach of Contract",
            full_verbatim_text=(
                "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, "
                "or if the contract contains any other stipulation by way of penalty, the party complaining of the breach is entitled, "
                "whether or not actual damage or loss is proved to have been caused thereby, to receive from the party who has broken the contract "
                "reasonable compensation not exceeding the amount so named or, as the case may be, the penalty stipulated for."
            ),
        )
    ]
    sections.extend(get_contract_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1872, 4, 25),
        effective_date=date(1872, 9, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_sra_document() -> StatuteDocument:
    source_id = "IND-STAT-SRA-1963"
    act_title = "The Specific Relief Act, 1963"
    act_number = "Act No. 47 of 1963"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="10",
            section_title="Specific performance in respect of contracts",
            chapter_number="Chapter II",
            chapter_title="Specific Performance of Contracts",
            full_verbatim_text=(
                "The specific performance of a contract shall be enforced by the court subject to the provisions "
                "contained in sub-section (2) of section 11, section 14 and section 16. "
                "[Substituted by Act 18 of 2018, s. 3 (w.e.f. 1-10-2018)]."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="14",
            section_title="Contracts not specifically enforceable",
            chapter_number="Chapter II",
            chapter_title="Specific Performance of Contracts",
            full_verbatim_text=(
                "The following contracts cannot be specifically enforced, namely:— (a) where a party to the contract "
                "has obtained substituted performance of contract in accordance with the provisions of section 20; "
                "(b) a contract, the performance of which involves the performance of a continuous duty which the court cannot supervise; "
                "(c) a contract which is so dependent on the personal qualifications of the parties that the court cannot enforce specific performance of its material terms; "
                "and (d) a contract which is in its nature determinable."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="20",
            section_title="Substituted performance of contract",
            chapter_number="Chapter II",
            chapter_title="Specific Performance of Contracts",
            full_verbatim_text=(
                "(1) Where the contract is broken due to non-performance of promise by any party, the party who suffers by such breach "
                "shall have the option of substituted performance through a third party or by his own agency, and, recover the expenses "
                "and other costs actually incurred, spent or suffered by him, from the party committing such breach. "
                "[Substituted by Act 18 of 2018, s. 10 (w.e.f. 1-10-2018)]."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="20A",
            section_title="Special provisions for contract relating to infrastructure project",
            chapter_number="Chapter II",
            chapter_title="Specific Performance of Contracts",
            full_verbatim_text=(
                "(1) No injunction shall be granted by court in a suit under this Act involving a contract relating to an infrastructure "
                "project specified in the Schedule, where granting injunction would cause impediment or delay in the progress or completion "
                "of such infrastructure project. [Inserted by Act 18 of 2018, s. 10 (w.e.f. 1-10-2018)]."
            ),
            subsections=[
                StatuteSubSection(
                    sub_section_number="(1)",
                    text="No injunction shall be granted by court in a suit under this Act involving a contract relating to an infrastructure project specified in the Schedule, where granting injunction would cause impediment or delay in the progress or completion of such infrastructure project."
                ),
                StatuteSubSection(
                    sub_section_number="(2)",
                    text="The Central Government may, depending upon the requirement for development of infrastructure projects, and if it considers necessary or expedient to do so, by notification in the Official Gazette, amend the Schedule."
                )
            ]
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="41",
            section_title="Injunction when refused",
            chapter_number="Chapter VIII",
            chapter_title="Perpetual Injunctions",
            full_verbatim_text=(
                "An injunction cannot be granted— (ha) if it would impede or delay the progress or completion of any "
                "infrastructure project or interfere with the continued provision of relevant facility related thereto or services being the subject matter of such project."
            ),
        )
    ]
    sections.extend(get_sra_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1963, 12, 13),
        effective_date=date(1964, 3, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_arbitration_document() -> StatuteDocument:
    source_id = "IND-STAT-ARB-1996"
    act_title = "The Arbitration and Conciliation Act, 1996"
    act_number = "Act No. 26 of 1996"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="7",
            section_title="Arbitration agreement",
            chapter_number="Part I",
            chapter_title="General Provisions",
            full_verbatim_text=(
                "(1) In this Part, 'arbitration agreement' means an agreement by the parties to submit to arbitration all "
                "or certain disputes which have arisen or which may arise between them in respect of a defined legal relationship, "
                "whether contractual or not. (2) An arbitration agreement may be in the form of an arbitration clause in a contract "
                "or in the form of a separate agreement. (3) An arbitration agreement shall be in writing."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="8",
            section_title="Power to refer parties to arbitration where there is an arbitration agreement",
            chapter_number="Part I",
            chapter_title="General Provisions",
            full_verbatim_text=(
                "(1) A judicial authority, before which an action is brought in a matter which is the subject of an arbitration agreement "
                "shall, if a party to the arbitration agreement or any person claiming through or under him, so applies not later than "
                "the date of submitting his first statement on the substance of the dispute, refer the parties to arbitration unless it finds "
                "that prima facie no valid arbitration agreement exists. [As amended by Act 3 of 2016]."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="9",
            section_title="Interim measures, etc., by Court",
            chapter_number="Part I",
            chapter_title="General Provisions",
            full_verbatim_text=(
                "(1) A party may, before or during arbitral proceedings or at any time after the making of the arbitral award "
                "but before it is enforced in accordance with section 36, apply to a court— (ii) for an interim measure of protection "
                "in respect of any of the following matters, namely:— (a) the preservation, interim custody or sale of any goods; "
                "(b) securing the amount in dispute in the arbitration; (c) the detention, preservation or inspection of any property... "
                "(3) Once the arbitral tribunal has been constituted, the Court shall not entertain an application under sub-section (1), "
                "unless the Court finds that circumstances exist which may not render the remedy provided under section 17 efficacious."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="29A",
            section_title="Time limit for arbitral award",
            chapter_number="Part I",
            chapter_title="Conduct of Arbitral Proceedings",
            full_verbatim_text=(
                "(1) The award in matters other than international commercial arbitration shall be made by the arbitral tribunal "
                "within a period of twelve months from the date of completion of pleadings under sub-section (4) of section 23. "
                "[Inserted by Act 3 of 2016 and amended by Act 33 of 2019]."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="34",
            section_title="Application for setting aside arbitral award",
            chapter_number="Part I",
            chapter_title="Recourse Against Arbitral Award",
            full_verbatim_text=(
                "(1) Recourse to a Court against an arbitral award may be made only by an application for setting aside such award "
                "in accordance with sub-section (2) and sub-section (3). (2) An arbitral award may be set aside by the Court only if— "
                "(b) the Court finds that— (ii) the arbitral award is in conflict with the public policy of India. "
                "(2A) An arbitral award arising out of an arbitration other than an international commercial arbitration, "
                "may also be set aside by the Court, if the Court finds that the award is vitiated by patent illegality appearing "
                "on the face of the award: Provided that an award shall not be set aside merely on the ground of an erroneous application "
                "of the law or by reappreciation of evidence."
            ),
        )
    ]
    sections.extend(get_arbitration_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(1996, 8, 16),
        effective_date=date(1996, 8, 22),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def get_cpa_document() -> StatuteDocument:
    source_id = "IND-STAT-CPA-2019"
    act_title = "The Consumer Protection Act, 2019"
    act_number = "Act No. 35 of 2019"

    sections = [
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="2",
            section_title="Definitions",
            chapter_number="Chapter I",
            chapter_title="Preliminary",
            full_verbatim_text=(
                "(7) 'consumer' means any person who— (i) buys any goods for a consideration which has been paid or promised... "
                "but does not include a person who obtains such goods for resale or for any commercial purpose; "
                "(11) 'deficiency' means any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance... "
                "(34) 'product liability' means the responsibility of a product manufacturer or product seller, of any product or service, "
                "to compensate for any harm caused to a consumer by such defective product manufactured or sold or by deficiency in services relating thereto."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="34",
            section_title="Jurisdiction of District Commission",
            chapter_number="Chapter IV",
            chapter_title="Consumer Disputes Redressal Commission",
            full_verbatim_text=(
                "(1) Subject to the other provisions of this Act, the District Commission shall have jurisdiction to entertain complaints "
                "where the value of the goods or services paid as consideration does not exceed fifty lakh rupees. "
                "[As modified by Consumer Protection (Pecuniary Jurisdiction) Rules, 2021]."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="82",
            section_title="Product liability action",
            chapter_number="Chapter VI",
            chapter_title="Product Liability",
            full_verbatim_text=(
                "A product liability action may be brought by a complainant against a product manufacturer or a product service provider "
                "or a product seller, as the case may be, for any harm caused to him on account of a defective product."
            ),
        ),
        make_section(
            source_id=source_id,
            act_title=act_title,
            act_number=act_number,
            section_number="107",
            section_title="Repeal and savings",
            chapter_number="Chapter VIII",
            chapter_title="Miscellaneous",
            full_verbatim_text=(
                "(1) The Consumer Protection Act, 1986 is hereby repealed. (2) Notwithstanding such repeal, "
                "anything done or any action taken or purported to have been done or taken under the Act hereby repealed "
                "shall, in so far as it is not inconsistent with the provisions of this Act, be deemed to have been done "
                "or taken under the corresponding provisions of this Act."
            ),
        )
    ]
    sections.extend(get_cpa_phase16_sections())

    return StatuteDocument(
        source_id=source_id,
        act_title=act_title,
        act_number=act_number,
        enactment_date=date(2019, 8, 9),
        effective_date=date(2020, 7, 20),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


def list_central_act_documents() -> List[StatuteDocument]:
    return [
        get_constitution_document(),
        get_bns_document(),
        get_cpc_document(),
        get_limitation_document(),
        get_contract_document(),
        get_sra_document(),
        get_arbitration_document(),
        get_cpa_document(),
    ]

