"""Tests for Phase 40 Operational High Court Acquisition, Devanagari OCR QA & Precedent Conflict Triage."""

import json
import os
import pytest

from legalmitra.judicial.connectors.connector_base import (
    BaseJudicialConnector,
    BoundedResponseError,
    RateLimiter,
    SourceDocumentState,
    SSRFProtectionError,
)
from legalmitra.judicial.connectors.delhi_high_court_connector import (
    DelhiHighCourtConnector,
)
from legalmitra.judicial.connectors.bombay_high_court_connector import (
    BombayHighCourtConnector,
)
from legalmitra.judicial.ecourts_protocol import (
    CNRDecomposition,
    ECourtsIngestionRecord,
    ECourtsProtocolValidator,
    ECourtsWorkflowStage,
)
from legalmitra.judicial.devanagari_ocr import (
    DevanagariOCREngine,
    DevanagariOCRResult,
)
from legalmitra.judicial.conflict_triage import (
    ConflictCategory,
    PrecedentConflictRecord,
    PrecedentConflictTriageManager,
    TriageStatus,
)


# --- 1. High Court Connectors & Safeguards Tests ---

def test_delhi_high_court_connector_init():
    conn = DelhiHighCourtConnector(dry_run=True)
    assert conn.court_id == "IND-HC-DEL"
    assert "delhihighcourt.nic.in" in conn.allowed_domains
    assert conn.dry_run is True


def test_delhi_high_court_connector_ssrf_blocking():
    conn = DelhiHighCourtConnector(dry_run=False)
    
    # Loopback IP
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("http://127.0.0.1/admin")
        
    # Cloud metadata endpoint
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("http://169.254.169.254/latest/meta-data/")
        
    # Private network RFC1918
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("http://192.168.1.10/judgment.pdf")

    # Unapproved external domain
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("https://malicious-court-mirror.org/doc.pdf")


def test_delhi_high_court_connector_allowed_url():
    conn = DelhiHighCourtConnector(dry_run=True)
    # Valid allowed domain passes without error
    conn.validate_url_security("https://delhihighcourt.nic.in/dhcqrydisp_o.asp?pn=123")


def test_delhi_high_court_discovery_dry_run():
    conn = DelhiHighCourtConnector(dry_run=True)
    discovered = conn.discover_documents({"year": 2024, "limit": 5})
    assert len(discovered) > 0
    for doc in discovered:
        assert doc.court_id == "IND-HC-DEL"
        assert "DHC" in doc.neutral_citation
        assert doc.current_state == SourceDocumentState.DISCOVERED


def test_bombay_high_court_connector_multi_bench():
    conn = BombayHighCourtConnector(dry_run=True)
    assert conn.court_id == "IND-HC-BOM"
    assert "bombayhighcourt.nic.in" in conn.allowed_domains
    
    discovered = conn.discover_documents({"year": 2023, "bench_code": "NAG", "limit": 3})
    assert len(discovered) > 0
    for doc in discovered:
        assert "BHC" in doc.neutral_citation


def test_rate_limiter():
    limiter = RateLimiter(requests_per_minute=30)
    # First token consumption should succeed immediately with 0 delay
    assert limiter.wait_if_needed() == 0.0


# --- 2. eCourts CIS Ingestion Protocol Tests ---

def test_ecourts_cnr_validation_success():
    validator = ECourtsProtocolValidator()
    
    # 16-char CNR: DLTH010012342023
    decomp = validator.validate_cnr("DLTH010012342023")
    assert decomp.is_valid is True
    assert decomp.state_code == "DL"
    assert decomp.district_code == "TH"
    assert decomp.establishment_code == "01"
    assert decomp.case_number == 1234
    assert decomp.filing_year == 2023


def test_ecourts_cnr_validation_failure():
    validator = ECourtsProtocolValidator()
    
    # Wrong length
    res1 = validator.validate_cnr("DLTH01001234202")
    assert res1.is_valid is False
    assert "exactly 16" in res1.error_message

    # Invalid filing year (out of 1950-2030 range)
    res2 = validator.validate_cnr("DLTH010012341920")
    assert res2.is_valid is False
    assert "out of reasonable range" in res2.error_message


def test_ecourts_staged_ingestion_workflow():
    validator = ECourtsProtocolValidator()
    raw = {
        "cnr_number": "MHCC020056782022",
        "state_name": "Maharashtra",
        "district_name": "Mumbai City Civil Court",
        "court_establishment": "Court Room 14",
        "case_type": "Summary Suit",
        "filing_number": "5678/2022",
        "registration_date": "2022-07-10",
        "petitioner": "Standard Mercantile Bank Ltd",
        "respondent": "Omkar Enterprises",
        "governing_acts": ["Order XXXVII CPC 1908"],
        "order_date": "2023-05-18",
        "disposal_nature": "DISPOSED_OF",
        "raw_text": "Commercial summary suit under Order 37 CPC. Regular commercial dispute without restricted subject matter.",
    }
    rec = validator.process_record(raw)
    assert rec.stage == ECourtsWorkflowStage.ELIGIBLE_INDEXED
    assert rec.is_retrieval_eligible is True
    assert rec.is_training_eligible is False  # Strict pretraining gate
    assert len(rec.audit_log) >= 5


def test_ecourts_privacy_restriction_gating():
    validator = ECourtsProtocolValidator()
    raw = {
        "cnr_number": "DLST010005552024",
        "state_name": "Delhi",
        "district_name": "South (Saket)",
        "court_establishment": "Special POCSO Court 01",
        "case_type": "Special Sessions Case",
        "filing_number": "555/2024",
        "registration_date": "2024-02-14",
        "petitioner": "State",
        "respondent": "Accused X",
        "governing_acts": ["POCSO Act 2012"],
        "order_date": "2024-08-30",
        "disposal_nature": "PENDING_TRIAL",
        "raw_text": "Special POCSO Court proceedings involving a minor victim under Section 6 of POCSO Act 2012.",
    }
    rec = validator.process_record(raw)
    assert rec.stage == ECourtsWorkflowStage.BLOCKED_RESTRICTED
    assert rec.is_retrieval_eligible is False
    assert rec.is_training_eligible is False


# --- 3. Devanagari OCR Normalization & QA Engine Tests ---

def test_devanagari_ocr_normalization_nfc():
    engine = DevanagariOCREngine()
    text = "उच्चतम न्यायालय  ने जमानत प्रदान की ।"
    res = engine.normalize(text)
    assert res.normalized_text == "उच्चतम न्यायालय ने जमानत प्रदान की।"
    assert "जमानत" in res.legal_tokens_detected
    assert "उच्चतम न्यायालय" in res.legal_tokens_detected


def test_devanagari_ocr_anomaly_detection():
    engine = DevanagariOCREngine()
    corrupt_text = "अभियुक्त धारा 439 \ufffd दण्ड प्रक्रिया संहिता"
    res = engine.normalize(corrupt_text)
    assert res.has_replacement_characters is True
    assert res.requires_human_review is True
    assert len(res.detected_anomalies) > 0


def test_devanagari_ocr_cer_wer_computation():
    engine = DevanagariOCREngine()
    ref = "जमानत एक नियम है"
    hyp_identical = "जमानत एक नियम है"
    hyp_mismatch = "जमानत एक अपवाद है"
    
    assert engine.compute_cer(ref, hyp_identical) == 0.0
    assert engine.compute_wer(ref, hyp_identical) == 0.0
    
    cer = engine.compute_cer(ref, hyp_mismatch)
    wer = engine.compute_wer(ref, hyp_mismatch)
    assert cer > 0.0
    assert wer > 0.0


# --- 4. Precedent Conflict Triage Engine Tests ---

def test_precedent_conflict_registration_requires_anchors():
    manager = PrecedentConflictTriageManager()
    
    # Missing passage anchor should raise ValueError
    invalid_record = PrecedentConflictRecord(
        conflict_id="CONF-INVALID",
        case_a_id="CASE-A",
        case_a_title="Case A",
        case_a_court_id="IND-HC-DEL",
        case_a_bench_count=1,
        case_a_passage_anchor="",  # Empty anchor
        case_a_proposition="Prop A",
        case_b_id="CASE-B",
        case_b_title="Case B",
        case_b_court_id="IND-HC-BOM",
        case_b_bench_count=1,
        case_b_passage_anchor="[2020] BHC 12, Para 4",
        case_b_proposition="Prop B",
        governing_statute_section="Sec 138 NI Act",
        category=ConflictCategory.CO_EQUAL_HIGH_COURT_CONFLICT,
    )
    with pytest.raises(ValueError, match="exact paragraph anchors"):
        manager.register_conflict(invalid_record)


def test_precedent_conflict_triage_authorization_gate():
    manager = PrecedentConflictTriageManager()
    
    valid_record = PrecedentConflictRecord(
        conflict_id="CONF-TEST-001",
        case_a_id="CASE-A",
        case_a_title="Case A",
        case_a_court_id="IND-HC-DEL",
        case_a_bench_count=2,
        case_a_passage_anchor="[2021] DHC 100, Para 12",
        case_a_proposition="Prop A",
        case_b_id="CASE-B",
        case_b_title="Case B",
        case_b_court_id="IND-HC-BOM",
        case_b_bench_count=2,
        case_b_passage_anchor="[2022] BHC 200, Para 15",
        case_b_proposition="Prop B",
        governing_statute_section="Sec 9 Arbitration Act",
        category=ConflictCategory.CO_EQUAL_HIGH_COURT_CONFLICT,
        priority_score=4.0,
    )
    manager.register_conflict(valid_record)
    
    # Unauthorized resolution attempt must raise PermissionError
    with pytest.raises(PermissionError, match="Unauthorized reviewer"):
        manager.resolve_conflict(
            conflict_id="CONF-TEST-001",
            reviewer_id="UNAUTHORIZED_USER_OR_BOT",
            resolution_status=TriageStatus.RESOLVED_FACTUALLY_DISTINGUISHED,
            rationale="Factual difference between contract clauses.",
        )
        
    # Authorized resolution succeeds
    manager.resolve_conflict(
        conflict_id="CONF-TEST-001",
        reviewer_id="ADV-SHATRUJEET-01",
        resolution_status=TriageStatus.RESOLVED_FACTUALLY_DISTINGUISHED,
        rationale="Factual difference between contract clauses.",
    )
    
    res = manager.get_conflict("CONF-TEST-001")
    assert res.status == TriageStatus.RESOLVED_FACTUALLY_DISTINGUISHED
    assert res.reviewer_authorized is True
    assert res.assigned_reviewer == "ADV-SHATRUJEET-01"


def test_precedent_conflict_priority_queue():
    manager = PrecedentConflictTriageManager()
    
    r1 = PrecedentConflictRecord(
        conflict_id="CONF-LOW",
        case_a_id="A1", case_a_title="T1", case_a_court_id="IND-HC-DEL", case_a_bench_count=1,
        case_a_passage_anchor="Para 1", case_a_proposition="P1",
        case_b_id="B1", case_b_title="T2", case_b_court_id="IND-HC-BOM", case_b_bench_count=1,
        case_b_passage_anchor="Para 2", case_b_proposition="P2",
        governing_statute_section="Sec 1", category=ConflictCategory.FACTUALLY_DISTINGUISHABLE,
        priority_score=2.0,
    )
    r2 = PrecedentConflictRecord(
        conflict_id="CONF-HIGH",
        case_a_id="A2", case_a_title="T3", case_a_court_id="IND-HC-DEL", case_a_bench_count=2,
        case_a_passage_anchor="Para 3", case_a_proposition="P3",
        case_b_id="B2", case_b_title="T4", case_b_court_id="IND-HC-BOM", case_b_bench_count=2,
        case_b_passage_anchor="Para 4", case_b_proposition="P4",
        governing_statute_section="Sec 2", category=ConflictCategory.CO_EQUAL_HIGH_COURT_CONFLICT,
        priority_score=4.9,
    )
    manager.register_conflict(r1)
    manager.register_conflict(r2)
    
    queue = manager.get_prioritized_queue()
    assert queue[0].conflict_id == "CONF-HIGH"
    assert queue[1].conflict_id == "CONF-LOW"


# --- 5. Phase 40 Artifacts Integrity Tests ---

def test_phase40_artifacts_exist_and_valid():
    artifact_paths = [
        "data/21_judicial_infrastructure/precedent_conflict_register.json",
        "data/21_judicial_infrastructure/devanagari_ocr_eval_manifest.json",
        "data/21_judicial_infrastructure/ecourts_sample_manifest.json",
        "data/21_judicial_infrastructure/judicial_coverage_matrix_v3.json",
        "data/21_judicial_infrastructure/independent_judicial_benchmark_v3.json",
    ]
    for p in artifact_paths:
        assert os.path.exists(p), f"Artifact missing: {p}"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data, f"Artifact is empty: {p}"


def test_independent_benchmark_v3_coverage():
    path = "data/21_judicial_infrastructure/independent_judicial_benchmark_v3.json"
    with open(path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)
    
    # Must have at least 45 test cases
    assert benchmark["total_test_cases"] >= 45
    assert len(benchmark["cases"]) >= 45
    
    # Check that new Phase 40 categories exist
    case_ids = {c["id"] for c in benchmark["cases"]}
    assert "CASE-36" in case_ids
    assert "CASE-40" in case_ids
    assert "CASE-44" in case_ids
    assert "CASE-48" in case_ids
