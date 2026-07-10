import os
import re

file = "inkluderande-rekrytering-npf.html"
filepath = os.path.join("/data/workspace/projects/neurovibe/static", file)
with open(filepath, "r") as f:
    content = f.read()

if '<div id="lead-magnet-container"' not in content:
    content = content.replace("</main>", '    <div id="lead-magnet-container" class="max-w-4xl mx-auto px-6 mt-12 mb-8"></div>\n</main>')
        
    content = content.replace("</body>", '    <script>\n        fetch("/lead-magnet-snippet.html").then(r => r.text()).then(html => {\n            const container = document.getElementById("lead-magnet-container");\n            if(container) container.innerHTML = html;\n        });\n    </script>\n</body>')

    with open(filepath, "w") as f:
        f.write(content)
    print(f"Updated {file}")

