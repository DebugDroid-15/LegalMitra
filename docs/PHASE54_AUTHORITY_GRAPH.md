# PHASE 54: CANONICAL LEGAL-AUTHORITY GRAPH SPECIFICATION

**Project:** LegalMitra  
**Component:** `legalmitra.caselaw.knowledge_graph`  
**Phase:** 54  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Executive Summary

Phase 54 establishes the Canonical Legal-Authority Graph (`LegalKnowledgeGraph`), transforming LegalMitra's case-law citation network into an auditable, multi-entity authority graph. The graph supports bidirectional relationship tracking across judgments, statutory provisions, constitutional articles, and delegated rules with temporal interval validity and endpoint referential integrity enforcement.

---

## 2. Graph Schema & Node/Edge Architecture

### 2.1 Node Entity Types
The graph models five primary node types:
1. `CaseLaw`: Judicial judgments from Supreme Court, High Courts, and Tribunals (e.g., `SC-1973-C1`, `SC-2020-C1`).
2. `Statute`: Enacted primary legislation (e.g., `IND-STAT-HSA-1956`, `IND-STAT-IBC-2016`).
3. `StatutoryProvision`: Granular sections/articles (e.g., `HSA-SEC-6`, `IT-SEC-66A`, `DPDP-SEC-1`).
4. `ConstitutionalArticle`: Articles of the Constitution of India (e.g., `CONST-ART-14`, `CONST-ART-21`, `CONST-ART-141`).
5. `DelegatedRule`: Rules and regulations formulated under statutory authority.

### 2.2 Edge Relationship Taxonomy & Temporal Intervals
Every edge contains explicit temporal validity intervals (`valid_from`, `valid_until`) and relationship semantics:
- `CITES`: General citation between judicial authorities.
- `OVERRULES`: Higher bench/court extinguishing the precedential validity of a prior ruling (`valid_from` = decision date, `is_terminal` = True).
- `DISTINGUISHES`: Authority restricting the application of a prior ruling to specific factual matrices.
- `UPHOLDS` / `AFFIRMS`: Bench affirming a previous line of authority.
- `INTERPRETS`: Judicial decision defining or qualifying the operative meaning of a statutory provision.
- `STRIKES_DOWN`: Judicial authority invalidating a statutory provision on constitutional grounds (`valid_from` = strike-down date).

---

## 3. Referential Integrity & Validation (`validate_graph_integrity`)

To prevent dangling relationships, orphan nodes, and temporal anomalies, `LegalKnowledgeGraph.validate_graph_integrity()` implements strict graph-theoretic guarantees:

```python
graph = build_default_knowledge_graph()
report = graph.validate_graph_integrity()
assert report["is_valid"] is True
assert report["dangling_edge_count"] == 0
assert report["orphan_node_count"] == 0
```

### Metrics Verified:
- **Total Nodes**: 21+ canonical entities (SC, High Courts, Central Statutes, Granular Sections).
- **Total Edges**: 28+ directed citation and authority edges.
- **Dangling Edges**: 0 (all source and target identifiers resolve to active nodes).
- **Orphan Nodes**: 0 (all registered nodes participate in at least one directional edge).
- **Cycle Detection**: Directed acyclic verification for overruling and hierarchical chains.

---

## 4. Production Integration

The authority graph is integrated directly into `UnifiedEvidenceOrchestrator.orchestrate_evidence()`, allowing the query pipeline to resolve precedent status, detect split benches, and trace overruling events at runtime.
