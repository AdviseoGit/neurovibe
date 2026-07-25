import os
import glob
import re

html_files = glob.glob("/data/workspace/projects/neurovibe/static/*.html")
html_files.append("/data/workspace/projects/neurovibe/om-sajten.html")

for file_path in html_files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "Denna sajt skapas och drivs helt av AI" not in content and "<footer" in content:
            # We want to insert the disclaimer before the philosophy link
            new_content = re.sub(
                r'(<div class="flex gap-12">\s*<a href="#philosophy")',
                r'<div class="flex gap-12">\n                <span>Denna sajt skapas och drivs helt av AI</span>\n                <a href="#philosophy"',
                content
            )
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
            else:
                print(f"Regex failed for {file_path}")

