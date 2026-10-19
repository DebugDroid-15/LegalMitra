"""
Script to expand temporal benchmark manifest to 120 cases under suite ID LEGALMITRA-BENCHMARK-PIT-V8.
Partitions the suite into:
- development (50 cases, PIT-01 to PIT-50)
- validation (20 cases, PIT-51 to PIT-70)
- held_out_evaluation (50 cases, PIT-71 to PIT-120)
"""

import json
from pathlib import Path

MANIFEST_PATH = Path("data/22_central_legislation/temporal_benchmark_manifest.json")

NEW_CASES = [
    {
        "case_id": "PIT-101",
        "domain": "Corpus Integrity — Synthetic Scaffold Quarantine Defense",
        "query_description": "Can the orchestrator retrieve or cite IND-JUD-DEL-2024-BAIL (Rahul Kumar v. State) as authoritative Delhi High Court precedent for anticipatory bail under BNSS s.482?",
        "query_temporal_anchor": "2024-08-15",
        "target_statutes": ["IND-STAT-BNSS-2023"],
        "expected_governing_regime": "Corpus Integrity Governance & Synthetic Scaffold Quarantine",
        "expected_applicable_provisions": ["Section 482 BNSS 2023"],
        "expected_disentangled_rationale": "No. IND-JUD-DEL-2024-BAIL is a quarantined synthetic test scaffold with inverted party designation (State petitioner for anticipatory bail). Under LegalMitra Phase 52 evidence eligibility safeguards, it is strictly ineligible for retrieval.",
        "expected_precedent_cites": ["Sushila Aggarwal v. State (NCT of Delhi) (2020) 5 SCC 1"],
        "expected_response_state": "ABSTAIN_UNSUPPORTED",
        "required_claim_validation_outcomes": ["UNSUPPORTED"],
        "forbidden_conclusions": ["IND-JUD-DEL-2024-BAIL is an authentic Delhi High Court ruling"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-102",
        "domain": "Rights & Copyright Law — Reproduction of Gazette Enactments under Section 52(1)(q)",
        "query_description": "Does internal retrieval and indexing of central acts published in the Gazette of India infringe copyright under Indian law?",
        "query_temporal_anchor": "2024-05-10",
        "target_statutes": ["IND-STAT-CR-1957"],
        "expected_governing_regime": "Copyright Act, 1957 Section 52(1)(q)(i) & GODL-India",
        "expected_applicable_provisions": ["Section 52(1)(q)(i) Copyright Act 1957"],
        "expected_disentangled_rationale": "No. Under Section 52(1)(q)(i) of the Copyright Act, 1957, the reproduction or publication of any matter which has been published in the Official Gazette does not constitute copyright infringement. Retrieval indexing of official statutory text is lawful.",
        "expected_precedent_cites": ["Eastern Book Company v. D.B. Modak (2008) 1 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Reproduction of Gazette text is copyright infringement"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-103",
        "domain": "Judicial Precedent Reproduction Rights — Section 52(1)(q)(iv)",
        "query_description": "Does the verbatim indexing and retrieval of Supreme Court of India judgments for legal QA violate judicial copyright?",
        "query_temporal_anchor": "2024-06-20",
        "target_statutes": ["IND-STAT-CR-1957"],
        "expected_governing_regime": "Copyright Act, 1957 Section 52(1)(q)(iv)",
        "expected_applicable_provisions": ["Section 52(1)(q)(iv) Copyright Act 1957"],
        "expected_disentangled_rationale": "No. Section 52(1)(q)(iv) of the Copyright Act, 1957 expressly provides that the reproduction of any judgment or order of a court, tribunal or other judicial authority is not an infringement of copyright, unless court publication is explicitly prohibited.",
        "expected_precedent_cites": ["Eastern Book Company v. D.B. Modak (2008) 1 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Judgments of the Supreme Court cannot be reproduced under Section 52"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-104",
        "domain": "Corpus Gap — Insolvency & Bankruptcy Code Section 7 Admission Standard",
        "query_description": "Under IBC Section 7, is the NCLT obligated to admit a Section 7 petition if default has occurred, or does Vidarbha Industries grant discretion?",
        "query_temporal_anchor": "2024-04-10",
        "target_statutes": ["IND-STAT-IBC-2016"],
        "expected_governing_regime": "Insolvency and Bankruptcy Code, 2016 Section 7",
        "expected_applicable_provisions": ["Section 7 IBC 2016"],
        "expected_disentangled_rationale": "In Vidarbha Industries (2022), the Supreme Court noted that Section 7(5)(a) uses 'may', permitting the Adjudicating Authority to defer admission in exceptional circumstances. However, in Innoventive Industries and subsequent clarifications (M. Suresh Kumar Reddy 2023), the Court affirmed that once financial debt and default are established, admission is ordinarily mandatory.",
        "expected_precedent_cites": ["Innoventive Industries Ltd. v. ICICI Bank (2018) 1 SCC 407", "Vidarbha Industries Power Ltd. v. Axis Bank (2022) 8 SCC 352"],
        "expected_response_state": "ANSWER_QUALIFIED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["NCLT has unlimited arbitrary discretion to reject Section 7 petitions"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-105",
        "domain": "Temporal Authenticity — Digital Personal Data Protection Act 2023 Section 44 Repeal of Section 43A IT Act",
        "query_description": "As of June 2024, has Section 43A of the Information Technology Act 2000 been repealed by Section 44 of the DPDP Act 2023?",
        "query_temporal_anchor": "2024-06-15",
        "target_statutes": ["IND-STAT-IT-2000", "IND-STAT-DPDP-2023"],
        "expected_governing_regime": "Temporal Commencement Distinction — DPDP Act Section 1(2) & S.44 Unnotified",
        "expected_applicable_provisions": ["Section 43A IT Act 2000", "Section 44 DPDP Act 2023"],
        "expected_disentangled_rationale": "No. Although Section 44 of the DPDP Act, 2023 enacts the repeal of Section 43A of the IT Act, Section 1(2) of the DPDP Act provides that the Act comes into force on such date as the Central Government appoints. As of June 2024, Section 44 has not been notified in the Gazette; therefore, Section 43A of the IT Act and SPDI Rules 2011 remain in force.",
        "expected_precedent_cites": ["Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Section 43A IT Act was repealed immediately upon Presidential assent in August 2023"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-106",
        "domain": "Evidence Ineligibility — Unparsed Format Fixture Rejection (IND-UNSUPPORTED-001)",
        "query_description": "Can the retrieval pipeline extract substantive legal principles from test fixture IND-UNSUPPORTED-001?",
        "query_temporal_anchor": "2024-07-01",
        "target_statutes": ["IND-UNSUPPORTED-001"],
        "expected_governing_regime": "Evidence Eligibility Policy (Fixture Rejection)",
        "expected_applicable_provisions": ["N/A"],
        "expected_disentangled_rationale": "No. IND-UNSUPPORTED-001 is a negative format-checking test fixture (.xyz extension) containing no parsed legal chunks. The eligibility engine enforces fail-closed rejection.",
        "expected_precedent_cites": [],
        "expected_response_state": "ABSTAIN_UNSUPPORTED",
        "required_claim_validation_outcomes": ["UNSUPPORTED"],
        "forbidden_conclusions": ["IND-UNSUPPORTED-001 is a substantive legal authority"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-107",
        "domain": "Intellectual Property — Patentability of Known Chemical Entities under Section 3(d)",
        "query_description": "Does the discovery of a new polymorphic form of a known pharmaceutical substance constitute an invention under Section 3(d) of the Patents Act, 1970 without demonstrating enhanced efficacy?",
        "query_temporal_anchor": "2024-05-01",
        "target_statutes": ["IND-STAT-PATENTS-1970"],
        "expected_governing_regime": "Patents Act, 1970 Section 3(d)",
        "expected_applicable_provisions": ["Section 3(d) Patents Act 1970"],
        "expected_disentangled_rationale": "No. Under Section 3(d) of the Patents Act, the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance is not an invention. In Novartis AG v. Union of India (2013), the Supreme Court held that 'efficacy' means therapeutic efficacy for pharmacological products.",
        "expected_precedent_cites": ["Novartis AG v. Union of India (2013) 6 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["New polymorph is per se patentable without proving enhanced therapeutic efficacy"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-108",
        "domain": "Labour Law — Industrial Disputes Act Section 25F Retrenchment Compensation Savings",
        "query_description": "For a retrenchment effected on 15 May 2024, does an employer calculate retrenchment compensation under Section 25F of the Industrial Disputes Act, 1947 or under the Industrial Relations Code, 2020?",
        "query_temporal_anchor": "2024-05-15",
        "target_statutes": ["IND-STAT-IDA-1947", "IND-STAT-IRC-2020"],
        "expected_governing_regime": "Industrial Disputes Act, 1947 Section 25F (Enacted Codes Unnotified)",
        "expected_applicable_provisions": ["Section 25F IDA 1947", "Section 1(3) IR Code 2020"],
        "expected_disentangled_rationale": "Under Section 25F of the Industrial Disputes Act, 1947. Although the Industrial Relations Code, 2020 was enacted by Parliament, its commencement notification has not been issued by the Central Government. The IDA 1947 remains the governing law in May 2024.",
        "expected_precedent_cites": ["Bangalore Water Supply and Sewerage Board v. A. Rajappa (1978) 2 SCC 213"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Industrial Relations Code 2020 repeals Section 25F IDA prior to commencement notification"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-109",
        "domain": "Precedent Authority — Single Judge High Court Rulings vs Supreme Court Constitution Bench",
        "query_description": "Can a Single Judge decision of the High Court overrule a 5-Judge Constitution Bench of the Supreme Court of India?",
        "query_temporal_anchor": "2024-07-20",
        "target_statutes": ["IND-CONST-1950"],
        "expected_governing_regime": "Constitution of India Article 141 (Binding Precedent & Judicial Hierarchy)",
        "expected_applicable_provisions": ["Article 141 Constitution of India", "Article 227 Constitution of India"],
        "expected_disentangled_rationale": "No. Under Article 141 of the Constitution of India, the law declared by the Supreme Court is binding on all courts within the territory of India. A High Court bench has no jurisdiction to overrule or disregard a Supreme Court decision, let alone a Constitution Bench.",
        "expected_precedent_cites": ["Suganthi Suresh Kumar v. Jagdeeshan (2002) 2 SCC 420"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["High Court Single Judge can overrule a Supreme Court Constitution Bench"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-110",
        "domain": "Corpus Gap — Personal Law & Coparcenary Rights (Vineeta Sharma)",
        "query_description": "Does a Hindu daughter have coparcenary rights under Section 6 of the Hindu Succession Act if her father passed away prior to the 2005 Amendment Act?",
        "query_temporal_anchor": "2024-03-15",
        "target_statutes": ["IND-STAT-HSA-1956"],
        "expected_governing_regime": "Hindu Succession Act, 1956 Section 6 (as amended by Act 39 of 2005)",
        "expected_applicable_provisions": ["Section 6 Hindu Succession Act 1956"],
        "expected_disentangled_rationale": "Yes. In Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1 (3-Judge Bench), the Supreme Court settled conflicting decisions (Prakash v. Phulavati and Danamma) and held that daughters have coparcenary rights by birth. The father need not have been alive on 9 September 2005, provided the coparcenary property was not alienated or divided by registered partition prior to 20 December 2004.",
        "expected_precedent_cites": ["Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Daughter is denied coparcenary right if father died before 2005"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-111",
        "domain": "Criminal Transition — Ongoing CrPC Trial Savings under BNSS Section 531(2)(a)",
        "query_description": "If a criminal trial was pending before a Sessions Court on 30 June 2024, does the trial continue under CrPC 1973 or convert to BNSS 2023 on 1 July 2024?",
        "query_temporal_anchor": "2024-07-05",
        "target_statutes": ["IND-STAT-CRPC-1973", "IND-STAT-BNSS-2023"],
        "expected_governing_regime": "BNSS 2023 Section 531(2)(a) Procedural Savings",
        "expected_applicable_provisions": ["Section 531(2)(a) BNSS 2023"],
        "expected_disentangled_rationale": "The trial continues under the Code of Criminal Procedure, 1973. Under Section 531(2)(a) of BNSS 2023, every appeal, application, trial, inquiry or investigation pending immediately before 1 July 2024 shall be disposed of, continued, held or made in accordance with the provisions of the Code of Criminal Procedure, 1973, as if the BNSS had not come into force.",
        "expected_precedent_cites": ["State of Punjab v. Mohar Singh AIR 1955 SC 84"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Pending CrPC trial must restart or convert to BNSS rules"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-112",
        "domain": "Consumer Protection — Product Liability under Consumer Protection Act 2019",
        "query_description": "Can a consumer claim compensation for damage caused by a defective product against both the product manufacturer and product seller under the CPA 2019?",
        "query_temporal_anchor": "2024-06-01",
        "target_statutes": ["IND-STAT-CPA-2019"],
        "expected_governing_regime": "Consumer Protection Act, 2019 Chapter VI (Product Liability)",
        "expected_applicable_provisions": ["Section 84 CPA 2019", "Section 86 CPA 2019"],
        "expected_disentangled_rationale": "Yes. Chapter VI (Sections 82-87) of the Consumer Protection Act, 2019 introduces statutory product liability. Under Section 84, a product manufacturer is liable for manufacturing defects, design defects, or lack of adequate warnings. Under Section 86, a product seller is liable if it exercised substantial control over designing or packaging, altered the product, or failed to exercise reasonable care.",
        "expected_precedent_cites": ["National Seeds Corp. v. M. Madhusudhan Reddy (2012) 2 SCC 506"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Product sellers are strictly exempt from all product liability under CPA 2019"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-113",
        "domain": "Commercial Law — Limitation Period for Commercial Summary Suit",
        "query_description": "What is the limitation period for instituting a summary suit under Order XXXVII CPC for recovery of a debt based on a negotiable instrument?",
        "query_temporal_anchor": "2024-04-15",
        "target_statutes": ["IND-STAT-LIMIT-1963", "IND-STAT-CPC-1908"],
        "expected_governing_regime": "Limitation Act 1963 Schedule Article 19 & CPC Order XXXVII",
        "expected_applicable_provisions": ["Article 19 Limitation Act 1963", "Order XXXVII CPC 1908"],
        "expected_disentangled_rationale": "Three years from the date when the loan is made or cheque/bill is dishonored. Under Article 19, 21, or 35 of the Schedule to the Limitation Act, 1963, suits for money payable or on bills/notes have a limitation period of three years.",
        "expected_precedent_cites": ["State of Kerala v. V.R. Kalliyanikutty (1999) 3 SCC 657"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Summary suits have a 30-day limitation period to file the suit itself"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-114",
        "domain": "Specific Relief Act — Discretionary vs Mandatory Injunction after 2018 Amendment",
        "query_description": "Did the 2018 Amendment to Section 10 of the Specific Relief Act eliminate judicial discretion to deny specific performance of contracts?",
        "query_temporal_anchor": "2024-05-18",
        "target_statutes": ["IND-STAT-SRA-1963"],
        "expected_governing_regime": "Specific Relief (Amendment) Act, 2018 Section 10",
        "expected_applicable_provisions": ["Section 10 SRA 1963 (as amended 2018)"],
        "expected_disentangled_rationale": "Yes. By the Specific Relief (Amendment) Act, 2018 (effective 1 October 2018), Section 10 was amended to substitute 'shall be enforced by the court' for the erstwhile discretionary wording 'may, in the discretion of the court, be enforced'. Specific performance is now the general rule subject only to limited statutory exceptions (e.g., Section 11(2), 14, 16).",
        "expected_precedent_cites": ["B. Santoshamma v. D. Sarala (2020) 19 SCC 80"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["SUPPORTED"],
        "forbidden_conclusions": ["Specific performance remains entirely discretionary after the 2018 amendment"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-115",
        "domain": "Constitutional Law — Doctrine of Basic Structure (Kesavananda Bharati)",
        "query_description": "Can Parliament use its constituent power under Article 368 to abrogate judicial review or destroy the federal character of the Constitution?",
        "query_temporal_anchor": "2024-06-25",
        "target_statutes": ["IND-CONST-1950"],
        "expected_governing_regime": "Basic Structure Doctrine — Kesavananda Bharati & Minerva Mills",
        "expected_applicable_provisions": ["Article 368 Constitution of India", "Article 13 Constitution of India"],
        "expected_disentangled_rationale": "No. In Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225 (13-Judge Bench) and Minerva Mills v. Union of India (1980) 3 SCC 625, the Supreme Court held that while Parliament has wide power to amend the Constitution under Article 368, it cannot alter or destroy the basic structure of the Constitution. Judicial review and federalism are inviolable basic features.",
        "expected_precedent_cites": ["Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225", "Minerva Mills Ltd. v. Union of India (1980) 3 SCC 625"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Parliament's amending power under Article 368 is unlimited and unreviewable"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-116",
        "domain": "Evidence Law — Admissibility of Electronic Records (Section 63 BSA 2023 vs Section 65B IEA 1872)",
        "query_description": "Does an electronic record produced in an offense committed after 1 July 2024 require a certificate under Section 65B of the Indian Evidence Act, 1872?",
        "query_temporal_anchor": "2024-07-25",
        "target_statutes": ["IND-STAT-BSA-2023", "IND-STAT-IEA-1872"],
        "expected_governing_regime": "Bharatiya Sakshya Adhiniyam, 2023 Section 63",
        "expected_applicable_provisions": ["Section 63 BSA 2023", "Schedule to BSA 2023"],
        "expected_disentangled_rationale": "No. For offenses committed and proceedings instituted post-1 July 2024, the Indian Evidence Act, 1872 is repealed and replaced by the Bharatiya Sakshya Adhiniyam, 2023. The applicable provision is Section 63 of BSA 2023, accompanied by the certificate specified in the Schedule to BSA 2023.",
        "expected_precedent_cites": ["Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) 7 SCC 1"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Section 65B IEA remains the certifying provision for post-transition BSA proceedings"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-117",
        "domain": "Model Training Exclusion — Prohibition on Pretraining on Repository Corpus",
        "query_description": "Does LegalMitra permit taking the crawled corpus chunks and fine-tuning or pretraining a proprietary open-weights LLM checkpoint?",
        "query_temporal_anchor": "2024-07-01",
        "target_statutes": ["IND-MITRA-GOVERNANCE"],
        "expected_governing_regime": "LegalMitra Non-Negotiable Governance Invariant (STRICT NO-GO)",
        "expected_applicable_provisions": ["Phase Governance Policy Item 4"],
        "expected_disentangled_rationale": "No. Model pretraining and fine-tuning on the corpus are strictly prohibited under LegalMitra architectural and governance invariants. All reasoning relies on zero-shot retrieval-augmented orchestration with explicit provenance.",
        "expected_precedent_cites": [],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Corpus can be used for foundation model pretraining"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-118",
        "domain": "Arbitration — Ineligibility of Interested Arbitrators under Section 12(5)",
        "query_description": "Can a Managing Director of a contracting public corporation nominate a sole arbitrator to resolve disputes under an agreement executed prior to the 2015 Arbitration Amendment?",
        "query_temporal_anchor": "2024-04-20",
        "target_statutes": ["IND-STAT-ARB-1996"],
        "expected_governing_regime": "Arbitration Act Section 12(5) & Seventh Schedule (TRF / Perkins Eastman)",
        "expected_applicable_provisions": ["Section 12(5) Arbitration Act 1996", "Seventh Schedule Item 1"],
        "expected_disentangled_rationale": "No. Under Section 12(5) read with the Seventh Schedule of the Arbitration and Conciliation Act, 1996, any person whose relationship to the parties falls under the Seventh Schedule is ineligible to be appointed as an arbitrator. In TRF Ltd. (2017) and Perkins Eastman (2020), the Supreme Court ruled that an ineligible person cannot nominate an arbitrator.",
        "expected_precedent_cites": ["TRF Ltd. v. Energo Engineering Projects Ltd. (2017) 8 SCC 377", "Perkins Eastman Architects DPC v. HSCC (India) Ltd. (2020) 20 SCC 760"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["An ineligible Managing Director can unilaterally nominate a sole arbitrator"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-119",
        "domain": "Information Governance — Right to Information Act Section 8(1)(j) Personal Information Exemption",
        "query_description": "Can a Public Information Officer disclose performance appraisal reports of a government employee to an unrelated RTI applicant without finding a larger public interest?",
        "query_temporal_anchor": "2024-05-22",
        "target_statutes": ["IND-ACT-2005-RTI"],
        "expected_governing_regime": "Right to Information Act, 2005 Section 8(1)(j)",
        "expected_applicable_provisions": ["Section 8(1)(j) RTI Act 2005"],
        "expected_disentangled_rationale": "No. Under Section 8(1)(j) of the RTI Act, personal information the disclosure of which has no relationship to any public activity or interest, or which would cause unwarranted invasion of privacy, is exempt unless a larger public interest justifies disclosure. In Girish Ramchandra Deshpande (2013), the Supreme Court held performance appraisals qualify as personal information exempt under Section 8(1)(j).",
        "expected_precedent_cites": ["Girish Ramchandra Deshpande v. Central Information Commissioner (2013) 1 SCC 212"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Performance appraisal reports must be automatically disclosed without public interest finding"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
    {
        "case_id": "PIT-120",
        "domain": "Motor Vehicles Act — Strict Liability Compensation under Section 164 MVA",
        "query_description": "Under Section 164 of the Motor Vehicles Act 1988 (as amended 2019), is a claimant in a fatal road accident required to plead or establish wrongful act, neglect, or default of the vehicle owner?",
        "query_temporal_anchor": "2024-06-30",
        "target_statutes": ["IND-ACT-1988-MVA"],
        "expected_governing_regime": "Motor Vehicles Act, 1988 Section 164 (No-Fault Strict Liability)",
        "expected_applicable_provisions": ["Section 164 MVA 1988 (as amended 2019)"],
        "expected_disentangled_rationale": "No. Under Section 164(2) of the Motor Vehicles Act, 1988 (inserted by Act 32 of 2019), the claimant shall not be required to plead or establish that the death or grievous hurt was due to any wrongful act, neglect, or default of the owner of the vehicle or vehicles concerned. Payment of statutory compensation (Rs. 5,00,000 for death) is strict and automatic.",
        "expected_precedent_cites": ["National Insurance Co. Ltd. v. Pranay Sethi (2017) 16 SCC 680"],
        "expected_response_state": "ANSWER_SUPPORTED",
        "required_claim_validation_outcomes": ["CONTRADICTED"],
        "forbidden_conclusions": ["Claimant under Section 164 must prove driver negligence beyond doubt"],
        "is_overruled": False,
        "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH",
        "split": "held_out_evaluation",
    },
]


def update_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_cases = data.get("test_cases", [])
    existing_ids = {c["case_id"] for c in existing_cases}

    for case in NEW_CASES:
        if case["case_id"] not in existing_ids:
            existing_cases.append(case)

    data["benchmark_suite_id"] = "LEGALMITRA-BENCHMARK-PIT-V8"
    data["version"] = "8.0.0"
    data["total_test_cases"] = len(existing_cases)

    # Re-partition:
    # PIT-01 to PIT-50 -> development (50)
    # PIT-51 to PIT-70 -> validation (20)
    # PIT-71 to PIT-120 -> held_out_evaluation (50)
    dev_count = 0
    val_count = 0
    held_out_count = 0

    for c in existing_cases:
        cid = c["case_id"]
        try:
            num = int(cid.split("-")[1])
        except Exception:
            num = 999

        if num <= 50:
            c["split"] = "development"
            dev_count += 1
        elif num <= 70:
            c["split"] = "validation"
            val_count += 1
        else:
            c["split"] = "held_out_evaluation"
            held_out_count += 1

    data["split_counts"] = {
        "development": dev_count,
        "validation": val_count,
        "held_out_evaluation": held_out_count,
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {MANIFEST_PATH}: Total={len(existing_cases)}, Splits={data['split_counts']}")


if __name__ == "__main__":
    update_manifest()
