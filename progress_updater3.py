with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()
    
new_log = "2026-07-14 | DATA/LEADFLOW | Bytte till SQLite för tool_usage och lade till lead magnets i alla verktyg | Datamoat & Konvertering | nästa: Fyll datarapporten med mer data eller utför outreach\n"
content = new_log + content

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(content)
