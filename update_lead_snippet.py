import os
import re

snippet_path = "/data/workspace/projects/neurovibe/static/lead-magnet-snippet.html"
with open(snippet_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace endpoint to something trackable or ensure it works. It currently hits /api/lead which works offline.
# We will verify all guider actually include it.

guider = [
    "adhd-anpassningar-jobb.html",
    "adhd-diagnos-vuxen.html",
    "maskering-pa-arbetsplatsen.html",
    "forsakringskassan-arbetsformedlingen-stod.html"
]

for guide in guider:
    guide_path = os.path.join("/data/workspace/projects/neurovibe/static", guide)
    with open(guide_path, "r", encoding="utf-8") as f:
        guide_content = f.read()
    
    if "lead-magnet-snippet.html" not in guide_content and "Få vår kompletta checklista" not in guide_content:
        print(f"Adding snippet to {guide}")
        # Insert before closing article tag or after a specific heading
        guide_content = guide_content.replace('</article>', f'\n<!-- Lead Magnet -->\n<div id="lead-magnet-container"></div>\n<script>\nfetch("/lead-magnet-snippet.html").then(r => r.text()).then(html => document.getElementById("lead-magnet-container").innerHTML = html);\n</script>\n</article>')
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
    else:
        print(f"Snippet already in {guide}")
