import datetime
import os

today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
progress_log = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"

entry = f"{today} | LEADS | Expose /api/stats/leads for scoreboard integration | Fix leads tracking -> >0 leads | nästa: Optimera leadsformulär conversion\n"

with open(progress_log, "r") as f:
    content = f.read()

with open(progress_log, "w") as f:
    f.write(entry + content)
