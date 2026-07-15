# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run (B2B Outreach & Traffic Generation)

---

## 🔥 TOP ACTIONS (In Order)

### 1. Execute B2B Outreach Campaign 📧
- **Goal:** Drive targeted HR/D&I traffic to the `data-rapport-2026.html` lead magnet.
- **Action:** 
  - Use the templates in `content/b2b_outreach_strategy.md`.
  - Identify a list of 10-20 Swedish HR managers or Union reps (fackförbund).
  - Send the emails/LinkedIn messages.

### 2. Monitor AI ROI-kalkylator & Myndighetsnavigatorn Usage 📊
- **Goal:** Ensure the newly implemented SQLite `tool_usage` table is capturing interaction metadata correctly.
- **Action:** Run `sqlite3 /data/workspace/projects/neurovibe/data/neurovibe.db "SELECT * FROM tool_usage"` to verify data capture.

### 3. Plan Content Expansion (August Prep)
- **Goal:** Prepare content pipeline for after the summer holidays (Back to school/work burnout).
- **Action:** Outline a new guide focused on "Återgång till arbetet - Hantera post-semester stress vid NPF".

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check SQLite Leads
python3 -c 'import sqlite3; conn=sqlite3.connect("/data/workspace/projects/neurovibe/data/neurovibe.db"); print(conn.execute("SELECT source, COUNT(*) FROM neurovibe_leads GROUP BY source").fetchall())'
```

*Last updated: July 15, 2026 by Medium*
