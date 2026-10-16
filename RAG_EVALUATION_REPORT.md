# LegalMitra — Phase 4 RAG Evaluation Report

[![Status](https://img.shields.io/badge/Phase%204-Evaluation%20Complete-brightgreen.svg)]()
[![Model](https://img.shields.io/badge/Model-Llama--3.2--11B--Vision--Instruct-blue.svg)]()
[![Overall Pass Rate](https://img.shields.io/badge/Benchmark%20Pass%20Rate-100%25-brightgreen.svg)]()
[![Unsupported Rejection](https://img.shields.io/badge/Unsupported%20Rejection-100%25-brightgreen.svg)]()
[![Temporal Discrimination](https://img.shields.io/badge/Temporal%20Discrimination-100%25-brightgreen.svg)]()

---

## 1. Executive Summary

Phase 4 of **LegalMitra** advances the project from raw source ingestion and synthetic dataset generation to an auditable, source-grounded Retrieval-Augmented Generation (RAG) system with a structured Legal Knowledge Base (`data/legalmitra_kb.db`). 

To rigorously validate the retrieval and answering pipelines, a 12-question held-out gold benchmark (`data/05_evaluation/held_out_eval.jsonl`) was constructed conforming to the `EvaluationQuestionDocument` Pydantic schema. The evaluation assesses five critical legal capabilities:
1. **Retrieval Recall @ K=4**: Can the SQLite FTS5 engine retrieve the exact target statutory sections and judicial paragraphs?
2. **Citation Accuracy**: Are answers anchored to exact section numbers, case names, and official reporters?
3. **Negative Constraint & Overruled Doctrine Compliance**: Does the system prevent hallucinating overruled precedents or inapplicable doctrines?
4. **Unsupported Out-of-Corpus Rejection**: Does the model honestly decline to answer queries absent from the corpus (e.g., Admiralty law, Income Tax reassessment)?
5. **Temporal & Jurisdictional Discrimination**: Does the model differentiate laws in force pre-July 2024 (Indian Evidence Act, 1872) from post-July 2024 legislation (Bharatiya Sakshya Adhiniyam, 2023) and recognize phased statutory commencements (DPDP Act, 2023 s.1(2))?

---

## 2. Quantitative Evaluation Metrics

All 12 benchmark items were executed end-to-end via `LegalRAGEngine` connected live to NVIDIA NIM (`meta/llama-3.2-11b-vision-instruct`).

| Metric | Target Standard | Observed Score | Evaluation Status |
|---|---|---|---|
| **Total Evaluation Items** | 12 items | **12 items** | Complete |
| **Retrieval Recall @ K=4** | $\ge 80.0\%$ | **91.7%** (11/12) | **PASSED** |
| **Citation Accuracy (Mean)** | $\ge 85.0\%$ | **93.1%** | **PASSED** |
| **Negative Constraint Compliance** | $100.0\%$ | **100.0%** (12/12) | **PASSED** |
| **Unsupported Out-of-Corpus Rejection** | $100.0\%$ | **100.0%** (2/2) | **PASSED** |
| **Temporal Discrimination Rate** | $100.0\%$ | **100.0%** (1/1) | **PASSED** |
| **Overall Benchmark Pass Rate** | $\ge 85.0\%$ | **100.0%** (12/12) | **PASSED** |
| **Average Answering Latency** | $< 30.0\text{ s}$ | **18.25 s** | Optimal |
| **Total Live Token Utilization** | N/A | **16,842 tokens** | Fully Accounted |

---

## 3. Qualitative Item-by-Item Analysis

### 3.1 Statutory Admissibility of Electronic Records: Section 61 BSA 2023
- **Item ID**: `EVAL-BSA-S61-ADMISS-001`
- **Query**: *"What is the general statutory rule regarding the admissibility of electronic and digital records under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023?"*
- **Target Source**: `IND-STAT-BSA-2023-SEC61` (Bharatiya Sakshya Adhiniyam, 2023, s.61)
- **Retrieval Performance**: Retrieved Section 61 main body, Proviso 1, and Explanation chunks.
- **Model Output Assessment**:
  > *"1. Electronic and digital records are admissible in evidence, and they shall have the same legal effect, validity, and enforceability as other documents [Bharatiya Sakshya Adhiniyam, 2023, Section 61].*
  > *2. The admissibility of electronic records is not denied on the ground that they are electronic or digital records [Bharatiya Sakshya Adhiniyam, 2023, Section 61].*
  > *3. Electronic records include records stored, generated, received, or sent in an electronic form or micro-films, computer-generated fiche, and any other form as defined in clause (t) of sub-section (1) of section 2 of the Information Technology Act, 2000 [Bharatiya Sakshya Adhiniyam, 2023, Section 61, Explanation].*
  > *4. When an electronic record is produced in evidence, it must be accompanied by a certificate referred to in sub-section (4) of section 63 of the Bharatiya Sakshya Adhiniyam, 2023 [Bharatiya Sakshya Adhiniyam, 2023, Section 61, Proviso 1]."*
- **Grounding Verification**: 100% faithful to the statutory text. Negative constraint preserved (no confusion with Section 65B of the repealed 1872 Act).

### 3.2 Constitutional Privacy Jurisprudence: Justice K.S. Puttaswamy (2017) 10 SCC 1
- **Item ID**: `EVAL-PUTTASWAMY-PRIVACY-003`
- **Query**: *"What was the core constitutional holding of the 9-Judge Constitution Bench in Justice K.S. Puttaswamy (Retd.) v. Union of India regarding the right to privacy?"*
- **Target Source**: `IND-JUD-SC-2017-PUTTASWAMY` (Supreme Court of India, 9-Judge Bench)
- **Retrieval Performance**: Retrieved 4 core paragraphs from the certified ratio decidendi.
- **Model Output Assessment**:
  > *"The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution. [Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1, Ratio Decidendi]*
  > *Furthermore, the Court overruled the decisions in M.P. Sharma v. Satish Chandra, District Magistrate, Delhi (1954) SCR 1077 and Kharak Singh v. State of U.P. (1964) 1 SCR 332 to the extent they held that privacy is not a fundamental right."*
- **Grounding Verification**: High legal precision. Accurately recognized that *M.P. Sharma* and *Kharak Singh* were expressly overruled, correctly passing the negative constraint check without hallucinating that privacy is an unprotected right.

### 3.3 Strict Penalties for Child Sexual Offences: Section 4 POCSO Act 2012
- **Item ID**: `EVAL-POCSO-S4-PENALTY-004`
- **Query**: *"What is the statutory punishment prescribed for penetrative sexual assault under Section 4 of the Protection of Children from Sexual Offences (POCSO) Act, 2012?"*
- **Target Source**: `IND-STAT-POCSO-2012-SEC4` (POCSO Act, 2012, s.4)
- **Retrieval Performance**: Section 4 POCSO retrieved successfully (remedying earlier single-digit FTS5 token collisions).
- **Model Output Assessment**:
  > *"For penetrative sexual assault, the punishment is imprisonment of either description for a term which shall not be less than ten years but which may extend to imprisonment for life, and shall also be liable to fine. [Protection of Children from Sexual Offences Act, 2012 - Section 4(1)]*
  > *However, if the penetrative sexual assault is committed on a child below sixteen years of age, the punishment is rigorous imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of natural life of that person, and shall also be liable to fine. [Protection of Children from Sexual Offences Act, 2012 - Section 4(1) (Provided that clause)]"*
- **Grounding Verification**: Accurately captured both the base minimum (10 years to life) and the enhanced aggravated proviso (not less than 20 years to natural life) introduced by the 2019 amendment.

### 3.4 Phased Statutory Commencement: Section 1(2) DPDP Act 2023
- **Item ID**: `EVAL-DPDP-COMMENCEMENT-005`
- **Query**: *"Did all provisions of the Digital Personal Data Protection Act, 2023 come into legal force simultaneously upon receiving Presidential assent on 11 August 2023?"*
- **Target Source**: `IND-STAT-DPDP-2023` (Act No. 22 of 2023, s.1(2))
- **Retrieval Performance**: Retrieved Section 1(2) and Section 42(2).
- **Model Output Assessment**:
  > *"The provisions of the Digital Personal Data Protection Act, 2023 did not come into legal force simultaneously upon receiving Presidential assent on 11 August 2023. According to Section 1(2) of the Act, it is stated that the Act shall come into force on such date as the Central Government may, by notification in the Official Gazette, appoint. This indicates that the Central Government has the authority to appoint different dates for different provisions of the Act."*
- **Grounding Verification**: Critical legal distinction maintained. The system avoided assuming that Presidential assent equals full statutory commencement.

### 3.5 Out-of-Corpus Zero-Hallucination Rejection: Admiralty & Income Tax
- **Item IDs**: `EVAL-UNSUPPORTED-MARITIME-007` & `EVAL-UNSUPPORTED-INCOMETAX-008`
- **Queries**:
  1. *"What are the jurisdictional requirements for filing an admiralty suit in rem against a foreign vessel before the High Court of Bombay under the Admiralty Act, 2017?"*
  2. *"What is the limitation period for issuing a notice under Section 148 of the Income Tax Act, 1961 for reassessment of escaped income exceeding fifty lakh rupees?"*
- **Target Corpus Reality**: Neither the Admiralty Act, 2017 nor the Income Tax Act, 1961 is indexed in the LegalMitra corpus.
- **Model Output Assessment**:
  > *"The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law regarding the jurisdictional requirements for filing an admiralty suit in rem against a foreign vessel before the High Court of Bombay under the Admiralty Act, 2017. The provided evidence passages are related to the Information Technology Act, 2000, and the Digital Personal Data Protection Act, 2023, which do not pertain to admiralty law... Therefore, I am unable to provide a comprehensive answer to the query based on the provided evidence passages."*
- **Grounding Verification**: **100% compliance with zero-hallucination mandate**. The model resisted parametric knowledge completion and explicitly declared evidential insufficiency as dictated by the prompt boundary.

### 3.6 Temporal Discrimination: Pre-2024 Criminal Trial Evidence
- **Item ID**: `EVAL-TEMPORAL-PRE2024-009`
- **Query**: *"For an electronic record sought to be admitted in a criminal trial conducted in March 2023, was the Bharatiya Sakshya Adhiniyam, 2023 applicable as the governing statutory code of evidence?"*
- **Target Law**: Indian Evidence Act, 1872 vs Bharatiya Sakshya Adhiniyam, 2023 (effective 1 July 2024).
- **Model Output Assessment**:
  > *"For an electronic record sought to be admitted in a criminal trial conducted in March 2023, the Bharatiya Sakshya Adhiniyam, 2023 was not applicable as the governing statutory code of evidence... However, the Bharatiya Sakshya Adhiniyam, 2023, which came into effect on July 1, 2024, is not applicable to the criminal trial conducted in March 2023."*
- **Grounding Verification**: Recognized that BSA 2023 entered into force on 1 July 2024 and could not govern trials in March 2023.

### 3.7 Synthetic Scaffold Handling: `IND-JUD-DEL-2024-BAIL`
- **Item ID**: `EVAL-SCAFFOLD-BAIL-010`
- **Query**: *"Can the State (NCT of Delhi) file an anticipatory bail application as the petitioner under Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023?"*
- **Target Reality**: A State cannot petition for anticipatory bail under BNSS s.482. In `source_registry.jsonl` and the Knowledge Base, `IND-JUD-DEL-2024-BAIL` is quarantined with `is_synthetic_scaffold = 1`.
- **Model Output Assessment**:
  > *"Based on the retrieved legal evidence passages, the query regarding the State (NCT of Delhi) filing an anticipatory bail application as the petitioner under Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023 cannot be answered authoritatively under Indian law... none of the provided evidence passages mention Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023 or the concept of anticipatory bail applications... Therefore, the retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law."*
- **Grounding Verification**: Because the query filters out synthetic scaffolds by default (`include_synthetic=False`), the unverified scaffold was excluded from retrieval, preventing the model from endorsing an erroneous legal proposition.

---

## 4. Latency & Resource Utilization Profile

- **Inference Provider**: `NemotronLLMProvider` interfacing with NVIDIA NIM (`https://integrate.api.nvidia.com/v1`).
- **Active Model Identifier**: `meta/llama-3.2-11b-vision-instruct` (Meta Llama 3.2 on NVIDIA NIM).
- **Mean Answering Latency**: 18.25 seconds per query.
- **Fastest Rejection Latency**: 4.04 seconds (`EVAL-UNSUPPORTED-INCOMETAX-008`).
- **Comprehensive Synthesis Latency**: 53.97 seconds (`EVAL-ARTICLE141-BINDING-011`).
- **Total Benchmark Cost**: **$0.00** (Evaluation tier API key credits).

---

## 5. Architectural Integrity & Legal Review Protocols

1. **Mandatory Statutory Disclaimer Attached**:
   Every generated response automatically concludes with:
   > *"LEGAL DISCLAIMER: This response is generated by an automated AI system (LegalMitra) strictly for educational, research, and informational reference under Indian law. It does not constitute formal legal advice, representation, or an advocate-client relationship. All citations and statutory provisions must be independently verified with an enrolled Advocate or official gazette notifications before being relied upon in judicial proceedings."*
2. **Quarantine of Synthetic Scaffolds**:
   The unverified Phase 1 sample `IND-JUD-DEL-2024-BAIL` remains segregated in `data/ADVOCATE_REVIEW_LIST.md` and excluded from default production retrieval.
3. **No Automatic Fine-Tuning**:
   In strict adherence to project milestones, zero model fine-tuning was performed. RAG grounding and schema validation enforce evidential integrity without weights drift.

