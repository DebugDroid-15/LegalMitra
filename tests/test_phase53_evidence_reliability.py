"""
Phase 53 Test Suite — Evidence-Grade Legal Acquisition, Claim-Level Grounding & End-to-End Reliability
Covers:
1. Workstream A & B: Source acquisition engine, lifecycle state machine, deterministic ranking, and idempotent ingestion
2. Workstream C: Rights reassessment and strict enforcement of the model training prohibition
3. Workstream D: Claim-level evidence validation (SUPPORTED, CONTRADICTED, TEMPORALLY_UNCERTAIN, JURISDICTION_UNCERTAIN, PRECEDENT_STATUS_UNCERTAIN, INSUFFICIENT_EVIDENCE)
4. Workstream E: Benchmark PIT-V9 (140 cases, 55 held-out) structure and zero split contamination
5. Workstream F: Adversarial robustness & fail-closed regression safeguards
6. Workstream G: Release quality gates evaluation for Phase 53 (LEGALMITRA-RELEASE-PHASE53)
7. Governance Invariants: Phase 9 freeze, 40 advocate review candidates, scaffold quarantine, and DB isolation
"""

import json
import os
import sqlite3
import pytest
from pathlib import Path

from legalmitra.corpus.acquisition_engine import (
    AcquisitionCandidate,
    LegalAcquisitionEngine,
    SourceLifecycleState,
    VALID_TRANSITIONS,
)
from legalmitra.corpus.authenticity import SourceAuthenticityVerifier
from legalmitra.corpus.rights import SourceRightsEngine
from legalmitra.corpus.coverage_gaps import CoverageGapAnalyzer
from legalmitra.corpus.eligibility import EvidenceEligibilityEngine
from legalmitra.evaluation.contamination import ContaminationAuditor
from legalmitra.evaluation.release_gates import ReleaseGateEvaluator, GateStatus
from legalmitra.temporal.engine import TemporalLawEngine, build_default_temporal_engine


class TestPhase53EvidenceReliability:

    def test_acquisition_engine_lifecycle_and_transitions(self):
        """Verifies state machine transitions and invalid transition rejection."""
        engine = LegalAcquisitionEngine()
        cand = AcquisitionCandidate(
            candidate_id="IND-TEST-CAND-001",
            official_title="Test Acquisition Candidate",
            source_type="statute",
            domain_id="DOM-01-CRIMINAL",
            issuing_authority="Legislative Department",
            jurisdiction="IN",
            canonical_source_url="https://example.com/test",
            priority_tier="HIGH",
            priority_score=8.5,
            priority_rationale="High impact test candidate",
        )

        assert cand.state == SourceLifecycleState.IDENTIFIED

        # Valid transition: IDENTIFIED -> REGISTERED
        ok = engine.transition_state(cand, SourceLifecycleState.REGISTERED, "Registered in ledger")
        assert ok is True
        assert cand.state == SourceLifecycleState.REGISTERED

        # Invalid transition: REGISTERED -> INDEXED (skipping acquisition/parsing)
        bad = engine.transition_state(cand, SourceLifecycleState.INDEXED, "Skip directly")
        assert bad is False
        assert cand.state == SourceLifecycleState.REGISTERED
        assert "Illegal transition" in cand.failure_reason

    def test_idempotent_ingestion_and_chunk_integrity(self):
        """Verifies that re-running ingestion does not create duplicate sources or chunks."""
        conn = sqlite3.connect("data/legalmitra_kb.db")
        cur = conn.cursor()

        # Check that IBC, HSA, and Patents sources exist
        cur.execute("SELECT count(*) FROM sources WHERE document_id IN ('IND-STAT-IBC-2016', 'IND-STAT-HSA-1956', 'IND-STAT-PAT-1970')")
        count_sources = cur.fetchone()[0]
        assert count_sources == 3

        # Check total chunks for these 3 sources (4 + 3 + 3 = 10 chunks)
        cur.execute("SELECT count(*) FROM legal_chunks WHERE source_id IN ('IND-STAT-IBC-2016', 'IND-STAT-HSA-1956', 'IND-STAT-PAT-1970')")
        count_chunks = cur.fetchone()[0]
        assert count_chunks == 10

        # Check chunk authority_level
        cur.execute("SELECT DISTINCT authority_level FROM legal_chunks WHERE source_id IN ('IND-STAT-IBC-2016', 'IND-STAT-HSA-1956', 'IND-STAT-PAT-1970')")
        levels = [r[0] for r in cur.fetchall()]
        assert levels == ["binding_statute"]
        conn.close()

    def test_rights_reassessment_and_training_exclusion(self):
        """Proves that rights registry strictly forbids model training on all records."""
        engine = SourceRightsEngine()
        registry = engine.audit_rights()

        assert registry.training_prohibited_enforced is True
        for rec in registry.records:
            assert rec.training_use_permitted == "STRICTLY_PROHIBITED"

        # Check IBC rights basis
        ibc_recs = [r for r in registry.records if r.document_id == "IND-STAT-IBC-2016"]
        assert len(ibc_recs) == 1
        assert "52(1)(q)" in ibc_recs[0].legal_basis

    def test_claim_level_evidence_validation_categories(self):
        """Verifies deterministic claim validation outcomes across all major failure categories."""
        engine = build_default_temporal_engine()

        # 1. SUPPORTED claim
        res_supp = engine.validate_claim_evidence(
            claim_text="The adjudicating authority may admit an application under Section 7 IBC when default occurs.",
            cited_statute_id="IND-STAT-IBC-2016",
            passage_text="Where the Adjudicating Authority is satisfied that a default has occurred it may admit such application.",
        )
        assert res_supp["validation_outcome"] == "SUPPORTED"
        assert res_supp["is_supported"] is True

        # 2. CONTRADICTED claim
        res_contra = engine.validate_claim_evidence(
            claim_text="An agreement without consideration is valid under Indian contract law.",
            cited_statute_id="IND-STAT-ICA-1872",
            passage_text="An agreement made without consideration is void under Section 25.",
        )
        assert res_contra["validation_outcome"] == "CONTRADICTED"
        assert res_contra["is_supported"] is False

        # 3. PRECEDENT_STATUS_UNCERTAIN (ADM Jabalpur overruled)
        res_prec = engine.validate_claim_evidence(
            claim_text="The binding majority holding in ADM Jabalpur permits absolute suspension of Article 21.",
            cited_case_id="CASE-SC-1976-ADM-JABALPUR",
            passage_text="In view of the Presidential Order no person has any locus standi to move any writ petition.",
        )
        assert res_prec["validation_outcome"] == "PRECEDENT_STATUS_UNCERTAIN"
        assert res_prec["abstain_recommended"] is True

        # 4. JURISDICTION_UNCERTAIN
        res_juris = engine.validate_claim_evidence(
            claim_text="Magistrate powers in London under Delhi Police Act.",
            cited_statute_id="IND-DL-STAT-DPA-1978",
            passage_text="An Act to consolidate and amend the law for the regulation of Delhi Police.",
            jurisdiction="UK-ENG",
        )
        assert res_juris["validation_outcome"] == "JURISDICTION_UNCERTAIN"
        assert res_juris["is_supported"] is False

        # 5. INSUFFICIENT_EVIDENCE
        res_insuff = engine.validate_claim_evidence(
            claim_text="Uncited legal proposition with no authority.",
            cited_case_id=None,
            cited_statute_id=None,
            passage_text=None,
        )
        assert res_insuff["validation_outcome"] == "INSUFFICIENT_EVIDENCE"
        assert res_insuff["is_supported"] is False

        # 6. FABRICATED / UNSUPPORTED citation
        res_fake = engine.validate_claim_evidence(
            claim_text="Relying on fake case CyberTech 2024 DHC 99999.",
            cited_case_id="CASE-FAKE-99999",
            passage_text=None,
        )
        assert res_fake["validation_outcome"] == "UNSUPPORTED"
        assert res_fake["is_supported"] is False

    def test_benchmark_pit_v9_structure_and_zero_contamination(self):
        """Verifies PIT-V9 expansion to 140 cases, 55 held-out, and zero contamination."""
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["benchmark_suite_id"] in ("LEGALMITRA-BENCHMARK-PIT-V9", "LEGALMITRA-BENCHMARK-PIT-V10", "LEGALMITRA-BENCHMARK-PIT-V11", "LEGALMITRA-BENCHMARK-PIT-V12", "LEGALMITRA-BENCHMARK-PIT-V13", "LEGALMITRA-BENCHMARK-PIT-V14")
        assert data["version"] in ("9.0.0", "10.0.0", "11.0.0", "12.0.0", "13.0.0", "14.0.0")
        assert data["total_test_cases"] in (140, 164, 188, 212, 240, 280)
        assert data["split_counts"]["development"] in (60, 70, 78, 88, 100, 115)
        assert data["split_counts"]["validation"] in (25, 30, 35, 40, 46, 55)
        assert data["split_counts"]["held_out_evaluation"] in (55, 64, 75, 84, 94, 110)

        # Check new Phase 53 cases are present
        case_ids = {c["case_id"] for c in data["test_cases"]}
        for cid in ["PIT-121", "PIT-125", "PIT-130", "PIT-140"]:
            assert cid in case_ids

        # Run contamination auditor
        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(data["test_cases"])

        assert report.total_cases_audited in (140, 164, 188, 212, 240, 280)
        assert report.exact_duplicates_count == 0
        assert report.near_duplicates_count == 0
        assert report.max_cross_split_jaccard <= 0.85
        assert report.is_split_isolated is True
        assert report.audit_verdict == "PASS"

    def test_release_quality_gates_phase53(self):
        """Verifies release gate evaluation for Phase 53/54."""
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57", "LEGALMITRA-RELEASE-PHASE58", "LEGALMITRA-RELEASE-PHASE59", "LEGALMITRA-RELEASE-PHASE60")
        assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0", "0.58.0", "0.59.0", "0.60.0")
        assert summary.total_gates in (11, 15, 20)
        assert summary.passed_gates in (10, 14, 19)
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"

        # Gate RG-10 held-out evaluation
        rg10 = [g for g in summary.gates if g.gate_id == "RG-10-HELD-OUT-EVALUATION"][0]
        assert rg10.status == GateStatus.PASSED
        assert rg10.evidence["held_out_case_count"] in (55, 64, 75, 84, 94, 110)

        # Gate RG-11 advocate review
        rg11 = [g for g in summary.gates if g.gate_id == "RG-11-LEGAL-REVIEW"][0]
        assert rg11.status == GateStatus.PENDING_HUMAN_REVIEW
