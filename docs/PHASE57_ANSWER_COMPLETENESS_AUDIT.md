# Phase 57 Answer Completeness & Qualification Audit Framework

**Component:** `legalmitra.evaluation.completeness_auditor`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. The 4 Orthogonal Dimensions

The `AnswerCompletenessAuditor` audits legal responses across 4 orthogonal dimensions:

### Dimension 1: Factual and Legal Support (Weight: 30%)
- Verification that citations listed in metadata are meaningfully anchored and integrated into the text body.
- Freedom from ungrounded factual speculation or missing citation backings.

### Dimension 2: Material Completeness (Weight: 30%)
- **Issue Decomposition Coverage**: Verifies that all material sub-issues parsed by the fact analyzer are directly addressed.
- **Mandatory Exception Preservation**: Enforces that statutory bars (e.g. SRA 20A infrastructure bar) and statutory provisos (e.g. HSA 6(1) proviso) are included.

### Dimension 3: Decision Calibration (Weight: 20%)
- Evaluates whether the chosen disposition (`ANSWER_DIRECT`, `ANSWER_QUALIFIED`, `ANSWER_CONDITIONAL`, `ANSWER_PARTIAL`, `ABSTAIN`) is calibrated.
- **False Certainty Penalty**: Penalizes emitting `ANSWER_DIRECT` when exceptions or factual contingencies exist.
- **False Abstention Penalty**: Penalizes emitting `ABSTAIN` on settled positive law.
- **Conflated Multi-Issue Detection**: Flags compound questions with divergent temporal statuses collapsed into a single binary answer.

### Dimension 4: Internal Consistency (Weight: 20%)
- Detection of mutually exclusive propositions between analysis and practical next steps (e.g. stating injunction is barred, but advising client to seek an injunction).
