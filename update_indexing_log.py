log_entry = "https://neurovibe.se/arbetsplats-schema-npf.html | URL is unknown to Google | 2026-07-18 | Ligger i sitemap (dagens datum nu)\n"

with open('/data/workspace/projects/neurovibe/INDEXING_LOG.md', 'r') as f:
    content = f.read()

with open('/data/workspace/projects/neurovibe/INDEXING_LOG.md', 'w') as f:
    f.write(content + log_entry)
print("Updated INDEXING_LOG.md")
