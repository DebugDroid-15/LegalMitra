# LegalMitra Phase 15 — Statutory Amendment History & Modification Engine

**Engine Version:** 1.0.0  
**Data Artifact:** `data/08_corpus/amendment_relationships.json`  
**Amending Instruments Registered:** 6  
**Provision-Level Modification Relationships:** 9  
**Target Repository:** `c:\PROJECTS\LegalMitra`

---

## 1. Overview and Purpose

A foundational challenge in Indian legal artificial intelligence is ensuring temporal fidelity—preventing models from applying amended or repealed provisions to pre-amendment disputes, or citing historical standards that have been legislatively superseded.

Phase 15 formalizes the **Amendment History & Statutory Modification Engine** (`legalmitra/corpus/amendments.py`). This engine maps:
1. The **Amending Instrument** (Act number, year, assent date, gazette notification, commencement date).
2. The **Target Provision** of the Principal Enactment.
3. The **Modification Action** (`substitution`, `insertion`, `omission`, `repeal`).
4. The **Temporal Effective Date** and statutory rationale.
5. The **Prior Law Summary** vs. **Amended Law Summary**.

---

## 2. Catalog of Registered Amending Instruments

| Instrument ID | Official Title | Enactment Ref | Commencement Date | Gazette Notification |
| :--- | :--- | :--- | :---: | :--- |
| `IND-AMEND-SRA-2018` | The Specific Relief (Amendment) Act, 2018 | Act No. 18 of 2018 | 2018-10-01 | S.O. 4888(E) dated 19 Sep 2018 |
| `IND-AMEND-ARB-2015` | The Arbitration and Conciliation (Amendment) Act, 2015 | Act No. 3 of 2016 | 2015-10-23 | Promulgated as Ordinance 23 Oct 2015 |
| `IND-AMEND-IT-2008` | The Information Technology (Amendment) Act, 2008 | Act No. 10 of 2009 | 2009-10-27 | S.O. 2689(E) dated 27 Oct 2009 |
| `IND-AMEND-CONST-106` | The Constitution (One Hundred and Sixth Amendment) Act, 2023 | Act No. 20 of 2023 | 2023-09-28 | Extraordinary Gazette 28 Sep 2023 |
| `IND-AMEND-BNS-2023` | The Bharatiya Nyaya Sanhita, 2023 (Section 358 Repeal & Savings) | Act No. 45 of 2023 | 2024-07-01 | S.O. 849(E) dated 23 Feb 2024 |
| `IND-AMEND-CPA-2019` | The Consumer Protection Act, 2019 (Section 107 Repeal & Savings) | Act No. 35 of 2019 | 2020-07-20 | S.O. 2351(E) dated 15 Jul 2020 |

---

## 3. Provision-Level Amendment Relationships

### 3.1 Specific Relief Act, 1963 (`IND-STAT-SRA-1963`)
1. **Section 10 Substitution (`REL-SRA-SEC10-SUBSTITUTION`):**
   - **Action:** Substitution by Act 18 of 2018, effective 2018-10-01.
   - **Prior Law:** Specific performance was discretionary with the court under former Section 20 ("may, in the discretion of the court, be enforced"). Damages were considered the normal remedy.
   - **Amended Law:** Specific performance is now mandatory ("The specific performance of a contract shall be enforced by the court subject to sections 11(2), 14, and 16").
   - **Significance:** Inverts the common law presumption; specific performance is the general rule, damages an exception.
2. **Section 20A Insertion (`REL-SRA-SEC20A-INSERTION`):**
   - **Action:** Insertion by Act 18 of 2018, effective 2018-10-01.
   - **Prior Law:** No special statutory bar existed preventing civil courts from granting interim or permanent injunctions in infrastructure projects.
   - **Amended Law:** Express statutory prohibition against granting injunctions in suits involving infrastructure projects listed in the Schedule if the injunction would impede or delay progress.
   - **Significance:** Protects highways, railways, power, and telecom projects from project-delaying interim injunctions.

### 3.2 Arbitration and Conciliation Act, 1996 (`IND-STAT-ARB-1996`)
1. **Section 34 Substitution (`REL-ARB-SEC34-SUBSTITUTION`):**
   - **Action:** Substitution and addition of subsection (2A) by Act 3 of 2016, effective 2015-10-23.
   - **Prior Law:** Ground of "public policy of India" was interpreted expansively under *ONGC v. Saw Pipes* to allow merits review and re-appreciation of evidence.
   - **Amended Law:** Patent illegality appearing on the face of the award restricted strictly to purely domestic arbitrations, excluding international commercial arbitrations. Proviso explicitly bars re-appreciation of evidence or review on merits.
   - **Significance:** Codifies the 246th Law Commission Report recommendations, insulating arbitral awards from judicial merits reassessment.
2. **Section 29A Insertion (`REL-ARB-SEC29A-INSERTION`):**
   - **Action:** Insertion by Act 3 of 2016, effective 2015-10-23 (further refined in 2019).
   - **Prior Law:** No statutory time limit existed for concluding arbitral proceedings; arbitration often suffered from protracted delays.
   - **Amended Law:** The arbitral award must be made within 12 months from completion of pleadings, extendable by party consent up to 6 months, after which mandate terminates unless extended by the court with potential reduction of arbitrator fees.
   - **Significance:** Enforces statutory timeliness and commercial certainty.

### 3.3 Information Technology Act, 2000 (`IND-STAT-IT-2000`)
1. **Section 43A Insertion (`REL-IT-SEC43A-INSERTION`):**
   - **Action:** Insertion by IT (Amendment) Act, 2008 (Act 10 of 2009), effective 2009-10-27.
   - **Prior Law:** Original IT Act 2000 lacked statutory corporate compensation for negligent handling of sensitive personal data or information (SPDI).
   - **Amended Law:** Mandates corporate liability to pay compensation to affected persons for negligence in implementing reasonable security practices and procedures.
   - **Significance:** Served as India's primary statutory data protection safeguard prior to the enactment of the Digital Personal Data Protection Act, 2023.
2. **Section 79 Substitution (`REL-IT-SEC79-SUBSTITUTION`):**
   - **Action:** Substitution by IT (Amendment) Act, 2008, effective 2009-10-27.
   - **Prior Law:** Limited "network service provider" exemption.
   - **Amended Law:** Comprehensive intermediary safe harbor immunity, conditional on lack of initiation/selection of transmission and observance of statutory due diligence and take-down upon receiving actual knowledge (*Shreya Singhal v. Union of India* (2015) 5 SCC 1).

### 3.4 The Constitution of India (`IND-CONST-1950`)
1. **Article 330A Insertion (`REL-CONST-ART330A-INSERTION`):**
   - **Action:** Insertion by Constitution (One Hundred and Sixth Amendment) Act, 2023 (*Nari Shakti Vandan Adhiniyam*), effective 2023-09-28.
   - **Prior Law:** No reservation of seats for women existed in the House of the People (Lok Sabha).
   - **Amended Law:** Mandates reservation of one-third of total seats in the Lok Sabha for women, including one-third of seats reserved for Scheduled Castes and Scheduled Tribes. Operative post-census delimitation.

### 3.5 Repeal and Savings Transitions
1. **IPC 1860 Repeal by BNS 2023 Section 358 (`REL-IPC-REPEAL-SAVINGS`):**
   - **Action:** Repeal with explicit statutory savings effective 2024-07-01 (S.O. 849(E)).
   - **Savings Mechanism:** Substantive criminal liability for offences committed prior to 1 July 2024 is preserved under Section 358(2) of BNS read with Article 20(1) of the Constitution (*ex post facto* protection).
2. **CPA 1986 Repeal by CPA 2019 Section 107 (`REL-CPA-REPEAL-SAVINGS`):**
   - **Action:** Repeal with statutory savings effective 2020-07-20 (S.O. 2351(E)).
   - **Savings Mechanism:** Pending complaints filed before District Forums, State Commissions, or NCDRC continue under the 1986 regime under Section 107(2), while new causes of action and proceedings fall under the 2019 regime (including CCPA and product liability).

---

## 4. Machine-Readable Export and Integration

The complete amendment relationship graph is serialized in `data/08_corpus/amendment_relationships.json`. The `AmendmentHistoryManager` class provides programmatic methods:
- `get_amendments_for_act(act_id)`: Retrieve all modifications targeting an Act.
- `get_amendments_for_provision(act_id, provision)`: Retrieve modifications targeting a provision (e.g. "Section 10").
- `export_json(path)` and `load_json(path)`: Full serializability and offline reproduction.

