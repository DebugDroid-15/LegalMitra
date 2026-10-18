# LegalMitra Phase 31: Benchmark v9 Design Specification

**Phase:** 31  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Benchmark v9 represents the largest, most rigorous legal evaluation dataset designed for LegalMitra to date. Unlike previous benchmarks which focused primarily on statutory lookup or rote citation checks, Benchmark v9 was authored specifically to test **real custom question behavior** across complex, messy, and adversarial Indian legal scenarios.

The dataset comprises **96 verified evaluation cases** across **15 distinct evaluation categories**, codified in `data/20_evaluation/evaluation_cases_v9.json` and secured by SHA-256 manifest `data/20_evaluation/manifest_v9.json`.

---

## 2. Category Distribution & Target Rationale

| Category | Count | Focus & Realistic Failure Mode Tested |
|---|---|---|
| **1. `single_provision`** | 6 | Strict single-section interpretation without hallucinating extraneous sections |
| **2. `multi_provision`** | 7 | Cross-statute synthesis (e.g. SRA + Limitation Act, CPC + Commercial Courts Act) |
| **3. `multi_turn_context`** | 7 | Anaphora resolution, follow-up queries with pronouns ("under it", "such order") |
| **4. `missing_ambiguous_facts`** | 7 | Detection of critical missing variables (e.g. tenancy location, agreement date) |
| **5. `multi_jurisdiction`** | 6 | State rent control conflicts (Delhi vs Maharashtra vs Central enactments) |
| **6. `commencement_amendment`** | 7 | Exact enforcement dates, retrospective application, omitted provisions |
| **7. `overruled_precedent`** | 6 | Distinguishing overruled doctrine (e.g. Navtej Johar, K.S. Puttaswamy, Anvar PV) |
| **8. `statute_precedent_synthesis`**| 7 | Binding Supreme Court guidelines synthesizing statutory power (e.g. Bhajan Lal + 528 BNSS) |
| **9. `procedural_deadlines`** | 6 | Strict limitation periods (e.g. Section 34(3) Arbitration Act 30-day condonation ceiling) |
| **10. `multi_domain_scenario`** | 7 | Complex factual matrices intersecting commercial fraud, criminal FIR, and consumer law |
| **11. `legal_remedies_steps`** | 6 | Step-by-step procedural remedies (e.g. Section 175(3) BNSS when police refuse FIR) |
| **12. `false_legal_premise`** | 6 | Assertions containing legally false assumptions that must be explicitly refuted |
| **13. `unanswerable_missing_evidence`** | 6 | Out-of-corpus foreign laws or non-existent sections where system must abstain |
| **14. `cautious_explanation`** | 6 | Nuanced judicial discretion where categorical yes/no answers are legally improper |
| **15. `adversarial_safety_bypass`** | 6 | Prompt injections, POCSO minor identity leaks, and synthetic scaffold bypasses |
| **TOTAL** | **96** | **Full 15-Category Coverage** |

---

## 3. Ground Truth Verification & Manifest

The dataset was generated deterministically via `scripts/build_benchmark_v9.py`.
- **Manifest:** `data/20_evaluation/manifest_v9.json`
- **SHA-256 Checksum:** `eef9935e310959b3b83de129d9c9142c7e1459b590cdfb96304d564040b19d2a`
- **Ground Truth Status:** All 96 cases are marked `is_verified_ground_truth: true` with explicitly annotated `golden_citations`, `forbidden_terms`, `should_abstain` flags, and detailed statutory rationales.
