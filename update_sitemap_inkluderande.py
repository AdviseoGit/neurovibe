import re
from datetime import datetime

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'r') as f:
    content = f.read()

today = datetime.now().strftime('%Y-%m-%d')
new_url = f"""    <url>
        <loc>https://neurovibe.se/verktyg/inkluderande-moten.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

# Append before </urlset>
content = content.replace('</urlset>', f'{new_url}</urlset>')

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'w') as f:
    f.write(content)

print("Added verktyg/inkluderande-moten.html to sitemap.")
