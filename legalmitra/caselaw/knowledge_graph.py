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
    APPROVES = "approves"                        # Case -> Case
    AFFIRMS = "affirms"                          # Case -> Case
    DISTINGUISHES = "distinguishes"              # Case -> Case
    DOUBTS = "doubts"                            # Case -> Case
    REFERS_TO_LARGER_BENCH = "refers_to_larger_bench"  # Case -> Case
    OVERRULES = "overrules"                      # Case -> Case
    PARTIALLY_OVERRULES = "partially_overrules"  # Case -> Case
    REVERSES = "reverses"                        # Case -> Case
    SETS_ASIDE = "sets_aside"                    # Case -> Case
    MODIFIES = "modifies"                        # Case -> Case
    REMANDS = "remands"                          # Case -> Case
    RECONSIDERS = "reconsiders"                  # Case -> Case
    DECLINES_TO_FOLLOW = "declines_to_follow"    # Case -> Case
    RELIES_ON = "relies_on"                      # Case -> Case
    CONSIDERS_CONSTITUTIONALITY = "considers_constitutionality"  # Case -> Section
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

    def is_case_overruled(
        self,
        case_node_id: str,
        target_proposition: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Checks if a case has been overruled.
        Returns: (is_overruled, reason_str)
        """
        incoming = self.get_incoming_edges(case_node_id, RelationType.OVERRULES)
        incoming.extend(self.get_incoming_edges(case_node_id, RelationType.PARTIALLY_OVERRULES))
        if not incoming:
            return False, None

        for edge in incoming:
            props = edge.properties or {}
            edge_prop = props.get("affected_proposition")
            is_partial = props.get("is_partial", False)
            scope = props.get("scope", "Entire judgment" if not is_partial else "Specific proposition")

            if target_proposition and edge_prop:
                if target_proposition.lower() not in edge_prop.lower() and edge_prop.lower() not in target_proposition.lower():
                    continue

            overruling_case = self.get_node(edge.source_id)
            name = overruling_case.name if overruling_case else edge.source_id
            
            status_desc = f"Partially overruled by {name} ({scope})" if is_partial else f"Overruled by {name}"
            return True, status_desc

        return False, None

    def evaluate_precedent_status(
        self,
        case_node_id: str,
        target_proposition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive doctrinal evaluation of precedent status.
        Includes scope, partial overruling, and affected propositions.
        """
        incoming = self.get_incoming_edges(case_node_id, RelationType.OVERRULES)
        incoming.extend(self.get_incoming_edges(case_node_id, RelationType.PARTIALLY_OVERRULES))
        if not incoming:
            return {"is_overruled": False, "status": "active_precedent", "overruling_cases": []}

        overruling_details = []
        for edge in incoming:
            props = edge.properties or {}
            overruling_case = self.get_node(edge.source_id)
            name = overruling_case.name if overruling_case else edge.source_id
            is_partial = props.get("is_partial", edge.relation == RelationType.PARTIALLY_OVERRULES)
            overruling_details.append({
                "overruling_case_id": edge.source_id,
                "overruling_case_name": name,
                "is_partial": is_partial,
                "scope": props.get("scope", "Entire judgment" if not is_partial else "Specific proposition"),
                "affected_proposition": props.get("affected_proposition")
            })


        return {
            "is_overruled": True,
            "status": "overruled" if not any(d["is_partial"] for d in overruling_details) else "partially_overruled",
            "overruling_details": overruling_details
        }



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


def build_national_judicial_knowledge_graph() -> LegalKnowledgeGraph:
    """Builds and returns the connected national litigation and statutory knowledge graph."""
    graph = LegalKnowledgeGraph()

    # 1. Statutory Provisions
    graph.add_node(GraphNode("SEC-BSA-63", EntityType.SECTION, "Section 63 BSA 2023", "BSA s.63"))
    graph.add_node(GraphNode("SEC-IEA-65B", EntityType.SECTION, "Section 65B IEA 1872", "IEA s.65B"))
    graph.add_node(GraphNode("SEC-NI-138", EntityType.SECTION, "Section 138 NI Act 1881", "NI Act s.138"))
    graph.add_node(GraphNode("SEC-NI-139", EntityType.SECTION, "Section 139 NI Act 1881", "NI Act s.139"))
    graph.add_node(GraphNode("SEC-ARB-11", EntityType.SECTION, "Section 11 Arb Act 1996", "Arbitration Act s.11"))
    graph.add_node(GraphNode("SEC-ARB-16", EntityType.SECTION, "Section 16 Arb Act 1996", "Arbitration Act s.16"))
    graph.add_node(GraphNode("ART-CONST-21", EntityType.ARTICLE, "Article 21 Constitution of India", "Art. 21"))
    graph.add_node(GraphNode("ART-CONST-14", EntityType.ARTICLE, "Article 14 Constitution of India", "Art. 14"))
    graph.add_node(GraphNode("ART-CONST-19", EntityType.ARTICLE, "Article 19 Constitution of India", "Art. 19"))
    graph.add_node(GraphNode("ART-CONST-368", EntityType.ARTICLE, "Article 368 Constitution of India", "Art. 368"))
    graph.add_node(GraphNode("SEC-CRPC-154", EntityType.SECTION, "Section 154 CrPC 1973", "CrPC s.154"))
    graph.add_node(GraphNode("SEC-BNSS-173", EntityType.SECTION, "Section 173 BNSS 2023", "BNSS s.173"))
    graph.add_node(GraphNode("SEC-CRPC-41", EntityType.SECTION, "Section 41 CrPC 1973", "CrPC s.41"))
    graph.add_node(GraphNode("SEC-BNSS-35", EntityType.SECTION, "Section 35 BNSS 2023", "BNSS s.35"))
    graph.add_node(GraphNode("SEC-CRPC-438", EntityType.SECTION, "Section 438 CrPC 1973", "CrPC s.438"))
    graph.add_node(GraphNode("SEC-BNSS-482", EntityType.SECTION, "Section 482 BNSS 2023", "BNSS s.482"))
    graph.add_node(GraphNode("SEC-IT-66A", EntityType.SECTION, "Section 66A IT Act 2000", "IT Act s.66A"))
    graph.add_node(GraphNode("SEC-IPC-304A", EntityType.SECTION, "Section 304A IPC 1860", "IPC s.304A"))
    graph.add_node(GraphNode("SEC-BNS-106", EntityType.SECTION, "Section 106 BNS 2023", "BNS s.106"))
    graph.add_node(GraphNode("SEC-ICA-56", EntityType.SECTION, "Section 56 Indian Contract Act 1872", "ICA s.56"))

    # 2. Case Nodes
    graph.add_node(GraphNode("CASE-ARJUN-KHOTKAR", EntityType.CASE, "Arjun Khotkar v. Kailash Gorantyal", "(2020) 7 SCC 1"))
    graph.add_node(GraphNode("CASE-ANVAR-PV", EntityType.CASE, "Anvar P.V. v. P.K. Basheer", "(2014) 10 SCC 473"))
    graph.add_node(GraphNode("CASE-SHAFHI-MOHD", EntityType.CASE, "Shafhi Mohammad v. State of H.P.", "(2018) 2 SCC 801"))
    graph.add_node(GraphNode("CASE-RANGAPPA", EntityType.CASE, "Rangappa v. Sri Mohan", "(2010) 11 SCC 441"))
    graph.add_node(GraphNode("CASE-KRISHNA-BHAT", EntityType.CASE, "Krishna Janardhan Bhat", "(2008) 4 SCC 54"))
    graph.add_node(GraphNode("CASE-STAMP-ARBITRATION", EntityType.CASE, "In Re: Arbitration Agreements & Stamp Act", "(2024) 6 SCC 1"))
    graph.add_node(GraphNode("CASE-NN-GLOBAL", EntityType.CASE, "NN Global Mercantile v. Indo Unique Flame", "(2023) 7 SCC 1"))
    graph.add_node(GraphNode("CASE-PUTTASWAMY", EntityType.CASE, "Justice K.S. Puttaswamy v. UOI", "(2017) 10 SCC 1"))
    # Phase 24 Additions
    graph.add_node(GraphNode("CASE-MANEKA-GANDHI", EntityType.CASE, "Maneka Gandhi v. Union of India", "(1978) 1 SCC 248"))
    graph.add_node(GraphNode("CASE-KESAVANANDA", EntityType.CASE, "Kesavananda Bharati v. State of Kerala", "(1973) 4 SCC 225"))
    graph.add_node(GraphNode("CASE-DK-BASU", EntityType.CASE, "D.K. Basu v. State of West Bengal", "(1997) 1 SCC 416"))
    graph.add_node(GraphNode("CASE-LALITA-KUMARI", EntityType.CASE, "Lalita Kumari v. Govt of UP", "(2014) 2 SCC 1"))
    graph.add_node(GraphNode("CASE-ARNESH-KUMAR", EntityType.CASE, "Arnesh Kumar v. State of Bihar", "(2014) 8 SCC 273"))
    graph.add_node(GraphNode("CASE-SHREYA-SINGHAL", EntityType.CASE, "Shreya Singhal v. Union of India", "(2015) 5 SCC 1"))
    graph.add_node(GraphNode("CASE-SUSHILA-AGGARWAL", EntityType.CASE, "Sushila Aggarwal v. State (NCT of Delhi)", "(2020) 5 SCC 1"))
    graph.add_node(GraphNode("CASE-SIBBIA", EntityType.CASE, "Gurbaksh Singh Sibbia v. State of Punjab", "(1980) 2 SCC 565"))
    graph.add_node(GraphNode("CASE-VIDYA-DROLIA", EntityType.CASE, "Vidya Drolia v. Durga Trading Corp.", "(2021) 2 SCC 1"))
    graph.add_node(GraphNode("CASE-HIMANGNI", EntityType.CASE, "Himangni Enterprises v. Kamaljeet Singh Ahluwalia", "(2017) 10 SCC 706"))
    graph.add_node(GraphNode("CASE-JACOB-MATHEW", EntityType.CASE, "Jacob Mathew v. State of Punjab", "(2005) 6 SCC 1"))
    graph.add_node(GraphNode("CASE-ENERGY-WATCHDOG", EntityType.CASE, "Energy Watchdog v. CERC", "(2017) 14 SCC 80"))

    # 3. Successor / Statutory Edges
    graph.add_edge(GraphEdge("E-SUCC-BSA63", "SEC-BSA-63", "SEC-IEA-65B", RelationType.SUCCESSOR_TO))
    graph.add_edge(GraphEdge("E-SUCC-BNSS173", "SEC-BNSS-173", "SEC-CRPC-154", RelationType.SUCCESSOR_TO))
    graph.add_edge(GraphEdge("E-SUCC-BNSS35", "SEC-BNSS-35", "SEC-CRPC-41", RelationType.SUCCESSOR_TO))
    graph.add_edge(GraphEdge("E-SUCC-BNSS482", "SEC-BNSS-482", "SEC-CRPC-438", RelationType.SUCCESSOR_TO))
    graph.add_edge(GraphEdge("E-SUCC-BNS106", "SEC-BNS-106", "SEC-IPC-304A", RelationType.SUCCESSOR_TO))

    # 4. Judicial Interpretation Edges
    graph.add_edge(GraphEdge("E-INT-ARJUN-65B", "CASE-ARJUN-KHOTKAR", "SEC-IEA-65B", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-ARJUN-BSA63", "CASE-ARJUN-KHOTKAR", "SEC-BSA-63", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-RANGAPPA-139", "CASE-RANGAPPA", "SEC-NI-139", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-STAMP-11", "CASE-STAMP-ARBITRATION", "SEC-ARB-11", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-PUTTA-21", "CASE-PUTTASWAMY", "ART-CONST-21", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-MANEKA-21", "CASE-MANEKA-GANDHI", "ART-CONST-21", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-MANEKA-14", "CASE-MANEKA-GANDHI", "ART-CONST-14", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-MANEKA-19", "CASE-MANEKA-GANDHI", "ART-CONST-19", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-KESAV-368", "CASE-KESAVANANDA", "ART-CONST-368", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-DKBASU-21", "CASE-DK-BASU", "ART-CONST-21", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-LALITA-154", "CASE-LALITA-KUMARI", "SEC-CRPC-154", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-LALITA-BNSS173", "CASE-LALITA-KUMARI", "SEC-BNSS-173", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-ARNESH-41", "CASE-ARNESH-KUMAR", "SEC-CRPC-41", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-ARNESH-BNSS35", "CASE-ARNESH-KUMAR", "SEC-BNSS-35", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-SHREYA-66A", "CASE-SHREYA-SINGHAL", "SEC-IT-66A", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-SUSHILA-438", "CASE-SUSHILA-AGGARWAL", "SEC-CRPC-438", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-SUSHILA-BNSS482", "CASE-SUSHILA-AGGARWAL", "SEC-BNSS-482", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-VIDYA-11", "CASE-VIDYA-DROLIA", "SEC-ARB-11", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-JACOB-304A", "CASE-JACOB-MATHEW", "SEC-IPC-304A", RelationType.INTERPRETS))
    graph.add_edge(GraphEdge("E-INT-ENERGY-56", "CASE-ENERGY-WATCHDOG", "SEC-ICA-56", RelationType.INTERPRETS))

    # 5. Precedent & Overruling Edges
    graph.add_edge(GraphEdge("E-FOLLOW-ARJUN-ANVAR", "CASE-ARJUN-KHOTKAR", "CASE-ANVAR-PV", RelationType.FOLLOWS))
    graph.add_edge(GraphEdge(
        "E-OVERRULE-ARJUN-SHAFHI", "CASE-ARJUN-KHOTKAR", "CASE-SHAFHI-MOHD", RelationType.PARTIALLY_OVERRULES,
        properties={"is_partial": True, "scope": "Electronic evidence certificate waiver", "affected_proposition": "Certificate waiver"}
    ))
    graph.add_edge(GraphEdge(
        "E-OVERRULE-RANGAPPA-BHAT", "CASE-RANGAPPA", "CASE-KRISHNA-BHAT", RelationType.OVERRULES,
        properties={"is_partial": False, "scope": "Entire dictum on Section 139 presumption not extending to debt"}
    ))
    graph.add_edge(GraphEdge(
        "E-OVERRULE-STAMP-NNGLOBAL", "CASE-STAMP-ARBITRATION", "CASE-NN-GLOBAL", RelationType.OVERRULES,
        properties={"is_partial": False, "scope": "Unstamped arbitration clause voidness at referral stage"}
    ))
    graph.add_edge(GraphEdge("E-AFFIRM-SUSHILA-SIBBIA", "CASE-SUSHILA-AGGARWAL", "CASE-SIBBIA", RelationType.AFFIRMS))
    graph.add_edge(GraphEdge(
        "E-OVERRULE-VIDYA-HIMANGNI", "CASE-VIDYA-DROLIA", "CASE-HIMANGNI", RelationType.OVERRULES,
        properties={"is_partial": False, "scope": "Non-arbitrability of landlord-tenant disputes governed by Transfer of Property Act"}
    ))

    return graph


