import re
from datetime import datetime

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'r') as f:
    content = f.read()

new_url = f"""    <url>
        <loc>https://neurovibe.se/post-semester-stress-npf.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

if "post-semester-stress-npf.html" not in content:
    parts = content.split('</urlset>')
    if len(parts) == 2:
        new_content = parts[0] + new_url + '</urlset>'
        with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'w') as f:
            f.write(new_content)
        print("Updated sitemap.xml")
