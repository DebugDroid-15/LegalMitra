"""
Tests for LegalMitra Pydantic Schemas.
Verifies structure, validation constraints, and explicit legal review statuses.
"""

from datetime import date
import pytest
from pydantic import ValidationError

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.drafting_example import DraftingClause, DraftingExampleDocument
from legalmitra.schemas.evaluation import EvaluationQuestionDocument, EvaluationRubric
from legalmitra.schemas.judgment import CaseHolding, JudgmentCitation, JudgmentDocument, JudgmentParagraph
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument, ProceduralStep
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import (
    StatuteClause,
    StatuteDocument,
    StatuteExplanation,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)


def test_source_registry_record_valid():
    rec = SourceRegistryRecord(
        document_id="IND-STAT-TEST-001",
        title="Test Statute Title",
        source_url="https://indiacode.nic.in/test",
        source_type=SourceType.STATUTE,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        document_date=date(2023, 12, 25),
        licence_or_terms="GODL-India",
        checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        raw_file_path="/tmp/test.txt",
        file_format=".txt",
        byte_size=100,
    )
    assert rec.document_id == "IND-STAT-TEST-001"
    assert rec.verification_status == LegalReviewStatus.UNVERIFIED_AUTOMATED


def test_source_registry_record_invalid_checksum():
    with pytest.raises(ValidationError):
        SourceRegistryRecord(
            document_id="IND-STAT-TEST-001",
            title="Test Statute Title",
            source_url="https://indiacode.nic.in/test",
            source_type=SourceType.STATUTE,
            document_date=date(2023, 12, 25),
            licence_or_terms="GODL-India",
            checksum="invalid_hex_checksum",
            raw_file_path="/tmp/test.txt",
            file_format=".txt",
            byte_size=100,
        )


def test_statute_schemas():
    clause = StatuteClause(clause_number="(a)", text="the electronic record was produced during regular operation")
    sub = StatuteSubSection(sub_section_number="(1)", text="Electronic records admissibility.", clauses=[clause])
    proviso = StatuteProviso(proviso_index=1, text="Provided that certificate under section 63(4) is produced.")
    expl = StatuteExplanation(explanation_identifier="Explanation", text="Includes microfilms and computer printouts.")

    sec = StatuteSection(
        section_id="BSA-SEC-61",
        source_id="IND-STAT-BSA-2023",
        act_title="Bharatiya Sakshya Adhiniyam, 2023",
        section_number="61",
        section_title="Admissibility of electronic records",
        full_verbatim_text="Section 61 text...",
        subsections=[sub],
        provisos=[proviso],
        explanations=[expl],
    )
    assert sec.legal_review_status == LegalReviewStatus.UNVERIFIED_AUTOMATED

    doc = StatuteDocument(
        source_id="IND-STAT-BSA-2023",
        act_title="Bharatiya Sakshya Adhiniyam, 2023",
        enactment_date=date(2023, 12, 25),
        sections=[sec],
    )
    assert len(doc.sections) == 1
    assert doc.sections[0].subsections[0].clauses[0].clause_number == "(a)"


def test_judgment_schemas():
    para = JudgmentParagraph(paragraph_number=1, verbatim_text="This appeal raises a question of constitutional importance.")
    cit = JudgmentCitation(citation_text="(2017) 10 SCC 1", reporter="SCC", year=2017)
    holding = CaseHolding(issue_number=1, issue_text="Is privacy a fundamental right?", holding_summary="Yes, under Article 21.")

    jd = JudgmentDocument(
        judgment_id="IND-SC-2017-PUTTASWAMY",
        source_id="IND-SC-2017-PUTTASWAMY",
        case_title="Justice K.S. Puttaswamy (Retd.) v. Union of India",
        court=CourtType.SUPREME_COURT,
        bench_coram=["J.S. Khehar, CJI", "D.Y. Chandrachud, J."],
        judgment_date=date(2017, 8, 24),
        citations=[cit],
        paragraphs=[para],
        holdings=[holding],
        ratio_decidendi="Right to privacy is an intrinsic part of the right to life under Article 21.",
    )
    assert jd.court == CourtType.SUPREME_COURT
    assert jd.is_victim_identity_redacted is True
    assert jd.legal_review_status == LegalReviewStatus.UNVERIFIED_AUTOMATED


def test_legal_qa_schema():
    ev = EvidencePassage(
        source_id="IND-STAT-BSA-2023",
        section_or_para_ref="Section 61",
        verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record.",
        page_number=1,
    )
    qa = LegalQADocument(
        qa_id="QA-BSA-001",
        question="Can electronic records be denied admissibility under Bharatiya Sakshya Adhiniyam, 2023?",
        answer="Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023, electronic or digital records cannot be denied admissibility solely on the ground of being in electronic form.",
        supporting_source_ids=["IND-STAT-BSA-2023"],
        evidence_passages=[ev],
        legal_domain="Criminal Law - Evidence",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
    )
    assert qa.supporting_source_ids == ["IND-STAT-BSA-2023"]
    assert "educational and analytical purposes" in qa.legal_disclaimer


def test_case_analysis_schema():
    ev = EvidencePassage(
        source_id="IND-SC-2017-PUTTASWAMY",
        section_or_para_ref="Paragraph 4",
        verbatim_text="Privacy is a constitutionally protected right under Article 21.",
    )
    ca = CaseAnalysisDocument(
        analysis_id="CA-PUTTASWAMY-001",
        case_id="IND-SC-2017-PUTTASWAMY",
        case_title="Justice K.S. Puttaswamy v. Union of India",
        court=CourtType.SUPREME_COURT,
        judgment_date=date(2017, 8, 24),
        factual_matrix_summary="Constitutional challenge to Aadhaar scheme on privacy grounds.",
        issues_raised=["Whether the right to privacy is guaranteed under Part III of the Constitution?"],
        ratio_decidendi="Privacy is intrinsic to life and personal liberty guaranteed under Article 21.",
        precedential_value="Binding Constitutional 9-Judge Precedent under Article 141",
        supporting_source_ids=["IND-SC-2017-PUTTASWAMY"],
        evidence_passages=[ev],
    )
    assert ca.court == CourtType.SUPREME_COURT
    assert len(ca.issues_raised) == 1


def test_procedural_guide_schema():
    step = ProceduralStep(
        step_number=1,
        step_title="Draft and Execute Anticipatory Bail Petition",
        action_description="Draft petition incorporating grounds of apprehension of arrest under BNS.",
        responsible_party="Advocate for Applicant",
        statutory_rule="Section 482 of BNSS, 2023",
        timeline_or_deadline="Prior to actual arrest by police",
    )
    ev = EvidencePassage(
        source_id="IND-STAT-BNSS-2023",
        section_or_para_ref="Section 482",
        verbatim_text="Direction for grant of bail to person apprehending arrest.",
    )
    guide = ProceduralGuidanceDocument(
        guide_id="PROC-BNSS-482-BAIL",
        procedure_title="Filing Anticipatory Bail Application under BNSS",
        governing_statutes=["Bharatiya Nagarik Suraksha Sanhita, 2023"],
        forum_or_court="Court of Session or High Court",
        steps=[step],
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[ev],
    )
    assert guide.steps[0].step_number == 1


def test_drafting_example_schema():
    clause = DraftingClause(
        clause_heading="Verification Clause",
        clause_text="I, the Deponent abovenamed, do hereby verify that the contents of paragraphs 1 to 5 are true to my knowledge.",
        is_mandatory=True,
        statutory_rationale="Mandatory under Order XIX Rule 3 CPC and High Court Rules.",
    )
    ev = EvidencePassage(
        source_id="IND-STAT-BSA-2023",
        section_or_para_ref="Section 63(4)",
        verbatim_text="Certificate signed by person in official charge of the device.",
    )
    draft = DraftingExampleDocument(
        template_id="DRAFT-BSA-CERT-001",
        template_title="Electronic Evidence Certificate under Section 63(4) BSA",
        category="Statutory Certificate",
        court_or_authority="Competent Trial Court",
        statutory_basis="Section 63(4) of Bharatiya Sakshya Adhiniyam, 2023",
        clauses=[clause],
        full_draft_template="I, [NAME OF DEPONENT], official in-charge of [DEVICE] certify that the records were produced during regular course of activity...",
        placeholders=["[NAME OF DEPONENT]", "[DEVICE]"],
        supporting_source_ids=["IND-STAT-BSA-2023"],
        evidence_passages=[ev],
    )
    assert "[DEVICE]" in draft.placeholders


def test_evaluation_question_schema():
    ev = EvidencePassage(
        source_id="IND-STAT-BSA-2023",
        section_or_para_ref="Section 61",
        verbatim_text="Admissibility of electronic records.",
    )
    eval_q = EvaluationQuestionDocument(
        eval_id="EVAL-BSA-001",
        question="Which provision of Bharatiya Sakshya Adhiniyam, 2023 governs admissibility of electronic records?",
        expected_answer="Section 61 of Bharatiya Sakshya Adhiniyam, 2023.",
        target_statute_or_case="Bharatiya Sakshya Adhiniyam, 2023",
        golden_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        forbidden_terms_or_repealed_citations=["Section 65B, Indian Evidence Act, 1872"],
        rubric=EvaluationRubric(accuracy_weight=0.5, statutory_citation_weight=0.5),
        supporting_source_ids=["IND-STAT-BSA-2023"],
        evidence_passages=[ev],
        legal_domain="Criminal Law - Evidence",
    )
    assert "Section 65B, Indian Evidence Act, 1872" in eval_q.forbidden_terms_or_repealed_citations

