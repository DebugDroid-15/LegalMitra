# LEGALMITRA — PHASE 16D: STATE & UNION TERRITORY LEGISLATION REGISTRY REPORT

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

India's constitutional legal order distributes legislative competence between the Union Parliament (List I) and State Legislatures (List II), with shared jurisdiction over Concurrent subjects (List III) under Article 246 and the Seventh Schedule.

Prior to Phase 16, LegalMitra primarily cataloged Central statutory instruments. In Phase 16D, a comprehensive **State and Union Territory Legislation Registry** was constructed covering all **28 States and 8 Union Territories** (36 sub-national jurisdictions).

The registry documents canonical India Code portals, official state gazette printing directories, responsible state law ministries, priority tiering, and active pilot coverage.

---

## 2. Jurisdiction Registry Structure & Coverage

The registry is formalized in `legalmitra/corpus/state_registry.py` and exported to `data/08_corpus/state_ut_registry.json`.

### Geographic Breakdown:
- **28 States**: Andhra Pradesh (`IN-AP`), Arunachal Pradesh (`IN-AR`), Assam (`IN-AS`), Bihar (`IN-BR`), Chhattisgarh (`IN-CT`), Goa (`IN-GA`), Gujarat (`IN-GJ`), Haryana (`IN-HR`), Himachal Pradesh (`IN-HP`), Jharkhand (`IN-JH`), Karnataka (`IN-KA`), Kerala (`IN-KL`), Madhya Pradesh (`IN-MP`), Maharashtra (`IN-MH`), Manipur (`IN-MN`), Meghalaya (`IN-ML`), Mizoram (`IN-MZ`), Nagaland (`IN-NL`), Odisha (`IN-OR`), Punjab (`IN-PB`), Rajasthan (`IN-RJ`), Sikkim (`IN-SK`), Tamil Nadu (`IN-TN`), Telangana (`IN-TG`), Tripura (`IN-TR`), Uttar Pradesh (`IN-UP`), Uttarakhand (`IN-UT`), West Bengal (`IN-WB`).
- **8 Union Territories**: Andaman & Nicobar (`IN-AN`), Chandigarh (`IN-CH`), Dadra & Nagar Haveli and Daman & Diu (`IN-DH`), National Capital Territory of Delhi (`IN-DL`), Jammu & Kashmir (`IN-JK`), Ladakh (`IN-LA`), Lakshadweep (`IN-LD`), Puducherry (`IN-PY`).

### Priority Tiering:
1. **Phase 16 Core Ingestion**:
   - **NCT of Delhi (`IN-DL`)**: High-density urban litigation, tenancy disputes, and police powers. Active in pilot.
   - **State of Maharashtra (`IN-MH`)**: Commercial hub, Bombay High Court jurisprudence, Rent Control Act, and Maharashtra Police Act. Active in pilot.
2. **Tier 2 High-Volume Jurisdictions**:
   - Karnataka (`IN-KA`), Tamil Nadu (`IN-TN`), Uttar Pradesh (`IN-UP`), West Bengal (`IN-WB`), Gujarat (`IN-GJ`), Telangana (`IN-TG`), Kerala (`IN-KL`), Punjab (`IN-PB`), Haryana (`IN-HR`), Rajasthan (`IN-RJ`), Bihar (`IN-BR`), Madhya Pradesh (`IN-MP`), Odisha (`IN-OR`), Assam (`IN-AS`), Jammu & Kashmir (`IN-JK`).
3. **Tier 3 Targeted Jurisdictions**:
   - Remaining Northeastern states, Himalayan states, and smaller Union Territories.

---

## 3. Data Integrity & Compliance

- Registry schema validates with Pydantic v2.
- JSON artifact generated: `data/08_corpus/state_ut_registry.json`.
- Zero impact on frozen pilot review artifacts.

