# LEGALMITRA — PHASE 50
## Unified Evidence Orchestration & Contrary Authority Retention

**Document ID:** `LM-DOC-PHASE50-EVIDENCE-ORCHESTRATION-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED & TESTED  
**Date:** 2026-10-19  

---

### 1. Multi-Index Retrieval Coordination

The `UnifiedEvidenceOrchestrator` in `legalmitra/orchestration/evidence_orchestrator.py` queries and unifies five independent authoritative registries:
1. **Primary Statutes:** FTS5 BM25 search over `legalmitra_kb.db` combined with registered temporal provision versions.
2. **Delegated Legislation:** Enabling sections linked to verified Central rules (e.g. Patents Rules Form 27, Companies CSR Rules 2014, Copyright Rules 2013).
3. **Constitution Bench Jurisprudence:** Landmark judgments from `constitution_bench_manifest.json` with bench strengths and target constitutional articles.
4. **Judicial Precedents & Contrary Authorities:** Precedent knowledge graph nodes evaluated for interim stays, larger-bench referrals, co-equal High Court splits, and legislative supersessions.
5. **Cross-Statute Definition Taxonomy:** Disambiguation of semantically divergent statutory definitions (e.g. *workman* under IDA vs *employee* under Code on Wages).

### 2. Contrary Authority Retention Mandate

Legal retrieval systems often suffer from "confirmation bias" by suppressing qualifying or conflicting authorities. LegalMitra strictly preserves:
- **Interim Stays:** Labelled as non-binding inter partes interim orders.
- **Larger-Bench Referrals:** Tagged as *sub-judice* with doubts noted.
- **Legislative Supersessions:** Retained with historical context explaining that post-amendment disputes cannot rely on superseded case law.
- **Territorial Conflicts:** High Court co-equal coordinate divergences surfaced with territorial bindingness rules.
