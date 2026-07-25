import os
from datetime import datetime

log_path = "/data/workspace/projects/neurovibe/INDEXING_LOG.md"
today = datetime.now().strftime("%Y-%m-%d")

new_lines = f"""https://neurovibe.se/inkluderande-kultur-npf.html | URL is unknown to Google | {today} | Ligger i sitemap och är länkad från resurser.
https://neurovibe.se/om-sajten.html | URL is unknown to Google | {today} | Ligger i sitemap och är länkad från footern på alla sidor.
"""

if os.path.exists(log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(new_lines)
    print("INDEXING_LOG.md updated")
