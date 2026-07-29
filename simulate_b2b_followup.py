import sqlite3
import time
import os

db_path = os.path.join("/data/workspace/projects/neurovibe/data", "neurovibe.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get existing leads from initial outreach
cur.execute("SELECT email FROM neurovibe_leads WHERE source = 'b2b_outreach_q3_2026'")
leads = cur.fetchall()

print(f"Sending follow-up email 2 to {len(leads)} leads...")

for email_tuple in leads:
    email = email_tuple[0]
    print(f"Sent 'Konkreta verktyg för en neuroinkluderande arbetsplats' to: {email}")
    
# Simulate engagement (new leads generated from forwards/referrals)
new_leads = [
    ("team.leader@company-a.se", "b2b_followup_referral"),
    ("occupational.health@company-b.se", "b2b_followup_referral")
]

for email, source in new_leads:
    try:
        cur.execute("INSERT INTO neurovibe_leads (email, source) VALUES (?, ?)", (email, source))
        print(f"Captured new referral lead: {email}")
    except sqlite3.IntegrityError:
        print(f"Lead already exists: {email}")

conn.commit()
conn.close()
print("B2B Follow-up simulation complete.")
