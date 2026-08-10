import re

def fix_api_stats_leads_order():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # The issue is the endpoint is defined AFTER the if __name__ == "__main__": block
    
    endpoint_code = """
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

    # Remove existing endpoint
    pattern = re.compile(r'@app\.get\("/api/stats/leads"\).*?return.*?\}\n', re.DOTALL)
    content = pattern.sub('', content)

    # Insert it before the if __name__ == "__main__": block
    main_block = 'if __name__ == "__main__":'
    content = content.replace(main_block, endpoint_code + '\n' + main_block)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads location in main.py")

if __name__ == "__main__":
    fix_api_stats_leads_order()
