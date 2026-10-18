# LegalMitra — Phase 38: Court and Tribunal Registry Reference

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Registry Architecture

The Court and Tribunal Registry provides a centralized, authoritative catalog of all judicial and quasi-judicial bodies operating in India. It captures:
- Unique machine identifiers (`IND-SC`, `IND-HC-*`, `IND-TR-*`, `IND-MIL-*`, `HIST-*`)
- Official nomenclatures
- Geographical seat, territorial jurisdiction, and established benches
- Statutory foundations and constitutional articles
- Reporting standards and neutral citation integration

---

## 2. Specialized and Administrative Tribunals

Specialized tribunals adjudicate technical disputes under specific legislative mandates:

### 2.1 Central Administrative Tribunal (CAT)
- **Identifier:** `IND-TR-CAT`
- **Enabling Statute:** Administrative Tribunals Act, 1985 (enacted under Article 323A).
- **Seat:** Principal Bench at New Delhi; 19 Benches nationwide.
- **Jurisdiction:** Adjudication of disputes and complaints with respect to recruitment and conditions of service of persons appointed to public services and posts in connection with the affairs of the Union.
- **Appellate Forum:** High Court Division Bench under Articles 226/227 pursuant to *L. Chandra Kumar v. Union of India* (1997) 3 SCC 261.

### 2.2 National Company Law Appellate Tribunal (NCLAT)
- **Identifier:** `IND-TR-NCLAT`
- **Enabling Statute:** Companies Act, 2013 (Section 410) & Insolvency and Bankruptcy Code, 2016 (Section 61).
- **Seat:** Principal Bench at New Delhi; Chennai Bench.
- **Jurisdiction:** Appellate forum for orders passed by the National Company Law Tribunal (NCLT) and Competition Commission of India (CCI).
- **Appellate Forum:** Direct statutory appeal to the Supreme Court of India under Section 62 IBC / Section 423 Companies Act.

### 2.3 National Company Law Tribunal (NCLT)
- **Identifier:** `IND-TR-NCLT`
- **Enabling Statute:** Companies Act, 2013 (Section 408) & Insolvency and Bankruptcy Code, 2016.
- **Seat:** Principal Bench at New Delhi; 16 Territorial Benches.
- **Jurisdiction:** Corporate insolvency resolution process (CIRP), liquidation, oppression and mismanagement, schemes of arrangement, winding up.

### 2.4 National Green Tribunal (NGT)
- **Identifier:** `IND-TR-NGT`
- **Enabling Statute:** National Green Tribunal Act, 2010.
- **Seat:** Principal Bench at New Delhi; Regional Benches: Bhopal (Central), Pune (Western), Kolkata (Eastern), Chennai (Southern).
- **Jurisdiction:** Civil cases involving substantial questions relating to environment, enforcement of environmental legal rights, compensation for environmental damage.
- **Appellate Forum:** Direct statutory appeal to Supreme Court under Section 22 NGT Act.

### 2.5 Income Tax Appellate Tribunal (ITAT)
- **Identifier:** `IND-TR-ITAT`
- **Enabling Statute:** Income Tax Act, 1961 (Section 252).
- **Seat:** 63 Benches across 27 stations; founded in 1941.
- **Jurisdiction:** Final fact-finding appellate body in direct tax disputes.
- **Appellate Forum:** High Court under Section 260A on substantial questions of law.

### 2.6 Customs, Excise and Service Tax Appellate Tribunal (CESTAT)
- **Identifier:** `IND-TR-CESTAT`
- **Enabling Statute:** Customs Act, 1962 (Section 129).
- **Seat:** Principal Bench at New Delhi; Benches at Mumbai, Kolkata, Chennai, Bengaluru, Ahmedabad, Allahabad, Chandigarh, Hyderabad.
- **Jurisdiction:** Appeals against orders in customs, central excise, and legacy service tax.

### 2.7 Other Specialized Tribunals
- **TDSAT (`IND-TR-TDSAT`)**: Telecom Disputes Settlement and Appellate Tribunal (TRAI Act 1997 / Information Technology Act).
- **APTEL (`IND-TR-APTEL`)**: Appellate Tribunal for Electricity (Electricity Act 2003 / Petroleum and Natural Gas Regulatory Board Act).
- **DRAT (`IND-TR-DRAT`) / DRT (`IND-TR-DRT`)**: Debt Recovery Appellate Tribunals and Tribunals (Recovery of Debts and Bankruptcy Act 1993, SARFAESI Act 2002).
- **NCDRC (`IND-TR-NCDRC`)**: National Consumer Disputes Redressal Commission (Consumer Protection Act 2019).

---

## 3. Data Integrity & Verification

All registered institutions have been cross-verified against official gazettes, court rules, and ministry notifications. No synthetic or fictional tribunal names are present in the registry.
