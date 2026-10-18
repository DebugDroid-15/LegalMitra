"""
Phase 35 National Legal Data Engine, Source Verification & Corpus Scaling Tests.
Tests:
1. Finite State Machine (FSM) lifecycle transitions and illegal transition rejection.
2. Source discovery prioritization based on legal importance, Hindi language gap, and rights.
3. Secure acquisition engine SSRF, private IP, and redirect validation.
4. Legal parser hierarchy extraction and defect detection (truncation, mojibake, header/footer).
5. Corpus versioning and temporal repeal/replacement tracking.
6. Corpus quality audit and source-grouped zero-leakage validation.
7. Training export pipeline with scaffold quarantine and dry-run mode.
"""

import json
from pathlib import Path
import pytest

from legalmitra.corpus.corpus_versioning import NationalCorpusVersioningEngine, VersionChangeType
from legalmitra.corpus.legal_parser import DefectSeverity, LegalDocumentParser
from legalmitra.corpus.quality_engine import CorpusQualityEngine
from legalmitra.corpus.secure_acquisition_engine import AcquisitionErrorType, SecureAcquisitionEngine
from legalmitra.corpus.source_discovery import DocumentCategory, NationalSourceDiscoveryEngine, SourceCandidate
from legalmitra.corpus.source_registry_engine import (
    IllegalStateTransitionError,
    SourceLifecycleState,
    UnifiedSourceRegistry,
)
from legalmitra.corpus.training_exporter import TrainingCorpusExporter


def test_fsm_source_lifecycle_transitions(tmp_path):
    registry_file = tmp_path / "test_registry.json"
    registry = UnifiedSourceRegistry(registry_file)

    entry = registry.register_discovered_source(
        source_id="TEST-STAT-2026",
        official_title="Test Legal Act 2026",
        issuing_authority="Parliament of India",
        source_url="https://www.indiacode.nic.in/handle/123456789/9999",
        source_type="statute",
        jurisdiction="IN",
        language="en",
        document_family="statutory",
        document_identifier="TEST-STAT-2026",
    )
    assert entry.current_state == SourceLifecycleState.DISCOVERED
    assert entry.pretraining_eligible is False

    # Sequential valid progression
    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.REGISTERED, "Metadata confirmed")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.REGISTERED

    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.ACQUIRED, "Downloaded cleanly")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.ACQUIRED

    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.PARSED, "Parsed successfully")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.PARSED

    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.AUTHENTICITY_VERIFIED, "Official Gazette match")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.AUTHENTICITY_VERIFIED

    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.RIGHTS_REVIEWED, "Section 52(1)(q) confirmed")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.RIGHTS_REVIEWED
    assert registry.get_source("TEST-STAT-2026").pretraining_eligible is False

    # Final eligibility gate
    registry.transition_state("TEST-STAT-2026", SourceLifecycleState.TRAINING_ELIGIBLE, "Cleared for manifest export")
    assert registry.get_source("TEST-STAT-2026").current_state == SourceLifecycleState.TRAINING_ELIGIBLE
    assert registry.get_source("TEST-STAT-2026").pretraining_eligible is True


def test_fsm_illegal_transition_rejection(tmp_path):
    registry_file = tmp_path / "test_registry.json"
    registry = UnifiedSourceRegistry(registry_file)

    registry.register_discovered_source(
        source_id="TEST-ILLEGAL-2026",
        official_title="Illegal Jump Act",
        issuing_authority="Parliament of India",
        source_url="https://www.indiacode.nic.in/handle/123456789/8888",
        source_type="statute",
        jurisdiction="IN",
        language="en",
        document_family="statutory",
        document_identifier="TEST-ILLEGAL-2026",
    )

    # Attempting to jump directly from DISCOVERED to TRAINING_ELIGIBLE must raise IllegalStateTransitionError
    with pytest.raises(IllegalStateTransitionError):
        registry.transition_state(
            "TEST-ILLEGAL-2026",
            SourceLifecycleState.TRAINING_ELIGIBLE,
            "Illegal skip without acquisition or rights review",
        )

    # Attempting to jump backwards from REGISTERED to DISCOVERED must raise error
    registry.transition_state("TEST-ILLEGAL-2026", SourceLifecycleState.REGISTERED, "Valid registration")
    with pytest.raises(IllegalStateTransitionError):
        registry.transition_state(
            "TEST-ILLEGAL-2026",
            SourceLifecycleState.DISCOVERED,
            "Illegal backward transition",
        )


def test_fsm_quarantine_isolation(tmp_path):
    registry_file = tmp_path / "test_registry.json"
    registry = UnifiedSourceRegistry(registry_file)

    registry.register_discovered_source(
        source_id="IND-JUD-DEL-2024-BAIL",
        official_title="Synthetic Scaffold Fixture",
        issuing_authority="Synthetic Court",
        source_url="https://delhihighcourt.nic.in/synthetic",
        source_type="judgment",
        jurisdiction="IN-DL",
        language="en",
        document_family="synthetic_scaffold",
        document_identifier="IND-JUD-DEL-2024-BAIL",
    )

    registry.transition_state(
        "IND-JUD-DEL-2024-BAIL",
        SourceLifecycleState.QUARANTINED,
        "Synthetic scaffold must remain quarantined",
        actor="security_gate",
    )

    entry = registry.get_source("IND-JUD-DEL-2024-BAIL")
    assert entry.current_state == SourceLifecycleState.QUARANTINED
    assert entry.pretraining_eligible is False
    assert entry not in registry.get_training_eligible_sources()


def test_source_discovery_prioritization(tmp_path):
    engine = NationalSourceDiscoveryEngine(tmp_path / "test_discovery.json")

    cand_en = SourceCandidate(
        candidate_id="CAND-EN-ACT",
        official_title="Central English Act",
        category=DocumentCategory.CENTRAL_ACT,
        jurisdiction="IN",
        language="en",
        official_portal="India Code",
        target_url="https://www.indiacode.nic.in/handle/123456789/100",
        issuing_authority="Parliament",
        enactment_or_decision_year=2020,
        has_section_52_exemption=True,
        expected_token_yield=10000,
    )
    cand_hi = SourceCandidate(
        candidate_id="CAND-HI-CODE",
        official_title="भारतीय आपराधिक संहिता",
        category=DocumentCategory.MULTILINGUAL_STATUTE,
        jurisdiction="IN",
        language="hi",
        official_portal="India Code",
        target_url="https://www.indiacode.nic.in/handle/123456789/200",
        issuing_authority="Parliament",
        enactment_or_decision_year=2023,
        has_section_52_exemption=True,
        expected_token_yield=10000,
    )

    engine.add_candidate(cand_en)
    engine.add_candidate(cand_hi)

    # Hindi statutory candidate must score higher due to language gap weighting
    assert cand_hi.priority_score > cand_en.priority_score
    ranked = engine.prioritize_candidates()
    assert ranked[0].candidate_id == "CAND-HI-CODE"


def test_secure_acquisition_ssrf_and_ip_checks(tmp_path):
    engine = SecureAcquisitionEngine(storage_dir=tmp_path / "storage", quarantine_dir=tmp_path / "quarantine")

    # Prohibited scheme
    ok, _, err, msg = engine.validate_url_and_ip("gopher://127.0.0.1/doc")
    assert ok is False
    assert err == AcquisitionErrorType.INVALID_SCHEME

    # Loopback IP
    ok, _, err, msg = engine.validate_url_and_ip("http://127.0.0.1:8000/legal")
    assert ok is False
    assert err in (AcquisitionErrorType.SSRF_BLOCKED, AcquisitionErrorType.PRIVATE_IP_BLOCKED)

    # Cloud metadata IP (169.254.169.254)
    ok, _, err, msg = engine.validate_url_and_ip("http://169.254.169.254/latest/meta-data")
    assert ok is False
    assert err == AcquisitionErrorType.SSRF_BLOCKED

    # Prohibited hostname localhost
    ok, _, err, msg = engine.validate_url_and_ip("http://localhost/admin")
    assert ok is False
    assert err == AcquisitionErrorType.SSRF_BLOCKED


def test_legal_parser_structure_and_defect_detection():
    parser = LegalDocumentParser()

    # Valid English statute text
    statute_text = """
    Section 1. Short Title and Commencement.
    (1) This Act may be called the Digital Law Act, 2026.
    (2) It shall come into force on such date as the Central Government may notify.

    Section 2. Definitions.
    In this Act, unless the context otherwise requires:
    (a) "court" means the Supreme Court or High Court.
    """
    doc = parser.parse_statute(statute_text, "DOC-STAT-001", "Digital Law Act, 2026")
    assert doc.is_valid_parse is True
    assert doc.total_provisions >= 2
    assert doc.nodes[0].reference == "Section 1"

    # Truncated document defect
    truncated_text = "Section 5. Confidential Disclosure without ending period"
    doc_trunc = parser.parse_statute(truncated_text, "DOC-TRUNC-001", "Truncated Act")
    assert any(d.defect_code == "ERR_TRUNCATED_TEXT" for d in doc_trunc.defects)
    assert doc_trunc.is_valid_parse is False

    # Devanagari replacement character corruption defect
    mojibake_text = "धारा 10. \ufffd\ufffd अप्राधिकृत प्रवेश।"
    doc_mojibake = parser.parse_statute(mojibake_text, "DOC-MOJI-001", "Corrupted Act", language="hi")
    assert any(d.defect_code == "ERR_DEVANAGARI_REPLACEMENT_CHAR" for d in doc_mojibake.defects)
    assert doc_mojibake.is_valid_parse is False

    # Running header/footer contamination
    header_leak_text = """
    Section 1. Short title.
    Printed on 15/08/2024 Page 1 of 42
    This Act extends to the whole of India.
    """
    doc_leak = parser.parse_statute(header_leak_text, "DOC-LEAK-001", "Leaked Act")
    assert any(d.defect_code == "WARN_HEADER_FOOTER_LEAK" for d in doc_leak.defects)


def test_corpus_versioning_and_repeal_tracking(tmp_path):
    engine = NationalCorpusVersioningEngine(tmp_path / "test_ledger.json")

    # Record repeal and replacement of IPC by BNS
    old_v, new_v = engine.record_repeal_replacement(
        old_source_id="IND-STAT-IPC-1860",
        new_source_id="IND-STAT-BNS-2023",
        commencement_date="2024-07-01",
        gazette_notification_ref="Gazette of India S.O. 850(E)",
    )

    assert old_v.change_type == VersionChangeType.REPEAL
    assert old_v.repealed_by_source_id == "IND-STAT-BNS-2023"
    assert new_v.change_type == VersionChangeType.COMMENCEMENT_NOTIFICATION
    assert new_v.superseded_source_id == "IND-STAT-IPC-1860"

    history = engine.get_version_history("IND-STAT-IPC-1860")
    assert len(history) == 1
    assert history[0].semantic_version == "repealed-2024"


def test_corpus_quality_and_zero_split_leakage():
    exporter = TrainingCorpusExporter()
    passages, scaffold_count, pending_count = exporter.collect_eligible_passages()

    test_sources = {
        "IND-STAT-LIMIT-1963",
        "IND-STAT-DPDP-2023",
        "IND-JUD-SC-2020-ARJUN-KHOTKAR",
        "IND-STAT-IT-2000-HI",
        "IND-JUD-BHC-2008-ROCHE-CIPLA",
    }
    val_sources = {
        "IND-STAT-NI-1881",
        "IND-STAT-SRA-1963",
        "IND-STAT-CPC-1908-HI",
        "IND-KA-STAT-KLRA-1961",
    }
    train_sources = {
        p["source_id"] for p in passages if p["source_id"] not in test_sources and p["source_id"] not in val_sources
    }

    quality_engine = CorpusQualityEngine()
    rep = quality_engine.audit_corpus(
        passages,
        train_sources=train_sources,
        val_sources=val_sources,
        test_sources=test_sources,
    )

    # Invariants
    assert rep.leakage_detected is False
    assert len(rep.leakage_details) == 0
    assert rep.exact_duplicate_rate == 0.0
    assert rep.total_tokens == 342965
    assert rep.eligible_en_tokens == 334348
    assert rep.eligible_hi_tokens == 8617


def test_training_export_dry_run_and_scaffold_exclusion():
    exporter = TrainingCorpusExporter()
    summary = exporter.export(dry_run=True, version="v4")

    assert summary.is_dry_run is True
    assert summary.manifest_version == "v4.0.0"
    assert summary.total_eligible_passages == 1559
    assert summary.scaffold_quarantined_count == 6
    assert summary.pending_review_excluded_count == 40
    assert summary.total_usable_tokens == 342965
    assert summary.dataset_manifest_sha256 != ""

