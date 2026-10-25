"""
Fix word boundary and precedence in evidence_matrix.py, query_understanding.py, and answer_assembler.py
"""

from pathlib import Path
import re

# 1. Fix evidence_matrix.py
em_path = Path("legalmitra/orchestration/evidence_matrix.py")
em_content = em_path.read_text(encoding="utf-8")

old_hsa_check = """            # Check if this issue is about Hindu Succession daughter's coparcenary and pre-2004 partition proviso
            elif "hindu succession" in stmt.lower() or "section 6" in stmt.lower() or "coparcen" in stmt.lower():"""

new_hsa_check = """            # Check if this issue is about Hindu Succession daughter's coparcenary and pre-2004 partition proviso
            elif ("hindu succession" in stmt.lower() or "coparcen" in stmt.lower() or "hsa" in stmt.lower()) and (bool(re.search(r"\\bsection\\s*6\\b(?![a-zA-Z0-9])", stmt, re.I)) or "coparcen" in stmt.lower() or "partition" in stmt.lower()):"""

assert old_hsa_check in em_content, "Could not find old_hsa_check in evidence_matrix.py"
em_content = em_content.replace(old_hsa_check, new_hsa_check, 1)
em_path.write_text(em_content, encoding="utf-8")
print("Fixed evidence_matrix.py")

# 2. Fix query_understanding.py compound pattern 4
qu_path = Path("legalmitra/orchestration/query_understanding.py")
qu_content = qu_path.read_text(encoding="utf-8")

old_pattern4 = """        # Compound Pattern 4: Retrenchment under IDA Sec 25F + Uncommenced Labour Code
        elif ("retrenchment" in q_lower or "25f" in q_lower) and any(t in q_lower for t in ["labour code", "code on wages", "industrial relations code"]):"""

new_pattern4 = """        # Compound Pattern 4: Retrenchment under IDA Sec 25F + Uncommenced Labour Code
        elif ("retrenchment" in q_lower or "25f" in q_lower) and any(t in q_lower for t in ["labour code", "code on wages", "industrial relations code"]) and not any(t in q_lower for t in ["definition", "2(s)", "managerial exclusion", "override"]):"""

assert old_pattern4 in qu_content, "Could not find old_pattern4 in query_understanding.py"
qu_content = qu_content.replace(old_pattern4, new_pattern4, 1)
qu_path.write_text(qu_content, encoding="utf-8")
print("Fixed query_understanding.py")

# 3. Fix answer_assembler.py claim synthesis order
aa_path = Path("legalmitra/orchestration/answer_assembler.py")
aa_content = aa_path.read_text(encoding="utf-8")

# In answer_assembler.py, we want primary statutes, constitution benches, delegated rules, judicial precedents first,
# and THEN statutory exceptions & provisos from the matrix.
old_order_chunk = """        # Synthesize claims for statutory exceptions & provisos identified in evidence matrix
        for rec in matrix.records:
            for exc in rec.applicable_exceptions:
                if exc not in competing_authorities:
                    competing_authorities.append(f"Statutory Exception: {exc}")
                exc_claim = AssembledClaim(
                    claim_id=f"CLAIM-{claim_idx}",
                    claim_text=f"Material Exception / Proviso ({rec.issue_id}): {exc}",
                    supporting_evidence_ids=rec.selected_evidence_ids,
                    verbatim_passage=exc[:200],
                    statutory_version=rec.temporal_status,
                    jurisdiction=parsed_query.jurisdiction or "IN",
                    authority_status="STATUTORY_EXCEPTION_PROVISO",
                    validation_verdict="PARTIALLY_SUPPORTED" if rec.issue_disposition.value == "QUALIFIED_ANSWER" else "SUPPORTED",
                    validation_rationale=rec.disposition_rationale or "Material statutory qualification/exception verified.",
                    is_supported=True,
                    requires_qualification=True,
                )
                claims.append(exc_claim)
                claim_idx += 1

        # Synthesize claims from primary statutes"""

new_order_chunk = """        # Synthesize claims from primary statutes"""

assert old_order_chunk in aa_content, "Could not find old_order_chunk in answer_assembler.py"
aa_content = aa_content.replace(old_order_chunk, new_order_chunk, 1)

# Now add statutory exceptions & provisos right after contrary authorities
old_contrary_end = """            claims.append(c)
            claim_idx += 1

        # Handle fabricated citation checks if user explicitly mentioned suspicious cases"""

new_contrary_end = """            claims.append(c)
            claim_idx += 1

        # Synthesize claims for statutory exceptions & provisos identified in evidence matrix (Phase 56)
        for rec in matrix.records:
            for exc in rec.applicable_exceptions:
                if exc not in competing_authorities:
                    competing_authorities.append(f"Statutory Exception: {exc}")
                exc_claim = AssembledClaim(
                    claim_id=f"CLAIM-{claim_idx}",
                    claim_text=f"Material Exception / Proviso ({rec.issue_id}): {exc}",
                    supporting_evidence_ids=rec.selected_evidence_ids,
                    verbatim_passage=exc[:200],
                    statutory_version=rec.temporal_status,
                    jurisdiction=parsed_query.jurisdiction or "IN",
                    authority_status="STATUTORY_EXCEPTION_PROVISO",
                    validation_verdict="PARTIALLY_SUPPORTED" if rec.issue_disposition.value == "QUALIFIED_ANSWER" else "SUPPORTED",
                    validation_rationale=rec.disposition_rationale or "Material statutory qualification/exception verified.",
                    is_supported=True,
                    requires_qualification=True,
                )
                claims.append(exc_claim)
                claim_idx += 1

        # Handle fabricated citation checks if user explicitly mentioned suspicious cases"""

assert old_contrary_end in aa_content, "Could not find old_contrary_end in answer_assembler.py"
aa_content = aa_content.replace(old_contrary_end, new_contrary_end, 1)

aa_path.write_text(aa_content, encoding="utf-8")
print("Fixed answer_assembler.py")
