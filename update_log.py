import datetime

date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
log_entry = f"{date_str} | LEADFLOW | Skapa Lead-magnet formulär för Neurovibe Checklista i guiderna | Leadflow & konvertering | nästa: Bygga databasen för att skicka checklistan\n"

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

# Make sure we don't insert duplicate entries for today if already testing
if "Skapa Lead-magnet formulär" not in content[:300]:
    with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
        f.write(log_entry + content)
