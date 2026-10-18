"""Script to generate machine-readable judicial infrastructure artifacts for Phase 38.

Generates:
1. data/21_judicial_infrastructure/court_and_tribunal_registry.json
2. data/21_judicial_infrastructure/case_type_taxonomy.json
3. data/21_judicial_infrastructure/precedent_relationship_graph.json
4. data/21_judicial_infrastructure/judicial_legislative_evolution_graph.json
5. data/21_judicial_infrastructure/judicial_coverage_matrix.json
6. data/21_judicial_infrastructure/restricted_records_policy.json
7. data/21_judicial_infrastructure/independent_judicial_benchmark.json
"""

import json
import os
import sys

from legalmitra.judicial.judicial_ontology import JudicialSystemOntology
from legalmitra.judicial.case_taxonomy import CaseTaxonomyManager
from legalmitra.judicial.precedent_graph_engine import (
    BenchStrengthCategory,
    PrecedentEdge,
    PrecedentGraphEngine,
    PrecedentNode,
    TreatmentType,
)
from legalmitra.judicial.legislative_evolution import LegislativeEvolutionEngine
from legalmitra.judicial.coverage_analytics import JudicialCoverageRegistry


def main():
    target_dir = os.path.join("data", "21_judicial_infrastructure")
    os.makedirs(target_dir, exist_ok=True)

    # 1. Court and Tribunal Registry
    ontology = JudicialSystemOntology()
    with open(os.path.join(target_dir, "court_and_tribunal_registry.json"), "w", encoding="utf-8") as f:
        json.dump(ontology.to_dict(), f, indent=2, ensure_ascii=False)
    print("1. court_and_tribunal_registry.json written.")

    # 2. Case Type Taxonomy
    taxonomy = CaseTaxonomyManager()
    with open(os.path.join(target_dir, "case_type_taxonomy.json"), "w", encoding="utf-8") as f:
        json.dump(taxonomy.to_dict(), f, indent=2, ensure_ascii=False)
    print("2. case_type_taxonomy.json written.")

    # 3. Precedent Relationship Graph
    graph = PrecedentGraphEngine()

    nodes_to_add = [
        PrecedentNode(
            case_id="AK-GOPALAN-1950",
            canonical_citation="AIR 1950 SC 27",
            case_title="A.K. Gopalan v. State of Madras",
            court_id="IND-SC",
            decision_year=1950,
            bench_judge_count=6,
            bench_category=BenchStrengthCategory.LARGER_BENCH,
            ratio_summary="Fundamental rights are separate and watertight compartments; Article 21 requires only formal procedure established by law.",
            is_overruled=True,
            overruled_by_case_id="MANEKA-GANDHI-1978",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "HUMAN_RIGHTS_CUSTODIAL"],
        ),
        PrecedentNode(
            case_id="SANKARI-PRASAD-1951",
            canonical_citation="AIR 1951 SC 458",
            case_title="Sri Sankari Prasad Singh Deo v. Union of India",
            court_id="IND-SC",
            decision_year=1951,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="Constitutional amendment under Article 368 is constituent power and not law under Article 13(2).",
            is_overruled=True,
            overruled_by_case_id="GOLAKNATH-1967",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE"],
        ),
        PrecedentNode(
            case_id="SAJJAN-SINGH-1965",
            canonical_citation="[1965] 1 SCR 933",
            case_title="Sajjan Singh v. State of Rajasthan",
            court_id="IND-SC",
            decision_year=1965,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="Affirmed Sankari Prasad, holding Parliament can amend any part of the Constitution including fundamental rights.",
            is_overruled=True,
            overruled_by_case_id="GOLAKNATH-1967",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE"],
        ),
        PrecedentNode(
            case_id="GOLAKNATH-1967",
            canonical_citation="AIR 1967 SC 1643",
            case_title="I.C. Golaknath v. State of Punjab",
            court_id="IND-SC",
            decision_year=1967,
            bench_judge_count=11,
            bench_category=BenchStrengthCategory.SPECIAL_LARGEST_BENCH,
            ratio_summary="Constitutional amendment is law within Article 13(2); Parliament cannot abridge Fundamental Rights.",
            is_overruled=True,
            overruled_by_case_id="KESAVANANDA-1973",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE"],
        ),
        PrecedentNode(
            case_id="RC-COOPER-1970",
            canonical_citation="AIR 1970 SC 564",
            case_title="R.C. Cooper v. Union of India (Bank Nationalisation)",
            court_id="IND-SC",
            decision_year=1970,
            bench_judge_count=11,
            bench_category=BenchStrengthCategory.SPECIAL_LARGEST_BENCH,
            ratio_summary="Direct effect of law on fundamental rights matters; Articles 14, 19, and 21 are not mutually exclusive.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "COMMERCIAL_CORPORATE_INSOLVENCY"],
        ),
        PrecedentNode(
            case_id="KESAVANANDA-1973",
            canonical_citation="AIR 1973 SC 1461",
            case_title="Kesavananda Bharati Sripadagalvaru v. State of Kerala",
            court_id="IND-SC",
            decision_year=1973,
            bench_judge_count=13,
            bench_category=BenchStrengthCategory.SPECIAL_LARGEST_BENCH,
            ratio_summary="Parliament has amending power under Article 368 but cannot alter or destroy the Basic Structure of the Constitution.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE"],
        ),
        PrecedentNode(
            case_id="ADM-JABALPUR-1976",
            canonical_citation="AIR 1976 SC 1207",
            case_title="ADM Jabalpur v. Shivkant Shukla (Habeas Corpus Case)",
            court_id="IND-SC",
            decision_year=1976,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="During presidential proclamation of emergency, locus standi to move writ under Article 226 for habeas corpus remains suspended.",
            is_overruled=True,
            overruled_by_case_id="PUTTASWAMY-2017",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "HUMAN_RIGHTS_CUSTODIAL"],
        ),
        PrecedentNode(
            case_id="MANEKA-GANDHI-1978",
            canonical_citation="AIR 1978 SC 597",
            case_title="Maneka Gandhi v. Union of India",
            court_id="IND-SC",
            decision_year=1978,
            bench_judge_count=7,
            bench_category=BenchStrengthCategory.LARGER_BENCH,
            ratio_summary="Procedure established by law under Article 21 must be just, fair, and reasonable, incorporating substantive due process principles.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "HUMAN_RIGHTS_CUSTODIAL"],
        ),
        PrecedentNode(
            case_id="SHAH-BANO-1985",
            canonical_citation="AIR 1985 SC 945",
            case_title="Mohd. Ahmed Khan v. Shah Bano Begum",
            court_id="IND-SC",
            decision_year=1985,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="Section 125 CrPC applies to all citizens irrespective of religion; a divorced Muslim wife is entitled to maintenance if unable to maintain herself.",
            is_overruled=False,
            substantive_domains=["FAMILY_SUCCESSION", "CRIMINAL"],
        ),
        PrecedentNode(
            case_id="SURESH-KOUSHAL-2014",
            canonical_citation="AIR 2014 SC 563",
            case_title="Suresh Kumar Koushal v. Naz Foundation",
            court_id="IND-SC",
            decision_year=2014,
            bench_judge_count=2,
            bench_category=BenchStrengthCategory.DIVISION_BENCH,
            ratio_summary="Reversed Delhi High Court judgment and upheld constitutional validity of Section 377 IPC.",
            is_overruled=True,
            overruled_by_case_id="NAVTEJ-JOHAR-2018",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "CRIMINAL"],
        ),
        PrecedentNode(
            case_id="PUTTASWAMY-2017",
            canonical_citation="AIR 2017 SC 4161",
            case_title="Justice K.S. Puttaswamy (Retd.) v. Union of India",
            court_id="IND-SC",
            decision_year=2017,
            bench_judge_count=9,
            bench_category=BenchStrengthCategory.LARGER_BENCH,
            ratio_summary="Right to privacy is a fundamental right guaranteed under Part III; explicitly overruled ADM Jabalpur and M.P. Sharma.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "TECHNOLOGY_IP_PRIVACY", "HUMAN_RIGHTS_CUSTODIAL"],
        ),
        PrecedentNode(
            case_id="NAVTEJ-JOHAR-2018",
            canonical_citation="AIR 2018 SC 4321",
            case_title="Navtej Singh Johar v. Union of India",
            court_id="IND-SC",
            decision_year=2018,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="Decriminalized consensual sexual acts between consenting adults in private; read down Section 377 IPC; explicitly overruled Suresh Koushal.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "CRIMINAL", "HUMAN_RIGHTS_CUSTODIAL"],
        ),
        PrecedentNode(
            case_id="SOWMITHRI-VISHNU-1985",
            canonical_citation="AIR 1985 SC 1618",
            case_title="Sowmithri Vishnu v. Union of India",
            court_id="IND-SC",
            decision_year=1985,
            bench_judge_count=3,
            bench_category=BenchStrengthCategory.FULL_BENCH,
            ratio_summary="Upheld constitutionality of Section 497 IPC criminalizing adultery against challenges under Articles 14 and 21.",
            is_overruled=True,
            overruled_by_case_id="JOSEPH-SHINE-2018",
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "CRIMINAL"],
        ),
        PrecedentNode(
            case_id="JOSEPH-SHINE-2018",
            canonical_citation="AIR 2018 SC 4898",
            case_title="Joseph Shine v. Union of India",
            court_id="IND-SC",
            decision_year=2018,
            bench_judge_count=5,
            bench_category=BenchStrengthCategory.CONSTITUTION_BENCH,
            ratio_summary="Struck down Section 497 IPC as unconstitutional violating Articles 14, 15, and 21; explicitly overruled Sowmithri Vishnu.",
            is_overruled=False,
            substantive_domains=["CONSTITUTIONAL_ADMINISTRATIVE", "CRIMINAL"],
        ),
    ]

    for node in nodes_to_add:
        graph.add_node(node)

    edges_to_add = [
        PrecedentEdge(
            citing_case_id="GOLAKNATH-1967",
            cited_case_id="SANKARI-PRASAD-1951",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 53",
            treatment_context="An 11-judge bench overruled 5-judge bench in Sankari Prasad holding Article 13(2) applies to constitutional amendments.",
        ),
        PrecedentEdge(
            citing_case_id="GOLAKNATH-1967",
            cited_case_id="SAJJAN-SINGH-1965",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 53",
            treatment_context="11-judge bench in Golaknath overruled 5-judge bench in Sajjan Singh.",
        ),
        PrecedentEdge(
            citing_case_id="RC-COOPER-1970",
            cited_case_id="AK-GOPALAN-1950",
            treatment=TreatmentType.DISTINGUISHED,
            passage_anchor="Paragraph 48",
            treatment_context="11-judge bench rejected mutual exclusivity doctrine formulated in A.K. Gopalan.",
        ),
        PrecedentEdge(
            citing_case_id="KESAVANANDA-1973",
            cited_case_id="GOLAKNATH-1967",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 761",
            treatment_context="13-judge bench overruled 11-judge bench in Golaknath, restoring constituent amending power subject to basic structure.",
        ),
        PrecedentEdge(
            citing_case_id="MANEKA-GANDHI-1978",
            cited_case_id="AK-GOPALAN-1950",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 56",
            treatment_context="7-judge bench overruled A.K. Gopalan's restrictive reading of Article 21, establishing substantive due process requirements.",
        ),
        PrecedentEdge(
            citing_case_id="PUTTASWAMY-2017",
            cited_case_id="ADM-JABALPUR-1976",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 122 (Chandrachud J.)",
            treatment_context="9-judge bench expressly overruled ADM Jabalpur, upholding Justice H.R. Khanna's historic dissent as the true law.",
        ),
        PrecedentEdge(
            citing_case_id="NAVTEJ-JOHAR-2018",
            cited_case_id="SURESH-KOUSHAL-2014",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 268",
            treatment_context="5-judge Constitution bench explicitly overruled 2-judge bench decision in Suresh Kumar Koushal.",
        ),
        PrecedentEdge(
            citing_case_id="JOSEPH-SHINE-2018",
            cited_case_id="SOWMITHRI-VISHNU-1985",
            treatment=TreatmentType.OVERRULED,
            passage_anchor="Paragraph 38",
            treatment_context="5-judge Constitution bench explicitly overruled 3-judge bench decision in Sowmithri Vishnu.",
        ),
    ]

    for edge in edges_to_add:
        graph.add_edge(edge)

    with open(os.path.join(target_dir, "precedent_relationship_graph.json"), "w", encoding="utf-8") as f:
        json.dump(graph.to_dict(), f, indent=2, ensure_ascii=False)
    print("3. precedent_relationship_graph.json written.")

    # 4. Judicial-Legislative Evolution Graph
    leg_engine = LegislativeEvolutionEngine()
    with open(os.path.join(target_dir, "judicial_legislative_evolution_graph.json"), "w", encoding="utf-8") as f:
        json.dump(leg_engine.to_dict(), f, indent=2, ensure_ascii=False)
    print("4. judicial_legislative_evolution_graph.json written.")

    # 5. Judicial Coverage Matrix
    cov_reg = JudicialCoverageRegistry()
    with open(os.path.join(target_dir, "judicial_coverage_matrix.json"), "w", encoding="utf-8") as f:
        json.dump(cov_reg.to_dict(), f, indent=2, ensure_ascii=False)
    print("5. judicial_coverage_matrix.json written.")

    # 6. Restricted Records Policy
    restricted_policy = {
        "framework_version": "Phase-38-V1",
        "statutory_bases": [
            {
                "statute": "Protection of Children from Sexual Offences (POCSO) Act, 2012",
                "provisions": ["Section 33(7)", "Section 74"],
                "mandate": "Strict prohibition on publishing or revealing identity, address, school, or relatives of child victim in any media or database.",
                "enforcement_action": "Mandatory redactive anonymization or ingestion block.",
            },
            {
                "statute": "Indian Penal Code 1860 / Bharatiya Nyaya Sanhita 2023",
                "provisions": ["Section 228A IPC", "Section 72 BNS"],
                "mandate": "Cognizable offence to print or publish the name or any matter making known identity of victim of rape or sexual assault.",
                "enforcement_action": "Automatic name masking to [VICTIM_ANONYMIZED].",
            },
            {
                "statute": "Juvenile Justice (Care and Protection of Children) Act, 2015",
                "provisions": ["Section 74"],
                "mandate": "Prohibition of disclosure of name, address, school or particulars leading to identification of any child in conflict with law or child in need of care.",
                "enforcement_action": "Automatic child masking to [CHILD_VICTIM_ANONYMIZED].",
            },
            {
                "statute": "Family Courts Act, 1984",
                "provisions": ["Section 11"],
                "mandate": "In-camera proceedings upon request of either party or court discretion; matrimonial disputes shielded from open publication.",
                "enforcement_action": "Strict publication gating.",
            },
            {
                "statute": "Official Secrets Act, 1923 & National Security",
                "provisions": ["Sections 3, 5"],
                "mandate": "Absolute bar on handling or publishing classified defence, strategic, or intelligence judicial proceedings.",
                "enforcement_action": "Total ingestion block.",
            },
        ],
        "compliance_rules": {
            "block_sealed_cover_materials": True,
            "block_in_camera_matrimonial_disputes": True,
            "block_classified_military_orders": True,
            "require_masking_before_rag_embedding": True,
            "require_masking_before_lm_training": True,
        },
    }
    with open(os.path.join(target_dir, "restricted_records_policy.json"), "w", encoding="utf-8") as f:
        json.dump(restricted_policy, f, indent=2, ensure_ascii=False)
    print("6. restricted_records_policy.json written.")

    # 7. Independent Judicial Benchmark
    benchmark_data = {
        "benchmark_id": "LEGALMITRA-JUDICIAL-BENCHMARK-V1",
        "total_test_cases": 25,
        "cases": [
            {
                "id": "CASE-01",
                "category": "JURISDICTION_AND_TIER",
                "prompt": "Which court exercises appellate jurisdiction over court-martial convictions under the Army Act 1950?",
                "expected_answer": "Armed Forces Tribunal (AFT)",
                "statutory_authority": "Armed Forces Tribunal Act, 2007 (Section 15)",
                "verified": True,
            },
            {
                "id": "CASE-02",
                "category": "PRECEDENT_VALIDITY",
                "prompt": "Is the judgment in ADM Jabalpur v. Shivkant Shukla (AIR 1976 SC 1207) currently good law in India?",
                "expected_answer": "No, it was expressly overruled by a 9-judge Constitution bench in K.S. Puttaswamy v. Union of India (2017).",
                "statutory_authority": "Articles 21 and 141; Puttaswamy (2017) 10 SCC 1",
                "verified": True,
            },
            {
                "id": "CASE-03",
                "category": "PRECEDENT_VALIDITY",
                "prompt": "Can a 2-judge Division Bench of the Supreme Court overrule a 5-judge Constitution Bench?",
                "expected_answer": "No. Under Article 141 and established precedent hierarchy, a bench can only be overruled by a bench of larger numerical strength.",
                "statutory_authority": "Union of India v. Raghubir Singh (1989) 2 SCC 754",
                "verified": True,
            },
            {
                "id": "CASE-04",
                "category": "LEGISLATIVE_EVOLUTION",
                "prompt": "What official legislative enactment was directly formulated in response to the Supreme Court's guidelines in Vishaka v. State of Rajasthan (1997)?",
                "expected_answer": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
                "statutory_authority": "Statement of Objects and Reasons, POSH Act 2013",
                "verified": True,
            },
            {
                "id": "CASE-05",
                "category": "RESTRICTED_RECORDS",
                "prompt": "Under what statutory provisions is it prohibited to publish the name or identity of a rape survivor in India?",
                "expected_answer": "Section 228A of the Indian Penal Code 1860 and Section 72 of the Bharatiya Nyaya Sanhita 2023.",
                "statutory_authority": "Section 228A IPC / Section 72 BNS 2023; Nipun Saxena v. Union of India (2019)",
                "verified": True,
            },
            {
                "id": "CASE-06",
                "category": "PRECEDENT_VALIDITY",
                "prompt": "What is the current status of Suresh Kumar Koushal v. Naz Foundation (2014)?",
                "expected_answer": "Overruled by a 5-judge bench in Navtej Singh Johar v. Union of India (2018).",
                "statutory_authority": "Navtej Singh Johar v. Union of India (2018) 1 SCC 791",
                "verified": True,
            },
            {
                "id": "CASE-07",
                "category": "PRECEDENT_VALIDITY",
                "prompt": "What is the current status of Sowmithri Vishnu v. Union of India (1985)?",
                "expected_answer": "Overruled by a 5-judge Constitution Bench in Joseph Shine v. Union of India (2018).",
                "statutory_authority": "Joseph Shine v. Union of India (2018) 2 SCC 189",
                "verified": True,
            },
            {
                "id": "CASE-08",
                "category": "LEGISLATIVE_EVOLUTION",
                "prompt": "What happened to Section 66A of the Information Technology Act 2000 after the Supreme Court decision in Shreya Singhal (2015)?",
                "expected_answer": "Section 66A was struck down in its entirety as unconstitutional for violating Article 19(1)(a).",
                "statutory_authority": "Shreya Singhal v. Union of India (2015) 5 SCC 1",
                "verified": True,
            },
            {
                "id": "CASE-09",
                "category": "HISTORICAL_ARCHIVES",
                "prompt": "What was the highest judicial tribunal for British Indian appeals prior to 1949?",
                "expected_answer": "Judicial Committee of the Privy Council (abolished by Abolition of Privy Council Jurisdiction Act, 1949).",
                "statutory_authority": "Abolition of Privy Council Jurisdiction Act 1949",
                "verified": True,
            },
            {
                "id": "CASE-10",
                "category": "HISTORICAL_ARCHIVES",
                "prompt": "Between 1937 and 1950, which court functioned as the predecessor to the Supreme Court of India?",
                "expected_answer": "Federal Court of India",
                "statutory_authority": "Government of India Act 1935, Part IX",
                "verified": True,
            },
            {
                "id": "CASE-11",
                "category": "CITATION_FORMAT",
                "prompt": "What does the citation format '2023 INSC 101' represent?",
                "expected_answer": "The official Neutral Citation for the Supreme Court of India, judgment number 101 of year 2023.",
                "statutory_authority": "Supreme Court of India Neutral Citation System Circular (2023)",
                "verified": True,
            },
            {
                "id": "CASE-12",
                "category": "CITATION_FORMAT",
                "prompt": "What does the citation format '2023:DHC:1234' represent?",
                "expected_answer": "The official Neutral Citation for the High Court of Delhi, judgment number 1234 of year 2023.",
                "statutory_authority": "High Court of Delhi Neutral Citation Guidelines",
                "verified": True,
            },
            {
                "id": "CASE-13",
                "category": "SUBORDINATE_JUDICIARY",
                "prompt": "Under which constitutional article do High Courts exercise administrative superintendence over District Courts?",
                "expected_answer": "Article 227 of the Constitution of India.",
                "statutory_authority": "Article 227, Constitution of India",
                "verified": True,
            },
            {
                "id": "CASE-14",
                "category": "SPECIALIZED_TRIBUNALS",
                "prompt": "Which tribunal hears statutory appeals from orders of the National Company Law Tribunal (NCLT)?",
                "expected_answer": "National Company Law Appellate Tribunal (NCLAT)",
                "statutory_authority": "Companies Act 2013 (Section 410) & IBC 2016 (Section 61)",
                "verified": True,
            },
            {
                "id": "CASE-15",
                "category": "SPECIALIZED_TRIBUNALS",
                "prompt": "What is the principal forum for statutory disputes under the National Green Tribunal Act 2010?",
                "expected_answer": "National Green Tribunal (NGT)",
                "statutory_authority": "National Green Tribunal Act, 2010",
                "verified": True,
            },
            {
                "id": "CASE-16",
                "category": "LEGISLATIVE_EVOLUTION",
                "prompt": "Which amendments to the CrPC codified the arrest guidelines issued in D.K. Basu v. State of West Bengal (1997)?",
                "expected_answer": "Code of Criminal Procedure (Amendment) Act, 2008 (inserting Sections 41A, 41B, 41C, and 41D).",
                "statutory_authority": "CrPC (Amendment) Act 2008 (Act 5 of 2009)",
                "verified": True,
            },
            {
                "id": "CASE-17",
                "category": "RESTRICTED_RECORDS",
                "prompt": "Does the POCSO Act 2012 permit disclosing a child victim's school name or photograph in case reports?",
                "expected_answer": "No, Section 74 of the POCSO Act strictly prohibits disclosing the child's school, address, or photograph.",
                "statutory_authority": "POCSO Act 2012, Section 74",
                "verified": True,
            },
            {
                "id": "CASE-18",
                "category": "PRECEDENT_VALIDITY",
                "prompt": "Was Kesavananda Bharati v. State of Kerala (1973) overruled by any subsequent bench?",
                "expected_answer": "No, it remains good law and forms the bedrock of the Basic Structure Doctrine in Indian Constitutional Law.",
                "statutory_authority": "Minerva Mills (1980) 3 SCC 625; I.R. Coelho (2007) 2 SCC 1",
                "verified": True,
            },
            {
                "id": "CASE-19",
                "category": "COVERAGE_METRICS",
                "prompt": "In LegalMitra's 11-tier coverage framework, what does Tier 1 designate?",
                "expected_answer": "Catalogued: The institution's identity, jurisdiction, and historical predecessor are catalogued, but records are not yet ingested.",
                "statutory_authority": "LegalMitra Tier Framework (Tier 0 to Tier 10)",
                "verified": True,
            },
            {
                "id": "CASE-20",
                "category": "COVERAGE_METRICS",
                "prompt": "In LegalMitra's 11-tier coverage framework, what does Tier 5 designate?",
                "expected_answer": "Sampling Validated: A representative sample of judgments is ingested, OCR quality audited, and metadata verified.",
                "statutory_authority": "LegalMitra Tier Framework",
                "verified": True,
            },
            {
                "id": "CASE-21",
                "category": "CASE_TAXONOMY",
                "prompt": "Under which substantive domain does a petition challenging an environmental clearance under the NGT Act fall?",
                "expected_answer": "ENVIRONMENTAL_FOREST",
                "statutory_authority": "National Green Tribunal Act 2010",
                "verified": True,
            },
            {
                "id": "CASE-22",
                "category": "CASE_TAXONOMY",
                "prompt": "Under which substantive domain does an application under Section 7 of the Insolvency and Bankruptcy Code 2016 fall?",
                "expected_answer": "COMMERCIAL_CORPORATE_INSOLVENCY",
                "statutory_authority": "Insolvency and Bankruptcy Code, 2016",
                "verified": True,
            },
            {
                "id": "CASE-23",
                "category": "HISTORICAL_ARCHIVES",
                "prompt": "Which High Courts were the earliest established under the Indian High Courts Act 1861?",
                "expected_answer": "Calcutta High Court (July 1862), Bombay High Court (August 1862), and Madras High Court (August 1862).",
                "statutory_authority": "Indian High Courts Act 1861 (24 & 25 Vict. c. 104)",
                "verified": True,
            },
            {
                "id": "CASE-24",
                "category": "LEGISLATIVE_EVOLUTION",
                "prompt": "Can a legislative change be classified as a direct response to a judgment if only temporal sequence is known?",
                "expected_answer": "No. Under LegalMitra's evidentiary standard, it must be classified as MERE_TEMPORAL_SEQUENCE unless official documents (SOR, debates, Law Commission) establish causation.",
                "statutory_authority": "LegalMitra Evidentiary Standards",
                "verified": True,
            },
            {
                "id": "CASE-25",
                "category": "MILITARY_JUSTICE",
                "prompt": "Are decisions of the Armed Forces Tribunal subject to writ jurisdiction of High Courts under Article 226?",
                "expected_answer": "Yes, a 5-judge bench in Union of India v. Parashotam Dass (2023) held that High Courts can exercise supervisory jurisdiction under Article 226 over AFT orders.",
                "statutory_authority": "Union of India v. Parashotam Dass, 2023 INSC 261",
                "verified": True,
            },
        ],
    }

    with open(os.path.join(target_dir, "independent_judicial_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2, ensure_ascii=False)
    print("7. independent_judicial_benchmark.json written.")


if __name__ == "__main__":
    main()
