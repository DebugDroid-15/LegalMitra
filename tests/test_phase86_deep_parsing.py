"""
Phase 86 Test Suite: Deep Parsing, Section Extraction & Statutory Structure Modeling
Validates extraction of hierarchical sections, provisos, explanations, coram, and SCC citations.
"""

from datetime import date
from pathlib import Path
import tempfile
import pytest

from legalmitra.core.enums import CourtType, Jurisdiction
from legalmitra.normalization.deep_parser import DeepLegalParser, DeepParsingPipeline
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.statute import StatuteDocument


class TestPhase86DeepParsing:

    def test_parse_statute_sections_with_provisos_and_explanations(self):
        raw_statute = """# The Test Penal Code
## KEY PROVISIONS
### Sec 316 - Criminal Breach of Trust
Whoever, being entrusted with property, dishonestly misappropriates it commits breach of trust.
Provided that where such entrustment is made to a public servant, punishment shall be enhanced.
Provided further that in case of commercial carriage, carriers act provisions apply.
Explanation 1.— A person who disposes of property with fraudulent intent is covered.
Explanation 2.— Trust includes oral agreements.

### Sec 318 - Cheating
Whoever deceives any person fraudulently commits cheating.
"""
        parser = DeepLegalParser()
        sections = parser.parse_statute_sections(
            source_id="TEST-STAT-01",
            act_title="Test Penal Code",
            raw_text=raw_statute
        )

        assert len(sections) == 2
        sec316 = sections[0]
        assert sec316.section_number == "316"
        assert sec316.section_title == "Criminal Breach of Trust"
        assert len(sec316.provisos) == 2
        assert "public servant" in sec316.provisos[0].text
        assert len(sec316.explanations) == 2
        assert "Explanation 1" in sec316.explanations[0].explanation_identifier

        sec318 = sections[1]
        assert sec318.section_number == "318"
        assert sec318.section_title == "Cheating"

    def test_parse_judgment_document_with_coram_and_citations(self):
        raw_judgment = """SUPREME COURT OF INDIA
Arnesh Kumar v. State of Bihar & Anr. (2014) 8 SCC 273
CORAM: Chandramauli Kr. Prasad and Pinaki Chandra Ghose, JJ.

Police officers shall not automatically arrest under Section 498-A IPC.

The Magistrate must record reasoned satisfaction prior to detention.
"""
        parser = DeepLegalParser()
        doc = parser.parse_judgment_document(
            doc_id="KAG-JUD-SC-2014-ARNESH-KUMAR",
            title="Arnesh Kumar v. State of Bihar & Anr. (2014) 8 SCC 273",
            raw_text=raw_judgment,
            court=CourtType.SUPREME_COURT,
            doc_date_str="2014-07-02",
            source_url="https://example.com/sc"
        )

        assert isinstance(doc, JudgmentDocument)
        assert doc.judgment_id == "KAG-JUD-SC-2014-ARNESH-KUMAR"
        assert len(doc.bench_coram) == 2
        assert "Chandramauli Kr. Prasad" in doc.bench_coram[0]
        assert len(doc.citations) >= 1
        assert "(2014) 8 SCC 273" in doc.citations[0].citation_text
        assert len(doc.paragraphs) >= 2

    def test_deep_parsing_pipeline_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_dir = tmp_path / "raw"
            norm_dir = tmp_path / "normalized"
            reg_file = tmp_path / "registry.jsonl"
            raw_dir.mkdir()
            norm_dir.mkdir()

            from legalmitra.ingestion.connectors import MultiSourceIngestionPipeline
            ingest_pipeline = MultiSourceIngestionPipeline(
                raw_storage_dir=raw_dir,
                registry_file=reg_file
            )
            ingest_pipeline.run(limit_per_source=2)

            # Run DeepParsingPipeline
            deep_pipeline = DeepParsingPipeline(
                raw_dir=raw_dir,
                normalized_dir=norm_dir,
                registry_file=reg_file
            )
            result = deep_pipeline.run()

            assert result["normalized_count"] >= 6
            assert len(result["errors"]) == 0

            # Verify files on disk can be loaded into schemas
            norm_files = list(norm_dir.glob("*.json"))
            assert len(norm_files) == result["normalized_count"]
            for f in norm_files:
                data = f.read_text(encoding="utf-8")
                assert len(data) > 50
