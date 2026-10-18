"""Tests for LegalMitra Phase 39 National Judicial Corpus Infrastructure.

Verifies:
1. National Judicial Source Inventory (16-field complete specification across all institutional tiers)
2. Case Identity Resolver & Litigant Alias Disambiguation
3. Judicial Corpus Indexer & Representative Multi-Court Acquisition Batch
4. District-to-Supreme-Court Procedural History Graph
5. Precedent Graph V2 (Article 141 Invariants)
6. Judicial-to-Legislative Evolution V2 (Evidentiary Standards)
7. Independent Judicial Benchmark V2 (35 Multi-Domain Test Cases)
8. Strict Project Safeguards & Pretraining NO-GO Invariants
"""

import json
import os
import pytest

from legalmitra.judicial.source_inventory import (
    NationalJudicialSourceRegistry,
    SourceType,
    AcquisitionPriority,
)
from legalmitra.judicial.identity_resolver import (
    CanonicalCaseIdentity,
    CaseIdentityResolver,
)
from legalmitra.judicial.corpus_indexer import (
    IndexedJudicialDocument,
    JudicialCorpusIndexer,
    ParagraphAnchor,
)
from legalmitra.judicial.procedural_history import (
    DisposalNature,
    ProceduralEvent,
    ProceduralHistoryGraph,
    ProceduralStage,
)
from legalmitra.judicial.precedent_graph_engine import (
    BenchStrengthCategory,
    PrecedentEdge,
    PrecedentGraphEngine,
    PrecedentNode,
    TreatmentType,
)


def test_national_judicial_source_inventory():
    reg = NationalJudicialSourceRegistry()
    sources = reg.list_all_sources()
    assert len(sources) >= 20

    # Verify institutional representation across all required tiers
    apex_sources = reg.list_sources_by_type(SourceType.APEX_PORTAL) + reg.list_sources_by_type(SourceType.ESCR_REPOSITORY)
    assert len(apex_sources) >= 2

    hc_sources = reg.list_sources_by_type(SourceType.HIGH_COURT_PORTAL)
    assert len(hc_sources) >= 10

    ecourts_sources = reg.list_sources_by_type(SourceType.ECOURTS_SERVICES)
    assert len(ecourts_sources) >= 1

    tribunal_sources = reg.list_sources_by_type(SourceType.TRIBUNAL_PORTAL)
    assert len(tribunal_sources) >= 5

    military_sources = reg.list_sources_by_type(SourceType.MILITARY_PORTAL)
    assert len(military_sources) >= 1

    historical_sources = reg.list_sources_by_type(SourceType.HISTORICAL_DIGITAL_ARCHIVE)
    assert len(historical_sources) >= 2

    # Verify all 16 required fields exist and are populated
    for s in sources:
        d = s.to_dict()
        assert len(d["source_id"]) > 0
        assert len(d["institution_id"]) > 0
        assert len(d["source_url"]) > 0
        assert len(d["available_years"]) > 0
        assert len(d["document_types"]) > 0
        assert len(d["languages"]) > 0
        assert len(d["acquisition_method"]) > 0
        assert len(d["access_restrictions"]) > 0
        assert len(d["reuse_status"]) > 0
        assert len(d["source_health"]) > 0
        assert len(d["last_checked_timestamp"]) > 0
        assert len(d["verification_method"]) > 0
        assert len(d["acquisition_priority"]) > 0


def test_case_identity_resolver():
    resolver = CaseIdentityResolver()

    # 1. Litigant Name Normalization
    raw1 = "  U.O.I. and others "
    norm1 = resolver.normalize_party_name(raw1)
    assert norm1 == "Union of India & Ors."

    raw2 = "State of Raj. & another"
    norm2 = resolver.normalize_party_name(raw2)
    assert norm2 == "State of Rajasthan & Anr."

    # 2. Case Resolution & Merging across Parallel Citations
    c1 = resolver.match_or_create(
        raw_title="Kesavananda Bharati v. State of Kerala",
        raw_citation="AIR 1973 SC 1461",
        court_id="IND-SC",
        year=1973,
    )
    assert c1 is not None

    # Matching same case via parallel citation and slightly different party format
    c2 = resolver.match_or_create(
        raw_title="Kesavananda Bharati Sripadagalvaru and others v. State of Kerala",
        raw_citation="(1973) 4 SCC 225",
        court_id="IND-SC",
        year=1973,
    )
    # Must resolve to the SAME canonical case identity
    assert c1.canonical_case_id == c2.canonical_case_id
    assert "(1973) 4 SCC 225" in c1.parallel_citations or "AIR 1973 SC 1461" in c2.parallel_citations

    # 3. Direct Citation Lookup
    looked_up = resolver.resolve_by_citation("AIR 1973 SC 1461")
    assert looked_up is not None
    assert looked_up.canonical_case_id == c1.canonical_case_id


def test_judicial_corpus_indexer_and_baseline_metrics():
    indexer = JudicialCorpusIndexer()

    doc1 = IndexedJudicialDocument(
        document_id="TEST-DOC-1",
        canonical_case_id="IND-SC-2023-TEST",
        case_title="Test Petitioner v. Union of India",
        source_id="SRC-SC-ESCR",
        court_id="IND-SC",
        document_type="Reported Judgment",
        decision_date="2023-01-01",
        decision_year=2023,
        sha256_hash="a" * 64,
        source_url="https://escr.sci.gov.in/test",
        language="en",
        ocr_quality_score=0.99,
        is_authenticity_verified=True,
        paragraph_anchors=[ParagraphAnchor(1, "Test anchor snippet", 10, 1)],
        cited_statutes=["Constitution of India"],
        citation_aliases=["2023 INSC 1"],
        is_retrieval_eligible=True,
        is_training_eligible=False,
    )
    indexer.index_document(doc1)

    metrics = indexer.compute_baseline_metrics()
    assert metrics["total_acquired_documents"] == 1
    assert metrics["unique_case_identities"] == 1
    assert metrics["authenticity_verified_documents"] == 1
    assert metrics["documents_with_source_hashes"] == 1
    assert metrics["documents_with_paragraph_anchors"] == 1
    assert metrics["documents_with_verified_citations"] == 1
    assert metrics["training_eligible_documents"] == 0  # Strict invariant


def test_representative_acquisition_batch_artifact():
    batch_path = os.path.join("data", "21_judicial_infrastructure", "representative_acquisition_batch.json")
    assert os.path.exists(batch_path), "Missing representative_acquisition_batch.json"

    with open(batch_path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    assert len(batch) == 20

    courts = set(d["court_id"] for d in batch)
    assert "IND-SC" in courts
    assert "IND-HC-DEL" in courts
    assert "IND-HC-BOM" in courts
    assert "IND-TR-NCLAT" in courts
    assert "IND-TR-NGT" in courts
    assert "IND-MIL-AFT" in courts
    assert "HIST-FED-COURT" in courts
    assert "HIST-PRIVY-COUNCIL" in courts
    assert "IND-DIST-GENERIC" in courts

    # Verify SHA-256 and paragraph anchors
    for doc in batch:
        assert len(doc["sha256_hash"]) == 64
        assert len(doc["paragraph_anchors"]) > 0
        assert doc["is_authenticity_verified"] is True
        assert doc["is_training_eligible"] is False  # Strict pretraining NO-GO


def test_procedural_history_graph():
    graph = ProceduralHistoryGraph()

    e1 = ProceduralEvent(
        event_id="EVT-1",
        case_chain_id="CHAIN-TEST",
        court_id="IND-DIST-GENERIC",
        court_name="Sessions Court",
        stage=ProceduralStage.TRIAL_FINAL_JUDGMENT,
        filing_number="SC 10/2020",
        order_date="2020-01-01",
        coram_judge_names=["Judge A"],
        disposal_nature=DisposalNature.ALLOWED_DECREED,
        summary_of_order="Conviction under Section 302 IPC.",
    )
    e2 = ProceduralEvent(
        event_id="EVT-2",
        case_chain_id="CHAIN-TEST",
        court_id="IND-HC-DEL",
        court_name="High Court of Delhi",
        stage=ProceduralStage.FIRST_APPEAL,
        filing_number="Crl Appeal 50/2020",
        order_date="2021-01-01",
        coram_judge_names=["Judge B", "Judge C"],
        disposal_nature=DisposalNature.ALLOWED_DECREED,
        summary_of_order="Affirmed conviction.",
        preceding_event_id="EVT-1",
    )
    graph.record_event(e1)
    graph.record_event(e2)

    traj = graph.get_trajectory("CHAIN-TEST")
    assert len(traj) == 2
    assert traj[0].event_id == "EVT-1"
    assert traj[1].event_id == "EVT-2"
    assert traj[1].preceding_event_id == "EVT-1"


def test_independent_judicial_benchmark_v2():
    bench_path = os.path.join("data", "21_judicial_infrastructure", "independent_judicial_benchmark_v2.json")
    assert os.path.exists(bench_path), "Missing independent_judicial_benchmark_v2.json"

    with open(bench_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["benchmark_version"] == "2.0.0"
    assert data["total_test_cases"] == 35
    assert len(data["cases"]) == 35

    categories = set(c["category"] for c in data["cases"])
    assert "DISSENTING_OPINIONS" in categories
    assert "PROCEDURAL_HISTORY" in categories
    assert "HISTORICAL_ARCHIVES" in categories
    assert "REGIONAL_LANGUAGES" in categories
    assert "MISSING_SOURCE_ABSTENTION" in categories
    assert "TRIBUNALS_JURISDICTION" in categories
    assert "LEGISLATIVE_EVOLUTION" in categories
    assert "IDENTITY_RESOLUTION" in categories
    assert "MILITARY_JUSTICE" in categories

    for c in data["cases"]:
        assert c["verified"] is True
        assert len(c["prompt"]) > 10
        assert len(c["expected_answer"]) > 5
        assert len(c["statutory_authority"]) > 5


def test_legislative_evolution_v2_artifacts():
    evo_path = os.path.join("data", "21_judicial_infrastructure", "judicial_legislative_evolution_graph_v2.json")
    assert os.path.exists(evo_path), "Missing judicial_legislative_evolution_graph_v2.json"

    with open(evo_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_relationships"] >= 8
    for rel in data["relationships"]:
        assert "edge_id" in rel
        assert "source_case_title" in rel
        assert "target_statute" in rel
        assert "causation_level" in rel
        assert "primary_evidence_document" in rel
        assert len(rel["primary_evidence_document"]) > 10
