content = """# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run

---

## 🔥 TOP ACTIONS (In Order)

### 1. Build out the "State of Neurodiversity 2026" Data Report 📊
- **Goal:** Fill the data report (`data-rapport-2026.html`) with actual data collected from the tools (Burnout-kalkylatorn, Myndighetsnavigatorn, etc.) over the last weeks.
- **Action:** Query the SQLite databases, aggregate the data, and update the HTML report with new charts/insights.

### 2. Outreach & Link Building 🔗
- **Goal:** Start driving targeted traffic and backlinks to the new tools.
- **Action:** Identify B2B targets (HR-chefer, fackförbund) and prepare an outreach campaign using the "State of Neurodiversity" report as a lead magnet.

### 3. Review Tool Performance
- Check if SQLite data capture is working as expected for the new lead magnets.
- Check if Burnout Calculator needs UX polish based on usage data.

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check Railway deployment status
cd /data/workspace/projects/neurovibe && git status
```

*Last updated: July 15, 2026 by Medium*
"""

with open('/data/workspace/projects/neurovibe/NEXT_SESSION_CHECKLIST.md', 'w') as f:
    f.write(content)
