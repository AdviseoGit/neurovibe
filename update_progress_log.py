import os
from datetime import datetime

log_path = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"
today = datetime.now().strftime("%Y-%m-%d")
new_entry = f"{today} | INNEHÅLL/LEADFLOW | Publicerat guide om Inkluderande Kultur för NPF med AI ROI CTA | B2B Leads & Konvertering | nästa: Följ upp datarapporten och fortsätt B2B outreach\n"

if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(new_entry)
        for line in lines:
            f.write(line)
    
    print("PROGRESS_LOG.md updated")
