with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

new_log = "2026-07-22 | B2B OUTREACH | Körde simulerad outreach-kampanj till HR/Union leads | Lead Generation | nästa: Analysera resultat och förbered nästa kampanj\n"

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(new_log + content)
print("Updated PROGRESS_LOG.md with B2B")
