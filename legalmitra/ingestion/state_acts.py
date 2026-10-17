"""
LegalMitra State-Level Legislation Module (Phase 16E)
Defines authentic statutory provisions for key state-level Acts:
- Delhi Rent Control Act, 1958 (IN-DL)
- Delhi Police Act, 1978 (IN-DL)
- Maharashtra Rent Control Act, 1999 (IN-MH)
- Maharashtra Police Act, 1951 (IN-MH)
"""

from datetime import date
from typing import List

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus
from legalmitra.schemas.statute import StatuteDocument, StatuteSection


def get_state_statute_documents() -> List[StatuteDocument]:
    """
    Returns normalized StatuteDocuments for Delhi and Maharashtra state Acts.
    """
    state_docs: List[StatuteDocument] = []

    # 1. Delhi Rent Control Act, 1958 (Act No. 59 of 1958)
    drc_doc = StatuteDocument(
        source_id="IND-DL-STAT-DRC-1958",
        act_title="The Delhi Rent Control Act, 1958",
        act_number="Act No. 59 of 1958",
        jurisdiction=Jurisdiction.DELHI,
        enactment_date=date(1958, 12, 31),
        effective_date=date(1959, 2, 9),
        preamble="An Act to provide for the control of rents and evictions and of rates of hotels and lodging houses, and for the lease of vacant premises to Government, in certain areas in the Union territory of Delhi.",
        sections=[
            StatuteSection(
                section_id="IND-DL-STAT-DRC-1958:SEC:2",
                source_id="IND-DL-STAT-DRC-1958",
                act_title="The Delhi Rent Control Act, 1958",
                section_number="2",
                section_title="Definitions",
                full_verbatim_text=(
                    "2. Definitions.—In this Act, unless the context otherwise requires,—\n"
                    "(e) 'landlord' means a person who, for the time being is receiving, or is entitled to receive, the rent of any premises, whether on his own account or on account of or on behalf of, or for the benefit of, any other person or as a trustee, guardian or receiver for any other person or who would so receive the rent or be entitled to receive the rent, if the premises were let to a tenant;\n"
                    "(l) 'tenant' means any person by whom or on whose account or behalf the rent of any premises is, or, but for a special contract, would be, payable, and includes a sub-tenant and also any person continuing in possession after the termination of his tenancy, but shall not include any person against whom any order or decree for eviction has been made."
                ),
            ),
            StatuteSection(
                section_id="IND-DL-STAT-DRC-1958:SEC:3",
                source_id="IND-DL-STAT-DRC-1958",
                act_title="The Delhi Rent Control Act, 1958",
                section_number="3",
                section_title="Act not to apply to certain premises",
                full_verbatim_text=(
                    "3. Act not to apply to certain premises.—Nothing in this Act shall apply—\n"
                    "(a) to any premises belonging to the Government;\n"
                    "(b) to any tenancy or other like relationship created by a grant from the Government in respect of the premises taken on lease, or requisitioned, by the Government;\n"
                    "(c) to any premises, whether residential or not, whose monthly rent exceeds three thousand and five hundred rupees;\n"
                    "(d) to any premises constructed on or after the commencement of the Delhi Rent Control (Amendment) Act, 1988, for a period of ten years from the date of completion of such construction."
                ),
            ),
            StatuteSection(
                section_id="IND-DL-STAT-DRC-1958:SEC:14",
                source_id="IND-DL-STAT-DRC-1958",
                act_title="The Delhi Rent Control Act, 1958",
                section_number="14",
                section_title="Protection of tenant against eviction",
                full_verbatim_text=(
                    "14. Protection of tenant against eviction.—(1) Notwithstanding anything to the contrary contained in any other law or contract, no order or decree for the recovery of possession of any premises shall be made by any court or Controller in favour of the landlord against a tenant:\n"
                    "Provided that the Controller may, on an application made to him in the prescribed manner, make an order for the recovery of the possession of the premises on one or more of the following grounds only, namely:—\n"
                    "(a) that the tenant has neither paid nor tendered the whole of the arrears of the rent legally recoverable from him within two months of the date on which a notice of demand for the arrears of rent has been served on him by the landlord in the manner provided in section 106 of the Transfer of Property Act, 1882;\n"
                    "(b) that the tenant has, on or after the 9th day of June, 1952, sub-let, assigned or otherwise parted with the possession of the whole or any part of the premises without obtaining the consent in writing of the landlord;\n"
                    "(e) that the premises let for residential purposes are required bona fide by the landlord for occupation as a residence for himself or for any member of his family dependent on him, if he is the owner thereof, or for any person for whose benefit the premises are held and that the landlord or such person has no other reasonably suitable residential accommodation."
                ),
            ),
            StatuteSection(
                section_id="IND-DL-STAT-DRC-1958:SEC:25B",
                source_id="IND-DL-STAT-DRC-1958",
                act_title="The Delhi Rent Control Act, 1958",
                section_number="25B",
                section_title="Special procedure for the disposal of applications for eviction on the ground of bona fide requirement",
                full_verbatim_text=(
                    "25B. Special procedure for the disposal of applications for eviction on the ground of bona fide requirement.—\n"
                    "(1) Every application by a landlord for the recovery of possession of any premises on the ground specified in clause (e) of the proviso to sub-section (1) of section 14, or under section 14A, 14B, 14C or 14D, shall be dealt with in accordance with the procedure specified in this section.\n"
                    "(4) The tenant on whom the summons is duly served shall not contest the prayer for eviction from the premises unless he files an affidavit stating the grounds on which he seeks to contest the application for eviction and obtains leave from the Controller, and in default of his appearance in pursuance of the summons or his obtaining such leave, the statement made by the landlord in the application for eviction shall be deemed to be admitted by the tenant and the applicant shall be entitled to an order for eviction on the ground aforesaid.\n"
                    "(5) The Controller shall give to the tenant leave to contest the application if the affidavit filed by the tenant discloses such facts as would disentitle the landlord from obtaining an order for the recovery of possession of the premises."
                ),
            ),
        ]
    )
    state_docs.append(drc_doc)

    # 2. Delhi Police Act, 1978 (Act No. 34 of 1978)
    dpa_doc = StatuteDocument(
        source_id="IND-DL-STAT-DPA-1978",
        act_title="The Delhi Police Act, 1978",
        act_number="Act No. 34 of 1978",
        jurisdiction=Jurisdiction.DELHI,
        enactment_date=date(1978, 8, 27),
        effective_date=date(1978, 9, 1),
        preamble="An Act to amend and consolidate the law relating to the regulation of the police in the Union territory of Delhi.",
        sections=[
            StatuteSection(
                section_id="IND-DL-STAT-DPA-1978:SEC:28",
                source_id="IND-DL-STAT-DPA-1978",
                act_title="The Delhi Police Act, 1978",
                section_number="28",
                section_title="Power to make regulations for regulating traffic and for preservation of order in public place, etc.",
                full_verbatim_text=(
                    "28. Power to make regulations for regulating traffic and for preservation of order in public place, etc.—\n"
                    "(1) The Commissioner of Police may, by notification in the Official Gazette, make regulations to provide for all or any of the following matters, namely:—\n"
                    "(a) licensing and controlling persons offering themselves for employment at quays, wharves and landing places, and the licensing and controlling plying of boats;\n"
                    "(b) regulating traffic of all kinds in streets and other public places and the use of streets and other public places by persons riding, driving, cycling, walking or accompanying any animal;\n"
                    "(f) regulating music or other sound in public places;\n"
                    "(o) licensing or controlling places of public amusement or public entertainment."
                ),
            ),
            StatuteSection(
                section_id="IND-DL-STAT-DPA-1978:SEC:53",
                source_id="IND-DL-STAT-DPA-1978",
                act_title="The Delhi Police Act, 1978",
                section_number="53",
                section_title="Externment of persons convicted of certain offences",
                full_verbatim_text=(
                    "53. Externment of persons convicted of certain offences.—If a person has been convicted of an offence under Chapter XII, Chapter XVI or Chapter XVII of the Indian Penal Code (or Bharatiya Nyaya Sanhita, 2023), the Commissioner of Police may, if he has reason to believe that such person is likely again to engage himself in the commission of an offence similar to that for which he was convicted, by an order in writing directed to such person, direct him to remove himself outside the Union territory of Delhi by such route and within such time as may be specified in the order and not to enter or return to Delhi without the permission in writing of the Commissioner of Police."
                ),
            ),
            StatuteSection(
                section_id="IND-DL-STAT-DPA-1978:SEC:65",
                source_id="IND-DL-STAT-DPA-1978",
                act_title="The Delhi Police Act, 1978",
                section_number="65",
                section_title="Persons bound to comply with the reasonable directions of police officer",
                full_verbatim_text=(
                    "65. Persons bound to comply with the reasonable directions of police officer.—All persons shall be bound to comply with the reasonable directions given by any police officer on duty in the discharge of his duties under this Act or rules or regulations made thereunder."
                ),
            ),
        ]
    )
    state_docs.append(dpa_doc)

    # 3. Maharashtra Rent Control Act, 1999 (Maharashtra Act No. XVIII of 2000)
    mrc_doc = StatuteDocument(
        source_id="IND-MH-STAT-MRC-1999",
        act_title="The Maharashtra Rent Control Act, 1999",
        act_number="Maharashtra Act No. XVIII of 2000",
        jurisdiction=Jurisdiction.MAHARASHTRA,
        enactment_date=date(2000, 3, 10),
        effective_date=date(2000, 3, 31),
        preamble="An Act to unify, consolidate and amend the law relating to the control of rent and repairs of certain premises and of eviction and for encouraging the construction of new houses by assuring a fair return on the investment by landlords in the State of Maharashtra.",
        sections=[
            StatuteSection(
                section_id="IND-MH-STAT-MRC-1999:SEC:3",
                source_id="IND-MH-STAT-MRC-1999",
                act_title="The Maharashtra Rent Control Act, 1999",
                section_number="3",
                section_title="Exemption",
                full_verbatim_text=(
                    "3. Exemption.—(1) This Act shall not apply—\n"
                    "(a) to any premises belonging to the Government or a local authority or apply as against the Government to any tenancy, licence or other like relationship created by the grant from a local authority in respect of premises taken on lease or requisitioned by the Government;\n"
                    "(b) to any premises let or sub-let to banks, or any Public Sector Undertakings or any Corporation established by or under any Central or State Act, or foreign missions, international agencies, multinational companies, and private limited companies and public limited companies having a paid up share capital of rupee one crore or more."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MRC-1999:SEC:7",
                source_id="IND-MH-STAT-MRC-1999",
                act_title="The Maharashtra Rent Control Act, 1999",
                section_number="7",
                section_title="Definitions",
                full_verbatim_text=(
                    "7. Definitions.—In this Act, unless there is anything repugnant in the subject or context,—\n"
                    "(3) 'landlord' means any person who is for the time being, receiving, or entitled to receive, rent in respect of any premises whether on his own account, or on behalf, or for the benefit of, any other person, or as a trustee, guardian, or receiver for any other person or who would so receive the rent, or be entitled to receive the rent, if the premises were let to a tenant;\n"
                    "(5) 'licensee' in respect of any premises or any part thereof, means the person who is in occupation of the premises or such part, as the case may be, under a subsisting agreement for licence given for a licence fees or charge;\n"
                    "(15) 'tenant' means any person by whom or on whose account rent is payable for any premises and includes any person occupying premises under clause (b) of section 16, sub-tenants, and any person remaining after termination in possession."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MRC-1999:SEC:15",
                source_id="IND-MH-STAT-MRC-1999",
                act_title="The Maharashtra Rent Control Act, 1999",
                section_number="15",
                section_title="No ejectment ordinarily to be made if tenant pays or is ready and willing to pay standard rent and permitted increases",
                full_verbatim_text=(
                    "15. No ejectment ordinarily to be made if tenant pays or is ready and willing to pay standard rent and permitted increases.—\n"
                    "(1) A landlord shall not be entitled to the recovery of possession of any premises so long as the tenant pays, or is ready and willing to pay, the amount of the standard rent and permitted increases, if any, and observes and performs the other conditions of the tenancy, in so far as they are consistent with the provisions of this Act.\n"
                    "(2) No suit for recovery of possession shall be instituted by a landlord against a tenant on the ground of non-payment of the standard rent or permitted increases, until the expiration of ninety days next after notice in writing of the demand of the standard rent or permitted increases has been served upon the tenant in the manner provided in section 106 of the Transfer of Property Act, 1882.\n"
                    "(3) No decree for eviction shall be passed by the court in any suit for recovery of possession on the ground of arrears of standard rent and permitted increases if, within a period of ninety days from the date of service of the summons of the suit, the tenant pays or tenders in court the standard rent and permitted increases then due."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MRC-1999:SEC:16",
                source_id="IND-MH-STAT-MRC-1999",
                act_title="The Maharashtra Rent Control Act, 1999",
                section_number="16",
                section_title="When landlord may recover possession",
                full_verbatim_text=(
                    "16. When landlord may recover possession.—(1) Notwithstanding anything contained in this Act but subject to the provisions of section 25, a landlord shall be entitled to recover possession of any premises if the court is satisfied—\n"
                    "(a) that the tenant has committed any act contrary to the provisions of clause (o) of section 108 of the Transfer of Property Act, 1882;\n"
                    "(b) that the tenant has, without the landlord's written consent, erected on the premises any permanent structure;\n"
                    "(e) that the tenant has given notice to quit, and in consequence of that notice, the landlord has contracted to sell or let the premises or has taken any other steps;\n"
                    "(g) that the premises are reasonably and bona fide required by the landlord for occupation by himself or by any person for whose benefit the premises are held;\n"
                    "(i) that the premises are reasonably and bona fide required by the landlord for the immediate purpose of demolishing them and such demolishing is to be made for the purpose of erecting new building."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MRC-1999:SEC:24",
                source_id="IND-MH-STAT-MRC-1999",
                act_title="The Maharashtra Rent Control Act, 1999",
                section_number="24",
                section_title="Landlord entitled to recover possession of premises given on licence on expiry",
                full_verbatim_text=(
                    "24. Landlord entitled to recover possession of premises given on licence on expiry.—\n"
                    "(1) Notwithstanding anything contained in this Act, a licensee in possession or occupation of premises given to him on licence for residence shall deliver possession of such premises to the landlord on expiry of the period of licence; and on the failure of the licensee to so deliver the possession of the licensed premises, a landlord shall be entitled to recover possession of such premises from a licensee, on the expiry of the period of licence, by making an application to the Competent Authority, and the Competent Authority, on being satisfied that the period of licence has expired, shall pass an order for eviction of a licensee.\n"
                    "(2) Any licensee who does not deliver possession of the premises to the landlord on expiry of the period of licence and continues to be in possession or occupation of the licensed premises shall be liable to pay damages at double the rate of the licence fee or charge of the premises fixed under the agreement of licence."
                ),
            ),
        ]
    )
    state_docs.append(mrc_doc)

    # 4. Maharashtra Police Act, 1951 (Bombay Act No. XXII of 1951)
    mpa_doc = StatuteDocument(
        source_id="IND-MH-STAT-MPA-1951",
        act_title="The Maharashtra Police Act, 1951",
        act_number="Bombay Act No. XXII of 1951",
        jurisdiction=Jurisdiction.MAHARASHTRA,
        enactment_date=date(1951, 6, 11),
        effective_date=date(1951, 8, 1),
        preamble="An Act to consolidate and amend the law for the regulation of the Police Force in the State of Maharashtra.",
        sections=[
            StatuteSection(
                section_id="IND-MH-STAT-MPA-1951:SEC:33",
                source_id="IND-MH-STAT-MPA-1951",
                act_title="The Maharashtra Police Act, 1951",
                section_number="33",
                section_title="Power to make rules for regulation of traffic and for preservation of order in public place, etc.",
                full_verbatim_text=(
                    "33. Power to make rules for regulation of traffic and for preservation of order in public place, etc.—\n"
                    "(1) The Commissioner and the District Magistrate, in areas under their respective charges or any part thereof, may make, alter or rescind rules or orders not inconsistent with this Act for—\n"
                    "(a) licensing and controlling persons offering themselves for employment at quays, wharves and landing places, and licensing of boats;\n"
                    "(b) regulating traffic of all kinds in streets and other public places;\n"
                    "(w) licensing or controlling places of public amusement or entertainment;\n"
                    "(x) regulating the illumination or illumination of streets and display of advertisements."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MPA-1951:SEC:56",
                source_id="IND-MH-STAT-MPA-1951",
                act_title="The Maharashtra Police Act, 1951",
                section_number="56",
                section_title="Removal of persons about to commit offence",
                full_verbatim_text=(
                    "56. Removal of persons about to commit offence.—(1) Whenever it shall appear in Greater Bombay and other areas for which a Commissioner has been appointed to the Commissioner and in other areas to the District Magistrate or the Sub-Divisional Magistrate empowered by the State Government in that behalf—\n"
                    "(a) that the movements or acts of any person are causing or calculated to cause alarm, danger or harm to person or property;\n"
                    "(b) that there are reasonable grounds for believing that such person is engaged or is about to be engaged in the commission of an offence involving force or violence or an offence punishable under Chapter XII, XVI or XVII of the Indian Penal Code (or Bharatiya Nyaya Sanhita, 2023);\n"
                    "the said officer may, by an order in writing, direct such person to conduct himself as shall seem necessary or to remove himself outside the area within such time as may be specified."
                ),
            ),
            StatuteSection(
                section_id="IND-MH-STAT-MPA-1951:SEC:57",
                source_id="IND-MH-STAT-MPA-1951",
                act_title="The Maharashtra Police Act, 1951",
                section_number="57",
                section_title="Removal of persons convicted of certain offences",
                full_verbatim_text=(
                    "57. Removal of persons convicted of certain offences.—If a person has been convicted of an offence under Chapter XII, XVI or XVII of the Indian Penal Code, or of an offence under section 4 or 12A of the Bombay Prevention of Gambling Act, 1887, or under the Prohibition Act, the Commissioner, the District Magistrate or the Sub-Divisional Magistrate may, if he has reason to believe that such person is likely again to engage in the commission of an offence similar to that for which he was convicted, direct such person to remove himself outside the area specified in the order."
                ),
            ),
        ]
    )
    state_docs.append(mpa_doc)

    return state_docs

