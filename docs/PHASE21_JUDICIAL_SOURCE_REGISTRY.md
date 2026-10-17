# PHASE 21 — NATIONAL JUDICIAL SOURCE REGISTRY
## Inventory of Supreme Court, High Courts, District Courts & Adjudicatory Tribunals

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Overview & Statutory Authority

Article 141 and Article 142 of the Constitution of India establish the Supreme Court of India as the apex court whose law declared is binding upon all courts and tribunals within the territory of India. Article 214 and Articles 226–227 establish the High Courts as constitutional courts of record with plenary writ jurisdiction and supervisory authority over subordinate courts and statutory tribunals.

Phase 21 establishes an official, evidence-grounded **National Judicial Source Registry** comprising **36 verified judicial and adjudicatory repositories** spanning:
1. **Supreme Court of India** (Main portal and official open-access e-SCR).
2. **All 25 High Courts** covering all 28 States and 8 Union Territories.
3. **National Subordinate Court Infrastructure** (eCourts Services and National Judicial Data Grid).
4. **Major National Specialized Tribunals** (NCLAT/NCLT, NGT, CAT, DRAT/DRT, ITAT, NCDRC).

Data files produced:
- `legalmitra/corpus/judicial_registry.py`
- `data/11_judicial_corpus/judicial_source_registry.json`

---

## 2. Ingested High Court & Apex Court Repositories

| Source ID | Institution Name | Tier | Territorial Jurisdiction | Official Search Domain | Neutral Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `IND-SRC-COURT-SCI` | Supreme Court of India | Apex Court | National (`IN`) | `sci.gov.in` | Yes (`YYYY INSC NNN`) |
| `IND-SRC-COURT-ESCR`| Electronic Supreme Court Reports | Apex Court | National (`IN`) | `escr.sci.gov.in` | Yes |
| `IND-SRC-HC-DEL` | High Court of Delhi | High Court | NCT of Delhi (`IN-DL`) | `delhihighcourt.nic.in` | Yes (`YYYY:DHC:NNNN`) |
| `IND-SRC-HC-BOM` | High Court of Judicature at Bombay | High Court | Maharashtra, Goa, DNH & DD | `bombayhighcourt.nic.in` | Yes (`YYYY:BHC-OS:NNN`) |
| `IND-SRC-HC-CAL` | High Court at Calcutta | High Court | West Bengal, A&N Islands | `calcuttahighcourt.gov.in` | Yes |
| `IND-SRC-HC-MAD` | High Court of Judicature at Madras | High Court | Tamil Nadu, Puducherry | `hcmadras.tn.gov.in` | Yes |
| `IND-SRC-HC-ALL` | High Court of Judicature at Allahabad | High Court | Uttar Pradesh (`IN-UP`) | `allahabadhighcourt.in` | Yes |
| `IND-SRC-HC-KAR` | High Court of Karnataka | High Court | Karnataka (`IN-KA`) | `karnatakahiighcourt.kar.nic.in` | Yes |
| `IND-SRC-HC-KER` | High Court of Kerala | High Court | Kerala, Lakshadweep | `hckerala.gov.in` | Yes |
| `IND-SRC-HC-GUJ` | High Court of Gujarat | High Court | Gujarat (`IN-GJ`) | `gujarathighcourt.nic.in` | Yes |
| `IND-SRC-HC-PUN` | High Court of Punjab & Haryana | High Court | Punjab, Haryana, Chandigarh | `highcourtchd.gov.in` | Yes |
| `IND-SRC-HC-RAJ` | High Court of Rajasthan | High Court | Rajasthan (`IN-RJ`) | `hcraj.nic.in` | Yes |
| `IND-SRC-HC-MP` | High Court of Madhya Pradesh | High Court | Madhya Pradesh (`IN-MP`) | `mphc.gov.in` | Yes |
| `IND-SRC-HC-PAT` | High Court of Judicature at Patna | High Court | Bihar (`IN-BR`) | `patnahighcourt.gov.in` | Yes |
| `IND-SRC-HC-ORI` | High Court of Orissa | High Court | Odisha (`IN-OD`) | `orissahighcourt.nic.in` | Yes |
| `IND-SRC-HC-TEL` | High Court of Telangana | High Court | Telangana (`IN-TS`) | `tshc.gov.in` | Yes |
| `IND-SRC-HC-AP` | High Court of Andhra Pradesh | High Court | Andhra Pradesh (`IN-AP`) | `aphc.gov.in` | Yes |
| `IND-SRC-HC-GAU` | Gauhati High Court | High Court | Assam, Nagaland, Mizoram, AP | `ghconline.gov.in` | Yes |
| `IND-SRC-HC-JK` | High Court of J&K and Ladakh | High Court | UT of J&K, UT of Ladakh | `jkhighcourt.nic.in` | Yes |
| `IND-SRC-HC-JHR` | High Court of Jharkhand | High Court | Jharkhand (`IN-JH`) | `jharkhandhighcourt.nic.in` | Yes |
| `IND-SRC-HC-CHG` | High Court of Chhattisgarh | High Court | Chhattisgarh (`IN-CG`) | `highcourt.cg.gov.in` | Yes |
| `IND-SRC-HC-UTK` | High Court of Uttarakhand | High Court | Uttarakhand (`IN-UK`) | `highcourtofuttarakhand.gov.in` | Yes |
| `IND-SRC-HC-HIM` | High Court of Himachal Pradesh | High Court | Himachal Pradesh (`IN-HP`) | `hphighcourt.nic.in` | Yes |
| `IND-SRC-HC-MAN` | High Court of Manipur | High Court | Manipur (`IN-MN`) | `hcmimphal.nic.in` | Yes |
| `IND-SRC-HC-MEG` | High Court of Meghalaya | High Court | Meghalaya (`IN-ML`) | `meghalayahighcourt.nic.in` | Yes |
| `IND-SRC-HC-TRI` | High Court of Tripura | High Court | Tripura (`IN-TR`) | `thc.nic.in` | Yes |
| `IND-SRC-HC-SIK` | High Court of Sikkim | High Court | Sikkim (`IN-SK`) | `highcourtofsikkim.nic.in` | Yes |

---

## 3. Subordinate Courts and Quasi-Judicial Tribunals

- **Subordinate Courts**: `services.ecourts.gov.in` and `njdg.ecourts.gov.in` covering over 3,000 court establishments.
- **Corporate & Insolvency**: National Company Law Appellate Tribunal (`nclat.nic.in`) and National Company Law Tribunal (`nclt.gov.in`).
- **Environmental**: National Green Tribunal (`greentribunal.gov.in`).
- **Service Matters**: Central Administrative Tribunal (`cgat.gov.in`).
- **Debt Recovery**: Debts Recovery Appellate Tribunal (`drat.gov.in`).
- **Taxation**: Income Tax Appellate Tribunal (`itat.gov.in`).
- **Consumer Disputes**: National Consumer Disputes Redressal Commission (`ncdrc.nic.in`).

