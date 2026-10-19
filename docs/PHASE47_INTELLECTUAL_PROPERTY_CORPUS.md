# PHASE 47: INTELLECTUAL PROPERTY CORPUS SPECIFICATION

**Project:** LegalMitra  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 19, 2026  

---

## 1. Executive Overview

Phase 47 ingests and structures India's foundational Intellectual Property statutory suite:
1. **The Copyright Act, 1957 (Act No. 14 of 1957)**: Enacted 04.06.1957; commenced 21.01.1958.
2. **The Patents Act, 1970 (Act No. 39 of 1970)**: Enacted 19.09.1970; commenced 20.04.1972.
3. **The Trade Marks Act, 1999 (Act No. 47 of 1999)**: Enacted 30.12.1999; commenced 15.09.2003.

All three instruments have been ingested under `LEGALMITRA-PROVENANCE-SPEC-V2` with official gazette verification, historical enactment texts, consolidated amendment tracks, and passage-level precedent links.

---

## 2. Acquired Statutory Instruments

| Statute Identifier | Official Short Title | Act No. / Year | Enactment / Commenced | Key Amendments Incorporated | Official Gazette Ref | Ingestion SHA-256 |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `IND-STAT-COPYRIGHT-1957` | The Copyright Act, 1957 | Act 14 of 1957 | 04.06.1957 / 21.01.1958 | 1983, 1984, 1992, 1994, 1999, **2012 (Act 27 of 2012)** | S.R.O. 269; S.O. 1393(E) | `507fa483...` |
| `IND-STAT-PATENTS-1970` | The Patents Act, 1970 | Act 39 of 1970 | 19.09.1970 / 20.04.1972 | 1999 (Mailbox), 2002, **2005 (Act 15 of 2005)** | S.O. 290(E); Act 15 of 2005 | `20d20d77...` |
| `IND-STAT-TRADEMARKS-1999` | The Trade Marks Act, 1999 | Act 47 of 1999 | 30.12.1999 / 15.09.2003 | **2010 (Act 40 of 2010 - Madrid Protocol)** | S.O. 1048(E); S.O. 1999(E) | `26e036e1...` |

---

## 3. Statutory Provision Decomposition

### 3.1 Copyright Act, 1957 Anchor Provisions
- **Section 13 (`COP-1957-SEC-13-V1`)**: Subsistence of copyright in original literary, dramatic, musical, and artistic works, cinematograph films, and sound recordings. Standard of originality governed by *Eastern Book Company v. D.B. Modak* (modicum of creativity).
- **Section 52 (`COP-1957-SEC-52-V1` & `V2`)**: Acts not constituting infringement / Fair Dealing. Pre-2012 limited to private use, research, and criticism. Post-2012 expanded to educational instruction (s.52(1)(i)), accessible formats for disabled persons (s.52(1)(zb)), and digital transient storage.
- **Section 57 (`COP-1957-SEC-57-V1` & `V2`)**: Author's special rights (moral rights of paternity and integrity). 2012 amendment removed expiration restriction, establishing perpetual moral rights enforceable by legal heirs under Section 57(2).

### 3.2 Patents Act, 1970 Anchor Provisions
- **Section 3(d) (`PAT-1970-SEC-3D-V1` & `V2`)**: Pre-2005 covered new use of known substance. Post-2005 amended via Act 15 of 2005 to mandate demonstrable enhancement of **therapeutic efficacy** for salts, esters, polymorphs, and derivatives of known chemical entities (*Novartis AG*).
- **Section 5 (Repealed)**: Deletion of prohibition against product patents for chemical, pharmaceutical, and food substances effective 01.01.2005.
- **Section 84 (`PAT-1970-SEC-84-V1`)**: Compulsory licenses available after 3 years from grant if reasonable public requirements not satisfied, priced unaffordably, or not worked in India (*Bayer v. Natco*).

### 3.3 Trade Marks Act, 1999 Anchor Provisions
- **Section 9 (`TM-1999-SEC-9-V1`)**: Absolute grounds for refusal (devoid of distinctiveness, descriptive, generic).
- **Section 11 (`TM-1999-SEC-11-V1`)**: Relative grounds for refusal (identity/similarity with earlier marks causing public confusion).
- **Section 29 (`TM-1999-SEC-29-V1`)**: Infringement through deceptive similarity in the course of trade; heightened threshold for pharmaceuticals per *Cadila Health Care*.

---

## 4. Verification and Cross-Referencing

All statutory provisions have been extracted from primary India Code and official Gazette PDFs, hashed via SHA-256, and linked with valid half-open intervals $[valid\_from, valid\_until)$ in `provision_provenance_manifest.json`.
