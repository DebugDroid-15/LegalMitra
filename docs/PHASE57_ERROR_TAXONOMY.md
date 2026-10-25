# Phase 57 Formal 28-Category Legal Error Taxonomy

**Component:** `legalmitra.evaluation.error_attribution`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Complete Taxonomy Across 7 Pipeline Stages

```
+---------------------------------------------------------------------------------------------------+
| Stage 1: QUERY_ANALYSIS                                                                           |
|   1. QUERY_INTERPRETATION_ERROR       : Failure to parse core legal inquiry or intent             |
|   2. DOMAIN_MISCLASSIFICATION         : Misrouting question to incorrect legal branch             |
|   3. TEMPORAL_ANCHOR_MISIDENTIFICATION: Conflating transaction date with query date               |
|   4. ISSUE_DECOMPOSITION_OMISSION     : Failing to extract compound sub-issues                    |
+---------------------------------------------------------------------------------------------------+
| Stage 2: RETRIEVAL                                                                                |
|   5. RETRIEVAL_OMISSION               : Controlling statutory provision/precedent unretrieved     |
|   6. OVERBROAD_RETRIEVAL              : Noise chunks obscuring primary rule                       |
|   7. FABRICATED_SOURCE_HALLUCINATION  : Retrieval of non-existent citation                        |
|   8. QUARANTINED_SOURCE_LEAKAGE       : Leakage of synthetic benchmark scaffold                   |
+---------------------------------------------------------------------------------------------------+
| Stage 3: TEMPORAL_RESOLUTION                                                                      |
|   9. OUTDATED_STATUTE_APPLIED         : Applying repealed law to post-repeal events               |
|  10. PREMATURE_UNCOMMENCED_ENACTMENT  : Applying unnotified statute (e.g. IR Code) as current law|
|  11. OVERRULED_PRECEDENT_APPLIED      : Treating overruled decision as binding                    |
|  12. AMENDED_PROVISO_IGNORED          : Using pre-amendment statutory text                        |
+---------------------------------------------------------------------------------------------------+
| Stage 4: EVIDENCE_MATRIX                                                                          |
|  13. MISSED_STATUTORY_EXCEPTION       : Omitting explicit statutory exception/bar                 |
|  14. MISSED_PROVISO_QUALIFICATION      : Failing to incorporate proviso condition                  |
|  15. SUPPRESSED_LEGISLATIVE_BAR       : Ignoring jurisdictional or procedural bar                 |
|  16. IGNORED_NON_OBSTANTE_CLAUSE      : Overlooking statutory override clause                     |
+---------------------------------------------------------------------------------------------------+
| Stage 5: CLAIM_VALIDATION                                                                         |
|  17. CLAIM_DEPENDENCY_FAILURE         : Propagating conclusion despite failed prerequisite        |
|  18. PREMISE_CONCLUSION_DISCONNECT    : Valid premises leading to non-sequitur conclusion         |
|  19. INTRA_ANSWER_CONTRADICTION       : Mutually exclusive propositions in text                   |
|  20. OVERSTATED_LEGAL_HOLDING         : Absolute claim for qualified legal right                  |
+---------------------------------------------------------------------------------------------------+
| Stage 6: DECISION_POLICY                                                                          |
|  21. FALSE_CERTAINTY_DISPOSITION      : Emitting ANSWER_DIRECT when qualification required        |
|  22. FALSE_ABSTENTION_DISPOSITION     : Emitting ABSTAIN on settled statutory question            |
|  23. CONFLATED_PARTIAL_DISPOSITION    : Collapsing divergent multi-issue into single state        |
|  24. UNCALIBRATED_CONDITIONALITY      : Attaching speculative conditions to direct mandate        |
+---------------------------------------------------------------------------------------------------+
| Stage 7: ANSWER_ASSEMBLY                                                                          |
|  25. CITATION_GROUNDING_MISMATCH      : Citation in metadata ungrounded in text body              |
|  26. MISSING_TRACEABILITY_MATRIX      : Omission of IssueEvidenceMatrix in output                 |
|  27. UNFORMATTED_PRECEDENT_HIERARCHY  : Conflating High Court with Supreme Court Bench            |
|  28. INCOHERENT_SYNTHESIS             : Disjointed synthesis obscuring legal takeaway             |
+---------------------------------------------------------------------------------------------------+
```
