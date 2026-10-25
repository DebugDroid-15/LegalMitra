# PHASE 56: RULE DEPENDENCY MODEL REPORT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  
**Module:** `legalmitra.orchestration.evidence_matrix`  

---

## 1. Executive Summary

The Rule Dependency Model formalizes the structural relationships between statutory rules, procedural conditions precedent, and exceptions. Downstream legal entitlements are modeled as conditional functions of prerequisite rules.

---

## 2. Dependency Typology

```text
+-----------------------+-----------------------------+----------------------------------------------+
| Dependency Type       | Structural Relationship     | Example                                      |
+-----------------------+-----------------------------+----------------------------------------------+
| PROCEDURAL_PREREQUISITE| Rule B valid ONLY if Rule A | Section 142 NI Act complaint valid ONLY if   |
|                       | procedural notice served    | Section 138 15-day notice issued on time     |
+-----------------------+-----------------------------+----------------------------------------------+
| STATUTORY_EXCEPTION   | Rule B defeats or limits    | Section 20A SRA bars injunctions if project  |
|                       | general right under Rule A  | is specified in Infrastructure Schedule      |
+-----------------------+-----------------------------+----------------------------------------------+
| SAVINGS_PROVISO       | Proviso B carves out prior  | Section 6(1) proviso HSA preserves pre-2004  |
|                       | transactions from Rule A    | partitions from daughter's coparcenary claim |
+-----------------------+-----------------------------+----------------------------------------------+
| SUBORDINATE_ENABLING  | Rule B valid ONLY within    | CSR Rules 2014 valid ONLY within enabling    |
|                       | scope of Parent Act Sec A   | authority of Section 135 Companies Act 2013 |
+-----------------------+-----------------------------+----------------------------------------------+
| NON_OBSTANTE_OVERRIDE | Rule A overrides Rule B via | Section 238 IBC overrides state electricity  |
|                       | statutory non-obstante clause| regulation charges per Paschimanchal Vidyut  |
+-----------------------+-----------------------------+----------------------------------------------+
```

---

## 3. Verification
Dependency graph evaluation is implemented in `ClaimDependencyValidator.build_matrix()` and verified in `tests/test_phase56_multi_authority_synthesis.py`.
