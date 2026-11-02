"""
Phase 85 Test Suite: Multi-Source Sovereign Ingestion Connectors & Pipeline
Validates end-to-end ingestion, checksum verification, and registry persistence across:
- India Code (IPC, CrPC, IEA, IT Act, NI Act)
- AI Kosh (MHA S.O. 848(E), S.O. 849(E), Legal Lexicon)
- Hugging Face (InLegalEval, ILQA)
- Kaggle e-SCR (Arnesh Kumar, Bhajan Lal, NCDRC)
"""

import tempfile
from pathlib import Path
import pytest

from legalmitra.core.enums import SourceType
from legalmitra.ingestion.connectors import (
    AIKoshConnector,
    HuggingFaceConnector,
    IndiaCodeConnector,
    IngestionOrigin,
    KaggleESCRConnector,
    MultiSourceIngestionPipeline,
)


class TestPhase85MultiSourceIngestion:

    def test_indiacode_connector_fetches_core_penal_acts(self):
        connector = IndiaCodeConnector()
        docs = connector.fetch_documents()

        assert len(docs) >= 5
        doc_ids = [d.document_id for d in docs]
        assert "IND-STAT-IPC-1860-ACT45" in doc_ids
        assert "IND-STAT-CRPC-1973-ACT02" in doc_ids
        assert "IND-STAT-IEA-1872-ACT01" in doc_ids
        assert "IND-STAT-IT-2000-ACT21" in doc_ids
        assert "IND-STAT-NIA-1881-ACT26" in doc_ids

        ipc_doc = next(d for d in docs if d.document_id == "IND-STAT-IPC-1860-ACT45")
        assert "Indian Penal Code" in ipc_doc.title
        assert ipc_doc.origin == IngestionOrigin.INDIA_CODE
        assert ipc_doc.compute_sha256() is not None
        assert ipc_doc.get_byte_size() > 100

    def test_aikosh_connector_fetches_gazette_notifications(self):
        connector = AIKoshConnector()
        docs = connector.fetch_documents()

        assert len(docs) >= 3
        doc_ids = [d.document_id for d in docs]
        assert "AIKOSH-GAZ-2024-MHA-SO848E" in doc_ids
        assert "AIKOSH-GAZ-2024-MHA-SO849E" in doc_ids

        so848e = next(d for d in docs if d.document_id == "AIKOSH-GAZ-2024-MHA-SO848E")
        assert so848e.source_type == SourceType.GAZETTE
        assert "106" in so848e.content_raw

    def test_huggingface_connector_fetches_gold_benchmark_pairs(self):
        connector = HuggingFaceConnector()
        docs = connector.fetch_documents()

        assert len(docs) >= 2
        rr_doc = next(d for d in docs if d.document_id == "HF-INLEGALEVAL-RR-SAMPLE01")
        assert "InLegalEval" in rr_doc.title
        assert "[RATIO]" in rr_doc.content_raw

    def test_kaggle_escr_connector_fetches_landmark_rulings(self):
        connector = KaggleESCRConnector()
        docs = connector.fetch_documents()

        assert len(docs) >= 3
        arnesh = next(d for d in docs if d.document_id == "KAG-JUD-SC-2014-ARNESH-KUMAR")
        bhajan = next(d for d in docs if d.document_id == "KAG-JUD-SC-1992-BHAJAN-LAL")

        assert "Arnesh Kumar" in arnesh.title
        assert "Section 41 CrPC" in arnesh.content_raw
        assert "Bhajan Lal" in bhajan.title
        assert "SEVEN GUIDELINES" in bhajan.content_raw

    def test_multi_source_orchestrator_end_to_end_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_dir = tmp_path / "raw"
            registry_file = tmp_path / "test_registry.jsonl"

            pipeline = MultiSourceIngestionPipeline(
                raw_storage_dir=raw_dir,
                registry_file=registry_file
            )

            # First run: All documents should be newly registered
            res1 = pipeline.run()
            assert res1.total_fetched >= 13
            assert res1.new_registered == res1.total_fetched
            assert res1.already_existing == 0
            assert res1.failed == 0

            # Verify files were saved to disk
            for doc_id in res1.registered_ids:
                expected_file = raw_dir / f"{doc_id}.txt"
                assert expected_file.exists()
                assert expected_file.stat().st_size > 0

            # Second run: Idempotence check - all documents should be recognized as existing
            res2 = pipeline.run()
            assert res2.total_fetched == res1.total_fetched
            assert res2.new_registered == 0
            assert res2.already_existing == res1.total_fetched
            assert res2.failed == 0
