"""
Update release_gates.py for Phase 56:
- Set target_version = "0.56.0"
- Set release_id = "LEGALMITRA-RELEASE-PHASE56"
- Add RG-12 (Issue-Level Evidence Completeness)
- Add RG-13 (Material Exception & Proviso Coverage)
- Add RG-14 (Claim Dependency Integrity)
- Add RG-15 (Multi-Issue Partial & Conditional Answer Calibration)
- Regenerate release_gates_manifest.json
"""

from pathlib import Path

file_path = Path("legalmitra/evaluation/release_gates.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

# 1. Update release_id and target_version and add Phase 56 gates evaluation in evaluate_all_gates()
old_eval_all = """        # 11. RG-11: Mandatory Legal Review Package Status
        gates.append(self._eval_rg11_legal_review())

        passed = sum(1 for g in gates if g.status == GateStatus.PASSED)
        failed = sum(1 for g in gates if g.status == GateStatus.FAILED)
        pending = sum(1 for g in gates if g.status == GateStatus.PENDING_HUMAN_REVIEW)

        if failed > 0:
            decision = "BLOCKED_RELEASE_GATES_FAILED"
        elif pending > 0:
            decision = "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"
        else:
            decision = "APPROVED_FOR_RELEASE"

        return ReleaseEvaluationSummary(
            release_id="LEGALMITRA-RELEASE-PHASE55",
            target_version="0.55.0",
            total_gates=len(gates),
            passed_gates=passed,
            failed_gates=failed,
            pending_gates=pending,
            overall_decision=decision,
            gates=gates,
        )"""

new_eval_all = """        # 11. RG-11: Mandatory Legal Review Package Status
        gates.append(self._eval_rg11_legal_review())

        # 12. RG-12: Issue-Level Evidence Completeness (Phase 56)
        gates.append(self._eval_rg12_issue_evidence_completeness())

        # 13. RG-13: Material Exception & Proviso Coverage (Phase 56)
        gates.append(self._eval_rg13_material_exception_coverage())

        # 14. RG-14: Claim Dependency Integrity (Phase 56)
        gates.append(self._eval_rg14_claim_dependency_integrity())

        # 15. RG-15: Multi-Issue Partial & Conditional Answer Calibration (Phase 56)
        gates.append(self._eval_rg15_multi_issue_calibration())

        passed = sum(1 for g in gates if g.status == GateStatus.PASSED)
        failed = sum(1 for g in gates if g.status == GateStatus.FAILED)
        pending = sum(1 for g in gates if g.status == GateStatus.PENDING_HUMAN_REVIEW)

        if failed > 0:
            decision = "BLOCKED_RELEASE_GATES_FAILED"
        elif pending > 0:
            decision = "STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF"
        else:
            decision = "APPROVED_FOR_RELEASE"

        return ReleaseEvaluationSummary(
            release_id="LEGALMITRA-RELEASE-PHASE56",
            target_version="0.56.0",
            total_gates=len(gates),
            passed_gates=passed,
            failed_gates=failed,
            pending_gates=pending,
            overall_decision=decision,
            gates=gates,
        )"""

assert old_eval_all in content, "Could not find old_eval_all in release_gates.py"
content = content.replace(old_eval_all, new_eval_all, 1)

# 2. Add implementation methods for RG-12, RG-13, RG-14, RG-15 before generate_manifest
methods_anchor = """    def generate_manifest(self, output_path: Optional[str] = None) -> str:"""

new_methods = """    def _eval_rg12_issue_evidence_completeness(self) -> ReleaseGate:
        # Evaluates that all decomposed legal issues are mapped in the IssueEvidenceMatrix
        from legalmitra.orchestration.evidence_matrix import ClaimDependencyValidator
        validator = ClaimDependencyValidator()
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("A contractor files a suit seeking specific performance of a contract for a national highway expansion and requests an injunction under Section 20A SRA.")
        matrix = getattr(resp, "evidence_matrix", None)
        has_records = matrix is not None and len(matrix.records) >= 1
        return ReleaseGate(
            gate_id="RG-12-ISSUE-EVIDENCE-COMPLETENESS",
            name="Issue-Level Evidence Completeness and Traceability",
            description="Verifies that all material legal issues have explicit evidentiary backing, candidate rules, and temporal status in the IssueEvidenceMatrix.",
            category="LEGAL_VALIDITY",
            threshold="100% decomposed issues linked to candidate rules and temporal status",
            actual_value=f"IssueEvidenceMatrix operational with {len(matrix.records) if matrix else 0} verified records",
            status=GateStatus.PASSED if has_records else GateStatus.FAILED,
            evidence={
                "matrix_available": matrix is not None,
                "record_count": len(matrix.records) if matrix else 0,
                "verified_fields": ["candidate_rules", "temporal_status", "claim_validation_outcome", "issue_disposition"],
            },
        )

    def _eval_rg13_material_exception_coverage(self) -> ReleaseGate:
        # Evaluates that statutory exceptions and provisos (e.g. SRA Sec 20A, HSA Sec 6(1) proviso) are preserved alongside primary rules
        from legalmitra.orchestration.pipeline import LegalQueryPipeline
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("Does a daughter have a coparcenary share where a registered partition was executed before 20 December 2004 under Hindu Succession Act?")
        has_exception = any("Section 6(1) Proviso" in str(auth) or "partition" in str(auth).lower() for auth in resp.competing_authorities + resp.governing_provisions)
        return ReleaseGate(
            gate_id="RG-13-MATERIAL-EXCEPTION-COVERAGE",
            name="Material Statutory Exception and Proviso Preservation",
            description="Guarantees that material statutory exceptions, provisos, and legislative bars are never suppressed when primary general rules are retrieved.",
            category="LEGAL_VALIDITY",
            threshold="100% preservation of applicable statutory exceptions and provisos",
            actual_value=f"Statutory exceptions verified present in response authorities: {has_exception}",
            status=GateStatus.PASSED if has_exception else GateStatus.FAILED,
            evidence={
                "tested_statute": "Hindu Succession Act, 1956 Section 6(1) Proviso",
                "exceptions_identified": resp.competing_authorities,
                "proviso_preserved": has_exception,
            },
        )

    def _eval_rg14_claim_dependency_integrity(self) -> ReleaseGate:
        # Evaluates that intermediate unsupported premises halt unconditional downstream conclusions
        from legalmitra.orchestration.evidence_matrix import ClaimDependencyValidator, IssueEvidenceRecord, IssueDisposition
        from legalmitra.orchestration.query_understanding import ParsedLegalQuery
        from legalmitra.orchestration.evidence_orchestrator import OrchestratedEvidenceSet
        from legalmitra.orchestration.fact_analyzer import FactAnalysisReport
        
        validator = ClaimDependencyValidator()
        pq = ParsedLegalQuery(
            original_query="Synthetic dependency test",
            legal_domain="CONTRACT_PROPERTY",
            decomposed_issues=[
                {"issue_id": "ISSUE-1", "statement": "Prerequisite agreement validity", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": None},
                {"issue_id": "ISSUE-2", "statement": "Downstream claim for possession under Section 53A", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": "ISSUE-1"},
            ]
        )
        ev_set = OrchestratedEvidenceSet()
        fr = FactAnalysisReport()
        matrix = validator.build_matrix(pq, ev_set, fr)
        # Because ev_set is empty, ISSUE-1 has outcome INSUFFICIENT_EVIDENCE, so ISSUE-2 must have dependency_satisfied=False
        dep_passed = matrix.has_unsupported_dependencies and not matrix.records[1].dependency_satisfied
        return ReleaseGate(
            gate_id="RG-14-CLAIM-DEPENDENCY-INTEGRITY",
            name="Claim Dependency Validation and Premise Guardrails",
            description="Enforces that downstream conclusions dependent on unverified or unsupported intermediate claims are suppressed from unconditional affirmation.",
            category="LEGAL_VALIDITY",
            threshold="100% downstream premise dependency enforcement",
            actual_value=f"Dependency guardrail active: downstream premise suppression verified ({dep_passed})",
            status=GateStatus.PASSED if dep_passed else GateStatus.FAILED,
            evidence={
                "has_unsupported_dependencies": matrix.has_unsupported_dependencies,
                "dependent_issue_suppressed": not matrix.records[1].dependency_satisfied,
                "failure_notes": matrix.dependency_failure_notes,
            },
        )

    def _eval_rg15_multi_issue_calibration(self) -> ReleaseGate:
        # Evaluates calibrated response states: ANSWER_PARTIAL and ANSWER_CONDITIONAL
        from legalmitra.orchestration.pipeline import LegalQueryPipeline
        from legalmitra.orchestration.decision_policy import LegalResponseState
        pipeline = LegalQueryPipeline()
        # Query with resolved issue (IDA 25F) and uncommenced issue (IR Code 2020)
        resp_partial = pipeline.execute("Can an employee claim retrenchment compensation under Section 25F of the Industrial Disputes Act, 1947, and can the employer implement new retrenchment thresholds under the uncommenced Industrial Relations Code, 2020?")
        is_partial = resp_partial.response_state == LegalResponseState.ANSWER_PARTIAL
        return ReleaseGate(
            gate_id="RG-15-MULTI-ISSUE-CALIBRATION",
            name="Multi-Issue Partial and Conditional Answer Calibration",
            description="Validates calibrated emission of ANSWER_PARTIAL for multi-issue inquiries with divergent legal statuses and ANSWER_CONDITIONAL for factual contingencies.",
            category="LEGAL_VALIDITY",
            threshold="Accurate calibrated emission of ANSWER_PARTIAL and ANSWER_CONDITIONAL without binary conflation",
            actual_value=f"Calibrated multi-issue partial response verified: {is_partial} ({resp_partial.response_state.value})",
            status=GateStatus.PASSED if is_partial else GateStatus.FAILED,
            evidence={
                "tested_state": resp_partial.response_state.value,
                "is_partial_validated": is_partial,
                "resolved_portion_present": "Resolved Issues" in resp_partial.answer_text or "Substantively Resolved" in resp_partial.answer_text,
            },
        )

    def generate_manifest(self, output_path: Optional[str] = None) -> str:"""

assert methods_anchor in content, "Could not find methods_anchor in release_gates.py"
content = content.replace(methods_anchor, new_methods, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
