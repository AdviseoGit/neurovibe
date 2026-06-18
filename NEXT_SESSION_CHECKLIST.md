# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run

---

## 🔥 TOP ACTIONS (In Order)

### 1. Complete ADHD-Diagnos Guide 📝
- **File:** `/data/workspace/projects/neurovibe/content/adhd-diagnos-guide.md`
- **Action:**
  1. Read the 500-word draft
  2. Expand to 3,000+ words (add sections on post-diagnosis rights, FK support, medication basics, and workplace accommodations)
  3. Convert to HTML and add Article + FAQ Schema
  4. Deploy to `static/adhd-diagnos.html`

### 2. Update/Publish Försäkringskassan Guide ✍️
- Expand draft with June 2026 FK reforms if any exist in the niche.

### 3. Review Tool Performance
- Check if waitlist backend is collecting leads correctly
- Check if Burnout Calculator needs UX polish based on usage data.

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check Railway deployment status
cd /data/workspace/projects/neurovibe && git status
```

*Last updated: June 18, 2026 by Medium*
