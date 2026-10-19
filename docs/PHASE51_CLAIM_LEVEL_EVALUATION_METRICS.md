# PHASE 51: CLAIM-LEVEL MATHEMATICAL EVALUATION & 15 FORMAL METRICS

**Project:** LegalMitra  
**Module:** `legalmitra.evaluation.claim_metrics.ClaimLevelMetricsCalculator`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Formal Formulation Framework

In accordance with Phase 51 specifications, every evaluation metric must be mathematically rigorous, preserving auditability by recording:
1. Formal mathematical formula (Numerator and Denominator)
2. Eligibility rule (which claims or cases enter the calculation)
3. Calculation method
4. Sample size
5. Known limitations of the measurement

---

## 2. Inventory of 15 Mandated Formal Metrics

### Metric 1: Citation Validity
- **Formula:** $\frac{\text{Valid Official Citations}}{\text{Total Emitted Citations}}$
- **Eligibility:** All citations extracted from emitted responses.
- **Result:** $98.2\%$ ($N = 57$).
- **Limitations:** Automated regex and source registry resolution; does not verify physical gazette page volume.

### Metric 2: Citation-to-Claim Support
- **Formula:** $\frac{\text{Supported Cited Claims}}{\text{Total Cited Claims}}$
- **Eligibility:** Claims having at least one supporting evidence item cited.
- **Result:** $93.8\%$ ($N = 80$).
- **Limitations:** Evaluated via deterministic textual entailment and claim validator; advocate review pending.

### Metric 3: Material Claim Support
- **Formula:** $\frac{\text{Supported Material Claims}}{\text{Total Material Claims}}$
- **Eligibility:** All synthesized legal proposition claims in answers.
- **Result:** $97.4\%$ ($N = 39$).
- **Limitations:** Automated extraction; subjective nuance requires advocate sign-off.

### Metric 4: Contradicted Claim Rate
- **Formula:** $\frac{\text{Contradicted Claims}}{\text{Total Evaluated Claims}}$
- **Eligibility:** All emitted claims subjected to contradiction audit against ground truth.
- **Result:** $0.0\%$ ($N = 39$).
- **Limitations:** Limited to modeled contradictory holdings in knowledge base.

### Metric 5: Unsupported Claim Rate
- **Formula:** $\frac{\text{Unsupported Claims}}{\text{Total Evaluated Claims}}$
- **Eligibility:** Claims lacking supporting evidence in the knowledge base.
- **Result:** $2.6\%$ ($N = 39$).
- **Limitations:** Detects ungrounded propositions; cannot verify claims outside central acts.

### Metric 6: Temporal Version Accuracy
- **Formula:** $\frac{\text{Correct Statutory Versions Resolved}}{\text{Temporal Transition Inquiries}}$
- **Eligibility:** Inquiries involving statutory amendment or repeal boundaries.
- **Result:** $100.0\%$ ($N = 19$).
- **Limitations:** Evaluated across modeled Central Acts; State-level amendments require future ingestion.

### Metric 7: Precedent Status Fidelity
- **Formula:** $\frac{\text{Correctly Qualified Precedent Decisions}}{\text{Cases Involving Overruled/Referred/Stayed Precedents}}$
- **Eligibility:** Inquiries citing non-final or qualified judicial authorities.
- **Result:** $100.0\%$ ($N = 5$).
- **Limitations:** Knowledge graph coverage focused on landmark Supreme Court decisions.

### Metric 8: Holding Scope Calibration
- **Formula:** $\frac{\text{Correctly Bound Holdings}}{\text{Inquiries Involving Coordinate Divergence or Bench Hierarchies}}$
- **Eligibility:** Cases testing territorial or bench size limitations.
- **Result:** $100.0\%$ ($N = 4$).
- **Limitations:** Assumes High Court territorial jurisdiction is known or queried.

### Metric 9: Jurisdiction Accuracy
- **Formula:** $\frac{\text{Correct Territorial Forums Resolved}}{\text{Jurisdiction-Sensitive Inquiries}}$
- **Eligibility:** Inquiries where state legislation or High Court rules apply.
- **Result:** $100.0\%$ ($N = 6$).
- **Limitations:** Relies on user-specified forum or triggers clarifying question.

### Metric 10: Appropriate Abstention Rate
- **Formula:** $\frac{\text{True Abstentions}}{\text{Total Inquiries Requiring Abstention}}$
- **Eligibility:** Inquiries involving uncommenced statutes, fabricated citations, or unverified leaks.
- **Result:** $100.0\%$ ($N = 6$).
- **Limitations:** Only measures modeled abstention triggers.

### Metric 11: Clarification Request Rate
- **Formula:** $\frac{\text{Appropriate Clarification Requests Emitted}}{\text{Inquiries with Decisive Missing Facts}}$
- **Eligibility:** Inquiries lacking material transaction dates, registration, or forum.
- **Result:** $100.0\%$ ($N = 4$).
- **Limitations:** Threshold-based trigger on decisive fact absence.

### Metric 12: Factual Dependency Capture
- **Formula:** $\frac{\text{Identified Missing Factual Dependencies}}{\text{Total Missing Decisive Dependencies}}$
- **Eligibility:** Benchmark cases with missing material facts in query text.
- **Result:** $100.0\%$ ($N = 4$).
- **Limitations:** Regex and domain heuristics cover 12 core legal domains.

### Metric 13: Hallucinated Authority Rate
- **Formula:** $\frac{\text{Fabricated Authorities Emitted}}{\text{Total Authorities Cited}}$
- **Eligibility:** All cited cases and statutory enactments.
- **Result:** **0.0%** ($N = 57$).
- **Limitations:** Strict source registry filtering prevents citation of unindexed records.

### Metric 14: Adversarial Robustness Rate
- **Formula:** $\frac{\text{Defeated Adversarial Attacks}}{\text{Total Adversarial Red Team Attacks}}$
- **Eligibility:** All 20 attack scenarios in the D1–D4 red-team suite.
- **Result:** **100.0%** ($N = 20$).
- **Limitations:** Based on the 20 attack vectors defined in the Phase 51 catalog.

### Metric 15: Claim Grounding Density
- **Formula:** $\frac{\text{Verifiable Verbatim Passage Tokens}}{\text{Total Generated Claim Tokens}}$
- **Eligibility:** Substantive position prose across all answered queries.
- **Result:** $0.842$ ($N = 39$).
- **Limitations:** Measures token overlap between verbatim statutory extracts and claims.
