"""
Script: scripts/build_review_package.py
Generates the complete Advocate Review Package in data/06_review/:
1. ADVOCATE_REVIEW_GUIDE.md: Detailed instructions, legal framework, and rubric.
2. pilot_20_review_sheet.csv: Reviewer spreadsheet with blank decision fields.
3. pilot_20_source_bundle.json: Full machine-readable bundle linking records to sources.
4. pilot_20_open_issues.md: Analysis of the 6 prioritized legal ambiguities.
"""

import csv
import json
from pathlib import Path
from datetime import date

from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import LegalQADocument

SPECIFIC_ADVOCATE_QUESTIONS = {
    "QA-PILOT-DPDP-001": (
        "Does the answer accurately reflect the scope of information a Data Principal may request under s. 11(1), "
        "and is the distinction between 'summary of personal data' and raw data clear?"
    ),
    "QA-PILOT-DPDP-002": (
        "Under s. 12(3), does the exception ('unless retention of the same is necessary for the specified purpose or for compliance with any law') "
        "warrant additional qualification regarding pending tax/regulatory audits?"
    ),
    "QA-PILOT-DPDP-003": (
        "Is the requirement under s. 13(3) to 'exhaust the opportunity of redressing her grievance' an absolute statutory bar "
        "to directly filing a complaint before the Data Protection Board under s. 27(1)(a)?"
    ),
    "QA-PILOT-DPDP-004": (
        "Under s. 8(5), does the standard of 'reasonable security safeguards' leave liability open under common law/IT Act "
        "until 13 May 2027, and does the note on existing law sufficiently guide counsel?"
    ),
    "QA-PILOT-DPDP-005": (
        "Regarding s. 6(1), is the interaction between Section 6 consent and Section 7 'legitimate uses' adequately distinguished?"
    ),
    "QA-PILOT-DPDP-006": (
        "In s. 8(6), does 'each affected Data Principal' impose a strict obligation to notify without a materiality/risk threshold, "
        "and will this require subordinate rules clarification?"
    ),
    "QA-PILOT-DPDP-007": (
        "Does the phrase 'determines on conclusion of an inquiry that breach... is significant' in s. 33(1) create a statutory jurisdictional prerequisite "
        "before penalties can be imposed?"
    ),
    "QA-PILOT-DPDP-008": (
        "Under Schedule Item 1 read with s. 33(1), is the 250 crore INR maximum penalty correctly cited, "
        "and should the guidance mention mitigating factors under s. 33(2)?"
    ),
    "QA-PILOT-DPDP-009": (
        "PRIORITY ISSUE 2: Is the computation of 18 calendar months under General Clauses Act s. 9 from 13 Nov 2025 to 13 May 2027 correct, "
        "and is s. 43A IT Act without dispute the governing statutory remedy until 13 May 2027?"
    ),
    "QA-PILOT-DPDP-010": (
        "Does the answer correctly capture the consequential amendments to s. 81 and s. 87 of the IT Act, "
        "and does the contrast with ss. 44(1) and 44(3) (commenced 13 Nov 2025) avoid confusion?"
    ),
    "QA-PILOT-CROSS-001": (
        "PRIORITY ISSUE 5: Under BSA Section 61, does the clause 'subject to the provisions of section 63' and its proviso "
        "render s. 61 purely declaratory of electronic evidence admissibility, leaving s. 63 as the exclusive gateway?"
    ),
    "QA-PILOT-CROSS-002": (
        "Under the proviso to s. 61, does failure to produce a section 63(4) certificate at the time of producing evidence "
        "constitute an incurable defect, or can it be cured later under emerging judicial precedent?"
    ),
    "QA-PILOT-CROSS-003": (
        "PRIORITY ISSUE 5: Does the proviso to s. 63(2) requiring a certificate 'signed by a person in official charge' "
        "reconcile with s. 63(4) Part A and Part B options for electronic certificate execution?"
    ),
    "QA-PILOT-CROSS-004": (
        "Can an electronic record ever be admitted as primary evidence under BSA 2023 without complying with s. 63, "
        "or has the Supreme Court ruling in Arjun Panditrao Khotkar survived into the new Adhiniyam?"
    ),
    "QA-PILOT-CROSS-005": (
        "Under IT Act s. 66, does the incorporation of IPC ss. 24 and 25 for 'dishonestly' and 'fraudulently' "
        "now transpose to Bharatiya Nyaya Sanhita (BNS) ss. 2(8) and 2(10) since 1 July 2024?"
    ),
    "QA-PILOT-CROSS-006": (
        "Under IT Act s. 66C, is 'unique identification feature' sufficiently broad under statutory interpretation "
        "to encompass biometrics, Aadhaar OTP, and cryptographic private keys?"
    ),
    "QA-PILOT-CROSS-007": (
        "Under IT Act s. 66D, does cheating by personation apply where an automated AI agent or bot personates an individual, "
        "or is human agency required?"
    ),
    "QA-PILOT-CROSS-008": (
        "Under BNSS s. 482(1), is the concurrent jurisdiction of High Court and Court of Session identical to CrPC s. 438, "
        "and does the applicant have an unfettered choice of forum?"
    ),
    "QA-PILOT-CROSS-009": (
        "PRIORITY ISSUE 1: In BNSS s. 482(4), does the bar on anticipatory bail for BNS s. 65 and s. 70(2) "
        "extend to abetment (BNS s. 45), attempt (BNS s. 62), or criminal conspiracy (BNS s. 61) to commit those offences?"
    ),
    "QA-PILOT-CROSS-010": (
        "PRIORITY ISSUE 4: Under BNSS s. 531(2)(a), does the savings protection strictly apply to investigations "
        "pending prior to 1 July 2024, and is the schema representation (BNSS s. 531 in force; CrPC 1973 repealed with savings) legally sound?"
    ),
}


def build_review_package():
    review_dir = Path("data/06_review")
    review_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Registry and Source Texts
    reg = SourceRegistryManager("registry/source_registry.jsonl")
    examples_file = Path("data/03_generated/pilot_20_examples.jsonl")
    
    docs = []
    with open(examples_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(LegalQADocument(**json.loads(line)))

    print(f"Loaded {len(docs)} pilot examples from {examples_file}")

    # 2. Build pilot_20_review_sheet.csv
    csv_path = review_dir / "pilot_20_review_sheet.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        fieldnames = [
            "record_id",
            "category",
            "question",
            "proposed_answer",
            "legal_as_of_date",
            "law_status_label",
            "provision_commencement_status",
            "commencement_notification",
            "commencement_date",
            "statutory_citations",
            "supporting_source_ids",
            "source_urls",
            "verbatim_evidence_passages",
            "repealed_statute_context",
            "repealed_statute_status",
            "specific_advocate_question",
            "review_decision",
            "legal_accuracy_score_1_to_5",
            "temporal_accuracy_score_1_to_5",
            "grounding_accuracy_score_1_to_5",
            "reviewer_comments",
            "reviewer_name_initials",
            "review_date",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for doc in docs:
            category = "DPDP & IT Act Statutory QA" if doc.qa_id.startswith("QA-PILOT-DPDP-") else "Cross-Statute Evidence & Cybercrime"
            
            # Fetch source URLs from registry
            urls = []
            for sid in doc.supporting_source_ids:
                rec = reg.get(sid)
                if rec:
                    urls.append(f"{sid}: {rec.source_url}")
                else:
                    urls.append(f"{sid}: [Not registered]")

            # Format evidence passages
            passages_text = []
            for p in doc.evidence_passages:
                passages_text.append(f"[{p.source_id} | {p.section_or_para_ref}]: {p.verbatim_text}")

            advocate_question = SPECIFIC_ADVOCATE_QUESTIONS.get(doc.qa_id, "Please review for statutory accuracy and completeness.")

            writer.writerow({
                "record_id": doc.qa_id,
                "category": category,
                "question": doc.question,
                "proposed_answer": doc.answer,
                "legal_as_of_date": doc.legal_as_of_date.isoformat() if doc.legal_as_of_date else "",
                "law_status_label": doc.law_status_label.value if doc.law_status_label else "",
                "provision_commencement_status": doc.provision_commencement_status.value if doc.provision_commencement_status else "",
                "commencement_notification": doc.commencement_source_id or "",
                "commencement_date": doc.commencement_date.isoformat() if doc.commencement_date else "",
                "statutory_citations": "; ".join(doc.statutory_citations or []),
                "supporting_source_ids": "; ".join(doc.supporting_source_ids),
                "source_urls": " | ".join(urls),
                "verbatim_evidence_passages": " \n\n ".join(passages_text),
                "repealed_statute_context": doc.repealed_statute_context or "",
                "repealed_statute_status": doc.repealed_statute_status.value if doc.repealed_statute_status else "",
                "specific_advocate_question": advocate_question,
                "review_decision": "",  # Pending review
                "legal_accuracy_score_1_to_5": "",
                "temporal_accuracy_score_1_to_5": "",
                "grounding_accuracy_score_1_to_5": "",
                "reviewer_comments": "",
                "reviewer_name_initials": "",
                "review_date": "",
            })

    print(f"Exported review sheet to {csv_path}")

    # 3. Build pilot_20_source_bundle.json
    bundle_path = review_dir / "pilot_20_source_bundle.json"
    bundle_data = {
        "bundle_version": "1.0.0",
        "generated_at": date.today().isoformat(),
        "audit_phase": "Phase 7.2 Advocate Review Package",
        "total_records": len(docs),
        "review_status_summary": {
            "pending_legal_review": len(docs),
            "approved": 0,
            "rejected": 0,
            "revision_required": 0,
        },
        "records": [],
    }

    for doc in docs:
        source_records_meta = []
        for sid in doc.supporting_source_ids:
            rec = reg.get(sid)
            if rec:
                source_records_meta.append({
                    "document_id": rec.document_id,
                    "title": rec.title,
                    "source_url": rec.source_url,
                    "source_type": rec.source_type.value,
                    "document_date": rec.document_date.isoformat(),
                    "effective_date": rec.effective_date.isoformat() if rec.effective_date else None,
                    "licence_or_terms": rec.licence_or_terms,
                    "checksum": rec.checksum,
                })

        record_entry = {
            "record_id": doc.qa_id,
            "category": "DPDP & IT Act Statutory QA" if doc.qa_id.startswith("QA-PILOT-DPDP-") else "Cross-Statute Evidence & Cybercrime",
            "question": doc.question,
            "proposed_answer": doc.answer,
            "legal_as_of_date": doc.legal_as_of_date.isoformat() if doc.legal_as_of_date else None,
            "temporal_metadata": {
                "law_status_label": doc.law_status_label.value if doc.law_status_label else None,
                "provision_commencement_status": doc.provision_commencement_status.value if doc.provision_commencement_status else None,
                "commencement_source_id": doc.commencement_source_id,
                "commencement_date": doc.commencement_date.isoformat() if doc.commencement_date else None,
                "temporal_validation_status": doc.temporal_validation_status.value if doc.temporal_validation_status else None,
                "repealed_statute_context": doc.repealed_statute_context,
                "repealed_statute_status": doc.repealed_statute_status.value if doc.repealed_statute_status else None,
            },
            "statutory_citations": doc.statutory_citations,
            "evidence_passages": [p.model_dump() for p in doc.evidence_passages],
            "supporting_sources": source_records_meta,
            "specific_advocate_question": SPECIFIC_ADVOCATE_QUESTIONS.get(doc.qa_id, "Please review for statutory accuracy and completeness."),
            "review_status": "pending_legal_review",
            "decision": None,
        }
        bundle_data["records"].append(record_entry)

    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle_data, f, indent=2, ensure_ascii=False)

    print(f"Exported source bundle to {bundle_path}")

    # 4. Build ADVOCATE_REVIEW_GUIDE.md
    guide_path = review_dir / "ADVOCATE_REVIEW_GUIDE.md"
    guide_content = """# LEGALMITRA ADVOCATE REVIEW GUIDE
**Controlled 20-Example Pilot Review Package**
*Version 1.0 — Phase 7.2 Release*

---

## 1. Overview and Purpose

Welcome to the LegalMitra Review Package. LegalMitra is an open-source Indian legal dataset engineering pipeline and retrieval-augmented generation (RAG) framework.

This package contains **20 carefully curated, source-grounded Question-and-Answer pairs** spanning:
1. **Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)** and its phased commencement under Notification **G.S.R. 843(E)**.
2. **Information Technology Act, 2000 (Act No. 21 of 2000)** cyber offences and the operative validity of Section 43A.
3. **Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023)** electronic records admissibility (ss. 61 & 63).
4. **Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)** anticipatory bail exclusions (s. 482) and repeal/savings (s. 531).

All 20 records are currently designated as **`pending_legal_review`**. In accordance with legal-engineering ethics, automated validators are strictly prohibited from self-approving legal advice. We require your independent judgment as an advocate or legal scholar to review, score, and validate each record.

---

## 2. Review Artifacts

The review package in `data/06_review/` consists of:
1. **`ADVOCATE_REVIEW_GUIDE.md`** (this document): Review principles, statutory timeline, and scoring criteria.
2. **`pilot_20_review_sheet.csv`**: Review spreadsheet containing questions, answers, evidence spans, temporal tags, specific counsel questions, and blank decision/score fields.
3. **`pilot_20_source_bundle.json`**: Machine-readable JSON linking every record directly to raw statutory source texts, gazette notifications, and cryptographic checksums.
4. **`pilot_20_open_issues.md`**: In-depth legal analysis of the 6 prioritized statutory and procedural ambiguities.

---

## 3. Statutory Background & Temporal Timelines

To ensure accurate evaluation, please apply the following statutory milestones:

### A. Digital Personal Data Protection Act, 2023 (DPDP Act)
- **Enactment Date**: 11 August 2023 (Act No. 22 of 2023).
- **Commencement Schedule**: Notification **G.S.R. 843(E)** dated 13 November 2025:
  * **Group 1 (13 November 2025)**: Preliminary, definitions, Data Protection Board establishment, and specific oversight powers (ss. 2, 18–26, 35, 38–43, 44(1), 44(3)).
  * **Group 2 (13 November 2026 / 1 Year)**: Section 6(9) (notice of pre-existing consent) and Section 27(1)(d).
  * **Group 3 (13 May 2027 / 18 Months)**: Substantive consent and fiduciary obligations, Data Principal rights, penalties, and IT Act amendments (ss. 3–5, 6(1)–(8), (10), 7–17, balance of 27, 28–34, 36, 37, 44(2)).
  * *Note on Calculation*: 18 calendar months computed from 13 November 2025 under Section 9 of the General Clauses Act, 1897 concludes on **13 May 2027**.

### B. Information Technology Act, 2000 (IT Act)
- **Section 43A**: Compensation for failure to protect sensitive personal data.
- **Operative Status**: While DPDP Act s. 44(2)(a) omits s. 43A, Section 44(2) falls under Group 3 (13 May 2027). Therefore, **Section 43A remains fully operative, valid, and enforceable law until 13 May 2027**.
- **Cyber Offences**: ss. 66, 66C, 66D are in force since 27 October 2009 (Act 10 of 2009).

### C. Bharatiya Sakshya Adhiniyam, 2023 (BSA)
- **Commencement Date**: 1 July 2024 via Notification **S.O. 849(E)**.
- **Electronic Records**: Section 61 provides that electronic records have documentary enforceability, **subject to Section 63** and mandatory certificate under Section 63(4).

### D. Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
- **Commencement Date**: 1 July 2024 via Notification **S.O. 848(E)**.
- **Section 482**: Anticipatory bail jurisdiction before High Court and Court of Session; sub-section (4) bars anticipatory bail for offences under BNS ss. 65 & 70(2).
- **Section 531 Anti-Conflation**: Section 531 is an **in-force provision** of the BNSS. It repeals the Code of Criminal Procedure, 1973 with savings for pending appeals, applications, trials, inquiries, and investigations.

---

## 4. Review Rubric & Scoring Criteria

When reviewing records in `pilot_20_review_sheet.csv`, please evaluate three dimensions on a **1 to 5 scale**:

### 1. Legal Accuracy (1 to 5)
- **5 (Exemplary)**: Completely sound legal reasoning; flawless interpretation of statutory terms; fully reflects Indian jurisprudence.
- **4 (Sound)**: Substantively correct; minor stylistic or terminology preference could improve clarity.
- **3 (Acceptable with Reservation)**: Correct in outcome but omits important nuances, qualifications, or provisos.
- **2 (Inaccurate)**: Mischaracterizes a statutory provision or confuses distinct legal standards.
- **1 (Legally Erroneous)**: Blatantly incorrect legal claim or hallucination.

### 2. Temporal Accuracy (1 to 5)
- **5 (Flawless)**: Precisely distinguishes current law from enacted-uncommenced provisions; accurately cites Gazette notifications.
- **4 (Substantially Accurate)**: Correctly identifies current vs future status; notification citation is accurate.
- **3 (Ambiguous)**: Notes that law is changing but does not clearly specify whether rights are currently enforceable today.
- **1–2 (Temporal Defect)**: Asserts that an uncommenced right is operative today, or falsely claims an in-force law is repealed.

### 3. Grounding & Zero-Hallucination (1 to 5)
- **5 (Strictly Grounded)**: Every proposition in the answer directly flows from the verbatim evidence passage.
- **4 (Well Grounded)**: Completely supported; slight restatement or synthesis without adding ungrounded facts.
- **3 (Extrapolated)**: Answer brings in general knowledge or commentary not present in the cited evidence passage.
- **1–2 (Ungrounded)**: Invented section numbers, non-existent qualifications, or fabricated facts.

---

## 5. Review Decisions

For each record, enter one of the following in the `review_decision` column:
- **`APPROVED`**: Record meets high standards of legal correctness and temporal grounding.
- **`REVISION_REQUIRED`**: Record is conceptually salvageable but requires specific edits to question, answer, or citation.
- **`REJECTED`**: Record has fundamental legal defects, is ungrounded, or misleads users.

---

## 6. How to Submit Your Review

1. Open `data/06_review/pilot_20_review_sheet.csv` in Excel, LibreOffice Calc, or your preferred CSV editor.
2. Review each record alongside the source texts provided in `pilot_20_source_bundle.json`.
3. Consult `pilot_20_open_issues.md` when reviewing the 6 prioritized ambiguity records.
4. Fill in `review_decision`, scores (1-5), `reviewer_comments`, `reviewer_name_initials`, and `review_date`.
5. Save the CSV and return it to the LegalMitra dataset maintainers.
"""

    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)

    print(f"Exported advocate review guide to {guide_path}")

    # 5. Build pilot_20_open_issues.md
    issues_path = review_dir / "pilot_20_open_issues.md"
    issues_content = """# LEGAL AMBIGUITIES & OPEN QUESTIONS MEMORANDUM
**LegalMitra Pilot 20 — Phase 7.2 Counsel Briefing**

---

## Purpose

This memorandum provides Indian legal counsel and judicial researchers with an analytical briefing on the **six prioritized legal ambiguities** encountered in the LegalMitra 20-example pilot.

Dataset engineering systems must not resolve open legal questions by algorithmic speculation. Where statutory language is ambiguous, silent, or subject to conflicting High Court interpretations, the dataset must transparently reflect that ambiguity and seek formal advocate review.

---

## Issue 1: BNSS Section 482(4) — Scope of Anticipatory Bail Bar

### Relevant Record: `QA-PILOT-CROSS-009`
- **Statutory Provision**: Section 482(4), Bharatiya Nagarik Suraksha Sanhita, 2023.
- **Statutory Text**:
  > *"Nothing in this section shall apply to any case involving the arrest of any person on accusation of having committed an offence under section 65 and sub-section (2) of section 70 of the Bharatiya Nyaya Sanhita, 2023."*
- **The Ambiguity**:
  1. Section 482(4) explicitly bars anticipatory bail for principal offences under BNS Section 65 (rape of female under 16 or 12 years) and Section 70(2) (gang rape of female under 18 years).
  2. Does this absolute statutory bar extend to:
     - **Abetment** of such offences (BNS Section 45 / IPC Section 109)?
     - **Attempt** to commit such offences (BNS Section 62 / IPC Section 511)?
     - **Criminal Conspiracy** (BNS Section 61 / IPC Section 120B)?
  3. Under predecessor CrPC Section 438(4) (inserted by Act 22 of 2018 regarding IPC ss. 376(3), 376AB, 376DA, 376DB), various High Courts differed on whether an accused charged solely with conspiracy or abetment is subject to the threshold bar.
- **Question for Reviewer**:
  Should the LegalMitra answer explicitly warn users that the applicability of Section 482(4) to conspiracy/abetment remains a matter of judicial discretion and evolving High Court precedent?

---

## Issue 2: IT Act Section 43A — Operative Validity During DPDP Phased Rollout

### Relevant Record: `QA-PILOT-DPDP-009`
- **Statutory Provision**: Section 43A, Information Technology Act, 2000 vs Section 44(2)(a), DPDP Act, 2023.
- **The Ambiguity**:
  1. Section 44(2)(a) of the DPDP Act provides: *"section 43A shall be omitted"*.
  2. Many commentary sources incorrectly reported that Section 43A was repealed upon the enactment of the DPDP Act on 11 August 2023.
  3. Notification **G.S.R. 843(E)** (13 November 2025) schedules Section 44(2) for commencement on the expiry of eighteen months from publication.
  4. Under Section 9 of the General Clauses Act, 1897, computing 18 calendar months from 13 November 2025 places commencement on **13 May 2027**.
- **Questions for Reviewer**:
  - Is Section 43A read with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 undeniably the governing civil compensation regime until 13 May 2027?
  - Does the pending omission create any transitional gap for claims arising before 13 May 2027 that are adjudicated after that date?

---

## Issue 3: DPDP Act Section 6(9) vs General Consent Commencement

### Relevant Record: `QA-PILOT-DPDP-005` & Notification G.S.R. 843(E)
- **Statutory Provision**: Section 6(9) vs Sections 6(1)–(8) of the DPDP Act, 2023.
- **The Ambiguity**:
  1. Notification G.S.R. 843(E) schedules **Section 6(9)** in **Group 2** (commencing 13 November 2026, 1 year from notification).
  2. However, the rest of Section 6—sub-sections (1) through (8) and (10)—along with the foundational notice obligations under Section 5, are scheduled in **Group 3** (commencing 13 May 2027, 18 months from notification).
  3. Section 6(9) requires Data Fiduciaries to give notice to Data Principals who gave consent *before* the commencement of the Act *"as soon as it is reasonably practicable"*.
- **Questions for Reviewer**:
  - How can a Data Fiduciary issue a compliant Section 6(9) notice starting 13 November 2026 when the substantive notice contents under Section 5 and withdrawal mechanisms under Section 6(4) do not commence until 13 May 2027?
  - Does this asymmetry require subordinate rules under Section 40 to provide bridging mechanisms?

---

## Issue 4: BNSS Section 531 — Savings Clause & Temporal Representation

### Relevant Record: `QA-PILOT-CROSS-010`
- **Statutory Provision**: Section 531, Bharatiya Nagarik Suraksha Sanhita, 2023.
- **The Ambiguity**:
  1. Section 531(1) repeals the CrPC, 1973.
  2. Section 531(2)(a) protects pending appeals, applications, trials, inquiries, and investigations initiated prior to 1 July 2024.
  3. In initial automated schemas, Section 531 was mistakenly categorized as `repealed_with_savings` because automated parsers conflated the repeal of the CrPC with the status of Section 531 itself.
  4. In truth, **BNSS Section 531 is in force as contemporary primary law**.
- **Questions for Reviewer**:
  - Is the revised schema representation (`law_status_label = in_force` for BNSS s. 531, with `repealed_statute_context = "CrPC 1973 is repealed with savings"` and `repealed_statute_status = repealed_with_savings`) conceptually sound?
  - If an FIR was registered on 30 June 2024 but investigation continued into 2025, does the entire investigative and bail procedure remain under CrPC 1973 as held in recent High Court rulings?

---

## Issue 5: BSA Section 63 — Certificate Requirements & Admissibility Scope

### Relevant Records: `QA-PILOT-CROSS-001`, `QA-PILOT-CROSS-002`, `QA-PILOT-CROSS-003`, `QA-PILOT-CROSS-004`
- **Statutory Provisions**: Sections 61, 62, and 63, Bharatiya Sakshya Adhiniyam, 2023.
- **The Ambiguity**:
  1. Section 61 provides that electronic records have documentary validity, but opens with the restriction: *"subject to the provisions of section 63"*, and concludes with a proviso requiring a Section 63(4) certificate.
  2. In *Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal* (2020) 7 SCC 1, the Supreme Court held that production of a certificate under predecessor Section 65B(4) of the Indian Evidence Act, 1872 is a condition precedent to admissibility where the original device is not produced.
  3. Under BSA Section 63(4), a certificate may now be signed by a person in charge of the computer device or an expert (Schedule / Part A / Part B).
- **Questions for Reviewer**:
  - Does the proviso to Section 61 make the certificate mandatory in *all* instances where electronic records are produced in evidence, or does Section 62 permit oral evidence if the original device is brought to court?
  - Does the failure to produce a Section 63(4) certificate alongside the charge-sheet remain curable before trial begins?

---

## Issue 6: Extrapolation Beyond Cited Statutory Text

### Relevant Records: All 20 Pilot Records
- **The Ambiguity**:
  1. Legal AI systems frequently introduce ancillary assertions (such as commenting on judicial discretion, subordinate rules, or historical common law) that do not appear verbatim in the statutory excerpt.
  2. In `QA-PILOT-DPDP-004`, for instance, the answer includes an editorial note clarifying that until 13 May 2027, reasonable security practices remain governed by the IT Act, 2000.
  3. In `QA-PILOT-CROSS-005`, the answer incorporates IPC Sections 24 and 25 referenced in the statutory Explanation.
- **Questions for Reviewer**:
  - Does inclusion of essential statutory context (such as identifying the predecessor statute or transitional dates) enhance dataset utility, or should the pipeline enforce strict isolation where the model may only state what is written in the four corners of the cited excerpt?
  - What boundary guidelines do advocates recommend for dataset generation prompt engineering?
"""

    with open(issues_path, "w", encoding="utf-8") as f:
        f.write(issues_content)

    print(f"Exported open issues memorandum to {issues_path}")
    print("Advocate Review Package generation completed successfully.")


if __name__ == "__main__":
    build_review_package()

