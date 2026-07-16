import sqlite3
import json
import os

db_path = os.path.join("/data/workspace/projects/neurovibe/data", "neurovibe.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Ensure table exists
cur.execute(
'''
CREATE TABLE IF NOT EXISTS tool_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool TEXT NOT NULL,
    modules TEXT,
    input_text TEXT,
    output_text TEXT,
    metadata TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
'''
)

# Simulate usage of AI ROI Calculator & Authority Navigator
usages = [
    ("roi_calculator", '["salary_analysis", "productivity_loss"]', "ADHD, 45000 SEK, 30% masking", "Estimated ROI: 150 000 SEK/year with proper accommodations", '{"role": "HR Manager"}'),
    ("roi_calculator", '["retention_cost"]', "Autism, 50000 SEK, high sensory load", "Estimated turnover cost saved: 300 000 SEK", '{"role": "Team Lead"}'),
    ("myndighetsnavigatorn", '["afs_2020_5"]', "Need to understand employer responsibility for sensory environment", "According to AFS 2020:5, employers must adapt the physical environment...", '{"role": "HR Specialist"}'),
    ("myndighetsnavigatorn", '["forsakringskassan"]', "How to apply for 'arbetshjälpmedel' for noise cancelling headphones", "1. Get medical certificate 2. Apply via...", '{"role": "Employee"}')
]

for tool, modules, input_text, output_text, metadata in usages:
    cur.execute("INSERT INTO tool_usage (tool, modules, input_text, output_text, metadata) VALUES (?, ?, ?, ?, ?)", 
                (tool, modules, input_text, output_text, metadata))
    print(f"Logged usage for: {tool}")

conn.commit()
conn.close()
print("Tool usage simulation complete.")
