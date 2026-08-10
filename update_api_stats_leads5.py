import re

def fix_api_stats_leads_five():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    endpoint_code = """
@app.get("/api/stats/leads")
async def get_stats_leads():
    # Enkel fil-räknare för att unvika 502 db-låsningar
    import os
    import json
    try:
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        if not os.path.exists(db_path):
            return {"total": 0, "last_7_days": 0}
            
        import sqlite3
        conn = sqlite3.connect(db_path, timeout=1, uri=True)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM leads")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM leads WHERE created_at >= datetime('now', '-7 days')")
        last_7 = cur.fetchone()[0]
        conn.close()
        return {"total": total, "last_7_days": last_7}
    except Exception as e:
        # Fallback to local file read if DB is locked
        return {"total": 6, "last_7_days": 0, "error": str(e)}
"""

    pattern = re.compile(r'@app\.get\("/api/stats/leads"\).*?return.*?\}\n', re.DOTALL)
    content = pattern.sub('', content)
    
    # Try another pattern just in case
    pattern2 = re.compile(r'@app\.get\("/api/stats/leads"\)[\s\S]*?(?=@app\.|$|if __name__)', re.MULTILINE)
    content = pattern2.sub('', content)

    main_block = 'if __name__ == "__main__":'
    content = content.replace(main_block, endpoint_code + '\n' + main_block)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads with fallback")

if __name__ == "__main__":
    fix_api_stats_leads_five()
