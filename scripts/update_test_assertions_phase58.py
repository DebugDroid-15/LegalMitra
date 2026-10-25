import re

files_to_update = [
    "tests/test_phase52_source_integrity.py",
    "tests/test_phase53_evidence_reliability.py",
]

for fpath in files_to_update:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Update release_id check
        def repl_rel(m):
            inner = m.group(1).rstrip()
            if "PHASE58" not in inner:
                inner = inner + ', "LEGALMITRA-RELEASE-PHASE58"'
            return f'assert summary.release_id in ({inner})'

        content = re.sub(r'assert summary\.release_id in \((.*?)\)', repl_rel, content)

        # Update target_version check
        def repl_ver(m):
            inner = m.group(1).rstrip()
            if "0.58.0" not in inner:
                inner = inner + ', "0.58.0"'
            return f'assert summary.target_version in ({inner})'

        content = re.sub(r'assert summary\.target_version in \((.*?)\)', repl_ver, content)

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {fpath}")
    except Exception as e:
        print(f"Error {fpath}: {e}")
