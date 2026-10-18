# Phase 35 Source Discovery and Prioritization Results

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Discovery Scope and Methodology

The Phase 35 Discovery Engine (`legalmitra/corpus/source_discovery.py`) catalogs national legal candidates across Central legislation, State Acts, Delegated Legislation, Gazette Notifications, Supreme Court and High Court precedents, and Hindi statutory translations.

Unlike simplistic scrapers that rank documents by file size, LegalMitra prioritizes sources according to a multi-attribute utility function:

$$\text{Priority Score} = W_{\text{importance}} \cdot \text{Category} + W_{\text{lang\_gap}} \cdot \text{LanguageGap} + W_{\text{jur\_gap}} \cdot \text{JurisdictionGap} + W_{\text{rights}} \cdot \text{RightsConfidence} + W_{\text{yield}} \cdot \text{YieldEfficiency}$$

### Scoring Weights:
1. **Category Importance:** Constitutional (30) > Multilingual Statutes (28) > Central Acts / Procedural Codes (25) > Judgments (18–22) > Delegated Rules (15) > Gazettes (12).
2. **Language Gap (Devanagari Hindi):** 30.0 points awarded for authentic Hindi legal text, addressing the 615x token deficit identified in Phase 34.
3. **Jurisdictional Coverage:** Underrepresented states (West Bengal, Tamil Nadu, Uttar Pradesh, Gujarat) receive 18.0 points.
4. **Rights Basis:** 15.0 points for clear statutory public edict exemption under Section 52(1)(q).
5. **Yield Efficiency:** Bounded logarithmic token efficiency bonus (max 10.0 points).

---

## 2. Seed National Discovery Candidates (Workstream B)

Ten high-priority legal candidates were identified, audited against official government portals, and registered in `data/09_national_corpus/discovery_candidates.json`:

| Candidate ID | Official Title | Jurisdiction | Language | Expected Yield | Priority Score | Official Portal |
|---|---|---|---|---|---|---|
| `CAND-HI-BNS-2023` | भारतीय न्याय संहिता, 2023 (BNS Hindi) | IN | hi | ~45,000 tokens | **98.00** | India Code / Legislative Dept |
| `CAND-HI-BNSS-2023` | भारतीय नागरिक सुरक्षा संहिता, 2023 (BNSS Hindi) | IN | hi | ~52,000 tokens | **98.00** | India Code / Legislative Dept |
| `CAND-HI-BSA-2023` | भारतीय साक्ष्य अधिनियम, 2023 (BSA Hindi) | IN | hi | ~25,000 tokens | **93.00** | India Code / Legislative Dept |
| `CAND-DEL-RULES-IT-2021` | Information Technology Intermediary Rules, 2021 | IN | en | ~12,000 tokens | **52.40** | MeitY / Gazette of India |
| `CAND-STATE-WB-LAND-1955` | West Bengal Land Reforms Act, 1955 | IN-WB | en | ~18,000 tokens | **54.60** | WB Legislative Assembly |
| `CAND-STATE-TN-TRANSP-1991` | Tamil Nadu Transparency in Tenders Act, 1998 | IN-TN | en | ~11,000 tokens | **53.20** | TN Government Portal |
| `CAND-JUD-BHC-2024-TELECOM` | Vodafone Idea Ltd v. UOI (Bombay HC 2024) | IN-MH | en | ~15,000 tokens | **46.00** | Bombay HC CIS |
| `CAND-JUD-CAL-2023-ENV` | Green Earth Foundation v. State of WB (Calcutta HC) | IN-WB | en | ~14,000 tokens | **53.80** | Calcutta HC Case Status |
| `CAND-GAZ-COMMENCE-BNS-2024`| Notification S.O. 850(E) - BNS Commencement | IN | en | ~2,500 tokens | **42.50** | Gazette of India (eGazette) |
| `CAND-PROC-DEL-HC-ORIG-2018`| Delhi High Court (Original Side) Rules, 2018 | IN-DL | en | ~22,000 tokens | **54.40** | Delhi HC Rules Portal |

---

## 3. Findings and Prioritization Analysis

1. **Strategic Dominance of Multilingual Codes:** The top 3 ranked documents are the newly enacted criminal codes in authentic Hindi (`BNS`, `BNSS`, `BSA`). Ingesting and clearing these three codes alone will yield approximately **122,000 authentic Devanagari tokens**, multiplying our current Hindi pretraining corpus by over **14x** (from 8,617 to ~130,000 tokens).
2. **Jurisdictional Expansion:** Inclusion of West Bengal (`IN-WB`) and Tamil Nadu (`IN-TN`) statutes and High Court decisions directly remediates the regional bias noted in previous phases, where Central Acts, Delhi High Court, and Bombay High Court represented 94% of judicial citations.
3. **Traceability:** Every candidate URL is mapped to an authoritative government domain (`indiacode.nic.in`, `egazette.gov.in`, `delhihighcourt.nic.in`, `calcuttahighcourt.gov.in`, `meity.gov.in`). No commercial legal portals (e.g. SCC Online, Manupatra) or unauthorized aggregators were registered.
