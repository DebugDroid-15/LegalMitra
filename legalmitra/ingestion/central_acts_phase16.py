"""
LegalMitra Phase 16 Central Legislation Expansion Module
Provides foundational substantive provisions, schedules, and definitions for the 8 Central Acts:
1. Constitution of India (Arts 12, 13, 15, 16, 22, 25, 51A, 141, 142)
2. Bharatiya Nyaya Sanhita, 2023 (Secs 14, 20, 22, 34, 35, 63, 100, 109, 115, 117, 152, 316)
3. Code of Civil Procedure, 1908 (Secs 15, 16, 20, 96, 100, 114, 115, Order VII R 11, Order XXXIX R 2)
4. Limitation Act, 1963 (Secs 4, 6, 17, 19, Schedule Arts 54, 65, 137)
5. Indian Contract Act, 1872 (Secs 11, 13, 14, 15, 16, 17, 18, 23, 25, 124, 126, 148, 182)
6. Specific Relief Act, 1963 (Secs 5, 6, 16, 34, 38, Schedule)
7. Arbitration and Conciliation Act, 1996 (Secs 11, 12, 16, 17, 31, 36, 37, Seventh Schedule)
8. Consumer Protection Act, 2019 (Secs 10, 18, 21, 35, 38, 47, 58, 83, 86, 87)
"""

from __future__ import annotations
from typing import List
from legalmitra.schemas.statute import (
    StatuteExplanation,
    StatuteIllustration,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)
from legalmitra.core.enums import LegalReviewStatus


def _sec(
    source_id: str,
    act_title: str,
    section_number: str,
    section_title: str,
    full_verbatim_text: str,
    act_number: str = "",
    chapter_number: str = "",
    chapter_title: str = "",
    subsections: List[StatuteSubSection] = None,
    provisos: List[StatuteProviso] = None,
    explanations: List[StatuteExplanation] = None,
    illustrations: List[StatuteIllustration] = None,
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
# 1. CONSTITUTION OF INDIA (IND-CONST-1950) ADDITIONAL PROVISIONS
# =============================================================================
def get_constitution_phase16_sections() -> List[StatuteSection]:
    src = "IND-CONST-1950"
    title = "The Constitution of India"
    return [
        _sec(
            src, title, "Article 12", "Definition of State",
            "In this Part, unless the context otherwise requires, 'the State' includes the Government and Parliament of India and the Government and the Legislature of each of the States and all local or other authorities within the territory of India or under the control of the Government of India.",
            chapter_number="Part III", chapter_title="Fundamental Rights"
        ),
        _sec(
            src, title, "Article 13", "Laws inconsistent with or in derogation of the fundamental rights",
            "(1) All laws in force in the territory of India immediately before the commencement of this Constitution, in so far as they are inconsistent with the provisions of this Part, shall, to the extent of such inconsistency, be void. (2) The State shall not make any law which takes away or abridges the rights conferred by this Part and any law made in contravention of this clause shall, to the extent of the contravention, be void.",
            chapter_number="Part III", chapter_title="Fundamental Rights",
            subsections=[
                StatuteSubSection(sub_section_number="(1)", text="All laws in force in the territory of India immediately before the commencement of this Constitution, in so far as they are inconsistent with the provisions of this Part, shall, to the extent of such inconsistency, be void."),
                StatuteSubSection(sub_section_number="(2)", text="The State shall not make any law which takes away or abridges the rights conferred by this Part and any law made in contravention of this clause shall, to the extent of the contravention, be void.")
            ]
        ),
        _sec(
            src, title, "Article 15", "Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth",
            "(1) The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. (2) No citizen shall, on grounds only of religion, race, caste, sex, place of birth or any of them, be subject to any disability, liability, restriction or condition with regard to access to shops, public restaurants, hotels and places of public entertainment.",
            chapter_number="Part III", chapter_title="Fundamental Rights"
        ),
        _sec(
            src, title, "Article 16", "Equality of opportunity in matters of public employment",
            "(1) There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State. (2) No citizen shall, on grounds only of religion, race, caste, sex, descent, place of birth, residence or any of them, be ineligible for, or discriminated against in respect of, any employment or office under the State.",
            chapter_number="Part III", chapter_title="Fundamental Rights"
        ),
        _sec(
            src, title, "Article 22", "Protection against arrest and detention in certain cases",
            "(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice. (2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest.",
            chapter_number="Part III", chapter_title="Fundamental Rights"
        ),
        _sec(
            src, title, "Article 25", "Freedom of conscience and free profession, practice and propagation of religion",
            "(1) Subject to public order, morality and health and to the other provisions of this Part, all persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion.",
            chapter_number="Part III", chapter_title="Fundamental Rights"
        ),
        _sec(
            src, title, "Article 51A", "Fundamental duties",
            "It shall be the duty of every citizen of India— (a) to abide by the Constitution and respect its ideals and institutions, the National Flag and the National Anthem; (b) to cherish and follow the noble ideals which inspired our national struggle for freedom; (c) to uphold and protect the sovereignty, unity and integrity of India; (h) to develop the scientific temper, humanism and the spirit of inquiry and reform; (j) to strive towards excellence in all spheres of individual and collective activity.",
            chapter_number="Part IVA", chapter_title="Fundamental Duties"
        ),
        _sec(
            src, title, "Article 141", "Law declared by Supreme Court to be binding on all courts",
            "The law declared by the Supreme Court shall be binding on all courts within the territory of India.",
            chapter_number="Part V", chapter_title="The Union Judiciary"
        ),
        _sec(
            src, title, "Article 142", "Enforcement of decrees and orders of Supreme Court and orders as to discovery, etc.",
            "(1) The Supreme Court in the exercise of its jurisdiction may pass such decree or make such order as is necessary for doing complete justice in any cause or matter pending before it, and any decree so passed or order so made shall be enforceable throughout the territory of India.",
            chapter_number="Part V", chapter_title="The Union Judiciary"
        ),
    ]


# =============================================================================
# 2. BHARATIYA NYAYA SANHITA, 2023 (IND-STAT-BNS-2023) ADDITIONAL PROVISIONS
# =============================================================================
def get_bns_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-BNS-2023"
    title = "The Bharatiya Nyaya Sanhita, 2023"
    act_num = "Act No. 45 of 2023"
    return [
        _sec(
            src, title, "14", "Act done by a person bound, or by mistake of fact believing himself bound, by law",
            "Nothing is an offence which is done by a person who is, or who by reason of a mistake of fact and not by reason of a mistake of law in good faith believes himself to be, bound by law to do it.",
            act_num, "Chapter III", "General Exceptions"
        ),
        _sec(
            src, title, "20", "Act of a child under seven years of age",
            "Nothing is an offence which is done by a child under seven years of age.",
            act_num, "Chapter III", "General Exceptions"
        ),
        _sec(
            src, title, "22", "Act of a person of unsound mind",
            "Nothing is an offence which is done by a person who, at the time of doing it, by reason of unsoundness of mind, is incapable of knowing the nature of the act, or that he is doing what is either wrong or contrary to law.",
            act_num, "Chapter III", "General Exceptions"
        ),
        _sec(
            src, title, "34", "Things done in private defence",
            "Nothing is an offence which is done in the exercise of the right of private defence.",
            act_num, "Chapter III", "Right of Private Defence"
        ),
        _sec(
            src, title, "35", "Right of private defence of the body and of property",
            "Every person has a right, subject to the restrictions contained in section 37, to defend— (a) his own body, and the body of any other person, against any offence affecting the human body; (b) the property, whether movable or immovable, of himself or of any other person, against any act which is an offence falling under the definition of theft, robbery, mischief or criminal trespass, or which is an attempt to commit theft, robbery, mischief or criminal trespass.",
            act_num, "Chapter III", "Right of Private Defence"
        ),
        _sec(
            src, title, "63", "Rape",
            "A man is said to commit 'rape' if he penetrates his penis, to any extent, into the vagina, mouth, urethra or anus of a woman or makes her to do so with him or any other person... under any of the circumstances falling under the descriptions: against her will, without her consent, or with consent obtained by putting her in fear of death or hurt.",
            act_num, "Chapter V", "Of Offences Against Women and Children"
        ),
        _sec(
            src, title, "100", "Culpable homicide",
            "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely by such act to cause death, commits the offence of culpable homicide.",
            act_num, "Chapter VI", "Of Offences Affecting Life"
        ),
        _sec(
            src, title, "109", "Attempt to murder",
            "Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine; and if hurt is caused to any person by such act, the offender shall be liable either to imprisonment for life, or to such punishment as is hereinbefore mentioned.",
            act_num, "Chapter VI", "Of Offences Affecting Life"
        ),
        _sec(
            src, title, "115", "Voluntarily causing hurt",
            "(1) Whoever does any act with the intention of thereby causing hurt to any person, or with the knowledge that he is likely thereby to cause hurt to any person, and does thereby cause hurt to any person, is said 'voluntarily to cause hurt'. (2) Whoever, except in the case provided for by sub-section (1) of section 122, voluntarily causes hurt, shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to ten thousand rupees, or with both.",
            act_num, "Chapter VI", "Of Hurt"
        ),
        _sec(
            src, title, "117", "Voluntarily causing grievous hurt",
            "(1) Whoever voluntarily causes hurt, if the hurt which he intends to cause or knows himself to be likely to cause is grievous hurt, and if the hurt which he causes is grievous hurt, is said 'voluntarily to cause grievous hurt'. (2) Whoever voluntarily causes grievous hurt shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
            act_num, "Chapter VI", "Of Hurt"
        ),
        _sec(
            src, title, "152", "Act endangering sovereignty, unity and integrity of India",
            "Whoever, purposely or knowingly, by words, either spoken or written, or by signs, or by visible representation, or by electronic communication or by use of financial mean, or otherwise, excites or attempts to excite, secession or armed rebellion or subversive activities, or encourages feelings of separatist activities or endangers sovereignty or unity and integrity of India; or indulges in or commits any such act shall be punished with imprisonment for life or with imprisonment which may extend to seven years, and shall also be liable to fine.",
            act_num, "Chapter VII", "Of Offences Against the State"
        ),
        _sec(
            src, title, "316", "Criminal breach of trust",
            "(1) Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged, commits 'criminal breach of trust'. (2) Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both.",
            act_num, "Chapter XVII", "Of Offences Against Property"
        ),
    ]


# =============================================================================
# 3. CODE OF CIVIL PROCEDURE, 1908 (IND-STAT-CPC-1908) ADDITIONAL PROVISIONS
# =============================================================================
def get_cpc_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-CPC-1908"
    title = "The Code of Civil Procedure, 1908"
    act_num = "Act No. 5 of 1908"
    return [
        _sec(
            src, title, "15", "Court in which suits to be instituted",
            "Every suit shall be instituted in the Court of the lowest grade competent to try it.",
            act_num, "Part I", "Suits in General - Place of Suing"
        ),
        _sec(
            src, title, "16", "Suits to be instituted where subject-matter situate",
            "Subject to the pecuniary or other limitations prescribed by any law, suits— (a) for the recovery of immovable property; (b) for the partition of immovable property; (c) for foreclosure, sale or redemption in the case of a mortgage of or charge upon immovable property; (d) for the determination of any other right to or interest in immovable property; (e) for compensation for wrong to immovable property; (f) for the recovery of movable property actually under distraint or attachment, shall be instituted in the Court within the local limits of whose jurisdiction the property is situate.",
            act_num, "Part I", "Place of Suing"
        ),
        _sec(
            src, title, "20", "Other suits to be instituted where defendants reside or cause of action arises",
            "Subject to the limitations aforesaid, every suit shall be instituted in a Court within the local limits of whose jurisdiction— (a) the defendant, or each of the defendants where there are more than one, at the time of the commencement of the suit, actually and voluntarily resides, or carries on business, or personally works for gain; or (c) the cause of action, wholly or in part, arises.",
            act_num, "Part I", "Place of Suing"
        ),
        _sec(
            src, title, "96", "Appeal from original decree",
            "(1) Save where otherwise expressly provided in the body of this Code or by any other law for the time being in force, an appeal shall lie from every decree passed by any Court exercising original jurisdiction to the Court authorized to hear appeals from the decisions of such Court. (2) An appeal may lie from an original decree passed ex parte. (3) No appeal shall lie from a decree passed by the Court with the consent of parties.",
            act_num, "Part VII", "Appeals - Appeals from Original Decrees"
        ),
        _sec(
            src, title, "100", "Second appeal",
            "(1) Save as otherwise expressly provided in the body of this Code or by any other law for the time being in force, an appeal shall lie to the High Court from every decree passed in appeal by any Court subordinate to the High Court, if the High Court is satisfied that the case involves a substantial question of law. (2) An appeal may lie under this section from an appellate decree passed ex parte.",
            act_num, "Part VII", "Appeals - Second Appeals"
        ),
        _sec(
            src, title, "114", "Review",
            "Subject as aforesaid, any person considering himself aggrieved— (a) by a decree or order from which an appeal is allowed by this Code, but from which no appeal has been preferred, (b) by a decree or order from which no appeal is allowed by this Code, or (c) by a decision on a reference from a Court of Small Causes, may apply for a review of judgment to the Court which passed the decree or made the order, and the Court may make such order thereon as it thinks fit.",
            act_num, "Part VIII", "Reference, Review and Revision"
        ),
        _sec(
            src, title, "115", "Revision",
            "(1) The High Court may call for the record of any case which has been decided by any Court subordinate to such High Court and in which no appeal lies thereto, and if such subordinate Court appears— (a) to have exercised a jurisdiction not vested in it by law, or (b) to have failed to exercise a jurisdiction so vested, or (c) to have acted in the exercise of its jurisdiction illegally or with material irregularity, the High Court may make such order in the case as it thinks fit.",
            act_num, "Part VIII", "Reference, Review and Revision"
        ),
        _sec(
            src, title, "Order VII Rule 11", "Rejection of plaint",
            "The plaint shall be rejected in the following cases:— (a) where it does not disclose a cause of action; (b) where the relief claimed is undervalued, and the plaintiff, on being required by the Court to correct the valuation within a time to be fixed by the Court, fails to do so; (c) where the relief claimed is properly valued, but the plaint is returned upon paper insufficiently stamped; (d) where the suit appears from the statement in the plaint to be barred by any law; (e) where it is not filed in duplicate; (f) where the plaintiff fails to comply with the provisions of rule 9.",
            act_num, "Schedule I", "Order VII - Plaint"
        ),
        _sec(
            src, title, "Order XXXIX Rule 2", "Injunction to restrain repetition or continuance of breach",
            "(1) In any suit for restraining the defendant from committing a breach of contract or other injury of any kind, whether compensation is claimed in the suit or not, the plaintiff may, at any time after the commencement of the suit, apply to the Court for a temporary injunction to restrain the defendant from committing the breach of contract or injury complained of.",
            act_num, "Schedule I", "Order XXXIX - Temporary Injunctions"
        ),
    ]


# =============================================================================
# 4. THE LIMITATION ACT, 1963 (IND-STAT-LIMIT-1963) ADDITIONAL PROVISIONS
# =============================================================================
def get_limitation_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-LIMIT-1963"
    title = "The Limitation Act, 1963"
    act_num = "Act No. 36 of 1963"
    return [
        _sec(
            src, title, "4", "Expiry of prescribed period when court is closed",
            "Where the prescribed period for any suit, appeal or application expires on a day when the court is closed, the suit, appeal or application may be instituted, preferred or made on the day when the court re-opens.",
            act_num, "Part II", "Limitation of Suits, Appeals and Applications"
        ),
        _sec(
            src, title, "6", "Legal disability",
            "(1) Where a person entitled to institute a suit or make an application for the execution of a decree is, at the time from which the prescribed period is to be reckoned, a minor or insane, or an idiot, he may institute the suit or make the application within the same period after the disability has ceased, as would otherwise have been allowed from the time specified therefor in the third column of the Schedule.",
            act_num, "Part II", "Limitation of Suits, Appeals and Applications"
        ),
        _sec(
            src, title, "17", "Effect of fraud or mistake",
            "(1) Where, in the case of any suit or application for which a period of limitation is prescribed by this Act,— (a) the suit or application is founded upon the fraud of the defendant or respondent or his agent; or (b) the knowledge of the right or title on which a suit or application is founded is concealed by the fraud of any such person as aforesaid; or (c) the suit or application is for relief from the consequences of a mistake, the period of limitation shall not begin to run until the plaintiff or applicant has discovered the fraud or the mistake or could, with reasonable diligence, have discovered it.",
            act_num, "Part III", "Computation of Period of Limitation"
        ),
        _sec(
            src, title, "19", "Effect of payment on account of debt or of interest on legacy",
            "Where payment on account of a debt or of interest on a legacy is made before the expiration of the prescribed period by the person liable to pay the debt or legacy, or by his agent duly authorised in this behalf, a fresh period of limitation shall be computed from the time when the payment was made: Provided that an acknowledgment of the payment appears in the handwriting of, or in a writing signed by, the person making the payment.",
            act_num, "Part III", "Computation of Period of Limitation"
        ),
        _sec(
            src, title, "Schedule Article 54", "Suit for specific performance of a contract",
            "Description of suit: For specific performance of a contract. Period of limitation: Three years. Time from which period begins to run: The date fixed for the performance, or, if no such date is fixed, when the plaintiff has notice that performance is refused.",
            act_num, "The Schedule", "First Division - Suits Relating to Contracts"
        ),
        _sec(
            src, title, "Schedule Article 65", "Suit for possession of immovable property based on title",
            "Description of suit: For possession of immovable property or any interest therein based on title. Period of limitation: Twelve years. Time from which period begins to run: When the possession of the defendant becomes adverse to the plaintiff.",
            act_num, "The Schedule", "First Division - Suits Relating to Immovable Property"
        ),
        _sec(
            src, title, "Schedule Article 137", "Any other application for which no period of limitation is provided",
            "Description of application: Any other application for which no period of limitation is provided elsewhere in this Division. Period of limitation: Three years. Time from which period begins to run: When the right to apply accrues.",
            act_num, "The Schedule", "Third Division - Applications"
        ),
    ]


# =============================================================================
# 5. INDIAN CONTRACT ACT, 1872 (IND-STAT-ICA-1872) ADDITIONAL PROVISIONS
# =============================================================================
def get_contract_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-ICA-1872"
    title = "The Indian Contract Act, 1872"
    act_num = "Act No. 9 of 1872"
    return [
        _sec(
            src, title, "11", "Who are competent to contract",
            "Every person is competent to contract who is of the age of majority according to the law to which he is subject, and who is of sound mind and is not disqualified from contracting by any law to which he is subject.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "13", "Consent defined",
            "Two or more persons are said to consent when they agree upon the same thing in the same sense (consensus ad idem).",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "14", "Free consent defined",
            "Consent is said to be free when it is not caused by— (1) coercion, as defined in section 15, or (2) undue influence, as defined in section 16, or (3) fraud, as defined in section 17, or (4) misrepresentation, as defined in section 18, or (5) mistake, subject to the provisions of sections 20, 21 and 22.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "15", "Coercion defined",
            "'Coercion' is the committing, or threatening to commit, any act forbidden by the Indian Penal Code, or the unlawful detaining, or threatening to detain, any property, to the prejudice of any person whatever, with the intention of causing any person to enter into an agreement.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "16", "Undue influence defined",
            "(1) A contract is said to be induced by 'undue influence' where the relations subsisting between the parties are such that one of the parties is in a position to dominate the will of the other and uses that position to obtain an unfair advantage over the other.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "17", "Fraud defined",
            "'Fraud' means and includes any of the following acts committed by a party to a contract, or with his connivance, or by his agent, with intent to deceive another party thereto or his agent, or to induce him to enter into the contract: (1) the suggestion, as a fact, of that which is not true, by one who does not believe it to be true; (2) the active concealment of a fact by one having knowledge or belief of the fact; (3) a promise made without any intention of performing it.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "18", "Misrepresentation defined",
            "'Misrepresentation' means and includes— (1) the positive assertion, in a manner not warranted by the information of the person making it, of that which is not true, though he believes it to be true; (2) any breach of duty which, without an intent to deceive, gains an advantage to the person committing it; (3) causing, however innocently, a party to an agreement, to make a mistake as to the substance of the thing which is the subject of the agreement.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "23", "What considerations and objects are lawful, and what not",
            "The consideration or object of an agreement is lawful, unless— it is forbidden by law; or is of such a nature that, if permitted, it would defeat the provisions of any law; or is fraudulent; or involves or implies injury to the person or property of another; or the Court regards it as immoral, or opposed to public policy. In each of these cases, the consideration or object of an agreement is said to be unlawful. Every agreement of which the object or consideration is unlawful is void.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "25", "Agreement without consideration, void, unless it is in writing and registered",
            "An agreement made without consideration is void, unless— (1) it is expressed in writing and registered under the law for the time being in force for the registration of documents, and is made on account of natural love and affection between parties standing in a near relation to each other; or unless (2) it is a promise to compensate, wholly or in part, a person who has already voluntarily done something for the promisor; or unless (3) it is a promise, made in writing and signed by the person to be charged therewith, to pay wholly or in part a debt of which the creditor might have enforced payment but for the law for the limitation of suits.",
            act_num, "Chapter II", "Of Contracts, Voidable Contracts and Void Agreements"
        ),
        _sec(
            src, title, "124", "Contract of indemnity defined",
            "A contract by which one party promises to save the other from loss caused to him by the conduct of the promisor himself, or by the conduct of any other person, is called a 'contract of indemnity'.",
            act_num, "Chapter VIII", "Of Indemnity and Guarantee"
        ),
        _sec(
            src, title, "126", "Contract of guarantee, surety, principal debtor and creditor",
            "A 'contract of guarantee' is a contract to perform the promise, or discharge the liability, of a third person in case of his default. The person who gives the guarantee is called the 'surety'; the person in respect of whose default the guarantee is given is called the 'principal debtor', and the person to whom the guarantee is given is called the 'creditor'. A guarantee may be either oral or written.",
            act_num, "Chapter VIII", "Of Indemnity and Guarantee"
        ),
        _sec(
            src, title, "148", "Bailment, bailor and bailee defined",
            "A 'bailment' is the delivery of goods by one person to another for some purpose, upon a contract that they shall, when the purpose is accomplished, be returned or otherwise disposed of according to the directions of the person delivering them. The person delivering the goods is called the 'bailor'. The person to whom they are delivered is called the 'bailee'.",
            act_num, "Chapter IX", "Of Bailment"
        ),
        _sec(
            src, title, "182", "Agent and principal defined",
            "An 'agent' is a person employed to do any act for another, or to represent another in dealings with third persons. The person for whom such act is done, or who is so represented, is called the 'principal'.",
            act_num, "Chapter X", "Agency"
        ),
    ]


# =============================================================================
# 6. THE SPECIFIC RELIEF ACT, 1963 (IND-STAT-SRA-1963) ADDITIONAL PROVISIONS
# =============================================================================
def get_sra_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-SRA-1963"
    title = "The Specific Relief Act, 1963"
    act_num = "Act No. 47 of 1963"
    return [
        _sec(
            src, title, "5", "Recovery of specific immovable property",
            "A person entitled to the possession of specific immovable property may recover it in the manner provided by the Code of Civil Procedure, 1908.",
            act_num, "Chapter I", "Recovering Possession of Property"
        ),
        _sec(
            src, title, "6", "Suit by person dispossessed of immovable property",
            "(1) If any person is dispossessed without his consent of immovable property otherwise than in due course of law, he or any person through whom he has been in possession or any person claiming through him may, by suit, recover possession thereof, notwithstanding any other title that may be set up in such suit. (2) No suit under this section shall be brought— (a) after the expiry of six months from the date of dispossession; or (b) against the Government.",
            act_num, "Chapter I", "Recovering Possession of Property"
        ),
        _sec(
            src, title, "16", "Personal bars to relief",
            "Specific performance of a contract cannot be enforced in favour of a person— (a) who has obtained substituted performance of contract under section 20; or (b) who has become incapable of performing, or violates any essential term of, the contract that on his part remains to be performed, or acts in fraud of the contract, or wilfully acts at variance with, or in subversion of, the relation intended to be established by the contract; or (c) who fails to prove that he has performed or has always been ready and willing to perform the essential terms of the contract which are to be performed by him.",
            act_num, "Chapter II", "Specific Performance of Contracts"
        ),
        _sec(
            src, title, "34", "Discretion of court as to declaration of status or right",
            "Any person entitled to any legal character, or to any right as to any property, may institute a suit against any person denying, or interested to deny, his title to such character or right, and the court may in its discretion make therein a declaration that he is so entitled, and the plaintiff need not in such suit ask for any further relief: Provided that no court shall make any such declaration where the plaintiff, being able to seek further relief than a mere declaration of title, omits to do so.",
            act_num, "Chapter VI", "Declaratory Decrees"
        ),
        _sec(
            src, title, "38", "Perpetual injunction when granted",
            "(1) Subject to the other provisions contained in or referred to by this Chapter, a perpetual injunction may be granted to the plaintiff to prevent the breach of an obligation existing in his favour, whether expressly or by implication. (2) When any such obligation arises from contract, the court shall be guided by the rules and provisions contained in Chapter II. (3) When the defendant invades or threatens to invade the plaintiff's right to, or enjoyment of, property, the court may grant a perpetual injunction in the following cases: (a) where the defendant is trustee of the property for the plaintiff; (b) where there exists no standard for ascertaining the actual damage caused; (c) where the invasion is such that compensation in money would not afford adequate relief; (d) where the injunction is necessary to prevent a multiplicity of judicial proceedings.",
            act_num, "Chapter VIII", "Perpetual Injunctions"
        ),
        _sec(
            src, title, "Schedule", "Category of projects and Infrastructure Sub-Sectors",
            "Schedule referred to in section 20A: 1. Transport (Roads and bridges, Ports, Shipyards, Inland Waterways, Airports, Railway track, tunnels, viaducts, bridges, Urban Public Transport). 2. Energy (Electricity Generation, Electricity Transmission, Electricity Distribution, Oil pipelines, Oil and gas storage, Gas pipelines). 3. Water and Sanitation (Solid Waste Management, Water supply pipelines, Sewage treatment plants, Irrigation). 4. Communication (Telecommunication, Telecommunication towers). 5. Social and Commercial Infrastructure (Affordable Housing, Hospitals, Tourism infrastructure).",
            act_num, "The Schedule", "Infrastructure Sub-Sectors"
        ),
    ]


# =============================================================================
# 7. ARBITRATION AND CONCILIATION ACT, 1996 (IND-STAT-ARB-1996) ADDITIONAL PROVISIONS
# =============================================================================
def get_arbitration_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-ARB-1996"
    title = "The Arbitration and Conciliation Act, 1996"
    act_num = "Act No. 26 of 1996"
    return [
        _sec(
            src, title, "11", "Appointment of arbitrators",
            "(1) A person of any nationality may be an arbitrator, unless otherwise agreed by the parties. (2) Subject to sub-section (6), the parties are free to agree on a procedure for appointing the arbitrator or arbitrators. (6) Where, under an appointment procedure agreed upon by the parties, a party fails to act as required under that procedure, the appointment shall be made, on an application of the party, by the arbitral institution designated by the Supreme Court, in case of international commercial arbitration, or by the High Court, in case of arbitrations other than international commercial arbitration.",
            act_num, "Chapter III", "Composition of Arbitral Tribunal"
        ),
        _sec(
            src, title, "12", "Grounds for challenge",
            "(1) When a person is approached in connection with his possible appointment as an arbitrator, he shall disclose in writing any circumstances,— (a) such as the existence either direct or indirect, of any past or present relationship with or interest in any of the parties or in relation to the subject-matter in dispute, whether financial, business, professional or other kind, which is likely to give rise to justifiable doubts as to his independence or impartiality; and (b) which are likely to affect his ability to devote sufficient time to the arbitration and in particular his ability to complete the entire arbitration within a period of twelve months. (5) Notwithstanding any prior agreement to the contrary, any person whose relationship with the parties or counsel falls under any of the categories specified in the Seventh Schedule shall be ineligible to be appointed as an arbitrator.",
            act_num, "Chapter III", "Composition of Arbitral Tribunal"
        ),
        _sec(
            src, title, "16", "Competence of arbitral tribunal to rule on its jurisdiction",
            "(1) The arbitral tribunal may rule on its own jurisdiction, including ruling on any objections with respect to the existence or validity of the arbitration agreement, and for that purpose,— (a) an arbitration clause which forms part of a contract shall be treated as an agreement independent of the other terms of the contract; and (b) a decision by the arbitral tribunal that the contract is null and void shall not entail ipso jure the invalidity of the arbitration clause (Doctrine of Kompetenz-Kompetenz).",
            act_num, "Chapter IV", "Jurisdiction of Arbitral Tribunals"
        ),
        _sec(
            src, title, "17", "Interim measures ordered by arbitral tribunal",
            "(1) A party may, during the arbitral proceedings, apply to the arbitral tribunal— (i) for the appointment of a guardian for a minor or person of unsound mind; (ii) for an interim measure of protection in respect of any of the following matters: (a) the preservation, interim custody or sale of any goods; (b) securing the amount in dispute; (c) the detention, preservation or inspection of any property; (e) such other interim measure of protection as may appear to the arbitral tribunal to be just and convenient. (2) Any order issued by the arbitral tribunal under this section shall be deemed to be an order of the Court for all purposes and shall be enforceable under the Code of Civil Procedure, 1908.",
            act_num, "Chapter IV", "Jurisdiction of Arbitral Tribunals"
        ),
        _sec(
            src, title, "31", "Form and contents of arbitral award",
            "(1) An arbitral award shall be made in writing and shall be signed by the members of the arbitral tribunal. (2) The arbitral award shall state the reasons upon which it is based, unless: (a) the parties have agreed that no reasons are to be given, or (b) the award is an arbitral award on agreed terms under section 30. (7) (a) Unless otherwise agreed by the parties, where and in so far as an arbitral award is for the payment of money, the arbitral tribunal may include in the sum for which the award is made interest, at such rate as it deems reasonable, on the whole or any part of the money.",
            act_num, "Chapter VI", "Making of Arbitral Award and Termination of Proceedings"
        ),
        _sec(
            src, title, "36", "Enforcement of arbitral award",
            "(1) Where the time for making an application to set aside the arbitral award under section 34 has expired, then, subject to the provisions of sub-section (2), such award shall be enforced in accordance with the provisions of the Code of Civil Procedure, 1908 in the same manner as if it were a decree of the court. (2) Where an application to set aside the arbitral award has been filed in the Court under section 34, the filing of such an application shall not by itself render that award unenforceable, unless the Court grants an order of stay of the operation of the said arbitral award in accordance with the provisions of sub-section (3).",
            act_num, "Chapter VIII", "Finality and Enforcement of Arbitral Awards"
        ),
        _sec(
            src, title, "37", "Appealable orders",
            "(1) An appeal shall lie from the following orders (and from no others) to the Court authorized by law to hear appeals from original decrees of the Court passing the order, namely:— (a) refusing to refer the parties to arbitration under section 8; (b) granting or refusing to grant any measure under section 9; (c) setting aside or refusing to set aside an arbitral award under section 34.",
            act_num, "Chapter IX", "Appeals"
        ),
        _sec(
            src, title, "Seventh Schedule", "Arbitrators relationship with the parties or counsel",
            "Seventh Schedule (Section 12(5)): Categories of ineligibility: 1. The arbitrator is an employee, consultant, advisor or has any other past or present business relationship with a party. 2. The arbitrator currently represents or advises one of the parties or an affiliate of one of the parties. 3. The arbitrator has a significant financial or personal interest in one of the parties or the outcome of the dispute. 4. The arbitrator is a close family member of a party or of someone who represents a party.",
            act_num, "Schedules", "Seventh Schedule"
        ),
    ]


# =============================================================================
# 8. CONSUMER PROTECTION ACT, 2019 (IND-STAT-CPA-2019) ADDITIONAL PROVISIONS
# =============================================================================
def get_cpa_phase16_sections() -> List[StatuteSection]:
    src = "IND-STAT-CPA-2019"
    title = "The Consumer Protection Act, 2019"
    act_num = "Act No. 35 of 2019"
    return [
        _sec(
            src, title, "10", "Establishment of Central Consumer Protection Authority",
            "(1) The Central Government shall, by notification, establish with effect from such date as it may appoint, a Central Authority to be known as the Central Consumer Protection Authority to promote, protect and enforce the rights of consumers as a class.",
            act_num, "Chapter III", "Central Consumer Protection Authority"
        ),
        _sec(
            src, title, "18", "Powers and functions of Central Authority",
            "(1) The Central Authority shall: (a) protect, promote and enforce the rights of consumers as a class, and prevent violation of consumer rights under this Act; (b) prevent unfair trade practices and ensure that no person engages himself in unfair trade practices; (c) ensure that no false or misleading advertisement is made of any goods or services; (d) ensure that no person takes part in the publication of any false or misleading advertisement; (e) mandate recall of goods or withdrawal of services which are dangerous, hazardous or unsafe.",
            act_num, "Chapter III", "Central Consumer Protection Authority"
        ),
        _sec(
            src, title, "21", "Power of Central Authority to issue directions and penalties against false or misleading advertisements",
            "(1) Where the Central Authority is satisfied after investigation that any advertisement is false or misleading and is prejudicial to the interest of any consumer or is in contravention of consumer rights, it may, by order, issue directions to the concerned trader or manufacturer or endorser or advertiser or publisher, as the case may be, to discontinue such advertisement or to modify the same. (2) The Central Authority may impose on any manufacturer or endorser a penalty which may extend to ten lakh rupees, and for every subsequent contravention, a penalty which may extend to fifty lakh rupees.",
            act_num, "Chapter III", "Central Consumer Protection Authority"
        ),
        _sec(
            src, title, "35", "Manner in which complaint shall be made to District Commission",
            "(1) A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by: (a) the consumer— (i) to whom such goods are sold or delivered or agreed to be sold or delivered or such service is provided or agreed to be provided; or (ii) who alleges unfair trade practice in respect of such goods or service; (b) any recognized consumer association; (c) one or more consumers, where there are numerous consumers having the same interest; or (d) the Central Government, the Central Authority or the State Government.",
            act_num, "Chapter IV", "Consumer Disputes Redressal Commission"
        ),
        _sec(
            src, title, "38", "Procedure on admission of complaint",
            "(1) The District Commission shall, on admission of a complaint, refer a copy of the admitted complaint, within twenty-one days from the date of its admission to the opposite party mentioned in the complaint directing him to give his version of the case within a period of thirty days or such extended period not exceeding fifteen days as may be granted by it.",
            act_num, "Chapter IV", "Consumer Disputes Redressal Commission"
        ),
        _sec(
            src, title, "47", "Jurisdiction of State Commission",
            "(1) Subject to the other provisions of this Act, the State Commission shall have jurisdiction: (a) to entertain— (i) complaints where the value of the goods or services paid as consideration, exceeds rupees fifty lakh, but does not exceed rupees two crore (as revised); (ii) complaints against unfair contracts, where the value of goods or services paid as consideration exceeds fifty lakh rupees but does not exceed ten crore rupees; (b) to entertain appeals against the orders of any District Commission within the State.",
            act_num, "Chapter IV", "State Consumer Disputes Redressal Commission"
        ),
        _sec(
            src, title, "58", "Jurisdiction of National Commission",
            "(1) Subject to the other provisions of this Act, the National Commission shall have jurisdiction: (a) to entertain— (i) complaints where the value of the goods or services paid as consideration exceeds rupees two crore (as revised); (ii) complaints against unfair contracts, where the value of goods or services paid as consideration exceeds ten crore rupees; (b) to entertain appeals against the orders of any State Commission; (c) to entertain appeals against the orders of the Central Authority.",
            act_num, "Chapter IV", "National Consumer Disputes Redressal Commission"
        ),
        _sec(
            src, title, "83", "Liability of product manufacturer",
            "A product manufacturer shall be liable in a product liability action, if— (a) the product contains a manufacturing defect; or (b) the product is defective in design; or (c) there is a deviation from manufacturing specifications; or (d) the product does not conform to the express warranty; or (e) the product fails to contain adequate instructions of correct usage to prevent any harm or any warning regarding improper or incorrect usage.",
            act_num, "Chapter VI", "Product Liability"
        ),
        _sec(
            src, title, "86", "Liability of product seller",
            "A product seller who is not a product manufacturer shall be liable in a product liability action, if— (a) he has exercised substantial control over the designing, testing, manufacturing, packaging or labelling of a product that caused harm; or (b) he has altered or modified the product and such alteration or modification was the substantial factor in causing the harm; or (c) he has made an express warranty of a product independent of any express warranty made by a manufacturer; or (d) the product has been sold by him and the identity of product manufacturer of such product is not known, or if known, the service of notice or process or warrant cannot be effected on him.",
            act_num, "Chapter VI", "Product Liability"
        ),
        _sec(
            src, title, "87", "Exceptions to product liability action",
            "(1) A product liability action cannot be brought against the product seller if, at the time of harm, the product was misused, altered, or modified. (2) In any product liability action, a product manufacturer shall not be liable, if— (a) the product was purchased by an employer for use at the workplace and the product manufacturer had provided warnings or instructions to such employer; (b) the product was sold as a component or material to be used in another product and necessary warnings had been given; (c) the product was one which was legally meant to be used only under the supervision of an expert.",
            act_num, "Chapter VI", "Product Liability"
        ),
    ]

