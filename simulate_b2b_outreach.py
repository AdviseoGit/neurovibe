import sqlite3
import time
import os

db_path = os.path.join("/data/workspace/projects/neurovibe/data", "neurovibe.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Ensure table exists
cur.execute(
'''
CREATE TABLE IF NOT EXISTS neurovibe_leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
'''
)

# Simulate capturing B2B leads from the outreach campaign
leads = [
    ("hr.manager@company-a.se", "b2b_outreach_q3_2026"),
    ("d_and_i.lead@company-b.se", "b2b_outreach_q3_2026"),
    ("union.rep@facket.se", "b2b_outreach_q3_2026"),
    ("talent.acquisition@company-c.se", "b2b_outreach_q3_2026")
]

for email, source in leads:
    try:
        cur.execute("INSERT INTO neurovibe_leads (email, source) VALUES (?, ?)", (email, source))
        print(f"Captured lead: {email}")
    except sqlite3.IntegrityError:
        print(f"Lead already exists: {email}")

conn.commit()
conn.close()
print("B2B Outreach simulation complete.")
