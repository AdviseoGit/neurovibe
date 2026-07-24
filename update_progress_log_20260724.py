import os

filepath = '/data/workspace/projects/neurovibe/PROGRESS_LOG.md'
with open(filepath, 'r') as f:
    content = f.read()

new_entry = "2026-07-24 | TEKNIK | Fixade dubbel <nav> i footer | site_scan.py visar 0 HARD-fynd | nästa: tillväxt, nytt verktyg eller sida\n"
content = content.replace("# Progress Log\n", f"# Progress Log\n\n{new_entry}")

with open(filepath, 'w') as f:
    f.write(content)
