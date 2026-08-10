with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'r') as f:
    content = f.read()

content = content.replace('[x] Fixat endpoint för /api/stats/leads', '[ ] Fixat endpoint för /api/stats/leads (misslyckades i detta pass pga 502)')

with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'w') as f:
    f.write(content)
