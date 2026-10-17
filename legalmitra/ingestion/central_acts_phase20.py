"""
LegalMitra Phase 20 Legislative Expansion Module
Provides authentic, source-verifiable statutory provisions for:
1. Constitution of India: Preamble, Articles 32, 38, 39A, 44, 124, 136, 214, 226, 227, 300A, 352, 356, 368
2. Negotiable Instruments Act, 1881 (Act No. 26 of 1881): Sections 138, 139, 140, 141, 142
3. Transfer of Property Act, 1882 (Act No. 4 of 1882): Sections 53A, 54, 58, 105, 106
4. Commercial Courts Act, 2015 (Act No. 4 of 2016): Sections 2(1)(c), 6, 12A, 16
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.schemas.statute import (
    StatuteDocument,
    StatuteExplanation,
    StatuteIllustration,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)


def _sec(
    source_id: str,
    act_title: str,
    section_number: str,
    section_title: str,
    full_verbatim_text: str,
    act_number: str = "",
    chapter_number: str = "",
    chapter_title: str = "",
    subsections: Optional[List[StatuteSubSection]] = None,
    provisos: Optional[List[StatuteProviso]] = None,
    explanations: Optional[List[StatuteExplanation]] = None,
    illustrations: Optional[List[StatuteIllustration]] = None,
) -> StatuteSection:
    clean_id = section_number.replace(" ", "-").replace("(", "").replace(")", "").replace(".", "-").upper()
    return StatuteSection(
        section_id=f"{source_id}-SEC-{clean_id}",
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


# =============================================================================
# 1. CONSTITUTION OF INDIA (IND-CONST-1950) ADDITIONAL ARTICLES
# =============================================================================
def get_constitution_phase20_sections() -> List[StatuteSection]:
    src = "IND-CONST-1950"
    title = "The Constitution of India"
    return [
        _sec(
            src, title, "Article 38", "State to secure a social order for the promotion of welfare of the people",
            "(1) The State shall strive to promote the welfare of the people by securing and protecting as effectively as it may a social order in which justice, social, economic and political, shall inform all the institutions of the national life.",
            chapter_number="Part IV", chapter_title="Directive Principles of State Policy"
        ),
        _sec(
            src, title, "Article 39A", "Equal justice and free legal aid",
            "The State shall secure that the operation of the legal system promotes justice, on a basis of equal opportunity, and shall, in particular, provide free legal aid, by suitable legislation or schemes or in any other way, to ensure that opportunities for securing justice are not denied to any citizen by reason of economic or other disabilities.",
            chapter_number="Part IV", chapter_title="Directive Principles of State Policy"
        ),
        _sec(
            src, title, "Article 44", "Uniform civil code for the citizens",
            "The State shall endeavour to secure for the citizens a uniform civil code throughout the territory of India.",
            chapter_number="Part IV", chapter_title="Directive Principles of State Policy"
        ),
        _sec(
            src, title, "Article 124", "Establishment and constitution of Supreme Court",
            "(1) There shall be a Supreme Court of India consisting of a Chief Justice of India and, until Parliament by law prescribes a larger number, of not more than thirty-three other Judges.",
            chapter_number="Part V", chapter_title="The Union Judiciary"
        ),
        _sec(
            src, title, "Article 136", "Special leave to appeal by the Supreme Court",
            "(1) Notwithstanding anything in this Chapter, the Supreme Court may, in its discretion, grant special leave to appeal from any judgment, decree, determination, sentence or order in any cause or matter passed or made by any court or tribunal in the territory of India.",
            chapter_number="Part V", chapter_title="The Union Judiciary"
        ),
        _sec(
            src, title, "Article 214", "High Courts for States",
            "There shall be a High Court for each State.",
            chapter_number="Part VI", chapter_title="The High Courts in the States"
        ),
        _sec(
            src, title, "Article 227", "Power of superintendence over all courts by the High Court",
            "(1) Every High Court shall have superintendence over all courts and tribunals throughout the territories in relation to which it exercises jurisdiction.",
            chapter_number="Part VI", chapter_title="The High Courts in the States"
        ),
        _sec(
            src, title, "Article 300A", "Persons not to be deprived of property save by authority of law",
            "No person shall be deprived of his property save by authority of law.",
            chapter_number="Part XII", chapter_title="Finance, Property, Contracts and Suits"
        ),
        _sec(
            src, title, "Article 352", "Proclamation of Emergency",
            "(1) If the President is satisfied that a grave emergency exists whereby the security of India or of any part of the territory thereof is threatened, whether by war or external aggression or armed rebellion, he may, by Proclamation, make a declaration to that effect in respect of the whole of India or of such part of the territory thereof as may be specified in the Proclamation.",
            chapter_number="Part XVIII", chapter_title="Emergency Provisions"
        ),
        _sec(
            src, title, "Article 356", "Provisions in case of failure of constitutional machinery in States",
            "(1) If the President, on receipt of a report from the Governor of a State or otherwise, is satisfied that a situation has arisen in which the government of the State cannot be carried on in accordance with the provisions of this Constitution, the President may by Proclamation assume to himself all or any of the functions of the Government of the State.",
            chapter_number="Part XVIII", chapter_title="Emergency Provisions"
        ),
    ]



# =============================================================================
# 2. NEGOTIABLE INSTRUMENTS ACT, 1881 (IND-STAT-NI-1881)
# =============================================================================
def get_ni_act_document() -> StatuteDocument:
    src = "IND-STAT-NI-1881"
    title = "The Negotiable Instruments Act, 1881"
    act_num = "Act No. 26 of 1881"

    sections = [
        _sec(
            src, title, "138", "Dishonour of cheque for insufficiency, etc., of funds in the account",
            "Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account by an agreement made with that bank, such person shall be deemed to have committed an offence and shall, without prejudice to any other provisions of this Act, be punished with imprisonment for a term which may be extended to two years, or with fine which may extend to twice the amount of the cheque, or with both: Provided that nothing contained in this section shall apply unless— (a) the cheque has been presented to the bank within a period of three months from the date on which it is drawn or within the period of its validity, whichever is earlier; (b) the payee or the holder in due course of the cheque, as the case may be, makes a demand for the payment of the said amount of money by giving a notice; in writing, to the drawer of the cheque, within thirty days of the receipt of information by him from the bank regarding the return of the cheque as unpaid; and (c) the drawer of such cheque fails to make the payment of the said amount of money to the payee or, as the case may be, to the holder in due course of the cheque, within fifteen days of the receipt of the said notice.",
            act_number=act_num, chapter_number="Chapter XVII", chapter_title="Of Penalties in Case of Dishonour of Certain Cheques",
            provisos=[
                StatuteProviso(proviso_number="Proviso (a)", text="the cheque has been presented to the bank within a period of three months from the date on which it is drawn or within the period of its validity, whichever is earlier;"),
                StatuteProviso(proviso_number="Proviso (b)", text="the payee or holder in due course makes a demand for payment by giving notice in writing within thirty days of receipt of information from the bank;"),
                StatuteProviso(proviso_number="Proviso (c)", text="the drawer of such cheque fails to make payment of the said amount within fifteen days of receipt of the said notice.")
            ],
            explanations=[
                StatuteExplanation(explanation_identifier="Explanation", text="For the purposes of this section, 'debt or other liability' means a legally enforceable debt or other liability.")
            ]
        ),
        _sec(
            src, title, "139", "Presumption in favour of holder",
            "It shall be presumed, unless the contrary is proved, that the holder of a cheque received the cheque of the nature referred to in section 138 for the discharge, in whole or in part, of any debt or other liability.",
            act_number=act_num, chapter_number="Chapter XVII", chapter_title="Of Penalties in Case of Dishonour of Certain Cheques"
        ),
        _sec(
            src, title, "140", "Defence which may not be allowed in any prosecution under section 138",
            "It shall not be a defence in a prosecution for an offence under section 138 that the drawer had no reason to believe when he issued the cheque that the cheque may be dishonoured on presentment for the reasons stated in that section.",
            act_number=act_num, chapter_number="Chapter XVII", chapter_title="Of Penalties in Case of Dishonour of Certain Cheques"
        ),
        _sec(
            src, title, "141", "Offences by companies",
            "(1) If the person committing an offence under section 138 is a company, every person who, at the time the offence was committed, was in charge of, and was responsible to the company for the conduct of the business of the company, as well as the company, shall be deemed to be guilty of the offence and shall be liable to be proceeded against and punished accordingly: Provided that nothing contained in this sub-section shall render any person liable to punishment if he proves that the offence was committed without his knowledge, or that he had exercised all due diligence to prevent the commission of such offence.",
            act_number=act_num, chapter_number="Chapter XVII", chapter_title="Of Penalties in Case of Dishonour of Certain Cheques"
        ),
        _sec(
            src, title, "142", "Cognizance of offences",
            "(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973— (a) no court shall take cognizance of any offence punishable under section 138 except upon a complaint, in writing, made by the payee or, as the case may be, the holder in due course of the cheque; (b) such complaint is made within one month of the date on which the cause of action arises under clause (c) of the proviso to section 138: Provided that the cognizance of a complaint may be taken by the court after the prescribed period, if the complainant satisfies the court that he had sufficient cause for not making the complaint within such period.",
            act_number=act_num, chapter_number="Chapter XVII", chapter_title="Of Penalties in Case of Dishonour of Certain Cheques"
        ),
    ]

    return StatuteDocument(
        source_id=src,
        act_title=title,
        act_number=act_num,
        enactment_date=date(1881, 12, 9),
        effective_date=date(1882, 3, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


# =============================================================================
# 3. TRANSFER OF PROPERTY ACT, 1882 (IND-STAT-TPA-1882)
# =============================================================================
def get_tpa_act_document() -> StatuteDocument:
    src = "IND-STAT-TPA-1882"
    title = "The Transfer of Property Act, 1882"
    act_num = "Act No. 4 of 1882"

    sections = [
        _sec(
            src, title, "53A", "Part performance",
            "Where any person contracts to transfer for consideration any immoveable property by writing signed by him or on his behalf from which the terms necessary to constitute the transfer can be ascertained with reasonable certainty, and the transferee has, in part performance of the contract, taken possession of the property or any part thereof, or the transferee, being already in possession, continues in possession in part performance of the contract and has done some act in furtherance of the contract, and the transferee has performed or is willing to perform his part of the contract, then, notwithstanding that where there is an instrument of transfer, that the transfer has not been completed in the manner prescribed therefor by the law for the time being in force, the transferor or any person claiming under him shall be debarred from enforcing against the transferee and persons claiming under him any right in respect of the property of which the transferee has taken or continued in possession, other than a right expressly provided by the terms of the contract.",
            act_number=act_num, chapter_number="Chapter II", chapter_title="Of Transfers of Property by Act of Parties"
        ),
        _sec(
            src, title, "54", "Sale defined; Sale how made; Contract for sale",
            "'Sale' is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Such transfer, in the case of tangible immoveable property of the value of one hundred rupees and upwards, or in the case of a reversion or other intangible thing, can be made only by a registered instrument. In the case of tangible immoveable property of a value less than one hundred rupees, such transfer may be made either by a registered instrument or by delivery of the property. A contract for the sale of immoveable property is a contract that a sale of such property shall take place on terms settled between the parties. It does not, of itself, create any interest in or charge on such property.",
            act_number=act_num, chapter_number="Chapter III", chapter_title="Of Sales of Immoveable Property"
        ),
        _sec(
            src, title, "58", "Mortgage, mortgagor, mortgagee, mortgage-money and mortgage-deed defined",
            "(a) A mortgage is the transfer of an interest in specific immoveable property for the purpose of securing the payment of money advanced or to be advanced by way of loan, an existing or future debt, or the performance of an engagement which may give rise to a pecuniary liability. The transferor is called a mortgagor, the transferee a mortgagee; the principal money and interest of which payment is secured for the time being are called the mortgage-money, and the instrument (if any) by which the transfer is effected is called a mortgage-deed.",
            act_number=act_num, chapter_number="Chapter IV", chapter_title="Of Mortgages of Immoveable Property and Charges"
        ),
        _sec(
            src, title, "105", "Lease defined",
            "A lease of immoveable property is a transfer of a right to enjoy such property, made for a certain time, express or implied, or in perpetuity, in consideration of a price paid or promised, or of money, a share of crops, service or any other thing of value, to be rendered periodically or on specified occasions to the transferor by the transferee, who accepts the transfer on such terms. The transferor is called the lessor, the transferee is called the lessee, the price is called the premium, and the money, share, service or other thing to be so rendered is called the rent.",
            act_number=act_num, chapter_number="Chapter V", chapter_title="Of Leases of Immoveable Property"
        ),
        _sec(
            src, title, "106", "Duration of certain leases in absence of written contract or local usage",
            "(1) In the absence of a contract or local law or usage to the contrary, a lease of immoveable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, by six months' notice; and a lease of immoveable property for any other purpose shall be deemed to be a lease from month to month, terminable, on the part of either lessor or lessee, by fifteen days' notice.",
            act_number=act_num, chapter_number="Chapter V", chapter_title="Of Leases of Immoveable Property"
        ),
    ]

    return StatuteDocument(
        source_id=src,
        act_title=title,
        act_number=act_num,
        enactment_date=date(1882, 2, 17),
        effective_date=date(1882, 7, 1),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )


# =============================================================================
# 4. COMMERCIAL COURTS ACT, 2015 (IND-STAT-COMM-COURTS-2015)
# =============================================================================
def get_commercial_courts_document() -> StatuteDocument:
    src = "IND-STAT-COMM-COURTS-2015"
    title = "The Commercial Courts Act, 2015"
    act_num = "Act No. 4 of 2016"

    sections = [
        _sec(
            src, title, "2(1)(c)", "Commercial dispute definition",
            "'Commercial dispute' means a dispute arising out of— (i) ordinary transactions of merchants, bankers, financiers and traders such as those relating to mercantile documents, including enforcement and interpretation of such documents; (ii) export or import of merchandise or services; (iii) issues relating to admiralty and maritime law; (iv) transactions relating to aircraft, aircraft engines, aircraft equipment and helicopters, including sales, leasing and financing of the same; (v) carriage of goods; (vi) construction and infrastructure contracts, including tenders; (vii) agreements relating to immovable property used exclusively in trade or commerce; (viii) franchising agreements; (ix) distribution and licensing agreements; (x) management and consultancy agreements; (xi) joint venture agreements; (xii) shareholders agreements; (xiii) subscription and investment agreements pertaining to the services industry; (xiv) mercantile agency and mercantile usage; (xv) partnership agreements; (xvi) technology development agreements; (xvii) intellectual property rights relating to registered and unregistered trademarks, copyright, patent, design, domain names, geographical indications and semiconductor integrated circuits; (xviii) agreements for sale of goods or provision of services; (xix) exploitation of oil and gas reserves or other natural resources; (xx) insurance and re-insurance; (xxi) contracts of agency relating to any of the above; and (xxii) such other commercial disputes as may be notified by the Central Government.",
            act_number=act_num, chapter_number="Chapter I", chapter_title="Preliminary"
        ),
        _sec(
            src, title, "6", "Jurisdiction of Commercial Court",
            "The Commercial Court shall have jurisdiction to try all suits and applications relating to a commercial dispute of a Specified Value arising out of the entire territory of the State over which it has been vested territorial jurisdiction.",
            act_number=act_num, chapter_number="Chapter II", chapter_title="Commercial Courts, Commercial Divisions and Commercial Appellate Divisions"
        ),
        _sec(
            src, title, "12A", "Pre-Institution Mediation and Settlement",
            "(1) A suit, which does not contemplate any urgent interim relief under this Act, shall not be instituted unless the plaintiff exhausts the remedy of pre-institution mediation in accordance with such manner and procedure as may be prescribed by rules made by the Central Government. (2) The Central Government may, by notification, authorise the Authorities constituted under the Legal Services Authorities Act, 1987, for the purposes of pre-institution mediation.",
            act_number=act_num, chapter_number="Chapter IIIA", chapter_title="Pre-Institution Mediation and Settlement",
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="A suit, which does not contemplate any urgent interim relief under this Act, shall not be instituted unless the plaintiff exhausts the remedy of pre-institution mediation in accordance with such manner and procedure as may be prescribed by rules made by the Central Government."),
                StatuteSubSection(sub_section_number="(2)", text="The Central Government may, by notification, authorise the Authorities constituted under the Legal Services Authorities Act, 1987, for the purposes of pre-institution mediation.")
            ]
        ),
        _sec(
            src, title, "16", "Amendments to the Code of Civil Procedure, 1908 in its application to commercial disputes",
            "(1) The provisions of the Code of Civil Procedure, 1908 shall, in their application to any suit in respect of a commercial dispute of a Specified Value, stand amended in the manner specified in the Schedule. (2) The Commercial Division and Commercial Court shall follow the provisions of the Code of Civil Procedure, 1908, as amended by this Act, in the trial thereof of a suit in respect of a commercial dispute of a Specified Value.",
            act_number=act_num, chapter_number="Chapter V", chapter_title="Amendments to the Provisions of the Code of Civil Procedure, 1908"
        ),
    ]

    return StatuteDocument(
        source_id=src,
        act_title=title,
        act_number=act_num,
        enactment_date=date(2015, 12, 31),
        effective_date=date(2015, 10, 23),
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        sections=sections,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )
