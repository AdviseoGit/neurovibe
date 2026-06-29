from datetime import datetime

# Update SITE_VISION.md
with open('/data/workspace/projects/neurovibe/SITE_VISION.md', 'r') as f:
    vision = f.read()

# Add to PROGRESS_LOG.md
date_str = datetime.utcnow().strftime("%Y-%m-%d")
log_entry = f"{date_str} | DATA/LEADFLOW | Test-endpoints data-capture & AI transparens | Mätning & SEO Trust | nästa: Utveckla databas/verktyg"

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    log = f.read()

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(log_entry + "\n" + log)

