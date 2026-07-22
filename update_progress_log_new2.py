with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()

new_log = "2026-07-22 | CONTENT/SEO | Publicerat 'Återgång till arbetet - Hantera post-semester stress vid NPF' | Augusti/Q3 Förberedelse | nästa: Fortsätt B2B Outreach\n"

if not content.startswith("2026-07-22"):
    with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
        f.write(new_log + content)
    print("Updated PROGRESS_LOG.md")
else:
    print("Log already updated today")
