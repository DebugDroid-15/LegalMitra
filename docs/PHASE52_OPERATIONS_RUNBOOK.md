# PHASE 52: OPERATIONS & CORPUS GOVERNANCE RUNBOOK

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Daily Ingestion & Governance Procedures

1. **Verify Phase 9 Freeze**:
   ```bash
   python scripts/verify_freeze.py
   ```
2. **Audit Review Packages**:
   ```bash
   python scripts/verify_review_packages.py
   ```
3. **Reconcile Corpus Inventory**:
   ```bash
   python -c "from legalmitra.corpus.inventory_reconciler import CorpusInventoryReconciler; CorpusInventoryReconciler().generate_manifest()"
   ```
4. **Audit Source Authenticity & Rights**:
   ```bash
   python -c "from legalmitra.corpus.authenticity import SourceAuthenticityVerifier; SourceAuthenticityVerifier().generate_register()"
   python -c "from legalmitra.corpus.rights import SourceRightsEngine; SourceRightsEngine().generate_registry()"
   ```
5. **Run Multi-Phase Test Suite**:
   ```bash
   pytest tests/test_phase52_source_integrity.py -v
   ```
