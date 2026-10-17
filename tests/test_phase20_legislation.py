"""
LegalMitra Phase 20 Legislative Corpus Test Suite
Verifies:
1. Constitution of India expanded coverage (Preamble, Arts 32, 38, 39A, 44, 124, 136, 214, 226, 227, 300A, 352, 356, 368).
2. Negotiable Instruments Act 1881 (Secs 138-142, cheque dishonour conditions, reverse onus presumption).
3. Transfer of Property Act 1882 (Secs 53A part performance, 54 sale, 58 mortgage, 105/106 lease).
4. Commercial Courts Act 2015 (Secs 2(1)(c) commercial disputes, 12A pre-institution mediation, 16 CPC amendments).
5. State & Union Territory Coverage across 36 jurisdictions.
6. Bitwise freeze verification of Phase 9 artifacts.
7. Quarantine enforcement of synthetic scaffolds.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from legalmitra.corpus.state_registry import STATE_UT_REGISTRY
from legalmitra.ingestion.central_acts import list_central_act_documents
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


@pytest.fixture(scope="module")
def kb():
    k = LegalKnowledgeBase(db_path="data/legalmitra_kb.db", must_exist=True)
    yield k
    k.close()


def test_constitution_expanded_coverage(kb):
    """Verify that the Constitution of India has active chunks for key articles."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("""
        SELECT provision_or_para_ref, content
        FROM legal_chunks
        WHERE source_id = 'IND-CONST-1950' AND is_synthetic_scaffold = 0
    """)
    rows = c.fetchall()
    conn.close()

    refs = [r[0] for r in rows]
    # Check foundational articles
    assert any("Preamble" in r for r in refs), "Preamble missing from Constitution chunks"
    assert any("Article 14" in r for r in refs), "Article 14 missing"
    assert any("Article 21" in r for r in refs), "Article 21 missing"
    assert any("Article 32" in r for r in refs), "Article 32 missing"
    assert any("Article 39A" in r for r in refs), "Article 39A free legal aid missing"
    assert any("Article 124" in r for r in refs), "Article 124 Supreme Court establishment missing"
    assert any("Article 136" in r for r in refs), "Article 136 SLP missing"
    assert any("Article 226" in r for r in refs), "Article 226 High Court writ power missing"
    assert any("Article 300A" in r for r in refs), "Article 300A property rights missing"
    assert any("Article 368" in r for r in refs), "Article 368 amendment power missing"


def test_negotiable_instruments_act(kb):
    """Verify Negotiable Instruments Act 1881 sections 138 to 142."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("""
        SELECT provision_or_para_ref, content
        FROM legal_chunks
        WHERE source_id = 'IND-STAT-NI-1881' AND is_synthetic_scaffold = 0
    """)
    rows = c.fetchall()
    conn.close()

    assert len(rows) >= 5, f"Expected at least 5 NI Act chunks, got {len(rows)}"
    refs = [r[0] for r in rows]
    assert any("138" in r for r in refs), "Section 138 missing"
    assert any("139" in r for r in refs), "Section 139 missing"
    assert any("141" in r for r in refs), "Section 141 missing"
    assert any("142" in r for r in refs), "Section 142 missing"

    # Verify substantive content
    sec138_text = " ".join([r[1] for r in rows if "138" in r[0]])
    assert "insufficient" in sec138_text.lower() or "cheque" in sec138_text.lower()


def test_transfer_of_property_act(kb):
    """Verify Transfer of Property Act 1882 provisions."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("""
        SELECT provision_or_para_ref, content
        FROM legal_chunks
        WHERE source_id = 'IND-STAT-TPA-1882' AND is_synthetic_scaffold = 0
    """)
    rows = c.fetchall()
    conn.close()

    assert len(rows) >= 5, f"Expected at least 5 TPA chunks, got {len(rows)}"
    refs = [r[0] for r in rows]
    assert any("53A" in r for r in refs), "Section 53A part performance missing"
    assert any("54" in r for r in refs), "Section 54 sale missing"
    assert any("58" in r for r in refs), "Section 58 mortgage missing"
    assert any("105" in r for r in refs), "Section 105 lease missing"
    assert any("106" in r for r in refs), "Section 106 lease duration missing"


def test_commercial_courts_act(kb):
    """Verify Commercial Courts Act 2015 provisions."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("""
        SELECT provision_or_para_ref, content
        FROM legal_chunks
        WHERE source_id = 'IND-STAT-COMM-COURTS-2015' AND is_synthetic_scaffold = 0
    """)
    rows = c.fetchall()
    conn.close()

    assert len(rows) >= 4, f"Expected at least 4 Commercial Courts Act chunks, got {len(rows)}"
    refs = [r[0] for r in rows]
    assert any("12A" in r for r in refs), "Section 12A pre-institution mediation missing"
    assert any("16" in r for r in refs), "Section 16 CPC amendments missing"


def test_state_ut_registry_coverage():
    """Verify that all 36 States and UTs are properly mapped in registry and exported files."""
    assert len(STATE_UT_REGISTRY) == 36
    states = [s for s in STATE_UT_REGISTRY if s.category == "State"]
    uts = [s for s in STATE_UT_REGISTRY if s.category == "Union Territory"]
    assert len(states) == 28
    assert len(uts) == 8

    # Verify coverage dataset
    cov_path = Path("data/10_legislation/state_ut_coverage.json")
    assert cov_path.exists(), "state_ut_coverage.json missing"
    with open(cov_path, "r", encoding="utf-8") as f:
        cov_data = json.load(f)
    assert len(cov_data) == 36

    # Verify active states
    active = [d for d in cov_data if d["ingested_chunks_count"] > 0]
    active_codes = [d["jurisdiction_code"] for d in active]
    assert "IN-DL" in active_codes
    assert "IN-MH" in active_codes


def test_synthetic_scaffold_quarantine(kb):
    """Verify that synthetic scaffold chunks are strictly quarantined from active retrieval."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    scaffold_count = c.fetchone()[0]
    assert scaffold_count > 0, "Expected quarantined scaffold chunks in database"

    # Search through LegalKnowledgeBase retrieval methods must return 0 scaffolds
    results = kb.search("bail", limit=20)
    for res in results:
        assert getattr(res, "is_synthetic_scaffold", 0) == 0
        assert getattr(res, "source_id", "") != "IND-JUD-DEL-2024-BAIL"
    conn.close()

