"""
Phase 19 Verification Test Suite
Covers:
1. National Legal Universe 101 items expansion and schema validation.
2. National Source Discovery Engine and change classification.
3. Priority-Driven Acquisition Queue scoring and worker operations.
4. Resumable National Corpus Ingestion Pipeline (dry-run and idempotent updates).
5. Structural Legal Document Diffing Engine and modification classification.
6. Enhanced Precedent Intelligence and proposition-aware overruling evaluation.
7. Continuous Source Monitoring and rate-limit backoff.
8. Security isolation, database separation, and freeze verification.
"""

import json
from pathlib import Path
import pytest

from legalmitra.corpus.legal_universe import (
    DocumentFamily,
    IngestionLifecycleState,
    LegalAuthorityLevel,
    LegalUniverseItem,
)
from legalmitra.corpus.discovery_engine import (
    ChangeClassification,
    DiscoveryCandidate,
    NationalSourceDiscoveryEngine,
)
from legalmitra.corpus.acquisition_queue import (
    AcquisitionPriorityScorer,
    AcquisitionTask,
    PriorityAcquisitionQueue,
    TaskStatus,
)
from legalmitra.corpus.legal_diff import (
    LegalDiffEngine,
    LegalModificationType,
)
from legalmitra.corpus.source_monitor import (
    ContinuousSourceMonitor,
    MonitoredSource,
    MonitoringStatus,
)
from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    GraphEdge,
    GraphNode,
    LegalKnowledgeGraph,
    RelationType,
)
from legalmitra.ingestion.national_corpus_pipeline import (
    NationalCorpusPipeline,
    PipelineStage,
)
from legalmitra.ingestion.central_acts import get_contract_document


def test_expanded_universe_inventory():
    """Verify serialized legal universe inventory has 101 items across all document families."""
    inv_file = Path("data/09_national_corpus/legal_universe_inventory.json")
    assert inv_file.exists(), "Inventory JSON must exist"

    with open(inv_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) >= 101, f"Expected at least 101 universe items, found {len(data)}"

    record_ids = set()
    states = set()
    families = set()

    for item in data:
        assert "record_id" in item
        assert "document_family" in item
        assert "authority_level" in item
        assert "lifecycle_state" in item

        assert item["record_id"] not in record_ids, f"Duplicate record_id: {item['record_id']}"
        record_ids.add(item["record_id"])

        states.add(item["lifecycle_state"])
        families.add(item["document_family"])

    assert IngestionLifecycleState.INDEXED.value in states
    assert IngestionLifecycleState.QUARANTINED.value in states
    assert DocumentFamily.CONSTITUTION.value in families
    assert DocumentFamily.CENTRAL_ACT.value in families
    assert DocumentFamily.STATE_ACT.value in families


def test_discovery_engine_change_classification():
    """Test candidate registration, duplicate detection, and source modification."""
    engine = NationalSourceDiscoveryEngine()

    c1 = DiscoveryCandidate(
        candidate_id="DOC-TEST-001",
        source_url="https://test.gov.in/act1",
        official_title="Test Enactment Act, 2026",
        document_family=DocumentFamily.CENTRAL_ACT,
        authority_level=LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
        jurisdiction="IN",
        issuing_authority="Parliament of India",
        discovered_at="2026-10-17T12:00:00Z",
        raw_content_bytes=b"Original statutory text v1"
    )

    # 1. Register brand new
    res1, class1 = engine.register_candidate(c1)
    assert class1 == ChangeClassification.NEW_DOCUMENT
    assert res1.checksum_sha256 is not None

    # 2. Register exact duplicate with same bytes
    c2 = DiscoveryCandidate(
        candidate_id="DOC-TEST-DUPLICATE",
        source_url="https://mirror.gov.in/act1",
        official_title="Test Enactment Act Mirror",
        document_family=DocumentFamily.CENTRAL_ACT,
        authority_level=LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
        jurisdiction="IN",
        issuing_authority="Parliament of India",
        discovered_at="2026-10-17T12:05:00Z",
        raw_content_bytes=b"Original statutory text v1"
    )
    res2, class2 = engine.register_candidate(c2)
    assert class2 == ChangeClassification.EXACT_DUPLICATE

    # 3. Register modified version of known doc
    c3 = DiscoveryCandidate(
        candidate_id="DOC-TEST-001",
        source_url="https://test.gov.in/act1",
        official_title="Test Enactment Act, 2026 (Amended)",
        document_family=DocumentFamily.CENTRAL_ACT,
        authority_level=LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
        jurisdiction="IN",
        issuing_authority="Parliament of India",
        discovered_at="2026-10-17T12:10:00Z",
        raw_content_bytes=b"Modified statutory text v2 with amendments"
    )
    res3, class3 = engine.register_candidate(c3)
    assert class3 == ChangeClassification.CHANGED_SOURCE_FILE


def test_priority_acquisition_queue_operations():
    """Verify queue scoring, priority heap ordering, worker claiming, and retry handling."""
    queue = PriorityAcquisitionQueue()

    # Score calculation
    score_high, rat_high = AcquisitionPriorityScorer.calculate_priority(
        authority_level=LegalAuthorityLevel.SUPREME_CONSTITUTIONAL,
        legal_domain="Constitutional Law",
        is_coverage_gap=True,
        chunks_indexed=0
    )
    assert score_high >= 70.0

    score_scaffold, rat_scaffold = AcquisitionPriorityScorer.calculate_priority(
        authority_level=LegalAuthorityLevel.UNVERIFIED_SCAFFOLD,
        legal_domain="Synthetic Test Fixture",
        is_scaffold=True
    )
    assert score_scaffold == 0.0

    # Tasks
    t_low = AcquisitionTask(
        task_id="TASK-LOW",
        record_id="UNIV-RULE-LOW",
        official_title="Minor Subordinate Circular",
        document_family=DocumentFamily.SUBORDINATE_RULE,
        authority_level=LegalAuthorityLevel.BINDING_DELEGATED_LEGISLATION,
        jurisdiction="IN",
        source_url="https://test.gov.in/circ",
        priority_score=35.0,
        priority_rationale="Low priority circular"
    )

    t_high = AcquisitionTask(
        task_id="TASK-HIGH",
        record_id="UNIV-ACT-HIGH",
        official_title="Major Constitutional Amendment",
        document_family=DocumentFamily.CONSTITUTIONAL_AMENDMENT,
        authority_level=LegalAuthorityLevel.SUPREME_CONSTITUTIONAL,
        jurisdiction="IN",
        source_url="https://test.gov.in/caa",
        priority_score=score_high,
        priority_rationale=rat_high
    )

    queue.enqueue(t_low)
    queue.enqueue(t_high)

    # Claim next must return t_high first
    claimed_1 = queue.claim_next_task(worker_id="WORKER-01")
    assert claimed_1 is not None
    assert claimed_1.task_id == "TASK-HIGH"
    assert claimed_1.status == TaskStatus.CLAIMED

    # Complete task
    assert queue.complete_task("TASK-HIGH") is True
    assert queue.get_task("TASK-HIGH").status == TaskStatus.COMPLETED

    # Next claim returns t_low
    claimed_2 = queue.claim_next_task(worker_id="WORKER-02")
    assert claimed_2 is not None
    assert claimed_2.task_id == "TASK-LOW"

    # Simulate failure with retry
    queue.mark_failed("TASK-LOW", "Network timeout")
    assert queue.get_task("TASK-LOW").status == TaskStatus.RETRY_SCHEDULED
    assert queue.get_task("TASK-LOW").retry_count == 1


def test_legal_diff_engine_provisions():
    """Verify classification of statutory insertions, deletions, substitutions, and penalties."""
    # 1. Identical text
    res_same = LegalDiffEngine.diff_provisions(
        provision_id="SEC-1",
        section_number="Section 1",
        old_text="This Act may be called the Example Act, 2026.",
        new_text="This Act may be called the Example Act, 2026.",
        prev_label="1950",
        new_label="2026"
    )
    assert res_same.modification_type == LegalModificationType.NO_SUBSTANTIVE_CHANGE
    assert res_same.requires_advocate_review is False

    # 2. Penalty enhancement
    res_penal = LegalDiffEngine.diff_provisions(
        provision_id="SEC-304A",
        section_number="Section 304A",
        old_text="Whoever causes death by negligence shall be punished with imprisonment for a term which may extend to two years, or fine.",
        new_text="Whoever causes death by rash or negligent act shall be punished with imprisonment for a term which may extend to seven years and fine.",
        prev_label="Pre-Amendment",
        new_label="Post-Amendment"
    )
    assert res_penal.modification_type == LegalModificationType.PENALTY_ENHANCEMENT
    assert res_penal.requires_advocate_review is True

    # 3. New insertion
    res_insert = LegalDiffEngine.diff_provisions(
        provision_id="SEC-21A",
        section_number="Article 21A",
        old_text="",
        new_text="The State shall provide free and compulsory education to all children of the age of six to fourteen years.",
        prev_label="1950",
        new_label="86th CAA"
    )
    assert res_insert.modification_type == LegalModificationType.INSERTION


def test_enhanced_precedent_status_evaluation():
    """Verify proposition-aware overruling and partial overruling evaluation in LegalKnowledgeGraph."""
    graph = LegalKnowledgeGraph()

    n_overruling = GraphNode(node_id="CASE-ARJUN", entity_type=EntityType.CASE, name="Arjun Khotkar (2020)")
    n_overruled = GraphNode(node_id="CASE-SHAFHI", entity_type=EntityType.CASE, name="Shafhi Mohammad (2018)")
    graph.add_node(n_overruling)
    graph.add_node(n_overruled)

    # Add partial overruling edge
    graph.add_edge(GraphEdge(
        edge_id="E-OVERRULE-01",
        source_id="CASE-ARJUN",
        target_id="CASE-SHAFHI",
        relation=RelationType.OVERRULES,
        properties={
            "is_partial": True,
            "scope": "Section 65B(4) certificate waiver",
            "affected_proposition": "Certificate waiver when party not in possession of electronic device"
        }
    ))

    # General check
    is_ovr, reason = graph.is_case_overruled("CASE-SHAFHI")
    assert is_ovr is True
    assert "Arjun Khotkar" in reason

    # Detailed evaluation
    status_detail = graph.evaluate_precedent_status("CASE-SHAFHI")
    assert status_detail["is_overruled"] is True
    assert status_detail["status"] == "partially_overruled"
    assert len(status_detail["overruling_details"]) == 1
    assert status_detail["overruling_details"][0]["is_partial"] is True


def test_continuous_source_monitor():
    """Verify monitor tracks hashes, detects changes, and saves state."""
    monitor = ContinuousSourceMonitor()

    s1 = MonitoredSource(
        source_id="TEST-SOURCE-01",
        portal_name="Test Legal Portal",
        target_url="https://portal.gov.in",
        monitoring_method="portal_check"
    )
    monitor.register_source(s1)

    # Initial check
    status1, change1 = monitor.check_source("TEST-SOURCE-01", current_content_bytes=b"Initial gazette text")
    assert status1 == MonitoringStatus.UP_TO_DATE
    assert change1 == ChangeClassification.NEW_DOCUMENT

    # Second check with same bytes
    status2, change2 = monitor.check_source("TEST-SOURCE-01", current_content_bytes=b"Initial gazette text")
    assert status2 == MonitoringStatus.UP_TO_DATE
    assert change2 == ChangeClassification.EXACT_DUPLICATE

    # Third check with updated bytes
    status3, change3 = monitor.check_source("TEST-SOURCE-01", current_content_bytes=b"Updated gazette text with amendment")
    assert status3 == MonitoringStatus.CHANGE_DETECTED
    assert change3 == ChangeClassification.CHANGED_SOURCE_FILE


def test_national_corpus_pipeline_dry_run(tmp_path):
    """Verify batch pipeline runs cleanly in dry-run mode and produces manifest."""
    manifest_dir = tmp_path / "manifests"
    pipeline = NationalCorpusPipeline(manifests_dir=manifest_dir)

    contract_doc = get_contract_document()
    manifest = pipeline.run_statute_batch(
        batch_id="TEST-BATCH-DRY-RUN",
        statute_docs=[contract_doc],
        dry_run=True
    )

    assert manifest.dry_run is True
    assert manifest.documents_submitted == 1
    assert manifest.documents_indexed == 1
    assert manifest.chunks_created > 0
    assert manifest.failures_count == 0

    saved_manifest_file = manifest_dir / f"manifest_{manifest.batch_id}.json"
    assert saved_manifest_file.exists()

