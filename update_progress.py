with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

new_log = "2026-06-21 | DATA | Implementerat data-capture för burnout-kalkylator | Data-tillgång | nästa: - \n" + content

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(new_log)
