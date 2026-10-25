"""
Fix PIT-71 qualification logic in evidence_matrix.py and answer_assembler.py
"""

from pathlib import Path

# 1. Update evidence_matrix.py for Section 12A
em_path = Path("legalmitra/orchestration/evidence_matrix.py")
em_content = em_path.read_text(encoding="utf-8")

old_12a = """            # Check if this issue is about Commercial Courts Act Section 12A mediation
            elif "12a" in stmt.lower() or "mediation" in stmt.lower():
                cand_rules.append("Commercial Courts Act, 2015 Section 12A")
                exceptions.append("Section 12A(1) exemption where suit contemplates urgent interim relief")
                if "urgent" in q_low or "interim" in q_low:
                    conditional_reasoning = (
                        "Branch A (Urgent interim relief contemplated): Pre-institution mediation under Section 12A is not mandatory.\\n"
                        "Branch B (No urgent interim relief sought): Pre-institution mediation is mandatory per Patil Automation (2022); non-compliance results in rejection of plaint under Order VII Rule 11 CPC."
                    )
                    disposition = IssueDisposition.CONDITIONAL_ANSWER
                    matrix.is_conditional = True
                    rationale = "Supreme Court in Patil Automation (2022) declared Section 12A mandatory, subject to urgent interim relief exception."
                else:
                    disposition = IssueDisposition.DIRECT_ANSWER"""

new_12a = """            # Check if this issue is about Commercial Courts Act Section 12A mediation
            elif "12a" in stmt.lower() or "mediation" in stmt.lower():
                cand_rules.append("Commercial Courts Act, 2015 Section 12A")
                for st in evidence_set.primary_statutes:
                    if "COMMERCIAL" in st.source_id:
                        ev_ids.append(st.item_id)
                if "urgent" in q_low or "interim" in q_low or "except" in q_low:
                    exceptions.append("Section 12A(1) exemption where suit contemplates urgent interim relief")
                    conditional_reasoning = (
                        "Branch A (Urgent interim relief contemplated): Pre-institution mediation under Section 12A is not mandatory.\\n"
                        "Branch B (No urgent interim relief sought): Pre-institution mediation is mandatory per Patil Automation (2022); non-compliance results in rejection of plaint under Order VII Rule 11 CPC."
                    )
                    disposition = IssueDisposition.CONDITIONAL_ANSWER
                    matrix.is_conditional = True
                    rationale = "Supreme Court in Patil Automation (2022) declared Section 12A mandatory, subject to urgent interim relief exception."
                else:
                    disposition = IssueDisposition.DIRECT_ANSWER
                    rationale = "Pre-institution mediation under Section 12A is mandatory as declared by the Supreme Court in Patil Automation (2022)."""

assert old_12a in em_content, "Could not find old_12a"
em_content = em_content.replace(old_12a, new_12a, 1)
em_path.write_text(em_content, encoding="utf-8")
print("Updated evidence_matrix.py")

# 2. Update answer_assembler.py so exception claims only require qualification if disposition is not DIRECT_ANSWER
aa_path = Path("legalmitra/orchestration/answer_assembler.py")
aa_content = aa_path.read_text(encoding="utf-8")

old_exc_claim = """                exc_claim = AssembledClaim(
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
                )"""

new_exc_claim = """                req_qual = rec.issue_disposition.value in ("QUALIFIED_ANSWER", "CONDITIONAL_ANSWER")
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
                    requires_qualification=req_qual,
                )"""

assert old_exc_claim in aa_content, "Could not find old_exc_claim"
aa_content = aa_content.replace(old_exc_claim, new_exc_claim, 1)
aa_path.write_text(aa_content, encoding="utf-8")
print("Updated answer_assembler.py")
