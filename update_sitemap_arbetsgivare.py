import os
from datetime import datetime

file_path = "/data/workspace/projects/neurovibe/sitemap.xml"
date_str = datetime.now().strftime("%Y-%m-%d")

with open(file_path, "r") as f:
    content = f.read()

# Add arbetsgivarpaketet.html if missing
if "arbetsgivarpaketet.html" not in content:
    new_url = f"""  <url>
    <loc>https://neurovibe.se/arbetsgivarpaketet.html</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>"""
    content = content.replace("</urlset>", new_url)
else:
    import re
    content = re.sub(
        r'(<loc>https://neurovibe.se/arbetsgivarpaketet.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        rf'\g<1>{date_str}\g<2>',
        content
    )

with open(file_path, "w") as f:
    f.write(content)
print("Updated sitemap.xml")
