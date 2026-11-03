"""
Phase 87 Test Suite: Extended Tri-Code Crosswalk & Temporal Knowledge Graph
Validates bidirectional mappings between IPC/CrPC/IEA and BNS/BNSS/BSA,
precedent lineage graph traversal, and incident date-based savings clause routing.
"""

from pathlib import Path
import pytest

from legalmitra.corpus.tri_code_crosswalk import (
    EquivalenceType,
    ExtendedTriCodeKnowledgeGraph,
    TransitionRegime,
)


class TestPhase87TriCodeCrosswalk:

    @pytest.fixture
    def graph(self):
        return ExtendedTriCodeKnowledgeGraph()

    def test_matrix_loading_and_scale(self, graph):
        assert len(graph._entries) >= 20
        # Check IPC, CRPC, and IEA are present
        old_codes = {e.old_code for e in graph._entries.values()}
        assert "IPC" in old_codes
        assert "CRPC" in old_codes
        assert "IEA" in old_codes

    def test_ipc_to_bns_cheating_lookup(self, graph):
        matches = graph.lookup_old_provision("IPC", "420")
        assert len(matches) >= 1
        m = matches[0]
        assert m.new_code == "BNS"
        assert "318" in m.new_section
        assert m.equivalence_type == EquivalenceType.SUCCESSOR_PROVISION
        assert "Hridaya Ranjan Prasad Verma" in " ".join(m.landmark_judgments)

    def test_bns_to_ipc_breach_of_trust_lookup(self, graph):
        matches = graph.lookup_new_provision("BNS", "316(1)")
        if not matches:
            matches = graph.lookup_new_provision("BNS", "316")
        assert len(matches) >= 1
        m = matches[0]
        assert m.old_code == "IPC"
        assert "405" in m.old_section
        assert "Chelloor Mankkal" in " ".join(m.landmark_judgments)

    def test_crpc_to_bnss_fir_and_quashing_lookups(self, graph):
        # 1. Section 154 CrPC -> Section 173 BNSS
        fir_matches = graph.lookup_old_provision("CRPC", "154")
        assert len(fir_matches) >= 1
        assert "173" in fir_matches[0].new_section
        assert "Lalita Kumari" in " ".join(fir_matches[0].landmark_judgments)

        # 2. Section 482 CrPC -> Section 528 BNSS
        quash_matches = graph.lookup_old_provision("CRPC", "482")
        assert len(quash_matches) >= 1
        assert "528" in quash_matches[0].new_section
        assert "Bhajan Lal" in " ".join(quash_matches[0].landmark_judgments)

    def test_iea_to_bsa_electronic_evidence_lookup(self, graph):
        matches = graph.lookup_old_provision("IEA", "65B")
        assert len(matches) >= 1
        m = matches[0]
        assert m.new_code == "BSA"
        assert "63" in m.new_section
        assert "Arjun Panditrao Khotkar" in " ".join(m.landmark_judgments)

    def test_precedent_graph_retrieval_across_eras(self, graph):
        # Searching by modern section should retrieve historic landmark precedents
        precedents = graph.get_precedents_for_provision("BNS", "85")
        assert len(precedents) >= 1
        assert any("Arnesh Kumar" in p for p in precedents)

        # Searching by old section should also retrieve precedents
        crpc_precedents = graph.get_precedents_for_provision("CRPC", "41")
        assert len(crpc_precedents) >= 1
        assert any("Arnesh Kumar" in p for p in precedents)

    def test_temporal_savings_clause_pre_july_2024(self, graph):
        decision = graph.route_by_incident_date("2024-05-15")
        assert decision.regime == TransitionRegime.HISTORIC_PRE_2024
        assert "Indian Penal Code, 1860" in decision.substantive_code
        assert "Code of Criminal Procedure, 1973" in decision.procedural_code
        assert "Section 531" in decision.savings_clause_citation
        assert "Article 20(1)" in decision.legal_explanation

    def test_temporal_savings_clause_post_july_2024(self, graph):
        decision = graph.route_by_incident_date("2024-09-01")
        assert decision.regime == TransitionRegime.MODERN_POST_2024
        assert "Bharatiya Nyaya Sanhita, 2023" in decision.substantive_code
        assert "Bharatiya Nagarik Suraksha Sanhita, 2023" in decision.procedural_code
        assert "Bharatiya Sakshya Adhiniyam, 2023" in decision.evidence_code
        assert "S.O. 848(E)" in decision.savings_clause_citation
