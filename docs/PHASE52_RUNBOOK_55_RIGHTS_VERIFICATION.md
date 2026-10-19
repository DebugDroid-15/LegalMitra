# RUNBOOK 55: RIGHTS VERIFICATION & TRAINING EXCLUSION ENFORCEMENT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Legal Verification Steps

1. **Check Copyright Act Section 52(1)(q)**:
   - Official Gazette publications, legislative acts, and judicial orders are exempt from copyright infringement for reproduction and reporting.
2. **Enforce Internal Retrieval vs Training Boundary**:
   - Verify that chunks are only accessible via SQLite FTS5 / Vector index for query-time augmentation.
   - Verify that no export script or training pipeline feeds corpus chunks to model weight optimization.
3. **Attribution**:
   - Ensure retrieved passages display appropriate attribution to the official law report or gazette publication.
