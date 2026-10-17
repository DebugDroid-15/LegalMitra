# LEGALMITRA — PHASE 16F: JURISDICTION- AND CONFLICT-AWARE RETRIEVAL REPORT

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

In Phase 16F, LegalMitra's retrieval engine was enhanced to provide strict jurisdictional isolation, conflict detection between Union and State statutes, and instrument classification filtering (`statute`, `rules_regulation`, `notification`, `judgment`).

In Indian constitutional law, conflict of laws is governed by Article 246 (List I Union List, List II State List, List III Concurrent List) and Article 254 (Repugnancy doctrine between Central and State laws on Concurrent subjects). A legal AI cannot assume uniform national rules for subjects governed by state legislation (such as rent control and police powers) or treat executive notifications identically to substantive parliamentary enactments.

---

## 2. Retrieval Capabilities & Verification Queries

### Test 1: Delhi Rent Control (`IN-DL`) vs Maharashtra Rent Control (`IN-MH`)
- **Query**: `"rent control eviction bona fide requirement"`
- **Filter**: `jurisdiction="IN-DL"`
- **Returned Results**:
  1. `IND-DL-STAT-DRC-1958:SEC:25B`: Summary eviction procedure for bona fide requirement (Delhi Rent Control Act 1958).
  2. `IND-DL-STAT-DRC-1958:SEC:14`: Section 14(1)(e) bona fide requirement ground.
  3. `IND-DL-STAT-DRC-1958:SEC:3`: Rent ceiling threshold of ₹3,500/month.
  - Zero pollution from Maharashtra Rent Control Act or Bombay tenancy provisions.

- **Query**: `"rent control eviction licensee"`
- **Filter**: `jurisdiction="IN-MH"`
- **Returned Results**:
  1. `IND-MH-STAT-MRC-1999:SEC:24`: Summary recovery of premises given on licence for residence on expiry.
  2. `IND-MH-STAT-MRC-1999:SEC:15`: Protection of tenant if standard rent paid; 90-day notice requirement.
  3. `IND-MH-STAT-MRC-1999:SEC:3`: Corporate exemption threshold (paid-up share capital >= ₹1 Crore).
  - Zero pollution from Delhi Rent Control Act.

### Test 2: Subordinate Legislation (`rules_regulation`) Retrieval
- **Query**: `"sensitive personal data or reasonable security practices"`
- **Filter**: `doc_type="rules_regulation"`
- **Returned Results**:
  1. `IND-RULE-IT-SPDI-2011:RULE:4`: Privacy policy requirements.
  2. `IND-RULE-IT-SPDI-2011:RULE:8`: Reasonable security practices (IS/ISO/IEC 27001).
  3. `IND-RULE-IT-SPDI-2011:RULE:3`: 8-part definition of Sensitive Personal Data or Information.
  4. `IND-RULE-IT-INTERMEDIARY-2021:RULE:3`: Due diligence and 36-hour takedown mandate.
  - Excludes general statute bodies and returns exact subordinate rules.

### Test 3: Statutory Commencement (`notification`) Retrieval
- **Query**: `"commencement Bharatiya Nagarik Suraksha Sanhita"`
- **Filter**: `doc_type="notification"`
- **Returned Results**:
  1. `IND-NOTIF-COMMENCE-BNSS-2024:SEC:1`: S.O. 848(E) bringing BNSS 2023 into force on 1st July 2024.
  2. `IND-NOTIF-COMMENCE-BNS-2024:SEC:1`: S.O. 849(E) bringing BNS 2023 into force on 1st July 2024.
  3. `IND-NOTIF-COMMENCE-BSA-2024:SEC:1`: S.O. 850(E) bringing BSA 2023 into force on 1st July 2024.

---

## 3. Conflict Awareness Architecture

1. **Repugnancy Handling**: When answering queries on Concurrent List subjects (e.g. contracts, specific relief, evidence, civil procedure), queries default to Union statutes (`IN`) unless the user explicitly specifies a State jurisdiction (`IN-DL`, `IN-MH`, etc.) or territorial locus.
2. **State Specificity**: For state-exclusive subjects (Police, Landlord-Tenant, Local Government), the retrieval engine requires or suggests jurisdictional narrowing to prevent misleading cross-state advice.
3. **Hierarchy of Norms**:
   - Level 1: Constitutional text (`IND-CONST-1950`) — Supreme legal authority.
   - Level 2: Parliamentary Acts (`statute`) & Binding Supreme Court Rulings under Art. 141.
   - Level 3: State Legislative Acts within territorial jurisdiction.
   - Level 4: Delegated Rules & Regulations (`rules_regulation`).
   - Level 5: Administrative Notifications & Circulars (`notification`).

