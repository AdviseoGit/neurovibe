import re

def fix_api_stats_leads():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    new_endpoint_code = """
@app.get("/api/stats/leads")
async def get_stats_leads():
    # Publika leads-stats för scoreboard
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM leads")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM leads WHERE created_at >= datetime('now', '-7 days')")
        last_7 = cur.fetchone()[0]
        conn.close()
        return {"total": total, "last_7_days": last_7}
    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}
"""
    
    # replace existing endpoint if it exists
    if 'def get_stats_leads():' in content:
        # find the function definition and replace it
        import re
        pattern = re.compile(r'@app\.get\("/api/stats/leads"\).*?return.*?\}', re.DOTALL)
        content = pattern.sub(new_endpoint_code.strip(), content)
    else:
        content += "\n" + new_endpoint_code

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads in main.py")

if __name__ == "__main__":
    fix_api_stats_leads()
