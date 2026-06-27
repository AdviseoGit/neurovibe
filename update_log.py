import datetime

d = datetime.datetime.utcnow().strftime("%Y-%m-%d")
log_entry = f"{d} | LEADFLOW | Fixa lead-formulär i guider & stabilisera mobilsida/navigering | Lead-konvertering & UX | nästa: Analysera data-capture for första rapport"

log_path = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"
with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.insert(0, log_entry + "\n")

with open(log_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
