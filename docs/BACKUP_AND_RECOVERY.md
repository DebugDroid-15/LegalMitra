# LEGALMITRA: BACKUP & DISASTER RECOVERY RUNBOOK

**Target Stores:**
1. `data/legalmitra_kb.db` (Read-only verified statutory and case law knowledge base)
2. `data/conversations.db` (User conversations, sessions, and evaluation feedback)
3. `data/03_generated/` and `data/06_review/` (Frozen pilot dataset and review package)

---

## 1. Backup Procedures

### 1.1 Hot SQLite Backup (Safe during live traffic)
Using SQLite's built-in vacuum/backup API prevents database corruption and lock contention during active conversations:

```bash
# Ensure backup directory exists
mkdir -p backups

# Backup user conversations
sqlite3 data/conversations.db ".backup 'backups/conversations_$(date +%Y%m%d_%H%M%S).db'"

# Backup legal knowledge base
sqlite3 data/legalmitra_kb.db ".backup 'backups/legalmitra_kb_$(date +%Y%m%d_%H%M%S).db'"
```

### 1.2 Frozen Pilot Dataset Verification
The frozen pilot is immutable. Before and after any system maintenance, verify its integrity:
```bash
python scripts/verify_freeze.py
```
If the script outputs `[OK]` for all 6 artifacts and prints their original SHA-256 hashes, the dataset is intact.

---

## 2. Disaster Recovery & Restoration

### Restoring Conversations from Backup:
1. Stop the application server:
   ```bash
   # Terminate run_server.py process
   ```
2. Replace the corrupted or compromised database:
   ```bash
   cp backups/conversations_YYYYMMDD_HHMMSS.db data/conversations.db
   ```
3. Run schema verification:
   ```bash
   python -c "from legalmitra.web.store import ConversationStore; cs = ConversationStore(); print('Loaded conversations:', len(cs.list_conversations('anonymous', limit=10)))"
   ```
4. Restart the service:
   ```bash
   python run_server.py
   ```

### Restoring the Legal Knowledge Base:
1. Copy verified snapshot to `data/legalmitra_kb.db`:
   ```bash
   cp backups/legalmitra_kb_YYYYMMDD_HHMMSS.db data/legalmitra_kb.db
   ```
2. Verify chunk count:
   ```bash
   python -c "from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase; kb = LegalKnowledgeBase(must_exist=True); print('Chunks verified:', kb.count_chunks())"
   # Must report 1,149 chunks
   ```

