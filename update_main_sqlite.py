import re

with open("main.py", "r") as f:
    content = f.read()

# Make sure we import sqlite3
if "import sqlite3" not in content:
    content = content.replace("import os", "import os\nimport sqlite3\n")

# Replace save_lead logic to save to sqlite instead of missing postgres
new_save_lead = """async def save_lead(req: LeadRequest, background: BackgroundTasks):
    background.add_task(_deliver_welcome_nv, req.email)
    
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "neurovibe.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS neurovibe_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        cur.execute(
            "INSERT OR IGNORE INTO neurovibe_leads (email, source) VALUES (?, ?)",
            (req.email, req.source)
        )
        conn.commit()
        conn.close()
        print(f"LEAD CAPTURED (SQLite): {req.email}")
        return {"status": "success", "message": "Email saved"}
    except Exception as e:
        print(f"SQLite Error: {e}")
        return {"status": "error", "message": "Failed to save email"}
"""

# Try to replace the save_lead function using regex
pattern = re.compile(r'async def save_lead\(req: LeadRequest, background: BackgroundTasks\):.*?return {"status": "success", "message": "Email saved"\}[\s]*\}[\s]*except Exception as e:.*?return {"status": "error", "message": "Failed to save email"\}', re.DOTALL)
# It's safer to just replace everything from async def save_lead down to its last line.
content = re.sub(r'async def save_lead\(req: LeadRequest, background: BackgroundTasks\):.*?return \{"status": "error", "message": "Failed to save email"\}', new_save_lead.strip(), content, flags=re.DOTALL)

with open("main.py", "w") as f:
    f.write(content)
print("Updated main.py")
