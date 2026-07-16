log_entry = "https://neurovibe.se/post-semester-stress-npf.html | URL is unknown to Google | 2026-07-16 | Ligger i sitemap (dagens datum nu)\n"

with open('/data/workspace/projects/neurovibe/INDEXING_LOG.md', 'r') as f:
    content = f.read()

with open('/data/workspace/projects/neurovibe/INDEXING_LOG.md', 'w') as f:
    f.write(content + log_entry)
