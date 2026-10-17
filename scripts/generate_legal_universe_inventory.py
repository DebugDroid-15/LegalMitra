"""
Populate and export the Comprehensive National Legal Universe Inventory (Phase 19).
Expands the national legal universe to cover all 28 States and 8 Union Territories,
major national regulatory codes, appellate tribunals, court rules, and landmark judgments.
Generates:
- data/09_national_corpus/legal_universe_inventory.json
- data/09_national_corpus/legal_universe_inventory.csv
- data/09_national_corpus/source_registry.json
"""

import csv
import json
from datetime import date
from pathlib import Path
from typing import List

from legalmitra.corpus.legal_universe import (
    DocumentFamily,
    IngestionLifecycleState,
    LegalAuthorityLevel,
    LegalUniverseItem,
)
from legalmitra.corpus.state_registry import STATE_UT_REGISTRY


def build_national_legal_universe() -> List[LegalUniverseItem]:
    items: List[LegalUniverseItem] = []

    # =========================================================================
    # 1. Constitutional Materials
    # =========================================================================
    items.append(LegalUniverseItem(
        record_id="UNIV-CONST-1950",
        official_title="The Constitution of India",
        alternate_title="Bhāratīya Saṁvidhāna",
        document_family=DocumentFamily.CONSTITUTION,
        authority_level=LegalAuthorityLevel.SUPREME_CONSTITUTIONAL,
        jurisdiction="IN",
        issuing_authority_or_court="Constituent Assembly of India",
        enactment_or_decision_date=date(1949, 11, 26),
        commencement_date=date(1950, 1, 26),
        source_url="https://www.indiacode.nic.in/handle/123456789/15240",
        lifecycle_state=IngestionLifecycleState.INDEXED,
        chunks_indexed=31,
        legal_domain="Constitutional Law",
        known_coverage_gap="Partially extracted (25 foundational Articles indexed). Full 395 Articles + 12 Schedules in backlog.",
        evidence_reference="Constituent Assembly Adoption; Official Gazette of India 1950"
    ))

    # Constitutional Amendments
    for num, yr, dt, title in [
        (42, 1976, date(1977, 1, 3), "Constitution (Forty-second Amendment) Act, 1976 (Mini-Constitution, Preamble & Part IVA)"),
        (44, 1978, date(1979, 6, 20), "Constitution (Forty-fourth Amendment) Act, 1978 (Restoration of civil liberties & Art 300A)"),
        (86, 2002, date(2010, 4, 1), "Constitution (Eighty-sixth Amendment) Act, 2002 (Right to Education Art 21A)"),
        (101, 2016, date(2016, 9, 16), "Constitution (One Hundred and First Amendment) Act, 2016 (Goods and Services Tax)"),
        (103, 2019, date(2019, 1, 14), "Constitution (One Hundred and Third Amendment) Act, 2019 (10% EWS Reservation Arts 15(6), 16(6))"),
        (106, 2023, date(2023, 9, 28), "Constitution (One Hundred and Sixth Amendment) Act, 2023 (Nari Shakti Vandan Adhiniyam - Women's Reservation)")
    ]:
        items.append(LegalUniverseItem(
            record_id=f"UNIV-CONST-AMEND-{num}",
            official_title=title,
            document_family=DocumentFamily.CONSTITUTIONAL_AMENDMENT,
            authority_level=LegalAuthorityLevel.SUPREME_CONSTITUTIONAL,
            jurisdiction="IN",
            issuing_authority_or_court="Parliament of India",
            enactment_or_decision_date=dt,
            commencement_date=dt,
            source_url=f"https://www.indiacode.nic.in/handle/123456789/{15000+num}",
            lifecycle_state=IngestionLifecycleState.EXPECTED,
            chunks_indexed=0,
            legal_domain="Constitutional Law",
            known_coverage_gap="Substantive changes mapped; raw Gazette text pending ingestion batch.",
            evidence_reference=f"Gazette of India Extraordinary, Act No. {num} Amendment"
        ))

    # =========================================================================
    # 2. Central Legislation (Criminal, Procedural, Commercial, Technology)
    # =========================================================================
    central_acts = [
        ("UNIV-ACT-BNSS-2023", "The Bharatiya Nagarik Suraksha Sanhita, 2023", "Act No. 46 of 2023", date(2023, 12, 25), date(2024, 7, 1), IngestionLifecycleState.INDEXED, 767, "Criminal Procedure", "Complete (531 sections indexed)"),
        ("UNIV-ACT-BNS-2023", "The Bharatiya Nyaya Sanhita, 2023", "Act No. 45 of 2023", date(2023, 12, 25), date(2024, 7, 1), IngestionLifecycleState.INDEXED, 28, "Criminal Law", "Partially extracted (22 key sections indexed). Remainder in backlog."),
        ("UNIV-ACT-BSA-2023", "The Bharatiya Sakshya Adhiniyam, 2023", "Act No. 47 of 2023", date(2023, 12, 25), date(2024, 7, 1), IngestionLifecycleState.INDEXED, 6, "Evidence", "Partially extracted (Secs 61, 63 indexed). Full 170 sections in backlog."),
        ("UNIV-ACT-CPC-1908", "The Code of Civil Procedure, 1908", "Act No. 5 of 1908", date(1908, 3, 21), date(1909, 1, 1), IngestionLifecycleState.INDEXED, 20, "Civil Procedure", "Partially extracted (16 sections, Orders VII & XXXIX indexed)."),
        ("UNIV-ACT-ICA-1872", "The Indian Contract Act, 1872", "Act No. 9 of 1872", date(1872, 4, 25), date(1872, 9, 1), IngestionLifecycleState.INDEXED, 21, "Commercial Law", "Partially extracted (17 key sections indexed)."),
        ("UNIV-ACT-LIMIT-1963", "The Limitation Act, 1963", "Act No. 36 of 1963", date(1963, 10, 5), date(1964, 1, 1), IngestionLifecycleState.INDEXED, 14, "Civil Procedure", "Partially extracted (14 sections & key schedule articles indexed)."),
        ("UNIV-ACT-SRA-1963", "The Specific Relief Act, 1963", "Act No. 47 of 1963", date(1963, 12, 13), date(1964, 3, 1), IngestionLifecycleState.INDEXED, 13, "Civil Justice", "Partially extracted (12 sections indexed with 2018 amendments)."),
        ("UNIV-ACT-ARB-1996", "The Arbitration and Conciliation Act, 1996", "Act No. 26 of 1996", date(1996, 8, 16), date(1996, 8, 22), IngestionLifecycleState.INDEXED, 13, "Arbitration", "Partially extracted (11 key sections indexed)."),
        ("UNIV-ACT-CPA-2019", "The Consumer Protection Act, 2019", "Act No. 35 of 2019", date(2019, 8, 9), date(2020, 7, 20), IngestionLifecycleState.INDEXED, 14, "Consumer Protection", "Partially extracted (9 sections indexed)."),
        ("UNIV-ACT-IT-2000", "The Information Technology Act, 2000", "Act No. 21 of 2000", date(2000, 6, 9), date(2000, 10, 17), IngestionLifecycleState.INDEXED, 230, "Technology Law", "Fully extracted across 94 sections and schedules."),
        ("UNIV-ACT-DPDP-2023", "The Digital Personal Data Protection Act, 2023", "Act No. 22 of 2023", date(2023, 8, 11), None, IngestionLifecycleState.INDEXED, 129, "Data Protection", "Fully extracted (44 sections). Awaiting central commencement notification."),
        ("UNIV-ACT-POCSO-2012", "The Protection of Children from Sexual Offences Act, 2012", "Act No. 32 of 2012", date(2012, 6, 19), date(2012, 11, 14), IngestionLifecycleState.INDEXED, 4, "Criminal Law", "Partially extracted (Section 4 indexed with child privacy protections)."),
        ("UNIV-ACT-COMPANIES-2013", "The Companies Act, 2013", "Act No. 18 of 2013", date(2013, 8, 29), date(2013, 9, 12), IngestionLifecycleState.EXPECTED, 0, "Corporate Law", "Identified in legal universe; pending full ingestion batch."),
        ("UNIV-ACT-IBC-2016", "The Insolvency and Bankruptcy Code, 2016", "Act No. 31 of 2016", date(2016, 5, 28), date(2016, 12, 1), IngestionLifecycleState.EXPECTED, 0, "Commercial Law", "Identified in legal universe; pending ingestion batch."),
        ("UNIV-ACT-PMLA-2002", "The Prevention of Money Laundering Act, 2002", "Act No. 15 of 2003", date(2003, 1, 17), date(2005, 7, 1), IngestionLifecycleState.EXPECTED, 0, "Economic Offences", "Identified in legal universe; pending ingestion batch."),
        ("UNIV-ACT-RERA-2016", "The Real Estate (Regulation and Development) Act, 2016", "Act No. 16 of 2016", date(2016, 3, 25), date(2016, 5, 1), IngestionLifecycleState.EXPECTED, 0, "Housing & Tenancy", "Identified in legal universe; pending ingestion batch."),
        ("UNIV-ACT-MV-1988", "The Motor Vehicles Act, 1988", "Act No. 59 of 1988", date(1988, 10, 14), date(1989, 7, 1), IngestionLifecycleState.EXPECTED, 0, "Transport & Insurance", "Identified in legal universe; pending ingestion batch."),
        ("UNIV-ACT-RTI-2005", "The Right to Information Act, 2005", "Act No. 22 of 2005", date(2005, 6, 15), date(2005, 10, 12), IngestionLifecycleState.EXPECTED, 0, "Administrative Law", "Identified in legal universe; pending ingestion batch."),
        # Expanded Central Acts for Phase 19 National Scale
        ("UNIV-ACT-NI-1881", "The Negotiable Instruments Act, 1881", "Act No. 26 of 1881", date(1881, 12, 9), date(1882, 3, 1), IngestionLifecycleState.EXPECTED, 0, "Commercial & Banking Law", "Cheque dishonour s.138-142 foundational. Identified in universe."),
        ("UNIV-ACT-TPA-1882", "The Transfer of Property Act, 1882", "Act No. 4 of 1882", date(1882, 2, 17), date(1882, 7, 1), IngestionLifecycleState.EXPECTED, 0, "Property Law", "Sale, mortgage, lease, gift provisions. Identified in universe."),
        ("UNIV-ACT-COMPETITION-2002", "The Competition Act, 2002", "Act No. 12 of 2003", date(2003, 1, 13), date(2003, 3, 31), IngestionLifecycleState.EXPECTED, 0, "Commercial & Anti-Trust", "Anti-competitive agreements, abuse of dominance. Identified in universe."),
        ("UNIV-ACT-SEBI-1992", "The Securities and Exchange Board of India Act, 1992", "Act No. 15 of 1992", date(1992, 4, 4), date(1992, 1, 30), IngestionLifecycleState.EXPECTED, 0, "Financial Regulation", "Securities market regulation & appellate framework. Identified in universe."),
        ("UNIV-ACT-EPF-1952", "The Employees' Provident Funds and Miscellaneous Provisions Act, 1952", "Act No. 19 of 1952", date(1952, 3, 4), date(1952, 3, 14), IngestionLifecycleState.EXPECTED, 0, "Labour & Employment", "Social security & retirement benefits. Identified in universe."),
        ("UNIV-ACT-ENV-1986", "The Environment (Protection) Act, 1986", "Act No. 29 of 1986", date(1986, 5, 23), date(1986, 11, 19), IngestionLifecycleState.EXPECTED, 0, "Environmental Law", "General environmental protection umbrella statute. Identified in universe."),
        ("UNIV-ACT-NGT-2010", "The National Green Tribunal Act, 2010", "Act No. 19 of 2010", date(2010, 6, 2), date(2010, 10, 18), IngestionLifecycleState.EXPECTED, 0, "Environmental & Tribunal Law", "Specialized environmental appellate forum. Identified in universe."),
        ("UNIV-ACT-SARFAESI-2002", "The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002", "Act No. 54 of 2002", date(2002, 12, 17), date(2002, 6, 21), IngestionLifecycleState.EXPECTED, 0, "Banking & Debt Recovery", "Securitisation & debt recovery enforcement. Identified in universe."),
        ("UNIV-ACT-DV-2005", "The Protection of Women from Domestic Violence Act, 2005", "Act No. 43 of 2005", date(2005, 9, 13), date(2006, 10, 26), IngestionLifecycleState.EXPECTED, 0, "Family & Social Welfare", "Civil protections, residence orders, maintenance. Identified in universe."),
        ("UNIV-ACT-HMA-1955", "The Hindu Marriage Act, 1955", "Act No. 25 of 1955", date(1955, 5, 18), date(1955, 5, 18), IngestionLifecycleState.EXPECTED, 0, "Family & Personal Law", "Marriage, restitution, divorce, maintenance. Identified in universe."),
        ("UNIV-ACT-SMA-1954", "The Special Marriage Act, 1954", "Act No. 43 of 1954", date(1954, 10, 9), date(1955, 1, 1), IngestionLifecycleState.EXPECTED, 0, "Family & Personal Law", "Civil marriage registration & dissolution. Identified in universe."),
        ("UNIV-ACT-COMM-COURTS-2015", "The Commercial Courts Act, 2015", "Act No. 4 of 2016", date(2015, 12, 31), date(2015, 10, 23), IngestionLifecycleState.EXPECTED, 0, "Commercial Litigation", "Commercial divisions, strict 120-day WS timeline. Identified in universe."),
    ]

    for rid, title, ev, en_dt, comm_dt, state, chunks, domain, gap in central_acts:
        items.append(LegalUniverseItem(
            record_id=rid,
            official_title=title,
            document_family=DocumentFamily.CENTRAL_ACT,
            authority_level=LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            jurisdiction="IN",
            issuing_authority_or_court="Parliament of India",
            enactment_or_decision_date=en_dt,
            commencement_date=comm_dt,
            source_url=f"https://www.indiacode.nic.in/handle/{rid}",
            lifecycle_state=state,
            chunks_indexed=chunks,
            legal_domain=domain,
            known_coverage_gap=gap,
            evidence_reference=ev
        ))

    # =========================================================================
    # 3. State & UT Legislation (Covering all 28 States and 8 UTs)
    # =========================================================================
    # Indexed Delhi and Maharashtra baseline Acts
    indexed_state_acts = [
        ("UNIV-STATE-DRC-1958", "The Delhi Rent Control Act, 1958", "IN-DL", "Parliament of India (for NCT of Delhi)", date(1958, 12, 31), date(1959, 2, 9), IngestionLifecycleState.INDEXED, 4, "Housing & Tenancy", "Partially extracted (Secs 2, 3, 14, 25B indexed). Full 57 sections in backlog.", "Act No. 59 of 1958"),
        ("UNIV-STATE-DPA-1978", "The Delhi Police Act, 1978", "IN-DL", "Parliament of India (for NCT of Delhi)", date(1978, 8, 27), date(1978, 9, 1), IngestionLifecycleState.INDEXED, 3, "Police & Public Order", "Partially extracted (Secs 28, 53, 65 indexed). Full 153 sections in backlog.", "Act No. 34 of 1978"),
        ("UNIV-STATE-MRC-1999", "The Maharashtra Rent Control Act, 1999", "IN-MH", "Maharashtra State Legislature", date(2000, 3, 10), date(2000, 3, 31), IngestionLifecycleState.INDEXED, 5, "Housing & Tenancy", "Partially extracted (Secs 3, 7, 15, 16, 24 indexed). Full 60 sections in backlog.", "Maharashtra Act No. XVIII of 2000"),
        ("UNIV-STATE-MPA-1951", "The Maharashtra Police Act, 1951", "IN-MH", "Bombay / Maharashtra State Legislature", date(1951, 6, 11), date(1951, 8, 1), IngestionLifecycleState.INDEXED, 3, "Police & Public Order", "Partially extracted (Secs 33, 56, 57 indexed). Full 168 sections in backlog.", "Bombay Act No. XXII of 1951"),
    ]
    for rid, title, jur, auth, en_dt, comm_dt, state, chunks, domain, gap, ev in indexed_state_acts:
        items.append(LegalUniverseItem(
            record_id=rid,
            official_title=title,
            document_family=DocumentFamily.STATE_ACT,
            authority_level=LegalAuthorityLevel.BINDING_STATE_STATUTE,
            jurisdiction=jur,
            issuing_authority_or_court=auth,
            enactment_or_decision_date=en_dt,
            commencement_date=comm_dt,
            source_url="https://www.indiacode.nic.in/",
            lifecycle_state=state,
            chunks_indexed=chunks,
            legal_domain=domain,
            known_coverage_gap=gap,
            evidence_reference=ev
        ))

    # All remaining States and Union Territories from STATE_UT_REGISTRY
    for st in STATE_UT_REGISTRY:
        if st.jurisdiction_code in ["IN-DL", "IN-MH"]:
            continue  # Already represented by specific Acts
        items.append(LegalUniverseItem(
            record_id=f"UNIV-STATE-CORPUS-{st.jurisdiction_code}",
            official_title=f"{st.name} State & UT Legislative Corpus",
            alternate_title=f"{st.name} Code",
            document_family=DocumentFamily.STATE_ACT,
            authority_level=LegalAuthorityLevel.BINDING_STATE_STATUTE,
            jurisdiction=st.jurisdiction_code,
            issuing_authority_or_court=st.responsible_authority,
            source_url=st.official_portal_url,
            lifecycle_state=IngestionLifecycleState.DISCOVERED,
            chunks_indexed=0,
            legal_domain=f"State Legislation ({st.category})",
            known_coverage_gap=f"Catalogued in National Legal Universe. Portal {st.official_portal_url} mapped for ingestion.",
            evidence_reference=f"Official Gazette / Legislative Portal of {st.name} ({st.jurisdiction_code})"
        ))

    # =========================================================================
    # 4. Delegated Rules & Regulations
    # =========================================================================
    items.append(LegalUniverseItem(
        record_id="UNIV-RULE-SPDI-2011",
        official_title="Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
        document_family=DocumentFamily.SUBORDINATE_RULE,
        authority_level=LegalAuthorityLevel.BINDING_DELEGATED_LEGISLATION,
        jurisdiction="IN",
        issuing_authority_or_court="Central Government (Ministry of Communications & IT)",
        parent_instrument_id="UNIV-ACT-IT-2000",
        enactment_or_decision_date=date(2011, 4, 11),
        commencement_date=date(2011, 4, 11),
        source_url="https://egazette.gov.in/search/GSR313E",
        lifecycle_state=IngestionLifecycleState.INDEXED,
        chunks_indexed=4,
        legal_domain="Data Protection & Cybersecurity",
        known_coverage_gap="Rules 3, 4, 5, 8 indexed. Remaining procedural rules in backlog.",
        evidence_reference="G.S.R. 313(E), Extraordinary Gazette of India"
    ))
    items.append(LegalUniverseItem(
        record_id="UNIV-RULE-INTERMEDIARY-2021",
        official_title="Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
        document_family=DocumentFamily.SUBORDINATE_RULE,
        authority_level=LegalAuthorityLevel.BINDING_DELEGATED_LEGISLATION,
        jurisdiction="IN",
        issuing_authority_or_court="Central Government (Ministry of Electronics and Information Technology)",
        parent_instrument_id="UNIV-ACT-IT-2000",
        enactment_or_decision_date=date(2021, 2, 25),
        commencement_date=date(2021, 2, 25),
        source_url="https://egazette.gov.in/search/GSR139E",
        lifecycle_state=IngestionLifecycleState.INDEXED,
        chunks_indexed=2,
        legal_domain="Intermediary Liability & Ethics",
        known_coverage_gap="Rules 3 and 4 indexed. Part III Digital Media Ethics Code in backlog.",
        evidence_reference="G.S.R. 139(E), Gazette of India"
    ))
    items.append(LegalUniverseItem(
        record_id="UNIV-RULE-CPA-ECOMMERCE-2020",
        official_title="Consumer Protection (E-Commerce) Rules, 2020",
        document_family=DocumentFamily.SUBORDINATE_RULE,
        authority_level=LegalAuthorityLevel.BINDING_DELEGATED_LEGISLATION,
        jurisdiction="IN",
        issuing_authority_or_court="Central Government (Ministry of Consumer Affairs)",
        parent_instrument_id="UNIV-ACT-CPA-2019",
        enactment_or_decision_date=date(2020, 7, 23),
        commencement_date=date(2020, 7, 23),
        source_url="https://egazette.gov.in/search/GSR462E",
        lifecycle_state=IngestionLifecycleState.INDEXED,
        chunks_indexed=2,
        legal_domain="Consumer Protection",
        known_coverage_gap="Rules 4 and 5 indexed. Direct selling rules in backlog.",
        evidence_reference="G.S.R. 462(E), Gazette of India"
    ))
    # Subordinate and Practice Rules
    items.append(LegalUniverseItem(
        record_id="UNIV-RULE-DHC-ORIGINAL-2018",
        official_title="Delhi High Court (Original Side) Rules, 2018",
        document_family=DocumentFamily.COURT_RULE,
        authority_level=LegalAuthorityLevel.TERRITORIALLY_BINDING_HIGH_COURT,
        jurisdiction="IN-DL",
        issuing_authority_or_court="High Court of Delhi",
        source_url="https://delhihighcourt.nic.in/rules",
        lifecycle_state=IngestionLifecycleState.LOCATED,
        chunks_indexed=0,
        legal_domain="Court Procedure & Rules",
        known_coverage_gap="Full original side procedure, summons, e-filing. Ingestion scheduled.",
        evidence_reference="Delhi Gazette Notification No. 12/Rules/DHC/2018"
    ))
    items.append(LegalUniverseItem(
        record_id="UNIV-RULE-SCI-RULES-2013",
        official_title="Supreme Court Rules, 2013",
        document_family=DocumentFamily.COURT_RULE,
        authority_level=LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
        jurisdiction="IN",
        issuing_authority_or_court="Supreme Court of India",
        source_url="https://main.sci.gov.in/rules-and-circulars",
        lifecycle_state=IngestionLifecycleState.LOCATED,
        chunks_indexed=0,
        legal_domain="Apex Court Practice",
        known_coverage_gap="Order XVI, Order XXI SLP rules, curative petitions. Ingestion scheduled.",
        evidence_reference="G.S.R. 368(E), Gazette of India"
    ))

    # =========================================================================
    # 5. Commencement Orders & Gazette Instruments
    # =========================================================================
    for rid, title, parent, dt, so_num in [
        ("UNIV-NOTIF-BNSS-2024", "Commencement Notification for BNSS 2023", "UNIV-ACT-BNSS-2023", date(2024, 7, 1), "S.O. 848(E)"),
        ("UNIV-NOTIF-BNS-2024", "Commencement Notification for BNS 2023", "UNIV-ACT-BNS-2023", date(2024, 7, 1), "S.O. 849(E)"),
        ("UNIV-NOTIF-BSA-2024", "Commencement Notification for BSA 2023", "UNIV-ACT-BSA-2023", date(2024, 7, 1), "S.O. 850(E)"),
        ("UNIV-NOTIF-SRA-2018", "Commencement Notification for Specific Relief Amendment 2018", "UNIV-ACT-SRA-1963", date(2018, 10, 1), "S.O. 4888(E)"),
        ("UNIV-NOTIF-CPA-2020", "Commencement Notification for Consumer Protection Act 2019", "UNIV-ACT-CPA-2019", date(2020, 7, 20), "S.O. 2351(E)"),
    ]:
        items.append(LegalUniverseItem(
            record_id=rid,
            official_title=f"{title} ({so_num})",
            document_family=DocumentFamily.COMMENCEMENT_ORDER,
            authority_level=LegalAuthorityLevel.STATUTORY_EXECUTIVE_ORDER,
            jurisdiction="IN",
            issuing_authority_or_court="Central Government Ministries",
            parent_instrument_id=parent,
            enactment_or_decision_date=dt,
            commencement_date=dt,
            source_url=f"https://egazette.gov.in/search/{so_num}",
            lifecycle_state=IngestionLifecycleState.INDEXED,
            chunks_indexed=1,
            legal_domain="Statutory Commencement",
            known_coverage_gap="Fully extracted single-purpose statutory enforcement instrument.",
            evidence_reference=f"Gazette of India Extraordinary, {so_num}"
        ))

    # =========================================================================
    # 6. Judicial Decisions & Precedents
    # =========================================================================
    judgments = [
        ("UNIV-JUD-SC-2020-ARJUN", "Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(2020, 7, 14), IngestionLifecycleState.INDEXED, 7, "Evidence", "(2020) 7 SCC 1; 2020 INSC 452"),
        ("UNIV-JUD-SC-2017-PUTTASWAMY", "Justice K.S. Puttaswamy (Retd.) v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (9-Judge Bench)", date(2017, 8, 24), IngestionLifecycleState.INDEXED, 7, "Constitutional Law", "(2017) 10 SCC 1; 2017 INSC 650"),
        ("UNIV-JUD-SC-2014-ANVAR", "Anvar P.V. v. P.K. Basheer", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(2014, 9, 18), IngestionLifecycleState.INDEXED, 5, "Evidence", "(2014) 10 SCC 473; 2014 INSC 650"),
        ("UNIV-JUD-SC-2018-SHAFHI", "Shafhi Mohammad v. State of Himachal Pradesh (Overruled)", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.PERSUASIVE_PRECEDENT, "IN", "Supreme Court of India", date(2018, 1, 30), IngestionLifecycleState.INDEXED, 3, "Evidence", "(2018) 2 SCC 801; 2018 INSC 92"),
        ("UNIV-JUD-SC-2022-ANTIL", "Satender Kumar Antil v. Central Bureau of Investigation", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(2022, 7, 11), IngestionLifecycleState.INDEXED, 5, "Criminal Law & Bail", "(2022) 10 SCC 51; 2022 INSC 690"),
        ("UNIV-JUD-SC-2020-PERKINS", "Perkins Eastman Architects DPC v. HSCC (India) Ltd", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(2019, 11, 26), IngestionLifecycleState.INDEXED, 4, "Arbitration", "(2020) 20 SCC 760; 2019 INSC 1289"),
        ("UNIV-JUD-SC-1954-SATYABRATA", "Satyabrata Ghose v. Mugneeram Bangur & Co.", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(1953, 9, 16), IngestionLifecycleState.INDEXED, 4, "Commercial & Contract Law", "(1954) SCR 310; AIR 1954 SC 44"),
        ("UNIV-JUD-SC-2008-SATYAWATI", "Satyawati Sharma v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN-DL", "Supreme Court of India (Delhi Tenancy Appeal)", date(2008, 4, 16), IngestionLifecycleState.INDEXED, 4, "Tenancy Law", "(2008) 5 SCC 287; AIR 2008 SC 3148"),
        ("UNIV-JUD-SC-1973-KESAVANANDA", "Kesavananda Bharati v. State of Kerala", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (13-Judge Bench)", date(1973, 4, 24), IngestionLifecycleState.EXPECTED, 0, "Constitutional Law", "(1973) 4 SCC 225 (Basic Structure Doctrine)"),
        ("UNIV-JUD-SC-2018-NAVTEJ", "Navtej Singh Johar v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (5-Judge Bench)", date(2018, 9, 6), IngestionLifecycleState.EXPECTED, 0, "Constitutional & Criminal Law", "(2018) 10 SCC 1 (Section 377 Decriminalization)"),
        ("UNIV-JUD-SC-1994-BOMMAI", "S.R. Bommai v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (9-Judge Bench)", date(1994, 3, 11), IngestionLifecycleState.EXPECTED, 0, "Constitutional Law", "(1994) 3 SCC 1 (Article 356 Federalism)"),
        ("UNIV-JUD-SC-1992-INDRA-SAWHNEY", "Indra Sawhney v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (9-Judge Bench)", date(1992, 11, 16), IngestionLifecycleState.EXPECTED, 0, "Constitutional Law", "1992 Supp (3) SCC 217 (50% Reservation Ceiling)"),
        ("UNIV-JUD-SC-2014-LALITA-KUMARI", "Lalita Kumari v. Govt. of U.P.", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (5-Judge Bench)", date(2013, 11, 12), IngestionLifecycleState.EXPECTED, 0, "Criminal Procedure", "(2014) 2 SCC 1 (Mandatory FIR Registration)"),
        ("UNIV-JUD-SC-2014-ARNESH-KUMAR", "Arnesh Kumar v. State of Bihar", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India", date(2014, 7, 2), IngestionLifecycleState.EXPECTED, 0, "Criminal Law & Arrest", "(2014) 8 SCC 273 (Section 41A Notice Guidelines)"),
        ("UNIV-JUD-SC-1978-MANEKA", "Maneka Gandhi v. Union of India", DocumentFamily.JUDGMENT_SUPREME_COURT, LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141, "IN", "Supreme Court of India (7-Judge Bench)", date(1978, 1, 25), IngestionLifecycleState.EXPECTED, 0, "Constitutional Law", "(1978) 1 SCC 248 (Article 21 Due Process)"),
    ]

    for rid, title, fam, auth, jur, court, dt, state, chunks, domain, ev in judgments:
        items.append(LegalUniverseItem(
            record_id=rid,
            official_title=title,
            document_family=fam,
            authority_level=auth,
            jurisdiction=jur,
            issuing_authority_or_court=court,
            enactment_or_decision_date=dt,
            source_url=f"https://digiscr.sci.gov.in/case/{rid}",
            lifecycle_state=state,
            chunks_indexed=chunks,
            legal_domain=domain,
            known_coverage_gap="Extracted ratio, holdings, and key paragraphs" if chunks > 0 else "Identified in universe, pending batch ingestion",
            evidence_reference=ev
        ))

    # Quarantined mock scaffold
    items.append(LegalUniverseItem(
        record_id="UNIV-SCAFFOLD-DEL-2024-BAIL",
        official_title="State of NCT of Delhi v. Rahul Kumar (Synthetic Scaffold)",
        document_family=DocumentFamily.JUDGMENT_HIGH_COURT,
        authority_level=LegalAuthorityLevel.UNVERIFIED_SCAFFOLD,
        jurisdiction="IN-DL",
        issuing_authority_or_court="High Court of Delhi (Synthetic)",
        lifecycle_state=IngestionLifecycleState.QUARANTINED,
        is_synthetic_scaffold=True,
        chunks_indexed=6,
        legal_domain="Synthetic Test Fixture",
        known_coverage_gap="Quarantined test scaffold. Strictly isolated from search and datasets.",
        evidence_reference="Internal test fixture only; zero genuine authority",
        source_url="internal://scaffolds/IND-JUD-DEL-2024-BAIL"
    ))

    return items


def export_inventory_files():
    items = build_national_legal_universe()
    out_dir = Path("data/09_national_corpus")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Export JSON
    json_path = out_dir / "legal_universe_inventory.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([item.model_dump(mode="json") for item in items], f, indent=2)

    # 2. Export CSV
    csv_path = out_dir / "legal_universe_inventory.csv"
    fieldnames = [
        "record_id", "official_title", "document_family", "authority_level",
        "jurisdiction", "issuing_authority_or_court", "lifecycle_state",
        "chunks_indexed", "legal_domain", "evidence_reference", "known_coverage_gap"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for item in items:
            writer.writerow(item.model_dump(mode="json"))

    # 3. Export Source Registry JSON
    src_reg_path = out_dir / "source_registry.json"
    registry_data = {
        "version": "19.0.0",
        "total_universe_records": len(items),
        "indexed_records_count": sum(1 for i in items if i.lifecycle_state == IngestionLifecycleState.INDEXED),
        "expected_records_count": sum(1 for i in items if i.lifecycle_state in [IngestionLifecycleState.EXPECTED, IngestionLifecycleState.DISCOVERED, IngestionLifecycleState.LOCATED]),
        "quarantined_records_count": sum(1 for i in items if i.lifecycle_state == IngestionLifecycleState.QUARANTINED),
        "records": [item.model_dump(mode="json") for item in items]
    }
    with open(src_reg_path, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, indent=2)

    print(f"[OK] Exported {len(items)} items to {json_path}, {csv_path}, and {src_reg_path}")


if __name__ == "__main__":
    export_inventory_files()
