from datetime import datetime

with open("PROGRESS_LOG.md", "r") as f:
    content = f.read()

# Make sure we prepend the log
today = datetime.now().strftime("%Y-%m-%d")
new_log = f"{today} | DATA | Bytt till SQLite för leads capture istället för fallback/Postgres | Data-tillgång | nästa: Bygg ut datarapport med insamlad myndighets- och burnout-data\n"
content = new_log + content

with open("PROGRESS_LOG.md", "w") as f:
    f.write(content)

