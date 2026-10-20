# PHASE 54: PRECEDENT & STATUTORY CONFLICT HANDLING

**Project:** LegalMitra  
**Component:** `legalmitra.caselaw.knowledge_graph`, `legalmitra.temporal.engine`  
**Phase:** 54  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Conflict Taxonomy

LegalMitra classifies legal conflicts into four operational categories:

1. **Temporal Statutory Version Conflict**:
   - Difference between historic wording and amended text. Handled via point-in-time applicability resolution.
2. **Direct Precedent Overruling**:
   - Prior decision declared no longer good law by larger bench or constitutional bench. Automatically detected via `OVERRULES` edges.
3. **Unresolved Co-Equal Bench Split**:
   - Conflicting rulings by identical bench strengths of the Supreme Court. The system abstains from selecting a single winner and reports both authorities with an explicit split warning.
4. **Inter-High Court Territorial Conflict**:
   - Divergent High Court interpretations where no Supreme Court ruling exists. Resolved by evaluating the query's forum jurisdiction. If forum is neutral/national, both views are presented as persuasive.

---

## 2. Safe Abstention & Warning Protocol

When an unresolved conflict is detected:
- The orchestrator appends an `authority_resolution_traces` entry with status `UNRESOLVED_CO_EQUAL_SPLIT` or `INTER_HIGH_COURT_SPLIT`.
- Claim validation enforces `PRECEDENT_STATUS_UNCERTAIN` or `PARTIALLY_SUPPORTED`.
- RAG generation issues an evidence disclosure warning highlighting the split and citing both authoritative decisions.
