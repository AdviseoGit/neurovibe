import sqlite3

def add_api_stats_leads():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    if '/api/stats/leads' in content:
        print("Endpoint /api/stats/leads already exists.")
        return

    endpoint_code = """
@app.get("/api/stats/leads")
async def get_stats_leads():
    # Publika leads-stats för scoreboard
    stats = leadengine.lead_stats()
    return {
        "total": stats.get("total", 0),
        "last_7_days": stats.get("last_7_days", 0)
    }
"""

    with open('/data/workspace/projects/neurovibe/main.py', 'a') as f:
        f.write(endpoint_code)
    
    print("Added /api/stats/leads to main.py")

if __name__ == "__main__":
    add_api_stats_leads()
