# LegalMitra — Phase 38: Indian Judicial System Ontology

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Overview

This document specifies the comprehensive machine-readable ontology of the Indian Judicial System designed, implemented, and validated in LegalMitra Phase 38. The ontology models the integrated judicial hierarchy from the Supreme Court of India down to district and subordinate courts, specialized and administrative tribunals, the military justice framework, and pre-independence historical judicial archives.

The ontology is implemented in `legalmitra/judicial/judicial_ontology.py` and serialized to `data/21_judicial_infrastructure/court_and_tribunal_registry.json`.

---

## 2. Institutional Hierarchy Tiers

The Indian judicial universe is structured into six mutually exclusive, hierarchically linked institutional tiers:

| Tier Code | Institutional Classification | Authority & Jurisdiction | Key Representative Institutions |
| :--- | :--- | :--- | :--- |
| `APEX` | Supreme Court of India | Constitutional Apex Court (Part V, Ch IV, Arts. 124–147); Law declared binding under Art. 141 | Supreme Court of India (New Delhi) |
| `HIGH_COURT` | Constitutional High Courts | Constitutional Courts of Record (Part VI, Ch V, Arts. 214–231); Writ & Supervisory powers (Arts. 226, 227) | 25 State/UT High Courts, 16 permanent benches, circuits |
| `DISTRICT_COURT` | District & Subordinate Judiciary | Civil and Criminal trial hierarchy (Arts. 233–237); State Judicial Services; eCourts CIS | District & Sessions, CJM, Civil Judge, JMFC, Gram Nyayalayas |
| `TRIBUNAL` | Specialized & Administrative Tribunals | Statutory tribunals under Arts. 323A, 323B, and sector statutes | CAT, NCLAT, NCLT, NGT, ITAT, CESTAT, TDSAT, APTEL, DRAT/DRT |
| `MILITARY_JUSTICE` | Military Justice & Armed Forces | Armed Forces Tribunal Act 2007; Army, Navy, Air Force Acts; Courts-Martial | Armed Forces Tribunal (Principal & 10 Regional Benches), GCM/DCM/SGCM/SCM |
| `HISTORICAL_ARCHIVE` | Pre-Independence Judicial Archives | Historical predecessor courts prior to January 28, 1950 | Federal Court of India (1937–50), Privy Council (1833–1949), Presidency Supreme Courts |

---

## 3. Apex Court Architecture: Supreme Court of India

- **Identifier:** `IND-SC`
- **Seat:** New Delhi (Tilak Marg)
- **Inauguration:** January 28, 1950
- **Constitutional Mandate:** Articles 124 to 147
- **Jurisdiction Types:**
  - Original Jurisdiction (Article 131: disputes between Union and States or between States)
  - Writ Jurisdiction (Article 32: enforcement of Fundamental Rights)
  - Appellate Jurisdiction:
    - Constitutional appeals (Article 132)
    - Civil appeals (Article 133)
    - Criminal appeals (Article 134)
    - Special Leave Petitions (Article 136)
  - Advisory Jurisdiction (Article 143: Presidential references)
  - Review Jurisdiction (Article 137) and Curative Jurisdiction (*Rupa Ashok Hurra*)
  - Complete Justice (Article 142)
  - Binding Precedent (Article 141)
- **Authoritative Law Reporter:** Supreme Court Reports (SCR)
- **Neutral Citation:** Supported (e.g., `2023 INSC 101`)

---

## 4. Constitutional High Courts (25 High Courts)

All 25 High Courts are fully catalogued with geographic jurisdictions, principal seats, permanent benches, circuit benches, establishment dates, and historical predecessors:

1. **High Court of Judicature at Allahabad (`IND-HC-ALL`)**: Prayagraj; Lucknow Bench; Est. 1866; Predecessor: High Court of Judicature for North-Western Provinces at Agra.
2. **High Court of Andhra Pradesh (`IND-HC-AND`)**: Amaravati; Est. 2019 (bifurcation under AP Reorganisation Act 2014); Predecessor: High Court of Judicature at Hyderabad.
3. **High Court of Judicature at Bombay (`IND-HC-BOM`)**: Mumbai; Benches: Nagpur, Aurangabad, Panaji (Goa); Est. 1862; Predecessor: Supreme Court of Bombay & Sadar Diwani/Faujdari Adalat.
4. **Calcutta High Court (`IND-HC-CAL`)**: Kolkata; Circuit Benches: Jalpaiguri, Port Blair (Andaman & Nicobar Islands); Est. 1862; Predecessor: Supreme Court of Judicature at Fort William & Sadar Adalat.
5. **High Court of Chhattisgarh (`IND-HC-CHH`)**: Bilaspur; Est. 2000.
6. **High Court of Delhi (`IND-HC-DEL`)**: New Delhi; Est. 1966; Predecessor: Circuit Bench of High Court of Punjab at Delhi.
7. **Gauhati High Court (`IND-HC-GAU`)**: Guwahati; Benches: Kohima (Nagaland), Aizawl (Mizoram), Itanagar (Arunachal Pradesh); Est. 1948.
8. **High Court of Gujarat (`IND-HC-GUJ`)**: Ahmedabad; Est. 1960.
9. **High Court of Himachal Pradesh (`IND-HC-HP`)**: Shimla; Est. 1971.
10. **High Court of Jammu & Kashmir and Ladakh (`IND-HC-JK`)**: Srinagar and Jammu; Est. 1928.
11. **High Court of Jharkhand (`IND-HC-JHK`)**: Ranchi; Est. 2000.
12. **High Court of Karnataka (`IND-HC-KAR`)**: Bengaluru; Benches: Dharwad, Kalaburagi; Est. 1884.
13. **High Court of Kerala (`IND-HC-KER`)**: Kochi; Est. 1956; Predecessor: High Court of Travancore-Cochin.
14. **High Court of Madhya Pradesh (`IND-HC-MP`)**: Jabalpur; Benches: Gwalior, Indore; Est. 1956; Predecessor: Nagpur High Court.
15. **High Court of Judicature at Madras (`IND-HC-MAD`)**: Chennai; Madurai Bench; Est. 1862; Predecessor: Supreme Court of Madras & Sadar Adalat.
16. **High Court of Manipur (`IND-HC-MAN`)**: Imphal; Est. 2013.
17. **High Court of Meghalaya (`IND-HC-MEG`)**: Shillong; Est. 2013.
18. **Orissa High Court (`IND-HC-ORI`)**: Cuttack; Est. 1948.
19. **High Court of Judicature at Patna (`IND-HC-PAT`)**: Patna; Est. 1916.
20. **High Court of Punjab and Haryana (`IND-HC-PNH`)**: Chandigarh; Est. 1947; Predecessor: High Court of Judicature at Lahore (1919) / Chief Court of the Punjab.
21. **High Court of Judicature for Rajasthan (`IND-HC-RAJ`)**: Jodhpur; Jaipur Bench; Est. 1949.
22. **High Court of Sikkim (`IND-HC-SIK`)**: Gangtok; Est. 1975.
23. **High Court for the State of Telangana (`IND-HC-TEL`)**: Hyderabad; Est. 2019.
24. **High Court of Tripura (`IND-HC-TRI`)**: Agartala; Est. 2013.
25. **High Court of Uttarakhand (`IND-HC-UTT`)**: Nainital; Est. 2000.

---

## 5. Subordinate & District Judicial Hierarchy

Governed under Chapter VI of Part VI of the Constitution (Articles 233 to 237) and State Judicial Services:
- **District and Sessions Judge**: Principal civil and criminal court of original and appellate jurisdiction in the district.
- **Additional District and Sessions Judge**: Exercising concurrent jurisdiction as assigned by District Judge.
- **Chief Judicial Magistrate (CJM) / Chief Metropolitan Magistrate (CMM)**: Trial of non-capital offences punishable up to 7 years.
- **Civil Judge (Senior Division) / Subordinate Judge**: Unlimited pecuniary jurisdiction in civil suits.
- **Judicial Magistrate First Class (JMFC) / Metropolitan Magistrate (MM)**: Offences punishable up to 3 years imprisonment or fine up to statutory ceiling.
- **Civil Judge (Junior Division) / Munsif Court**: Civil suits within local pecuniary thresholds.
- **Gram Nyayalayas**: Rural grassroots adjudication under the Gram Nyayalayas Act 2008.

---

## 6. Predecessor Linkage and Invariance

The ontology maintains rigorous genealogical linking:
- `get_predecessor_chain("IND-SC")` resolves to `[HIST-FED-COURT, HIST-PRIVY-COUNCIL]`.
- `get_predecessor_chain("IND-HC-BOM")` resolves to `[HIST-SC-BOMBAY, HIST-SADAR-BOM]`.
- No orphan courts or broken parent links exist in the validated catalog.
