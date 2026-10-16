from pathlib import Path

source = Path("stitch_assets/landing_page.html")
target = Path("legalmitra/web/templates/landing_page.html")

content = source.read_text(encoding="utf-8")

# Wire up the CTAs to route to /chat
content = content.replace('href="#showcase"', 'href="/chat"')
content = content.replace('href="#hero"', 'href="/chat"')

target.write_text(content, encoding="utf-8")
print(f"Landing page template written successfully: {len(content):,} characters")

