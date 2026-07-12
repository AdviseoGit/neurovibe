import re
with open("main.py", "r") as f:
    content = f.read()
    
# Manual replace
start_idx = content.find("async def save_lead")
end_idx = content.find("async def save_feedback", start_idx)

if start_idx != -1 and end_idx != -1:
    new_func = """async def save_lead(req: LeadRequest, background: BackgroundTasks):
    background.add_task(_deliver_welcome_nv, req.email)
    
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "neurovibe.db")
    
    try:
        import sqlite3
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
        print(f"LEAD CAPTURED (SQLite): {req.email} source: {req.source}")
        return {"status": "success", "message": "Email saved"}
    except Exception as e:
        print(f"SQLite Error: {e}")
        return {"status": "error", "message": "Failed to save email"}

@app.post("/api/feedback")
"""
    content = content[:start_idx] + new_func + content[end_idx+len("@app.post(\"/api/feedback\")\n"):]
    with open("main.py", "w") as f:
        f.write(content)
    print("Updated")
else:
    print("Not found")
