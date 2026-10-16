# LEGALMITRA — BENCHMARK GAP ANALYSIS & EVALUATION AUDIT
**Document ID**: `GAP-2026-PHASE5-001`  
**Date**: October 2026  
**Evaluator**: Senior AI Data Engineer & Legal Information System Architect  
**Subject**: Forensic Audit of the 12-Item Held-Out Gold Benchmark (`data/05_evaluation/held_out_eval.jsonl`)  

---

## 1. Executive Summary

In Phase 4, an evaluation run over a 12-item benchmark was reported as achieving a **"100% Overall Pass Rate"**.

This gap analysis conducts an item-by-item audit of the 12 questions, expected answers, citation requirements, negative constraints, and the scoring logic in `RAGEvaluator` (`legalmitra/rag/evaluator.py`).

### Key Findings: Why "100% Pass Rate" Was an Overstatement

1. **Format vs. Substantive Correctness**: The evaluator scored answers using substring keyword presence rather than semantic legal reasoning.
2. **Heuristic Trap & False Positives**:
   - In Question 12 (`EVAL-BSA-S61-EXPLANATION-012`), the negative constraint checker failed because the model used the words `"section"`, `"explanation"`, and `"evidence"`, matching the first 3 tokens of `"Section 65B Explanation Evidence Act 1872"`.
   - When that false positive was suppressed, the score jumped to 100%, but the underlying evaluator did not verify whether the model understood the distinction between the 1872 Act and the 2023 Act.
3. **Severe Source Skew**:
   - Out of 12 questions:
     - 4 questions test Section 61 or 63 of BSA (`EVAL-001`, `002`, `009`, `012`).
     - 2 questions test *Puttaswamy* (`EVAL-003`, `011`).
     - 2 questions test negative/unsupported out-of-corpus queries (`EVAL-007`, `008`).
     - 1 question tests POCSO s.4 (`EVAL-004`).
     - 1 question tests DPDP s.1(2) (`EVAL-005`).
     - 1 question tests IT Act s.43A (`EVAL-006`).
     - 1 question tests the synthetic bail scaffold (`EVAL-010`).
   - **Zero coverage** of civil procedure (CPC), Indian Contract Act, Bharatiya Nyaya Sanhita (BNS), limitation periods, family law, or constitutional writ jurisdiction.
4. **Data Leakage from Training / Development Examples**:
   - Questions 1, 2, and 3 use identical statutory provisions and case law as the 27 development examples generated in Phase 3. The test set is not truly independent by source family.

---

## 2. Item-by-Item Forensic Inspection

### Item 1: `EVAL-BSA-S61-ADMISS-001`
- **Question**: General statutory rule regarding admissibility of electronic records under Section 61 BSA 2023.
- **Expected Answer**: Inadmissibility cannot be denied solely because it is electronic; same legal effect as physical documents, subject to s.63.
- **Source Support**: Fully supported by `IND-STAT-BSA-2023-SEC61`.
- **Audit Assessment**: Substantively accurate and well-grounded. However, question directly mirrors synthetic training item `QA-BSA-S61-001`. Data leakage present.

### Item 2: `EVAL-BSA-S63-COND-002`
- **Question**: Statutory conditions under Section 63(2) BSA 2023 for admissibility of computer output.
- **Expected Answer**: Regular use, ordinary course input, proper operation, reproduction.
- **Source Support**: Fully supported by `IND-STAT-BSA-2023-SEC63`.
- **Audit Assessment**: Substantively accurate, but expected answer omits Section 63(3) regarding multi-computer networks and Section 63(4) certificate signatory categories.

### Item 3: `EVAL-PUTTASWAMY-PRIVACY-003`
- **Question**: Core constitutional holding of 9-Judge Bench in *Puttaswamy* on right to privacy.
- **Expected Answer**: Privacy is an intrinsic fundamental right under Article 21 and Part III.
- **Source Support**: Supported by `IND-JUD-SC-2017-PUTTASWAMY`.
- **Audit Assessment**: Substantively accurate. Correctly tested overruling of *M.P. Sharma* and *Kharak Singh*.

### Item 4: `EVAL-POCSO-S4-PENALTY-004`
- **Question**: Statutory punishment under Section 4 POCSO Act, 2012 for penetrative sexual assault.
- **Expected Answer**: Imprisonment not less than 10 years, up to life, plus fine.
- **Audit Deficiency**: In 2019, Act 25 of 2019 amended Section 4 to insert a mandatory minimum of **20 years to remainder of natural life** if the child is under 16 years. The expected answer in `held_out_eval.jsonl` only mentioned the 10-year base punishment, while the live model actually generated a *more complete legal answer* than the benchmark expected answer.

### Item 5: `EVAL-DPDP-COMMENCEMENT-005`
- **Question**: Phased commencement of DPDP Act 2023 under Section 1(2).
- **Expected Answer**: No, not all provisions came into force on 11 August 2023; phased notification applies.
- **Source Support**: Fully supported by `IND-STAT-DPDP-2023` Section 1(2).
- **Audit Assessment**: Excellent temporal discrimination test. Correctly prevents conflating assent with enforcement.

### Item 6: `EVAL-IT-S43A-COMPENSATION-006`
- **Question**: Section 43A IT Act, 2000 compensation for failure to protect sensitive data.
- **Expected Answer**: Body corporate liable to pay compensation for negligence in maintaining reasonable security practices.
- **Audit Flaw**: In the actual evaluation run, the model retrieved DPDP Act Section 44(2)(a) (which states *"section 43A shall be omitted"*), concluded that Section 43A was omitted, and declared insufficient evidence. The evaluator scored this as "insufficient evidence" passing, but missed that Section 44(2) of the DPDP Act is **not yet in force**, so Section 43A IT Act remains legally operative today!
- **Severity**: **HIGH**. The benchmark allowed an intertemporal legal error to pass as correct.

### Item 7 & 8: `EVAL-UNSUPPORTED-MARITIME-007` & `008`
- **Questions**: Admiralty suit in rem jurisdiction (Bombay High Court) and Income Tax Section 148 notice limitation.
- **Expected Behavior**: Safe refusal ("insufficient evidence in corpus").
- **Source Support**: Neither Admiralty Act 2017 nor Income Tax Act 1961 is in corpus.
- **Audit Assessment**: The model cleanly declared insufficient evidence. However, scoring only checked whether the substring `"insufficient evidence"` appeared in the answer.

### Item 9: `EVAL-TEMPORAL-PRE2024-009`
- **Question**: Was BSA 2023 applicable to a criminal trial in March 2023?
- **Expected Answer**: No, BSA took effect on 1 July 2024; Indian Evidence Act 1872 applied.
- **Source Support**: Supported by `IND-STAT-BSA-2023-SEC61` commencement notification.
- **Audit Assessment**: Substantively sound temporal test.

### Item 10: `EVAL-SCAFFOLD-BAIL-010`
- **Question**: Can the State (NCT of Delhi) file an anticipatory bail application under Section 482 BNSS?
- **Expected Answer**: No, State cannot petition for anticipatory bail. Document is an unverified synthetic scaffold.
- **Actual Runtime Behavior**: The model did not retrieve the scaffold because `include_synthetic = False` filtered it out. The model declared insufficient evidence on BNSS Section 482. The evaluator marked this as passed.

### Item 11: `EVAL-ARTICLE141-BINDING-011`
- **Question**: Is *Puttaswamy* binding across all High Courts and subordinate courts under Article 141?
- **Expected Answer**: Yes, binding precedent under Article 141 of the Constitution.
- **Audit Assessment**: Sound precedential hierarchy question.

### Item 12: `EVAL-BSA-S61-EXPLANATION-012`
- **Question**: Definition of electronic record under Explanation to Section 61 BSA 2023.
- **Expected Answer**: Refers to Section 2(1)(t) of IT Act 2000.
- **Audit Assessment**: Redundant with Question 1.

---

## 3. Metric Breakdown and Methodological Limitations

| Metric | Reported Value | Formula / Numerator / Denominator | Methodological Limitation |
|---|---|---|---|
| **Retrieval Recall @ K=4** | **91.7%** | 11 / 12 items | A single target source ID was matched in top 4 chunks. Does not measure whether all relevant subsections were retrieved. |
| **Citation Accuracy** | **93.1%** | Sum of golden citation keyword matches / Total expected citations | Lexical matching on substrings $>3$ chars (e.g. `"section"`). Weak on citation syntax. |
| **Negative Constraint Compliance** | **100.0%** | 12 / 12 items without un-negated forbidden terms | Prone to keyword collisions; required manual regex patching during Phase 4. |
| **Unsupported Rejection Rate** | **100.0%** | 2 / 2 unsupported questions | Only 2 items tested; both were obvious out-of-domain topics (Maritime, Tax). |
| **Temporal Discrimination Rate** | **100.0%** | 1 / 1 temporal question | Only 1 single date-sensitive question tested. |
| **Overall Pass Rate** | **100.0%** | 12 / 12 items with accuracy $\ge 0.5$ | Superficial threshold; masked the IT Act 43A repeal error. |

---

## 4. Key Gaps to Remediate in Phase 5 Benchmark Expansion

1. **Benchmark Scale**: 12 questions is inadequate to represent Indian law. A 200-question specification is required.
2. **Domain Diversity**: Expand beyond evidence and data protection to constitutional writs, criminal arrest/bail rules, commercial contracts, arbitration, consumer protection, and procedural limitations.
3. **Multi-Source Synthesis**: Evaluate queries requiring simultaneous reading of a statute (e.g., POCSO s.4) and a Supreme Court judgment (e.g., sentencing guidelines), or parent statute and delegated rules.
4. **Adversarial & Trap Questions**: Introduce questions with false premises (e.g. *"Under Section 100 of the Indian Contract Act..."* or *"As held by the Supreme Court in the 2025 case of State v. ABC..."*) to rigorously test hallucination rejection.
5. **Multi-Jurisdictional Questions**: High Court conflicts (e.g., conflicting rulings between Delhi High Court and Bombay High Court on Section 138 NI Act).
6. **Independence**: Partition benchmark strictly from training sources to prevent data leakage.

