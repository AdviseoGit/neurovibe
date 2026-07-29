import os
import glob
import re

html_files = glob.glob('/data/workspace/projects/neurovibe/static/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # If the file already has the link to the tool, skip
    if 'verktyg/inkluderande-moten.html' in content:
        continue
    
    # We will try to add it to the Mer/Verktyg dropdown if it exists
    # Or in the nav if there is no dropdown but there's a nav
    
    # Actually, let's just make sure it's in the sitemap and linked from a main hub page like verktyg-anpassningsgenerator.html or resurser.html
    pass
