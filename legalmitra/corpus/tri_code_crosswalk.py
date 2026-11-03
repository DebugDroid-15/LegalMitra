"""
Phase 87: Extended Tri-Code Crosswalk & Temporal Knowledge Graph
Provides comprehensive bidirectional provision mapping (IPC <-> BNS, CrPC <-> BNSS, IEA <-> BSA),
incident date-based savings clause routing (BNSS Sec 531, BNS Sec 358, BSA Sec 170),
and links statutory sections to binding Supreme Court precedents.
"""

from __future__ import annotations

import datetime
import json
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("tri_code_crosswalk")


class CodeType(str, Enum):
    IPC = "IPC"
    CRPC = "CRPC"
    IEA = "IEA"
    BNS = "BNS"
    BNSS = "BNSS"
    BSA = "BSA"


class EquivalenceType(str, Enum):
    EQUIVALENT = "equivalent"                          # Direct 1:1 substantive correspondence
    SUCCESSOR_PROVISION = "successor_provision"        # Re-enacted with structural modification
    PARTIAL_OVERLAP = "partial_overlap"                # Subsumed partially or split across multiple sections
    REQUIRES_LEGAL_REVIEW = "requires_legal_review"    # Significant change in punishment, elements, or procedure


class TransitionRegime(str, Enum):
    HISTORIC_PRE_2024 = "historic_pre_2024"            # Governed by IPC 1860 / CrPC 1973 / IEA 1872
    MODERN_POST_2024 = "modern_post_2024"              # Governed by BNS 2023 / BNSS 2023 / BSA 2023


@dataclass
class TriCodeEntry:
    mapping_id: str
    old_code: str
    old_section: str
    old_title: str
    new_code: str
    new_section: str
    new_title: str
    equivalence_type: EquivalenceType
    statutory_changes: str
    savings_ref: str
    landmark_judgments: List[str] = field(default_factory=list)


@dataclass
class TemporalRoutingDecision:
    incident_date: str
    regime: TransitionRegime
    substantive_code: str
    procedural_code: str
    evidence_code: str
    savings_clause_citation: str
    legal_explanation: str


class ExtendedTriCodeKnowledgeGraph:
    """
    High-capacity knowledge graph and crosswalk engine for criminal code transition.
    """

    TRANSITION_CUTOFF_DATE = "2024-07-01"

    def __init__(self, matrix_path: Optional[Path] = None):
        self.matrix_path = matrix_path or Path("data/crosswalk/tri_code_matrix.json")
        self._entries: Dict[str, TriCodeEntry] = {}
        self._old_index: Dict[Tuple[str, str], List[TriCodeEntry]] = {}
        self._new_index: Dict[Tuple[str, str], List[TriCodeEntry]] = {}
        self._precedent_graph: Dict[str, Set[str]] = {}  # Section (e.g. "BNS 316") -> Set[Judgment names]
        self._load_matrix()

    def _normalize_sec(self, sec: str) -> str:
        s = sec.strip().upper()
        s = s.replace("SECTION", "").replace("SEC.", "").replace("SEC", "").strip()
        # strip subclause parentheses if needed for broad search, but keep exact as primary
        return s

    def _load_matrix(self) -> None:
        if not self.matrix_path.exists():
            logger.warning(f"Matrix file not found at {self.matrix_path}")
            return

        data = json.loads(self.matrix_path.read_text(encoding="utf-8"))
        for item in data:
            entry = TriCodeEntry(
                mapping_id=item["mapping_id"],
                old_code=item["old_code"].upper(),
                old_section=item["old_section"],
                old_title=item["old_title"],
                new_code=item["new_code"].upper(),
                new_section=item["new_section"],
                new_title=item["new_title"],
                equivalence_type=EquivalenceType(item.get("equivalence_type", "equivalent")),
                statutory_changes=item.get("statutory_changes", ""),
                savings_ref=item.get("savings_ref", ""),
                landmark_judgments=item.get("landmark_judgments", [])
            )
            self._entries[entry.mapping_id] = entry

            old_k = (entry.old_code, self._normalize_sec(entry.old_section))
            self._old_index.setdefault(old_k, []).append(entry)

            new_k = (entry.new_code, self._normalize_sec(entry.new_section))
            self._new_index.setdefault(new_k, []).append(entry)

            # Build precedent graph
            old_node = f"{entry.old_code} {entry.old_section}"
            new_node = f"{entry.new_code} {entry.new_section}"
            self._precedent_graph.setdefault(old_node, set()).update(entry.landmark_judgments)
            self._precedent_graph.setdefault(new_node, set()).update(entry.landmark_judgments)

        logger.info(f"Loaded {len(self._entries)} crosswalk entries into TriCode Knowledge Graph.")

    def lookup_old_provision(self, code: str, section: str) -> List[TriCodeEntry]:
        """Lookup modern provision from historical code (e.g. IPC 420 -> BNS 318(4))."""
        k = (code.upper().strip(), self._normalize_sec(section))
        return self._old_index.get(k, [])

    def lookup_new_provision(self, code: str, section: str) -> List[TriCodeEntry]:
        """Lookup historical provision from modern code (e.g. BNS 316 -> IPC 405)."""
        k = (code.upper().strip(), self._normalize_sec(section))
        return self._new_index.get(k, [])

    def get_precedents_for_provision(self, code: str, section: str) -> List[str]:
        """Returns binding Supreme Court precedents associated with this provision across both eras."""
        # 1. Direct query
        node = f"{code.upper().strip()} {section.strip()}"
        precedents = set(self._precedent_graph.get(node, []))

        # 2. Crosswalk search if not directly found
        if not precedents:
            # try finding via crosswalk
            matches = self.lookup_old_provision(code, section) or self.lookup_new_provision(code, section)
            for m in matches:
                precedents.update(m.landmark_judgments)

        return sorted(list(precedents))

    def route_by_incident_date(self, incident_date_str: str) -> TemporalRoutingDecision:
        """
        Applies Article 20(1) Constitution & BNSS Sec 531 savings rules to dictate governing codes.
        """
        try:
            inc_date = datetime.date.fromisoformat(incident_date_str)
            cutoff = datetime.date.fromisoformat(self.TRANSITION_CUTOFF_DATE)
        except Exception:
            # Default to modern if unparseable
            inc_date = datetime.date(2025, 1, 1)
            cutoff = datetime.date(2024, 7, 1)

        if inc_date < cutoff:
            return TemporalRoutingDecision(
                incident_date=incident_date_str,
                regime=TransitionRegime.HISTORIC_PRE_2024,
                substantive_code="Indian Penal Code, 1860 (IPC)",
                procedural_code="Code of Criminal Procedure, 1973 (CrPC)",
                evidence_code="Indian Evidence Act, 1872 (IEA)",
                savings_clause_citation="Section 531(2)(a) BNSS & Section 358(1) BNS",
                legal_explanation=(
                    f"Under Article 20(1) of the Constitution (protection against ex post facto laws), "
                    f"an offence committed on {incident_date_str} (prior to 1 July 2024) must be charged "
                    f"substantively under the Indian Penal Code, 1860. Inquiries and trials commenced thereunder "
                    f"continue under the Code of Criminal Procedure, 1973 per Section 531(2)(a) BNSS savings."
                )
            )
        else:
            return TemporalRoutingDecision(
                incident_date=incident_date_str,
                regime=TransitionRegime.MODERN_POST_2024,
                substantive_code="Bharatiya Nyaya Sanhita, 2023 (BNS)",
                procedural_code="Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
                evidence_code="Bharatiya Sakshya Adhiniyam, 2023 (BSA)",
                savings_clause_citation="Ministry of Home Affairs Notification S.O. 848(E)",
                legal_explanation=(
                    f"The incident occurred on {incident_date_str} (on or after 1 July 2024). "
                    f"Substantive criminal liability is governed strictly by the Bharatiya Nyaya Sanhita, 2023 (BNS); "
                    f"police investigation and court proceedings follow the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS); "
                    f"and evidence admissibility follows the Bharatiya Sakshya Adhiniyam, 2023 (BSA)."
                )
            )
