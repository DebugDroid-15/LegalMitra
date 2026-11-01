"""Visual Precedent & Statutory Authority Graph Explorer (Phase 75).

Extracts, filters, and formats subgraphs from the 99-node National Judicial
Knowledge Graph into interactive HTML/Vis.js network visualizers and JSON payloads
for the Web Workbench and REST API.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Set

from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    LegalKnowledgeGraph,
    RelationType,
    build_national_judicial_knowledge_graph,
)


class AuthorityGraphVisualizer:
    """Renders interactive and filtered authority networks of statutes and case laws."""

    # Color palette by EntityType
    COLOR_MAP = {
        "statute": {"background": "#EBF8FF", "border": "#3182CE", "highlight": "#2B6CB0"},
        "section": {"background": "#EDFDFD", "border": "#319795", "highlight": "#285E61"},
        "article": {"background": "#FAF5FF", "border": "#805AD5", "highlight": "#553C9A"},
        "case": {"background": "#FFF5F5", "border": "#E53E3E", "highlight": "#9B2C2C"},
        "delegated_rule": {"background": "#F0FFF4", "border": "#38A169", "highlight": "#22543D"},
    }

    # Relation line colors
    RELATION_COLOR_MAP = {
        "overrules": "#E53E3E",
        "partially_overrules": "#DD6B20",
        "conflicts_with": "#E53E3E",
        "successor_to": "#3182CE",
        "interprets": "#805AD5",
        "affirms": "#38A169",
        "follows": "#38A169",
        "applies": "#4A5568",
        "refers_to_larger_bench": "#D69E2E",
        "stayed": "#C53030",
        "distinguishes": "#4A5568",
    }

    def __init__(self, knowledge_graph: Optional[LegalKnowledgeGraph] = None):
        self.kg = knowledge_graph or build_national_judicial_knowledge_graph()

    def get_subgraph_data(
        self,
        focus_node_id: Optional[str] = None,
        entity_filter: Optional[List[str]] = None,
        max_hops: int = 1,
    ) -> Dict[str, Any]:
        """
        Extracts nodes and edges for visualization, optionally centering around a focus node.
        """
        included_node_ids: Set[str] = set()

        if focus_node_id and focus_node_id in self.kg._nodes:
            included_node_ids.add(focus_node_id)
            current_level = {focus_node_id}
            for _ in range(max_hops):
                next_level = set()
                for nid in current_level:
                    # Collect targets
                    for e in self.kg.get_outgoing_edges(nid):
                        included_node_ids.add(e.target_id)
                        next_level.add(e.target_id)
                    # Collect sources
                    for e in self.kg.get_incoming_edges(nid):
                        included_node_ids.add(e.source_id)
                        next_level.add(e.source_id)
                current_level = next_level
        else:
            # Include all nodes matching entity filter
            for nid, node in self.kg._nodes.items():
                etype = node.entity_type.value if hasattr(node.entity_type, "value") else str(node.entity_type)
                if not entity_filter or etype in entity_filter:
                    included_node_ids.add(nid)

        nodes_list = []
        for nid in included_node_ids:
            if nid not in self.kg._nodes:
                continue
            n = self.kg._nodes[nid]
            etype = n.entity_type.value if hasattr(n.entity_type, "value") else str(n.entity_type)
            c = self.COLOR_MAP.get(etype, {"background": "#EDF2F7", "border": "#4A5568", "highlight": "#2D3748"})
            nodes_list.append({
                "id": n.node_id,
                "label": n.name,
                "group": etype,
                "title": f"<b>{n.name}</b><br/>Type: {etype}<br/>Citation: {n.canonical_citation or 'N/A'}<br/>Jurisdiction: {n.jurisdiction}",
                "color": c,
                "shape": "box" if etype in ("statute", "section", "article") else "ellipse",
            })

        edges_list = []
        for e in self.kg._edges.values():
            if e.source_id in included_node_ids and e.target_id in included_node_ids:
                rel = e.relation.value if hasattr(e.relation, "value") else str(e.relation)
                col = self.RELATION_COLOR_MAP.get(rel, "#718096")
                is_dashed = rel in ("conflicts_with", "stayed", "refers_to_larger_bench")
                edges_list.append({
                    "from": e.source_id,
                    "to": e.target_id,
                    "label": rel.replace("_", " "),
                    "arrows": "to",
                    "color": {"color": col, "highlight": col},
                    "dashes": is_dashed,
                    "font": {"size": 9, "align": "middle", "color": "#4A5568"},
                })

        return {
            "nodes": nodes_list,
            "edges": edges_list,
            "total_nodes": len(nodes_list),
            "total_edges": len(edges_list),
        }

    def render_visjs_html(
        self,
        focus_node_id: Optional[str] = None,
        entity_filter: Optional[List[str]] = None,
        height: str = "550px",
    ) -> str:
        """
        Renders a self-contained interactive Vis.js graph in HTML with physics layout.
        """
        data = self.get_subgraph_data(focus_node_id=focus_node_id, entity_filter=entity_filter)
        nodes_json = json.dumps(data["nodes"])
        edges_json = json.dumps(data["edges"])

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        #network {{
            width: 100%;
            height: {height};
            border: 1px solid #E2E8F0;
            background-color: #F8FAFC;
            border-radius: 8px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .legend {{
            margin-top: 8px;
            font-size: 12px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            color: #4A5568;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .legend-box {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div id="network"></div>
    <div class="legend">
        <div class="legend-item"><div class="legend-box" style="background:#EBF8FF;border:1px solid #3182CE;"></div>Statute</div>
        <div class="legend-item"><div class="legend-box" style="background:#EDFDFD;border:1px solid #319795;"></div>Section / Provision</div>
        <div class="legend-item"><div class="legend-box" style="background:#FAF5FF;border:1px solid #805AD5;"></div>Article</div>
        <div class="legend-item"><div class="legend-box" style="background:#FFF5F5;border:1px solid #E53E3E;border-radius:50%;"></div>Case Law / Precedent</div>
        <div class="legend-item"><div class="legend-box" style="background:#F0FFF4;border:1px solid #38A169;"></div>Delegated Rule</div>
        <div class="legend-item" style="margin-left:auto;"><i>Click & Drag nodes • Scroll to Zoom</i></div>
    </div>
    <script type="text/javascript">
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json});
        var container = document.getElementById('network');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            nodes: {{
                font: {{ size: 12, face: 'Segoe UI, Arial' }},
                borderWidth: 1.5,
                shadow: true
            }},
            edges: {{
                width: 1.5,
                smooth: {{ type: 'cubicBezier', roundness: 0.2 }}
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -3500,
                    centralGravity: 0.3,
                    springLength: 95,
                    springConstant: 0.04
                }},
                maxVelocity: 50,
                minVelocity: 0.1,
                solver: 'barnesHut',
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                navigationButtons: true,
                tooltipDelay: 100
            }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
        return html_template

