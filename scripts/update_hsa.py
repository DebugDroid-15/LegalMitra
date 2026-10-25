from pathlib import Path

p = Path("legalmitra/temporal/engine.py")
text = p.read_text(encoding="utf-8")

old_snippet = 'amendment_act_id="IND-AMEND-HSA-2005",\n        temporal_status=TemporalStatus.ACTIVE,\n    ))'
new_snippet = '''amendment_act_id="IND-AMEND-HSA-2005",
        temporal_status=TemporalStatus.ACTIVE,
        is_retrospective=True,
        retrospective_basis="Supreme Court of India in Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1 held that rights under amended Section 6 apply retroactively to daughters living on or after 2005-09-09 irrespective of date of birth or survival of coparcener father.",
    ))'''

if old_snippet in text:
    text = text.replace(old_snippet, new_snippet)
elif old_snippet.replace('\n', '\r\n') in text:
    text = text.replace(old_snippet.replace('\n', '\r\n'), new_snippet.replace('\n', '\r\n'))
else:
    print("Could not find snippet")

p.write_text(text, encoding="utf-8")
print("Done")

