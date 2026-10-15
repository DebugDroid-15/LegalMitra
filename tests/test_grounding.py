"""
Tests for LegalMitra Source Grounding and Traceability Verification.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import LegalReviewStatus, SourceType
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.validation.grounding_validator import GroundingValidator


def test_grounding_valid_evidence(temp_env_dir):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    rec = SourceRegistryRecord(
        document_id="IND-STAT-BSA-2023",
        title="Bharatiya Sakshya Adhiniyam, 2023",
        source_url="https://indiacode.nic.in/bsa",
        source_type=SourceType.STATUTE,
        document_date=date(2023, 12, 25),
        licence_or_terms="GODL-India",
        checksum="3" * 64,
        raw_file_path="/tmp/bsa.txt",
        file_format=".txt",
        byte_size=1000,
    )
    mgr.register(rec)

    validator = GroundingValidator(mgr)

    source_text = "61. Admissibility of electronic records.—Nothing in this Adhiniyam shall apply to deny admissibility."
    ev = EvidencePassage(
        source_id="IND-STAT-BSA-2023",
        section_or_para_ref="Section 61",
        verbatim_text="Nothing in this Adhiniyam shall apply to deny admissibility.",
    )

    qa = LegalQADocument(
        qa_id="QA-TEST-001",
        question="Can electronic records be admitted under Section 61?",
        answer="Under Section 61, nothing in this Adhiniyam shall apply to deny admissibility of electronic records.",
        supporting_source_ids=["IND-STAT-BSA-2023"],
        evidence_passages=[ev],
        legal_domain="Evidence Law",
    )

    is_grounded, issues = validator.validate_grounding(qa, source_texts={"IND-STAT-BSA-2023": source_text})
    assert is_grounded is True
    assert len(issues) == 0
    assert qa.flagged_unsupported is False


def test_grounding_detects_unregistered_source(temp_env_dir):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    validator = GroundingValidator(mgr)

    ev = EvidencePassage(
        source_id="NON-EXISTENT-SOURCE",
        section_or_para_ref="Section 1",
        verbatim_text="Some text",
    )
    qa = LegalQADocument(
        qa_id="QA-TEST-002",
        question="Is this legal query backed by an authoritative Indian statute?",
        answer="Answer without valid registered source.",
        supporting_source_ids=["NON-EXISTENT-SOURCE"],
        evidence_passages=[ev],
        legal_domain="Evidence Law",
    )

    is_grounded, issues = validator.validate_grounding(qa)
    assert is_grounded is False
    assert any("not registered in the Source Registry" in issue for issue in issues)
    assert qa.flagged_unsupported is True
    assert qa.legal_review_status == LegalReviewStatus.FLAGGED_UNSUPPORTED


def test_grounding_detects_invented_statutory_section(temp_env_dir):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    rec = SourceRegistryRecord(
        document_id="IND-STAT-BSA-2023",
        title="Bharatiya Sakshya Adhiniyam, 2023",
        source_url="https://indiacode.nic.in/bsa",
        source_type=SourceType.STATUTE,
        document_date=date(2023, 12, 25),
        licence_or_terms="GODL-India",
        checksum="4" * 64,
        raw_file_path="/tmp/bsa.txt",
        file_format=".txt",
        byte_size=1000,
    )
    mgr.register(rec)

    validator = GroundingValidator(mgr)

    # Evidence only mentions Section 61
    ev = EvidencePassage(
        source_id="IND-STAT-BSA-2023",
        section_or_para_ref="Section 61",
        verbatim_text="Section 61. Admissibility of electronic records.",
    )

    # Answer hallucinates Section 999
    qa = LegalQADocument(
        qa_id="QA-TEST-003",
        question="Which section governs electronic records?",
        answer="Under Section 999, electronic records are admissible.",
        supporting_source_ids=["IND-STAT-BSA-2023"],
        evidence_passages=[ev],
        legal_domain="Evidence Law",
    )

    is_grounded, issues = validator.validate_grounding(qa)
    assert is_grounded is False
    assert any("Section 999" in issue for issue in issues)
    assert qa.flagged_unsupported is True
    assert qa.legal_review_status == LegalReviewStatus.FLAGGED_UNSUPPORTED
