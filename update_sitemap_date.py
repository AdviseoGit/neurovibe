import re
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'r') as f:
    sitemap = f.read()

# Update lastmod for data-rapport-2026.html
sitemap = re.sub(
    r'(<loc>https://neurovibe.se/data-rapport-2026\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
    rf'\g<1>{today}\g<2>',
    sitemap
)

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'w') as f:
    f.write(sitemap)
print("Updated sitemap")
