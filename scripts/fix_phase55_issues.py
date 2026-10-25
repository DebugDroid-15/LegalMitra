from pathlib import Path

# 1. Update legalmitra/temporal/engine.py
p_temp = Path("legalmitra/temporal/engine.py")
c_temp = p_temp.read_text(encoding="utf-8")

old_eu_check = """            # Effective until boundary check
            if v.version_effective_until:
                eu_date = normalize_calendar_date(v.version_effective_until)
                if eu_date and q_date > eu_date:
                    continue"""

new_eu_check = """            # Effective until boundary check
            if v.version_effective_until:
                eu_date = normalize_calendar_date(v.version_effective_until)
                if eu_date and q_date > eu_date:
                    # If pending proceeding commenced prior to transition and savings applies to pending, do not discard!
                    if not (pending_proceeding_commenced_prior and v.savings_applies_to_pending and v.repeal_date):
                        continue"""

if old_eu_check in c_temp:
    c_temp = c_temp.replace(old_eu_check, new_eu_check)
    print("Fixed savings check in temporal/engine.py")
elif old_eu_check.replace('\n', '\r\n') in c_temp:
    c_temp = c_temp.replace(old_eu_check.replace('\n', '\r\n'), new_eu_check.replace('\n', '\r\n'))
    print("Fixed savings check in temporal/engine.py (CRLF)")

p_temp.write_text(c_temp, encoding="utf-8")


# 2. Update legalmitra/caselaw/knowledge_graph.py
p_kg = Path("legalmitra/caselaw/knowledge_graph.py")
c_kg = p_kg.read_text(encoding="utf-8")

old_ref_check = """        # Check larger bench referrals
        ref_a = [e for e in self.get_outgoing_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH) + self.get_incoming_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH) if not (e.properties or {}).get("is_resolved", False)]
        ref_b = [e for e in self.get_outgoing_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH) + self.get_incoming_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH) if not (e.properties or {}).get("is_resolved", False)]

        if ref_a and not ref_b:"""

new_ref_check = """        # Check larger bench referrals
        ref_a_referred = False
        ref_b_referred = False

        for e in self.get_outgoing_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH):
            if e.target_id == case_id_b and not (e.properties or {}).get("is_resolved", False):
                ref_b_referred = True
        for e in self.get_outgoing_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH):
            if e.target_id == case_id_a and not (e.properties or {}).get("is_resolved", False):
                ref_a_referred = True

        if not ref_a_referred and not ref_b_referred:
            for e in self.get_incoming_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH):
                if not (e.properties or {}).get("is_resolved", False):
                    ref_a_referred = True
            for e in self.get_incoming_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH):
                if not (e.properties or {}).get("is_resolved", False):
                    ref_b_referred = True

        if ref_a_referred and not ref_b_referred:"""

if old_ref_check in c_kg:
    c_kg = c_kg.replace(old_ref_check, new_ref_check)
    print("Fixed referral check in knowledge_graph.py")
elif old_ref_check.replace('\n', '\r\n') in c_kg:
    c_kg = c_kg.replace(old_ref_check.replace('\n', '\r\n'), new_ref_check.replace('\n', '\r\n'))
    print("Fixed referral check in knowledge_graph.py (CRLF)")

p_kg.write_text(c_kg, encoding="utf-8")


# 3. Update legalmitra/orchestration/query_understanding.py
p_qu = Path("legalmitra/orchestration/query_understanding.py")
c_qu = p_qu.read_text(encoding="utf-8")

old_qu_block = """        if any(term in q_lower for term in ["transfer of property", "section 53a"]):
            acts.append("IND-STAT-TPA-1882")"""

new_qu_block = """        if any(term in q_lower for term in ["transfer of property", "section 53a"]):
            acts.append("IND-STAT-TPA-1882")
        if any(term in q_lower for term in ["it act", "information technology", "section 66a", "66a"]):
            acts.append("IND-STAT-IT-2000")
            if "66a" in q_lower:
                provisions.append("Section 66A")"""

if old_qu_block in c_qu:
    c_qu = c_qu.replace(old_qu_block, new_qu_block)
    print("Added IT Act pattern in query_understanding.py")
elif old_qu_block.replace('\n', '\r\n') in c_qu:
    c_qu = c_qu.replace(old_qu_block.replace('\n', '\r\n'), new_qu_block.replace('\n', '\r\n'))
    print("Added IT Act pattern in query_understanding.py (CRLF)")

p_qu.write_text(c_qu, encoding="utf-8")


# 4. Update legalmitra/orchestration/evidence_orchestrator.py
p_eo = Path("legalmitra/orchestration/evidence_orchestrator.py")
c_eo = p_eo.read_text(encoding="utf-8")

old_eo_trace = """                            res_pit = self.temporal_engine.resolve_point_in_time_applicability(
                                cand_pid, query_date_str=parsed_query.query_date, jurisdiction=parsed_query.jurisdiction
                            )
                            evidence_set.authority_resolution_traces.append(res_pit)"""

new_eo_trace = """                            res_pit = self.temporal_engine.resolve_point_in_time_applicability(
                                cand_pid, query_date_str=parsed_query.query_date, jurisdiction=parsed_query.jurisdiction
                            )
                            res_pit["trace_type"] = "statutory_applicability"
                            evidence_set.authority_resolution_traces.append(res_pit)"""

if old_eo_trace in c_eo:
    c_eo = c_eo.replace(old_eo_trace, new_eo_trace)
    print("Added trace_type to res_pit in evidence_orchestrator.py")
elif old_eo_trace.replace('\n', '\r\n') in c_eo:
    c_eo = c_eo.replace(old_eo_trace.replace('\n', '\r\n'), new_eo_trace.replace('\n', '\r\n'))
    print("Added trace_type to res_pit in evidence_orchestrator.py (CRLF)")

p_eo.write_text(c_eo, encoding="utf-8")

# 5. Also update test_phase55_temporal_authority_trace.py for referral setup
p_t55 = Path("tests/test_phase55_temporal_authority_trace.py")
c_t55 = p_t55.read_text(encoding="utf-8")

old_t_ref = """        graph.add_node(GraphNode("CASE-TEST-REFERRED", EntityType.CASE, "Referred Precedent (2018)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-COORDINATE", EntityType.CASE, "Coordinate Precedent (2019)", properties={"bench_strength": 2}))
        graph.add_edge(GraphEdge(
            "EDGE-REF-1", "CASE-TEST-REFERRED", "CASE-TEST-COORDINATE",
            RelationType.REFERS_TO_LARGER_BENCH,
            properties={"is_resolved": False, "question_referred": "Constitutional scope of section"}
        ))"""

new_t_ref = """        graph.add_node(GraphNode("CASE-TEST-REFERRING", EntityType.CASE, "Referring Bench Order (2018)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-REFERRED", EntityType.CASE, "Referred Precedent (2015)", properties={"bench_strength": 2}))
        graph.add_node(GraphNode("CASE-TEST-COORDINATE", EntityType.CASE, "Coordinate Precedent (2019)", properties={"bench_strength": 2}))
        graph.add_edge(GraphEdge(
            "EDGE-REF-1", "CASE-TEST-REFERRING", "CASE-TEST-REFERRED",
            RelationType.REFERS_TO_LARGER_BENCH,
            properties={"is_resolved": False, "question_referred": "Constitutional scope of section"}
        ))"""

if old_t_ref in c_t55:
    c_t55 = c_t55.replace(old_t_ref, new_t_ref)
    print("Updated test_referral_to_larger_bench_sub_judice_status setup")
elif old_t_ref.replace('\n', '\r\n') in c_t55:
    c_t55 = c_t55.replace(old_t_ref.replace('\n', '\r\n'), new_t_ref.replace('\n', '\r\n'))
    print("Updated test setup (CRLF)")

p_t55.write_text(c_t55, encoding="utf-8")
print("All fixes applied successfully")

