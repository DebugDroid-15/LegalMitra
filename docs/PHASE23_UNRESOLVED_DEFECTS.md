# LegalMitra Phase 23 Unresolved Defects & Backlog Register
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Defect Classification & Severity Standards

- **Critical:** Blocking releases (0 active).
- **High:** Substantive legal or operational limitation requiring mitigation prior to full production rollout.
- **Medium:** Usability, latency, or edge-case statutory coverage gap.
- **Low:** Cosmetic phrasing or non-critical documentation debt.

---

## 2. Active Defect & Technical Backlog Register

| Defect ID | Severity | Category | Description | Mitigation / Status |
| :--- | :---: | :--- | :--- | :--- |
| **DEF-23-001** | **HIGH** | External LLM Latency & Timeouts | NVIDIA Nemotron API endpoints occasionally experience read timeouts (>60s) during high concurrent traffic. | **Mitigated:** Integrated local extractive grounded fallback in `LegalRAGEngine` to maintain 100% uptime and grounding. |
| **DEF-23-002** | **MEDIUM** | Advocate Review Pending Queue | 40 candidates in Package A and Package B remain pending human advocate review. | **Operational:** Maintained strict NO-GO on fine-tuning; established complete CLI/workflow for advocate import. |
| **DEF-23-003** | **MEDIUM** | State Legislation Depth | While national central acts are well-represented (1,380 chunks), state-level coverage is currently limited to Delhi (11 chunks) and Maharashtra (8 chunks). | **Backlog:** Scheduled for subsequent phase expansion across high-volume litigation states (Uttar Pradesh, Karnataka, West Bengal). |
| **DEF-23-004** | **LOW** | Lexical Ranking Stopwords | BM25 FTS queries without stopword filtering can dilute ranks on long descriptive queries. | **Resolved:** Applied stopword filtering and legal acronym expansion in `runner.py` and `LegalKnowledgeBase`. |

