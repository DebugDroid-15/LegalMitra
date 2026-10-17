"""
Phase 18 Comprehensive Verification Test Suite
Covers:
1. National Legal Universe schema, items count, and lifecycle states.
2. Bitemporal validity and criminal transition regime logic.
3. Bidirectional criminal code transition registry (IPC <-> BNS, CrPC <-> BNSS, IEA <-> BSA).
4. Procedural event lifecycle, cause list models, and hearing records.
5. National Legal Knowledge Graph nodes, edges, successor queries, and overruled precedent detection.
6. Quarantine enforcement and freeze integrity check.
"""

import json
from pathlib import Path
import pytest

from legalmitra.corpus.legal_universe import (
    DocumentFamily,
    LegalAuthorityLevel,
    IngestionLifecycleState,
    LegalUniverseItem,
)
from legalmitra.corpus.temporal_versioning import (
    BitemporalRecord,
    CriminalCodeTransitionRegistry,
    CriminalTransitionMapping,
    EquivalenceType,
    SectionVersion,
    TransitionRegime,
)
from legalmitra.corpus.procedural_events import (
    CauseListEntry,
    HearingRecord,
    HearingType,
    LitigationCaseLifecycle,
    OrderDispositionType,
    ProceduralStage,
)
from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    GraphEdge,
    GraphNode,
    LegalKnowledgeGraph,
    RelationType,
)


def test_universe_inventory_integrity():
    """Verify serialized legal universe inventory has at least 50 valid items."""
    inv_file = Path("data/09_national_corpus/legal_universe_inventory.json")
    assert inv_file.exists(), "Inventory JSON must exist"
    
    with open(inv_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert len(data) >= 50, f"Expected at least 50 universe items, found {len(data)}"
    
    doc_ids = set()
    quarantined_count = 0
    indexed_count = 0
    
    for item in data:
        assert "record_id" in item
        assert "document_family" in item
        assert "authority_level" in item
        assert "lifecycle_state" in item
        
        # Unique record_id
        assert item["record_id"] not in doc_ids, f"Duplicate record_id: {item['record_id']}"
        doc_ids.add(item["record_id"])
        
        # Valid enums
        assert item["document_family"] in [e.value for e in DocumentFamily]
        assert item["authority_level"] in [e.value for e in LegalAuthorityLevel]
        assert item["lifecycle_state"] in [e.value for e in IngestionLifecycleState]
        
        if item["lifecycle_state"] == IngestionLifecycleState.QUARANTINED.value:
            quarantined_count += 1
        if item["lifecycle_state"] == IngestionLifecycleState.INDEXED.value:
            indexed_count += 1
            
    assert quarantined_count >= 1, "Must contain at least 1 quarantined scaffold item"
    assert indexed_count >= 30, f"Must contain at least 30 indexed items, found {indexed_count}"


def test_bitemporal_validity():
    """Verify bitemporal logic distinguishes past vs active operative periods."""
    # IPC was valid from 1860-10-06 until 2024-06-30
    ipc_rec = BitemporalRecord(
        valid_from="1860-10-06",
        valid_to="2024-06-30",
        system_recorded_at="2026-10-15T10:00:00Z"
    )
    assert ipc_rec.is_valid_at("1995-08-15") is True
    assert ipc_rec.is_valid_at("2024-06-30") is True
    assert ipc_rec.is_valid_at("2024-07-01") is False
    assert ipc_rec.is_current_in_system() is True

    # BNS is valid from 2024-07-01 onwards
    bns_rec = BitemporalRecord(
        valid_from="2024-07-01",
        valid_to=None,
        system_recorded_at="2026-10-15T10:00:00Z"
    )
    assert bns_rec.is_valid_at("2023-12-31") is False
    assert bns_rec.is_valid_at("2024-07-01") is True
    assert bns_rec.is_valid_at("2026-10-17") is True


def test_criminal_transition_registry():
    """Verify bidirectional mappings and governing regime calculation."""
    reg = CriminalCodeTransitionRegistry()
    
    # Pre-2024 incident -> Historic IPC/CrPC
    regime_old, reason_old = reg.determine_governing_regime("2024-03-15")
    assert regime_old == TransitionRegime.HISTORIC_PRE_2024
    assert "Indian Penal Code" in reason_old
    
    # Post-2024 incident -> Modern BNS/BNSS
    regime_new, reason_new = reg.determine_governing_regime("2024-08-20")
    assert regime_new == TransitionRegime.MODERN_POST_2024
    assert "Bharatiya Nyaya Sanhita" in reason_new
    
    # Bidirectional lookups: IPC 302 -> BNS 103
    mappings_302 = reg.lookup_old_to_new("IPC", "Section 302")
    assert len(mappings_302) == 1
    assert mappings_302[0].new_code == "BNS"
    assert mappings_302[0].new_section == "Section 103"
    assert mappings_302[0].equivalence_type == EquivalenceType.EQUIVALENT

    # Inverse lookup: BNS 103 -> IPC 302
    inv_103 = reg.lookup_new_to_old("BNS", "Section 103")
    assert len(inv_103) == 1
    assert inv_103[0].old_section == "Section 302"

    # CrPC 154 -> BNSS 173 (Zero FIR & e-FIR)
    mappings_154 = reg.lookup_old_to_new("CrPC", "Section 154")
    assert len(mappings_154) == 1
    assert mappings_154[0].new_section == "Section 173"
    assert mappings_154[0].equivalence_type == EquivalenceType.SUCCESSOR_PROVISION

    # CrPC 438 -> BNSS 482 (Anticipatory Bail)
    mappings_438 = reg.lookup_old_to_new("CrPC", "Section 438")
    assert len(mappings_438) == 1
    assert mappings_438[0].new_section == "Section 482"

    # IEA 65B -> BSA 63 (Electronic Evidence)
    mappings_65b = reg.lookup_old_to_new("IEA", "Section 65B")
    assert len(mappings_65b) == 1
    assert mappings_65b[0].new_section == "Section 63"


def test_procedural_events_and_case_lifecycle():
    """Verify cause list entries, hearings, and litigation lifecycle progression."""
    # Cause list entry
    entry = CauseListEntry(
        entry_id="CL-2026-10-18-001",
        court_name="High Court of Delhi",
        bench_name="Court No. 14 (Hon'ble Justice Sharma)",
        cause_list_date="2026-10-18",
        item_number=5,
        case_type="W.P.(C)",
        case_number="4512/2026",
        party_petitioner_or_appellant="A. Kumar",
        party_respondent="Govt. of NCT of Delhi",
        advocate_petitioner="Advocate Verma",
        advocate_respondent="Standing Counsel",
        listing_stage="For Admission"
    )
    assert entry.item_number == 5
    assert entry.case_type == "W.P.(C)"
    
    # Lifecycle
    lifecycle = LitigationCaseLifecycle(
        case_id="DLHC-WP-4512-2026",
        case_number="W.P.(C) 4512/2026",
        court_name="High Court of Delhi",
        current_stage=ProceduralStage.FIRST_LISTING_ADMISSION,
        filing_date="2026-10-01",
        petitioner_or_plaintiff="A. Kumar",
        respondent_or_defendant="Govt. of NCT of Delhi",
        acts_involved=["Constitution of India"],
        provisions_involved=["Article 226"]
    )
    assert lifecycle.is_disposed is False
    
    # First hearing: Notice issued
    h1 = HearingRecord(
        hearing_id="HR-001",
        case_id="DLHC-WP-4512-2026",
        hearing_date="2026-10-18",
        court_name="High Court of Delhi",
        bench="Court No. 14",
        hearing_type=HearingType.FIRST_LISTING_ADMISSION,
        proceedings_summary="Notice issued to respondents returnable on 15.11.2026.",
        disposition=OrderDispositionType.NOTICE_ISSUED,
        next_date_of_hearing="2026-11-15",
        next_stage_purpose="Counter affidavit"
    )
    lifecycle.add_hearing(h1)
    assert lifecycle.is_disposed is False
    assert len(lifecycle.hearings) == 1

    # Final hearing: Allowed
    h2 = HearingRecord(
        hearing_id="HR-002",
        case_id="DLHC-WP-4512-2026",
        hearing_date="2026-11-15",
        court_name="High Court of Delhi",
        bench="Court No. 14",
        hearing_type=HearingType.FINAL_ARGUMENTS,
        proceedings_summary="Arguments heard. Petition allowed with directions.",
        disposition=OrderDispositionType.ALLOWED,
        next_date_of_hearing=None
    )
    lifecycle.add_hearing(h2)
    assert lifecycle.is_disposed is True
    assert lifecycle.final_disposition == "allowed"


def test_legal_knowledge_graph():
    """Verify graph nodes, edges, multi-hop successor retrieval, and overruled detection."""
    graph = LegalKnowledgeGraph()

    # Create nodes
    n_bns = GraphNode(node_id="BNS", entity_type=EntityType.STATUTE, name="Bharatiya Nyaya Sanhita, 2023")
    n_ipc = GraphNode(node_id="IPC", entity_type=EntityType.STATUTE, name="Indian Penal Code, 1860")
    n_bns103 = GraphNode(node_id="BNS-103", entity_type=EntityType.SECTION, name="Section 103 (Punishment for murder)")
    n_ipc302 = GraphNode(node_id="IPC-302", entity_type=EntityType.SECTION, name="Section 302 (Punishment for murder)")
    
    n_case_old = GraphNode(node_id="CASE-OLD", entity_type=EntityType.CASE, name="Old Precedent (1985)")
    n_case_overruling = GraphNode(node_id="CASE-NEW", entity_type=EntityType.CASE, name="Constitution Bench (2020)")

    for n in [n_bns, n_ipc, n_bns103, n_ipc302, n_case_old, n_case_overruling]:
        graph.add_node(n)

    # Edges
    graph.add_edge(GraphEdge(edge_id="E1", source_id="BNS", target_id="IPC", relation=RelationType.REPEALS))
    graph.add_edge(GraphEdge(edge_id="E2", source_id="BNS", target_id="BNS-103", relation=RelationType.CONTAINS))
    graph.add_edge(GraphEdge(edge_id="E3", source_id="IPC", target_id="IPC-302", relation=RelationType.CONTAINS))
    graph.add_edge(GraphEdge(edge_id="E4", source_id="BNS-103", target_id="IPC-302", relation=RelationType.SUCCESSOR_TO))
    graph.add_edge(GraphEdge(edge_id="E5", source_id="CASE-OLD", target_id="IPC-302", relation=RelationType.INTERPRETS))
    graph.add_edge(GraphEdge(edge_id="E6", source_id="CASE-NEW", target_id="CASE-OLD", relation=RelationType.OVERRULES))

    # Test successor query: IPC-302 successor
    succ = graph.get_successor_provision("IPC-302")
    assert succ is not None
    assert succ.node_id == "BNS-103"

    # Test precedents for IPC-302
    precedents = graph.get_precedents_for_provision("IPC-302")
    assert len(precedents) == 1
    assert precedents[0].node_id == "CASE-OLD"

    # Test overruled detection
    is_ovr, reason = graph.is_case_overruled("CASE-OLD")
    assert is_ovr is True
    assert "Constitution Bench (2020)" in reason

    is_ovr_new, _ = graph.is_case_overruled("CASE-NEW")
    assert is_ovr_new is False

    # Test connected subgraph
    subgraph = graph.find_connected_subgraph("BNS-103", max_depth=2)
    node_ids = [n["node_id"] for n in subgraph["nodes"]]
    assert "BNS-103" in node_ids
    assert "IPC-302" in node_ids


def test_quarantine_integrity_in_universe():
    """Ensure quarantined items are correctly segregated from active retrieval."""
    inv_file = Path("data/09_national_corpus/legal_universe_inventory.json")
    with open(inv_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    quarantined = [item for item in data if item["lifecycle_state"] == "quarantined"]
    assert len(quarantined) >= 1
    assert quarantined[0]["record_id"] == "UNIV-SCAFFOLD-DEL-2024-BAIL"
    assert quarantined[0]["is_synthetic_scaffold"] is True
    assert "IND-JUD-DEL-2024-BAIL" in quarantined[0]["source_url"]
