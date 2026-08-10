import re

def fix_api_stats_leads_again():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # The 502 issue is because leadengine module isn't imported or we need to use it instead of sqlite3 directly to match the existing lead capture setup
    
    endpoint_code = """
@app.get("/api/stats/leads")
async def get_stats_leads():
    # Publika leads-stats för scoreboard
    try:
        stats = leadengine.lead_stats()
        return {
            "total": stats.get("total", 0),
            "last_7_days": stats.get("last_7_days", 0)
        }
    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}
"""

    pattern = re.compile(r'@app\.get\("/api/stats/leads"\).*?return.*?\}\n', re.DOTALL)
    content = pattern.sub('', content)

    main_block = 'if __name__ == "__main__":'
    content = content.replace(main_block, endpoint_code + '\n' + main_block)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Updated /api/stats/leads in main.py to use leadengine")

if __name__ == "__main__":
    fix_api_stats_leads_again()
