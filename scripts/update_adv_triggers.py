from pathlib import Path

p = Path("legalmitra/orchestration/query_understanding.py")
text = p.read_text(encoding="utf-8")
old_str = '"law", "statute", "instruction"'
new_str = '"law", "statute", "statutory", "instruction", "provisos", "exceptions"'
assert old_str in text, "old_str not found"
text = text.replace(old_str, new_str, 1)
p.write_text(text, encoding="utf-8")
print("Updated successfully.")
