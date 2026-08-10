from datetime import datetime

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    lines = f.readlines()

new_log_entry = f"{datetime.now().strftime('%Y-%m-%d')} | LEADS | Lagt till ovan-vecket lead capture-formulär för arbetsgivare | Kampanj: Fix leads tracking -> >0 leads | nästa: Utvärdera leads\n"

# Replace the previous entry
lines[0] = new_log_entry

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.writelines(lines)
