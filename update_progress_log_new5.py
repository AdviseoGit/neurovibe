import os
from datetime import datetime

log_path = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"
date_str = datetime.now().strftime("%Y-%m-%d")

with open(log_path, "r") as f:
    content = f.read()

new_entry = f"{date_str} | LEADFLOW/INNEHÅLL | Färdigställde Samtalsmall i Arbetsgivarpaketet och länkade på plats | B2B Leads | nästa: Fyll datarapporten med mer data eller utför B2B outreach\n"

with open(log_path, "w") as f:
    f.write(new_entry + content)
print("Updated PROGRESS_LOG.md")
