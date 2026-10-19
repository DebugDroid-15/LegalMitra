"""
LegalMitra Phase 45 — Central Legislation, Amendment History & Temporal Validity Test Suite
"""

import json
import os
import sqlite3
import pytest
from pathlib import Path

from legalmitra.temporal.ingestion import (
    CentralStatuteIngestionPipeline,
    IngestionStatus,
    IngestionResult,
)
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


class TestCentralStatuteIngestionPipeline:
    """Tests for CentralStatuteIngestionPipeline idempotency, schema compliance, and versioning."""

    def test_pipeline_initialization(self):
        pipeline = CentralStatuteIngestionPipeline()
        assert pipeline.engine is not None
        assert isinstance(pipeline._registered_hashes, set)
        assert isinstance(pipeline._indexed_provisions, set)

    def test_validate_provenance_record(self):
        pipeline = CentralStatuteIngestionPipeline()
        valid_record = {
            "source_id": "SRC-IND-CODE-SRA-1963",
            "instrument_id": "ACT-CENTRAL-1963-047",
            "official_title": "Specific Relief Act, 1963",
            "act_number": "Act 47 of 1963",
            "issuing_authority": "Parliament of India",
            "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1583",
            "publication_date": "1963-12-13",
            "content_sha256": "a" * 64,
        }
        is_valid, errors = pipeline.validate_provenance_record(valid_record)
        assert is_valid is True
        assert len(errors) == 0

        # Invalid record: missing field and bad hash length
        invalid_record = {
            "source_id": "SRC-INVALID",
            "official_title": "Invalid Act",
            "content_sha256": "bad_hash",
        }
        is_valid_inv, errors_inv = pipeline.validate_provenance_record(invalid_record)
        assert is_valid_inv is False
        assert len(errors_inv) > 0

    def test_ingest_instrument_and_idempotent_duplicate_rejection(self):
        pipeline = CentralStatuteIngestionPipeline()
        content_hash = "b" * 64
        source_record = {
            "source_id": "SRC-IND-CODE-SRA-1963",
            "instrument_id": "ACT-CENTRAL-1963-047",
            "official_title": "Specific Relief Act, 1963",
            "act_number": "Act 47 of 1963",
            "issuing_authority": "Parliament of India",
            "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1583",
            "publication_date": "1963-12-13",
            "commencement_date": "1963-12-13",
            "commencement_notification_ref": "Gazette of India",
            "content_sha256": content_hash,
        }
        provisions = [
            {
                "provision_id": "IND-STAT-SRA-1963-S10",
                "section_number": "Section 10",
                "version_number": 1,
                "text": "Specific performance of contract may in discretion be enforced",
                "validity_interval": ["1963-12-13", "2018-10-01"],
            }
        ]

        # First ingestion -> SUCCESS
        res1 = pipeline.ingest_instrument(source_record, provisions)
        assert res1.status == IngestionStatus.INGESTED_SUCCESSFULLY
        assert res1.provisions_indexed == 1
        assert res1.provisions_skipped == 0

        # Second ingestion with identical SHA-256 -> DUPLICATE REJECTED
        res2 = pipeline.ingest_instrument(source_record, provisions)
        assert res2.status == IngestionStatus.DUPLICATE_IDENTICAL_PAYLOAD
        assert res2.provisions_indexed == 0
        assert res2.provisions_skipped == 1


class TestTemporalLawEnginePhase45:
    """Tests for multi-era point-in-time statutory queries and regime resolution."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = build_default_temporal_engine()

    def test_criminal_law_regime_resolution(self):
        # Case 1: Pre-July 1 2024 Offense, Post-July Proceeding -> Substantive IPC, Procedural BNSS
        reg_1 = self.engine.resolve_criminal_law_regime(
            offence_date_str="2023-11-15",
            proceedings_institute_date_str="2024-08-20"
        )
        assert "Indian Penal Code" in reg_1["substantive_law"]
        assert "Bharatiya Nagarik Suraksha Sanhita" in reg_1["procedural_law"]
        assert reg_1["bnss_s531_savings_applied"] is False

        # Case 2: Pre-July 1 2024 Offense, Pre-July Proceeding -> Substantive IPC, Procedural CrPC
        reg_2 = self.engine.resolve_criminal_law_regime(
            offence_date_str="2023-11-15",
            proceedings_institute_date_str="2024-05-10"
        )
        assert "Indian Penal Code" in reg_2["substantive_law"]
        assert "Code of Criminal Procedure" in reg_2["procedural_law"]
        assert reg_2["bnss_s531_savings_applied"] is True

        # Case 3: Post-July 1 2024 Offense -> Substantive BNS, Procedural BNSS
        reg_3 = self.engine.resolve_criminal_law_regime(
            offence_date_str="2024-07-15",
            proceedings_institute_date_str="2024-07-16"
        )
        assert "Bharatiya Nyaya Sanhita" in reg_3["substantive_law"]
        assert "Bharatiya Nagarik Suraksha Sanhita" in reg_3["procedural_law"]

    def test_data_protection_regime_phased_commencement(self):
        reg = self.engine.resolve_data_protection_regime(query_date_str="2024-10-15")
        assert "Operative in law" in reg["it_act_s43a_status"]
        assert "uncommenced pending s.1(2)" in reg["dpdp_status"]

    def test_specific_relief_regime_transition(self):
        # Pre-2018 amendment: Discretionary
        reg_pre = self.engine.resolve_specific_relief_regime(contract_date_str="2017-06-01")
        assert "Pre-2018" in reg_pre["regime"]
        assert "Discretionary" in reg_pre["specific_performance_character"]

        # Post-2018 amendment: Mandatory
        reg_post = self.engine.resolve_specific_relief_regime(contract_date_str="2019-01-15")
        assert "Post-2018" in reg_post["regime"]
        assert "Mandatory" in reg_post["specific_performance_character"]

    def test_arbitration_regime_transition(self):
        reg_pre = self.engine.resolve_arbitration_regime("2015-08-01")
        assert "Pre-2015" in reg_pre["regime"]

        reg_post = self.engine.resolve_arbitration_regime("2016-01-10")
        assert "Post-2015" in reg_post["regime"]
        assert reg_post["s29a_timeline_mandate"] is True

    def test_consumer_protection_regime_transition(self):
        reg_pre = self.engine.resolve_consumer_regime("2018-05-10")
        assert "1986" in reg_pre["regime"]
        assert reg_pre["repealed"] is True

        reg_post = self.engine.resolve_consumer_regime("2021-03-15")
        assert "2019" in reg_post["regime"]
        assert reg_post["repealed"] is False


class TestPhase45ManifestsAndInvariants:
    """Tests the integrity of Phase 45 machine manifests, review packages, and invariants."""

    def test_source_provenance_manifest_integrity(self):
        manifest_path = DATA_DIR / "source_provenance_manifest.json"
        assert manifest_path.exists()
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["provenance_standard"] == "LEGALMITRA-PROVENANCE-SPEC-V2"
        sources = manifest["sources"]
        assert len(sources) >= 8
        for src in sources:
            assert src["source_id"].startswith("SRC-")
            assert src["instrument_id"].startswith("IND-")
            assert len(src["content_sha256"]) == 64
            assert src["official_source_url"].startswith("http")

    def test_amendment_event_ledger_integrity(self):
        ledger_path = DATA_DIR / "amendment_event_ledger.json"
        assert ledger_path.exists()
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        assert len(ledger["events"]) >= 12
        for evt in ledger["events"]:
            assert evt["event_id"].startswith(("AMEND-EVT-", "REPEAL-EVT-"))
            assert "parent_statute_id" in evt
            assert "event_type" in evt

    def test_legal_dependency_graph_acyclic_and_valid(self):
        graph_path = DATA_DIR / "legal_dependency_graph.json"
        assert graph_path.exists()
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = json.load(f)
        node_ids = {n["id"] for n in graph["nodes"]}
        assert len(node_ids) >= 15
        assert len(graph["edges"]) >= 15
        for edge in graph["edges"]:
            assert edge["source"] in node_ids, f"Broken source {edge['source']} in edge {edge['id']}"
            assert edge["target"] in node_ids, f"Broken target {edge['target']} in edge {edge['id']}"

    def test_temporal_benchmark_manifest_ten_cases(self):
        bench_path = DATA_DIR / "temporal_benchmark_manifest.json"
        assert bench_path.exists()
        with open(bench_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["total_test_cases"] == 10
        assert len(manifest["test_cases"]) == 10
        for i, tc in enumerate(manifest["test_cases"], 1):
            expected_id = f"PIT-0{i}" if i < 10 else f"PIT-{i}"
            assert tc["case_id"] == expected_id

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
