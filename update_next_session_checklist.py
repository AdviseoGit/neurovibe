import os

path = "/data/workspace/projects/neurovibe/NEXT_SESSION_CHECKLIST.md"

content = """# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run (AI Tools Expansion & Content)

---

## 🔥 TOP ACTIONS (In Order)

### 1. Develop Neuroinclusive Meeting Checklist Generator 🛠️
- **Goal:** Build the interactive tool outlined in `content/ai_meeting_checklist_tool.md`.
- **Action:** Create the HTML/JS for the tool, save it in the `verktyg` directory, and link it from the main navigation and relevant articles.

### 2. Monitor "Återgång till arbetet" Guide Performance 📊
- **Goal:** Continue tracking indexing and traffic for post-semester content as August approaches.
- **Action:** Run GSC report and analyze impressions/clicks for `post-semester-stress-npf.html`.

### 3. Expand Datarapport 📈
- **Goal:** Add more insights to `data-rapport-2026.html` to keep the lead magnet fresh.
- **Action:** Add an insight regarding the impact of inclusive meetings on cognitive fatigue based on the new tool.

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check SQLite Leads
python3 -c 'import sqlite3; conn=sqlite3.connect("/data/workspace/projects/neurovibe/data/neurovibe.db"); print(conn.execute("SELECT source, COUNT(*) FROM neurovibe_leads GROUP BY source").fetchall())'
```

*Last updated: 2026-07-29 by Medium*
"""

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("NEXT_SESSION_CHECKLIST.md updated successfully.")
