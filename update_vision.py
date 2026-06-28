import re
with open('/data/workspace/projects/neurovibe/SITE_VISION.md', 'r') as f:
    content = f.read()

# Try to find milestone 2 and check lead-formulär
if "[ ] Lead-formulär (waitlist) är live" in content:
    content = content.replace("[ ] Lead-formulär (waitlist) är live", "[x] Lead-formulär (waitlist) är live")
    with open('/data/workspace/projects/neurovibe/SITE_VISION.md', 'w') as f:
        f.write(content)
