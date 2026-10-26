# PHASE 62 BACKUP RETENTION AND OPERATIONS
**Module:** `legalmitra.operations.backup_recovery`  
**Policy Name:** Disaster Recovery Point Retention Policy  
**Target Release:** 0.62.0  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Retention Policy Purpose & Principles

Continuous generation of backup snapshots is required for point-in-time disaster recovery. However, unmanaged backup accumulation risks disk exhaustion and operational confusion.

The LegalMitra Backup Retention Policy balances storage efficiency with disaster recovery resilience based on three fundamental principles:
1. **Singleton Preservation Invariant:** A pruning operation must never delete the only existing backup snapshot under any circumstances, even if an operator or automated job specifies `keep_count = 0`.
2. **Metadata Co-Deletion:** Pruning a backup `.db` file must atomically prune its corresponding `.meta.json` sidecar.
3. **Chronological Preservation:** When pruning to $N$ backups, the subsystem preserves the $N$ newest backups based on timestamp parsing, removing older recovery points.

---

## 2. Implementation Specifications

### 2.1 `list_backups()`
Enumerates all `.db` files in the backup directory (excluding temporary `.tmp_part` and `.tmp_restore` files), parses timestamps from filenames, verifies file presence, and returns a list of `BackupManifest` objects ordered from newest to oldest.

### 2.2 `prune_backups(keep_count=5)`
```python
def prune_backups(self, keep_count: int = 5) -> List[str]:
    backups = self.list_backups()
    if len(backups) <= 1:
        # SINGLETON PROTECTION: Never prune if only 1 backup remains
        return []
    
    # Enforce minimum retention of at least 1 backup
    effective_keep = max(1, keep_count)
    if len(backups) <= effective_keep:
        return []
        
    to_delete = backups[effective_keep:]
    deleted = []
    for manifest in to_delete:
        db_path = Path(manifest.backup_file)
        meta_path = db_path.with_name(f"{db_path.name}.meta.json")
        if db_path.exists():
            db_path.unlink()
            deleted.append(str(db_path))
        if meta_path.exists():
            meta_path.unlink()
    return deleted
```

---

## 3. Operational CLI Commands

Operators can manage backup retention using `scripts/backup_kb.py`:

### Listing Available Recovery Points
```bash
$ python scripts/backup_kb.py --list
Available Backups in data/backups:
  [1] legalmitra_kb_20261026T134846_943189Z.db (4,833,280 bytes) - 2026-10-26T13:48:46_943189Z - Chunks: 1515 - Sources: 62 - Valid: True
  [2] legalmitra_kb_20261026T115207Z.db (4,833,280 bytes) - 2026-10-26T11:52:07Z - Chunks: 1515 - Sources: 62 - Valid: True
```

### Pruning Older Recovery Points
```bash
$ python scripts/backup_kb.py --prune 2
Retaining 2 newest backups; evaluating retention...
Pruned 0 older backup artifacts.
```

---

## 4. Edge Cases Tested

| Test Condition | Behavior | Result |
| :--- | :--- | :--- |
| Single backup exists, operator calls `--prune 0` | Singleton protection intercepts call, refuses to delete sole backup. | PASS |
| Single backup exists, operator calls `--prune 1` | Retention satisfied, 0 files deleted. | PASS |
| 4 backups exist, operator calls `--prune 2` | 2 oldest backups and their `.meta.json` deleted; 2 newest preserved. | PASS |
| Backup `.db` exists without `.meta.json` | Prunes `.db` cleanly without raising `FileNotFoundError`. | PASS |
| Temporary `.tmp_part` file present | Ignored by `list_backups()` and protected from naive pruning. | PASS |

---

## 5. Storage Capacity Planning & Retention Guidelines

Based on measured storage metrics:
- Single backup snapshot size: ~4.61 MB
- Daily backup generation (hourly snapshots during working hours): ~46 MB / day
- Recommended production retention policy:
  - Keep all hourly snapshots for 24 hours (`keep_count=24`)
  - Keep 1 daily snapshot for 30 days
  - Keep 1 monthly snapshot for 1 year
- At current corpus scale, 30 days of daily backups consumes only ~138 MB, making comprehensive retention highly cost-effective and operationally safe.

## 6. Formal Proof of Singleton Retention Invariant

Let $B = \{b_1, b_2, \dots, b_k\}$ represent the set of available backup manifests ordered by creation timestamp descending. Let $k = |B|$ be the current count of backups, and let $K_{\text{req}}$ be the operator-requested retention count.

The effective retention threshold is defined as:
$$K_{\text{eff}} = \max(1, K_{\text{req}})$$

The pruning function specifies:
$$\text{Prune}(B, K_{\text{req}}) = \begin{cases} \emptyset & \text{if } k \le 1 \\ \emptyset & \text{if } k \le K_{\text{eff}} \\ \{b_{K_{\text{eff}}+1}, \dots, b_k\} & \text{if } k > K_{\text{eff}} \end{cases}$$

### Proof of Non-Empty Post-State:
1. If $k \le 1$, the pruned set is $\emptyset$, and the remaining backups are $B$. Since $k = 1$, $|B| = 1 > 0$.
2. If $k > 1$ and $k \le K_{\text{eff}}$, the pruned set is $\emptyset$, and remaining backups are $B$. Thus $|B| \ge 2 > 0$.
3. If $k > K_{\text{eff}}$, the number of backups preserved is $|B \setminus \text{Prune}(B, K_{\text{req}})| = K_{\text{eff}} = \max(1, K_{\text{req}}) \ge 1$.

Therefore, for any integer $K_{\text{req}} \in [-\infty, \infty]$, the number of preserved backups is strictly bounded below by 1:
$$\forall K_{\text{req}} \in \mathbb{Z}, \quad |B_{\text{post}}| \ge 1$$
Q.E.D.
