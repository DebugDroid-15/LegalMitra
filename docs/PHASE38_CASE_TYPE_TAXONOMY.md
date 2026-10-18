# LegalMitra — Phase 38: Multi-Axis Case Classification Taxonomy

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the multi-axis case classification taxonomy implemented in `legalmitra/judicial/case_taxonomy.py` and exported to `data/21_judicial_infrastructure/case_type_taxonomy.json`. The taxonomy organizes legal disputes along substantive domains, procedural postures, constitutional touchpoints, and remedial categories across 14 legal domains.

---

## 2. 14 Substantive Legal Domains

| Domain Code | Substantive Domain | Core Governing Statutes | Typical Procedural Postures |
| :--- | :--- | :--- | :--- |
| `CONSTITUTIONAL_ADMINISTRATIVE` | Constitutional & Administrative Law | Constitution of India | Writ Petition (Art 32/226), Civil Appeal, Curative |
| `CRIMINAL` | Criminal Law & Procedure | IPC / BNS, CrPC / BNSS, IEA / BSA, POCSO, NDPS | Bail Application, Anticipatory Bail, Criminal Appeal, Quashing Sec 482 |
| `CIVIL_PROPERTY_CONTRACT` | Civil Law, Property & Contract | CPC 1908, Contract Act 1872, TPA 1882, Specific Relief Act | Original Suit, Civil Appeal, Revision Petition |
| `FAMILY_SUCCESSION` | Family, Marriage & Succession | HMA 1955, HSA 1956, SMA 1954, Guardians & Wards Act | Civil Appeal, SLP (Civil), Transfer Petition |
| `COMMERCIAL_CORPORATE_INSOLVENCY` | Commercial, Corporate & IBC | Companies Act 2013, IBC 2016, Arbitration Act 1996, NI Act | Company Petition, Section 11/34 Arbitration, Commercial Appeal |
| `LABOUR_SERVICE` | Labour & Employment Law | Industrial Disputes Act 1947, AT Act 1985, Gratuity Act | Writ Petition (Art 226), Service Appeal |
| `LAND_TENANCY_AGRARIAN` | Land Acquisition & Tenancy | LARR Act 2013, Land Acquisition Act 1894, Rent Control | Civil Appeal, Writ Petition |
| `ENVIRONMENTAL_FOREST` | Environmental & Forest Law | Environment Act 1986, NGT Act 2010, Wildlife Act 1972 | Original Application (NGT), Statutory Appeal |
| `TECHNOLOGY_IP_PRIVACY` | Technology, IP & Cyber Law | IT Act 2000, DPDP Act 2023, Patents, Trademarks, Copyright | Commercial Suit, Writ Petition |
| `TAXATION_CUSTOMS_GST` | Direct & Indirect Taxation | Income Tax Act 1961, CGST Act 2017, Customs Act 1962 | ITAT Appeal, High Court Sec 260A, SLP |
| `EDUCATION_HEALTH` | Education & Public Health | RTE Act 2009, NMC Act 2019, UGC Act 1956 | Writ Petition (Art 226/32) |
| `ELECTION_GOVERNANCE` | Election Law & Democratic Process | Representation of the People Act 1951 | Election Petition, Civil Appeal |
| `HUMAN_RIGHTS_CUSTODIAL` | Human Rights & Custodial Justice | Protection of Human Rights Act 1993, Arts 20-22 | Habeas Corpus, Public Law Compensation Writ |
| `TRANSNATIONAL_ADMIRALTY` | Transnational & Admiralty Law | Admiralty Act 2017, Extradition Act 1962, CPC Sec 44A | Admiralty Suit, Writ Petition |

---

## 3. Procedural Posture Hierarchy

Procedural postures define the statutory vehicle by which the litigation is brought:
1. `BAIL_APPLICATION`: Regular bail under Section 439 CrPC / Section 483 BNSS.
2. `ANTICIPATORY_BAIL`: Pre-arrest bail under Section 438 CrPC / Section 482 BNSS.
3. `SECTION_482_QUASHING`: Inherent powers of High Court to quash FIR, complaint, or charge-sheet under Section 482 CrPC / Section 528 BNSS.
4. `WRIT_PETITION_ARTICLE_32`: Original constitutional writ before the Supreme Court.
5. `WRIT_PETITION_ARTICLE_226`: Original constitutional writ before High Courts.
6. `SPECIAL_LEAVE_PETITION_CIVIL` / `CRIMINAL`: Discretionary appellate petition under Article 136.
7. `CIVIL_APPEAL` / `CRIMINAL_APPEAL`: Regular statutory or constitutional appeals.
8. `COMPANY_PETITION_IBC`: Petitions under Sections 7, 9, or 10 of the Insolvency and Bankruptcy Code.
9. `ARBITRATION_PETITION`: Petitions for appointment of arbitrator (Sec 11) or challenge to arbitral award (Sec 34).
10. `CURATIVE_PETITION`: Final remedial hearing under inherent powers (*Rupa Ashok Hurra* doctrine).

---

## 4. Rule-Based Classification Validation

The classification engine in `CaseTaxonomyManager` combines statutory token recognition, keyword frequency density, and procedural title markers to achieve deterministic, explainable tagging without black-box hallucination.
