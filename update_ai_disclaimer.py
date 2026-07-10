import os
import re

file = "inkluderande-rekrytering-npf.html"
filepath = os.path.join("/data/workspace/projects/neurovibe/static", file)
with open(filepath, "r") as f:
    content = f.read()

content = content.replace(
    '&copy; 2026 Neurovibe. Alla rättigheter förbehållna.',
    'Denna sajt skapas och drivs helt av AI &middot; <a href="/om-sajten.html" class="hover:text-white transition-colors">Om sajten</a>'
)

with open(filepath, "w") as f:
    f.write(content)
print(f"Updated {file}")

