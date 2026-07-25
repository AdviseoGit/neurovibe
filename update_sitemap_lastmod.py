import os
import glob
from datetime import datetime
import re

sitemap_path = "/data/workspace/projects/neurovibe/static/sitemap.xml"
if os.path.exists(sitemap_path):
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    today = datetime.now().strftime("%Y-%m-%d")
    
    # Update lastmod for om-sajten.html
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/om-sajten\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        content
    )
    # Also update the pages in INDEXING_LOG.md
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/verktyg-myndighetsnavigator\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        new_content
    )
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/lagkrav-anpassningar-arbetsmiljo\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        new_content
    )
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/arbetsplats-schema-npf\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        new_content
    )
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/kognitiv-ergonomi-npf\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        new_content
    )
    new_content = re.sub(
        r'(<loc>https://neurovibe\.se/adhd-diagnos-guide\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        fr'\g<1>{today}\g<2>',
        new_content
    )


    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Sitemap lastmod updated.")
