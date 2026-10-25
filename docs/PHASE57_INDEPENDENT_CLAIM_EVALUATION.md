# Phase 57 Independent Claim Evaluation Architecture

**Component:** `legalmitra.evaluation.independent_evaluator`  
**Release:** `LEGALMITRA-RELEASE-PHASE57`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Evaluator Independence Principles

The `IndependentClaimEvaluator` operates post-orchestration without trusting or relying on internal pipeline assertions:
1. **Zero Trust in Internal Status Labels**: Does not assume an answer is valid because `assembled_answer.overall_validation_status == "FULLY_VALIDATED"`.
2. **Separation of Citation Existence from Substantive Support**: Verifies whether cited legal authorities actually stand for the proposition asserted, detecting citations that exist but are substantively contradictory or irrelevant.
3. **Proposition-Level Decomposition**: Extracts individual legal sentences/propositions from answer text, preserving case citations (e.g. `Prakash v. Phulavati`) and statutory abbreviations.
4. **Overstatement Scoring**: Detects absolute or uncalibrated language ("unconditionally", "in all circumstances", "without exception") where rights are subject to statutory qualifications.
5. **Omitted Provisos & Exceptions**: Checks for mandatory statutory provisos (HSA Sec 6(1) proviso, SRA Sec 20A infrastructure bar, Commercial Courts Sec 12A urgency exception).

---

## 2. Proposition Verdict Taxonomy

```
+-------------------------------------------------------------------------+
|                        PropositionVerdict                               |
+-------------------------------------------------------------------------+
| - SUBSTANTIVELY_SUPPORTED         : Exact match with authentic authority|
| - PARTIALLY_SUPPORTED             : Substantive core true, minor lapse  |
| - OVERSTATED_CLAIM                : Absolute claim for qualified right  |
| - CONTRADICTED_BY_SOURCE          : Cited authority refutes claim       |
| - CITATION_EXISTS_BUT_IRRELEVANT  : Citation valid, proposition unbacked|
| - FABRICATED_CITATION             : Non-existent neutral/reporter cite  |
| - QUARANTINED_SOURCE_USED         : Scaffold IND-JUD-DEL-2024-BAIL used |
| - TEMPORALLY_SUPERSEDED           : Overruled precedent cited as binding|
| - OMITTED_MATERIAL_QUALIFICATION  : Essential proviso missing           |
| - PREMISE_DEPENDENCY_FAILED       : Failed intermediate claim           |
| - UNVERIFIABLE                    : Lack of verifiable source record    |
+-------------------------------------------------------------------------+
```

---

## 3. Trustworthiness Scoring Formula

$$\text{Trustworthiness} = w_s \cdot R_{\text{support}} + w_o \cdot (1 - R_{\text{overstatement}}) + w_c \cdot R_{\text{citation\_valid}} + w_{cons} \cdot \mathbb{I}_{\text{consistent}}$$

Where:
- $w_s = 0.45, w_o = 0.25, w_c = 0.15, w_{cons} = 0.15$
- Penalties:
  - Fabricated citation: multiplier $\times 0.2$
  - Quarantined scaffold: multiplier $\times 0.1$
  - Intra-answer contradiction: multiplier $\times 0.5$
