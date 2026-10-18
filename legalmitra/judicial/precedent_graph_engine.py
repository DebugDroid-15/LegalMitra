"""LegalMitra Judicial Knowledge Infrastructure — Typed Precedent Graph Engine.

Implements an evidentiary precedent graph model supporting:
- Bench strength hierarchy and bindingness under Article 141
- Multi-dimensional precedent treatment (Followed, Distinguished, Overruled, Doubted, Explained)
- Passage anchors and ratio decidendi provenance
- Validity and "good law" status determination
- Historical doctrine evolution lineages
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class TreatmentType(str, Enum):
    FOLLOWED = "FOLLOWED"
    DISTINGUISHED = "DISTINGUISHED"
    OVERRULED = "OVERRULED"
    DOUBTED = "DOUBTED"
    EXPLAINED = "EXPLAINED"
    REFERRED_TO = "REFERRED_TO"
    AFFIRMED = "AFFIRMED"
    REVERSED_ON_APPEAL = "REVERSED_ON_APPEAL"


class BenchStrengthCategory(str, Enum):
    SINGLE_BENCH = "SINGLE_BENCH"          # 1 Judge
    DIVISION_BENCH = "DIVISION_BENCH"      # 2 Judges
    FULL_BENCH = "FULL_BENCH"              # 3 Judges
    CONSTITUTION_BENCH = "CONSTITUTION_BENCH"  # 5 Judges
    LARGER_BENCH = "LARGER_BENCH"          # 7 or 9 Judges
    SPECIAL_LARGEST_BENCH = "SPECIAL_LARGEST_BENCH"  # 11 or 13 Judges (e.g. Kesavananda Bharati)


@dataclass
class PrecedentNode:
    case_id: str
    canonical_citation: str
    case_title: str
    court_id: str
    decision_year: int
    bench_judge_count: int
    bench_category: BenchStrengthCategory
    ratio_summary: str
    is_overruled: bool = False
    overruled_by_case_id: Optional[str] = None
    substantive_domains: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "canonical_citation": self.canonical_citation,
            "case_title": self.case_title,
            "court_id": self.court_id,
            "decision_year": self.decision_year,
            "bench_judge_count": self.bench_judge_count,
            "bench_category": self.bench_category.value,
            "ratio_summary": self.ratio_summary,
            "is_overruled": self.is_overruled,
            "overruled_by_case_id": self.overruled_by_case_id,
            "substantive_domains": self.substantive_domains,
        }


@dataclass
class PrecedentEdge:
    citing_case_id: str
    cited_case_id: str
    treatment: TreatmentType
    passage_anchor: str
    treatment_context: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "citing_case_id": self.citing_case_id,
            "cited_case_id": self.cited_case_id,
            "treatment": self.treatment.value,
            "passage_anchor": self.passage_anchor,
            "treatment_context": self.treatment_context,
        }


class PrecedentGraphEngine:
    """Manages the graph of judgments and citation treatments."""

    def __init__(self) -> None:
        self._nodes: Dict[str, PrecedentNode] = {}
        self._outgoing_edges: Dict[str, List[PrecedentEdge]] = {}  # citing -> list of edges
        self._incoming_edges: Dict[str, List[PrecedentEdge]] = {}  # cited -> list of edges

    def add_node(self, node: PrecedentNode) -> None:
        self._nodes[node.case_id] = node
        if node.case_id not in self._outgoing_edges:
            self._outgoing_edges[node.case_id] = []
        if node.case_id not in self._incoming_edges:
            self._incoming_edges[node.case_id] = []

    def add_edge(self, edge: PrecedentEdge) -> None:
        # Validate that both cases exist in graph
        if edge.citing_case_id not in self._nodes or edge.cited_case_id not in self._nodes:
            raise ValueError(f"Cannot add edge between {edge.citing_case_id} and {edge.cited_case_id}: missing nodes")

        citing_node = self._nodes[edge.citing_case_id]
        cited_node = self._nodes[edge.cited_case_id]

        # In Indian jurisprudence under Art. 141, a smaller or co-equal bench cannot overrule a larger bench
        if edge.treatment == TreatmentType.OVERRULED:
            if citing_node.bench_judge_count < cited_node.bench_judge_count:
                raise ValueError(
                    f"Jurisprudential Invariant Violation: Citing bench ({citing_node.bench_judge_count} judges) "
                    f"cannot overrule larger bench ({cited_node.bench_judge_count} judges)."
                )
            cited_node.is_overruled = True
            cited_node.overruled_by_case_id = citing_node.case_id

        self._outgoing_edges[edge.citing_case_id].append(edge)
        self._incoming_edges[edge.cited_case_id].append(edge)

    def get_node(self, case_id: str) -> Optional[PrecedentNode]:
        return self._nodes.get(case_id)

    def is_good_law(self, case_id: str) -> Tuple[bool, Optional[str]]:
        """Determine if case is good law or has been overruled."""
        node = self.get_node(case_id)
        if not node:
            return False, "Case not found in graph"
        if node.is_overruled:
            overruling_node = self.get_node(node.overruled_by_case_id or "")
            ref_info = overruling_node.canonical_citation if overruling_node else node.overruled_by_case_id
            return False, f"Overruled by {ref_info}"
        return True, "Good law (no overruling detected)"

    def get_citation_history(self, case_id: str) -> List[PrecedentEdge]:
        """Return all cases that cite this case."""
        return self._incoming_edges.get(case_id, [])

    def get_cases_cited_by(self, case_id: str) -> List[PrecedentEdge]:
        """Return all cases cited by this case."""
        return self._outgoing_edges.get(case_id, [])

    def trace_lineage(self, start_case_id: str) -> List[Dict[str, Any]]:
        """Trace how subsequent cases treated this precedent."""
        lineage = []
        for edge in self.get_citation_history(start_case_id):
            citing_node = self.get_node(edge.citing_case_id)
            if citing_node:
                lineage.append({
                    "citing_case": citing_node.case_title,
                    "citation": citing_node.canonical_citation,
                    "year": citing_node.decision_year,
                    "treatment": edge.treatment.value,
                    "context": edge.treatment_context,
                    "passage": edge.passage_anchor,
                })
        return sorted(lineage, key=lambda x: x["year"])

    def to_dict(self) -> Dict[str, Any]:
        all_edges = []
        for edges in self._outgoing_edges.values():
            for e in edges:
                all_edges.append(e.to_dict())

        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(all_edges),
            "nodes": {cid: n.to_dict() for cid, n in self._nodes.items()},
            "edges": all_edges,
        }
