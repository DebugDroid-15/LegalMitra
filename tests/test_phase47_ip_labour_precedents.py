"""
LegalMitra Phase 47 — Intellectual Property Law, Labour Codes & Precedent-to-Statute Linking Test Suite
"""

import json
import pytest
from pathlib import Path

from legalmitra.temporal.engine import (
    TemporalLawEngine,
    StatuteLifecycle,
    ProvisionTemporalVersion,
    TemporalStatus,
    build_default_temporal_engine,
)
from legalmitra.caselaw.knowledge_graph import (
    LegalKnowledgeGraph,
    RelationType,
    EntityType,
    build_national_judicial_knowledge_graph,
)
from scripts.verify_freeze import verify_freeze

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "22_central_legislation"


class TestPhase47IPResolvers:
    """Tests for Intellectual Property regime resolution."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = build_default_temporal_engine()

    def test_copyright_2012_moral_rights_and_fair_dealing(self):
        # Case A: Pre-2012 (2010-04-15)
        res_pre = self.engine.resolve_copyright_regime("2010-04-15")
        assert "Pre-2012" in res_pre["regime"]
        assert "Restricted" in res_pre["moral_rights_status"] or "Subject to" in res_pre["moral_rights_status"]
        assert res_pre["educational_coursepack_protection"] is False
        assert res_pre["disability_accessible_format_exception"] is False
        assert res_pre["inalienable_author_royalties"] is False

        # Case B: Post-2012 (2018-06-25)
        res_post = self.engine.resolve_copyright_regime("2018-06-25")
        assert "Post-2012" in res_post["regime"]
        assert "Perpetual" in res_post["moral_rights_status"]
        assert res_post["educational_coursepack_protection"] is True
        assert res_post["disability_accessible_format_exception"] is True
        assert res_post["inalienable_author_royalties"] is True
        assert "S.O. 1393(E)" in res_post["notification_ref"]

    def test_patent_2005_therapeutic_efficacy_and_product_patents(self):
        # Case A: Pre-2005 (2001-08-10)
        res_pre = self.engine.resolve_patent_section3d_regime("2001-08-10")
        assert "Pre-2005" in res_pre["regime"]
        assert res_pre["product_patents_available"] is False
        assert res_pre["therapeutic_efficacy_mandate"] is False
        assert "Process / method" in res_pre["pharmaceutical_protection"]

        # Case B: Post-2005 (2014-05-12)
        res_post = self.engine.resolve_patent_section3d_regime("2014-05-12")
        assert "Post-2005" in res_post["regime"]
        assert res_post["product_patents_available"] is True
        assert res_post["therapeutic_efficacy_mandate"] is True
        assert "Novartis AG" in res_post["landmark_precedent"]

    def test_trademark_regime_and_madrid_accession(self):
        # Case A: Prior to 1999 Act commencement (2001-02-15)
        res_1958 = self.engine.resolve_trademark_regime("2001-02-15")
        assert res_1958["status"] == "HISTORICAL_PREDECESSOR"
        assert "1958" in res_1958["regime"]

        # Case B: Post-1999 Act, Pre-Madrid (2008-04-10)
        res_nat = self.engine.resolve_trademark_regime("2008-04-10")
        assert res_nat["status"] == "ACTIVE_NATIONAL"
        assert res_nat["madrid_protocol_active"] is False
        assert "Cadila" in res_nat["medicinal_deceptive_similarity_standard"]

        # Case C: Post-Madrid Protocol (2016-09-15)
        res_mad = self.engine.resolve_trademark_regime("2016-09-15")
        assert res_mad["status"] == "ACTIVE_INTERNATIONAL_ALIGNED"
        assert res_mad["madrid_protocol_active"] is True
        assert "S.O. 1999(E)" in res_mad["notification_ref"]


class TestPhase47LabourCodeResolvers:
    """Tests for Labour Code commencement status and predecessor preservation."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = build_default_temporal_engine()

    def test_code_on_wages_partial_commencement(self):
        status = self.engine.resolve_labour_code_commencement_status("IND-STAT-WAGES-2019")
        assert status["status"] == "PARTIALLY_COMMENCED"
        assert status["substantive_in_force"] is False
        assert status["repeal_in_force"] is False
        assert "142" in status["commenced_sections"]
        assert "Minimum Wages Act, 1948" in status["operative_predecessors"]
        assert "Payment of Wages Act, 1936" in status["operative_predecessors"]

    def test_industrial_relations_code_uncommenced(self):
        status = self.engine.resolve_labour_code_commencement_status("IND-STAT-IRCODE-2020")
        assert status["status"] == "ENACTED_UNCOMMENCED"
        assert status["substantive_in_force"] is False
        assert status["repeal_in_force"] is False
        assert len(status["commenced_sections"]) == 0
        assert "Industrial Disputes Act, 1947" in status["operative_predecessors"]

    def test_code_on_social_security_partial_commencement(self):
        status = self.engine.resolve_labour_code_commencement_status("IND-STAT-SSCODE-2020")
        assert status["status"] == "PARTIALLY_COMMENCED"
        assert status["substantive_in_force"] is False
        assert status["repeal_in_force"] is False
        assert "Employees' Provident Funds and Miscellaneous Provisions Act, 1952" in status["operative_predecessors"]
        assert "S.O. 1730(E)" in status["commenced_notifications"][0]

    def test_osh_code_uncommenced(self):
        status = self.engine.resolve_labour_code_commencement_status("IND-STAT-OSHCODE-2020")
        assert status["status"] == "ENACTED_UNCOMMENCED"
        assert status["substantive_in_force"] is False
        assert "Factories Act, 1948" in status["operative_predecessors"]

    def test_retrenchment_in_2024_governed_by_ida_1947(self):
        res = self.engine.resolve_industrial_disputes_retrenchment_regime("2024-10-15", continuous_service_days=250)
        assert res["governing_statute"] == "Industrial Disputes Act, 1947"
        assert res["is_ir_code_in_force"] is False
        assert res["ir_code_repeal_operative"] is False
        assert res["continuous_service_qualification"]["qualifies_continuous_service"] is True
        assert "American Express" in res["continuous_service_qualification"]["precedent_authority"]

    def test_ida_section25o_closure_across_excel_wear(self):
        # Window A: Pre-invalidation (1977-05-10)
        res_pre = self.engine.resolve_ida_closure_regime("1977-05-10")
        assert res_pre["status"] == "OPERATIVE_STATUTE"
        assert res_pre["is_constitutionally_valid"] is True

        # Window B: Invalidation interval (1979-02-14)
        res_inval = self.engine.resolve_ida_closure_regime("1979-02-14")
        assert res_inval["status"] == "JUDICIALLY_INVALIDATED"
        assert res_inval["is_constitutionally_valid"] is False
        assert "Excel Wear" in res_inval["landmark_precedent"]

        # Window C: Post-1984 reenactment (1990-11-20)
        res_post = self.engine.resolve_ida_closure_regime("1990-11-20")
        assert res_post["status"] == "OPERATIVE_REENACTED"
        assert res_post["is_constitutionally_valid"] is True


class TestPrecedentToStatuteLinking:
    """Tests for precedent-to-statute links and knowledge graph grounding."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = build_default_temporal_engine()
        self.kg = build_national_judicial_knowledge_graph()

    def test_precedent_manifest_structure(self):
        path = DATA_DIR / "precedent_statute_manifest.json"
        assert path.exists()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["total_links"] == 10
        assert len(data["links"]) == 10

        novartis = [l for l in data["links"] if l["case_id"] == "CASE-NOVARTIS-2013"][0]
        assert novartis["target_statute_id"] == "IND-STAT-PATENTS-1970"
        assert novartis["target_section"] == "3(d)"
        assert novartis["relationship_type"] == "INTERPRETS"
        assert "therapeutic efficacy" in novartis["holding_summary"]
        assert "Paras 157-192" in novartis["paragraph_anchor"]

    def test_resolve_precedent_query(self):
        links_pat = self.engine.resolve_precedent_for_provision("IND-STAT-PATENTS-1970", "3(d)")
        assert len(links_pat) >= 1
        assert links_pat[0]["case_id"] == "CASE-NOVARTIS-2013"

        links_ida = self.engine.resolve_precedent_for_provision("IND-STAT-IDA-1947", "25-O")
        assert len(links_ida) >= 1
        assert links_ida[0]["case_id"] == "CASE-EXCEL-WEAR-1978"
        assert links_ida[0]["relationship_type"] == "INVALIDATES"

    def test_caselaw_knowledge_graph_integration(self):
        node = self.kg.get_node("CASE-NOVARTIS-2013")
        assert node is not None
        assert node.canonical_citation == "(2013) 6 SCC 1"

        sec_node = self.kg.get_node("SEC-PAT-3D")
        assert sec_node is not None

        out_edges = self.kg.get_outgoing_edges("CASE-NOVARTIS-2013", RelationType.INTERPRETS)
        assert len(out_edges) >= 1
        assert out_edges[0].target_id == "SEC-PAT-3D"


class TestPhase47ManifestsAndInvariants:
    """Verifies manifest counts, benchmark expansion, and system invariants."""

    def test_manifest_record_counts(self):
        with open(DATA_DIR / "source_provenance_manifest.json", "r", encoding="utf-8") as f:
            sources = json.load(f)["sources"]
            assert len(sources) == 23

        with open(DATA_DIR / "provision_provenance_manifest.json", "r", encoding="utf-8") as f:
            provisions = json.load(f)["provisions"]
            assert len(provisions) == 46

        with open(DATA_DIR / "amendment_event_ledger.json", "r", encoding="utf-8") as f:
            events = json.load(f)["events"]
            assert len(events) == 28

        with open(DATA_DIR / "legal_dependency_graph.json", "r", encoding="utf-8") as f:
            graph = json.load(f)
            assert len(graph["nodes"]) == 48
            assert len(graph["edges"]) == 35

        with open(DATA_DIR / "temporal_benchmark_manifest.json", "r", encoding="utf-8") as f:
            cases = json.load(f)["test_cases"]
            assert len(cases) >= 30

    def test_pit_v3_benchmark_cases(self):
        with open(DATA_DIR / "temporal_benchmark_manifest.json", "r", encoding="utf-8") as f:
            cases = json.load(f)["test_cases"]

        case_map = {c["case_id"]: c for c in cases}
        # Check new Phase 47 benchmark cases
        assert "PIT-21" in case_map
        assert "PIT-24" in case_map
        assert "PIT-27" in case_map
        assert "PIT-30" in case_map

        assert "Section 57" in case_map["PIT-21"]["expected_governing_regime"]
        assert "Section 3(d)" in case_map["PIT-24"]["expected_governing_regime"]
        assert "Industrial Disputes Act, 1947" in case_map["PIT-27"]["expected_governing_regime"]
        assert "Excel Wear" in case_map["PIT-30"]["expected_precedent_cites"][0]

    def test_phase9_freeze_compliance(self):
        # Must return dict of 6 verified hashes without error
        res = verify_freeze()
        assert len(res) == 6
