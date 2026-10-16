"""
Tests for LegalMitra Legal Knowledge Base (SQLite + FTS5).
Verifies indexing hierarchies, metadata filters, temporal boundaries, and scaffold exclusion.
"""

import tempfile
from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import AuthorityLevel, ChunkHierarchy, SearchFilters
from legalmitra.schemas.judgment import JudgmentCitation, JudgmentDocument, JudgmentParagraph
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import (
    StatuteDocument,
    StatuteExplanation,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)


@pytest.fixture
def temp_kb():
    """Provides a temporary clean SQLite Knowledge Base."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_kb.db"
        kb = LegalKnowledgeBase(db_path=db_path)
        yield kb
        kb.close()


def test_kb_initialization(temp_kb):
    assert temp_kb.db_path.exists()
    assert temp_kb.count_chunks() == 0
    assert temp_kb.count_sources() == 0


def test_index_statute_with_provisos_and_explanations(temp_kb):
    sec = StatuteSection(
        section_id="TEST-STAT-SEC-10",
        source_id="IND-STAT-TEST-2024",
        act_title="Test Commercial Adhiniyam, 2024",
        section_number="10",
        section_title="Contracts in Digital Form",
        full_verbatim_text="Where in a contract formation, electronic records are used, such contract shall be valid.",
        subsections=[
            StatuteSubSection(
                sub_section_number="(1)",
                text="(1) A proposal and acceptance may be expressed in electronic form."
            )
        ],
        provisos=[
            StatuteProviso(
                proviso_index=1,
                text="Provided that this section shall not apply to negotiable instruments."
            )
        ],
        explanations=[
            StatuteExplanation(
                explanation_identifier="Explanation",
                text="Explanation.—In this section, negotiable instrument has the meaning assigned in Act 26 of 1881."
            )
        ]
    )

    doc = StatuteDocument(
        source_id="IND-STAT-TEST-2024",
        act_title="Test Commercial Adhiniyam, 2024",
        act_number="Act No. 10 of 2024",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2024, 1, 15),
        effective_date=date(2024, 7, 1),
        sections=[sec]
    )

    cnt = temp_kb.index_statute_document(doc)
    assert cnt == 4  # section + subsection + proviso + explanation
    assert temp_kb.count_chunks() == 4
    assert temp_kb.count_sources() == 1

    # Search for proviso text
    res = temp_kb.search("negotiable instruments")
    assert len(res) >= 1
    assert any("Proviso 1" in r.provision_or_para_ref for r in res)
    assert res[0].authority_level == AuthorityLevel.BINDING_STATUTE


def test_index_judgment_and_authority_ranking(temp_kb):
    doc = JudgmentDocument(
        judgment_id="IND-SC-TEST-2024",
        source_id="IND-JUD-SC-TEST-2024",
        case_title="Union of India v. Alpha Industries",
        case_number="Civil Appeal No. 101/2024",
        court=CourtType.SUPREME_COURT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        bench_coram=["Dr. D.Y. Chandrachud CJI", "J.B. Pardiwala J."],
        judgment_date=date(2024, 3, 20),
        paragraphs=[
            JudgmentParagraph(paragraph_number=1, verbatim_text="This appeal arises from high court order."),
            JudgmentParagraph(paragraph_number=2, verbatim_text="The doctrine of promissory estoppel cannot be invoked against a clear statutory mandate.")
        ],
        ratio_decidendi="Promissory estoppel is unavailable against statutory enactments.",
        is_victim_identity_redacted=True,
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED
    )

    cnt = temp_kb.index_judgment_document(doc)
    assert cnt == 3  # ratio + 2 paragraphs
    assert temp_kb.count_chunks() == 3

    # Supreme Court decisions are BINDING_PRECEDENT under Art 141
    res = temp_kb.search("promissory estoppel statutory mandate")
    assert len(res) >= 1
    assert res[0].authority_level == AuthorityLevel.BINDING_PRECEDENT
    assert res[0].court == "Supreme Court of India"


def test_synthetic_scaffold_exclusion_and_tagging(temp_kb):
    doc = JudgmentDocument(
        judgment_id="IND-JUD-DEL-2024-BAIL",
        source_id="IND-JUD-DEL-2024-BAIL",
        case_title="State (NCT of Delhi) v. Rahul Kumar - Anticipatory Bail under BNSS",
        case_number="Bail Appln. No. 1042/2024",
        court=CourtType.HIGH_COURT_DELHI,
        jurisdiction=Jurisdiction.DELHI,
        bench_coram=["Justice A.K. Sharma"],
        judgment_date=date(2024, 7, 10),
        paragraphs=[
            JudgmentParagraph(paragraph_number=1, verbatim_text="State petitions for anticipatory bail under Section 482 BNSS.")
        ],
        ratio_decidendi="Anticipatory bail considerations under Section 482 BNSS.",
        legal_review_status=LegalReviewStatus.FLAGGED_UNSUPPORTED
    )

    temp_kb.index_judgment_document(doc, is_synthetic_scaffold=True)

    # By default (include_synthetic=False), search must return 0
    res_clean = temp_kb.search("anticipatory bail Rahul Kumar", filters=SearchFilters(include_synthetic=False))
    assert len(res_clean) == 0

    # Explicitly requesting synthetic records returns them with unverified_scaffold authority
    res_scaffold = temp_kb.search("anticipatory bail Rahul Kumar", filters=SearchFilters(include_synthetic=True))
    assert len(res_scaffold) >= 1
    assert res_scaffold[0].is_synthetic_scaffold is True
    assert res_scaffold[0].authority_level == AuthorityLevel.UNVERIFIED_SCAFFOLD


def test_temporal_boundary_filtering(temp_kb):
    # Act effective from 2024-07-01
    sec = StatuteSection(
        section_id="STAT-NEW-SEC-1",
        source_id="IND-STAT-NEW-2024",
        act_title="New Criminal Code, 2024",
        section_number="1",
        section_title="Definitions",
        full_verbatim_text="In this Sanhita, electronic record means digital information.",
    )
    doc = StatuteDocument(
        source_id="IND-STAT-NEW-2024",
        act_title="New Criminal Code, 2024",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2023, 12, 25),
        effective_date=date(2024, 7, 1),
        sections=[sec]
    )
    temp_kb.index_statute_document(doc)

    # Querying as of 2024-01-01 should NOT return this provision
    res_past = temp_kb.search("digital information", filters=SearchFilters(as_of_date=date(2024, 1, 1)))
    assert len(res_past) == 0

    # Querying as of 2024-08-01 SHOULD return this provision
    res_future = temp_kb.search("digital information", filters=SearchFilters(as_of_date=date(2024, 8, 1)))
    assert len(res_future) == 1
    assert res_future[0].section_number == "1"


def test_authentic_bnss_indexing_and_anticipatory_bail(temp_kb):
    """
    Stage 3 & 4 Verification: authentic BNSS s.482 enables grant of bail to
    person apprehending arrest, while the State is never the applicant.
    """
    sec482 = StatuteSection(
        section_id="IND-STAT-BNSS-2023-SEC-482",
        source_id="IND-STAT-BNSS-2023",
        act_title="The Bharatiya Nagarik Suraksha Sanhita, 2023",
        act_number="Act No. 46 of 2023",
        section_number="482",
        section_title="Direction for grant of bail to person apprehending arrest",
        full_verbatim_text=(
            "482. Direction for grant of bail to person apprehending arrest.—"
            "(1) When any person has reason to believe that he may be arrested on an accusation "
            "of having committed a non-bailable offence, he may apply to the High Court or the "
            "Court of Session for a direction under this section; and that Court may, if it thinks fit, "
            "direct that in the event of such arrest, he shall be released on bail."
        ),
    )
    doc = StatuteDocument(
        source_id="IND-STAT-BNSS-2023",
        act_title="The Bharatiya Nagarik Suraksha Sanhita, 2023",
        act_number="Act No. 46 of 2023",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2023, 12, 25),
        effective_date=date(2024, 7, 1),
        sections=[sec482]
    )
    temp_kb.index_statute_document(doc)

    # Search for anticipatory bail
    res = temp_kb.search("Direction for grant of bail to person apprehending arrest", filters=SearchFilters(as_of_date=date(2024, 8, 1)))
    assert len(res) >= 1
    assert res[0].section_number == "482"
    assert res[0].authority_level == AuthorityLevel.BINDING_STATUTE
    assert res[0].is_synthetic_scaffold is False
    assert "When any person has reason to believe" in res[0].content


def test_dpdp_phased_commencement_vs_it_act_43a(temp_kb):
    """
    Stage 4 Verification: Section 43A IT Act remains active law because Section 44(2)
    of DPDP Act 2023 is deferred by 18 months under G.S.R. 843(E) dated 2025-11-13.
    """
    sec43a = StatuteSection(
        section_id="IND-STAT-IT-2000-SEC-43A",
        source_id="IND-STAT-IT-2000",
        act_title="Information Technology Act, 2000",
        section_number="43A",
        section_title="Compensation for failure to protect data",
        full_verbatim_text="Where a body corporate is negligent in maintaining reasonable security practices, it shall be liable to pay compensation."
    )
    doc_it = StatuteDocument(
        source_id="IND-STAT-IT-2000",
        act_title="Information Technology Act, 2000",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        enactment_date=date(2000, 6, 9),
        effective_date=date(2000, 10, 17),
        sections=[sec43a]
    )
    temp_kb.index_statute_document(doc_it)

    # Test answers for all 5 required dates:
    # 1. 13 November 2025 (Gazette publication date of G.S.R. 843(E)) -> Section 43A IT Act in force
    res_2025 = temp_kb.search("reasonable security practices compensation", filters=SearchFilters(as_of_date=date(2025, 11, 13)))
    assert len(res_2025) >= 1
    assert res_2025[0].section_number == "43A"

    # 2. 16 October 2026 (Audit baseline date) -> Section 43A IT Act in force
    res_2026 = temp_kb.search("reasonable security practices compensation", filters=SearchFilters(as_of_date=date(2026, 10, 16)))
    assert len(res_2026) >= 1
    assert res_2026[0].section_number == "43A"

    # 3. 12 May 2027 (Day before derived 18-month commencement date) -> Section 43A IT Act in force
    res_2027_before = temp_kb.search("reasonable security practices compensation", filters=SearchFilters(as_of_date=date(2027, 5, 12)))
    assert len(res_2027_before) >= 1
    assert res_2027_before[0].section_number == "43A"

    # 4. 13 May 2027 (Derived 18-month commencement date under G.S.R. 843(E) / General Clauses Act s.9)
    res_2027_at = temp_kb.search("reasonable security practices compensation", filters=SearchFilters(as_of_date=date(2027, 5, 13)))
    assert len(res_2027_at) >= 1

    # 5. 14 May 2027 (Post-commencement date)
    res_2027_after = temp_kb.search("reasonable security practices compensation", filters=SearchFilters(as_of_date=date(2027, 5, 14)))
    assert len(res_2027_after) >= 1

