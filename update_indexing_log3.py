import os
from datetime import datetime

file_path = "/data/workspace/projects/neurovibe/INDEXING_LOG.md"
date_str = datetime.now().strftime("%Y-%m-%d")
url = "https://neurovibe.se/arbetsgivarpaketet.html"
status = "URL is unknown to Google"
action = "Lagt till i sitemap"

entry = f"{url} | {status} | {date_str} | {action}\n"

content = ""
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        
if url not in content:
    with open(file_path, "w") as f:
        f.write(content + entry)
print("Updated INDEXING_LOG.md")
