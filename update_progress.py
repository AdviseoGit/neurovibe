import datetime

log_file = "/data/workspace/projects/neurovibe/PROGRESS_LOG.md"

date_str = datetime.datetime.now().strftime("%Y-%m-%d")

new_entry = f"{date_str} | LEADFLOW/INNEHÅLL | Producera arbetsgivarpaketets fem dokument | B2B Leads | nästa: Fyll mediakit med GA4-siffror\n"

try:
    with open(log_file, "r") as f:
        lines = f.readlines()
    
    with open(log_file, "w") as f:
        f.write(new_entry)
        f.writelines(lines)
    print("PROGRESS_LOG.md updated.")
except Exception as e:
    print(f"Error: {e}")
