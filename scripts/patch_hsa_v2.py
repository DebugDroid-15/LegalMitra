from pathlib import Path

file_path = Path("legalmitra/temporal/engine.py")
content = file_path.read_text(encoding="utf-8")

old_text = 'amendment_act_id="HSA-AMEND-2005",\n        temporal_status=TemporalStatus.ACTIVE,'
new_text = '''amendment_act_id="HSA-AMEND-2005",
        temporal_status=TemporalStatus.ACTIVE,
        is_retrospective=True,
        retrospective_basis="Supreme Court of India in Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1 held that rights under amended Section 6 apply retroactively to daughters living on or after 2005-09-09 irrespective of date of birth or survival of coparcener father.",'''

if old_text in content:
    content = content.replace(old_text, new_text)
    file_path.write_text(content, encoding="utf-8")
    print("Updated HSA-SEC-6 version 2 successfully")
else:
    print("Already updated or old_text not found")

