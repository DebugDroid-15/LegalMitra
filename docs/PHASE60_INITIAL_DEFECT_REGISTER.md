# LEGALMITRA PHASE 60 — INITIAL DEFECT REGISTER

**Project:** LegalMitra  
**Phase Identifier:** `LEGALMITRA-PHASE60`  
**Classification:** Engineering Defect Audit & Adversarial Preflight  
**Audit Date:** 2026-10-25  

---

## Initial Defect Inventory

| Defect ID | Severity | Subsystem | Description & Root-Cause Analysis | Target Remediation Plan |
|:---|:---:|:---|:---|:---|
| **DEF-60-01** | HIGH | Pipeline Orchestration | **Omission of Post-Generation Safety Guard**: `LegalQueryPipeline.execute()` constructs and returns `OrchestratedLegalResponse` without executing `IndependentClaimEvaluator` or `AnswerCompletenessAuditor` on the final assembled text. Final internal contradictions or fabricated citations are not caught at runtime. | Wire `IndependentClaimEvaluator` into post-generation pipeline verification; downgrade to `CLARIFICATION_REQUIRED` or `ABSTAIN` if critical safety violations or internal contradictions are detected. |
| **DEF-60-02** | HIGH | Provenance Integrity | **Unverified Runtime Provenance Lifecycle**: `AnswerAssembler` instantiates `LegalPropositionProvenance` objects, but does not run `PropositionProvenanceAuditor.audit_answer_propositions()`. Broken prerequisite states (e.g. `CLAIM_GROUNDED` without valid `TEMPORAL_BOUNDED` or `ACQUISITION_VERIFIED`) pass silently into the return object. | Wire `PropositionProvenanceAuditor` into `Pipeline.execute()` and `AnswerAssembler`; block propositions failing state transitions or cryptographic integrity. |
| **DEF-60-03** | MEDIUM | Precedent Retrieval | **Coarse Precedent Filtering in Evidence Orchestrator**: `UnifiedEvidenceOrchestrator` filters judicial authorities based on case-level overruled status, but does not evaluate `target_proposition` scope. In cases with multiple holdings (e.g. *Subhash Kashinath Mahajan*), valid surviving propositions risk suppression or overruled propositions risk retrieval. | Integrate proposition-sensitive precedent filtering into `UnifiedEvidenceOrchestrator.orchestrate_evidence()`. |
| **DEF-60-04** | HIGH | Decision Policy | **Compound Multi-Issue Conflation Failure**: When a multi-issue query has mixed evidence quality (e.g. Issue 1 supported by active statute, Issue 2 blocked by uncommenced statute, Issue 3 affected by precedent conflict), `LegalDecisionPolicy` evaluates issues sequentially and can prematurely collapse the entire response into either total abstention or an over-generalized single response. | Enhance `LegalDecisionPolicy` to evaluate per-issue verdicts using `IssueEvidenceMatrix`, generating calibrated multi-part answers that state positive holdings for supported issues while explicitly cordoning off unresolved issues. |
| **DEF-60-05** | MEDIUM | Cryptographic Audit | **Lack of Canonical Hash Re-verification**: Audit hashes in `LegalPropositionProvenance` are computed at creation time, but no runtime check verifies that modifying source text or metadata invalidates the hash. | Add tamper detection and cryptographic canonicalization tests in the integration test harness. |
