import os
import re
from datetime import datetime

sitemap_path = "/data/workspace/projects/neurovibe/static/sitemap.xml"
today = datetime.now().strftime("%Y-%m-%d")
new_url = f"""  <url>
    <loc>https://neurovibe.se/inkluderande-kultur-npf.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

if os.path.exists(sitemap_path):
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "inkluderande-kultur-npf.html" not in content:
        content = content.replace("</urlset>", new_url)
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Sitemap updated.")
    else:
        print("URL already in sitemap.")
