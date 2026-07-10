import datetime

today = datetime.datetime.now().strftime("%Y-%m-%d")
log_entry = f"{today} | LEADFLOW/DATA | Förbättrad UX och data capture; AI-disclaimer rekrytering | Leadflow & AI | nästa: Implementera backend för ny UX tracker\n"

with open("/data/workspace/projects/neurovibe/PROGRESS_LOG.md", "r") as f:
    content = f.read()

with open("/data/workspace/projects/neurovibe/PROGRESS_LOG.md", "w") as f:
    f.write(log_entry + content)
print("Updated PROGRESS_LOG.md")
