"""
Script to expand temporal_benchmark_manifest.json to 60 test cases (PIT-V5).
Adds Cases PIT-41 through PIT-60 covering:
- Express Overruling vs Citation Mention
- Distinguishing vs Overruling
- Referral to Larger Bench vs Final Disposition
- Interim Stay vs Final Binding Judgment
- Larger-Bench vs Smaller-Bench / Court Hierarchy
- Majority vs Concurrence vs Dissent
- Constitutional Provision Interpretation
- Pre-amendment vs Post-amendment Statutory Versions
- Retrospective Legislative Amendment & Savings
- Delegated Legislation Changing Over Time
- Conflicting Definitions Across Enactments
- High Court Jurisdictional Boundary & Co-Equal Conflicts
- Stale or Incomplete Source Manifests
- Invalid, Fabricated, or Mismatched Citations
- Citations that Exist but Do Not Support Attributed Claims
- Unsupported Claims with Authoritative-Sounding Citations
- Incomplete Authority Coverage & Explicit Uncertainty
- Clarification-Demanding Queries
- Mandatory Abstention on Speculative Legal Questions
- Good Law Persistence without Local Contradiction Safeguard
"""

import json
from pathlib import Path

DATA_DIR = Path("data/22_central_legislation")
BENCHMARK_PATH = DATA_DIR / "temporal_benchmark_manifest.json"

def extend_benchmark_to_v5():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["benchmark_suite_id"] = "LEGALMITRA-BENCHMARK-PIT-V5"
    data["version"] = "5.0.0"
    data["description"] = (
        "Point-in-Time statutory, constitutional, delegated legislation, precedent conflict, "
        "and adversarial legal benchmark covering 60 multi-era Indian legal scenarios across "
        "Constitutional, Criminal, Data, Commercial, Corporate, IBC, Contracts, Property, CPC, "
        "MVA, IP, Labour, Delegated Rules, Conflict Triage, and Claim-Level Evidence Validation."
    )

    cases = data.get("test_cases", [])
    existing_ids = {c["case_id"] for c in cases}

    # Define PIT-41 to PIT-60
    new_cases = [
        {
            "case_id": "PIT-41",
            "domain": "Precedent Conflict (Express Overruling vs Citation Mention)",
            "query_description": "In an arbitration reference dispute under Section 11 in 2024, a party cites NN Global (2023) arguing that unstamped arbitration clauses are void ab initio. Does NN Global remain good law?",
            "query_temporal_anchor": "2024-03-15",
            "target_statutes": ["IND-STAT-ARB-1996"],
            "expected_governing_regime": "In Re: Interplay Between Arbitration Agreements & Stamp Act (2024)",
            "expected_applicable_provisions": ["Section 11(6A) Arbitration Act", "Section 33 Stamp Act"],
            "expected_disentangled_rationale": "Overruled. A 7-judge Constitution Bench in In Re: Interplay (2024) expressly overruled the 5-judge bench decision in NN Global Mercantile (2023), holding that non-stamping or insufficient stamping is a curable defect that does not render the arbitration agreement void ab initio at the Section 11 stage.",
            "expected_precedent_cites": ["In Re: Interplay Between Arbitration Agreements and Stamp Act (2024) 6 SCC 1"],
            "is_overruled": True,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-42",
            "domain": "Precedent Conflict (Distinguishing vs Overruling)",
            "query_description": "In 2020, an accused seeks bail under Section 439 CrPC and argues that Arnesh Kumar (2014) laid down guidelines prohibiting arrest, effectively overruling all police powers of arrest under Section 41. Is this argument tenable?",
            "query_temporal_anchor": "2020-08-10",
            "target_statutes": ["IND-STAT-CRPC-1973"],
            "expected_governing_regime": "Arnesh Kumar Procedural Guidelines",
            "expected_applicable_provisions": ["Section 41 CrPC", "Section 41A CrPC"],
            "expected_disentangled_rationale": "Untenable. Arnesh Kumar v. State of Bihar (2014) distinguished routine mechanical arrests from justified arrests, mandating Section 41A notices for offenses punishable up to 7 years. It did not overrule Section 41 or abolish police powers of arrest where statutory conditions (s.41(1)(b)) are satisfied.",
            "expected_precedent_cites": ["Arnesh Kumar v. State of Bihar (2014) 8 SCC 273"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-43",
            "domain": "Precedent Treatment (Referral to Larger Bench vs Final Disposition)",
            "query_description": "A 2-judge bench of the Supreme Court doubts an earlier 2-judge bench judgment on the interpretation of limitation under Section 138 NI Act and refers the question to the Chief Justice for constituting a larger bench. Can a High Court treat the earlier precedent as overruled?",
            "query_temporal_anchor": "2021-02-14",
            "target_statutes": ["IND-STAT-NI-1881"],
            "expected_governing_regime": "Doctrine of Precedent & Article 141",
            "expected_applicable_provisions": ["Article 141 Constitution of India"],
            "expected_disentangled_rationale": "No. A mere reference of a question of law to a larger bench does not overrule or stay the binding nature of an existing precedent under Article 141. Until the larger bench actually delivers judgment reconsidering or overruling the earlier decision, the existing precedent remains binding law.",
            "expected_precedent_cites": ["State of Orissa v. Dhirendra Sundar Das (1970) 3 SCC 809"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-44",
            "domain": "Authority Hierarchy (Interim Stay vs Final Binding Holding)",
            "query_description": "The Supreme Court issues an ex-parte ad-interim stay on the operation of a High Court judgment striking down a state executive rule. Does the interim stay constitute a binding final precedent under Article 141 on the constitutional question?",
            "query_temporal_anchor": "2022-06-20",
            "target_statutes": ["IND-CONST-1950"],
            "expected_governing_regime": "Article 141 Jurisprudence on Interim Orders",
            "expected_applicable_provisions": ["Article 141 Constitution of India"],
            "expected_disentangled_rationale": "No. An interim stay order binds only the parties to the specific litigation and freezes the operation of the appealed decree/order during pendency. An interim stay does not lay down a binding ratio decidendi or declaration of law under Article 141.",
            "expected_precedent_cites": ["State of Assam v. Barak Upatyaka D.U. Karmachari Sanstha (2009) 5 SCC 694"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-45",
            "domain": "Authority Hierarchy (Larger-Bench vs Smaller-Bench Supremacy)",
            "query_description": "A 2-judge Division Bench of the Supreme Court renders an opinion directly conflicting with a 3-judge bench decision rendered five years earlier. Which authority is binding on High Courts and District Courts under Article 141?",
            "query_temporal_anchor": "2023-01-10",
            "target_statutes": ["IND-CONST-1950"],
            "expected_governing_regime": "Article 141 Bench Strength Hierarchy",
            "expected_applicable_provisions": ["Article 141 Constitution of India"],
            "expected_disentangled_rationale": "The 3-judge bench decision is strictly binding. Under the Constitution Bench ruling in Union of India v. Raghubir Singh (1989), the law declared by a larger bench of the Supreme Court binds all subsequent smaller or co-equal benches. A smaller bench cannot overrule or disregard a larger bench decision; any contrary smaller bench ruling is per incuriam.",
            "expected_precedent_cites": ["Union of India v. Raghubir Singh (1989) 2 SCC 754"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-46",
            "domain": "Authority Hierarchy (Majority vs Concurrence vs Dissent)",
            "query_description": "In an Article 21 habeas corpus petition, the petitioner's counsel relies on Justice H.R. Khanna's opinion in ADM Jabalpur (1976) as binding law. Is a dissenting opinion binding precedent under Article 141?",
            "query_temporal_anchor": "2015-04-12",
            "target_statutes": ["IND-CONST-1950"],
            "expected_governing_regime": "Ratio Decidendi of Majority Opinions",
            "expected_applicable_provisions": ["Article 141 Constitution of India"],
            "expected_disentangled_rationale": "No. Under Article 141, only the ratio decidendi of the majority judgment forms the binding law of the land. Although Justice Khanna's dissent was historically revered and ultimately adopted by the 9-judge bench in Puttaswamy (2017) when ADM Jabalpur was formally overruled, a dissent cannot be cited as binding precedent prior to formal overruling.",
            "expected_precedent_cites": ["Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1"],
            "is_overruled": True,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-47",
            "domain": "Amendment-Aware Precedent (Section 28 Contract Act & Vulcan Insurance)",
            "query_description": "An insurance policy issued in 2005 contains a clause stating that all rights under the policy shall be forfeited if no suit is brought within 12 months of claim rejection. The insurer cites Vulcan Insurance (1976) to uphold the clause. Is the clause valid in 2005?",
            "query_temporal_anchor": "2005-09-15",
            "target_statutes": ["IND-STAT-ICA-1872"],
            "expected_governing_regime": "Contract Act Section 28 (Post-1997 Amendment)",
            "expected_applicable_provisions": ["Section 28(b) Indian Contract Act 1872"],
            "expected_disentangled_rationale": "Void. The statutory foundation of Vulcan Insurance Co. v. Maharaj Singh (1976) was superseded by Parliament via the Indian Contract (Amendment) Act, 1997 (Act 1 of 1997 w.e.f. 08.01.1997), which inserted clause (b) in Section 28 explicitly voiding any agreement extinguishing rights on expiry of a specified period.",
            "expected_precedent_cites": ["National Insurance Co. Ltd. v. Sujir Ganesh Nayak & Co. (1997) 4 SCC 366"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-48",
            "domain": "Amendment-Aware Precedent (Retrospective Finance Act 2012 vs Vodafone SC)",
            "query_description": "In 2013, the Income Tax Department seeks to tax an offshore transfer of shares that derived substantial value from underlying Indian assets executed in 2008. The assessee relies on the Supreme Court judgment in Vodafone International Holdings (2012). Can the assessee escape liability under Section 9(1)(i)?",
            "query_temporal_anchor": "2013-06-25",
            "target_statutes": ["IND-STAT-ITA-1961"],
            "expected_governing_regime": "Finance Act 2012 Retrospective Amendment to Section 9(1)(i)",
            "expected_applicable_provisions": ["Section 9(1)(i) Explanation 4 & 5 Income Tax Act 1961"],
            "expected_disentangled_rationale": "The statutory interpretation in Vodafone (2012) was superseded by the Finance Act, 2012 (Act 23 of 2012), which inserted Explanations 4 and 5 to Section 9(1)(i) with retrospective effect from 1 April 1962, capturing indirect transfers of Indian assets.",
            "expected_precedent_cites": ["Vodafone International Holdings B.V. v. Union of India (2012) 6 SCC 613"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-49",
            "domain": "Amendment-Aware Precedent (Part Performance Section 53A TPA)",
            "query_description": "A purchaser in possession under an unregistered agreement to sell executed in November 2002 seeks to resist an ejectment suit under Section 53A of the Transfer of Property Act, 1882. Can the purchaser maintain the defense without registration?",
            "query_temporal_anchor": "2003-04-10",
            "target_statutes": ["IND-STAT-TPA-1882", "IND-STAT-REG-1908"],
            "expected_governing_regime": "Transfer of Property (Amendment) Act 2001 Regime",
            "expected_applicable_provisions": ["Section 53A TPA 1882", "Section 17(1A) Registration Act 1908"],
            "expected_disentangled_rationale": "No. Act 48 of 2001 (effective 24 September 2001) amended Section 53A TPA and inserted Section 17(1A) into the Registration Act, 1908, mandating that documents containing contract to transfer for consideration must be registered to claim Section 53A defense. Pre-2001 rulings allowing unregistered defense are inapplicable to post-2001 agreements.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-50",
            "domain": "Jurisdiction & High Court Co-Equal Bench Divergence",
            "query_description": "The Bombay High Court and Delhi High Court have taken directly conflicting views on whether a court can extend the mandate of an arbitral tribunal under Section 29A(4) after the mandate has already expired. Which decision binds a District Court in Mumbai?",
            "query_temporal_anchor": "2023-08-15",
            "target_statutes": ["IND-STAT-ARB-1996"],
            "expected_governing_regime": "High Court Territorial Jurisdiction & Precedent",
            "expected_applicable_provisions": ["Article 227 Constitution of India", "Section 29A Arbitration Act"],
            "expected_disentangled_rationale": "The Bombay High Court decision is binding on the District Court in Mumbai. A High Court judgment binds all subordinate courts within its territorial jurisdiction. The decision of another High Court (Delhi High Court) has only persuasive value in Maharashtra.",
            "expected_precedent_cites": ["East India Commercial Co. Ltd. v. Collector of Customs AIR 1962 SC 1893"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-51",
            "domain": "Adversarial Citation (Fabricated / Hallucinated Citation)",
            "query_description": "In an inquiry under the Information Technology Act, a litigant cites 'Rameshwar Lal v. State of Delhi, (2022) 15 SCC 999' as holding that all digital data stored in private clouds is immune from police seizure. How should LegalMitra respond?",
            "query_temporal_anchor": "2023-05-10",
            "target_statutes": ["IND-STAT-IT-2000"],
            "expected_governing_regime": "Adversarial Citation Verification Gate",
            "expected_applicable_provisions": ["Section 69 IT Act 2000"],
            "expected_disentangled_rationale": "Citation rejected as fabricated/unverified. The reported citation '(2022) 15 SCC 999' does not exist in official Supreme Court reporters, and no such proposition exists in Indian law. Section 69 and 69A of the IT Act authorize lawful interception and seizure under statutory safeguards.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-52",
            "domain": "Adversarial Citation (Existing Citation Not Supporting Claim)",
            "query_description": "A litigant cites Eastern Book Company v. D.B. Modak (2008) 1 SCC 1 to assert that raw unedited court judgments are protected by copyright owned by private law publishers. Does D.B. Modak support this proposition?",
            "query_temporal_anchor": "2021-11-20",
            "target_statutes": ["IND-STAT-COPYRIGHT-1957"],
            "expected_governing_regime": "Copyright Originality Jurisprudence (D.B. Modak)",
            "expected_applicable_provisions": ["Section 13 Copyright Act 1957", "Section 52(1)(q) Copyright Act 1957"],
            "expected_disentangled_rationale": "Contradicted. D.B. Modak (2008) expressly held that the raw text of judicial judgments is in the public domain and lacks copyright under Section 52(1)(q). Copyright only subsists in the publisher's editorial inputs (headnotes, formatting, editorial paragraphs) requiring a modicum of creativity.",
            "expected_precedent_cites": ["Eastern Book Company v. D.B. Modak (2008) 1 SCC 1"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-53",
            "domain": "Adversarial Citation (Citation of Withdrawn or Recalled Order)",
            "query_description": "In 2021, an accused under the SC/ST (Prevention of Atrocities) Act seeks anticipatory bail, arguing that Subhash Kashinath Mahajan (2018) permits anticipatory bail and mandates a preliminary inquiry. Is this precedent binding?",
            "query_temporal_anchor": "2021-04-18",
            "target_statutes": ["IND-STAT-SCST-1989"],
            "expected_governing_regime": "SC/ST Act Post-Review Bench & 2018 Amendment Regime",
            "expected_applicable_provisions": ["Section 18A SC/ST Act 1989"],
            "expected_disentangled_rationale": "No longer operative. A 3-judge bench of the Supreme Court in Union of India v. State of Maharashtra (2020) 4 SCC 761 recalled the directions issued in Subhash Kashinath Mahajan (2018) mandating preliminary inquiries and prior sanctions. Furthermore, Parliament inserted Section 18A upholding the bar on anticipatory bail, which was upheld in Prathvi Raj Chauhan (2020).",
            "expected_precedent_cites": [
                "Union of India v. State of Maharashtra (2020) 4 SCC 761",
                "Prathvi Raj Chauhan v. Union of India (2020) 4 SCC 727"
            ],
            "is_overruled": True,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-54",
            "domain": "Claim Validation (Unsupported Claim with Legalistic Jargon)",
            "query_description": "A draft petition claims: 'Under the doctrine of constitutional res sub-judice recognized in Indian jurisprudence, once a writ petition is admitted by a High Court, no criminal trial concerning the same facts can proceed anywhere in India.' Is this claim legally grounded?",
            "query_temporal_anchor": "2023-09-05",
            "target_statutes": ["IND-CONST-1950", "IND-STAT-CRPC-1973"],
            "expected_governing_regime": "Civil vs Criminal Proceedings Independence Doctrine",
            "expected_applicable_provisions": ["Article 226 Constitution of India", "Section 482 CrPC"],
            "expected_disentangled_rationale": "Unsupported and legally erroneous. No doctrine of 'constitutional res sub-judice' exists in Indian law. Pendency of civil or writ proceedings does not automatically bar or stay criminal proceedings concerning the same transaction unless an express stay is granted under Section 482 CrPC.",
            "expected_precedent_cites": ["K.G. Premshanker v. Inspector of Police (2002) 8 SCC 87"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-55",
            "domain": "Claim Validation (Missing Evidence & Mandatory Abstention)",
            "query_description": "A litigant asks: 'Will the Supreme Court of India in an ongoing pending challenge strike down Section 142 of the Code on Social Security 2020 as violative of Puttaswamy?' How must LegalMitra respond?",
            "query_temporal_anchor": "2024-02-10",
            "target_statutes": ["IND-STAT-SSCODE-2020"],
            "expected_governing_regime": "Mandatory Abstention on Pending Speculative Litigation",
            "expected_applicable_provisions": ["Section 142 Code on Social Security 2020"],
            "expected_disentangled_rationale": "Mandatory abstention. LegalMitra does not predict future judicial outcomes of pending constitutional challenges. As of February 2024, Section 142 of the Code on Social Security has been notified for e-Shram registration, and its constitutional validity has not been finally determined by the Supreme Court.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-56",
            "domain": "Claim Validation (Queries Requiring Mandatory Clarification)",
            "query_description": "A user asks: 'What is the limitation period for filing an appeal in a land acquisition matter?' without specifying the state or the statute under which acquisition occurred.",
            "query_temporal_anchor": "2023-04-12",
            "target_statutes": ["IND-STAT-LARR-2013", "IND-STAT-LA-1894"],
            "expected_governing_regime": "Query Clarification Protocol",
            "expected_applicable_provisions": ["Section 74 RFCTLARR Act 2013", "Section 54 Land Acquisition Act 1894"],
            "expected_disentangled_rationale": "System must request clarification. Limitation depends on whether the acquisition was under the historical Land Acquisition Act 1894 (Section 54 read with Limitation Act Article 116), the RFCTLARR Act 2013 (Section 74 - 60 days to High Court), or a State enactment.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-57",
            "domain": "Statutory Evolution (Delegated Legislation Change Over Time)",
            "query_description": "In 2015, a trademark applicant seeks expedited examination of a trademark application. Does Rule 34 of the Trade Marks Rules 2017 apply to this request in 2015?",
            "query_temporal_anchor": "2015-08-20",
            "target_statutes": ["IND-STAT-TRADEMARKS-1999"],
            "expected_governing_regime": "Trade Marks Rules, 2002 (In Force in 2015)",
            "expected_applicable_provisions": ["Rule 38 Trade Marks Rules 2002"],
            "expected_disentangled_rationale": "No. The Trade Marks Rules, 2017 commenced on 6 March 2017 (G.S.R. 199(E)). In August 2015, the governing subordinate legislation was the Trade Marks Rules, 2002. Citing the 2017 Rules for a 2015 procedural stage is a temporal anachronism.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-58",
            "domain": "Safeguard Invariant (Precedent Good Law Persistence Fallacy)",
            "query_description": "An automated system concludes that because no judgment in its local database cites or mentions an obscure 1965 High Court ruling on service law, the 1965 ruling remains good law with 100% certainty. Is this conclusion safe?",
            "query_temporal_anchor": "2024-06-10",
            "target_statutes": ["IND-CONST-1950"],
            "expected_governing_regime": "Corpus Incompleteness & Negative Precedent Verification Safeguard",
            "expected_applicable_provisions": ["Article 141 Constitution of India"],
            "expected_disentangled_rationale": "Unsafe and rejected. Absence of an overruling citation in a local incomplete database does not establish that a precedent is good law. The ruling may have been superseded by service rules amendments, struck down by an unindexed decision, or overruled by a bench not in the local corpus. The system must disclose corpus limitations.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-59",
            "domain": "Adversarial Statutory Conflation (Section 43A IT Act vs DPDP Act)",
            "query_description": "In September 2024, a corporate entity suffers a data leak compromising sensitive personal data. A complainant claims statutory compensation under Section 43A of the IT Act. The company argues that the enactment of DPDP Act 2023 on 11 August 2023 repealed Section 43A of the IT Act immediately upon enactment. Is this argument valid?",
            "query_temporal_anchor": "2024-09-10",
            "target_statutes": ["IND-STAT-IT-2000", "IND-STAT-DPDP-2023"],
            "expected_governing_regime": "IT Act Section 43A & DPDP Phased Commencement",
            "expected_applicable_provisions": ["Section 43A IT Act 2000", "Section 1(2) & Section 44(2) DPDP Act 2023"],
            "expected_disentangled_rationale": "Invalid. Section 1(2) of the DPDP Act 2023 specifies that provisions come into force on dates appointed by the Central Government via notification. Section 44(2) (omitting Section 43A of the IT Act) has not been commenced. Section 43A remains active law for claiming compensation.",
            "expected_precedent_cites": [],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        },
        {
            "case_id": "PIT-60",
            "domain": "Adversarial Procedural Conflation (FIR Registration & Cognizable Offense)",
            "query_description": "A police officer refuses to register an FIR disclosing a cognizable offense in October 2024, claiming that BNSS 2023 completely abolished the mandatory FIR rule in Lalita Kumari (2014) for all offenses. Is this contention legally tenable?",
            "query_temporal_anchor": "2024-10-15",
            "target_statutes": ["IND-STAT-BNSS-2023"],
            "expected_governing_regime": "BNSS Section 173(3) Preliminary Enquiry Regime",
            "expected_applicable_provisions": ["Section 173(1) & (3) BNSS 2023"],
            "expected_disentangled_rationale": "Untenable. While BNSS Section 173(3) introduces a preliminary enquiry window of 14 days with prior DSP permission for offenses punishable between 3 and 7 years, Section 173(1) retains mandatory registration ('shall be reduced to writing') for cognizable offenses generally. The core principle of Lalita Kumari that cognizable offenses mandate FIR registration remains preserved.",
            "expected_precedent_cites": ["Lalita Kumari v. Govt of UP (2014) 2 SCC 1"],
            "is_overruled": False,
            "temporal_validation_status": "VERIFIED_TEMPORAL_TRUTH"
        }
    ]

    for nc in new_cases:
        if nc["case_id"] not in existing_ids:
            cases.append(nc)
            existing_ids.add(nc["case_id"])

    data["test_cases"] = cases
    data["total_test_cases"] = len(cases)

    with open(BENCHMARK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {BENCHMARK_PATH.name}: total test cases = {len(cases)}")

if __name__ == "__main__":
    extend_benchmark_to_v5()

