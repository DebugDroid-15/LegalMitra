"""
LegalMitra Comprehensive Indian Legal Taxonomy Engine
Provides machine-readable hierarchy, multi-topic classification, jurisdiction separation,
and search term normalization across Central, State, and Judicial domains.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class TaxonomyNode:
    code: str
    name: str
    description: str
    parent_code: Optional[str] = None
    jurisdiction_scope: str = "ALL"  # "CENTRAL", "STATE", "ALL"
    aliases: List[str] = field(default_factory=list)
    key_statutes: List[str] = field(default_factory=list)
    search_keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaxonomyNode:
        return cls(**data)


class LegalTaxonomyManager:
    """Manages the hierarchical taxonomy tree for Indian law."""

    VERSION = "1.0.0"

    def __init__(self, nodes: Optional[List[TaxonomyNode]] = None):
        self._nodes: Dict[str, TaxonomyNode] = {}
        self._children: Dict[str, List[str]] = {}
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node: TaxonomyNode) -> None:
        self._nodes[node.code] = node
        if node.parent_code:
            self._children.setdefault(node.parent_code, []).append(node.code)

    def get_node(self, code: str) -> Optional[TaxonomyNode]:
        return self._nodes.get(code)

    def list_nodes(self) -> List[TaxonomyNode]:
        return list(self._nodes.values())

    def get_children(self, parent_code: str) -> List[TaxonomyNode]:
        child_codes = self._children.get(parent_code, [])
        return [self._nodes[c] for c in child_codes if c in self._nodes]

    def get_root_nodes(self) -> List[TaxonomyNode]:
        return [n for n in self._nodes.values() if not n.parent_code]

    def search_by_keyword(self, keyword: str) -> List[TaxonomyNode]:
        kw = keyword.lower()
        results: List[TaxonomyNode] = []
        for node in self._nodes.values():
            if (
                kw in node.name.lower()
                or kw in node.description.lower()
                or any(kw in alias.lower() for alias in node.aliases)
                or any(kw in statute.lower() for statute in node.key_statutes)
                or any(kw in term.lower() for term in node.search_keywords)
            ):
                results.append(node)
        return results

    def classify_text(self, text: str) -> List[str]:
        """Returns matching taxonomy codes for a given legal passage or question."""
        text_lower = text.lower()
        matched_codes: Set[str] = set()
        for node in self._nodes.values():
            for kw in node.search_keywords:
                if kw.lower() in text_lower:
                    matched_codes.add(node.code)
                    break
        return sorted(list(matched_codes))

    def export_json(self, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": self.VERSION,
            "total_nodes": len(self._nodes),
            "domains": [node.to_dict() for node in self._nodes.values() if not node.parent_code],
            "all_nodes": [node.to_dict() for node in self._nodes.values()],
        }
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_json(cls, source_path: Path) -> LegalTaxonomyManager:
        with open(source_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        nodes_data = payload.get("all_nodes", [])
        nodes = [TaxonomyNode.from_dict(d) for d in nodes_data]
        return cls(nodes)


def build_default_indian_legal_taxonomy() -> LegalTaxonomyManager:
    """Builds the comprehensive 8-domain Indian legal taxonomy tree."""
    mgr = LegalTaxonomyManager()

    # =========================================================================
    # DOMAIN 1: CONSTITUTIONAL & PUBLIC LAW
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-CONST",
        name="Constitutional & Public Law",
        description="The Constitution of India, fundamental rights, constitutional remedies, federal relations, and administrative review.",
        jurisdiction_scope="CENTRAL",
        aliases=["Constitutional Law", "Public Law", "Samvidhan"],
        key_statutes=["The Constitution of India"],
        search_keywords=["constitution", "fundamental rights", "article 21", "article 14", "article 19", "article 32", "article 226", "basic structure", "writ"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CONST-FR",
        name="Fundamental Rights & Remedies",
        description="Part III of the Constitution (Articles 12-35), equality, freedoms, personal liberty, and writ jurisdiction (Articles 32 and 226).",
        parent_code="TAX-CONST",
        jurisdiction_scope="CENTRAL",
        aliases=["Part III", "Fundamental Rights", "Writ Jurisdiction"],
        key_statutes=["The Constitution of India (Articles 12-35, 32, 226)"],
        search_keywords=["equality before law", "freedom of speech", "personal liberty", "habeas corpus", "mandamus", "certiorari", "quo warranto", "prohibition", "due process"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CONST-FED",
        name="Federalism & Legislative Powers",
        description="Union-State relations, Seventh Schedule (Union, State, Concurrent Lists), Article 356, and federal governance.",
        parent_code="TAX-CONST",
        jurisdiction_scope="ALL",
        aliases=["Federal Relations", "Seventh Schedule", "President's Rule"],
        key_statutes=["The Constitution of India (Articles 245-255, 356, Seventh Schedule)"],
        search_keywords=["seventh schedule", "union list", "state list", "concurrent list", "presidents rule", "article 356", "floor test", "pith and substance"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CONST-ADMIN",
        name="Administrative Law & Judicial Review",
        description="Principles of natural justice, delegated legislation review, administrative discretion, and tribunals.",
        parent_code="TAX-CONST",
        jurisdiction_scope="ALL",
        aliases=["Administrative Law", "Judicial Review"],
        key_statutes=["Administrative Tribunals Act, 1985"],
        search_keywords=["natural justice", "audi alteram partem", "ultra vires", "proportionality", "administrative tribunal", "CAT"]
    ))

    # =========================================================================
    # DOMAIN 2: CRIMINAL LAW & PROCEDURE
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-CRIM",
        name="Criminal Law & Procedure",
        description="Substantive criminal codes, criminal procedure, evidence law, investigations, bail, trial, and special criminal statutes.",
        jurisdiction_scope="ALL",
        aliases=["Criminal Law", "Penal Law", "Criminal Justice"],
        key_statutes=["Bharatiya Nyaya Sanhita, 2023", "Bharatiya Nagarik Suraksha Sanhita, 2023", "Bharatiya Sakshya Adhiniyam, 2023", "Indian Penal Code, 1860", "Code of Criminal Procedure, 1973", "Indian Evidence Act, 1872"],
        search_keywords=["criminal", "penal", "bns", "bnss", "bsa", "ipc", "crpc", "evidence", "fir", "bail", "investigation"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CRIM-SUB",
        name="Substantive Penal Law",
        description="Offences against the state, human body, property, public tranquility, women, children, and organized crime under BNS 2023 and IPC 1860.",
        parent_code="TAX-CRIM",
        jurisdiction_scope="CENTRAL",
        aliases=["Penal Offences", "BNS", "IPC"],
        key_statutes=["Bharatiya Nyaya Sanhita, 2023", "Indian Penal Code, 1860"],
        search_keywords=["murder", "culpable homicide", "theft", "extortion", "cheating", "criminal breach of trust", "organized crime", "terrorist act", "snatching", "mob lynching"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CRIM-PROC",
        name="Criminal Procedure & Investigation",
        description="Arrest, search, seizure, custody, FIR, charge-sheet, bail, trial, sentencing, and appeals under BNSS 2023 and CrPC 1973.",
        parent_code="TAX-CRIM",
        jurisdiction_scope="CENTRAL",
        aliases=["Criminal Procedure", "BNSS", "CrPC"],
        key_statutes=["Bharatiya Nagarik Suraksha Sanhita, 2023", "Code of Criminal Procedure, 1973"],
        search_keywords=["section 482", "anticipatory bail", "regular bail", "default bail", "remand", "zero fir", "charge sheet", "cognizable", "non-cognizable", "section 531 savings"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CRIM-EVID",
        name="Evidence & Electronic Proof",
        description="Law of evidence, primary and secondary proof, digital evidence, electronic certificates under BSA 2023 s.63 and IEA 1872 s.65B.",
        parent_code="TAX-CRIM",
        jurisdiction_scope="CENTRAL",
        aliases=["Evidence Law", "Electronic Evidence", "BSA", "IEA"],
        key_statutes=["Bharatiya Sakshya Adhiniyam, 2023", "Indian Evidence Act, 1872"],
        search_keywords=["electronic record", "section 63 certificate", "section 65b", "primary evidence", "secondary evidence", "hash value", "digital signature", "burden of proof"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CRIM-SPEC",
        name="Special Criminal Statutes",
        description="Specialized penal statutes including POCSO, NDPS, PMLA, Prevention of Corruption Act, and UAPA.",
        parent_code="TAX-CRIM",
        jurisdiction_scope="CENTRAL",
        aliases=["Special Acts", "POCSO", "NDPS", "PMLA"],
        key_statutes=["Protection of Children from Sexual Offences Act, 2012", "Narcotic Drugs and Psychotropic Substances Act, 1985", "Prevention of Money Laundering Act, 2002", "Prevention of Corruption Act, 1988"],
        search_keywords=["pocso", "penetrative sexual assault", "ndps", "commercial quantity", "pmla", "twin bail conditions", "scheduled offence", "enforcement directorate"]
    ))

    # =========================================================================
    # DOMAIN 3: CIVIL JUSTICE & DISPUTE RESOLUTION
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL",
        name="Civil Justice & Dispute Resolution",
        description="Civil procedure, limitation periods, contract law, specific relief, property, succession, family law, and arbitration.",
        jurisdiction_scope="ALL",
        aliases=["Civil Law", "Civil Litigation", "Private Law"],
        key_statutes=["Code of Civil Procedure, 1908", "Limitation Act, 1963", "Indian Contract Act, 1872", "Specific Relief Act, 1963", "Arbitration and Conciliation Act, 1996"],
        search_keywords=["civil suit", "cpc", "injunction", "specific performance", "limitation", "contract", "arbitration", "res judicata"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL-PROC",
        name="Civil Procedure & Execution",
        description="Institution of suits, pleadings, discovery, Order 39 temporary injunctions, execution of decrees, appeals, and revision.",
        parent_code="TAX-CIVIL",
        jurisdiction_scope="CENTRAL",
        aliases=["CPC", "Civil Court Procedure"],
        key_statutes=["Code of Civil Procedure, 1908"],
        search_keywords=["plaint", "written statement", "order 39", "temporary injunction", "execution of decree", "section 100", "second appeal", "section 115 revision", "res judicata"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL-LIMIT",
        name="Limitation & Condonation",
        description="Statutory limitation periods for suits, appeals, and applications, Section 5 condonation of delay, and legal disability.",
        parent_code="TAX-CIVIL",
        jurisdiction_scope="CENTRAL",
        aliases=["Limitation Law"],
        key_statutes=["The Limitation Act, 1963"],
        search_keywords=["limitation period", "section 5 condonation", "sufficient cause", "prescribed period", "acknowledgment in writing", "statute barred"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL-CONT",
        name="Contract & Specific Relief",
        description="Formation of contracts, consideration, breach, damages under Section 73/74, mandatory specific performance, and substituted performance.",
        parent_code="TAX-CIVIL",
        jurisdiction_scope="CENTRAL",
        aliases=["Contract Law", "Specific Relief"],
        key_statutes=["Indian Contract Act, 1872", "Specific Relief Act, 1963"],
        search_keywords=["offer and acceptance", "consideration", "breach of contract", "liquidated damages", "specific performance", "substituted performance", "section 20a infrastructure bar"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL-ADR",
        name="Arbitration & ADR",
        description="Domestic and international commercial arbitration, Section 9 interim relief, Section 11 arbitrator appointment, Section 34 setting aside awards, and mediation.",
        parent_code="TAX-CIVIL",
        jurisdiction_scope="CENTRAL",
        aliases=["Arbitration", "Mediation", "ADR"],
        key_statutes=["Arbitration and Conciliation Act, 1996", "Mediation Act, 2023"],
        search_keywords=["arbitration agreement", "section 9 interim relief", "section 11 appointment", "section 34 setting aside", "patent illegality", "mediation act"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-CIVIL-PROP",
        name="Property, Transfer & Registration",
        description="Transfer of Property Act, registration of documents, sale, mortgage, lease, gift, easements, and succession.",
        parent_code="TAX-CIVIL",
        jurisdiction_scope="ALL",
        aliases=["Property Law", "Transfer of Property"],
        key_statutes=["Transfer of Property Act, 1882", "Registration Act, 1908", "Indian Succession Act, 1925"],
        search_keywords=["sale deed", "mortgage", "lease", "gift deed", "registration section 17", "succession", "probate", "letters of administration"]
    ))

    # =========================================================================
    # DOMAIN 4: BUSINESS, CORPORATE & ECONOMIC LAW
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-BIZ",
        name="Business, Corporate & Economic Law",
        description="Company law, corporate insolvency, banking, direct and indirect taxation, competition, securities, and consumer protection.",
        jurisdiction_scope="CENTRAL",
        aliases=["Corporate Law", "Commercial Law", "Economic Law"],
        key_statutes=["Companies Act, 2013", "Insolvency and Bankruptcy Code, 2016", "Consumer Protection Act, 2019", "Competition Act, 2002", "Income Tax Act, 1961", "Central Goods and Services Tax Act, 2017"],
        search_keywords=["corporate", "company", "ibc", "insolvency", "taxation", "gst", "consumer", "sebi", "competition commission"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-BIZ-CORP",
        name="Companies & Corporate Governance",
        description="Incorporation, board meetings, director duties, oppression and mismanagement, NCLT jurisdiction, and corporate compliance.",
        parent_code="TAX-BIZ",
        jurisdiction_scope="CENTRAL",
        aliases=["Company Law", "Corporate Governance"],
        key_statutes=["Companies Act, 2013"],
        search_keywords=["incorporation", "board of directors", "fiduciary duty", "oppression and mismanagement", "section 241", "nclt", "nclat", "csr"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-BIZ-IBC",
        name="Insolvency & Bankruptcy (IBC)",
        description="Corporate Insolvency Resolution Process (CIRP), Section 7 financial creditor, Section 9 operational creditor, Section 14 moratorium, and liquidation.",
        parent_code="TAX-BIZ",
        jurisdiction_scope="CENTRAL",
        aliases=["IBC", "Insolvency"],
        key_statutes=["Insolvency and Bankruptcy Code, 2016"],
        search_keywords=["cirp", "financial creditor", "operational creditor", "moratorium section 14", "resolution plan", "committee of creditors", "coc", "insolvency professional"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-BIZ-CONS",
        name="Consumer Protection & E-Commerce",
        description="Consumer rights, unfair trade practices, deficiency in service, product liability, Central Consumer Protection Authority (CCPA), and Consumer Commissions.",
        parent_code="TAX-BIZ",
        jurisdiction_scope="ALL",
        aliases=["Consumer Law", "Consumer Protection"],
        key_statutes=["Consumer Protection Act, 2019"],
        search_keywords=["consumer complaint", "deficiency of service", "unfair trade practice", "product liability", "district commission", "state commission", "ncdrc", "e-commerce rules"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-BIZ-TAX",
        name="Taxation (Direct & Indirect / GST)",
        description="Income Tax, corporate tax, assessment, appeals, ITAT, Goods and Services Tax (CGST, SGST, IGST), input tax credit, and advance rulings.",
        parent_code="TAX-BIZ",
        jurisdiction_scope="ALL",
        aliases=["Tax Law", "GST", "Income Tax"],
        key_statutes=["Income Tax Act, 1961", "Central Goods and Services Tax Act, 2017"],
        search_keywords=["income tax", "gst", "input tax credit", "cgst", "sgst", "igst", "assessment", "itat", "tax evasion", "advance ruling"]
    ))

    # =========================================================================
    # DOMAIN 5: EMPLOYMENT, LABOUR & SOCIAL PROTECTION
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-LABOUR",
        name="Employment, Labour & Social Protection",
        description="Labour codes, wages, industrial relations, social security, occupational safety, POSH workplace protections, and welfare.",
        jurisdiction_scope="ALL",
        aliases=["Labour Law", "Employment Law", "Industrial Law"],
        key_statutes=["Code on Wages, 2019", "Industrial Relations Code, 2020", "Code on Social Security, 2020", "Occupational Safety, Health and Working Conditions Code, 2020", "POSH Act, 2013", "Industrial Disputes Act, 1947"],
        search_keywords=["labour", "employment", "wages", "industrial dispute", "gratuity", "provident fund", "posh", "workplace harassment", "social security"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-LABOUR-POSH",
        name="Prevention of Workplace Harassment (POSH)",
        description="Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013, Internal Complaints Committee (ICC), inquiry procedure, and employer liability.",
        parent_code="TAX-LABOUR",
        jurisdiction_scope="ALL",
        aliases=["POSH Act", "Workplace Harassment"],
        key_statutes=["Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013"],
        search_keywords=["posh act", "internal committee", "icc", "workplace harassment", "local committee", "inquiry report", "vishaka guidelines"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-LABOUR-WAGES",
        name="Wages, Benefits & Social Security",
        description="Minimum wages, overtime, payment of bonus, gratuity, Employees Provident Fund (EPF), Employees State Insurance (ESI), and unorganized workers.",
        parent_code="TAX-LABOUR",
        jurisdiction_scope="ALL",
        aliases=["Wages Law", "Social Security"],
        key_statutes=["Code on Wages, 2019", "Code on Social Security, 2020", "Payment of Gratuity Act, 1972", "Employees' Provident Funds and Miscellaneous Provisions Act, 1952"],
        search_keywords=["minimum wages", "gratuity", "epf", "esi", "bonus", "severance", "social security code"]
    ))

    # =========================================================================
    # DOMAIN 6: TECHNOLOGY & EMERGING REGULATION
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-TECH",
        name="Technology & Emerging Regulation",
        description="Data protection and privacy (DPDP Act), information technology, intermediary guidelines, digital governance, telecommunications, and cyber law.",
        jurisdiction_scope="CENTRAL",
        aliases=["Cyber Law", "Tech Law", "Digital Law"],
        key_statutes=["Digital Personal Data Protection Act, 2023", "Information Technology Act, 2000", "Telecommunications Act, 2023"],
        search_keywords=["data protection", "dpdp", "privacy", "cyber security", "intermediary liability", "it act", "telecommunications", "data fiduciary"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-TECH-DPDP",
        name="Data Protection & Privacy (DPDP)",
        description="Digital Personal Data Protection Act, 2023, data fiduciary obligations, data principal rights, consent managers, Data Protection Board of India, and cross-border transfer.",
        parent_code="TAX-TECH",
        jurisdiction_scope="CENTRAL",
        aliases=["DPDP Act", "Data Protection Law"],
        key_statutes=["Digital Personal Data Protection Act, 2023"],
        search_keywords=["dpdp act", "data principal", "data fiduciary", "significant data fiduciary", "consent manager", "data protection board", "right to erasure", "phased commencement"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-TECH-CYBER",
        name="Cybercrime & Intermediary Regulation",
        description="Offences under the IT Act, Section 66, Section 67, Section 79 safe harbor for intermediaries, IT Rules 2021, digital forensics, and electronic intercept.",
        parent_code="TAX-TECH",
        jurisdiction_scope="CENTRAL",
        aliases=["Cybercrime Law", "IT Rules"],
        key_statutes=["Information Technology Act, 2000", "Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021"],
        search_keywords=["section 79 safe harbour", "intermediary due diligence", "section 66 cyber crime", "hacking", "identity theft", "grievance appellate committee"]
    ))

    # =========================================================================
    # DOMAIN 7: ENVIRONMENT, LAND & INFRASTRUCTURE
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-ENV",
        name="Environment, Land & Infrastructure",
        description="Environmental protection, forests, wildlife, pollution control, NGT jurisdiction, real estate regulation (RERA), and land acquisition.",
        jurisdiction_scope="ALL",
        aliases=["Environmental Law", "Land Law", "Real Estate Law"],
        key_statutes=["Environment (Protection) Act, 1986", "National Green Tribunal Act, 2010", "Real Estate (Regulation and Development) Act, 2016", "Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act, 2013"],
        search_keywords=["environment", "pollution", "ngt", "national green tribunal", "rera", "real estate", "land acquisition", "forest conservation"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-ENV-RERA",
        name="Real Estate Regulation (RERA)",
        description="Real Estate (Regulation and Development) Act, 2016, mandatory project registration, allottee protection, escrow accounts, delayed possession interest, and State RERA authorities.",
        parent_code="TAX-ENV",
        jurisdiction_scope="ALL",
        aliases=["RERA Law", "Real Estate Regulation"],
        key_statutes=["Real Estate (Regulation and Development) Act, 2016"],
        search_keywords=["rera", "homebuyer rights", "delayed possession", "allottee", "promoter liability", "escrow account", "maharera", "rera tribunal"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-ENV-POLLUTION",
        name="Pollution & National Green Tribunal",
        description="Air and Water pollution control, Environmental Impact Assessment (EIA), polluter pays principle, public trust doctrine, and NGT orders.",
        parent_code="TAX-ENV",
        jurisdiction_scope="ALL",
        aliases=["Pollution Law", "NGT Law"],
        key_statutes=["Environment (Protection) Act, 1986", "National Green Tribunal Act, 2010", "Air (Prevention and Control of Pollution) Act, 1981", "Water (Prevention and Control of Pollution) Act, 1974"],
        search_keywords=["ngt", "national green tribunal", "eia", "environmental clearance", "polluter pays", "public trust doctrine", "air pollution", "water pollution"]
    ))

    # =========================================================================
    # DOMAIN 8: SPECIALIZED & PUBLIC STATUTORY REGULATION
    # =========================================================================
    mgr.add_node(TaxonomyNode(
        code="TAX-SPEC",
        name="Specialized & Public Statutory Regulation",
        description="Election law, citizenship and immigration, public procurement, food and drug regulation, intellectual property, and human rights.",
        jurisdiction_scope="ALL",
        aliases=["Public Regulation", "Specialized Laws"],
        key_statutes=["Representation of the People Act, 1951", "Citizenship Act, 1955", "Protection of Human Rights Act, 1993", "Patents Act, 1970", "Copyright Act, 1957", "Trade Marks Act, 1999"],
        search_keywords=["election", "citizenship", "procurement", "patents", "copyright", "trademark", "human rights", "nhrc"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-SPEC-IP",
        name="Intellectual Property Rights (IPR)",
        description="Patents, copyright, trademarks, geographical indications, trade secrets, design registration, and patent/trademark litigation.",
        parent_code="TAX-SPEC",
        jurisdiction_scope="CENTRAL",
        aliases=["IPR", "Intellectual Property"],
        key_statutes=["The Patents Act, 1970", "The Copyright Act, 1957", "The Trade Marks Act, 1999"],
        search_keywords=["patent infringement", "copyright fair use", "trademark infringement", "passing off", "section 52 copyright act", "commercial court"]
    ))
    mgr.add_node(TaxonomyNode(
        code="TAX-SPEC-ELECTION",
        name="Election Law & Representation",
        description="Representation of the People Acts (1950 & 1951), Election Commission of India powers, election petitions, disqualification of candidates, and Model Code of Conduct.",
        parent_code="TAX-SPEC",
        jurisdiction_scope="CENTRAL",
        aliases=["Election Law"],
        key_statutes=["Representation of the People Act, 1951", "The Constitution of India (Articles 324-329)"],
        search_keywords=["election petition", "disqualification", "model code of conduct", "election commission", "article 324", "corrupt practice"]
    ))

    return mgr

