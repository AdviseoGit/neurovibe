import os

html_files = [f for f in os.listdir("/data/workspace/projects/neurovibe/static") if f.endswith(".html")]

count = 0
for file in html_files:
    filepath = os.path.join("/data/workspace/projects/neurovibe/static", file)
    with open(filepath, "r") as f:
        content = f.read()
    
    if 'Denna sajt skapas och drivs helt av AI' not in content and file not in ['lead-magnet-snippet.html', 'waitlist-success.html']:
        print(f"No AI disclaimer in {file}")

