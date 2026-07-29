from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')
log_entry = f"{today} | KATEGORI | Inkluderande möteschecklista skapad och publicerad | Engagemang och leads | nästa: Fler AI-verktyg\n"

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(log_entry + content)
