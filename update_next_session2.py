content = """# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run (B2B Follow-up & AI Tools Expansion)

---

## 🔥 TOP ACTIONS (In Order)

### 1. Execute B2B Follow-up Campaign 📧
- **Goal:** Follow up on the initial outreach for the `data-rapport-2026.html` lead magnet.
- **Action:** Send "Email 2" from `content/b2b_outreach_strategy.md` highlighting the AI tools (ROI Calculator & Anpassningsgenerator).

### 2. Monitor "Återgång till arbetet" Guide Performance 📊
- **Goal:** Check if the new post-semester stress guide is starting to index or get traffic.
- **Action:** Run GSC report and check pageviews for `post-semester-stress-npf.html`.

### 3. Plan AI Tools Expansion
- **Goal:** Continue building the moat with new interactive tools.
- **Action:** Draft a blueprint for a "Neuroinclusive Meeting Checklist Generator" tool.

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check SQLite Leads
python3 -c 'import sqlite3; conn=sqlite3.connect("/data/workspace/projects/neurovibe/data/neurovibe.db"); print(conn.execute("SELECT source, COUNT(*) FROM neurovibe_leads GROUP BY source").fetchall())'
```

*Last updated: July 22, 2026 by Medium*
"""
with open('/data/workspace/projects/neurovibe/NEXT_SESSION_CHECKLIST.md', 'w') as f:
    f.write(content)
print("Updated NEXT_SESSION_CHECKLIST.md")
