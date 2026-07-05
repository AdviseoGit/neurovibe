import os
import json

directory = '/data/workspace/projects/neurovibe/static'

for filename in os.listdir(directory):
    if filename.endswith(".html") and filename not in ["index.html", "admin.html", "feedback.html", "waitlist-success.html", "om-sajten.html", "resurser.html", "integritetspolicy.html", "lead-magnet-snippet.html"]:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            if "application/ld+json" not in content:
                print(f"Missing schema in {filename}")
