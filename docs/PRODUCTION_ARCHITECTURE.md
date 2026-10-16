# LEGALMITRA: PRODUCTION & STAGING ARCHITECTURE

## 1. System Overview

LegalMitra is a source-grounded Indian Legal Intelligence Assistant. It bridges authentic Indian statutory texts (Acts of Parliament, Gazette Notifications) and landmark judicial rulings (Supreme Court of India, High Courts) with modern conversational AI, adhering strictly to evidential boundaries.

```
                           +-------------------------------------+
                           |      User Browser / Client          |
                           |   Constitutional Modernism UI       |
                           |  (Landing Page `/` & Chat `/chat`)  |
                           +------------------+------------------+
                                              | HTTP / REST
                                              v
                           +-------------------------------------+
                           |      LegalMitra FastAPI Service     |
                           |   (Security Headers, CORS, Routes)  |
                           +--------+-------------------+--------+
                                    |                   |
               +--------------------+                   +--------------------+
               |                                                             |
               v                                                             v
+-------------------------------+                             +-------------------------------+
|  ConversationStore (SQLite)   |                             |    LegalRAGEngine (Python)    |
|  - `data/conversations.db`    |                             |  - Evidential Grounding Rules |
|  - Sessions & Messages        |                             |  - Authority Categorization   |
|  - Evaluator Feedback         |                             |  - Temporal Boundary Checks   |
+-------------------------------+                             +---------------+---------------+
                                                                              |
                                                      +-----------------------+-----------------------+
                                                      |                                               |
                                                      v                                               v
                                      +-------------------------------+               +-------------------------------+
                                      |   LegalKnowledgeBase (SQLite) |               |      NVIDIA NIM / Llama       |
                                      |  - `data/legalmitra_kb.db`    |               |  - LLM Inference Provider     |
                                      |  - 1,149 Indexed Provisions   |               |  - Strict Grounding Prompts   |
                                      |  - FTS5 Full-Text Search      |               |  - Model Temperature = 0.0    |
                                      +-------------------------------+               +-------------------------------+
```

---

## 2. Key Architecture Principles

1. **Separation of Concerns**:
   - The verified Indian legal knowledge base (`data/legalmitra_kb.db`) is read-only during inference and strictly separated from user conversation sessions (`data/conversations.db`).
   - Private user queries and sessions never modify the legal dataset or the frozen review pilot.

2. **Source-Grounded Answering & Evidential Boundaries**:
   - Every legal statement is synthesized from retrieved evidence chunks containing verbatim text, authority levels, and commencement metadata.
   - If evidence is missing or ambiguous, the engine produces a structured cautious response and prompts for clarifying facts rather than hallucinating statutory provisions.

3. **Temporal-Law Awareness**:
   - The engine validates commencement status (e.g., BNSS July 1, 2024 commencement via S.O. 848(E); DPDP 2023 phased enforcement vs. Section 43A IT Act).
   - Provisions are flagged as either operative or uncommenced relative to the legal-as-of date.

4. **Security & Credential Isolation**:
   - Model provider keys (NVIDIA NIM API key) and system tokens (Stitch API key) reside solely in environment variables and are never bundled into client JS or exposed via API payloads.
   - Security headers (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`) are injected by FastAPI middleware.

