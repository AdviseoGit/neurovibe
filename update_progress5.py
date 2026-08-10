from datetime import datetime

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    lines = f.readlines()

new_log_entry = f"{datetime.now().strftime('%Y-%m-%d')} | LEADS | Ovan-vecket lead capture-formulär för arbetsgivare (endpoint /api/stats/leads reverterad - blockerade appen) | Kampanj: Fix leads tracking -> >0 leads | nästa: Optimera stats endpoint så att vi kan se leads\n"

# Replace the previous entry
lines[0] = new_log_entry

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.writelines(lines)
