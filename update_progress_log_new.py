with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

new_log = "2026-07-21 | DATA/LEADFLOW | Ny data i rapporten (Insikt 4 ROI) & uppdaterad sitemap | Data-Moat & B2B Leads | nästa: Fyll datarapporten med mer data eller kör outreach\n"

if not content.startswith("2026-07-21"):
    with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
        f.write(new_log + content)
    print("Updated PROGRESS_LOG.md")
else:
    print("Log already updated today")
