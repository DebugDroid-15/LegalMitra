# PHASE 54: PRECEDENT STATUS & HIERARCHY RESOLUTION

**Project:** LegalMitra  
**Component:** `legalmitra.caselaw.knowledge_graph`  
**Phase:** 54  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Constitutional Foundations (Article 141)

Under Article 141 of the Constitution of India, the law declared by the Supreme Court shall be binding on all courts within the territory of India.

However, judicial conflicts arise when:
1. A larger bench overrules or modifies a smaller bench decision.
2. Two benches of equal strength express conflicting views without a reference to a larger bench.
3. High Courts issue divergent rulings across state jurisdictions.

---

## 2. Precedent Conflict Resolution Algorithm

`LegalKnowledgeGraph.resolve_precedent_conflict(citation_a, citation_b, forum_court, context_date)` evaluates:

1. **Court Tier Hierarchy**:
   - Supreme Court strictly overrules/prevails over any High Court decision.
2. **Bench Strength Doctrine**:
   - In the Supreme Court, a larger bench (e.g. 5-Judge Constitution Bench in *Vineeta Sharma*) prevails over a smaller bench (e.g. 2-Judge Bench in *Prakash v. Phulavati*).
3. **Territorial Jurisdiction & High Court Bindingness**:
   - In High Court forum `DELHI_HC`, a ruling from Delhi High Court is binding precedent; a conflicting ruling from Bombay High Court is persuasive only.
4. **Unresolved Co-Equal Bench Splits**:
   - Two 2-Judge benches of the Supreme Court with conflicting holdings without subsequent reference are classified as `UNRESOLVED_CO_EQUAL_SPLIT`.
5. **Inter-High Court Splits**:
   - Rulings between different High Courts absent Supreme Court resolution are classified as `INTER_HIGH_COURT_SPLIT`.

---

## 3. Empirical Test Coverage

The engine is verified through 13 dedicated test assertions in `tests/test_phase54_authority_graph.py`:
- SC vs HC authority preference.
- Bench strength overruling (*Vineeta Sharma* over *Prakash*).
- Forum-specific binding authority resolution.
- Neutral conflict preservation for unresolved splits.
