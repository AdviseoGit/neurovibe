import re
from datetime import datetime

with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'r') as f:
    xml = f.read()

today = datetime.now().strftime('%Y-%m-%d')
new_url = f'''  <url>
    <loc>https://neurovibe.se/post-semester-stress-npf.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>'''

if 'post-semester-stress-npf.html' not in xml:
    xml = xml.replace('</urlset>', new_url)
    with open('/data/workspace/projects/neurovibe/static/sitemap.xml', 'w') as f:
        f.write(xml)
