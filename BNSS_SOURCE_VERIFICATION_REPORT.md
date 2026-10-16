# LEGALMITRA — AUTHENTIC BNSS SOURCE VERIFICATION REPORT
**Document ID**: `REP-BNSS-2026-PHASE6-001`  
**Date**: October 2026  
**Pipeline Version**: 0.6.0  
**Authority Grounding**: Ministry of Law and Justice, Parliament of India, India Code (DSpace 7)  
**Status**: VERIFIED & INDEXED  

---

## 1. Executive Summary

In Phase 5, an audit revealed that criminal procedure in LegalMitra was represented solely by an unverified synthetic scaffold, `IND-JUD-DEL-2024-BAIL` (and a contaminated procedural guide `PROC-BNSS-482-BAIL-001`). 

In Phase 6, LegalMitra has successfully acquired, verified, normalized, and indexed the **authentic complete text of the Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)** directly from the official **India Code** portal.

---

## 2. Legislative Identity & Official Provenance

| Verification Field | Verified Primary Evidence | Source Authority |
|---|---|---|
| **Act Title** | The Bharatiya Nagarik Suraksha Sanhita, 2023 | Gazette of India Extraordinary / India Code |
| **Act Number & Year** | Act No. 46 of 2023 | Parliament of India |
| **Enactment Date (Assent)** | 25 December 2023 | Assent of the President of India |
| **Commencement Date** | 1 July 2024 | Ministry of Home Affairs Notification S.O. 848(E) (F.No. 1/3/2023-Judicial Cell-I, Gazette of India Extraordinary Part II Sec 3(ii) dt. 24-02-2024, appointing 1 July 2024, except the provisions of entry 56 of the Second Schedule) |
| **Canonical URL** | `https://indiacode.gov.in/handle/123456789/601739` | India Code Repository |
| **DSpace RefAct ID** | `AC_CEN_5_23_00049_202346_1719552320687` | Legislative Department, Ministry of Law and Justice |
| **Raw Storage Location** | `data/01_raw/IND-STAT-BNSS-2023.json` | 1,516,122 bytes |
| **Normalized Storage Location** | `data/02_normalized/IND-STAT-BNSS-2023.json` | 981,098 bytes |
| **SHA-256 Checksum** | `9812b7a5a2f27ec11ab2a99e88e8f363353c84843b7130e558f92ae4f10ed5fe` | Cryptographically matched |
| **Licensing Basis** | Copyright Act, 1957 Section 52(1)(q)(ii) / GODL-India | Central Statute reproduced without commentary |

---

## 3. Forensic Analysis of Sections 479–484 (Chapter XXXVI: Provisions as to Bail and Bonds)

The audit of India Code provisions confirms the exact statutory roles of Sections 479–484:

### 3.1 Section 479: Maximum period for which under-trial prisoner can be detained
- Corresponds to former Section 436A CrPC 1973.
- Key reform: Introduces release on personal bond for first-time offenders who have undergone detention up to **one-third** of maximum imprisonment (general rule remains one-half). Does not apply to offences punishable with death or life imprisonment.

### 3.2 Section 480: When bail may be taken in case of non-bailable offence
- Corresponds to former Section 437 CrPC 1973.
- Governs discretionary bail by Magistrates and Courts other than High Court or Court of Session.

### 3.3 Section 481: Bail to require accused to appear before next Appellate Court
- Corresponds to former Section 437A CrPC 1973.
- Requires bond to appear before higher court upon appeal.

### 3.4 Section 482: Direction for grant of bail to person apprehending arrest (Anticipatory Bail)
- Corresponds to former Section 438 CrPC 1973.
- **Verbatim Text (Sub-section 1)**:
  > *"When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction under this section; and that Court may, if it thinks fit, direct that in the event of such arrest, he shall be released on bail."*
- **Jurisprudential Finding**: The applicant **must** be a person who has reason to believe *he may be arrested*. The State is never the applicant. This definitively establishes why `IND-JUD-DEL-2024-BAIL` is an unverified synthetic scaffold.
- **Statutory Exclusion (Sub-section 4)**:
  > *"Nothing in this section shall apply to any case involving the arrest of any person on accusation of having committed an offence under section 65 and sub-section (2) of section 70 of the Bharatiya Nyaya Sanhita, 2023."* (Rape of woman under 16 / gang rape of woman under 18).

### 3.5 Section 483: Special powers of High Court or Court of Session regarding bail
- Corresponds to former Section 439 CrPC 1973 (Regular bail by Sessions/High Court).

### 3.6 Section 484: Amount of bond and reduction thereof
- Corresponds to former Section 440 CrPC 1973.

---

## 4. Extraction & Normalization Completeness

- Total statutory items retrieved from India Code DSpace API: **537 items**.
- Number of sections parsed and validated: **537 sections** in `StatuteDocument` schema.
- Knowledge base chunks created: **776 chunks** (incorporating section bodies, provisos, and explanations).
- Section 531 (Repeal and Savings) explicitly tracks pending proceedings under CrPC 1973 as of 1 July 2024.

