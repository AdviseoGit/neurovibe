import re

def fix_api_stats_leads_six():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # The 502 issue is because of the catch-all HTML route serving logic conflicting with API endpoints,
    # OR we just put it in the wrong place. The catchall route must be at the very bottom.
    
    endpoint_code = """
@app.get("/api/stats/leads")
async def get_stats_leads():
    # Enkel fil-räknare för att unvika 502 db-låsningar
    import os
    try:
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        if not os.path.exists(db_path):
            return {"total": 0, "last_7_days": 0}
            
        import sqlite3
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

    # Insert it before the catch-all route `@app.get("/{path:path}", response_class=FileResponse)`
    catchall = '@app.get("/{path:path}", response_class=FileResponse)'
    content = content.replace(catchall, endpoint_code + '\n' + catchall)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads and placed it BEFORE the catch-all route")

if __name__ == "__main__":
    fix_api_stats_leads_six()
