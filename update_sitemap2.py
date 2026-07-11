import re
from datetime import datetime

with open('static/sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

# Fix the broken line
sitemap = sitemap.replace('<url>P26-07-11</lastmod><priority>0.8</priority></url>', '')
sitemap = sitemap.replace('<url><loc>https://neurovibe.se/verktyg-myndighetsnavigator.html</loc><lastmod>2026-07-06</lastmod><priority>0.8</priority></url>', '')
sitemap = sitemap.replace('</urlset>', f'<url><loc>https://neurovibe.se/verktyg-myndighetsnavigator.html</loc><lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod><priority>0.8</priority></url>\n</urlset>')

with open('static/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
