"""
LegalMitra Phase 46 — Central Legislation Batch 2 & PIT-V2 Test Suite
"""

import json
import sqlite3
import pytest
from pathlib import Path

from legalmitra.temporal.engine import (
    TemporalLawEngine,
    StatuteLifecycle,
    ProvisionTemporalVersion,
    TemporalStatus,
    build_default_temporal_engine,
)
from scripts.verify_freeze import verify_freeze
from scripts.reconcile_phase44_corpus import run_reconciliation

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "22_central_legislation"


class TestBatch2TemporalResolvers:
    """Tests for Batch 2 domain resolvers in TemporalLawEngine."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = build_default_temporal_engine()

    def test_companies_act_csr_transition(self):
        # Case A: FY 2018-19 (Pre-amendment query date: 2019-05-15)
        res_pre = self.engine.resolve_companies_act_csr_regime("2019-05-15")
        assert "Pre-2020" in res_pre["regime"]
        assert "Comply or explain" in res_pre["csr_character"]
        assert "Section 450" in res_pre["penalty_type"]
        assert res_pre["unspent_transfer_mandate"] is False

        # Case B: FY 2022-23 (Post-amendment query date: 2023-04-10)
        res_post = self.engine.resolve_companies_act_csr_regime("2023-04-10")
        assert "Post-2020" in res_post["regime"]
        assert "Mandatory spending" in res_post["csr_character"]
        assert "Civil monetary" in res_post["penalty_type"]
        assert res_post["unspent_transfer_mandate"] is True
        assert "S.O. 325(E)" in res_post["notification_ref"]

    def test_ibc_clean_slate_immunity(self):
        # Pre-Section 32A (2018-05-10)
        res_pre = self.engine.resolve_ibc_clean_slate_regime("2018-05-10")
        assert res_pre["clean_slate_statutory_immunity"] is False
        assert res_pre["asset_attachment_bar"] is False

        # Post-Section 32A (2021-06-15)
        res_post = self.engine.resolve_ibc_clean_slate_regime("2021-06-15")
        assert res_post["clean_slate_statutory_immunity"] is True
        assert res_post["asset_attachment_bar"] is True
        assert "Section 32A" in res_post["governing_rule"]

    def test_contract_act_section28_extinguishment(self):
        # Pre-1997 Amendment (1995-04-10): Extinguishment clause valid
        res_pre = self.engine.resolve_contract_section28_regime("1995-04-10")
        assert res_pre["extinguishment_clause_valid"] is True
        assert "Vulcan Insurance" in res_pre["doctrine"]
        assert res_pre["clause_b_active"] is False

        # Post-1997 Amendment (2002-08-15): Extinguishment clause void
        res_post = self.engine.resolve_contract_section28_regime("2002-08-15")
        assert res_post["extinguishment_clause_valid"] is False
        assert res_post["clause_b_active"] is True
        assert "void" in res_post["doctrine"]

    def test_tpa_part_performance_registration(self):
        # Pre-2001 Amendment (1998-03-12): Unregistered defense valid
        res_pre = self.engine.resolve_tpa_part_performance_regime("1998-03-12")
        assert res_pre["mandatory_registration"] is False
        assert res_pre["s53a_protection_unregistered"] is True

        # Post-2001 Amendment (2005-11-20): Mandatory registration required
        res_post = self.engine.resolve_tpa_part_performance_regime("2005-11-20")
        assert res_post["mandatory_registration"] is True
        assert res_post["s53a_protection_unregistered"] is False
        assert res_post["registration_act_s17_1a_required"] is True

    def test_cpc_commercial_timeline(self):
        # Ordinary Civil Suit at Day 105: Condonable, not forfeited
        res_ord = self.engine.resolve_cpc_commercial_timeline(is_commercial_dispute=False, days_elapsed=105)
        assert res_ord["delay_condonable"] is True
        assert res_ord["right_to_file_forfeited"] is False

        # Commercial Suit at Day 105: Within 120 days, condonable on costs
        res_comm_105 = self.engine.resolve_cpc_commercial_timeline(is_commercial_dispute=True, days_elapsed=105)
        assert res_comm_105["delay_condonable"] is True
        assert res_comm_105["right_to_file_forfeited"] is False

        # Commercial Suit at Day 125: Beyond 120 days, strictly forfeited
        res_comm_125 = self.engine.resolve_cpc_commercial_timeline(is_commercial_dispute=True, days_elapsed=125)
        assert res_comm_125["delay_condonable"] is False
        assert res_comm_125["right_to_file_forfeited"] is True

    def test_mva_compensation_transition(self):
        # Pre-2022 Accident (2021-08-10): Section 163A formula
        res_pre = self.engine.resolve_mva_compensation_regime("2021-08-10")
        assert "Section 163A" in res_pre["governing_section"]
        assert res_pre["fixed_no_fault_sum"] is None

        # Post-2022 Accident (2022-09-15): Section 164 fixed sum
        res_post = self.engine.resolve_mva_compensation_regime("2022-09-15")
        assert "Section 164" in res_post["governing_section"]
        assert res_post["fixed_sum_death"] == 500000
        assert res_post["fixed_sum_grievous_hurt"] == 250000


class TestBatch2ManifestsAndIntegrity:
    """Tests the integrity and scale of Phase 46 manifests."""

    def test_source_provenance_manifest_fourteen_sources(self):
        manifest_path = DATA_DIR / "source_provenance_manifest.json"
        assert manifest_path.exists()
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["provenance_standard"] == "LEGALMITRA-PROVENANCE-SPEC-V2"
        sources = manifest["sources"]
        assert len(sources) == 14
        expected_instruments = {
            "IND-STAT-BNS-2023", "IND-STAT-BNSS-2023", "IND-STAT-BSA-2023",
            "IND-STAT-IT-2000", "IND-STAT-DPDP-2023", "IND-STAT-SRA-1963",
            "IND-STAT-ARB-1996", "IND-STAT-CPA-2019", "IND-STAT-COMP-2013",
            "IND-STAT-IBC-2016", "IND-STAT-CONTRACT-1872", "IND-STAT-TPA-1882",
            "IND-STAT-CPC-1908", "IND-STAT-MVA-1988"
        }
        actual_instruments = {s["instrument_id"] for s in sources}
        assert expected_instruments.issubset(actual_instruments)

    def test_provision_provenance_manifest_twenty_nine_provisions(self):
        manifest_path = DATA_DIR / "provision_provenance_manifest.json"
        assert manifest_path.exists()
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        provisions = manifest["provisions"]
        assert len(provisions) == 29
        for p in provisions:
            assert len(p["validity_interval"]) == 2

    def test_amendment_event_ledger_twenty_events(self):
        ledger_path = DATA_DIR / "amendment_event_ledger.json"
        assert ledger_path.exists()
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        events = ledger["events"]
        assert len(events) == 20
        for evt in events:
            assert evt["event_id"].startswith(("AMEND-EVT-", "REPEAL-EVT-", "SAVINGS-EVT-"))

    def test_legal_dependency_graph_thirty_two_nodes_twenty_five_edges(self):
        graph_path = DATA_DIR / "legal_dependency_graph.json"
        assert graph_path.exists()
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = json.load(f)
        nodes = graph["nodes"]
        edges = graph["edges"]
        assert len(nodes) == 32
        assert len(edges) == 25
        node_ids = {n["id"] for n in nodes}
        for e in edges:
            assert e["source"] in node_ids, f"Broken source {e['source']}"
            assert e["target"] in node_ids, f"Broken target {e['target']}"

    def test_temporal_benchmark_manifest_twenty_cases(self):
        bench_path = DATA_DIR / "temporal_benchmark_manifest.json"
        assert bench_path.exists()
        with open(bench_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["total_test_cases"] == 20
        assert len(manifest["test_cases"]) == 20
        for i, tc in enumerate(manifest["test_cases"], 1):
            expected_id = f"PIT-0{i}" if i < 10 else f"PIT-{i}"
            assert tc["case_id"] == expected_id


class TestPhase46Invariants:
    """Tests non-negotiable architectural invariants for Phase 46."""

    def test_phase9_freeze_integrity(self):
        hash_data = verify_freeze()
        assert len(hash_data) == 6

    def test_precedent_review_packages_remain_pending(self):
        reg_path = BASE_DIR / "data" / "07_batches" / "review" / "review_tracking_register.json"
        assert reg_path.exists()
        with open(reg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["total_tracked_records"] == 40
        for entry in data["entries"]:
            assert entry["review_status"] == "pending_legal_review"

    def test_scaffold_records_remain_quarantined(self):
        rec = run_reconciliation()
        assert rec["scaffold_chunk_isolation_verified"] is True
        assert rec["database_separation_verified"] is True

    def test_database_isolation(self):
        kb_path = BASE_DIR / "data" / "legalmitra_kb.db"
        conv_path = BASE_DIR / "data" / "conversations.db"
        if kb_path.exists() and conv_path.exists():
            with sqlite3.connect(kb_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                kb_tables = {row[0] for row in cursor.fetchall()}
                assert "conversations" not in kb_tables
                assert "messages" not in kb_tables
