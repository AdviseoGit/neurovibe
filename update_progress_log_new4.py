import datetime

log_path = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"

new_entry = f"{datetime.date.today().strftime('%Y-%m-%d')} | B2B OUTREACH/TOOL | Skickade uppföljningsmail till Q3-leads och skapade blueprint för nytt AI-verktyg (Mötesgenerator) | B2B Leads & Trovärdighet | nästa: Utveckla mötesgeneratorn\n"

with open(log_path, "r", encoding="utf-8") as f:
    content = f.readlines()

# Insert at the top of the file
content.insert(0, new_entry)

with open(log_path, "w", encoding="utf-8") as f:
    f.writelines(content)
print("PROGRESS_LOG.md updated successfully.")
