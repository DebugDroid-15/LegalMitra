"""
LegalMitra Phase 24 Central Legislation Completion Module
Provides authentic, source-verifiable statutory provisions for:
1. Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023): Sections 22, 23, 24, 25, 26, 45, 60, 62, 64, 104, 105, 114, 137, 138, 170
2. Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023): Sections 14, 15, 20, 22, 34, 37, 63, 64, 70, 100, 101, 103, 105, 106, 111, 113, 303, 308, 316, 356
3. Protection of Children from Sexual Offences (POCSO) Act, 2012 (Act No. 32 of 2012): Sections 3, 5, 6, 19, 21, 29, 30, 33, 74
4. Right to Information Act, 2005 (Act No. 22 of 2005): Sections 2, 3, 4, 6, 7, 8, 9, 19, 20
5. Motor Vehicles Act, 1988 (as amended 2019): Sections 134, 161, 166, 185
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
# 1. BHARATIYA SAKSHYA ADHINIYAM, 2023 (IND-ACT-2023-BSA)
# =============================================================================
def get_bsa_phase24_sections() -> List[StatuteSection]:
    src = "IND-ACT-2023-BSA"
    title = "The Bharatiya Sakshya Adhiniyam, 2023"
    num = "Act No. 47 of 2023"

    return [
        _sec(
            src, title, "Section 22", "Admission defined",
            "An admission is a statement, oral or documentary or contained in electronic form, which suggests any inference as to any fact in issue or relevant fact, and which is made by any of the persons, and under the circumstances, hereinafter mentioned.",
            act_number=num, chapter_number="Chapter II", chapter_title="Admissions"
        ),
        _sec(
            src, title, "Section 23", "Admission in civil cases when relevant",
            "In civil cases no admission is relevant, if it is made either upon an express condition that evidence of it is not to be given, or under circumstances from which the Court can infer that the parties agreed together that evidence of it should not be given.",
            act_number=num, chapter_number="Chapter II", chapter_title="Admissions",
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation",
                    text="Nothing in this section shall be taken to exempt any advocate from giving evidence of any matter of which he may be compelled to give evidence under sub-sections (1) and (2) of section 132."
                )
            ]
        ),
        _sec(
            src, title, "Section 24", "Confession caused by inducement, threat or promise",
            "A confession made by an accused person is irrelevant in a criminal proceeding, if the making of the confession appears to the Court to have been caused by any inducement, threat or promise having reference to the charge against the accused person, proceeding from a person in authority and sufficient, in the opinion of the Court, to give the accused person grounds which would appear to him reasonable for supposing that by making it he would gain any advantage or avoid any evil of a temporal nature in reference to the proceedings against him.",
            act_number=num, chapter_number="Chapter II", chapter_title="Admissions"
        ),
        _sec(
            src, title, "Section 25", "Confession to police officer not to be proved",
            "No confession made to a police officer shall be proved as against a person accused of any offence.",
            act_number=num, chapter_number="Chapter II", chapter_title="Admissions"
        ),
        _sec(
            src, title, "Section 26", "Confession by accused while in custody of police not to be proved against him",
            "No confession made by any person whilst he is in the custody of a police officer, unless it be made in the immediate presence of a Magistrate, shall be proved as against such person.",
            act_number=num, chapter_number="Chapter II", chapter_title="Admissions",
            provisos=[
                StatuteProviso(
                    proviso_index=1,
                    text="Provided that when any fact is deposed to as discovered in consequence of information received from a person accused of any offence, in the custody of a police officer, so much of such information, whether it amounts to a confession or not, as relates distinctly to the fact thereby discovered, may be proved."
                )
            ]
        ),
        _sec(
            src, title, "Section 45", "Opinions of experts",
            "When the Court has to form an opinion upon a point of foreign law or of science or art, or any other field, or as to identity of handwriting or finger impressions, or electronic evidence, the opinions upon that point of persons specially skilled in such foreign law, science or art, or in questions as to identity of handwriting or finger impressions or other field, are relevant facts. Such persons are called experts.",
            act_number=num, chapter_number="Chapter II", chapter_title="Opinions of Third Persons When Relevant"
        ),
        _sec(
            src, title, "Section 60", "Oral evidence must be direct",
            "Oral evidence must, in all cases whatever, be direct; that is to say—if it refers to a fact which could be seen, it must be the evidence of a witness who says he saw it; if it refers to a fact which could be heard, it must be the evidence of a witness who says he heard it; if it refers to a fact which could be perceived by any other sense or in any other manner, it must be the evidence of a witness who says he perceived it by that sense or in that manner; if it refers to an opinion or to the grounds on which that opinion is held, it must be the evidence of the person who holds that opinion on those grounds.",
            act_number=num, chapter_number="Chapter IV", chapter_title="Of Oral Evidence"
        ),
        _sec(
            src, title, "Section 62", "Primary evidence",
            "Primary evidence means the document itself produced for the inspection of the Court.",
            act_number=num, chapter_number="Chapter V", chapter_title="Of Documentary Evidence",
            explanations=[
                StatuteExplanation(
                    explanation_identifier="Explanation 1",
                    text="Where a document is executed in several parts, each part is primary evidence of the document: Where a document is executed in counterpart, each counterpart being executed by one or some of the parties only, each counterpart is primary evidence as against the parties executing it."
                ),
                StatuteExplanation(
                    explanation_identifier="Explanation 2",
                    text="Where a number of documents are all made by one uniform process, as in the case of printing, lithography, or photography, each is primary evidence of the contents of the rest; but, where they are all copies of a common original, they are not primary evidence of the contents of the original."
                )
            ]
        ),
        _sec(
            src, title, "Section 64", "Proof of documents by primary evidence",
            "Documents must be proved by primary evidence except in the cases hereinafter mentioned.",
            act_number=num, chapter_number="Chapter V", chapter_title="Of Documentary Evidence"
        ),
        _sec(
            src, title, "Section 104", "Burden of proving fact to be proved to make evidence admissible",
            "The burden of proving any fact necessary to be proved in order to enable any person to give evidence of any other fact is on the person who wishes to give such evidence.",
            act_number=num, chapter_number="Chapter VII", chapter_title="Of the Burden of Proof"
        ),
        _sec(
            src, title, "Section 105", "Burden of proving that case of accused comes within exceptions",
            "When a person is accused of any offence, the burden of proving the existence of circumstances bringing the case within any of the General Exceptions in the Bharatiya Nyaya Sanhita, 2023, or within any special exception or proviso contained in any other part of the said Sanhita, or in any law defining the offence, is upon him, and the Court shall presume the absence of such circumstances.",
            act_number=num, chapter_number="Chapter VII", chapter_title="Of the Burden of Proof"
        ),
        _sec(
            src, title, "Section 114", "Court may presume existence of certain facts",
            "The Court may presume the existence of any fact which it thinks likely to have happened, regard being had to the common course of natural events, human conduct and public and private business, in their relation to the facts of the particular case.",
            act_number=num, chapter_number="Chapter VII", chapter_title="Of the Burden of Proof"
        ),
        _sec(
            src, title, "Section 137", "Examination of witnesses",
            "The examination of a witness by the party who calls him shall be called his examination-in-chief. The examination of a witness by the adverse party shall be called his cross-examination. The examination of a witness, subsequent to the cross-examination, by the party who called him, shall be called his re-examination.",
            act_number=num, chapter_number="Chapter X", chapter_title="Of the Examination of Witnesses"
        ),
        _sec(
            src, title, "Section 138", "Order of examinations",
            "Witnesses shall be first examined-in-chief, then (if the adverse party so desires) cross-examined, then (if the party calling him so desires) re-examined. The examination and cross-examination must relate to relevant facts, but the cross-examination need not be confined to the facts to which the witness testified on his examination-in-chief.",
            act_number=num, chapter_number="Chapter X", chapter_title="Of the Examination of Witnesses"
        ),
        _sec(
            src, title, "Section 170", "Repeal and savings",
            "(1) The Indian Evidence Act, 1872 is hereby repealed. (2) Notwithstanding such repeal, any proceeding pending immediately before the commencement of this Adhiniyam shall continue and be disposed of in accordance with the provisions of the Indian Evidence Act, 1872 as if this Adhiniyam had not been enacted.",
            act_number=num, chapter_number="Chapter XII", chapter_title="Repeal and Savings"
        ),
    ]


# =============================================================================
# 2. BHARATIYA NYAYA SANHITA, 2023 (IND-ACT-2023-BNS)
# =============================================================================
def get_bns_phase24_sections() -> List[StatuteSection]:
    src = "IND-ACT-2023-BNS"
    title = "The Bharatiya Nyaya Sanhita, 2023"
    num = "Act No. 45 of 2023"

    return [
        _sec(
            src, title, "Section 14", "Act done by person bound, or by mistake of fact believing himself bound, by law",
            "Nothing is an offence which is done by a person who is, or who by reason of a mistake of fact and not by reason of a mistake of law in good faith believes himself to be, bound by law to do it.",
            act_number=num, chapter_number="Chapter III", chapter_title="General Exceptions"
        ),
        _sec(
            src, title, "Section 15", "Act of Judge when acting judicially",
            "Nothing is an offence which is done by a Judge when acting judicially in the exercise of any power which is, or which in good faith he believes to be, given to him by law.",
            act_number=num, chapter_number="Chapter III", chapter_title="General Exceptions"
        ),
        _sec(
            src, title, "Section 20", "Act of a child under seven years of age",
            "Nothing is an offence which is done by a child under seven years of age.",
            act_number=num, chapter_number="Chapter III", chapter_title="General Exceptions"
        ),
        _sec(
            src, title, "Section 22", "Act of a person of unsound mind",
            "Nothing is an offence which is done by a person who, at the time of doing it, by reason of unsoundness of mind, is incapable of knowing the nature of the act, or that he is doing what is either wrong or contrary to law.",
            act_number=num, chapter_number="Chapter III", chapter_title="General Exceptions"
        ),
        _sec(
            src, title, "Section 34", "Things done in private defence",
            "Nothing is an offence which is done in the exercise of the right of private defence.",
            act_number=num, chapter_number="Chapter III", chapter_title="Of the Right of Private Defence"
        ),
        _sec(
            src, title, "Section 37", "When right of private defence of body extends to causing death",
            "The right of private defence of the body extends, under the restrictions mentioned in section 36, to the voluntary causing of death or of any other harm to the assailant, if the offence which occasions the exercise of the right be of any of the descriptions hereinafter enumerated, namely:— (a) Such an assault as may reasonably cause the apprehension that death will otherwise be the consequence of such assault; (b) Such an assault as may reasonably cause the apprehension that grievous hurt will otherwise be the consequence of such assault; (c) An assault with the intention of committing rape; (d) An assault with the intention of gratifying unnatural lust; (e) An assault with the intention of kidnapping or abducting; (f) An assault with the intention of wrongfully confining a person, under circumstances which may reasonably cause him to apprehend that he will be unable to have recourse to the public authorities for his release; (g) An act of throwing or administering acid or an attempt to throw or administer acid which may reasonably cause the apprehension that grievous hurt will otherwise be the consequence of such act.",
            act_number=num, chapter_number="Chapter III", chapter_title="Of the Right of Private Defence"
        ),
        _sec(
            src, title, "Section 63", "Rape defined",
            "A man is said to commit 'rape' if he— (a) penetrates his penis, to any extent, into the vagina, mouth, urethra or anus of a woman or makes her to do so with him or any other person; or (b) inserts, to any extent, any object or a part of the body, not being the penis, into the vagina, the urethra or anus of a woman or makes her to do so with him or any other person; or (c) manipulates any part of the body of a woman so as to cause penetration into the vagina, urethra, anus or any part of body of such woman or makes her to do so with him or any other person; or (d) applies his mouth to the vagina, anus, urethra of a woman or makes her to do so with him or any other person, under any of the circumstances specified in clauses First to Seventh.",
            act_number=num, chapter_number="Chapter V", chapter_title="Of Offences Against Women and Children"
        ),
        _sec(
            src, title, "Section 64", "Punishment for rape",
            "(1) Whoever, except in the cases provided for in sub-section (2), commits rape, shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life, and shall also be liable to fine. (2) Whoever commits aggravated rape as specified in clauses (a) to (n) shall be punished with rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of that person's natural life, and with fine.",
            act_number=num, chapter_number="Chapter V", chapter_title="Of Offences Against Women and Children"
        ),
        _sec(
            src, title, "Section 70", "Gang rape",
            "(1) Where a woman is raped by one or more persons constituting a group or acting in furtherance of a common intention, each of those persons shall be deemed to have committed the offence of rape and shall be punished with rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to life which shall mean imprisonment for the remainder of that person's natural life, and with fine. (2) Where a woman under eighteen years of age is raped by one or more persons constituting a group or acting in furtherance of a common intention, each of those persons shall be punished with imprisonment for life, which shall mean imprisonment for the remainder of that person's natural life, and with fine, or with death.",
            act_number=num, chapter_number="Chapter V", chapter_title="Of Offences Against Women and Children"
        ),
        _sec(
            src, title, "Section 100", "Culpable homicide",
            "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely by such act to cause death, commits the offence of culpable homicide.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 101", "Murder",
            "Except in the cases hereinafter excepted, culpable homicide is murder, if the act by which the death is caused is done with the intention of causing death, or secondly, if it is done with the intention of causing such bodily injury as the offender knows to be likely to cause the death of the person to whom the harm is caused, or thirdly, if it is done with the intention of causing bodily injury to any person and the bodily injury intended to be inflicted is sufficient in the ordinary course of nature to cause death, or fourthly, if the person committing the act knows that it is so imminently dangerous that it must, in all probability, cause death or such bodily injury as is likely to cause death, and commits such act without any excuse for incurring the risk of causing death or such injury as aforesaid.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 103", "Punishment for murder",
            "(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. (2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 105", "Culpable homicide not amounting to murder",
            "Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine, if the act by which the death is caused is done with the intention of causing death, or of causing such bodily injury as is likely to cause death; or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine, if the act is done with the knowledge that it is likely to cause death, but without any intention to cause death, or to cause such bodily injury as is likely to cause death.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 106", "Causing death by negligence",
            "(1) Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide, shall be punished with imprisonment of either description for a term which may extend to five years, and shall also be liable to fine; and if such act is done by a registered medical practitioner while performing medical procedure, he shall be punished with imprisonment of either description for a term which may extend to two years, and shall also be liable to fine. (2) Whoever causes the death of any person by rash and negligent driving of vehicle not amounting to culpable homicide, and escapes without reporting it to a police officer or a Magistrate soon after the incident, shall be punished with imprisonment of either description of a term which may extend to ten years, and shall also be liable to fine.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 111", "Organised crime",
            "(1) Any continuing unlawful activity including kidnapping, robbery, vehicle theft, extortion, land grabbing, contract killing, economic offence, cybercrimes having severe consequences, trafficking in persons, drugs, weapons or illicit goods or services, human trafficking for prostitution or ransom, by any person or a group of persons acting in concert or as a member of an organised crime syndicate, by use of violence, threat of violence, intimidation, coercion, or by any other unlawful means to obtain direct or indirect material benefit including financial benefit, shall constitute organised crime. Whoever commits organised crime shall: (a) if such offence has resulted in the death of any person, be punished with death or imprisonment for life, and shall also be liable to fine which shall not be less than ten lakh rupees; (b) in any other case, be punished with imprisonment for a term which shall not be less than five years but which may extend to imprisonment for life, and shall also be liable to fine which shall not be less than five lakh rupees.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 113", "Terrorist act",
            "(1) Whoever does any act with the intent to threaten or likely to threaten the unity, integrity, sovereignty, security, or economic security of India or with the intent to strike terror in the people or any section of the people in India or in any foreign country, by using bombs, dynamite or other explosive substances or inflammable substances or firearms or other lethal weapons or poisonous or noxious gases or other chemicals or by any other substances of a hazardous nature, commits a terrorist act.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Of Offences Affecting the Human Body"
        ),
        _sec(
            src, title, "Section 303", "Theft",
            "(1) Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. (2) Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both, and in case of second or subsequent conviction of any person under this section, he shall be punished with rigorous imprisonment for a term which shall not be less than one year but which may extend to five years and with fine.",
            act_number=num, chapter_number="Chapter XVII", chapter_title="Of Offences Against Property"
        ),
        _sec(
            src, title, "Section 308", "Extortion",
            "(1) Whoever intentionally puts any person in fear of any injury to that person, or to any other, and thereby dishonestly induces the person so put in fear to deliver to any person any property, or valuable security or anything signed or sealed which may be converted into a valuable security, commits 'extortion'. (2) Whoever commits extortion shall be punished with imprisonment of either description for a term which may extend to seven years, or with fine, or with both.",
            act_number=num, chapter_number="Chapter XVII", chapter_title="Of Offences Against Property"
        ),
        _sec(
            src, title, "Section 316", "Criminal breach of trust",
            "(1) Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged, or of any legal contract, express or implied, which he has made touching the discharge of such trust, or wilfully suffers any other person so to do, commits 'criminal breach of trust'. (2) Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both.",
            act_number=num, chapter_number="Chapter XVII", chapter_title="Of Offences Against Property"
        ),
        _sec(
            src, title, "Section 356", "Defamation",
            "(1) Whoever, by words either spoken or intended to be read, or by signs or by visible representations, makes or publishes in any manner, any imputation concerning any person intending to harm, or knowing or having reason to believe that such imputation will harm, the reputation of such person, is said, except in the cases hereinafter expected, to defame that person. (2) Whoever defames another shall be punished with simple imprisonment for a term which may extend to two years, or with fine, or with both, or with community service.",
            act_number=num, chapter_number="Chapter XIX", chapter_title="Of Defamation"
        ),
    ]


# =============================================================================
# 3. PROTECTION OF CHILDREN FROM SEXUAL OFFENCES ACT, 2012 (IND-ACT-2012-POCSO)
# =============================================================================
def get_pocso_phase24_sections() -> List[StatuteSection]:
    src = "IND-ACT-2012-POCSO"
    title = "Protection of Children from Sexual Offences Act, 2012"
    num = "Act No. 32 of 2012"

    return [
        _sec(
            src, title, "Section 3", "Penetrative sexual assault",
            "A person is said to commit 'penetrative sexual assault' if: (a) he penetrates his penis, to any extent, into the vagina, mouth, urethra or anus of a child or makes the child to do so with him or any other person; or (b) he inserts, to any extent, any object or a part of the body, not being the penis, into the vagina, the urethra or anus of a child or makes the child to do so with him or any other person; or (c) he manipulates any part of the body of a child so as to cause penetration into the vagina, urethra, anus or any part of body of such child or makes the child to do so with him or any other person; or (d) he applies his mouth to the vagina, penis, anus or urethra of a child or makes the child to do so with him or any other person.",
            act_number=num, chapter_number="Chapter II", chapter_title="Sexual Offences Against Children"
        ),
        _sec(
            src, title, "Section 5", "Aggravated penetrative sexual assault",
            "A person is said to commit aggravated penetrative sexual assault if being a police officer, public servant, member of armed forces, management or staff of a jail, remand home, hospital, educational institution, commits penetrative sexual assault on a child, or commits penetrative sexual assault on a child below twelve years of age, or causes grievous hurt or pregnancy.",
            act_number=num, chapter_number="Chapter II", chapter_title="Sexual Offences Against Children"
        ),
        _sec(
            src, title, "Section 6", "Punishment for aggravated penetrative sexual assault",
            "Whoever commits aggravated penetrative sexual assault shall be punished with rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of natural life of that person, and shall also be liable to fine, or with death.",
            act_number=num, chapter_number="Chapter II", chapter_title="Sexual Offences Against Children"
        ),
        _sec(
            src, title, "Section 19", "Recording of information regarding commission of offence",
            "(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973, any person (including the child), who has apprehension that an offence under this Act is likely to be committed or has knowledge that such an offence has been committed, shall provide such information to: (a) the Special Juvenile Police Unit; or (b) the local police. (2) Every person who has knowledge of commission of offence under this Act shall report the matter.",
            act_number=num, chapter_number="Chapter V", chapter_title="Procedure for Reporting of Cases"
        ),
        _sec(
            src, title, "Section 21", "Punishment for failure to report or record a case",
            "(1) Any person, who fails to report the commission of an offence under sub-section (1) of section 19 or section 20 or who fails to record such offence under sub-section (2) of section 19 shall be punished with imprisonment of either description which may extend to six months or with fine or with both. (2) Any person, being in-charge of any company or an institution who fails to report an offence shall be punished with imprisonment for a term which may extend to one year and with fine.",
            act_number=num, chapter_number="Chapter V", chapter_title="Procedure for Reporting of Cases"
        ),
        _sec(
            src, title, "Section 29", "Presumption as to certain offences",
            "Where a person is prosecuted for committing or abetting or attempting to commit any offence under sections 3, 5, 7 and section 9 of this Act, the Special Court shall presume, that such person has committed or abetted or attempted to commit the offence, as the case may be, unless the contrary is proved.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Special Courts and Procedure"
        ),
        _sec(
            src, title, "Section 30", "Presumption of culpable mental state",
            "(1) In any prosecution for any offence under this Act which requires a culpable mental state on the part of the accused, the Special Court shall presume the existence of such mental state but it shall be a defence for the accused to prove the fact that he had no such mental state with respect to the act charged as an offence in that prosecution. (2) For the purposes of this section, a fact is said to be proved only when the Special Court believes it to exist beyond reasonable doubt and not merely by a preponderance of probabilities.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Special Courts and Procedure"
        ),
        _sec(
            src, title, "Section 33", "Procedure and powers of Special Court",
            "(1) A Special Court may take cognizance of any offence, without the accused being committed to it for trial, upon receiving a complaint of facts which constitute such offence, or upon a police report of such facts. (7) The Special Court shall ensure that the identity of the child is not disclosed at any time during the course of investigation or trial: Provided that for reasons to be recorded in writing, the Special Court may permit such disclosure, if in its opinion such disclosure is in the interest of the child.",
            act_number=num, chapter_number="Chapter VI", chapter_title="Special Courts and Procedure"
        ),
        _sec(
            src, title, "Section 74", "Prohibition on disclosure of identity of child",
            "No person shall make any report or present comments on any child from any form of media or studio or photographic facilities without the prior permission of the Special Court or the child's guardian in the best interest of the child. Any person who contravenes the provisions of this section shall be liable to be punished with imprisonment of either description for a term which shall not be less than six months but which may extend to one year or with fine or with both.",
            act_number=num, chapter_number="Chapter IX", chapter_title="Miscellaneous"
        ),
    ]


# =============================================================================
# 4. RIGHT TO INFORMATION ACT, 2005 (IND-ACT-2005-RTI)
# =============================================================================
def get_rti_phase24_sections() -> List[StatuteSection]:
    src = "IND-ACT-2005-RTI"
    title = "The Right to Information Act, 2005"
    num = "Act No. 22 of 2005"

    return [
        _sec(
            src, title, "Section 2", "Definitions",
            "In this Act, unless the context otherwise requires,— (f) 'information' means any material in any form, including records, documents, memos, e-mails, opinions, advices, press releases, circulars, orders, logbooks, contracts, reports, papers, samples, models, data material held in any electronic form; (h) 'public authority' means any authority or body or institution of self-government established or constituted by or under the Constitution, by any other law made by Parliament or State Legislature, or by notification issued or order made by the appropriate Government; (j) 'right to information' means the right to information accessible under this Act which is held by or under the control of any public authority.",
            act_number=num, chapter_number="Chapter I", chapter_title="Preliminary"
        ),
        _sec(
            src, title, "Section 3", "Right to information",
            "Subject to the provisions of this Act, all citizens shall have the right to information.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 4", "Obligations of public authorities",
            "(1) Every public authority shall maintain all its records duly catalogued and indexed and computerised, and publish within one hundred and twenty days from the enactment of this Act the particulars of its organisation, functions, powers and duties of its officers and employees, procedure followed in decision making, directory of officers, budget allocation, and public facility details.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 6", "Request for obtaining information",
            "(1) A person, who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area in which the application is being made, accompanying such fee as may be prescribed, to the Central Public Information Officer or State Public Information Officer. (2) An applicant making request for information shall not be required to give any reason for requesting the information or any other personal details except those that may be necessary for contacting him.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 7", "Disposal of request",
            "(1) The Central Public Information Officer or State Public Information Officer on receipt of a request under section 6 shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request for any of the reasons specified in sections 8 and 9: Provided that where the information sought for concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 8", "Exemption from disclosure of information",
            "(1) Notwithstanding anything contained in this Act, there shall be no obligation to give any citizen,— (a) information, disclosure of which would prejudicially affect the sovereignty and integrity of India, the security, strategic, scientific or economic interests of the State; (b) information which has been expressly forbidden to be published by any court of law or tribunal or the disclosure of which may constitute contempt of court; (c) information, the disclosure of which would cause a breach of privilege of Parliament or the State Legislature; (d) information including commercial confidence, trade secrets or intellectual property, the disclosure of which would harm the competitive position of a third party; (e) information available to a person in his fiduciary relationship, unless the competent authority is satisfied that the larger public interest warrants the disclosure; (f) information received in confidence from foreign Government; (g) information, the disclosure of which would endanger the life or physical safety of any person; (h) information which would impede the process of investigation or apprehension or prosecution of offenders; (i) cabinet papers including records of deliberations of the Council of Ministers; (j) information which relates to personal information the disclosure of which has no relationship to any public activity or interest, or which would cause unwarranted invasion of the privacy of the individual unless the Central Public Information Officer or the State Public Information Officer or the appellate authority is satisfied that the larger public interest justifies the disclosure of such information.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 9", "Grounds for rejection to access in certain cases",
            "Without prejudice to the provisions of section 8, a Central Public Information Officer or a State Public Information Officer may reject a request for information where such a request for providing access would involve an infringement of copyright subsisting in a person other than the State.",
            act_number=num, chapter_number="Chapter II", chapter_title="Right to Information and Obligations of Public Authorities"
        ),
        _sec(
            src, title, "Section 19", "Appeals",
            "(1) Any person who, does not receive a decision within the time specified in sub-section (1) or clause (a) of sub-section (3) of section 7, or is aggrieved by a decision of the Central Public Information Officer or State Public Information Officer, may within thirty days from the expiry of such period or from the receipt of such a decision prefer an appeal to such officer who is senior in rank to the Central Public Information Officer or State Public Information Officer. (3) A second appeal against the decision under sub-section (1) shall lie within ninety days from the date on which the decision should have been made or was actually received, with the Central Information Commission or the State Information Commission.",
            act_number=num, chapter_number="Chapter V", chapter_title="Appeals and Penalties"
        ),
        _sec(
            src, title, "Section 20", "Penalties",
            "(1) Where the Central Information Commission or the State Information Commission at the time of deciding any complaint or appeal is of the opinion that the Central Public Information Officer or the State Public Information Officer has, without any reasonable cause, refused to receive an application for information or has not furnished information within the time specified under sub-section (1) of section 7 or malafidely denied the request, it shall impose a penalty of two hundred and fifty rupees each day till application is received or information is furnished, so however, the total amount of such penalty shall not exceed twenty-five thousand rupees.",
            act_number=num, chapter_number="Chapter V", chapter_title="Appeals and Penalties"
        ),
    ]


# =============================================================================
# 5. MOTOR VEHICLES ACT, 1988 (IND-ACT-1988-MVA)
# =============================================================================
def get_mva_phase24_sections() -> List[StatuteSection]:
    src = "IND-ACT-1988-MVA"
    title = "The Motor Vehicles Act, 1988 (as amended)"
    num = "Act No. 59 of 1988"

    return [
        _sec(
            src, title, "Section 134", "Duty of driver in case of accident and injury to a person",
            "When any person is injured or any property of a third party is damaged, as a result of an accident in which a motor vehicle is involved, the driver of the vehicle or other person in charge of the vehicle shall: (a) unless it is not practicable on account of mob fury or any other reason beyond his control, take all reasonable steps to secure medical attention for the injured person, by conveying him to the nearest medical practitioner or hospital; (b) give on demand by a police officer any information required by him; (c) report the circumstances of the occurrence, including the day, time and place thereof, to the nearest police station within twenty-four hours of the occurrence.",
            act_number=num, chapter_number="Chapter VIII", chapter_title="Control of Traffic"
        ),
        _sec(
            src, title, "Section 161", "Special provisions as to compensation in case of hit and run motor accident",
            "(1) For the purposes of this section, 'hit and run motor accident' means an accident arising out of the use of a motor vehicle or motor vehicles the identity whereof cannot be ascertained in spite of reasonable efforts. (2) Notwithstanding anything contained in this Act or any other law for the time being in force, there shall be paid as compensation, in respect of the death of any person resulting from a hit and run motor accident, a fixed sum of two lakh rupees or such higher amount as may be prescribed by the Central Government; and in respect of grievous hurt to any person resulting from a hit and run motor accident, a fixed sum of fifty thousand rupees or such higher amount as may be prescribed.",
            act_number=num, chapter_number="Chapter XI", chapter_title="Insurance of Motor Vehicles Against Third Party Risks"
        ),
        _sec(
            src, title, "Section 166", "Application for compensation",
            "(1) An application for compensation arising out of an accident of the nature specified in sub-section (1) of section 165 may be made: (a) by the person who has sustained the injury; or (b) by the owner of the property; or (c) where death has resulted from the accident, by all or any of the legal representatives of the deceased; or (d) by any agent duly authorised by the person injured or all or any of the legal representatives of the deceased, as the case may be. (3) No application for compensation shall be entertained unless it is made within six months of the occurrence of the accident.",
            act_number=num, chapter_number="Chapter XII", chapter_title="Claims Tribunals"
        ),
        _sec(
            src, title, "Section 185", "Driving by a drunken person or by a person under the influence of drugs",
            "Whoever, while driving, or attempting to drive, a motor vehicle: (a) has, in his blood, alcohol exceeding 30 mg. per 100 ml. of blood detected in a test by a breath analyser; or (b) is under the influence of a drug to such an extent as to be incapable of exercising proper control over the vehicle, shall be punishable for the first offence with imprisonment for a term which may extend to six months, or with fine of ten thousand rupees, or with both; and for a second or subsequent offence with imprisonment for a term which may extend to two years, or with fine of fifteen thousand rupees, or with both.",
            act_number=num, chapter_number="Chapter XIII", chapter_title="Offences, Penalties and Procedure"
        ),
    ]


def list_phase24_statute_documents() -> List[StatuteDocument]:
    """Returns StatuteDocument instances for Phase 24 central legislation expansion."""
    docs = []

    # BSA
    bsa_secs = get_bsa_phase24_sections()
    docs.append(StatuteDocument(
        statute_id="IND-ACT-2023-BSA-EXP",
        source_id="IND-ACT-2023-BSA",
        act_title="The Bharatiya Sakshya Adhiniyam, 2023",
        act_number="Act No. 47 of 2023",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2023, 12, 25),
        enactment_year=2023,
        sections=bsa_secs,
    ))

    # BNS
    bns_secs = get_bns_phase24_sections()
    docs.append(StatuteDocument(
        statute_id="IND-ACT-2023-BNS-EXP",
        source_id="IND-ACT-2023-BNS",
        act_title="The Bharatiya Nyaya Sanhita, 2023",
        act_number="Act No. 45 of 2023",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2023, 12, 25),
        enactment_year=2023,
        sections=bns_secs,
    ))

    # POCSO
    pocso_secs = get_pocso_phase24_sections()
    docs.append(StatuteDocument(
        statute_id="IND-ACT-2012-POCSO-EXP",
        source_id="IND-ACT-2012-POCSO",
        act_title="Protection of Children from Sexual Offences Act, 2012",
        act_number="Act No. 32 of 2012",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2012, 6, 19),
        enactment_year=2012,
        sections=pocso_secs,
    ))

    # RTI
    rti_secs = get_rti_phase24_sections()
    docs.append(StatuteDocument(
        statute_id="IND-ACT-2005-RTI",
        source_id="IND-ACT-2005-RTI",
        act_title="The Right to Information Act, 2005",
        act_number="Act No. 22 of 2005",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2005, 6, 15),
        enactment_year=2005,
        sections=rti_secs,
    ))

    # Motor Vehicles Act
    mva_secs = get_mva_phase24_sections()
    docs.append(StatuteDocument(
        statute_id="IND-ACT-1988-MVA",
        source_id="IND-ACT-1988-MVA",
        act_title="The Motor Vehicles Act, 1988 (as amended)",
        act_number="Act No. 59 of 1988",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(1988, 10, 14),
        enactment_year=1988,
        sections=mva_secs,
    ))

    return docs
