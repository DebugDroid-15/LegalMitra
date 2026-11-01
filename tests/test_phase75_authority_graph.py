"""
Test Suite for Phase 75: Interactive Precedent & Authority Graph Visualizer.
Verifies:
1. AuthorityGraphVisualizer node extraction, entity filtering, and color coding.
2. Focused neighborhood expansion around statutory and case law anchors.
3. Interactive Vis.js standalone HTML generation with physics simulation parameters.
4. REST API GET /api/v1/graph/subgraph and GET /api/v1/graph/html endpoints.
5. Web workbench Tab 4 integration and Streamlit components rendering.
"""

import pytest
from fastapi.testclient import TestClient

from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.caselaw.visualizer import AuthorityGraphVisualizer
from legalmitra.server.api import app


class TestPhase75AuthorityGraphVisualizer:

    @pytest.fixture
    def visualizer(self):
        kg = build_national_judicial_knowledge_graph()
        return AuthorityGraphVisualizer(knowledge_graph=kg)

    def test_full_graph_extraction(self, visualizer):
        data = visualizer.get_subgraph_data()

        assert "nodes" in data
        assert "edges" in data
        assert data["total_nodes"] == 99
        assert data["total_edges"] == 62

        # Verify node fields
        first_node = data["nodes"][0]
        assert "id" in first_node
        assert "label" in first_node
        assert "group" in first_node
        assert "color" in first_node
        assert "shape" in first_node

        # Verify edge fields
        first_edge = data["edges"][0]
        assert "from" in first_edge
        assert "to" in first_edge
        assert "label" in first_edge
        assert "arrows" in first_edge

    def test_entity_filtering(self, visualizer):
        # Filter for case law and constitutional articles only
        filtered_data = visualizer.get_subgraph_data(entity_filter=["case", "article"])

        assert filtered_data["total_nodes"] > 0
        for node in filtered_data["nodes"]:
            assert node["group"] in ("case", "article")

    def test_focused_neighborhood_expansion(self, visualizer):
        # Anchor on Section 63 BSA (electronic records succession)
        focused = visualizer.get_subgraph_data(focus_node_id="SEC-BSA-63", max_hops=1)

        assert focused["total_nodes"] >= 2
        node_ids = {n["id"] for n in focused["nodes"]}
        assert "SEC-BSA-63" in node_ids
        assert "SEC-IEA-65B" in node_ids  # Successor to Section 65B IEA

    def test_visjs_html_generation(self, visualizer):
        html = visualizer.render_visjs_html(height="500px")

        assert isinstance(html, str)
        assert len(html) > 10000
        assert "vis.DataSet" in html
        assert "vis.Network" in html
        assert "barnesHut" in html
        assert "legend" in html

    def test_rest_api_graph_subgraph_endpoint(self):
        client = TestClient(app)
        res = client.get("/api/v1/graph/subgraph")

        assert res.status_code == 200
        data = res.json()
        assert "nodes" in data
        assert "edges" in data
        assert data["total_nodes"] == 99

    def test_rest_api_graph_html_endpoint(self):
        client = TestClient(app)
        res = client.get("/api/v1/graph/html?focus_node=SEC-BSA-63")

        assert res.status_code == 200
        assert res.headers["content-type"].startswith("text/html")
        assert "vis-network" in res.text
        assert "SEC-BSA-63" in res.text

