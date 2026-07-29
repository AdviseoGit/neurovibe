with open('/data/workspace/projects/neurovibe/NEXT_SESSION_CHECKLIST.md', 'r') as f:
    content = f.read()

# Replace top actions with checkmarks or cleared
new_content = """# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run (AI Tools Expansion & Content)

---

## 🔥 TOP ACTIONS (In Order)

### 1. Develop Neuroinclusive Meeting Checklist Generator 🛠️
- **Status:** ✅ KLAR. Skapad under `static/verktyg/inkluderande-moten.html`, länkad från `resurser.html` och tillagd i sitemap.

### 2. Monitor "Återgång till arbetet" Guide Performance 📊
- **Status:** ✅ KLAR. Kollade GSC. Både `post-semester-stress-npf.html` och `data-rapport-2026.html` genererar impressions. 

### 3. Expand Datarapport 📈
- **Status:** ✅ KLAR. La till Insikt 6 om Mötesstrukturen.

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check SQLite Leads
python3 -c 'import sqlite3; conn=sqlite3.connect("/data/workspace/projects/neurovibe/data/neurovibe.db"); print(conn.execute("SELECT source, COUNT(*) FROM neurovibe_leads GROUP BY source").fetchall())'
```

*Last updated: 2026-07-29 by Medium (Subagent)*
"""
with open('/data/workspace/projects/neurovibe/NEXT_SESSION_CHECKLIST.md', 'w') as f:
    f.write(new_content)
