from pathlib import Path

p = Path("legalmitra/orchestration/evidence_orchestrator.py")
content = p.read_text(encoding="utf-8")

# 1. Update precedent status trace appending
old_prec_loop = """        # 4. Precedent Conflict & Status Retrieval from Knowledge Graph
        # Evaluate status of all candidate precedents
        for prec_id in parsed_query.candidate_precedents:
            status = self.knowledge_graph.evaluate_precedent_status(prec_id)"""

new_prec_loop = """        # 4. Precedent Conflict & Status Retrieval from Knowledge Graph
        # Evaluate status of all candidate precedents
        for prec_id in parsed_query.candidate_precedents:
            status = self.knowledge_graph.evaluate_precedent_status(prec_id)
            evidence_set.authority_resolution_traces.append({
                "trace_type": "precedent_status",
                "precedent_id": prec_id,
                "status": status.get("status"),
                "is_good_law": status.get("is_good_law"),
                "is_overruled": status.get("is_overruled"),
                "is_referred": status.get("is_referred"),
                "has_active_stay": status.get("has_active_stay"),
            })"""

if old_prec_loop in content:
    content = content.replace(old_prec_loop, new_prec_loop)
    print("Added precedent status trace appending")
elif old_prec_loop.replace('\n', '\r\n') in content:
    content = content.replace(old_prec_loop.replace('\n', '\r\n'), new_prec_loop.replace('\n', '\r\n'))
    print("Added precedent status trace appending (CRLF)")

# 2. Update conflict tracing: record all valid conflict analyses in traces, and unresolved in unresolved_conflicts
old_conf_res = """                        if conf_res.get("conflict_status") not in ("MISSING_AUTHORITY_EVIDENCE", "RESOLVED_BY_HIERARCHY"):
                            evidence_set.unresolved_conflicts.append(conf_res)
                            evidence_set.authority_resolution_traces.append(conf_res)"""

new_conf_res = """                        if conf_res.get("conflict_status") != "MISSING_AUTHORITY_EVIDENCE":
                            conf_res["trace_type"] = "precedent_conflict"
                            evidence_set.authority_resolution_traces.append(conf_res)
                            if not conf_res.get("is_resolvable", True) or conf_res.get("requires_qualification", False):
                                evidence_set.unresolved_conflicts.append(conf_res)"""

if old_conf_res in content:
    content = content.replace(old_conf_res, new_conf_res)
    print("Updated precedent conflict trace appending")
elif old_conf_res.replace('\n', '\r\n') in content:
    content = content.replace(old_conf_res.replace('\n', '\r\n'), new_conf_res.replace('\n', '\r\n'))
    print("Updated precedent conflict trace appending (CRLF)")

p.write_text(content, encoding="utf-8")
print("Saved patched legalmitra/orchestration/evidence_orchestrator.py")

