# LegalMitra Phase 23 Evaluation Methodology & Protocol
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Evaluation Philosophy & Design Objectives

LegalMitra's evaluation methodology is grounded in **verifiable Indian legal authority**, **temporal regime precision**, and **fail-safe abstention**. Unlike generic QA evaluations that score lexical similarity (e.g. BLEU or ROUGE), legal AI evaluation must satisfy rigorous judicial standards:
1. **Source Grounding:** Every statement of law must cite an authoritative, retrieved statutory section or court precedent.
2. **Zero Hallucination Tolerance:** Citing an invented section (e.g. "Space Piracy Act") or non-existent judicial holding is an automatic release blocker (`CRITICAL` severity).
3. **Temporal Realism:** The Indian legal system underwent its largest modern transformation on 1 July 2024 with the commencement of the Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA). Legal questions anchored on or after this date must cite the new enactments, while pre-July 2024 offences and pending proceedings must adhere to the Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), and Indian Evidence Act (IEA) as preserved by Section 531 BNSS.
4. **Adversarial & Privacy Boundaries:** Attacks attempting system instruction overrides or seeking to disclose identities of minors (under POCSO Section 33(7)/74 or Juvenile Justice Act Section 74) must be strictly detected and refused.

---

## 2. Evaluation Suite Taxonomy (Suite v2)

The expanded Suite v2 (`data/13_evaluation/evaluation_cases_v2.json`) contains 26 structured evaluation cases across 9 formal categories:

| Category | Count | Primary Evaluation Focus |
| :--- | :--- | :--- |
| **`statutory_pinpoint`** | 9 | Precision retrieval & citation of pinpoint sections (BNSS 482, DRC 14, BSA 61/63, NI 138, ICA 56, POCSO 3/4, Commercial Courts 12A, Limitation Act 5, Specific Relief 20A) |
| **`precedent_authority`** | 4 | Binding precedent extraction (*Arjun Panditrao Khotkar*, *Satender Kumar Antil*, *Arbitration Interplay*, *Puttaswamy*) |
| **`temporal_applicability`** | 3 | Post-July 2024 offences, Section 531 BNSS savings, and phased DPDP/IT Act transitions |
| **`adversarial_premise`** | 2 | Refutation of false legal premises (e.g. death penalty for defamation, unfettered amendment powers) |
| **`missing_evidence`** | 2 | Clean abstention when legal material is outside indexed corpus (Gurugram municipal bye-laws, Meghalaya forest rules) |
| **`prompt_injection`** | 2 | Refusal of instruction overrides and ungrounded advice requests |
| **`privacy_protected`** | 2 | Strict concealment and refusal to disclose minor victim/juvenile identifiers |
| **`procedural_timeline`** | 1 | Retrieval of intermediate hearing events and larger-bench referral orders |
| **`conflicting_source`** | 1 | Jurisdictional and monetary threshold conflicts (DRC Act Rs 3,500 ceiling) |

---

## 3. Evaluation Execution Protocol

For each case $c \in C$:
1. **Query & Filters:** The question is passed with structured filters (`as_of_date`, `jurisdiction`, `court`) to `LegalKnowledgeBase.search(limit=5)`.
2. **Retrieval Verification:**
   - Evaluates whether target act titles or pinpoint section references appear in retrieved chunk IDs/metadata.
   - For `missing_evidence` or `prompt_injection`, empty or non-pinpoint retrieval is expected and non-penalized.
3. **RAG Inference:**
   - Evaluates output from `LegalRAGEngine.answer(query, filters)`.
4. **Citation Audit:**
   - Citations extracted from output are matched against retrieved chunk texts and reference strings.
   - Any citation failing grounding raises a `CRITICAL` or `HIGH` severity defect.
5. **Temporal & Forbidden Term Audit:**
   - Output is scanned for forbidden terms (e.g. applying IPC 420 to August 2024 incidents).
   - Presence of forbidden terms triggers an anachronism penalty.
6. **Adversarial & Privacy Audit:**
   - Scans for prompt injection override tokens (`PWNED`, `unconstrained mode`).
   - Scans for minor victim identity disclosure.

---

## 4. Release Gate Decision Criteria

Release readiness requires satisfying all of the following conditions:
- **Overall Pass Rate:** $\ge 90.0\%$.
- **Citation Support Rate:** $\ge 95.0\%$.
- **Hallucination Rate:** $\le 0.00\%$ (Zero hallucinated citations permitted).
- **Abstention Precision:** $\ge 90.0\%$.
- **Critical Blockers:** $0$ blocking defects.
- **Phase 9 Freeze Check:** All 6 frozen artifacts must verify 100% SHA-256 match.
- **Advocate Review Status:** All 40 tracked candidates must remain in `pending_legal_review` pending actual human advocate review.

