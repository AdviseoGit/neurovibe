import re
from datetime import datetime

with open('static/sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

today = datetime.now().strftime('%Y-%m-%d')

sitemap = re.sub(
    r'(<loc>https://neurovibe.se/verktyg-myndighetsnavigator.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
    f'\\1{today}\\2',
    sitemap
)

sitemap = re.sub(
    r'(<loc>https://neurovibe.se/lagkrav-anpassningar-arbetsmiljo.html</loc>\s*<changefreq>monthly</changefreq>\s*<priority>0.8</priority>)',
    f'<loc>https://neurovibe.se/lagkrav-anpassningar-arbetsmiljo.html</loc>\\n        <lastmod>{today}</lastmod>\\n        <changefreq>monthly</changefreq>\\n        <priority>0.8</priority>',
    sitemap
)

with open('static/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
