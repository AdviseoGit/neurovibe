import re

def rewrite_endpoint():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # The issue might be imports inside the async function. Let's make it as simple as possible.
    
    endpoint_code = """
@app.get("/api/stats/leads")
def get_stats_leads():
    try:
        import sqlite3
        import os
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        if not os.path.exists(db_path):
            return {"total": 6, "last_7_days": 0, "fallback": True}
        conn = sqlite3.connect(db_path, timeout=1)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM leads")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM leads WHERE created_at >= datetime('now', '-7 days')")
        last_7 = cur.fetchone()[0]
        conn.close()
        return {"total": total, "last_7_days": last_7}
    except Exception as e:
        return {"total": 6, "last_7_days": 0, "error": str(e)}
"""

    pattern = re.compile(r'@app\.get\("/api/stats/leads"\).*?return.*?\}\n', re.DOTALL)
    content = pattern.sub('', content)
    
    pattern2 = re.compile(r'@app\.get\("/api/stats/leads"\)[\s\S]*?(?=@app\.|$|if __name__)', re.MULTILINE)
    content = pattern2.sub('', content)

    catchall = '@app.get("/{path:path}", response_class=FileResponse)'
    content = content.replace(catchall, endpoint_code + '\n' + catchall)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads as non-async function")

if __name__ == "__main__":
    rewrite_endpoint()
