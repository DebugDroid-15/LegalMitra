"""LegalMitra Judicial Knowledge Infrastructure — Multi-Axis Case Classification System.

Implements a 14-domain taxonomy covering substantive and procedural classifications:
1. Constitutional & Administrative Law
2. Criminal Law & Criminal Procedure
3. Civil Law, Property, Equity & Contract
4. Family, Succession & Matrimonial Law
5. Commercial, Corporate, Insolvency & Arbitration
6. Labour, Employment & Service Jurisprudence
7. Land Acquisition, Tenancy & Agrarian Reforms
8. Environmental, Forest & Wildlife Protection
9. Technology, Intellectual Property, Cyber Law & Privacy
10. Direct & Indirect Taxation, Customs & GST
11. Education, Public Health & Utilities
12. Election Law & Democratic Governance
13. Human Rights & Custodial Justice
14. Transnational, Admiralty & International Law
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class SubstantiveDomain(str, Enum):
    CONSTITUTIONAL_ADMINISTRATIVE = "CONSTITUTIONAL_ADMINISTRATIVE"
    CRIMINAL = "CRIMINAL"
    CIVIL_PROPERTY_CONTRACT = "CIVIL_PROPERTY_CONTRACT"
    FAMILY_SUCCESSION = "FAMILY_SUCCESSION"
    COMMERCIAL_CORPORATE_INSOLVENCY = "COMMERCIAL_CORPORATE_INSOLVENCY"
    LABOUR_SERVICE = "LABOUR_SERVICE"
    LAND_TENANCY_AGRARIAN = "LAND_TENANCY_AGRARIAN"
    ENVIRONMENTAL_FOREST = "ENVIRONMENTAL_FOREST"
    TECHNOLOGY_IP_PRIVACY = "TECHNOLOGY_IP_PRIVACY"
    TAXATION_CUSTOMS_GST = "TAXATION_CUSTOMS_GST"
    EDUCATION_HEALTH = "EDUCATION_HEALTH"
    ELECTION_GOVERNANCE = "ELECTION_GOVERNANCE"
    HUMAN_RIGHTS_CUSTODIAL = "HUMAN_RIGHTS_CUSTODIAL"
    TRANSNATIONAL_ADMIRALTY = "TRANSNATIONAL_ADMIRALTY"


class ProceduralPosture(str, Enum):
    BAIL_APPLICATION = "BAIL_APPLICATION"
    ANTICIPATORY_BAIL = "ANTICIPATORY_BAIL"
    WRIT_PETITION_ARTICLE_32 = "WRIT_PETITION_ARTICLE_32"
    WRIT_PETITION_ARTICLE_226 = "WRIT_PETITION_ARTICLE_226"
    SPECIAL_LEAVE_PETITION_CIVIL = "SPECIAL_LEAVE_PETITION_CIVIL"
    SPECIAL_LEAVE_PETITION_CRIMINAL = "SPECIAL_LEAVE_PETITION_CRIMINAL"
    CIVIL_APPEAL = "CIVIL_APPEAL"
    CRIMINAL_APPEAL = "CRIMINAL_APPEAL"
    SECTION_482_QUASHING = "SECTION_482_QUASHING"
    REVISION_PETITION = "REVISION_PETITION"
    REVIEW_PETITION = "REVIEW_PETITION"
    CURATIVE_PETITION = "CURATIVE_PETITION"
    ORIGINAL_SUIT = "ORIGINAL_SUIT"
    ARBITRATION_PETITION = "ARBITRATION_PETITION"
    COMPANY_PETITION_IBC = "COMPANY_PETITION_IBC"
    STATUTORY_APPEAL_TRIBUNAL = "STATUTORY_APPEAL_TRIBUNAL"
    INTERLOCUTORY_APPLICATION = "INTERLOCUTORY_APPLICATION"
    MISCELLANEOUS = "MISCELLANEOUS"


@dataclass
class DomainDefinition:
    domain: SubstantiveDomain
    name: str
    description: str
    primary_statutes: List[str]
    characteristic_keywords: List[str]
    typical_postures: List[ProceduralPosture]


class CaseTaxonomyManager:
    """Manages multi-axis legal case taxonomy and rule-based classification."""

    def __init__(self) -> None:
        self._domains: Dict[SubstantiveDomain, DomainDefinition] = {}
        self._populate_domain_definitions()

    def get_domain(self, domain: SubstantiveDomain) -> Optional[DomainDefinition]:
        return self._domains.get(domain)

    def list_all_domains(self) -> List[DomainDefinition]:
        return list(self._domains.values())

    def classify_text(self, text: str) -> Dict[str, Any]:
        """Classify judicial text into primary/secondary domains and procedural posture."""
        text_lower = text.lower()

        scores: Dict[SubstantiveDomain, int] = {}
        for domain, defn in self._domains.items():
            score = 0
            for kw in defn.characteristic_keywords:
                if kw.lower() in text_lower:
                    score += 1
            for stat in defn.primary_statutes:
                if stat.lower() in text_lower:
                    score += 2
            scores[domain] = score

        sorted_domains = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        primary_domain = sorted_domains[0][0] if sorted_domains and sorted_domains[0][1] > 0 else SubstantiveDomain.CONSTITUTIONAL_ADMINISTRATIVE
        secondary_domain = sorted_domains[1][0] if len(sorted_domains) > 1 and sorted_domains[1][1] > 0 else None

        detected_posture = self._detect_posture(text_lower)

        return {
            "primary_domain": primary_domain.value,
            "secondary_domain": secondary_domain.value if secondary_domain else None,
            "domain_confidence_score": sorted_domains[0][1] if sorted_domains else 0,
            "procedural_posture": detected_posture.value,
        }

    def _detect_posture(self, text_lower: str) -> ProceduralPosture:
        if "anticipatory bail" in text_lower or "section 438" in text_lower:
            return ProceduralPosture.ANTICIPATORY_BAIL
        if "regular bail" in text_lower or "section 439" in text_lower or "bail application" in text_lower:
            return ProceduralPosture.BAIL_APPLICATION
        if "section 482" in text_lower or "quashing" in text_lower:
            return ProceduralPosture.SECTION_482_QUASHING
        if "article 32" in text_lower or "writ petition (civil) no." in text_lower:
            return ProceduralPosture.WRIT_PETITION_ARTICLE_32
        if "article 226" in text_lower:
            return ProceduralPosture.WRIT_PETITION_ARTICLE_226
        if "special leave petition (criminal)" in text_lower or "slp (crl)" in text_lower:
            return ProceduralPosture.SPECIAL_LEAVE_PETITION_CRIMINAL
        if "special leave petition (civil)" in text_lower or "slp (c)" in text_lower:
            return ProceduralPosture.SPECIAL_LEAVE_PETITION_CIVIL
        if "curative petition" in text_lower:
            return ProceduralPosture.CURATIVE_PETITION
        if "review petition" in text_lower:
            return ProceduralPosture.REVIEW_PETITION
        if "arbitration petition" in text_lower or "section 11" in text_lower or "section 34" in text_lower:
            return ProceduralPosture.ARBITRATION_PETITION
        if "insolvency" in text_lower or "corporate insolvency" in text_lower or "section 7 ibc" in text_lower:
            return ProceduralPosture.COMPANY_PETITION_IBC
        if "criminal appeal" in text_lower:
            return ProceduralPosture.CRIMINAL_APPEAL
        if "civil appeal" in text_lower:
            return ProceduralPosture.CIVIL_APPEAL
        return ProceduralPosture.MISCELLANEOUS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_domains": len(self._domains),
            "domains": {
                dom.value: {
                    "name": defn.name,
                    "description": defn.description,
                    "primary_statutes": defn.primary_statutes,
                    "characteristic_keywords": defn.characteristic_keywords,
                    "typical_postures": [p.value for p in defn.typical_postures],
                }
                for dom, defn in self._domains.items()
            },
        }

    def _populate_domain_definitions(self) -> None:
        self._domains[SubstantiveDomain.CONSTITUTIONAL_ADMINISTRATIVE] = DomainDefinition(
            domain=SubstantiveDomain.CONSTITUTIONAL_ADMINISTRATIVE,
            name="Constitutional & Administrative Law",
            description="Fundamental rights, judicial review, separation of powers, executive actions, doctrine of basic structure.",
            primary_statutes=["Constitution of India"],
            characteristic_keywords=["fundamental rights", "article 14", "article 19", "article 21", "article 32", "article 226", "basic structure", "ultra vires", "mandamus", "certiorari", "habeas corpus"],
            typical_postures=[ProceduralPosture.WRIT_PETITION_ARTICLE_32, ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.CIVIL_APPEAL],
        )

        self._domains[SubstantiveDomain.CRIMINAL] = DomainDefinition(
            domain=SubstantiveDomain.CRIMINAL,
            name="Criminal Law & Procedure",
            description="Substantive offences, investigations, trials, evidence, sentencing, and bail jurisprudence.",
            primary_statutes=["Indian Penal Code 1860", "Bharatiya Nyaya Sanhita 2023", "Code of Criminal Procedure 1973", "Bharatiya Nagarik Suraksha Sanhita 2023", "Indian Evidence Act 1872", "Bharatiya Sakshya Adhiniyam 2023", "POCSO Act 2012", "NDPS Act 1985"],
            characteristic_keywords=["bail", "charge sheet", "fir", "cognizable", "murder", "theft", "section 302", "section 376", "section 420", "mens rea", "acquittal", "conviction", "sentence"],
            typical_postures=[ProceduralPosture.BAIL_APPLICATION, ProceduralPosture.ANTICIPATORY_BAIL, ProceduralPosture.CRIMINAL_APPEAL, ProceduralPosture.SPECIAL_LEAVE_PETITION_CRIMINAL, ProceduralPosture.SECTION_482_QUASHING],
        )

        self._domains[SubstantiveDomain.CIVIL_PROPERTY_CONTRACT] = DomainDefinition(
            domain=SubstantiveDomain.CIVIL_PROPERTY_CONTRACT,
            name="Civil Law, Property, Equity & Contract",
            description="Contracts, specific performance, property transfer, torts, injunctions, and declaratory relief.",
            primary_statutes=["Code of Civil Procedure 1908", "Indian Contract Act 1872", "Transfer of Property Act 1882", "Specific Relief Act 1963", "Limitation Act 1963"],
            characteristic_keywords=["breach of contract", "damages", "title suit", "injunction", "partition suit", "conveyance", "easement", "specific performance"],
            typical_postures=[ProceduralPosture.ORIGINAL_SUIT, ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.SPECIAL_LEAVE_PETITION_CIVIL, ProceduralPosture.REVISION_PETITION],
        )

        self._domains[SubstantiveDomain.FAMILY_SUCCESSION] = DomainDefinition(
            domain=SubstantiveDomain.FAMILY_SUCCESSION,
            name="Family, Succession & Matrimonial Law",
            description="Marriage, divorce, maintenance, custody, adoption, and testamentary and intestate succession.",
            primary_statutes=["Hindu Marriage Act 1955", "Hindu Succession Act 1956", "Special Marriage Act 1954", "Muslim Personal Law (Shariat) Application Act 1937", "Guardians and Wards Act 1890", "Indian Succession Act 1925"],
            characteristic_keywords=["divorce", "alimony", "maintenance", "custody of child", "restitution of conjugal rights", "coparcenary", "ancestral property", "will", "probate"],
            typical_postures=[ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.SPECIAL_LEAVE_PETITION_CIVIL, ProceduralPosture.WRIT_PETITION_ARTICLE_226],
        )

        self._domains[SubstantiveDomain.COMMERCIAL_CORPORATE_INSOLVENCY] = DomainDefinition(
            domain=SubstantiveDomain.COMMERCIAL_CORPORATE_INSOLVENCY,
            name="Commercial, Corporate, Insolvency & Arbitration",
            description="Company law, corporate governance, corporate insolvency resolution, domestic and international arbitration, negotiable instruments.",
            primary_statutes=["Companies Act 2013", "Insolvency and Bankruptcy Code 2016", "Arbitration and Conciliation Act 1996", "Commercial Courts Act 2015", "Negotiable Instruments Act 1881"],
            characteristic_keywords=["cirp", "resolution plan", "operational creditor", "financial creditor", "arbitral tribunal", "section 138", "cheque bounce", "corporate debtor", "winding up"],
            typical_postures=[ProceduralPosture.COMPANY_PETITION_IBC, ProceduralPosture.ARBITRATION_PETITION, ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.STATUTORY_APPEAL_TRIBUNAL],
        )

        self._domains[SubstantiveDomain.LABOUR_SERVICE] = DomainDefinition(
            domain=SubstantiveDomain.LABOUR_SERVICE,
            name="Labour, Employment & Service Jurisprudence",
            description="Industrial disputes, retrenchment, disciplinary proceedings, government service rules, pensions, and promotions.",
            primary_statutes=["Industrial Disputes Act 1947", "Administrative Tribunals Act 1985", "Payment of Gratuity Act 1972", "Employees Provident Funds Act 1952", "Industrial Relations Code 2020"],
            characteristic_keywords=["reinstatement", "retrenchment", "back wages", "departmental inquiry", "disciplinary proceedings", "seniority", "promotion", "pension", "charge memo"],
            typical_postures=[ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.STATUTORY_APPEAL_TRIBUNAL, ProceduralPosture.CIVIL_APPEAL],
        )

        self._domains[SubstantiveDomain.LAND_TENANCY_AGRARIAN] = DomainDefinition(
            domain=SubstantiveDomain.LAND_TENANCY_AGRARIAN,
            name="Land Acquisition, Tenancy & Agrarian Reforms",
            description="Compulsory land acquisition, rehabilitation and resettlement, agricultural land ceiling, rent control and eviction.",
            primary_statutes=["Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act 2013", "Land Acquisition Act 1894", "State Rent Control Acts"],
            characteristic_keywords=["land acquisition", "compensation", "rehabilitation", "solatium", "fair market value", "eviction", "standard rent", "tenant"],
            typical_postures=[ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.SPECIAL_LEAVE_PETITION_CIVIL],
        )

        self._domains[SubstantiveDomain.ENVIRONMENTAL_FOREST] = DomainDefinition(
            domain=SubstantiveDomain.ENVIRONMENTAL_FOREST,
            name="Environmental, Forest & Wildlife Protection",
            description="Pollution control, forest conservation, wildlife protection, precautionary principle, polluter pays doctrine, sustainable development.",
            primary_statutes=["Environment (Protection) Act 1986", "National Green Tribunal Act 2010", "Forest (Conservation) Act 1980", "Wildlife (Protection) Act 1972", "Water (Prevention and Control of Pollution) Act 1974", "Air Act 1981"],
            characteristic_keywords=["environmental clearance", "ngt", "polluter pays", "precautionary principle", "forest land", "air pollution", "water pollution", "ecological damage", "crz"],
            typical_postures=[ProceduralPosture.STATUTORY_APPEAL_TRIBUNAL, ProceduralPosture.WRIT_PETITION_ARTICLE_32, ProceduralPosture.CIVIL_APPEAL],
        )

        self._domains[SubstantiveDomain.TECHNOLOGY_IP_PRIVACY] = DomainDefinition(
            domain=SubstantiveDomain.TECHNOLOGY_IP_PRIVACY,
            name="Technology, Intellectual Property, Cyber Law & Privacy",
            description="Patents, trademarks, copyright, trade secrets, data privacy, intermediary liability, cybercrimes.",
            primary_statutes=["Information Technology Act 2000", "Digital Personal Data Protection Act 2023", "Trade Marks Act 1999", "Copyright Act 1957", "Patents Act 1970"],
            characteristic_keywords=["trademark infringement", "patent revocation", "copyright infringement", "passing off", "data protection", "privacy", "intermediary liability", "section 66a", "cybercrime"],
            typical_postures=[ProceduralPosture.ORIGINAL_SUIT, ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.WRIT_PETITION_ARTICLE_226],
        )

        self._domains[SubstantiveDomain.TAXATION_CUSTOMS_GST] = DomainDefinition(
            domain=SubstantiveDomain.TAXATION_CUSTOMS_GST,
            name="Direct & Indirect Taxation, Customs & GST",
            description="Income tax, corporate tax, transfer pricing, goods and services tax, customs duties, excise.",
            primary_statutes=["Income Tax Act 1961", "Central Goods and Services Tax Act 2017", "Customs Act 1962", "Central Excise Act 1944"],
            characteristic_keywords=["assessment order", "reassessment", "search and seizure", "itc", "input tax credit", "customs duty", "classification", "transfer pricing", "escaped assessment"],
            typical_postures=[ProceduralPosture.STATUTORY_APPEAL_TRIBUNAL, ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.WRIT_PETITION_ARTICLE_226],
        )

        self._domains[SubstantiveDomain.EDUCATION_HEALTH] = DomainDefinition(
            domain=SubstantiveDomain.EDUCATION_HEALTH,
            name="Education, Public Health & Utilities",
            description="Admissions, university governance, affirmative action in education, medical negligence, healthcare regulations, public utilities.",
            primary_statutes=["Right of Children to Free and Compulsory Education Act 2009", "National Medical Commission Act 2019", "University Grants Commission Act 1956", "Consumer Protection Act 2019 (Medical Negligence)"],
            characteristic_keywords=["neet", "admission quota", "capitation fee", "medical negligence", "affiliation", "examination cancellation", "consumer forum medical", "public utility"],
            typical_postures=[ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.WRIT_PETITION_ARTICLE_32, ProceduralPosture.CIVIL_APPEAL],
        )

        self._domains[SubstantiveDomain.ELECTION_GOVERNANCE] = DomainDefinition(
            domain=SubstantiveDomain.ELECTION_GOVERNANCE,
            name="Election Law & Democratic Governance",
            description="Representation of the People, corrupt practices, disqualification, delimitation, municipal and panchayat elections.",
            primary_statutes=["Representation of the People Act 1951", "Conduct of Elections Rules 1961", "Delimitation Act 2002"],
            characteristic_keywords=["election petition", "corrupt practice", "disqualification of mla", "disqualification of mp", "model code of conduct", "nomination rejection", "voter verification"],
            typical_postures=[ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.WRIT_PETITION_ARTICLE_32],
        )

        self._domains[SubstantiveDomain.HUMAN_RIGHTS_CUSTODIAL] = DomainDefinition(
            domain=SubstantiveDomain.HUMAN_RIGHTS_CUSTODIAL,
            name="Human Rights & Custodial Justice",
            description="Custodial death, encounter killings, illegal detention, prisoners' rights, compensation for state atrocities, NHRC/SHRC proceedings.",
            primary_statutes=["Protection of Human Rights Act 1993", "Constitution of India (Articles 20, 21, 22)"],
            characteristic_keywords=["custodial violence", "custodial death", "encounter", "illegal detention", "handcuffing", "compensation under public law", "prisoners rights", "solitary confinement"],
            typical_postures=[ProceduralPosture.WRIT_PETITION_ARTICLE_32, ProceduralPosture.WRIT_PETITION_ARTICLE_226, ProceduralPosture.CIVIL_APPEAL],
        )

        self._domains[SubstantiveDomain.TRANSNATIONAL_ADMIRALTY] = DomainDefinition(
            domain=SubstantiveDomain.TRANSNATIONAL_ADMIRALTY,
            name="Transnational, Admiralty & International Law",
            description="Admiralty jurisdiction, ship arrest, extradition, sovereign immunity, cross-border insolvencies, enforcement of foreign judgments.",
            primary_statutes=["Admiralty (Jurisdiction and Settlement of Maritime Claims) Act 2017", "Extradition Act 1962", "Code of Civil Procedure 1908 (Section 44A)"],
            characteristic_keywords=["admiralty suit", "ship arrest", "maritime lien", "extradition", "foreign decree", "letters of request", "sovereign immunity", "cross-border"],
            typical_postures=[ProceduralPosture.ORIGINAL_SUIT, ProceduralPosture.CIVIL_APPEAL, ProceduralPosture.WRIT_PETITION_ARTICLE_226],
        )
