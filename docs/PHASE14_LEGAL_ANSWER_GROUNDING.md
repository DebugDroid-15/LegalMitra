# LegalMitra Grounded Legal Answer Generation Specification

**System Architecture Specification — Phase 14H**  
**Version:** 1.0.0  
**Engine Implementation:** `legalmitra/rag/engine.py`  
**Classification:** Evidence Grounding, Temporal Safety & Absence-of-Evidence Abstention

---

## 1. Principles of Legal Grounding

Legal responses in LegalMitra must strictly reflect verifiable law:
1. **Verbatim Traceability:** Every factual or legal assertion must directly link to a retrieved statutory provision (`CitedEvidence`) or reported judicial paragraph.
2. **Mandatory Citation Verification:** The engine extracts and cross-validates citations against the retrieved chunk IDs. Hallucinated section numbers or fabricated case citations are strictly prohibited.
3. **Absence-of-Evidence Abstention:** When no matching authoritative sources are found in `legalmitra_kb.db`, the system immediately abstains:
   > *"The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law. No relevant provisions or precedents matching this query were located in the verified LegalMitra Knowledge Base."*
4. **Temporal Fact Prompts:** If a user asks a general criminal law question without stating when the event occurred, the engine issues a missing-facts prompt highlighting the 1 July 2024 transition between IPC/CrPC and BNS/BNSS.
5. **Advocate Escalation Boundary:** Responses clearly remind users that automated legal information does not replace individualized counsel from a licensed advocate enrolled with a State Bar Council.

---

## 2. Distinction Between Evidentiary Tiers

To prevent confusion between legislative mandates and judicial interpretation, the engine categorizes evidence:
- **Binding Authorities:** Central Acts, State Enactments, and Supreme Court rulings.
- **Persuasive Authorities:** High Court rulings outside territorial jurisdiction, Law Commission recommendations, and draft rules.
- **Unverified Scaffolds:** Strictly quarantined and barred from candidate answer generation.

