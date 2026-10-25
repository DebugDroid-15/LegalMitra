# PHASE 56: LEGAL ISSUE DECOMPOSITION AND ISSUE DEPENDENCY REPORT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  
**Module:** `legalmitra.orchestration.query_understanding`  

---

## 1. Executive Summary

Phase 56 introduces structured natural-language query decomposition, transforming unstructured legal questions into auditable, multi-issue directed graphs. Each decomposed issue is assigned a unique identifier (`ISSUE-1`, `ISSUE-2`), a governing statutory framework, a relationship type (`PRIMARY_RULE`, `STATUTORY_EXCEPTION`, `PROCEDURAL_PREREQUISITE`, `UNCOMMENCED_REGIME`), and explicit prerequisite dependencies.

---

## 2. Multi-Issue Decomposition Architecture

### 2.1 Supported Compound Query Patterns
1. **Specific Relief Act (Specific Performance + Infrastructure Bar)**:
   - `ISSUE-1`: Specific performance under Section 10 SRA 1963 (`PRIMARY_RULE`).
   - `ISSUE-2`: Statutory bar on injunctions in infrastructure projects under Section 20A SRA 1963 (`STATUTORY_EXCEPTION`).
   - Dependency: `ISSUE-2` qualifies/bars injunctive remedies under `ISSUE-1`.
2. **Hindu Succession Act (Daughter's Coparcenary + Pre-2004 Partition)**:
   - `ISSUE-1`: Coparcenary rights by birth under Section 6(1) HSA 1956 (`PRIMARY_RULE`).
   - `ISSUE-2`: Statutory savings of registered partitions before 20 Dec 2004 under Section 6(1) proviso (`STATUTORY_EXCEPTION`).
   - Dependency: `ISSUE-2` is an exception that defeats coparcenary claims if partition occurred prior to 20 Dec 2004.
3. **Negotiable Instruments Act (Section 138 Notice + Section 142 Limitation)**:
   - `ISSUE-1`: Statutory demand notice within 30 days under Section 138 proviso (b) (`PROCEDURAL_PREREQUISITE`).
   - `ISSUE-2`: Limitation period of 1 month for complaint under Section 142(1)(b) (`PRIMARY_RULE`).
   - Dependency: `ISSUE-1` is a mandatory condition precedent for the cause of action in `ISSUE-2`.
4. **Labour Codes & Predecessor Statutes (Active Law + Uncommenced Enactment)**:
   - `ISSUE-1`: Retrenchment compensation under Section 25F Industrial Disputes Act, 1947 (`PRIMARY_RULE`, In Force).
   - `ISSUE-2`: Inapplicability of uncommenced Industrial Relations Code, 2020 (`UNCOMMENCED_REGIME`).
   - Dependency: Independent multi-issue analysis resolved via `ANSWER_PARTIAL`.
5. **Commercial Courts Act (Section 12A Mediation + Urgent Interim Relief)**:
   - `ISSUE-1`: Mandatory pre-institution mediation under Section 12A (`PRIMARY_RULE`).
   - `ISSUE-2`: Exemption where urgent interim relief is contemplated (`STATUTORY_EXCEPTION`).
   - Dependency: `ISSUE-2` qualifies the mandatory requirement of `ISSUE-1`.
6. **Insolvency and Bankruptcy Code (Section 32A Clean Slate + Promoter Liability)**:
   - `ISSUE-1`: Cessation of liability of corporate debtor under Section 32A(1) IBC (`PRIMARY_RULE`).
   - `ISSUE-2`: Continued criminal liability of erstwhile promoters under Section 32A(1) proviso (`STATUTORY_EXCEPTION`).

---

## 3. Procedural Posture Classification
The analyzer categorizes inquirers into procedural postures:
- `STATUTORY_PRE_SUIT_NOTICE`: Demand notice under Section 138 NI Act or Section 80 CPC.
- `COMMERCIAL_PRE_INSTITUTION_MEDIATION`: Pre-suit stage under Section 12A Commercial Courts Act.
- `INVESTIGATION_STAGE`: FIR registration, police investigation, arrest, or search.
- `BAIL_APPLICATION`: Regular or anticipatory bail under Section 438/439 CrPC or Section 482/483 BNSS.
- `QUASHING_PETITION`: High Court inherent powers under Section 482 CrPC or Section 528 BNSS.
- `ARBITRAL_MANDATE_EXTENSION`: Section 29A application before High Court or Commercial Court.
- `AWARD_CHALLENGE`: Setting aside petition under Section 34 Arbitration Act.
- `ORIGINAL_CIVIL_SUIT`: Civil suit for declaration, specific performance, or injunction.
- `APPELLATE_PROCEEDING`: First appeal, second appeal, criminal appeal, or SLP.
