# PHASE 56: FACT ANALYSIS AND EPISTEMIC SEPARATION REPORT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  
**Module:** `legalmitra.orchestration.fact_analyzer` & `legalmitra.orchestration.query_understanding`  

---

## 1. Executive Summary

Phase 56 establishes strict epistemic separation between user-supplied assertions, unverified allegations, analytical inferences, source-established statutory facts, and material unknowns. The system enforces an immutable architectural invariant: **user assertions are never silently converted into proven legal facts or external occurrences**.

---

## 2. Epistemic Fact Taxonomy

LegalMitra classifies all factual propositions into four formal categories:
1. `USER_PROVIDED_FACT`: Factual assertions directly stated by the inquirer (e.g., date of contract signing, cheque dishonour date). Epistemic status: *Supplied by user; not independently verified by court record or official gazette*.
2. `USER_ALLEGATION`: Contentious claims, alleged offences, or disputed claims (e.g. accused of fraud, claimed oral agreement). Epistemic status: *Unsubstantiated allegation; cannot be treated as proven fact*.
3. `ANALYTICAL_INFERENCE`: Logical propositions deduced by the system through legal reasoning. Epistemic status: *System deduction; subject to validation against primary rules*.
4. `UNKNOWN_OR_DISPUTED_FACT` / `MATERIAL_UNKNOWN`: Crucial factual parameters omitted by the inquirer that alter the governing substantive rule or jurisdictional forum. Epistemic status: *Unresolved contingency; outcome conditioned upon factual resolution*.

---

## 3. Handling Contradictory & Missing Facts

### 3.1 Contradictory User Facts
When an inquirer supplies mutually incompatible statements in a single prompt (e.g., asserting an agreement was signed in 2022 while simultaneously claiming no agreement existed), the engine:
- Logs both assertions in `FactAnalysisReport.facts` with distinct `fact_id` tags.
- Flags factual inconsistency in `unresolved_factual_dependencies`.
- Formulates conditional analysis explaining the divergent legal outcomes under each factual alternative.

### 3.2 Material Unknowns and Substantive Rule Shifts
The engine explicitly identifies when an unknown fact alters governing law:
- **Partition Execution Date (HSA Sec 6)**: If before 20 Dec 2004, the registered partition is protected by Section 6(1) proviso; if after, the daughter holds an equal coparcenary share.
- **Urgent Interim Relief (Commercial Courts Act Sec 12A)**: If urgent interim relief is contemplated, pre-institution mediation is exempted; if not, mediation is mandatory per *Patil Automation* (2022).
- **Transaction / Offence Date (IPC vs BNS / BNSS)**: Offences committed before 1 July 2024 are governed by IPC 1860; offences on or after 1 July 2024 are governed by BNS 2023.

---

## 4. Verification and Test Results
All fact-epistemic classifications are verified in `tests/test_phase50_query_orchestration.py` and `tests/test_phase56_multi_authority_synthesis.py` (20 passed in 1.77s).
