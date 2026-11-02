"""Citizen Legal Guidance & Intent Resolution Engine (Phase 83).

Provides human-accessible, plain-English legal explanations, step-by-step
actionable remedies, emergency helplines, evidence collection checklists,
and statutory transitions (BNS/BNSS/BSA) for everyday Indian citizens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class CitizenLegalGuidance:
    """Structured guidance for a common citizen legal situation."""
    scenario_id: str
    category: str
    direct_answer: str
    step_by_step_actions: List[str]
    evidence_to_preserve: List[str]
    helplines: List[str]
    governing_statutes: List[str]
    legal_provisions_summary: str
    keywords: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Comprehensive Citizen Knowledge Base (Q1 to Q25)
# ---------------------------------------------------------------------------
CITIZEN_KNOWLEDGE_BASE: List[CitizenLegalGuidance] = [
    # 1. Police, FIR and Basic Rights
    CitizenLegalGuidance(
        scenario_id="Q1_FIR_REFUSAL",
        category="Police, FIR & Criminal Procedure",
        direct_answer=(
            "If the police refuse to record information about a cognizable offence, "
            "you have statutory remedies under Indian law to compel registration."
        ),
        step_by_step_actions=[
            "Send your complaint in writing by registered post or speed post to the Superintendent of Police (SP) or Deputy Commissioner of Police (DCP) under Section 173(4) of the Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023.",
            "If the SP/DCP fails to direct an investigation, approach the Judicial Magistrate under Section 175(3) BNSS with an application seeking directions to the police to register the FIR and investigate.",
            "Keep signed copies of your written complaint and postal acknowledgment/speed post tracking receipts as proof of submission.",
            "If you are facing immediate threats or danger, call the Emergency Helpline at 112 immediately."
        ],
        evidence_to_preserve=["Written complaint copy", "Postal/speed post tracking receipts", "Police station visit details (date, time, officer name)"],
        helplines=["112 (National Emergency Helpline)"],
        governing_statutes=["The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173(4))", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 175(3))"],
        legal_provisions_summary=(
            "Section 173(4) BNSS empowers the Superintendent of Police to investigate or direct investigation if a station house officer refuses to register an FIR. "
            "Section 175(3) BNSS empowers the Magistrate to order registration of FIR upon examining the applicant."
        ),
        keywords=["refusing to register", "refuse to register fir", "fir nahi likh rahe", "police not taking fir", "police refused fir", "fir refusal"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q2_ARREST_GROUNDS",
        category="Constitutional Rights & Arrest",
        direct_answer=(
            "No. The police cannot arrest you without communicating the full particulars and reasons for your arrest."
        ),
        step_by_step_actions=[
            "Ask the arresting officer clearly for the specific grounds of arrest and whether the alleged offence is bailable or non-bailable.",
            "Under Article 22(1) of the Constitution and Section 47 BNSS, you have the fundamental right to be informed of the grounds of arrest immediately.",
            "Request that your family member or nominated friend be notified of your arrest and custody location under Section 48 BNSS.",
            "Demand access to consult and be defended by a legal practitioner (lawyer) of your choice.",
            "Do not physically resist lawful police action, but verify that an arrest memo is prepared and signed with the time and date of arrest."
        ],
        evidence_to_preserve=["Arrest memo copy", "Identity/badge details of arresting officer", "Names of witnesses present at arrest"],
        helplines=["112 (Police Emergency)", "15100 (NALSA Free Legal Aid)"],
        governing_statutes=["Constitution of India (Article 22(1))", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 47)", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 48)"],
        legal_provisions_summary=(
            "Article 22(1) of the Constitution guarantees the right to be informed of grounds of arrest. "
            "Section 47 BNSS (erstwhile Section 50 CrPC) makes it mandatory for the officer arresting any person without warrant to forthwith communicate full particulars of the offence and grounds of arrest."
        ),
        keywords=["arrest me without telling", "arrest bina bataye", "grounds of arrest", "can police arrest without reason", "police arrest rights"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q3_CRIMINAL_INTIMIDATION",
        category="Preventive Law & Intimidation",
        direct_answer=(
            "Yes. You can report credible threats to the police even if no physical assault has occurred yet."
        ),
        step_by_step_actions=[
            "File a complaint for criminal intimidation at your local police station.",
            "Depending on the severity, Section 351 of the Bharatiya Nyaya Sanhita (BNS), 2023 applies to anyone who threatens another with injury to their person, reputation, or property.",
            "If the threats are continuous or immediate, request the police to register a Non-Cognizable Report (NCR) or FIR, or seek preventive action under Chapter VIII BNSS.",
            "Preserve any threatening audio recordings, SMS/WhatsApp messages, CCTV footage, or eyewitness statements.",
            "If there is immediate danger to your physical safety, call 112 without delay."
        ],
        evidence_to_preserve=["WhatsApp/SMS messages", "Call recordings lawfully obtained", "CCTV footage", "Eyewitness details"],
        helplines=["112 (National Emergency Helpline)"],
        governing_statutes=["The Bharatiya Nyaya Sanhita, 2023 (Section 351)"],
        legal_provisions_summary=(
            "Section 351 BNS (erstwhile Section 503 & 506 IPC) defines and punishes criminal intimidation. "
            "Threatening injury to cause alarm or force someone to act against their will is a punishable offence."
        ),
        keywords=["neighbour threatening", "threat to beat", "dhamki de raha hai", "threatening to beat me", "threaten without hitting", "criminal intimidation"]
    ),

    # 2. Cybercrime and Online Fraud
    CitizenLegalGuidance(
        scenario_id="Q4_CYBER_BANK_FRAUD",
        category="Cybercrime & Financial Fraud",
        direct_answer=(
            "Act immediately within the 'golden hour' to maximize the chances of freezing and recovering your stolen funds."
        ),
        step_by_step_actions=[
            "Call 1930 immediately—India's National Cyber Financial Fraud Helpline—to report the fraudulent transaction and request a temporary hold/freeze on the recipient's bank account or digital wallet.",
            "Lodge an online complaint at the National Cyber Crime Reporting Portal: https://cybercrime.gov.in.",
            "Contact your bank's 24/7 fraud reporting helpline immediately, block your debit/credit card, freeze netbanking credentials, and register an official disputed transaction grievance.",
            "Preserve the transaction UTR/reference number, bank debit SMS, fake caller's phone number, call logs, and screenshots.",
            "Prompt reporting within hours greatly increases the likelihood of inter-bank freezing, though full recovery depends on whether funds have already been withdrawn."
        ],
        evidence_to_preserve=["Bank debit SMS", "Transaction reference/UTR number", "Call logs of fraudulent caller", "Bank account statement"],
        helplines=["1930 (National Cyber Financial Fraud Helpline)", "cybercrime.gov.in (Online Cybercrime Portal)"],
        governing_statutes=["Information Technology Act, 2000 (Section 66D)", "The Bharatiya Nyaya Sanhita, 2023 (Section 318)"],
        legal_provisions_summary=(
            "Section 66D IT Act punishes cheating by personation using computer resources. "
            "Section 318 BNS (erstwhile Section 420 IPC) penalizes cheating and dishonestly inducing delivery of property."
        ),
        keywords=["pretending to be bank", "stole money from account", "bank employee fraud", "1930", "paise kat gaye", "cyber fraud account"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q5_FAKE_SOCIAL_PROFILE",
        category="Digital Identity & Cyber Harassment",
        direct_answer=(
            "Yes. Creating a fake profile using another person's photographs and name is illegal and actionable under cyber and criminal laws."
        ),
        step_by_step_actions=[
            "Report the fake account directly within the social media platform (Instagram/Facebook/X) for impersonation.",
            "Take screenshots of the profile URL, username, bio, uploaded photos, and any direct messages or interactions.",
            "File an official cybercrime report on https://cybercrime.gov.in under the category 'Cyber Crime against Women and Children' or 'Other Cyber Crimes'.",
            "Such conduct attracts Section 66C (identity theft) and Section 66D (cheating by personation) of the Information Technology Act, 2000, as well as provisions of the Bharatiya Nyaya Sanhita (BNS) for defamation and criminal intimidation where applicable.",
            "If the account is soliciting money or involved in financial extortion, call 1930."
        ],
        evidence_to_preserve=["Fake profile URL", "Screenshots of fake profile & photos", "Original unedited photos proving ownership", "Screenshots of chats/messages"],
        helplines=["cybercrime.gov.in (Cybercrime Reporting Portal)", "1930 (if financial fraud)"],
        governing_statutes=["Information Technology Act, 2000 (Section 66C)", "Information Technology Act, 2000 (Section 66D)", "The Bharatiya Nyaya Sanhita, 2023 (Section 356)"],
        legal_provisions_summary=(
            "Section 66C IT Act penalizes identity theft using unique identification features. "
            "Section 66D IT Act penalizes cheating by personation over computer systems."
        ),
        keywords=["fake instagram", "fake account", "using my photos", "impersonation instagram", "fake profile photo"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q6_OTP_SHARING_LIABILITY",
        category="Banking Safety & Financial Liability",
        direct_answer=(
            "No. No person has legal permission to withdraw or steal money from your account simply because you shared an OTP."
        ),
        step_by_step_actions=[
            "Immediately contact your bank's fraud line to block all linked debit cards, UPI IDs, and internet banking access.",
            "Report the unauthorized debit transaction to the bank in writing within 3 working days.",
            "Under RBI's Circular on Customer Liability in Unauthorized Electronic Banking Transactions, customer liability depends on whether the fraud was due to bank negligence, third-party breach, or customer negligence (like OTP sharing), and how quickly you notified the bank.",
            "Call 1930 and file a complaint on cybercrime.gov.in to initiate inter-bank recovery.",
            "Change all net banking passwords, UPI PINs, and linked email account passwords immediately."
        ],
        evidence_to_preserve=["SMS containing OTP and subsequent debit SMS", "Call logs with timestamp", "Bank formal complaint acknowledgement"],
        helplines=["1930 (Cyber Fraud Helpline)", "Bank 24x7 Customer Care"],
        governing_statutes=["RBI Master Direction on Customer Protection – Limiting Liability in Unauthorised Electronic Banking Transactions (2017)", "Information Technology Act, 2000 (Section 66D)"],
        legal_provisions_summary=(
            "RBI guidelines specify that zero liability applies if fraud occurs without customer contribution, but customer negligence like sharing credentials requires immediate notification to limit liability."
        ),
        keywords=["shared an otp", "shared otp accidentally", "can they take money otp", "otp share ho gaya", "otp shared liability"]
    ),

    # 3. Consumer Rights and Shopping
    CitizenLegalGuidance(
        scenario_id="Q7_DEFECTIVE_PRODUCT_SHOP",
        category="Consumer Protection & Product Liability",
        direct_answer=(
            "You have statutory remedies under the Consumer Protection Act, 2019 against the seller and manufacturer for selling a defective good."
        ),
        step_by_step_actions=[
            "Issue a formal written notice/email to both the shopkeeper and the manufacturer detailing the defect and demanding replacement or refund within 15 days.",
            "Preserve your original purchase invoice/bill, warranty card, product box, photos/videos of the defect, and any job sheets from authorized service centres.",
            "Lodge a grievance with the National Consumer Helpline by calling 1915 or online at https://consumerhelpline.gov.in.",
            "If the grievance remains unresolved, file a consumer complaint before the District Consumer Disputes Redressal Commission (DCDRC) via the e-Daakhil portal (https://edaakhil.nic.in)."
        ],
        evidence_to_preserve=["Original retail tax invoice", "Warranty card", "Photographs/video of defect", "Service centre job card or written refusal"],
        helplines=["1915 (National Consumer Helpline)", "consumerhelpline.gov.in", "edaakhil.nic.in"],
        governing_statutes=["Consumer Protection Act, 2019 (Section 2(10) Defect)", "Consumer Protection Act, 2019 (Section 35)"],
        legal_provisions_summary=(
            "Section 2(10) Consumer Protection Act, 2019 defines defect as any fault, imperfection or shortcoming in quality, quantity, potency or standard. "
            "Consumers can claim replacement, refund, and compensation for deficiency in service and unfair trade practice."
        ),
        keywords=["bought a new phone", "stopped working after five days", "shopkeeper refuses to replace", "defective phone", "consumer replacement"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q8_ECOMMERCE_NONDELIVERY",
        category="E-Commerce Consumer Dispute",
        direct_answer=(
            "Failing to deliver goods after accepting advance payment constitutes deficiency of service and unfair trade practice, and may also amount to cheating if done dishonestly."
        ),
        step_by_step_actions=[
            "Save the order confirmation email, payment transaction receipt/UTR, tracking link, and all customer support ticket communications.",
            "Raise an official grievance on the National Consumer Helpline at 1915 or through consumerhelpline.gov.in.",
            "Contact your credit card issuer or payment gateway (UPI/bank) to raise a chargeback or payment dispute for non-delivery of service.",
            "If there is evidence of an intentional fraudulent website created solely to deceive buyers without any intention to deliver, lodge a complaint on https://cybercrime.gov.in or report to 1930.",
            "If unresolved, file an e-complaint against the e-commerce entity on e-Daakhil."
        ],
        evidence_to_preserve=["Order confirmation receipt", "Bank debit statement", "Screenshots of order status showing non-delivery", "Email correspondence with support"],
        helplines=["1915 (National Consumer Helpline)", "1930 (if fake fraudulent website)"],
        governing_statutes=["Consumer Protection (E-Commerce) Rules, 2020", "Consumer Protection Act, 2019", "The Bharatiya Nyaya Sanhita, 2023 (Section 318)"],
        legal_provisions_summary=(
            "Under the Consumer Protection (E-Commerce) Rules, 2020, e-commerce entities must provide an explicit grievance redressal mechanism and refund within statutory timelines upon non-delivery."
        ),
        keywords=["online shopping took money", "never delivered product", "online order not delivered", "paise kat gaye saman nahi aaya", "ecommerce fraud delivery"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q9_MENU_OVERCHARGING",
        category="Consumer Rights & Pricing",
        direct_answer=(
            "No. A restaurant cannot charge more than the price explicitly printed on its menu, other than applicable statutory taxes (GST) and properly disclosed charges."
        ),
        step_by_step_actions=[
            "Examine the itemized bill and compare each item against the printed menu price.",
            "Point out the discrepancy to the restaurant management and insist on paying only the printed menu price plus applicable taxes.",
            "Under the Consumer Protection Act, 2019, charging more than the displayed price constitutes an unfair trade practice under Section 2(47).",
            "Take a photograph of the menu page showing the price and preserve the paid bill copy.",
            "If the restaurant refuses to rectify the bill, lodge a complaint with the National Consumer Helpline by dialing 1915 or SMS/WhatsApp via consumerhelpline.gov.in."
        ],
        evidence_to_preserve=["Photograph of printed menu with price", "Final itemized restaurant invoice/bill", "Payment proof"],
        helplines=["1915 (National Consumer Helpline)"],
        governing_statutes=["Consumer Protection Act, 2019 (Section 2(47) Unfair Trade Practice)"],
        legal_provisions_summary=(
            "Section 2(47) Consumer Protection Act, 2019 prohibits unfair trade practices, including deceptive pricing and charging above the agreed or displayed price."
        ),
        keywords=["charged more than menu", "restaurant charged more", "menu price overcharging", "extra charge restaurant", "menu se zyada paise"]
    ),

    # 4. Family, Marriage and Women's Rights
    CitizenLegalGuidance(
        scenario_id="Q10_WIFE_MAINTENANCE",
        category="Family Law & Women's Rights",
        direct_answer=(
            "Yes. A husband has a legal obligation to maintain his wife, and Indian law provides multiple statutory avenues for maintenance and protection."
        ),
        step_by_step_actions=[
            "File an application for maintenance under Section 144 of the Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 (erstwhile Section 125 CrPC) before the Family Court or Judicial Magistrate.",
            "Under the Protection of Women from Domestic Violence Act, 2005 (PWDVA), financial deprivation (economic abuse) is a recognized form of domestic violence. You can seek monetary relief (Section 20), residence orders (Section 19), and interim maintenance.",
            "You can approach the local Protection Officer (appointed in every district), a registered Service Provider, or a Magistrate directly.",
            "If you cannot afford legal fees, you are entitled to completely free legal assistance from the District Legal Services Authority (DLSA).",
            "Call the Women Helpline at 181 or 112 if you are facing harassment, confinement, or physical danger."
        ],
        evidence_to_preserve=["Marriage certificate or wedding photos", "Household expenditure records", "Husband's income proof / bank details if available", "Rental/residence proof"],
        helplines=["181 (Women Helpline)", "15100 (Free Legal Aid - NALSA)", "112 (Emergency)"],
        governing_statutes=["The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 144)", "Protection of Women from Domestic Violence Act, 2005 (Sections 12, 19, 20)"],
        legal_provisions_summary=(
            "Section 144 BNSS provides for maintenance of wives, children, and parents unable to maintain themselves. "
            "The Domestic Violence Act 2005 covers economic abuse and provides immediate interim maintenance and right of residence."
        ),
        keywords=["husband not giving money", "household expenses wife", "pati kharcha nahi deta", "maintenance rights wife", "husband refuses expenses"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q11_FORCED_MARRIAGE",
        category="Fundamental Rights & Personal Autonomy",
        direct_answer=(
            "Yes. An adult citizen has the absolute constitutional right to decide whether, when, and whom to marry. Forced marriage is illegal."
        ),
        step_by_step_actions=[
            "As an adult (18 years or older for women, 21 for men), your free and voluntary consent is an indispensable legal requirement for a valid marriage under all Indian marriage laws.",
            "Neither parents nor family members have any legal authority to compel or coerce you into marriage against your will.",
            "If you face confinement, physical violence, or threats, call the Emergency Helpline at 112 or Women Helpline at 181 immediately.",
            "You can seek judicial protection by approaching the High Court or Sessions Court for a protection order against family interference.",
            "Free legal counsel and shelter support can be obtained through the District Legal Services Authority (DLSA)."
        ],
        evidence_to_preserve=["Threat messages or audio recordings", "Identity proof showing adult age (Aadhaar/10th Marksheet/Voter ID)"],
        helplines=["112 (National Emergency Helpline)", "181 (Women Helpline)", "15100 (NALSA Legal Aid)"],
        governing_statutes=["Constitution of India (Article 21 - Right to Life & Personal Liberty)", "Special Marriage Act, 1954 (Section 4)", "Hindu Marriage Act, 1955 (Section 5)"],
        legal_provisions_summary=(
            "The Supreme Court in Shafin Jahan v. Asokan K.M. (2018) and Shakti Vahini v. Union of India (2018) held that the right to marry a person of one's choice is an integral aspect of Article 21. Forced consent renders marriage voidable."
        ),
        keywords=["parents forcing to marry", "forced marriage", "shaadi ke liye dabav", "parents forcing marriage legal", "can i refuse marriage"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q12_STALKING_HARASSMENT",
        category="Women's Safety & Criminal Law",
        direct_answer=(
            "Yes. Repeatedly sending unwanted romantic or personal messages after you have clearly indicated disinterest constitutes the criminal offence of stalking."
        ),
        step_by_step_actions=[
            "Clearly and in writing tell the sender once: 'I am not interested. Do not contact me again.'",
            "Under Section 78 of the Bharatiya Nyaya Sanhita (BNS), 2023, monitoring a woman's internet/email/messaging usage or attempting contact despite clear disinterest is punishable stalking.",
            "Do not delete the messages. Take complete screenshots showing phone numbers, handles, timestamps, and message contents.",
            "File a complaint at the nearest police station (or Women Police Station), or submit an online complaint on https://cybercrime.gov.in.",
            "If you face any intimidation or fear of physical harm, dial 112 or 181 immediately."
        ],
        evidence_to_preserve=["Screenshots of all messages and profiles", "Call records and timestamps", "Screenshot of your message clearly saying 'no'"],
        helplines=["112 (Emergency)", "181 (Women Helpline)", "cybercrime.gov.in"],
        governing_statutes=["The Bharatiya Nyaya Sanhita, 2023 (Section 78)", "Information Technology Act, 2000 (Section 67)"],
        legal_provisions_summary=(
            "Section 78 BNS (erstwhile Section 354D IPC) makes stalking a cognizable offence. A first conviction carries imprisonment up to 3 years and a fine."
        ),
        keywords=["romantic messages unwanted", "harassment messages after no", "stalking bns", "unwanted messages harassment", "baar baar message kar raha"]
    ),

    # 5. Employment, Salary and Education
    CitizenLegalGuidance(
        scenario_id="Q13_UNPAID_SALARY",
        category="Labour Law & Employment Rights",
        direct_answer=(
            "You have the legal right to demand and receive payment of earned wages for work performed."
        ),
        step_by_step_actions=[
            "Send a formal written demand email or letter to the employer/HR specifying the outstanding salary amount and giving a 7 to 15-day deadline to disburse the funds.",
            "Gather and preserve your appointment letter/contract, monthly salary slips, attendance records, office emails, and bank account statements.",
            "If unpaid, you can file a complaint before the jurisdictional Labour Commissioner or Authority under the Payment of Wages Act, 1936 or state Shops and Establishments Act.",
            "You can also serve a statutory Legal Notice through an advocate demanding immediate settlement along with interest.",
            "For corporate entities, non-payment of legitimate dues can also be pursued through civil recovery suits or summary suits under Order XXXVII CPC."
        ],
        evidence_to_preserve=["Appointment letter / employment contract", "Attendance logs / login hours", "Previous salary slips", "Bank statements showing non-credit"],
        helplines=["Labour Commissioner Office (Jurisdictional)", "15100 (Legal Aid)"],
        governing_statutes=["Payment of Wages Act, 1936 (Section 15)", "State Shops and Establishments Acts"],
        legal_provisions_summary=(
            "Section 15 Payment of Wages Act provides a summary mechanism before the Authority to direct payment of delayed wages along with compensation."
        ),
        keywords=["not paying my salary", "salary unpaid two months", "salary nahi mil rahi", "employer not paying", "unpaid salary remedy"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q14_COLLEGE_CERTIFICATE_WITHHELD",
        category="Education Rights & Student Protection",
        direct_answer=(
            "No. Educational institutions are prohibited from withholding original academic certificates and marksheets."
        ),
        step_by_step_actions=[
            "University Grants Commission (UGC) regulations and Ministry of Education mandates explicitly bar colleges from retaining original certificates of students.",
            "Original certificates belong to the student and cannot be held as ransom or lien to enforce disputed fee payments or other institutional claims.",
            "Submit a formal written representation to the Principal/Registrar demanding return within 7 days, citing UGC guidelines.",
            "If the college refuses, lodge a complaint with the affiliating University's Grievance Redressal Cell and the UGC e-Samadhan portal (https://samadhan.ugc.ac.in).",
            "In case of persistent refusal, you can approach the High Court under Article 226 for a writ of mandamus directing immediate release of your original documents."
        ],
        evidence_to_preserve=["Fee clearance receipts / no-dues receipts", "Acknowledgment of submission of original certificates", "Written letters sent to college administration"],
        helplines=["samadhan.ugc.ac.in (UGC Grievance Portal)"],
        governing_statutes=["UGC Notification on Refund of Fees and Non-Retention of Original Certificates", "Constitution of India (Article 226)"],
        legal_provisions_summary=(
            "UGC mandate strictly prohibits institutions from retaining original personal or academic certificates (like migration, marksheets) under any circumstances."
        ),
        keywords=["college refusing to return certificates", "withholding original certificates", "college marksheet nahi de raha", "certificates withheld by college"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q15_SUDDEN_TERMINATION",
        category="Employment & Labour Law",
        direct_answer=(
            "Possibly, depending on your employment agreement, classification, and length of service. Sudden termination without notice is often subject to contractual or statutory challenge."
        ),
        step_by_step_actions=[
            "Review your employment contract/appointment letter for the 'Termination' clause, which typically specifies mandatory notice period (e.g., 30 to 90 days) or salary in lieu of notice.",
            "If terminated without notice or cause, you are generally entitled to notice pay and accrued encashable benefits.",
            "For workmen under the Industrial Disputes Act, 1947, retrenchment without statutory notice and retrenchment compensation is illegal.",
            "Preserve your appointment letter, termination email/letter, salary slips, and appraisal records.",
            "Send a written representation requesting contractual notice pay, and consult an employment lawyer or labour officer before signing any settlement or full-and-final release."
        ],
        evidence_to_preserve=["Appointment letter", "Termination letter/email", "Full and final settlement statement", "Attendance and performance records"],
        helplines=["Jurisdictional Labour Department", "15100 (Legal Aid)"],
        governing_statutes=["Industrial Disputes Act, 1947 (Section 25F)", "State Shops and Establishments Act"],
        legal_provisions_summary=(
            "Section 25F Industrial Disputes Act mandates 1 month notice in writing and retrenchment compensation for eligible workmen. Contractual employees can enforce notice pay under the contract."
        ),
        keywords=["fired without notice", "terminated without notice", "bina notice nikala", "employer fired no notice", "sudden job termination"]
    ),

    # 6. Property, Rent and Neighbourhood Disputes
    CitizenLegalGuidance(
        scenario_id="Q16_ILLEGAL_EVICTION",
        category="Tenancy & Property Rights",
        direct_answer=(
            "No. A landlord cannot forcibly throw you out overnight, change locks, or throw away your belongings without following due legal process."
        ),
        step_by_step_actions=[
            "Under Indian tenancy laws, a tenant cannot be evicted without due process of law, which requires a formal written notice to vacate and an eviction order from a competent Rent Controller or Civil Court.",
            "Landlords are strictly prohibited from disconnecting essential services like electricity or water to force eviction.",
            "Keep copies of your registered rent agreement, rent payment receipts, bank transfer records, and landlord communications on your phone and accessible.",
            "If the landlord attempts physical force, trespassing, or lockout, call the Police at 112 immediately and report criminal trespass under Section 329 BNS.",
            "You can approach the local Civil Court or Rent Authority to obtain an urgent temporary injunction restraining the landlord from illegal dispossession."
        ],
        evidence_to_preserve=["Rent agreement", "Bank statements / rent receipts", "Photos/videos of any lockout or disconnection", "Messages from landlord"],
        helplines=["112 (Police Emergency)", "15100 (NALSA Legal Aid)"],
        governing_statutes=["Transfer of Property Act, 1882 (Section 106)", "The Bharatiya Nyaya Sanhita, 2023 (Section 329)", "State Rent Control Acts"],
        legal_provisions_summary=(
            "The Supreme Court in Midnapore Zamindary and subsequent rulings firmly established that even a tenant whose lease has expired cannot be dispossessed except in accordance with law."
        ),
        keywords=["landlord asking to leave tomorrow", "throw me out immediately", "makan malik nikal raha hai", "landlord evict tomorrow", "illegal eviction locks"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q17_LAND_ENCROACHMENT",
        category="Civil Property Disputes",
        direct_answer=(
            "Do not use physical force to reclaim the land. Handle encroachment through documentary verification and civil court remedies."
        ),
        step_by_step_actions=[
            "Gather all primary title deeds, registered sale deed, demarcation map, property tax receipts, and municipal revenue records showing clear ownership and boundary lines.",
            "Apply to the local Tehsildar / Revenue Department for an official government land survey and boundary demarcation.",
            "Send a formal legal notice through an advocate calling upon the neighbour to remove the unauthorized encroachment within 15 days.",
            "If unheeded, file a Civil Suit for Demarcation, Permanent Injunction, and Possession before the jurisdictional Civil Court.",
            "Avoid physical confrontations, as taking law into your own hands can lead to cross-complaints of criminal trespass and breach of peace."
        ],
        evidence_to_preserve=["Registered Sale Deed", "Revenue / Khatiyan / Jamabandi records", "Survey and boundary demarcation map", "Photographs of current encroachment"],
        helplines=["District Revenue Department / Tehsildar Office"],
        governing_statutes=["Specific Relief Act, 1963 (Section 5 & 6)", "Code of Civil Procedure, 1908 (Order XXXIX)"],
        legal_provisions_summary=(
            "Section 5 & 6 Specific Relief Act, 1963 provide the statutory mechanism to recover possession of immovable property based on title or prior possession."
        ),
        keywords=["neighbour occupied land", "encroachment land neighbour", "kabza kar liya", "neighbour encroached plot", "land encroachment civil"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q18_NOISE_POLLUTION",
        category="Environmental Law & Public Nuisance",
        direct_answer=(
            "Yes. You have the legal right to peace and quiet, and India's noise pollution regulations strictly prohibit loud music at night."
        ),
        step_by_step_actions=[
            "Under the Noise Pollution (Regulation and Control) Rules, 2000, loudspeakers and high-volume public address systems cannot be operated at night between 10:00 PM and 6:00 AM (except during specially permitted cultural events).",
            "In residential areas, noise levels must not exceed 55 dB(A) during day and 45 dB(A) during night.",
            "When loud music plays at night, call 112 immediately to report public nuisance and noise violation.",
            "Record video/audio from inside your residence with timestamps showing the disturbance.",
            "If continuous, lodge a written complaint with the Station House Officer (SHO) under Section 292 BNS (public nuisance) and the State Pollution Control Board."
        ],
        evidence_to_preserve=["Timestamped audio/video recordings from inside residence", "Call logs to 112 with call registration numbers", "Written complaint copy"],
        helplines=["112 (Police Emergency)", "Local State Pollution Control Board"],
        governing_statutes=["Noise Pollution (Regulation and Control) Rules, 2000", "The Bharatiya Nyaya Sanhita, 2023 (Section 292 Public Nuisance)"],
        legal_provisions_summary=(
            "The Noise Pollution Rules 2000 framed under the Environment (Protection) Act, 1986 prohibit nocturnal noise. Section 292 BNS punishes public nuisance causing common injury or annoyance."
        ),
        keywords=["neighbour plays loud music", "loud music every night", "raat ko tez gaane", "noise pollution neighbour", "loud speaker night complaint"]
    ),

    # 7. Road Accidents, Public Services and Legal Assistance
    CitizenLegalGuidance(
        scenario_id="Q19_VEHICLE_ACCIDENT_DUTIES",
        category="Motor Vehicle Law & Emergency Duties",
        direct_answer=(
            "Stop safely immediately, render medical assistance if required, and comply with your statutory duties under the Motor Vehicles Act."
        ),
        step_by_step_actions=[
            "Immediately stop your vehicle safely at the side of the road without obstructing traffic. Never flee the scene (hit-and-run carries severe criminal penalties).",
            "Check if anyone is injured. If yes, call 108 for an ambulance or take reasonable steps to secure medical attention.",
            "Section 134 of the Motor Vehicles Act, 1988 mandates that the driver involved in an accident must render medical help and report the occurrence to the police within 24 hours.",
            "Exchange vehicle registration numbers and insurance details calmly. Avoid physical arguments or admitting fault at the roadside.",
            "Notify your motor insurance company immediately to initiate the third-party claims process and take photos of vehicle damage."
        ],
        evidence_to_preserve=["Photographs of both vehicles and road conditions", "Vehicle registration and third-party insurance certificate", "General Diary (GD) or police intimation copy"],
        helplines=["108 (Ambulance / Medical Emergency)", "112 (Police)"],
        governing_statutes=["Motor Vehicles Act, 1988 (Section 134)", "The Bharatiya Nyaya Sanhita, 2023 (Section 281 & 106)"],
        legal_provisions_summary=(
            "Section 134 Motor Vehicles Act specifies the affirmative duty of driver in case of accident to secure medical attention and report to police."
        ),
        keywords=["hit someone vehicle with bike", "accidentally hit car bike", "accident ho gaya", "bike accident duties", "hit vehicle what to do"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q20_FREE_LEGAL_AID",
        category="Access to Justice & Legal Aid",
        direct_answer=(
            "No. Inability to afford a private lawyer does not mean you cannot fight your case. India provides free, government-funded legal representation."
        ),
        step_by_step_actions=[
            "Under the Legal Services Authorities Act, 1987, eligible citizens are entitled to free legal aid, including a court-appointed advocate and exemption from court fees.",
            "Eligible categories include: women, children, members of SC/ST, persons with disabilities, victims of trafficking, undertrial prisoners, and individuals whose annual income is below statutory state thresholds (typically INR 3 Lakhs or as notified).",
            "You can approach the District Legal Services Authority (DLSA) located inside any District Court premises, or the Taluk Legal Services Committee.",
            "You can call the National Legal Services Authority (NALSA) toll-free helpline at 15100 or apply online on https://nalsa.gov.in.",
            "Court clerks and judicial magistrates are duty-bound to inform unrepresented persons of their right to legal aid."
        ],
        evidence_to_preserve=["Income certificate or BPL card if applicable", "Identity proof (Aadhaar/Voter ID)", "Case court papers or summons received"],
        helplines=["15100 (NALSA National Legal Aid Helpline)", "nalsa.gov.in"],
        governing_statutes=["Legal Services Authorities Act, 1987 (Section 12)", "Constitution of India (Article 39A)"],
        legal_provisions_summary=(
            "Article 39A of the Constitution directs the State to provide free legal aid. Section 12 of the Legal Services Authorities Act 1987 defines the categories of persons entitled to free services."
        ),
        keywords=["cannot afford a lawyer", "free lawyer legal aid", "paise nahi hain lawyer ke", "free legal aid nalsa", "dlsa free advocate"]
    ),

    # 8. Important Edge Cases (Q21 to Q25)
    CitizenLegalGuidance(
        scenario_id="Q21_AADHAAR_LOSS_MISUSE",
        category="Identity Security & Aadhaar",
        direct_answer=(
            "Losing a physical Aadhaar card does not automatically mean identity theft has occurred, because your biometric data is protected on UIDAI servers."
        ),
        step_by_step_actions=[
            "Log in to the official UIDAI portal (https://myaadhaar.uidai.gov.in) using your registered mobile number and OTP.",
            "Use the 'Lock Biometrics' feature immediately so no person can authenticate transactions using your fingerprint or iris.",
            "Check your 'Authentication History' on myAadhaar to verify if any unauthorized authentication attempts have taken place.",
            "Order a replacement Aadhaar PVC card directly through the UIDAI portal.",
            "File an online lost document report (Lost Article Report) with your local State Police portal as a precautionary record."
        ],
        evidence_to_preserve=["Online Lost Document General Diary receipt", "Aadhaar number or Enrollment ID"],
        helplines=["1947 (UIDAI Toll-Free Helpline)", "myaadhaar.uidai.gov.in"],
        governing_statutes=["Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) Act, 2016"],
        legal_provisions_summary=(
            "Aadhaar authentication requires biometric matching or OTP validation sent to the registered mobile number. Mere possession of a lost printed card cannot bypass multi-factor authentication."
        ),
        keywords=["lost aadhaar card", "aadhaar card kho gaya", "can someone misuse aadhaar", "lost my aadhaar misuse", "aadhaar biometric lock"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q22_MONEY_LENT_CIVIL_VS_CRIMINAL",
        category="Civil Debt vs Criminal Cheating",
        direct_answer=(
            "Generally, mere failure to return borrowed money is a civil debt-recovery dispute, not a criminal offence that sends someone straight to jail."
        ),
        step_by_step_actions=[
            "Understand the legal distinction: Inability or refusal to repay a loan is a breach of contract/debt matter. It becomes criminal cheating (Section 318 BNS) only if the borrower had dishonest, fraudulent intention right from the start when taking the money.",
            "If this was a friendly or commercial loan, your legal remedy is to file a Civil Recovery Suit or Summary Suit under Order XXXVII of the CPC.",
            "Start by sending a formal Legal Notice through an advocate demanding repayment within 15 days.",
            "If the borrower gave you a cheque that bounced upon presentation, you can file a criminal complaint under Section 138 of the Negotiable Instruments Act within 30 days of the statutory notice period.",
            "Preserve bank transfer receipts, WhatsApp chat admissions of debt, promissory notes, or written agreements."
        ],
        evidence_to_preserve=["Bank transfer statement showing money sent", "Chat messages/emails admitting receipt of loan and promise to return", "Promissory note or loan agreement"],
        helplines=["15100 (Legal Aid)"],
        governing_statutes=["Code of Civil Procedure, 1908 (Order XXXVII)", "The Negotiable Instruments Act, 1881 (Section 138)", "The Bharatiya Nyaya Sanhita, 2023 (Section 318)"],
        legal_provisions_summary=(
            "The Supreme Court has consistently held (e.g. in Dalip Kaur v. Jagnar Singh) that breach of contract does not give rise to criminal cheating unless fraudulent intent existed at the inception."
        ),
        keywords=["borrowed money refusing to return", "send them to jail money", "udhaar wapas nahi de raha", "jail for borrowed money", "can i jail borrower"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q23_ADULT_INDEPENDENCE",
        category="Constitutional Rights & Adult Autonomy",
        direct_answer=(
            "No. Once you attain the age of majority (18 years), your parents cannot legally force or confine you to live with them against your will."
        ),
        step_by_step_actions=[
            "Under Indian law, every person aged 18 or above is an independent adult endowed with full legal capacity.",
            "Article 21 of the Constitution guarantees the fundamental right to life, personal liberty, and freedom of movement anywhere within the territory of India.",
            "Parents cannot legally lodge kidnapping or abduction charges against an adult or third parties assisting an adult to live independently.",
            "If parents threaten, physically confine, or attempt to forcefully take you, call 112 or seek a writ of habeas corpus or police protection order through the High Court.",
            "Keep your identity documents (Aadhaar, educational certificates, passport) in your personal possession."
        ],
        evidence_to_preserve=["Identity proof confirming age over 18", "Messages/records of threats of confinement"],
        helplines=["112 (National Emergency Helpline)", "15100 (Legal Aid)"],
        governing_statutes=["Constitution of India (Article 21 & Article 19(1)(d))", "Indian Majority Act, 1875 (Section 3)"],
        legal_provisions_summary=(
            "Under Section 3 Indian Majority Act 1875, majority is attained at 18 years. An adult cannot be compelled to reside in custody of parents against their consent."
        ),
        keywords=["parents stop me living independently", "stop living independently after 18", "parents forcing to live with them 18", "adult independence parents"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q24_PRIVATE_PHOTO_FORWARDING",
        category="Cyber Privacy & Consent",
        direct_answer=(
            "No. Forwarding or sharing private, intimate photographs without explicit consent is illegal and carries severe criminal penalties."
        ),
        step_by_step_actions=[
            "Do not forward or publish the photograph. Receipt of a private photo confers no legal right to share it with friends, groups, or online platforms.",
            "Publishing or transmitting private intimate images without consent is punishable under Section 66E (violation of privacy) and Section 67/67A of the Information Technology Act, 2000.",
            "Under Section 77 and Section 78 of the Bharatiya Nyaya Sanhita (BNS), 2023, voyeurism and non-consensual circulation of intimate images carry substantial imprisonment.",
            "Delete the content or keep it strictly confidential. Once circulated, digital footprints are easily traceable to the sender's device and IP address.",
            "If someone is threatening to circulate your private photos, report immediately to https://cybercrime.gov.in and call 1930."
        ],
        evidence_to_preserve=["Do not share further"],
        helplines=["1930 (Cybercrime Helpline)", "cybercrime.gov.in"],
        governing_statutes=["Information Technology Act, 2000 (Section 66E & Section 67)", "The Bharatiya Nyaya Sanhita, 2023 (Section 77 & Section 78)"],
        legal_provisions_summary=(
            "Section 66E IT Act penalizes intentionally capturing or transmitting the image of a private area of any person without consent. Section 77 BNS penalizes voyeurism and sharing."
        ),
        keywords=["forward private photo whatsapp", "friend sent private photo", "can i forward private photo", "private photo whatsapp group", "forwarding intimate photos"]
    ),
    CitizenLegalGuidance(
        scenario_id="Q25_COURT_NOTICE_IGNORING",
        category="Civil & Criminal Procedure",
        direct_answer=(
            "No. Never ignore a court notice or judicial summons under any circumstances."
        ),
        step_by_step_actions=[
            "Check the notice immediately for: (a) Name of the Court, (b) Case Number, (c) Date of Hearing / Appearance, and (d) Next steps demanded.",
            "Ignoring a Civil Notice can result in the Court proceeding 'ex-parte' (deciding the case against you in your absence and ordering attachment of bank accounts/property).",
            "Ignoring a Criminal Summons or Section 138 Notice can lead to the Magistrate issuing bailable or Non-Bailable Warrants (NBW) for your arrest.",
            "Consult a practicing advocate immediately with the complete summons papers to prepare a formal written reply or appearance.",
            "If you cannot afford an advocate, carry the notice directly to the District Legal Services Authority (DLSA) at the court complex for a free government advocate."
        ],
        evidence_to_preserve=["Complete copy of summons / notice received", "Postal envelope showing delivery date", "Attached plaint or complaint copy"],
        helplines=["15100 (NALSA Free Legal Aid)", "Local District Court DLSA Front Desk"],
        governing_statutes=["Code of Civil Procedure, 1908 (Order IX)", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 64 & Section 73)"],
        legal_provisions_summary=(
            "Order IX CPC allows the court to make an ex-parte decree if defendant fails to appear after valid service. BNSS provisions authorize arrest warrants for non-appearance after summons."
        ),
        keywords=["received a court notice", "can i ignore court notice", "court notice ignore kar sakte hain", "court summons ignore", "what if ignore court notice"]
    )
]


class CitizenLegalGuidanceEngine:
    """Matches citizen queries to structured, plain-English guidance and practical remedies."""

    @classmethod
    def match_citizen_query(cls, query: str) -> Optional[CitizenLegalGuidance]:
        """Detect whether a query corresponds to one of the benchmark citizen situations."""
        if not query or not query.strip():
            return None

        q_lower = query.lower()
        import re
        q_words = set(re.findall(r"\w+", q_lower))

        best_match = None
        highest_score = 0

        for guidance in CITIZEN_KNOWLEDGE_BASE:
            score = 0
            for kw in guidance.keywords:
                kw_lower = kw.lower()
                if kw_lower in q_lower:
                    score += 8
                else:
                    kw_words = set(re.findall(r"\w+", kw_lower))
                    if kw_words:
                        overlap = len(kw_words.intersection(q_words))
                        match_ratio = overlap / len(kw_words)
                        if match_ratio >= 0.5 and overlap >= 2:
                            score += int(match_ratio * 6)

            # Specific high-intent keyword boosts for all citizen scenarios (Q1-Q25)
            if guidance.scenario_id == "Q1_FIR_REFUSAL":
                if ("fir" in q_words or "police complaint" in q_lower or "complaint" in q_words) and ("refus" in q_lower or "not registering" in q_lower or "nahi likh" in q_lower or "mana" in q_lower):
                    score += 15
            elif guidance.scenario_id == "Q2_ARREST_GROUNDS":
                if ("arrest" in q_words or "hirasat" in q_lower) and ("without telling" in q_lower or "grounds" in q_words or "reason" in q_words or "bina bataye" in q_lower or "kyu" in q_lower):
                    score += 15
            elif guidance.scenario_id == "Q3_CRIMINAL_INTIMIDATION":
                if ("threatening" in q_words or "threat" in q_words or "dhamki" in q_lower) and ("beat" in q_words or "hit" in q_words or "kill" in q_words or "maarne" in q_lower or "police" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q4_CYBER_BANK_FRAUD":
                if ("stole" in q_words or "stolen" in q_words or "fraud" in q_words or "paise kat gaye" in q_lower or "deducted" in q_words) and ("bank" in q_words or "account" in q_words or "1930" in q_words or "pretending" in q_words or "cyber" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q5_FAKE_SOCIAL_PROFILE":
                if ("fake" in q_words or "impersonat" in q_lower or "misuse" in q_words) and ("instagram" in q_words or "profile" in q_words or "account" in q_words or "photos" in q_words or "photo" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q6_OTP_SHARING_LIABILITY":
                if "otp" in q_words and ("shared" in q_words or "share" in q_words or "accidentally" in q_words or "galti" in q_lower or "take money" in q_lower):
                    score += 15
            elif guidance.scenario_id == "Q7_DEFECTIVE_PRODUCT_SHOP":
                if ("phone" in q_words or "product" in q_words or "item" in q_words or "samaan" in q_lower) and ("defect" in q_lower or "stopped working" in q_lower or "refuses to replace" in q_lower or "warranty" in q_words or "replace" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q8_ECOMMERCE_NONDELIVERY":
                if ("online" in q_words or "shopping" in q_words or "amazon" in q_words or "flipkart" in q_words or "website" in q_words) and ("not delivered" in q_lower or "never delivered" in q_lower or "delivery" in q_words or "took money" in q_lower):
                    score += 15
            elif guidance.scenario_id == "Q9_MENU_OVERCHARGING":
                if ("restaurant" in q_words or "cafe" in q_words or "hotel" in q_words or "menu" in q_words or "mrp" in q_words) and ("charged more" in q_lower or "overcharg" in q_lower or "extra charge" in q_lower or "printed" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q10_WIFE_MAINTENANCE":
                if ("husband" in q_words or "pati" in q_words) and ("expenses" in q_words or "kharcha" in q_words or "money" in q_words or "maintenance" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q11_FORCED_MARRIAGE":
                if ("marry" in q_words or "marriage" in q_words or "shaadi" in q_words) and ("forcing" in q_words or "force" in q_words or "refuse" in q_words or "parents" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q12_STALKING_HARASSMENT":
                if ("messages" in q_words or "message" in q_words) and ("unwanted" in q_words or "romantic" in q_words or "harassment" in q_words or "stalking" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q13_UNPAID_SALARY":
                if ("salary" in q_words or "wages" in q_words) and ("not paying" in q_lower or "unpaid" in q_words or "nahi de raha" in q_lower):
                    score += 10
            elif guidance.scenario_id == "Q14_COLLEGE_CERTIFICATE_WITHHELD":
                if ("college" in q_words or "university" in q_words or "school" in q_words) and ("certificates" in q_words or "certificate" in q_words or "marksheet" in q_words or "degree" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q15_SUDDEN_TERMINATION":
                if ("fired" in q_words or "terminated" in q_words or "termination" in q_words or "job" in q_words or "unlawful termination" in q_lower) and ("notice" in q_words or "bina notice" in q_lower or "rights" in q_words or "unlawful" in q_words or "employment" in q_words):
                    score += 15
            elif guidance.scenario_id == "Q16_ILLEGAL_EVICTION":
                if ("landlord" in q_words or "makan malik" in q_lower or "rented" in q_words) and ("leave" in q_words or "throw" in q_words or "evict" in q_words or "tomorrow" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q17_LAND_ENCROACHMENT":
                if ("neighbour" in q_words or "neighbor" in q_words or "padosi" in q_words) and ("land" in q_words or "plot" in q_words or "occupied" in q_words or "encroached" in q_words or "kabza" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q18_NOISE_POLLUTION":
                if ("loud music" in q_lower or "music" in q_words or "speaker" in q_words or "sound" in q_words) and ("night" in q_words or "every night" in q_lower or "raat" in q_words or "neighbour" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q19_VEHICLE_ACCIDENT_DUTIES":
                if ("hit" in q_words or "accident" in q_words or "collision" in q_words) and ("bike" in q_words or "car" in q_words or "vehicle" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q20_FREE_LEGAL_AID":
                if ("cannot afford" in q_lower or "no money" in q_lower or "paise nahi" in q_lower or "free" in q_words) and ("lawyer" in q_words or "advocate" in q_words or "case" in q_words or "legal aid" in q_lower):
                    score += 10
            elif guidance.scenario_id == "Q21_AADHAAR_LOSS_MISUSE":
                if "aadhaar" in q_words and ("lost" in q_words or "misuse" in q_words or "kho gaya" in q_lower):
                    score += 10
            elif guidance.scenario_id == "Q22_MONEY_LENT_CIVIL_VS_CRIMINAL":
                if ("borrowed" in q_words or "lent" in q_words or "udhaar" in q_words or "refusing to return" in q_lower) and ("jail" in q_words or "money" in q_words or "cheating" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q23_ADULT_INDEPENDENCE":
                if ("parents" in q_words or "family" in q_words) and ("independently" in q_words or "18" in q_words or "leave home" in q_lower or "independent" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q24_PRIVATE_PHOTO_FORWARDING":
                if ("photo" in q_words or "picture" in q_words or "image" in q_words) and ("private" in q_words or "intimate" in q_words or "forward" in q_words or "whatsapp" in q_words):
                    score += 10
            elif guidance.scenario_id == "Q25_COURT_NOTICE_IGNORING":
                if ("court" in q_words or "summons" in q_words or "notice" in q_words) and ("ignore" in q_words or "don't understand" in q_lower or "received" in q_words):
                    score += 10

            if score > highest_score and score >= 4:
                highest_score = score
                best_match = guidance

        return best_match

    @classmethod
    def format_citizen_response(cls, guidance: CitizenLegalGuidance) -> str:
        """Format the guidance into a clean, human-friendly, three-tier response."""
        parts = []

        # 1. Direct Plain-English Answer
        parts.append(f"### Direct Position (In Plain Words)\n{guidance.direct_answer}")

        # 2. Actionable Step-by-Step Guide
        action_lines = "\n".join([f"- **Step {i+1}:** {act}" for i, act in enumerate(guidance.step_by_step_actions)])
        parts.append(f"### Practical Action Guide (What You Should Do)\n{action_lines}")

        # 3. Evidence to Preserve & Emergency Helplines
        evidence_str = ", ".join(guidance.evidence_to_preserve)
        helplines_str = ", ".join(guidance.helplines)
        parts.append(f"### Important Checklists & Helplines\n- **Evidence to Preserve:** {evidence_str}\n- **Emergency Helplines:** {helplines_str}")

        # 4. Simplified Legal Basis (Collapsible Reference)
        statutes_str = "\n".join([f"- {s}" for s in guidance.governing_statutes])
        parts.append(
            f"### Governing Law & Statutory References\n"
            f"{guidance.legal_provisions_summary}\n\n"
            f"**Applicable Provisions:**\n{statutes_str}"
        )

        return "\n\n".join(parts)
