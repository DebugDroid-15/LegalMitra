# Phase 59 Initial Defect Register

**Project:** LegalMitra  
**Phase Identifier:** LEGALMITRA-PHASE59  
**Audit Target:** End-to-End Legal Authority Verification, Provenance, and Precedent Resolution  
**Status:** Open / Under Remediation  

---

## Defect Summary Table

| Defect ID | Severity | Category | Component | Description | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-59-01** | High | Evaluator Bias | `independent_evaluator.py` | Lookup failures and unindexed authorities are automatically conflated with `FABRICATED_CITATION`, falsely penalizing legitimate legal answers when evidence is merely unavailable. | **OPEN** |
| **DEF-59-02** | High | Provenance Gap | `answer_assembler.py` / `pipeline.py` | Final generated propositions lack structured end-to-end provenance linking proposition IDs to pinpoint source locators, territorial jurisdiction, and the 12 evidence states. | **OPEN** |
| **DEF-59-03** | Medium | Temporal Semantics | `temporal/engine.py` | Temporal intervals lack unified explicit endpoint documentation (half-open vs closed), causing subtle boundary ambiguity on transition dates (e.g. 1 July 2024 BNSS commencement). | **OPEN** |
| **DEF-59-04** | Medium | Precedent Hierarchy | `caselaw/knowledge_graph.py` | Precedent resolution collapses entire judgments when only a specific proposition or ratio was overruled, rather than tracking proposition-level holding scopes. | **OPEN** |
| **DEF-59-05** | Medium | Citation vs Support | `claim_metrics.py` / `independent_evaluator.py` | Citation existence is occasionally treated as substantive support if keyword tokens match, failing to detect subtle contradiction or omitted provisos. | **OPEN** |

---

## Detailed Initial Defect Descriptions

### DEF-59-01: Conflation of Unavailable/Unindexed Citations with Fabrications
- **Affected File:** `legalmitra/evaluation/independent_evaluator.py`
- **Mechanism:** In `_verify_citation`, if SQLite lookup does not find a match and valid regex patterns do not trigger, `(False, False)` is returned. In `_evaluate_single_proposition`, any `val == False and not quar` is classified as `PropositionVerdict.FABRICATED_CITATION`.
- **Impact:** An authentic citation that is unindexed or from a specialized tribunal order is marked with maximum overstatement penalty and severe trustworthiness collapse, distorting evaluation fidelity.
- **Remediation Plan:** Introduce distinct citation existence states: `FABRICATED_CITATION`, `UNINDEXED_OR_UNAVAILABLE_CITATION`, `MALFORMED_CITATION`, and `AUTHENTIC_VERIFIED_CITATION`.

### DEF-59-02: Missing Proposition-to-Source Provenance Chain
- **Affected File:** `legalmitra/orchestration/answer_assembler.py`, `pipeline.py`
- **Mechanism:** Assembled claims currently record only text and a flat list of citation strings. They do not retain links to the 12 evidence states, pinpoint passage hashes, or territorial jurisdiction.
- **Impact:** End-to-end evidence auditing is difficult because final propositions cannot be traced back through the evidence matrix to primary gazette or judgment text.
- **Remediation Plan:** Build a formal `LegalPropositionProvenance` model capturing all 12 evidence states, pinpoint locators, and statutory intervals.

### DEF-59-03: Temporal Endpoint Ambiguity on Boundary Dates
- **Affected File:** `legalmitra/temporal/engine.py`
- **Mechanism:** Some components treat `effective_until` as inclusive up to 23:59:59 IST, while others check `< effective_until`. This risks misclassifying actions occurring on the exact commencement day of replacement statutes (e.g., 1 July 2024 for BNS/BNSS/BSA).
- **Remediation Plan:** Enforce a canonical temporal interval convention with explicit inclusive boundary handling and automated boundary-date regression tests.

### DEF-59-04: Coarse-Grained Judgment Overruling Collapses Unaffected Ratios
- **Affected File:** `legalmitra/caselaw/knowledge_graph.py`
- **Mechanism:** When a case is marked `is_overruled = True`, queries seeking principles unaffected by the overruling (e.g. *Subhash Kashinath Mahajan* on principles of malicious prosecution) risk being broadly rejected.
- **Remediation Plan:** Implement proposition-level holding scope tracking in precedent evaluation.
