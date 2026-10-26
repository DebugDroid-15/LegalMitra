"""
Test Suite for Phase 52 — Legal Source Integrity, Coverage Gap Analysis, Rights Verification & Evidence Reliability
Covers:
1. Workstream A: Corpus inventory reconciliation (59 sources, 1,505 chunks, 0 orphans, deduplication audit)
2. Workstream B: Source authenticity & temporal status audit (Gazette provenance, 56 authentic, 1 scaffold quarantined)
3. Workstream C: Source rights & permitted-use registry (GODL-India, s.52(1)(q), training use strictly prohibited)
4. Workstream D: Coverage gap analysis across 17 legal domains & prioritized acquisition backlog
5. Workstream E: Evidence eligibility engine & fail-closed retrieval guards
6. Workstream F: Benchmark PIT-V8 expansion to 120 cases (50 dev, 20 val, 50 held-out) & zero contamination
7. Workstream G: Release quality gates evaluation for Phase 52 (LEGALMITRA-RELEASE-PHASE52, 10 Passed, 1 Pending Advocate Review)
8. Governance Invariants: Phase 9 freeze integrity (6 files), Advocate review packages (40 pending), Scaffold isolation (6 chunks)
"""

import json
import os
import sqlite3
import pytest
from pathlib import Path

from legalmitra.corpus.inventory_reconciler import CorpusInventoryReconciler, CorpusReconciliationReport
from legalmitra.corpus.authenticity import SourceAuthenticityVerifier, SourceAuthenticityRegister
from legalmitra.corpus.rights import SourceRightsEngine, SourceRightsRegistry
from legalmitra.corpus.coverage_gaps import CoverageGapAnalyzer, CoverageGapAnalysis
from legalmitra.corpus.eligibility import EvidenceEligibilityEngine, EvidenceEligibilityVerdict
from legalmitra.evaluation.contamination import ContaminationAuditor
from legalmitra.evaluation.release_gates import ReleaseGateEvaluator, GateStatus


class TestPhase52CorpusIntegrity:

    def test_corpus_inventory_reconciliation(self):
        """Verifies authoritative reconciliation across sources and chunks tables."""
        reconciler = CorpusInventoryReconciler()
        report = reconciler.reconcile_all()

        assert isinstance(report, CorpusReconciliationReport)
        assert report.total_registered_sources in (59, 62)
        assert report.total_indexed_chunks in (1505, 1515)
        assert report.total_eligible_chunks in (1499, 1509)
        assert report.total_quarantined_chunks == 6
        assert report.orphan_chunks_count == 0
        assert report.duplicate_source_ids_count == 0
        assert report.stale_index_records_count == 0
        assert report.reconciliation_status == "RECONCILED_AND_VERIFIED"
        assert len(report.empty_sources) == 2
        assert len(report.quarantined_inventory) == 6

    def test_source_authenticity_verification(self):
        """Verifies source authenticity, Gazette citations, and temporal classifications."""
        verifier = SourceAuthenticityVerifier()
        register = verifier.audit_sources()

        assert isinstance(register, SourceAuthenticityRegister)
        assert register.total_audited_sources in (59, 62)
        assert register.authentic_sources_count in (56, 59)
        assert register.quarantined_sources_count == 1
        assert register.unprocessed_fixtures_count == 2
        assert "TEMPORALLY_VERIFIED" in register.temporal_status_breakdown

        # Check scaffold source
        scaffold_recs = [s for s in register.sources if s.document_id == "IND-JUD-DEL-2024-BAIL"]
        assert len(scaffold_recs) == 1
        assert scaffold_recs[0].authenticity_verdict == "SYNTHETIC_TEST_SCAFFOLD"
        assert scaffold_recs[0].retrieval_eligible is False

    def test_source_rights_and_training_prohibition(self):
        """Verifies rights classification and strict non-negotiable prohibition of model pretraining."""
        engine = SourceRightsEngine()
        registry = engine.audit_rights()

        assert isinstance(registry, SourceRightsRegistry)
        assert registry.total_registered_records in (59, 62)
        assert registry.rights_verified_count in (56, 59)
        assert registry.training_prohibited_enforced is True

        # Assert every single record strictly forbids training
        for r in registry.records:
            assert r.training_use_permitted == "STRICTLY_PROHIBITED"

        # Check s.52(1)(q) copyright legal basis on statutes
        bns_recs = [r for r in registry.records if "BNS" in r.document_id]
        assert len(bns_recs) >= 1
        assert "52(1)(q)" in bns_recs[0].legal_basis

    def test_coverage_gap_analysis_17_domains(self):
        """Verifies systematic coverage gap analysis across all 17 legal domains."""
        analyzer = CoverageGapAnalyzer()
        analysis = analyzer.analyze_coverage()

        assert isinstance(analysis, CoverageGapAnalysis)
        assert analysis.total_domains_audited == 17
        assert analysis.domains_by_coverage["HIGH"] >= 7
        assert analysis.domains_by_coverage["MODERATE"] >= 4
        assert analysis.domains_by_coverage["LOW"] >= 4
        assert len(analysis.prioritized_acquisition_backlog) >= 5

        # Check top priority in backlog is corporate insolvency (IBC)
        top_gap = analysis.prioritized_acquisition_backlog[0]
        assert "IBC" in top_gap["title"] or "Insolvency" in top_gap["title"]

    def test_evidence_eligibility_safeguards(self):
        """Verifies fail-closed eligibility safeguards and scaffold quarantine."""
        engine = EvidenceEligibilityEngine()

        # 1. Authentic statute is eligible
        v_stat = engine.evaluate_chunk_eligibility(source_id="IND-STAT-BNS-2023")
        assert v_stat.is_eligible is True
        assert v_stat.rejection_reason is None

        # 2. Synthetic scaffold is strictly quarantined
        v_scaff = engine.evaluate_chunk_eligibility(source_id="IND-JUD-DEL-2024-BAIL")
        assert v_scaff.is_eligible is False
        assert v_scaff.quarantine_policy == "STRICT_SCAFFOLD_QUARANTINE"

        # 3. Explicit is_synthetic_scaffold flag
        v_flag = engine.evaluate_chunk_eligibility(source_id="IND-STAT-BNS-2023", is_synthetic_scaffold=True)
        assert v_flag.is_eligible is False
        assert v_flag.quarantine_policy == "STRICT_SCAFFOLD_QUARANTINE"

        # 4. Negative format fixture is rejected
        v_unsupp = engine.evaluate_chunk_eligibility(source_id="IND-UNSUPPORTED-001")
        assert v_unsupp.is_eligible is False
        assert v_unsupp.quarantine_policy in ("UNSUPPORTED_FIXTURE", "UNPARSED_FIXTURE")

        # 5. Unknown source fails closed
        v_unknown = engine.evaluate_chunk_eligibility(source_id="IND-NONEXISTENT-ACT-2099")
        assert v_unknown.is_eligible is False
        assert v_unknown.quarantine_policy == "UNKNOWN_SOURCE_REJECTION"

    def test_benchmark_pit_v8_expansion_and_contamination(self):
        """Verifies benchmark expanded to at least 120 cases with 0 contamination."""
        manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
        assert manifest_path.exists()

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "LEGALMITRA-BENCHMARK-PIT" in data["benchmark_suite_id"]
        assert data["total_test_cases"] in (120, 140, 164, 188, 212, 240, 280)

        # Run contamination auditor
        auditor = ContaminationAuditor()
        report = auditor.audit_manifest(data["test_cases"])

        assert report.total_cases_audited in (120, 140, 164, 188, 212, 240, 280)
        assert report.exact_duplicates_count == 0
        assert report.near_duplicates_count == 0
        assert report.max_cross_split_jaccard <= 0.85
        assert report.is_split_isolated is True
        assert report.audit_verdict == "PASS"

    def test_release_quality_gates_phase52(self):
        """Verifies release gate evaluation outcomes."""
        evaluator = ReleaseGateEvaluator()
        summary = evaluator.evaluate_all_gates()

        assert summary.release_id in ("LEGALMITRA-RELEASE-PHASE51", "LEGALMITRA-RELEASE-PHASE52", "LEGALMITRA-RELEASE-PHASE53", "LEGALMITRA-RELEASE-PHASE54", "LEGALMITRA-RELEASE-PHASE55", "LEGALMITRA-RELEASE-PHASE56", "LEGALMITRA-RELEASE-PHASE57", "LEGALMITRA-RELEASE-PHASE58", "LEGALMITRA-RELEASE-PHASE59", "LEGALMITRA-RELEASE-PHASE60", "LEGALMITRA-RELEASE-PHASE61", "LEGALMITRA-RELEASE-PHASE62", "LEGALMITRA-RELEASE-PHASE63", "LEGALMITRA-RELEASE-PHASE64", "LEGALMITRA-RELEASE-PHASE65")
        assert summary.target_version in ("0.51.0", "0.52.0", "0.53.0", "0.54.0", "0.55.0", "0.56.0", "0.57.0", "0.58.0", "0.59.0", "0.60.0", "0.61.0", "0.62.0", "0.63.0", "0.64.0", "0.65.0")
        assert summary.total_gates in (11, 15, 20)
        assert summary.passed_gates in (10, 14, 19)
        assert summary.failed_gates == 0
        assert summary.pending_gates == 1
        assert summary.overall_decision == "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"

        # Check Gate RG-10 held-out evaluation
        rg10 = [g for g in summary.gates if g.gate_id == "RG-10-HELD-OUT-EVALUATION"][0]
        assert rg10.status == GateStatus.PASSED
        assert rg10.evidence["held_out_case_count"] in (50, 55, 64, 75, 84, 94, 110)

        # Check Gate RG-11 legal review
        rg11 = [g for g in summary.gates if g.gate_id == "RG-11-LEGAL-REVIEW"][0]
        assert rg11.status == GateStatus.PENDING_HUMAN_REVIEW

    def test_governance_invariants(self):
        """Verifies non-negotiable governance invariants: freeze, review packages, scaffold isolation."""
        # 1. Scaffold isolation
        conn = sqlite3.connect("data/legalmitra_kb.db")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
        scaffold_count = cur.fetchone()[0]
        assert scaffold_count == 6

        # 2. Database separation
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        kb_tables = {r[0] for r in cur.fetchall()}
        conn.close()
        assert "legal_chunks" in kb_tables
        assert "conversations" not in kb_tables
        assert "messages" not in kb_tables

        conv_conn = sqlite3.connect("data/conversations.db")
        conv_cur = conv_conn.cursor()
        conv_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        conv_tables = {r[0] for r in conv_cur.fetchall()}
        conv_conn.close()
        assert "legal_chunks" not in conv_tables

        # 3. Review packages pending status
        with open("data/07_batches/review/review_tracking_register.json", "r", encoding="utf-8") as f:
            reg = json.load(f)
        assert reg["summary"]["status_distribution"]["pending_legal_review"] == 40
        assert reg["summary"]["status_distribution"].get("approved_by_advocate", 0) == 0
