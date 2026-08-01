import os

file_path = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"
with open(file_path, "r") as f:
    content = f.read()

new_log_entry = "2026-08-01 | LEADFLOW | Uppdaterade länkar till arbetsgivarpaketet | för_arbetsgivare konvertering | nästa: Leg granskare / pris\n"

if new_log_entry not in content:
    lines = content.split('\n')
    lines.insert(2, new_log_entry.strip())
    content = '\n'.join(lines)

with open(file_path, "w") as f:
    f.write(content)

