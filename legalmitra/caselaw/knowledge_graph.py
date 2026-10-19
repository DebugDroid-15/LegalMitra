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
    INVALIDATES = "invalidates"
    CONSIDERS_CONSTITUTIONALITY = "considers_constitutionality"  # Case -> Section
    DECIDED_BY = "decided_by"                    # Case -> Court
    HEARD_BY = "heard_by"                        # Case -> Judge
    STAYED = "stayed"                            # Order -> Case / Operation
    VACATED = "vacated"                          # Order -> Order / Decision
    LIMITS = "limits"                            # Case -> Case / Doctrine
    CONFLICTS_WITH = "conflicts_with"            # Case -> Case (divergent High Court or co-equal bench)
    SUPERSEDES_STATUTORY_BASIS = "supersedes_statutory_basis"  # Statute/Amendment -> Case proposition


    
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
        Includes scope, partial overruling, stays, larger-bench referrals,
        distinguishing treatments, conflicts, and legislative supersessions.
        """
        incoming_overrules = self.get_incoming_edges(case_node_id, RelationType.OVERRULES)
        incoming_overrules.extend(self.get_incoming_edges(case_node_id, RelationType.PARTIALLY_OVERRULES))

        incoming_stays = self.get_incoming_edges(case_node_id, RelationType.STAYED)
        incoming_referrals = self.get_incoming_edges(case_node_id, RelationType.REFERS_TO_LARGER_BENCH)
        outgoing_referrals = self.get_outgoing_edges(case_node_id, RelationType.REFERS_TO_LARGER_BENCH)
        incoming_distinguished = self.get_incoming_edges(case_node_id, RelationType.DISTINGUISHES)
        incoming_conflicts = self.get_incoming_edges(case_node_id, RelationType.CONFLICTS_WITH)
        outgoing_conflicts = self.get_outgoing_edges(case_node_id, RelationType.CONFLICTS_WITH)
        incoming_superseded = self.get_incoming_edges(case_node_id, RelationType.SUPERSEDES_STATUTORY_BASIS)

        # 1. Overruling Evaluation
        overruling_details = []
        for edge in incoming_overrules:
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

        # 2. Stay Evaluation
        stay_details = []
        for edge in incoming_stays:
            props = edge.properties or {}
            staying_entity = self.get_node(edge.source_id)
            stay_details.append({
                "staying_entity_id": edge.source_id,
                "staying_entity_name": staying_entity.name if staying_entity else edge.source_id,
                "scope": props.get("scope", "Interim stay on operation of judgment"),
                "is_interim": props.get("is_interim", True),
            })

        # 3. Referral to Larger Bench Evaluation
        referral_details = []
        for edge in incoming_referrals + outgoing_referrals:
            props = edge.properties or {}
            other_node_id = edge.target_id if edge.source_id == case_node_id else edge.source_id
            other_node = self.get_node(other_node_id)
            referral_details.append({
                "referring_case_id": edge.source_id,
                "target_case_id": edge.target_id,
                "other_case_name": other_node.name if other_node else other_node_id,
                "question_referred": props.get("question_referred", "Substantial question of law"),
                "bench_sought": props.get("bench_sought", "Larger Bench"),
                "is_resolved": props.get("is_resolved", False)
            })

        # 4. Distinguishing Treatments
        distinguished_details = []
        for edge in incoming_distinguished:
            props = edge.properties or {}
            dist_case = self.get_node(edge.source_id)
            distinguished_details.append({
                "distinguishing_case_id": edge.source_id,
                "distinguishing_case_name": dist_case.name if dist_case else edge.source_id,
                "distinguishing_ground": props.get("distinguishing_ground", "Factual / statutory divergence")
            })

        # 5. Precedent Conflicts
        conflict_details = []
        for edge in incoming_conflicts + outgoing_conflicts:
            other_id = edge.target_id if edge.source_id == case_node_id else edge.source_id
            other_case = self.get_node(other_id)
            props = edge.properties or {}
            conflict_details.append({
                "conflicting_case_id": other_id,
                "conflicting_case_name": other_case.name if other_case else other_id,
                "conflict_issue": props.get("conflict_issue", "Divergent interpretation of statutory provision"),
                "status": props.get("status", "UNRESOLVED_CONFLICT")
            })

        # 6. Legislative Supersession
        supersession_details = []
        for edge in incoming_superseded:
            props = edge.properties or {}
            stat_node = self.get_node(edge.source_id)
            supersession_details.append({
                "superseding_statute_id": edge.source_id,
                "superseding_statute_name": stat_node.name if stat_node else edge.source_id,
                "amendment_reference": props.get("amendment_reference", "Legislative amendment substituted text"),
                "amendment_date": props.get("amendment_date"),
                "effect_on_precedent": "Statutory basis superseded by legislative amendment"
            })

        # Synthesize primary precedent status
        if overruling_details:
            if not any(d["is_partial"] for d in overruling_details):
                primary_status = "overruled"
            else:
                primary_status = "partially_overruled"
        elif supersession_details:
            primary_status = "statutory_basis_superseded"
        elif stay_details:
            primary_status = "operation_stayed"
        elif referral_details and not any(r["is_resolved"] for r in referral_details):
            primary_status = "referred_to_larger_bench"
        elif conflict_details:
            primary_status = "conflicting_co_equal_authority"
        else:
            primary_status = "active_precedent"

        return {
            "case_id": case_node_id,
            "is_overruled": len(overruling_details) > 0,
            "status": primary_status,
            "is_good_law": primary_status in ["active_precedent", "partially_overruled", "conflicting_co_equal_authority"],
            "has_active_stay": len(stay_details) > 0,
            "is_referred": len(referral_details) > 0 and not all(r["is_resolved"] for r in referral_details),
            "overruling_details": overruling_details,
            "stay_details": stay_details,
            "referral_details": referral_details,
            "distinguished_by": distinguished_details,
            "conflicts": conflict_details,
            "superseded_by_legislation": supersession_details,
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

    # Phase 26 High Court Additions
    graph.add_node(GraphNode("SEC-IT-79", EntityType.SECTION, "Section 79 IT Act 2000", "IT Act s.79"))
    graph.add_node(GraphNode("CASE-DHC-LOUBOUTIN", EntityType.CASE, "Christian Louboutin SAS v. Nakul Bajaj", "2018:DHC:7175", "IN-DL"))
    graph.add_node(GraphNode("CASE-DHC-TATA-GREENPEACE", EntityType.CASE, "Tata Sons Ltd. v. Greenpeace International", "2011:DHC:452", "IN-DL"))

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
    # Phase 26 HC Interpretation Edges
    graph.add_edge(GraphEdge("E-INT-LOUBOUTIN-79", "CASE-DHC-LOUBOUTIN", "SEC-IT-79", RelationType.INTERPRETS, properties={"holding": "E-commerce platform active participation negates Section 79 safe harbor"}))
    graph.add_edge(GraphEdge("E-INT-GREENPEACE-19", "CASE-DHC-TATA-GREENPEACE", "ART-CONST-19", RelationType.INTERPRETS, properties={"holding": "Parody and fair public criticism protected under Article 19(1)(a)"}))

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


    # --- PHASE 47 INTELLECTUAL PROPERTY & LABOUR NODES ---
    # Section Nodes
    graph.add_node(GraphNode("SEC-PAT-3D", EntityType.SECTION, "Section 3(d) Patents Act 1970", "Patents Act s.3(d)"))
    graph.add_node(GraphNode("SEC-PAT-84", EntityType.SECTION, "Section 84 Patents Act 1970", "Patents Act s.84"))
    graph.add_node(GraphNode("SEC-COP-13", EntityType.SECTION, "Section 13 Copyright Act 1957", "Copyright Act s.13"))
    graph.add_node(GraphNode("SEC-COP-51", EntityType.SECTION, "Section 51 Copyright Act 1957", "Copyright Act s.51"))
    graph.add_node(GraphNode("SEC-COP-52", EntityType.SECTION, "Section 52 Copyright Act 1957", "Copyright Act s.52"))
    graph.add_node(GraphNode("SEC-TM-11", EntityType.SECTION, "Section 11 Trade Marks Act 1999", "Trade Marks Act s.11"))
    graph.add_node(GraphNode("SEC-IDA-2J", EntityType.SECTION, "Section 2(j) Industrial Disputes Act 1947", "IDA s.2(j)"))
    graph.add_node(GraphNode("SEC-IDA-25F", EntityType.SECTION, "Section 25F Industrial Disputes Act 1947", "IDA s.25F"))
    graph.add_node(GraphNode("SEC-IDA-25O", EntityType.SECTION, "Section 25-O Industrial Disputes Act 1947", "IDA s.25-O"))
    graph.add_node(GraphNode("SEC-IBC-32A", EntityType.SECTION, "Section 32A Insolvency & Bankruptcy Code 2016", "IBC s.32A"))

    # Landmark Case Nodes
    graph.add_node(GraphNode("CASE-NOVARTIS-2013", EntityType.CASE, "Novartis AG v. Union of India", "(2013) 6 SCC 1"))
    graph.add_node(GraphNode("CASE-BAYER-NATCO-2014", EntityType.CASE, "Bayer Corporation v. Union of India", "2014 SCC OnLine Bom 563", "IN-MH"))
    graph.add_node(GraphNode("CASE-EBC-MODAK-2008", EntityType.CASE, "Eastern Book Company v. D.B. Modak", "(2008) 1 SCC 1"))
    graph.add_node(GraphNode("CASE-RG-ANAND-1978", EntityType.CASE, "R.G. Anand v. Delux Films", "(1978) 4 SCC 118"))
    graph.add_node(GraphNode("CASE-RAMESHWARI-2016", EntityType.CASE, "Oxford University v. Rameshwari Photocopy Service", "2016 SCC OnLine Del 6229", "IN-DL"))
    graph.add_node(GraphNode("CASE-CADILA-2001", EntityType.CASE, "Cadila Health Care v. Cadila Pharmaceuticals", "(2001) 5 SCC 73"))
    graph.add_node(GraphNode("CASE-BANGALORE-WATER-1978", EntityType.CASE, "Bangalore Water Supply v. A. Rajappa", "(1978) 2 SCC 213"))
    graph.add_node(GraphNode("CASE-EXCEL-WEAR-1978", EntityType.CASE, "Excel Wear v. Union of India", "(1978) 4 SCC 224"))
    graph.add_node(GraphNode("CASE-AMEX-1985", EntityType.CASE, "Workmen of American Express v. Management", "(1985) 4 SCC 71"))
    graph.add_node(GraphNode("CASE-MANISH-KUMAR-2021", EntityType.CASE, "Manish Kumar v. Union of India", "(2021) 5 SCC 1"))

    # Phase 47 Precedent Interpretation / Application Edges
    graph.add_edge(GraphEdge("E-INT-NOVARTIS-3D", "CASE-NOVARTIS-2013", "SEC-PAT-3D", RelationType.INTERPRETS, properties={"holding": "Therapeutic efficacy requirement for polymorphs under Section 3(d)"}))
    graph.add_edge(GraphEdge("E-APP-BAYER-84", "CASE-BAYER-NATCO-2014", "SEC-PAT-84", RelationType.APPLIES, properties={"holding": "Compulsory licensing for unaffordable cancer drug Nexavar"}))
    graph.add_edge(GraphEdge("E-INT-EBC-13", "CASE-EBC-MODAK-2008", "SEC-COP-13", RelationType.INTERPRETS, properties={"holding": "Modicum of creativity standard for copyright originality"}))
    graph.add_edge(GraphEdge("E-INT-RGANAND-51", "CASE-RG-ANAND-1978", "SEC-COP-51", RelationType.INTERPRETS, properties={"holding": "Idea-expression dichotomy and substantial similarity"}))
    graph.add_edge(GraphEdge("E-INT-RAMESHWARI-52", "CASE-RAMESHWARI-2016", "SEC-COP-52", RelationType.INTERPRETS, properties={"holding": "Educational course pack fair dealing under Section 52(1)(i)"}))
    graph.add_edge(GraphEdge("E-INT-CADILA-11", "CASE-CADILA-2001", "SEC-TM-11", RelationType.INTERPRETS, properties={"holding": "Strict deceptive similarity standard for medicinal products"}))
    graph.add_edge(GraphEdge("E-INT-BANGALORE-2J", "CASE-BANGALORE-WATER-1978", "SEC-IDA-2J", RelationType.INTERPRETS, properties={"holding": "Triple test for industry under Section 2(j)"}))
    graph.add_edge(GraphEdge("E-INVAL-EXCEL-25O", "CASE-EXCEL-WEAR-1978", "SEC-IDA-25O", RelationType.INVALIDATES, properties={"holding": "Section 25-O closure permission struck down under Article 19(1)(g)"}))
    graph.add_edge(GraphEdge("E-APP-AMEX-25F", "CASE-AMEX-1985", "SEC-IDA-25F", RelationType.APPLIES, properties={"holding": "Continuous service of 240 days includes Sundays and paid holidays"}))
    graph.add_edge(GraphEdge("E-APP-MANISH-32A", "CASE-MANISH-KUMAR-2021", "SEC-IBC-32A", RelationType.APPLIES, properties={"holding": "Upholds Section 32A clean-slate immunity for corporate debtor"}))

    # --- PHASE 48 CONSTITUTION BENCH JURISPRUDENCE & DELEGATED REGISTRY NODES ---
    # Constitutional Articles
    graph.add_node(GraphNode("ART-CONST-31B", EntityType.ARTICLE, "Article 31B Constitution of India", "Art. 31B"))
    graph.add_node(GraphNode("ART-CONST-31C", EntityType.ARTICLE, "Article 31C Constitution of India", "Art. 31C"))
    graph.add_node(GraphNode("ART-CONST-245", EntityType.ARTICLE, "Article 245 Constitution of India", "Art. 245"))
    graph.add_node(GraphNode("ART-CONST-29", EntityType.ARTICLE, "Article 29 Constitution of India", "Art. 29"))
    graph.add_node(GraphNode("ART-CONST-15", EntityType.ARTICLE, "Article 15 Constitution of India", "Art. 15"))
    graph.add_node(GraphNode("ART-CONST-356", EntityType.ARTICLE, "Article 356 Constitution of India", "Art. 356"))

    # Constitution Bench Landmark Cases
    graph.add_node(GraphNode("CASE-SC-CONST-KESAVANANDA-1973", EntityType.CASE, "Kesavananda Bharati v. State of Kerala", "(1973) 4 SCC 225", properties={"bench_strength": 13, "majority_ratio": "7:6"}))
    graph.add_node(GraphNode("CASE-SC-CONST-MINERVA-MILLS-1980", EntityType.CASE, "Minerva Mills Ltd. v. Union of India", "(1980) 3 SCC 625", properties={"bench_strength": 5, "majority_ratio": "4:1"}))
    graph.add_node(GraphNode("CASE-SC-CONST-MANEKA-GANDHI-1978", EntityType.CASE, "Maneka Gandhi v. Union of India", "(1978) 1 SCC 248", properties={"bench_strength": 7, "majority_ratio": "7:0"}))
    graph.add_node(GraphNode("CASE-SC-CONST-IR-COELHO-2007", EntityType.CASE, "I.R. Coelho v. State of Tamil Nadu", "(2007) 2 SCC 1", properties={"bench_strength": 9, "majority_ratio": "9:0"}))
    graph.add_node(GraphNode("CASE-SC-CONST-PUTTASWAMY-2017", EntityType.CASE, "Justice K.S. Puttaswamy (Retd.) v. Union of India", "(2017) 10 SCC 1", properties={"bench_strength": 9, "majority_ratio": "9:0"}))
    graph.add_node(GraphNode("CASE-SC-CONST-BOMMAI-1994", EntityType.CASE, "S.R. Bommai v. Union of India", "(1994) 3 SCC 1", properties={"bench_strength": 9, "majority_ratio": "9:0"}))
    graph.add_node(GraphNode("CASE-SC-CONST-DELHI-LAWS-1951", EntityType.CASE, "In re: The Delhi Laws Act, 1912", "AIR 1951 SC 332", properties={"bench_strength": 7, "majority_ratio": "7:0"}))
    graph.add_node(GraphNode("CASE-SC-CONST-CHAMPAKAM-1951", EntityType.CASE, "State of Madras v. Champakam Dorairajan", "AIR 1951 SC 226", properties={"bench_strength": 7, "majority_ratio": "7:0"}))

    # Phase 48 Constitution Bench Interpretation / Invalidation Edges
    graph.add_edge(GraphEdge("E-INT-CONST-KESAV-368", "CASE-SC-CONST-KESAVANANDA-1973", "ART-CONST-368", RelationType.INTERPRETS, properties={"holding": "Basic Structure doctrine limits amending power"}))
    graph.add_edge(GraphEdge("E-INVAL-MINERVA-368", "CASE-SC-CONST-MINERVA-MILLS-1980", "ART-CONST-368", RelationType.INVALIDATES, properties={"holding": "Clauses (4) and (5) of Article 368 struck down as unconstitutional"}))
    graph.add_edge(GraphEdge("E-INT-CONST-MANEKA-21", "CASE-SC-CONST-MANEKA-GANDHI-1978", "ART-CONST-21", RelationType.INTERPRETS, properties={"holding": "Procedure established by law must be just, fair and reasonable"}))
    graph.add_edge(GraphEdge("E-INT-COELHO-31B", "CASE-SC-CONST-IR-COELHO-2007", "ART-CONST-31B", RelationType.INTERPRETS, properties={"holding": "Ninth Schedule laws inserted post 24.04.1973 subject to Basic Structure review"}))
    graph.add_edge(GraphEdge("E-INT-CONST-PUTTA-21", "CASE-SC-CONST-PUTTASWAMY-2017", "ART-CONST-21", RelationType.INTERPRETS, properties={"holding": "Fundamental right to privacy under Article 21"}))
    graph.add_edge(GraphEdge("E-INT-BOMMAI-356", "CASE-SC-CONST-BOMMAI-1994", "ART-CONST-356", RelationType.INTERPRETS, properties={"holding": "Proclamation of President's Rule under Article 356 subject to judicial review"}))
    graph.add_edge(GraphEdge("E-INT-DELHI-245", "CASE-SC-CONST-DELHI-LAWS-1951", "ART-CONST-245", RelationType.INTERPRETS, properties={"holding": "Essential legislative function cannot be delegated to executive"}))
    graph.add_edge(GraphEdge("E-INVAL-CHAMPAKAM-29", "CASE-SC-CONST-CHAMPAKAM-1951", "ART-CONST-29", RelationType.INVALIDATES, properties={"holding": "Communal G.O. violated Article 29(2) and Article 15(1); prompted 1st Constitutional Amendment"}))

    # Delegated Legislation Rule Nodes
    graph.add_node(GraphNode("RULE-COPYRIGHT-2013", EntityType.DELEGATED_RULE, "Copyright Rules, 2013", "G.S.R. 172(E)"))
    graph.add_node(GraphNode("RULE-PATENTS-2003", EntityType.DELEGATED_RULE, "Patents Rules, 2003", "S.O. 493(E)"))
    graph.add_node(GraphNode("RULE-COMPANIES-CSR-2014", EntityType.DELEGATED_RULE, "Companies (Corporate Social Responsibility Policy) Rules, 2014", "G.S.R. 129(E)"))
    graph.add_node(GraphNode("RULE-TRADEMARKS-2017", EntityType.DELEGATED_RULE, "Trade Marks Rules, 2017", "G.S.R. 199(E)"))

    # Enabling / Empowering Sections
    graph.add_node(GraphNode("SEC-COP-78", EntityType.SECTION, "Section 78 Copyright Act 1957", "Copyright Act s.78"))
    graph.add_node(GraphNode("SEC-PAT-159", EntityType.SECTION, "Section 159 Patents Act 1970", "Patents Act s.159"))
    graph.add_node(GraphNode("SEC-CA-135", EntityType.SECTION, "Section 135 Companies Act 2013", "Companies Act s.135"))
    graph.add_node(GraphNode("SEC-CA-469", EntityType.SECTION, "Section 469 Companies Act 2013", "Companies Act s.469"))
    graph.add_node(GraphNode("SEC-TM-157", EntityType.SECTION, "Section 157 Trade Marks Act 1999", "Trade Marks Act s.157"))

    # Empowering Edges
    graph.add_edge(GraphEdge("E-EMP-COP-78-RULES", "SEC-COP-78", "RULE-COPYRIGHT-2013", RelationType.EMPOWERS))
    graph.add_edge(GraphEdge("E-EMP-PAT-159-RULES", "SEC-PAT-159", "RULE-PATENTS-2003", RelationType.EMPOWERS))
    graph.add_edge(GraphEdge("E-EMP-CA-469-CSR", "SEC-CA-469", "RULE-COMPANIES-CSR-2014", RelationType.EMPOWERS))
    graph.add_edge(GraphEdge("E-EMP-TM-157-RULES", "SEC-TM-157", "RULE-TRADEMARKS-2017", RelationType.EMPOWERS))

    # --- PHASE 49 PRECEDENT CONFLICT RESOLUTION & LEGISLATIVE TRACKING NODES ---
    # Phase 49 Case Nodes
    graph.add_node(GraphNode("CASE-HC-BOM-VODAFONE-2010", EntityType.CASE, "Vodafone International Holdings v. UOI (HC)", "2010 SCC OnLine Bom 1391", "IN-MH"))
    graph.add_node(GraphNode("CASE-SC-VODAFONE-2012", EntityType.CASE, "Vodafone International Holdings v. UOI (SC)", "(2012) 6 SCC 613", "IN"))
    graph.add_node(GraphNode("STAT-AMEND-FINANCE-2012", EntityType.STATUTE, "Finance Act 2012 Retrospective Indirect Transfer", "Act 23 of 2012"))
    graph.add_node(GraphNode("CASE-SC-ASGARALI-1957", EntityType.CASE, "State of Bombay v. Asgarali", "(1957) SCR 678"))
    graph.add_node(GraphNode("CASE-SC-RAMESH-VERMA-2017", EntityType.CASE, "Ramesh Verma v. Union of India", "(2017) 4 SCC 321"))
    graph.add_node(GraphNode("CASE-SC-SUBHASH-KASHINATH-2018", EntityType.CASE, "Subhash Kashinath Mahajan v. State of Maharashtra", "(2018) 6 SCC 454"))
    graph.add_node(GraphNode("CASE-SC-REVIEW-UNION-SC-ST-2019", EntityType.CASE, "Union of India v. State of Maharashtra (Review)", "(2020) 4 SCC 761"))
    graph.add_node(GraphNode("ORDER-SC-STAY-MAHAJAN-2018", EntityType.CASE, "Stay Order in Union of India v. Subhash Kashinath", "Order dated 03.04.2018"))
    graph.add_node(GraphNode("CASE-HC-DEL-ST-STEPHENS-2022", EntityType.CASE, "St. Stephen's College v. University of Delhi", "2022 SCC OnLine Del 2866", "IN-DL"))
    graph.add_node(GraphNode("ORDER-SC-STAY-STEPHENS-2022", EntityType.CASE, "Supreme Court Stay Order in St. Stephen's SLP", "SLP(C) No. 17290/2022"))
    graph.add_node(GraphNode("CASE-SC-RAMESH-CHANDRA-REF-2019", EntityType.CASE, "Reference in Ramesh Chandra v. State of U.P.", "Ref Order (2019) 11 SCC 45"))
    graph.add_node(GraphNode("CASE-HC-BOM-ARBITRATION-2021", EntityType.CASE, "ABC Infra v. Union of India", "2021 SCC OnLine Bom 4012", "IN-MH"))
    graph.add_node(GraphNode("CASE-HC-DEL-ARBITRATION-2021", EntityType.CASE, "XYZ Developers v. Union of India", "2021 SCC OnLine Del 3110", "IN-DL"))

    # Phase 49 Relationship Edges
    # 1. Reversal on appeal (Vodafone HC -> SC)
    graph.add_edge(GraphEdge("E-REV-SC-BOM-VODAFONE", "CASE-SC-VODAFONE-2012", "CASE-HC-BOM-VODAFONE-2010", RelationType.REVERSES, properties={"holding": "Look at vs Look through doctrine in offshore share transfers"}))

    # 2. Legislative Supersession (Finance Act 2012 retrospective amendment vs Vodafone SC 2012)
    graph.add_edge(GraphEdge("E-SUP-FIN-VODAFONE", "STAT-AMEND-FINANCE-2012", "CASE-SC-VODAFONE-2012", RelationType.SUPERSEDES_STATUTORY_BASIS, properties={"amendment_reference": "Explanation 4 & 5 to Section 9(1)(i) Income Tax Act inserted retrospectively w.e.f. 01.04.1962", "amendment_date": "2012-05-28"}))

    # 3. Interim Stay (Stay Order -> St. Stephen's judgment)
    graph.add_edge(GraphEdge("E-STAY-STEPHENS", "ORDER-SC-STAY-STEPHENS-2022", "CASE-HC-DEL-ST-STEPHENS-2022", RelationType.STAYED, properties={"scope": "Stay on High Court direction regarding minority quota interview weightage", "is_interim": True}))

    # 4. Referral to Larger Bench without final resolution
    graph.add_edge(GraphEdge("E-REF-RAMESH-CHANDRA", "CASE-SC-RAMESH-CHANDRA-REF-2019", "CASE-SC-RAMESH-VERMA-2017", RelationType.REFERS_TO_LARGER_BENCH, properties={"question_referred": "Correctness of 2-judge bench interpretation of Section 138 NI Act limitation", "bench_sought": "3-Judge Bench", "is_resolved": False}))

    # 5. Inter-High Court Conflict (Bombay HC vs Delhi HC on identical central statute)
    graph.add_edge(GraphEdge("E-CONF-BOM-DEL-ARB", "CASE-HC-BOM-ARBITRATION-2021", "CASE-HC-DEL-ARBITRATION-2021", RelationType.CONFLICTS_WITH, properties={"conflict_issue": "Interpretation of Section 29A Arbitration Act extension power after tribunal mandate expiry", "status": "UNRESOLVED_CONFLICT"}))

    # 6. Distinguishing (Maneka Gandhi distinguishes A.K. Gopalan on personal liberty)
    graph.add_edge(GraphEdge("E-DIST-MANEKA-GOPALAN", "CASE-SC-CONST-MANEKA-GANDHI-1978", "CASE-DK-BASU", RelationType.DISTINGUISHES, properties={"distinguishing_ground": "Narrow spatial view of liberty in Gopalan distinguished and abandoned in favor of substantive due process"}))

    # 7. Recall/Reversal on Review (Review Bench recalls Subhash Kashinath preliminary inquiry direction)
    graph.add_edge(GraphEdge("E-RECALL-MAHAJAN-REVIEW", "CASE-SC-REVIEW-UNION-SC-ST-2019", "CASE-SC-SUBHASH-KASHINATH-2018", RelationType.OVERRULES, properties={"is_partial": True, "scope": "Directions mandating preliminary enquiry and prior sanction for arrest under SC/ST Act recalled", "affected_proposition": "Mandatory preliminary enquiry for SC/ST complaints"}))

    return graph


