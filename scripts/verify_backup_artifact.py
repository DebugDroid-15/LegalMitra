import os
import hashlib
import json

def verify_backup_artifact():
    backup_file = "data/backups/legalmitra_kb_20261026T115207Z.db"
    meta_file = backup_file + ".meta.json"
    
    print("=== Phase 62 Backup Artifact Verification ===")
    print(f"Backup file path: {backup_file}")
    print(f"Backup file exists: {os.path.exists(backup_file)}")
    print(f"Meta file path: {meta_file}")
    print(f"Meta file exists: {os.path.exists(meta_file)}")
    
    if os.path.exists(backup_file):
        sz = os.path.getsize(backup_file)
        with open(backup_file, "rb") as f:
            computed_sha = hashlib.sha256(f.read()).hexdigest()
        print(f"Physical Size: {sz:,} bytes")
        print(f"Computed SHA256: {computed_sha}")
        
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            recorded_sha = meta.get("sha256_checksum")
            print(f"Recorded SHA256: {recorded_sha}")
            print(f"Digest Exact Match: {computed_sha == recorded_sha}")
            print(f"Backup ID: {meta.get('backup_id')}")
            print(f"Timestamp: {meta.get('timestamp_utc')}")
            print(f"Sources: {meta.get('total_sources')} | Chunks: {meta.get('total_chunks')} (Authentic: {meta.get('authentic_chunks')}, Scaffold: {meta.get('quarantined_scaffold_chunks')})")
            print(f"Target Release: {meta.get('target_release')}")
            print(f"Quarantine Compliant: {meta.get('is_quarantine_compliant')}")
            print(f"Status: {meta.get('status')}")
    else:
        print("[FAIL] Backup artifact not found!")

if __name__ == "__main__":
    verify_backup_artifact()
