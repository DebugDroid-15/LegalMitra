# Phase 29: Coverage Transparency & User-Facing Metadata Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. Transparency Principle

In legal research, silence or unwarranted assumptions about an unindexed jurisdiction create severe malpractice risk. LegalMitra enforces strict **coverage transparency**: if a user queries a state or high court jurisdiction that is not yet verified or indexed, the system must not attempt to substitute a central statute or guess state provisions; it must provide an affirmative, informative abstention.

---

## 2. In-System Abstention & Boundary Enforcement

LegalMitra's `LegalRAGEngine` enforces state and territorial boundaries through multi-tier verification:

1. **Explicit Jurisdiction Filters:** When queries target an unindexed jurisdiction (e.g. `IN-KA`, `IN-WB`, `IN-TN`), the retrieval engine searches within that territorial boundary.
2. **Relevance Gating:** If no authentic chunks exist for the specified jurisdiction, the engine intercepts the response before dispatching to an LLM, returning:
   > *"The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law. No relevant provisions or precedents matching this query were located in the verified LegalMitra Knowledge Base."*
3. **Missing Facts Guidance:** The engine actively prompts the user with clarifying instructions:
   > *"Please specify the applicable Act name, section number, or specific High Court jurisdiction."*

---

## 3. UI and API Metadata Transparency

The REST API and Web Interface communicate coverage status:
- Active jurisdictions (Central, Delhi, Maharashtra) return verified badges with authority classifications (`binding_statute`, `persuasive_precedent`).
- Unindexed states clearly report `evidence_sufficiency: insufficient` and `is_grounded: true` with zero hallucinated tokens.
- All 36 sub-national jurisdictions are exposed via `data/09_national_corpus/jurisdiction_coverage_matrix.json`, enabling front-end search bars and filters to dynamically indicate coverage maturity.
