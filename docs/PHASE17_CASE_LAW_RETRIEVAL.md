# LEGALMITRA — PHASE 17F: PASSAGE-LEVEL CASE-LAW RETRIEVAL REPORT

**Workspace:** `c:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

Legal AI tools often produce vague or hallucinatory legal propositions by returning high-level document summaries rather than pinpoint citations. 

In Phase 17F, LegalMitra updated `legalmitra/knowledge/knowledge_base.py` and `legalmitra/knowledge/models.py` to enable **passage-level retrieval**, allowing queries to filter by:
1. Exact paragraph number (`paragraph_number=51`, `paragraph_number=21`, etc.)
2. Hierarchy level (`hierarchy_level="ratio"`, `"holding"`, `"paragraph"`)
3. Neutral and official citation string (`case_citation="2020 INSC 452"`, `case_citation="(2020) 7 SCC 1"`)
4. Legal domain and jurisdiction (`jurisdiction="IN-DL"`, `doc_type="judgment"`)

---

## 2. Verification Query Results

### Query 1: Exact Numbered Paragraph Retrieval
- **Query**: `"certificate condition precedent electronic record"`
- **Filter**: `doc_type="judgment"`, `paragraph_number=51`
- **Result Returned**:
  ```
  Chunk ID: IND-JUD-SC-2020-ARJUN-KHOTKAR:PARA:51
  Title:    Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal - Para 51
  Text:     "51. It is clear that the certificate under sub-section (4) is a condition precedent
             to the admissibility of evidence by way of electronic record, as has been held in Anvar P.V.
             Oral evidence in the place of such certificate cannot possibly suffice for the reason
             that Section 65B(4) is a mandatory requirement of the law..."
  ```
  *Precision*: Returns exactly Paragraph 51 without noise.

### Query 2: Neutral Citation Direct Lookup
- **Query**: `""` (Empty query string)
- **Filter**: `case_citation="2020 INSC 452"`
- **Result Returned**:
  ```
  Chunk ID: IND-JUD-SC-2020-ARJUN-KHOTKAR:RATIO
  Title:    Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal - Ratio Decidendi
  Score:    -120.0 (Direct Citation Match Boost)
  ```

### Query 3: Unilateral Arbitrator Ineligibility
- **Query**: `"sole arbitrator unilateral appointment"`
- **Filter**: `doc_type="judgment"`
- **Results Returned**:
  1. `IND-JUD-SC-2020-PERKINS-EASTMAN:HOLDING:1`: Holding on Section 12(5) and Seventh Schedule ineligibility.
  2. `IND-JUD-SC-2020-PERKINS-EASTMAN:RATIO`: Ratio on independence and impartiality.
  3. `IND-JUD-SC-2020-PERKINS-EASTMAN:PARA:21`: Paragraph 21 extending TRF Ltd disqualification.
  4. `IND-JUD-SC-2020-PERKINS-EASTMAN:PARA:16`: Paragraph 16 analyzing TRF Ltd.

### Query 4: Delhi State Commercial Tenancy
- **Query**: `"bona fide requirement commercial premises residential"`
- **Filter**: `doc_type="judgment"`, `jurisdiction="IN-DL"`
- **Results Returned**:
  1. `IND-JUD-SC-2008-SATYAWATI:HOLDING:1`: Striking down discriminatory distinction under Article 14.
  2. `IND-JUD-SC-2008-SATYAWATI:RATIO`: Severance of 'let for residential purposes'.
  3. `IND-JUD-SC-2008-SATYAWATI:PARA:38`: Paragraph 38 finding violation of Article 14.
  4. `IND-JUD-SC-2008-SATYAWATI:PARA:41`: Paragraph 41 modified text of Section 14(1)(e).

---

## 3. Truthful Citation Guarantee

1. Responses generated from judgment passages cite the exact paragraph number (`Paragraph 51`, `Paragraph 21`, `Paragraph 38`).
2. If a legal proposition is derived from ratio decidendi rather than a specific factual paragraph, the hierarchy level explicitly specifies `Ratio Decidendi`.
3. If an issue is framed but not decided in the passage, the system returns `Holding` with supporting paragraphs rather than inventing text.

