"""
LegalMitra National Legal Knowledge Graph Engine
Models multi-relational graphs linking Constitutional provisions, Statutes, Sections,
Delegated Rules, Court Decisions, Judges, and Litigation Practice concepts.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class EntityType(str, Enum):
    CONSTITUTION = "constitution"
    ARTICLE = "article"
    STATUTE = "statute"
    SECTION = "section"
    DELEGATED_RULE = "delegated_rule"
    COURT = "court"
    JUDGE = "judge"
    CASE = "case"
    LEGAL_CONCEPT = "legal_concept"
    PROCEDURAL_STAGE = "procedural_stage"


class RelationType(str, Enum):
    # Statutory & Constitutional Relations
    CONTAINS = "contains"                        # Statute -> Section; Constitution -> Article
    EMPOWERS = "empowers"                        # Section -> Delegated Rule
    AMENDS = "amends"                            # Amending Act -> Section
    REPEALS = "repeals"                          # Act -> Act
    SUCCESSOR_TO = "successor_to"                # BNS Section 103 -> IPC Section 302
    
    # Judicial & Precedent Relations
    CITES = "cites"                              # Case -> Case / Section
    INTERPRETS = "interprets"                    # Case -> Section / Article
    FOLLOWS = "follows"                          # Case -> Case
    APPLIES = "applies"                          # Case -> Case
    DISTINGUISHES = "distinguishes"              # Case -> Case
    OVERRULES = "overrules"                      # Case -> Case
    DECIDED_BY = "decided_by"                    # Case -> Court
    HEARD_BY = "heard_by"                        # Case -> Judge
    
    # Procedural & Practice Relations
    GOVERNS_STAGE = "governs_stage"              # Section -> Procedural Stage
    EXEMPLIFIES = "exemplifies"                  # Case -> Legal Concept


@dataclass
class GraphNode:
    node_id: str
    entity_type: EntityType
    name: str
    canonical_citation: str = ""
    jurisdiction: str = "IN"
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["entity_type"] = self.entity_type.value
        return d


@dataclass
class GraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation: RelationType
    properties: Dict[str, Any] = field(default_factory=dict)
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["relation"] = self.relation.value
        return d


class LegalKnowledgeGraph:
    """
    In-memory graph index with multi-hop relational traversal and authority path resolution.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}
        self._outgoing: Dict[str, List[str]] = {}  # node_id -> [edge_id]
        self._incoming: Dict[str, List[str]] = {}  # node_id -> [edge_id]

    def add_node(self, node: GraphNode) -> None:
        self._nodes[node.node_id] = node
        self._outgoing.setdefault(node.node_id, [])
        self._incoming.setdefault(node.node_id, [])

    def add_edge(self, edge: GraphEdge) -> None:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError(f"Both source '{edge.source_id}' and target '{edge.target_id}' must exist in graph.")
        self._edges[edge.edge_id] = edge
        self._outgoing[edge.source_id].append(edge.edge_id)
        self._incoming[edge.target_id].append(edge.edge_id)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def get_outgoing_edges(self, node_id: str, relation: Optional[RelationType] = None) -> List[GraphEdge]:
        edge_ids = self._outgoing.get(node_id, [])
        edges = [self._edges[eid] for eid in edge_ids]
        if relation:
            edges = [e for e in edges if e.relation == relation]
        return edges

    def get_incoming_edges(self, node_id: str, relation: Optional[RelationType] = None) -> List[GraphEdge]:
        edge_ids = self._incoming.get(node_id, [])
        edges = [self._edges[eid] for eid in edge_ids]
        if relation:
            edges = [e for e in edges if e.relation == relation]
        return edges

    def get_precedents_for_provision(self, provision_node_id: str) -> List[GraphNode]:
        """Returns all cases that interpret or cite the given provision."""
        incoming = self.get_incoming_edges(provision_node_id)
        case_nodes = []
        for e in incoming:
            if e.relation in [RelationType.INTERPRETS, RelationType.CITES]:
                node = self.get_node(e.source_id)
                if node and node.entity_type == EntityType.CASE:
                    case_nodes.append(node)
        return case_nodes

    def get_successor_provision(self, old_provision_node_id: str) -> Optional[GraphNode]:
        """Finds the modern successor provision (e.g., IPC 302 -> BNS 103)."""
        incoming = self.get_incoming_edges(old_provision_node_id, RelationType.SUCCESSOR_TO)
        if incoming:
            return self.get_node(incoming[0].source_id)
        return None

    def is_case_overruled(self, case_node_id: str) -> Tuple[bool, Optional[str]]:
        """Checks if a case has been overruled by an incoming OVERRULES edge."""
        incoming = self.get_incoming_edges(case_node_id, RelationType.OVERRULES)
        if incoming:
            overruling_case = self.get_node(incoming[0].source_id)
            name = overruling_case.name if overruling_case else incoming[0].source_id
            return True, f"Overruled by {name}"
        return False, None

    def find_connected_subgraph(self, root_node_id: str, max_depth: int = 2) -> Dict[str, Any]:
        """Extracts an ego-network subgraph around a focal entity."""
        visited_nodes: Set[str] = set()
        collected_edges: List[GraphEdge] = []
        
        queue: List[Tuple[str, int]] = [(root_node_id, 0)]
        visited_nodes.add(root_node_id)

        while queue:
            curr_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.get_outgoing_edges(curr_id):
                collected_edges.append(edge)
                if edge.target_id not in visited_nodes:
                    visited_nodes.add(edge.target_id)
                    queue.append((edge.target_id, depth + 1))

            for edge in self.get_incoming_edges(curr_id):
                collected_edges.append(edge)
                if edge.source_id not in visited_nodes:
                    visited_nodes.add(edge.source_id)
                    queue.append((edge.source_id, depth + 1))

        nodes_data = [self._nodes[nid].to_dict() for nid in visited_nodes if nid in self._nodes]
        edges_data = [e.to_dict() for e in collected_edges]
        return {"nodes": nodes_data, "edges": edges_data}

