"""
Test Suite for LegalMitra Phase 48:
- Supreme Court Landmark Constitution Bench Jurisprudence
- Central Delegated Legislation Registry
- Cross-Statute Definition Taxonomy
- Point-in-Time Temporal Benchmark Extension (40 Cases)
"""

import json
from pathlib import Path
import pytest

from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.temporal.engine import (
    TemporalLawEngine,
    build_default_temporal_engine,
)


@pytest.fixture
def knowledge_graph():
    return build_national_judicial_knowledge_graph()


@pytest.fixture
def temporal_engine():
    return build_default_temporal_engine()


# =====================================================================
# 1. CONSTITUTION BENCH JURISPRUDENCE TESTS
# =====================================================================

def test_constitution_bench_manifest_loaded():
    manifest_path = Path("data/22_central_legislation/constitution_bench_manifest.json")
    assert manifest_path.exists(), "constitution_bench_manifest.json must exist"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cases = data.get("cases", [])
    assert len(cases) == 8, f"Expected 8 Constitution Bench cases, got {len(cases)}"
    
    # Verify mandatory case IDs
    case_ids = {c["case_id"] for c in cases}
    expected_ids = {
        "CASE-SC-CONST-KESAVANANDA-1973",
        "CASE-SC-CONST-MINERVA-MILLS-1980",
        "CASE-SC-CONST-MANEKA-GANDHI-1978",
        "CASE-SC-CONST-IR-COELHO-2007",
        "CASE-SC-CONST-PUTTASWAMY-2017",
        "CASE-SC-CONST-SR-BOMMAI-1994",
        "CASE-SC-CONST-DELHI-LAWS-1951",
        "CASE-SC-CONST-CHAMPAKAM-1951",
    }
    assert expected_ids.issubset(case_ids), f"Missing required cases: {expected_ids - case_ids}"


def test_constitution_bench_properties_and_roster():
    manifest_path = Path("data/22_central_legislation/constitution_bench_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for case in data.get("cases", []):
        assert case["bench_strength"] >= 5, f"Constitution Bench must have >= 5 judges: {case['case_id']}"
        assert len(case["bench_roster"]) == case["bench_strength"], f"Roster size mismatch in {case['case_id']}"
        assert len(case["target_constitutional_articles"]) > 0
        assert case["holding_summary"] != ""
        assert "outcome_breakdown" in case


def test_constitution_bench_graph_nodes_and_edges(knowledge_graph):
    # Verify Kesavananda Bharati node and edge
    kesav_node = knowledge_graph.get_node("CASE-SC-CONST-KESAVANANDA-1973")
    assert kesav_node is not None
    assert kesav_node.properties.get("bench_strength") == 13
    assert kesav_node.properties.get("majority_ratio") == "7:6"

    # Verify edge to Article 368
    out_edges = knowledge_graph.get_outgoing_edges("CASE-SC-CONST-KESAVANANDA-1973", RelationType.INTERPRETS)
    assert any(e.target_id == "ART-CONST-368" for e in out_edges)

    # Verify Minerva Mills strikes down Art. 368(4) & (5)
    minerva_edges = knowledge_graph.get_outgoing_edges("CASE-SC-CONST-MINERVA-MILLS-1980", RelationType.INVALIDATES)
    assert any(e.target_id == "ART-CONST-368" for e in minerva_edges)

    # Verify I.R. Coelho Ninth Schedule review
    coelho_edges = knowledge_graph.get_outgoing_edges("CASE-SC-CONST-IR-COELHO-2007", RelationType.INTERPRETS)
    assert any(e.target_id == "ART-CONST-31B" for e in coelho_edges)


def test_temporal_engine_resolve_constitution_bench(temporal_engine):
    # Query for Article 368
    res_368 = temporal_engine.resolve_constitution_bench_precedent("Article 368")
    assert len(res_368) >= 2  # Kesavananda and Minerva Mills
    res_case_ids = {c["case_id"] for c in res_368}
    assert "CASE-SC-CONST-KESAVANANDA-1973" in res_case_ids
    assert "CASE-SC-CONST-MINERVA-MILLS-1980" in res_case_ids

    # Query for Article 21
    res_21 = temporal_engine.resolve_constitution_bench_precedent("Article 21")
    assert len(res_21) >= 2  # Maneka Gandhi and Puttaswamy
    res_21_ids = {c["case_id"] for c in res_21}
    assert "CASE-SC-CONST-MANEKA-GANDHI-1978" in res_21_ids
    assert "CASE-SC-CONST-PUTTASWAMY-2017" in res_21_ids


# =====================================================================
# 2. CENTRAL DELEGATED LEGISLATION REGISTRY TESTS
# =====================================================================

def test_delegated_legislation_manifest_loaded():
    manifest_path = Path("data/22_central_legislation/delegated_legislation_manifest.json")
    assert manifest_path.exists(), "delegated_legislation_manifest.json must exist"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rules = data.get("instruments", [])
    assert len(rules) == 4, f"Expected 4 delegated instruments, got {len(rules)}"
    
    rule_ids = {r["instrument_id"] for r in rules}
    expected_rule_ids = {
        "IND-RULE-COPYRIGHT-2013",
        "IND-RULE-PATENTS-2003",
        "IND-RULE-COMP-CSR-2014",
        "IND-RULE-TRADEMARKS-2017",
    }
    assert expected_rule_ids == rule_ids


def test_delegated_legislation_graph_empowers(knowledge_graph):
    # Check Section 78 empowers Copyright Rules 2013
    cop_edges = knowledge_graph.get_outgoing_edges("SEC-COP-78", RelationType.EMPOWERS)
    assert any(e.target_id == "RULE-COPYRIGHT-2013" for e in cop_edges)

    # Check Section 159 empowers Patents Rules 2003
    pat_edges = knowledge_graph.get_outgoing_edges("SEC-PAT-159", RelationType.EMPOWERS)
    assert any(e.target_id == "RULE-PATENTS-2003" for e in pat_edges)

    # Check Section 469 empowers Companies CSR Rules 2014
    ca_edges = knowledge_graph.get_outgoing_edges("SEC-CA-469", RelationType.EMPOWERS)
    assert any(e.target_id == "RULE-COMPANIES-CSR-2014" for e in ca_edges)


def test_temporal_engine_resolve_delegated_rules(temporal_engine):
    # Query rules for Copyright Act 1957
    cop_rules = temporal_engine.resolve_delegated_rule_for_statute("IND-STAT-COPYRIGHT-1957")
    assert len(cop_rules) == 1
    assert cop_rules[0]["instrument_id"] == "IND-RULE-COPYRIGHT-2013"
    assert cop_rules[0]["replaces_instrument_id"] == "IND-RULE-COPYRIGHT-1958"

    # Query rule with enabling section
    csr_rules = temporal_engine.resolve_delegated_rule_for_statute("IND-STAT-COMP-2013", section="135")
    assert len(csr_rules) == 1
    assert csr_rules[0]["instrument_id"] == "IND-RULE-COMP-CSR-2014"


# =====================================================================
# 3. CROSS-STATUTE DEFINITION TAXONOMY TESTS
# =====================================================================

def test_cross_statute_definitions_manifest_loaded():
    manifest_path = Path("data/22_central_legislation/cross_statute_definitions.json")
    assert manifest_path.exists(), "cross_statute_definitions.json must exist"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    terms = data.get("terms", [])
    assert len(terms) == 8, f"Expected 8 defined terms, got {len(terms)}"
    
    term_keys = {t["term_key"] for t in terms}
    expected_terms = {
        "workman_vs_worker_vs_employee",
        "industry",
        "goods",
        "consumer",
        "invention",
        "electronic_record",
        "appropriate_government",
        "company",
    }
    assert expected_terms == term_keys


def test_semantic_divergence_goods(temporal_engine):
    comp = temporal_engine.compare_cross_statute_definitions("goods")
    assert comp["found"] is True
    defs = comp["definitions"]
    assert "IND-STAT-SOGA-1930" in defs
    assert "IND-STAT-CGST-2017" in defs

    # In SOGA, stocks and shares are INCLUDED, actionable claims are EXCLUDED
    soga_def = defs["IND-STAT-SOGA-1930"]
    assert any("shares" in inc.lower() for inc in soga_def["statutory_inclusions"])
    assert any("actionable claim" in exc.lower() for exc in soga_def["statutory_exclusions"])

    # In CGST, securities (shares) are EXCLUDED, actionable claims are INCLUDED
    cgst_def = defs["IND-STAT-CGST-2017"]
    assert any("securities" in exc.lower() for exc in cgst_def["statutory_exclusions"])
    assert any("actionable claim" in inc.lower() for inc in cgst_def["statutory_inclusions"])


def test_semantic_divergence_workman_vs_employee(temporal_engine):
    comp = temporal_engine.compare_cross_statute_definitions("workman")
    assert comp["found"] is True
    defs = comp["definitions"]
    assert "IND-STAT-IDA-1947" in defs
    assert "IND-STAT-WAGES-2019" in defs

    # IDA definition is in force
    ida_res = temporal_engine.resolve_term_definition("workman", "IND-STAT-IDA-1947")
    assert ida_res["in_force"] is True
    assert any("managerial" in exc.lower() for exc in ida_res["statutory_exclusions"])

    # Code on Wages definition of employee is NOT commenced
    wages_res = temporal_engine.resolve_term_definition("workman", "IND-STAT-WAGES-2019")
    assert wages_res["in_force"] is False
    assert wages_res["operational_status"] == "ENACTED_UNCOMMENCED"


# =====================================================================
# 4. POINT-IN-TIME TEMPORAL BENCHMARK (PIT-V4: 40 CASES)
# =====================================================================

def test_temporal_benchmark_has_40_cases():
    manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cases = data.get("test_cases", [])
    assert len(cases) == 40, f"Expected 40 temporal test cases under PIT-V4, got {len(cases)}"
    assert data.get("benchmark_suite_id") == "LEGALMITRA-BENCHMARK-PIT-V4"


def test_pit_v4_cases_execution(temporal_engine):
    manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validate new Phase 48 cases (PIT-31 to PIT-40)
    phase48_cases = [c for c in data["test_cases"] if int(c["case_id"].replace("PIT-", "")) >= 31]
    assert len(phase48_cases) == 10

    for tc in phase48_cases:
        cid = tc["case_id"]

        if cid == "PIT-31":
            # Kesavananda Bharati / Minerva Mills
            res = temporal_engine.resolve_constitution_bench_precedent("Article 368")
            assert any(c["case_id"] == "CASE-SC-CONST-KESAVANANDA-1973" for c in res)
            assert any(c["bench_strength"] == 13 for c in res)

        elif cid == "PIT-32":
            # I.R. Coelho
            res = temporal_engine.resolve_constitution_bench_precedent("Article 31B")
            assert any(c["case_id"] == "CASE-SC-CONST-IR-COELHO-2007" for c in res)
            coelho = next(c for c in res if c["case_id"] == "CASE-SC-CONST-IR-COELHO-2007")
            assert coelho["bench_strength"] == 9

        elif cid == "PIT-33":
            # Puttaswamy
            res = temporal_engine.resolve_constitution_bench_precedent("Article 21")
            putta = next(c for c in res if c["case_id"] == "CASE-SC-CONST-PUTTASWAMY-2017")
            assert putta["bench_strength"] == 9

        elif cid == "PIT-34":
            # Delhi Laws Act
            res = temporal_engine.resolve_constitution_bench_precedent("Article 245")
            delhi = next(c for c in res if c["case_id"] == "CASE-SC-CONST-DELHI-LAWS-1951")
            assert delhi["bench_strength"] == 7

        elif cid == "PIT-35":
            # Copyright Rules 2013
            res = temporal_engine.resolve_delegated_rule_for_statute("IND-STAT-COPYRIGHT-1957", section="78")
            assert len(res) == 1
            assert res[0]["instrument_id"] == "IND-RULE-COPYRIGHT-2013"

        elif cid == "PIT-36":
            # Companies CSR Rules 2014
            res = temporal_engine.resolve_delegated_rule_for_statute("IND-STAT-COMP-2013", section="135")
            assert len(res) == 1
            assert res[0]["instrument_id"] == "IND-RULE-COMP-CSR-2014"

        elif cid == "PIT-37":
            # Cross-statute "workman"
            res_ida = temporal_engine.resolve_term_definition("workman", "IND-STAT-IDA-1947")
            assert res_ida["in_force"] is True
            assert any("managerial" in exc.lower() for exc in res_ida["statutory_exclusions"])

        elif cid == "PIT-38":
            # Cross-statute "goods"
            res = temporal_engine.compare_cross_statute_definitions("goods")
            assert res["found"] is True
            defs = res["definitions"]
            assert any("shares" in inc.lower() for inc in defs["IND-STAT-SOGA-1930"]["statutory_inclusions"])
            assert any("securities" in exc.lower() for exc in defs["IND-STAT-CGST-2017"]["statutory_exclusions"])

        elif cid == "PIT-39":
            # Uncommenced IR Code
            res_ir = temporal_engine.resolve_term_definition("worker", "IND-STAT-IRCODE-2020")
            assert res_ir["in_force"] is False

        elif cid == "PIT-40":
            # Bommai
            res = temporal_engine.resolve_constitution_bench_precedent("Article 356")
            bommai = next(c for c in res if c["case_id"] == "CASE-SC-CONST-SR-BOMMAI-1994")
            assert bommai["bench_strength"] == 9

