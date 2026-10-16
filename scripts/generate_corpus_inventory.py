"""
Script to generate machine-readable corpus coverage inventory for LegalMitra (Phase 14A).
Produces data/08_corpus/coverage_inventory.json and data/08_corpus/coverage_inventory.csv.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from legalmitra.corpus.inventory import (
    CorpusInventoryItem,
    CorpusInventoryManager,
    CorpusStatus,
    DocumentClass,
)


def get_db_chunk_counts(db_path: Path) -> dict[str, int]:
    if not db_path.exists():
        return {}
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        rows = cur.execute("SELECT source_id, COUNT(*) FROM legal_chunks GROUP BY source_id").fetchall()
        return dict(rows)
    except Exception:
        return {}
    finally:
        conn.close()


def build_inventory() -> CorpusInventoryManager:
    kb_path = Path("data/legalmitra_kb.db")
    chunk_counts = get_db_chunk_counts(kb_path)
    mgr = CorpusInventoryManager()

    # --- Currently Registered Active Sources ---

    # 1. IND-STAT-BSA-2023-SEC61
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-BSA-2023-SEC61",
        official_title="Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
        aliases=["BSA Section 61", "Admissibility of Electronic Records in Evidence"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Evidence",
        topic_taxonomy=["Evidence", "Electronic Evidence", "Admissibility", "Digital Records"],
        source_url="https://www.indiacode.nic.in/handle/123456789/20000",
        retrieval_date="2026-10-15",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        effective_date="2024-07-01",
        version="1.0.0",
        repeal_metadata="Replaced Indian Evidence Act 1872 Section 65A",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-BSA-2023-SEC61", 3),
        review_requirements="Pending advocate review in Pilot 20 (QA-PILOT-001)"
    ))

    # 2. IND-STAT-BSA-2023-SEC63
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-BSA-2023-SEC63",
        official_title="Bharatiya Sakshya Adhiniyam, 2023 - Section 63",
        aliases=["BSA Section 63", "Certificate for Admissibility of Electronic Records"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Evidence",
        topic_taxonomy=["Evidence", "Electronic Evidence", "Section 63 Certificate", "Digital Proof"],
        source_url="https://www.indiacode.nic.in/handle/123456789/20000",
        retrieval_date="2026-10-15",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        effective_date="2024-07-01",
        version="1.0.0",
        repeal_metadata="Replaced Indian Evidence Act 1872 Section 65B",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-BSA-2023-SEC63", 3),
        review_requirements="Pending advocate review in Pilot 20 (QA-PILOT-002)"
    ))

    # 3. IND-STAT-POCSO-2012-SEC4
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-POCSO-2012-SEC4",
        official_title="Protection of Children from Sexual Offences Act, 2012 - Section 4",
        aliases=["POCSO Section 4", "Punishment for Penetrative Sexual Assault"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Child Protection",
        topic_taxonomy=["Penal Law", "Special Criminal Law", "Child Protection", "Penetrative Sexual Assault"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2056",
        retrieval_date="2026-10-15",
        enactment_date="2012-06-19",
        assent_date="2012-06-19",
        commencement_date="2012-11-14",
        effective_date="2012-11-14",
        version="1.0.0",
        amendment_history=["Amended by POCSO (Amendment) Act, 2019 (Act 25 of 2019)"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-POCSO-2012-SEC4", 4),
        review_requirements="Pending advocate review in Pilot 20 (QA-PILOT-003, POCSO s.33(7) mandatory victim redaction applied)"
    ))

    # 4. IND-STAT-BNSS-2023
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-BNSS-2023",
        official_title="The Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)",
        aliases=["BNSS 2023", "Code of Criminal Procedure 2023 replacement"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Procedure",
        topic_taxonomy=["Criminal Procedure", "Arrest", "Bail", "Investigation", "Trial", "Appeals", "Sentencing"],
        source_url="https://indiacode.gov.in/handle/123456789/601739",
        retrieval_date="2026-10-16",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        effective_date="2024-07-01",
        version="1.0.0",
        repeal_metadata="Repealed Code of Criminal Procedure 1973 under Section 531(1), with pending proceedings saved under Section 531(2)(a)",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-BNSS-2023", 767),
        review_requirements="Pending advocate review in Batch 1 (QA-BATCH1-001 to 004); Anti-conflation regression verified"
    ))

    # 5. IND-STAT-DPDP-2023
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-DPDP-2023",
        official_title="The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)",
        aliases=["DPDP Act 2023", "Data Protection Law India"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Technology & Emerging Regulation",
        topic_taxonomy=["Privacy", "Data Protection", "Digital Rights", "Data Fiduciary", "Data Principal"],
        source_url="https://indiacode.gov.in/handle/123456789/496508",
        retrieval_date="2026-10-16",
        enactment_date="2023-08-11",
        assent_date="2023-08-11",
        commencement_date=None,  # Section 1(2) phased commencement
        effective_date=None,
        version="1.0.0",
        repeal_metadata="Section 44(2) amends IT Act 2000 by omitting section 43A (repeal effective only upon gazette appointment)",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-DPDP-2023", 129),
        coverage_gap_notes="Substantive provisions uncommenced pending central notification under s.1(2)",
        review_requirements="Batch 1 candidates cover phased commencement boundary"
    ))

    # 6. IND-STAT-IT-2000
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-IT-2000",
        official_title="The Information Technology Act, 2000 (Act No. 21 of 2000, as amended)",
        aliases=["IT Act 2000", "Cyber Law India"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Technology & Emerging Regulation",
        topic_taxonomy=["Cyber Law", "Electronic Governance", "Intermediary Liability", "Cyber Offences"],
        source_url="https://indiacode.gov.in/handle/123456789/496511",
        retrieval_date="2026-10-16",
        enactment_date="2000-06-09",
        assent_date="2000-06-09",
        commencement_date="2000-10-17",
        effective_date="2000-10-17",
        version="1.0.0",
        amendment_history=["Information Technology (Amendment) Act, 2008 (Act 10 of 2009)"],
        repeal_metadata="Section 43A slated for repeal upon DPDP s.44(2) notification; currently operative in law",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-STAT-IT-2000", 230),
        review_requirements="Intermediary rules and s.43A operative status evaluated in Batch 1"
    ))

    # 7. IND-JUD-SC-2017-PUTTASWAMY
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-2017-PUTTASWAMY",
        official_title="Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1",
        aliases=["Puttaswamy I", "Privacy Judgment", "Right to Privacy Case", "AIR 2017 SC 4161"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Fundamental Rights", "Article 21", "Right to Privacy", "Constitutional Law", "Proportionality"],
        source_url="https://main.sci.gov.in/judgments",
        retrieval_date="2026-10-15",
        publication_date="2017-08-24",
        version="1.0.0",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="completed",
        validation_status="validated",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=chunk_counts.get("IND-JUD-SC-2017-PUTTASWAMY", 7),
        review_requirements="9-Judge Constitution Bench holding confirming privacy as fundamental right under Art 21"
    ))

    # 8. IND-JUD-DEL-2024-BAIL (Quarantined Synthetic Scaffold)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-DEL-2024-BAIL",
        official_title="State (NCT of Delhi) v. Rahul Kumar - Anticipatory Bail under BNSS [QUARANTINED]",
        aliases=["Synthetic Test Scaffold 2024", "BNSS Bail Scaffold"],
        issuing_authority="High Court of Delhi (Synthetic)",
        jurisdiction="IN-DL",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Criminal Law & Procedure",
        topic_taxonomy=["Bail", "Anticipatory Bail", "Synthetic Test Case"],
        source_url="https://delhihighcourt.nic.in/judgments",
        retrieval_date="2026-10-15",
        publication_date="2024-07-10",
        version="1.0.0",
        authenticity_status="flagged_unsupported",
        licence_or_terms="Quarantined Internal Fixture",
        extraction_status="quarantined",
        validation_status="failed",
        corpus_status=CorpusStatus.QUARANTINED,
        indexed_chunk_count=chunk_counts.get("IND-JUD-DEL-2024-BAIL", 6),
        coverage_gap_notes="QUARANTINED SYNTHETIC TEST SCAFFOLD: Inverted party designation (State petitioner for anticipatory bail under BNSS s.482). Permanently excluded from RAG retrieval and training sets.",
        review_requirements="Do NOT include in advocate review or active retrieval"
    ))

    # 9. IND-GUIDE-SCI-PROC-2025 (Inaccessible / Extraction Failure)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-GUIDE-SCI-PROC-2025",
        official_title="Supreme Court of India Handbook on Practice and Procedure and Office Procedure (2017, updated to 06.10.2025)",
        aliases=["SCI Practice Handbook 2025", "Supreme Court Practice Rules"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.PRACTICE_DIRECTION,
        legal_domain="Civil Justice & Judicial Procedure",
        topic_taxonomy=["Supreme Court Rules", "Filing Procedures", "Registry Practice", "Office Procedure"],
        source_url="https://www.sci.gov.in/handbook-on-practice-procedure-and-office-procedure-2017/",
        retrieval_date="2026-10-16",
        publication_date="2025-10-06",
        version="1.0.0",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court of India",
        extraction_status="failed",
        validation_status="pending",
        corpus_status=CorpusStatus.INACCESSIBLE,
        indexed_chunk_count=0,
        coverage_gap_notes="Docling 15-page limit exceeded (278 pages). Requires multi-part chunking extraction pipeline.",
        review_requirements="Pending chunked extraction"
    ))

    # 10. IND-UNSUPPORTED-001 (Unsupported test case)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-UNSUPPORTED-001",
        official_title="Corrupt or Unsupported Document Format (.xyz)",
        aliases=["Unsupported Format Fixture"],
        issuing_authority="Synthetic Negative Test",
        jurisdiction="IN",
        document_class=DocumentClass.OTHER,
        legal_domain="Test Fixtures",
        topic_taxonomy=["Negative Test"],
        source_url="https://example.com/unsupported",
        retrieval_date="2026-10-15",
        version="1.0.0",
        authenticity_status="synthetic_negative",
        licence_or_terms="Internal Test",
        extraction_status="failed",
        validation_status="failed",
        corpus_status=CorpusStatus.UNVERIFIED,
        indexed_chunk_count=0,
        coverage_gap_notes="Negative test fixture verifying pipeline rejection of unknown extensions.",
        review_requirements="None"
    ))

    # --- Target National Legal Universe (Planned & Prioritized Corpus Inventory) ---

    # 11. IND-CONST-1950: Constitution of India
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-CONST-1950",
        official_title="The Constitution of India",
        aliases=["Constitution of India", "Indian Constitution", "Samvidhan"],
        issuing_authority="Constituent Assembly of India / Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.CONSTITUTION,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Fundamental Rights", "Directive Principles", "Judiciary", "Executive", "Legislature", "Federalism", "Amendments"],
        source_url="https://legislative.gov.in/constitution-of-india/",
        enactment_date="1949-11-26",
        assent_date="1949-11-26",
        commencement_date="1950-01-26",
        effective_date="1950-01-26",
        version="106th Amendment (as of 2024)",
        amendment_history=["1st Amendment 1951 to 106th Amendment (Nari Shakti Vandan Adhiniyam) 2023"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Full text scheduled for Phase 14 Batch 2 ingestion.",
        review_requirements="High-priority constitutional foundation."
    ))

    # 12. IND-STAT-BNS-2023: Bharatiya Nyaya Sanhita, 2023
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-BNS-2023",
        official_title="The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023)",
        aliases=["BNS 2023", "Indian Penal Code 2023 replacement"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Procedure",
        topic_taxonomy=["Substantive Penal Law", "Offences Against State", "Offences Against Body", "Offences Against Property", "Organized Crime", "Terrorism"],
        source_url="https://indiacode.gov.in/handle/123456789/601738",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        effective_date="2024-07-01",
        version="1.0.0",
        repeal_metadata="Repealed Indian Penal Code, 1860 under Section 358(1), subject to savings under Section 358(2)",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Primary substantive criminal enactment in force from 2024-07-01.",
        review_requirements="Mandatory pairing with BNSS and BSA."
    ))

    # 13. IND-STAT-IPC-1860: Indian Penal Code, 1860 (Historical)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-IPC-1860",
        official_title="The Indian Penal Code (Act No. 45 of 1860)",
        aliases=["IPC 1860", "Indian Penal Code"],
        issuing_authority="Governor-General in Council / Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Procedure",
        topic_taxonomy=["Historical Penal Law", "Pre-2024 Offences", "Substantive Criminal Law"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2263",
        enactment_date="1860-10-06",
        commencement_date="1862-01-01",
        effective_date="1862-01-01",
        version="Historical consolidated as of 2024-06-30",
        repeal_metadata="Repealed by BNS 2023 s.358 w.e.f. 2024-07-01; governing substantive offenses committed prior to 2024-07-01",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.HISTORICAL,
        indexed_chunk_count=0,
        coverage_gap_notes="Essential for offences committed on or before 2024-06-30 (Article 20(1) ex post facto protection).",
        review_requirements="Temporal point-in-time indexing required."
    ))

    # 14. IND-STAT-CRPC-1973: Code of Criminal Procedure, 1973 (Historical)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-CRPC-1973",
        official_title="The Code of Criminal Procedure, 1973 (Act No. 2 of 1974)",
        aliases=["CrPC 1973", "Code of Criminal Procedure"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Procedure",
        topic_taxonomy=["Historical Criminal Procedure", "Pending Investigations", "Pending Trials", "Section 531 Savings"],
        source_url="https://www.indiacode.nic.in/handle/123456789/1611",
        enactment_date="1974-01-25",
        commencement_date="1974-04-01",
        effective_date="1974-04-01",
        version="Historical consolidated as of 2024-06-30",
        repeal_metadata="Repealed by BNSS 2023 s.531(1) w.e.f. 2024-07-01; saved for pending inquiries, trials, and investigations under s.531(2)(a)",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.HISTORICAL,
        indexed_chunk_count=0,
        coverage_gap_notes="Required for procedural guidance on pending criminal matters instituted prior to 2024-07-01.",
        review_requirements="Must maintain distinct status from BNSS Section 531."
    ))

    # 15. IND-STAT-IEA-1872: Indian Evidence Act, 1872 (Historical)
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-IEA-1872",
        official_title="The Indian Evidence Act, 1872 (Act No. 1 of 1872)",
        aliases=["IEA 1872", "Indian Evidence Act"],
        issuing_authority="Governor-General in Council / Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Evidence",
        topic_taxonomy=["Historical Evidence Law", "Section 65B Certificate", "Primary Evidence", "Secondary Evidence"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2188",
        enactment_date="1872-03-15",
        commencement_date="1872-09-01",
        effective_date="1872-09-01",
        version="Historical consolidated as of 2024-06-30",
        repeal_metadata="Repealed by BSA 2023 s.170(1) w.e.f. 2024-07-01; saved under s.170(2)",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.HISTORICAL,
        indexed_chunk_count=0,
        coverage_gap_notes="Required for evidence admitted in proceedings initiated prior to 2024-07-01.",
        review_requirements="Verify s.65B transition to BSA s.63."
    ))

    # 16. IND-STAT-CPC-1908: Code of Civil Procedure, 1908
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-CPC-1908",
        official_title="The Code of Civil Procedure, 1908 (Act No. 5 of 1908)",
        aliases=["CPC 1908", "Civil Procedure Code"],
        issuing_authority="Governor-General in Council / Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice",
        topic_taxonomy=["Civil Procedure", "Suits", "Injunctions", "Execution", "Appeals", "Revision", "Res Judicata"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2191",
        enactment_date="1908-03-21",
        commencement_date="1909-01-01",
        effective_date="1909-01-01",
        version="Consolidated as amended",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Foundational statute for civil dispute resolution and court jurisdiction.",
        review_requirements="Order 39 temporary injunction rules prioritized."
    ))

    # 17. IND-STAT-LIMIT-1963: Limitation Act, 1963
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-LIMIT-1963",
        official_title="The Limitation Act, 1963 (Act No. 36 of 1963)",
        aliases=["Limitation Act 1963"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice",
        topic_taxonomy=["Limitation Periods", "Condonation of Delay", "Section 5", "Extinguishment of Right"],
        source_url="https://www.indiacode.nic.in/handle/123456789/1565",
        enactment_date="1963-10-05",
        commencement_date="1964-01-01",
        effective_date="1964-01-01",
        version="Consolidated",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Critical for preventing statute-barred claims across civil, consumer, and writ jurisdiction.",
        review_requirements="Section 5 condonation rules and schedule periods."
    ))

    # 18. IND-STAT-ICA-1872: Indian Contract Act, 1872
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-ICA-1872",
        official_title="The Indian Contract Act, 1872 (Act No. 9 of 1872)",
        aliases=["Contract Act 1872", "Indian Contract Act"],
        issuing_authority="Governor-General in Council / Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice & Commercial Law",
        topic_taxonomy=["Formation of Contract", "Breach", "Damages", "Indemnity", "Guarantee", "Bailment", "Agency"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2187",
        enactment_date="1872-04-25",
        commencement_date="1872-09-01",
        effective_date="1872-09-01",
        version="Consolidated",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Core commercial agreement framework; s.73/74 liquidated damages.",
        review_requirements="Essential commercial law foundation."
    ))

    # 19. IND-STAT-SRA-1963: Specific Relief Act, 1963
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-SRA-1963",
        official_title="The Specific Relief Act, 1963 (Act No. 47 of 1963, as amended)",
        aliases=["Specific Relief Act 1963", "SRA"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice & Commercial Law",
        topic_taxonomy=["Specific Performance", "Injunctions", "Substituted Performance", "Infrastructure Contracts"],
        source_url="https://www.indiacode.nic.in/handle/123456789/1583",
        enactment_date="1963-12-13",
        commencement_date="1964-03-01",
        effective_date="1964-03-01",
        version="As amended by Specific Relief (Amendment) Act, 2018 (Act 18 of 2018)",
        amendment_history=["Specific Relief (Amendment) Act, 2018 (Act 18 of 2018 w.e.f. 2018-10-01)"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="2018 Amendment transformed specific performance from discretionary to mandatory relief.",
        review_requirements="Section 10 and 20A infrastructure bar."
    ))

    # 20. IND-STAT-ARB-1996: Arbitration and Conciliation Act, 1996
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-ARB-1996",
        official_title="The Arbitration and Conciliation Act, 1996 (Act No. 26 of 1996)",
        aliases=["Arbitration Act 1996", "ADR Act India"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice & Commercial Law",
        topic_taxonomy=["Domestic Arbitration", "International Commercial Arbitration", "Section 9 Interim Relief", "Section 34 Setting Aside Award"],
        source_url="https://www.indiacode.nic.in/handle/123456789/1978",
        enactment_date="1996-08-16",
        commencement_date="1996-08-22",
        effective_date="1996-08-22",
        version="As amended (2015, 2019, 2021)",
        amendment_history=["Arbitration Amendment Acts of 2015, 2019, 2021"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Key commercial dispute resolution statute in India.",
        review_requirements="Section 9 and Section 34 grounds."
    ))

    # 21. IND-STAT-COMP-2013: Companies Act, 2013
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-COMP-2013",
        official_title="The Companies Act, 2013 (Act No. 18 of 2013)",
        aliases=["Companies Act 2013", "Corporate Law India"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Business & Economic Law",
        topic_taxonomy=["Corporate Governance", "Directors Duties", "NCLT", "Oppression and Mismanagement", "Share Capital", "CSR"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2114",
        enactment_date="2013-08-29",
        commencement_date="2013-09-12",
        effective_date="2013-09-12",
        version="As amended (2017, 2019, 2020 decriminalization)",
        amendment_history=["Companies (Amendment) Act 2015, 2017, 2019, 2020"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Phased notifications across 2013-2014; major decriminalization of technical defaults in 2020.",
        review_requirements="High-frequency corporate governance queries."
    ))

    # 22. IND-STAT-IBC-2016: Insolvency and Bankruptcy Code, 2016
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-IBC-2016",
        official_title="The Insolvency and Bankruptcy Code, 2016 (Act No. 31 of 2016)",
        aliases=["IBC 2016", "Insolvency Code"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Business & Economic Law",
        topic_taxonomy=["CIRP", "Liquidation", "Section 7 Financial Creditor", "Section 9 Operational Creditor", "Moratorium Section 14"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2155",
        enactment_date="2016-05-28",
        commencement_date="2016-08-05",
        effective_date="2016-08-05",
        version="As amended",
        amendment_history=["Multiple amendments 2017-2021"],
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Strict timelines; section 14 moratorium interaction with Section 138 NI Act.",
        review_requirements="Insolvency process triggers."
    ))

    # 23. IND-STAT-CPA-2019: Consumer Protection Act, 2019
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-CPA-2019",
        official_title="The Consumer Protection Act, 2019 (Act No. 35 of 2019)",
        aliases=["CPA 2019", "Consumer Protection Law"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Business & Economic Law",
        topic_taxonomy=["Consumer Rights", "Deficiency in Service", "Unfair Trade Practices", "Product Liability", "CCPA", "E-Commerce Rules"],
        source_url="https://www.indiacode.nic.in/handle/123456789/15256",
        enactment_date="2019-08-09",
        commencement_date="2020-07-20",
        effective_date="2020-07-20",
        version="Consolidated",
        repeal_metadata="Repealed Consumer Protection Act, 1986 under Section 107",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Includes e-commerce liability and mediation provisions.",
        review_requirements="District, State, and National Commission pecuniary jurisdiction."
    ))

    # 24. IND-STAT-PMLA-2002: Prevention of Money Laundering Act, 2002
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-PMLA-2002",
        official_title="The Prevention of Money Laundering Act, 2002 (Act No. 15 of 2003)",
        aliases=["PMLA 2002"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Criminal Law & Financial Regulation",
        topic_taxonomy=["Money Laundering", "Attachment of Property", "Section 3 Offence", "Section 45 Twin Bail Conditions", "ED Powers"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2053",
        enactment_date="2003-01-17",
        commencement_date="2005-07-01",
        effective_date="2005-07-01",
        version="As amended by Finance Acts up to 2023",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Twin conditions for bail under Section 45 affirmed in Vijay Madanlal Choudhary (2022).",
        review_requirements="Stringent bail conditions and burden of proof."
    ))

    # 25. IND-STAT-TELECOM-2023: Telecommunications Act, 2023
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-TELECOM-2023",
        official_title="The Telecommunications Act, 2023 (Act No. 44 of 2023)",
        aliases=["Telecom Act 2023"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Technology & Emerging Regulation",
        topic_taxonomy=["Telecommunications", "Spectrum Authorization", "Interception Rules", "Digital Infrastructure"],
        source_url="https://www.indiacode.nic.in/handle/123456789/20005",
        enactment_date="2023-12-24",
        commencement_date="2024-06-26",
        effective_date="2024-06-26",
        version="1.0.0",
        repeal_metadata="Repeals Indian Telegraph Act 1885 and Indian Wireless Telegraphy Act 1933 upon phased notification",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Certain provisions commenced 26 June 2024; rest pending.",
        review_requirements="Phased commencement tracking."
    ))

    # 26. IND-STAT-EPA-1986: Environment (Protection) Act, 1986
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-EPA-1986",
        official_title="The Environment (Protection) Act, 1986 (Act No. 29 of 1986)",
        aliases=["EPA 1986", "Environment Act"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Environment, Land & Infrastructure",
        topic_taxonomy=["Environmental Protection", "EIA", "Pollution Control", "Central Government Powers", "NGT Jurisdiction"],
        source_url="https://www.indiacode.nic.in/handle/123456789/1660",
        enactment_date="1986-05-23",
        commencement_date="1986-11-19",
        effective_date="1986-11-19",
        version="Consolidated",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Umbrella legislation for air, water, and biological diversity conservation.",
        review_requirements="Environmental clearance guidelines."
    ))

    # 27. IND-STAT-RERA-2016: Real Estate (Regulation and Development) Act, 2016
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-STAT-RERA-2016",
        official_title="The Real Estate (Regulation and Development) Act, 2016 (Act No. 16 of 2016)",
        aliases=["RERA 2016", "Real Estate Act"],
        issuing_authority="Parliament of India",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Environment, Land & Infrastructure",
        topic_taxonomy=["Real Estate Regulation", "Allottee Rights", "Homebuyers", "Project Registration", "Escrow Account", "RERA Authority"],
        source_url="https://www.indiacode.nic.in/handle/123456789/2158",
        enactment_date="2016-03-25",
        commencement_date="2016-05-01",
        effective_date="2017-05-01",
        version="Consolidated",
        authenticity_status="official_gazette",
        licence_or_terms="Government of India Open Data License (GODL-India)",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Concurrent state rules (e.g. MahaRERA, HRERA) establish state-level tribunals.",
        review_requirements="High public-benefit value for individual homebuyers."
    ))

    # --- Landmark Precedent Corpus Inventory ---

    # 28. IND-JUD-SC-1973-KESAVANANDA: Basic Structure Doctrine
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1973-KESAVANANDA",
        official_title="Kesavananda Bharati Sripadagalvaru v. State of Kerala (1973) 4 SCC 225",
        aliases=["Kesavananda Bharati", "Fundamental Rights Case", "Basic Structure Case", "AIR 1973 SC 1461"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Basic Structure Doctrine", "Constitutional Amendment", "Article 368", "Judicial Review", "Supremacy of Constitution"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1973-04-24",
        version="13-Judge Bench Holding",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Highest authority on constitutional amending power limitations.",
        review_requirements="Authoritative ratio summary."
    ))

    # 29. IND-JUD-SC-1978-MANEKA: Due Process / Article 21
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1978-MANEKA",
        official_title="Maneka Gandhi v. Union of India (1978) 1 SCC 248",
        aliases=["Maneka Gandhi Passport Case", "AIR 1978 SC 597"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Article 21", "Right to Travel", "Substantive Due Process", "Golden Triangle (Arts 14, 19, 21)", "Natural Justice"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1978-01-25",
        version="7-Judge Bench Holding",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Established that procedure established by law must be just, fair, and reasonable.",
        review_requirements="Golden Triangle jurisprudence."
    ))

    # 30. IND-JUD-SC-1980-MINERVA: Directive Principles and Fundamental Rights
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1980-MINERVA",
        official_title="Minerva Mills Ltd. v. Union of India (1980) 3 SCC 625",
        aliases=["Minerva Mills", "AIR 1980 SC 1789"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Harmonious Construction", "Part III & Part IV Balance", "Basic Structure", "Article 31C"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1980-07-31",
        version="5-Judge Constitution Bench",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Balance between Fundamental Rights and Directive Principles is part of the basic structure.",
        review_requirements="Article 368(4) and (5) striking down."
    ))

    # 31. IND-JUD-SC-1992-INDRA: Affirmative Action & 50% Rule
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1992-INDRA",
        official_title="Indra Sawhney v. Union of India (1992) Supp (3) SCC 217",
        aliases=["Mandal Case", "Mandal Commission Judgment", "AIR 1993 SC 477"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Reservation", "Article 16(4)", "Creamy Layer", "50 Percent Ceiling", "OBC Reservation"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1992-11-16",
        version="9-Judge Constitution Bench",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Leading precedent on reservations in public employment and backward classes identification.",
        review_requirements="50% cap and creamy layer doctrine."
    ))

    # 32. IND-JUD-SC-1994-BOMMAI: Federalism & Article 356
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1994-BOMMAI",
        official_title="S.R. Bommai v. Union of India (1994) 3 SCC 1",
        aliases=["Bommai Judgment", "AIR 1994 SC 1918"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Federalism", "Article 356", "President's Rule", "Secularism as Basic Structure", "Floor Test"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1994-03-11",
        version="9-Judge Constitution Bench",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Stringent guidelines on the invocation of Article 356 and preservation of elected state assemblies.",
        review_requirements="Floor test mandatory requirement."
    ))

    # 33. IND-JUD-SC-1997-VISHAKA: Sexual Harassment at Workplace
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-1997-VISHAKA",
        official_title="Vishaka v. State of Rajasthan (1997) 6 SCC 241",
        aliases=["Vishaka Guidelines", "AIR 1997 SC 3011"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Employment & Social Protection",
        topic_taxonomy=["Workplace Sexual Harassment", "Gender Equality", "Article 14", "Article 21", "POSH Act Origin"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="1997-08-13",
        version="3-Judge Bench Holding",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.HISTORICAL,
        indexed_chunk_count=0,
        repeal_metadata="Guidelines codified into statute by Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        coverage_gap_notes="Judicial guidelines operating as law until codified by 2013 POSH Act.",
        review_requirements="Codification relationship with POSH Act 2013."
    ))

    # 34. IND-JUD-SC-2018-NAVTEJ: Decriminalization of Section 377
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-2018-NAVTEJ",
        official_title="Navtej Singh Johar v. Union of India (2018) 10 SCC 1",
        aliases=["Section 377 Decriminalization", "Navtej Johar", "AIR 2018 SC 4321"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["LGBTQ+ Rights", "Section 377 IPC", "Article 14", "Article 15", "Article 19(1)(a)", "Article 21", "Constitutional Morality"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="2018-09-06",
        version="5-Judge Constitution Bench",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Overruled Suresh Kumar Koushal v. Naz Foundation (2014) 1 SCC 1.",
        review_requirements="Decriminalization of consensual sexual acts in private."
    ))

    # 35. IND-JUD-SC-2018-JOSEPH: Decriminalization of Adultery
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-2018-JOSEPH",
        official_title="Joseph Shine v. Union of India (2018) 2 SCC 189",
        aliases=["Joseph Shine", "Section 497 IPC Unconstitutional", "AIR 2018 SC 4898"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Public Law",
        topic_taxonomy=["Section 497 IPC", "Section 198(2) CrPC", "Gender Equality", "Autonomy of Women", "Article 14", "Article 15", "Article 21"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="2018-09-27",
        version="5-Judge Constitution Bench",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Struck down Section 497 IPC as unconstitutional; reflected in BNS 2023 which omits adultery as a criminal offence.",
        review_requirements="Interplay with BNS 2023 omission of criminal adultery."
    ))

    # 36. IND-JUD-SC-2020-BABITA: Permanent Commission for Women in Armed Forces
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-2020-BABITA",
        official_title="Secretary, Ministry of Defence v. Babita Puniya (2020) 7 SCC 469",
        aliases=["Babita Puniya", "Women in Armed Forces", "AIR 2020 SC 1110"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Employment Law",
        topic_taxonomy=["Gender Justice", "Armed Forces", "Permanent Commission", "Article 14", "Article 15", "Non-Discrimination"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="2020-02-17",
        version="2-Judge Bench Holding",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Affirmed constitutional right of women officers to permanent commission and command criteria parity.",
        review_requirements="Equality in public defense service."
    ))

    # 37. IND-JUD-SC-2024-SUKANYA: Caste Discrimination in Prison Manuals
    mgr.add_item(CorpusInventoryItem(
        document_id="IND-JUD-SC-2024-SUKANYA",
        official_title="Sukanya Shantha v. Union of India 2024 INSC 753",
        aliases=["Prison Manuals Caste Case", "Sukanya Shantha"],
        issuing_authority="Supreme Court of India",
        jurisdiction="IN",
        document_class=DocumentClass.JUDGMENT,
        legal_domain="Constitutional & Criminal Justice",
        topic_taxonomy=["Prison Reforms", "Article 14", "Article 15", "Article 17 Untouchability", "Article 21", "Article 23 Forced Labour", "State Prison Rules"],
        source_url="https://main.sci.gov.in/judgments",
        publication_date="2024-10-03",
        version="3-Judge Bench Holding (CJI DY Chandrachud, JB Pardiwala, Manoj Misra)",
        authenticity_status="supreme_court_record",
        licence_or_terms="Public Domain / Supreme Court Records",
        extraction_status="pending",
        validation_status="pending",
        corpus_status=CorpusStatus.CURRENT,
        indexed_chunk_count=0,
        coverage_gap_notes="Invalidated discriminatory caste-based labor and barracks segregation in State Prison Manuals.",
        review_requirements="State prison rules compliance and revision tracking."
    ))

    return mgr


def main() -> None:
    print("Building LegalMitra National Indian Legal Corpus Inventory...")
    mgr = build_inventory()
    items = mgr.list_items()
    print(f"Total inventory items compiled: {len(items)}")

    json_path = Path("data/08_corpus/coverage_inventory.json")
    csv_path = Path("data/08_corpus/coverage_inventory.csv")

    mgr.export_json(json_path)
    print(f"Exported JSON inventory: {json_path} ({json_path.stat().st_size} bytes)")

    mgr.export_csv(csv_path)
    print(f"Exported CSV inventory: {csv_path} ({csv_path.stat().st_size} bytes)")

    print("\nSummary by Status:")
    for status in CorpusStatus:
        matching = mgr.filter_by_status(status)
        print(f"  - {status.value}: {len(matching)}")

    print("\nSummary by Document Class:")
    for doc_class in DocumentClass:
        matching = [i for i in items if i.document_class == doc_class]
        if matching:
            print(f"  - {doc_class.value}: {len(matching)}")


if __name__ == "__main__":
    main()

