from pathlib import Path

p = Path("legalmitra/caselaw/knowledge_graph.py")
content = p.read_text(encoding="utf-8")

old_func_sig = """    def resolve_precedent_conflict(
        self,
        case_id_a: str,
        case_id_b: str,
        target_jurisdiction: str = "IN",
        statutory_provision_id: Optional[str] = None,
    ) -> Dict[str, Any]:"""

new_func_sig = """    def resolve_precedent_conflict(
        self,
        case_id_a: str,
        case_id_b: str,
        target_jurisdiction: str = "IN",
        statutory_provision_id: Optional[str] = None,
        substantive_issue: Optional[str] = None,
    ) -> Dict[str, Any]:"""

if old_func_sig in content:
    content = content.replace(old_func_sig, new_func_sig)
    print("Replaced resolve_precedent_conflict signature")

# Insert referral, distinguishing, obiter, and issue checks right after overruling check
old_after_overruling = """        # Extract court and bench details
        props_a = node_a.properties or {}
        props_b = node_b.properties or {}"""

new_after_overruling = """        # Check substantive issue alignment
        props_a = node_a.properties or {}
        props_b = node_b.properties or {}

        if substantive_issue:
            issues_a = [str(i).lower() for i in props_a.get("legal_issues", [])] + [node_a.name.lower()]
            issues_b = [str(i).lower() for i in props_b.get("legal_issues", [])] + [node_b.name.lower()]
            s_clean = substantive_issue.lower()
            match_a = any(s_clean in iss or iss in s_clean for iss in issues_a)
            match_b = any(s_clean in iss or iss in s_clean for iss in issues_b)
            if not match_a or not match_b:
                return {
                    "conflict_status": "DIFFERENT_LEGAL_ISSUES_NO_CONFLICT",
                    "is_resolvable": False,
                    "binding_authority": None,
                    "rationale": f"Authorities '{node_a.name}' and '{node_b.name}' concern materially distinct legal issues; no true doctrinal conflict exists on '{substantive_issue}'.",
                    "competing_positions": [{"case_id": case_id_a}, {"case_id": case_id_b}],
                    "requires_qualification": True,
                    "abstain_recommended": False,
                }

        # Check larger bench referrals
        ref_a = [e for e in self.get_outgoing_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH) + self.get_incoming_edges(case_id_a, RelationType.REFERS_TO_LARGER_BENCH) if not (e.properties or {}).get("is_resolved", False)]
        ref_b = [e for e in self.get_outgoing_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH) + self.get_incoming_edges(case_id_b, RelationType.REFERS_TO_LARGER_BENCH) if not (e.properties or {}).get("is_resolved", False)]

        if ref_a and not ref_b:
            return {
                "conflict_status": "REFERRED_SUB_JUDICE",
                "is_resolvable": False,
                "binding_authority": None,
                "referred_authority": case_id_a,
                "coordinate_authority": case_id_b,
                "rationale": f"Correctness of '{node_a.name}' has been referred to a larger bench and remains sub-judice. The decision cannot be treated as formally overruled, but requires qualified application.",
                "competing_positions": [{"case_id": case_id_a, "status": "REFERRED_SUB_JUDICE"}, {"case_id": case_id_b, "status": "COORDINATE_ACTIVE"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }
        elif ref_b and not ref_a:
            return {
                "conflict_status": "REFERRED_SUB_JUDICE",
                "is_resolvable": False,
                "binding_authority": None,
                "referred_authority": case_id_b,
                "coordinate_authority": case_id_a,
                "rationale": f"Correctness of '{node_b.name}' has been referred to a larger bench and remains sub-judice. The decision cannot be treated as formally overruled, but requires qualified application.",
                "competing_positions": [{"case_id": case_id_b, "status": "REFERRED_SUB_JUDICE"}, {"case_id": case_id_a, "status": "COORDINATE_ACTIVE"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }

        # Check distinguishing treatment
        dist_a_b = [e for e in self.get_outgoing_edges(case_id_a, RelationType.DISTINGUISHES) if e.target_id == case_id_b]
        dist_b_a = [e for e in self.get_outgoing_edges(case_id_b, RelationType.DISTINGUISHES) if e.target_id == case_id_a]

        if dist_a_b:
            ground = (dist_a_b[0].properties or {}).get("distinguishing_ground", "Factual/statutory divergence")
            return {
                "conflict_status": "DISTINGUISHED_NOT_OVERRULED",
                "is_resolvable": True,
                "binding_authority": case_id_a,
                "distinguished_authority": case_id_b,
                "rationale": f"'{node_a.name}' distinguished '{node_b.name}' on grounds of {ground}. Both authorities remain valid within their distinct factual/statutory matrices.",
                "competing_positions": [{"case_id": case_id_a, "status": "DISTINGUISHING_RULING"}, {"case_id": case_id_b, "status": "DISTINGUISHED_RULING"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }
        elif dist_b_a:
            ground = (dist_b_a[0].properties or {}).get("distinguishing_ground", "Factual/statutory divergence")
            return {
                "conflict_status": "DISTINGUISHED_NOT_OVERRULED",
                "is_resolvable": True,
                "binding_authority": case_id_b,
                "distinguished_authority": case_id_a,
                "rationale": f"'{node_b.name}' distinguished '{node_a.name}' on grounds of {ground}. Both authorities remain valid within their distinct factual/statutory matrices.",
                "competing_positions": [{"case_id": case_id_b, "status": "DISTINGUISHING_RULING"}, {"case_id": case_id_a, "status": "DISTINGUISHED_RULING"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }

        # Check ratio decidendi vs obiter dicta
        is_obiter_a = props_a.get("is_obiter", False)
        is_obiter_b = props_b.get("is_obiter", False)

        if is_obiter_a and not is_obiter_b:
            return {
                "conflict_status": "PERSUASIVE_OBITER_NOT_BINDING_RATIO",
                "is_resolvable": True,
                "binding_authority": case_id_b,
                "persuasive_authority": case_id_a,
                "rationale": f"Observation in '{node_a.name}' was obiter dicta, which cannot displace the binding ratio decidendi in '{node_b.name}'.",
                "competing_positions": [{"case_id": case_id_b, "status": "BINDING_RATIO"}, {"case_id": case_id_a, "status": "PERSUASIVE_OBITER"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }
        elif is_obiter_b and not is_obiter_a:
            return {
                "conflict_status": "PERSUASIVE_OBITER_NOT_BINDING_RATIO",
                "is_resolvable": True,
                "binding_authority": case_id_a,
                "persuasive_authority": case_id_b,
                "rationale": f"Observation in '{node_b.name}' was obiter dicta, which cannot displace the binding ratio decidendi in '{node_a.name}'.",
                "competing_positions": [{"case_id": case_id_a, "status": "BINDING_RATIO"}, {"case_id": case_id_b, "status": "PERSUASIVE_OBITER"}],
                "requires_qualification": True,
                "abstain_recommended": False,
            }

        # Extract court and bench details
        props_a = node_a.properties or {}
        props_b = node_b.properties or {}"""

if old_after_overruling in content:
    content = content.replace(old_after_overruling, new_after_overruling)
    print("Inserted precedent calibrations")
elif old_after_overruling.replace('\n', '\r\n') in content:
    content = content.replace(old_after_overruling.replace('\n', '\r\n'), new_after_overruling.replace('\n', '\r\n'))
    print("Inserted precedent calibrations (CRLF)")

p.write_text(content, encoding="utf-8")
print("Saved patched legalmitra/caselaw/knowledge_graph.py")

