# Neurovibe - Next Session Quick Checklist
**For:** Next maintenance run (August Content + SEO Optimization)
**Updated:** 2026-08-05

---

## 🔥 TOP ACTIONS (In Priority Order)

### 1. Fix "Post-semester stress" Page (CRITICAL) ⏰ 2h
- **Status:** ⏸️ PENDING (Railway token invalid - prep locally)
- **Why:** Position 11.6 with 9 impressions = high potential for quick wins
- **Actions:**
  - [ ] Rewrite title: "Hantera stress efter semestern med NPF - 7 strategier"
  - [ ] Add FAQ schema (5 Q&As about post-vacation NPF challenges)
  - [ ] Internal links to: burnout calculator, schema tool, focus timer
  - [ ] Add comparison table: "Pre-vacation prep vs. Post-vacation recovery"
- **Expected Impact:** Position 11 → 7, gain 2-3 clicks/week

### 2. Create "Höstplanering för NPF" Guide ⏰ 4h
- **Status:** ⏸️ PENDING (prep content, deploy when token fixed)
- **Why:** Seasonal opportunity (early August = planning for fall)
- **File:** `static/hostplanering-npf.html`
- **Sections:**
  - Energihantering efter semestern
  - Rutinuppbyggnad steg-för-steg (August → Sept → Oct)
  - Verktyg-länkar: Fokus Timer, Schema-guide, Anpassningsgenerator
  - Lead magnet: PDF checklist download
- **Schema.org:** HowTo + FAQPage
- **Expected Impact:** Capture "adhd höstplanering" + "npf rutiner höst"

### 3. Schema.org Audit + Implementation ⏰ 1h
- **Status:** ⏸️ PENDING
- **Priority Pages (Top 10 by impressions):**
  - [ ] forsakringskassan-arbetsformedlingen-stod.html → FAQPage
  - [ ] adhd-anpassningar-jobb.html → Article + FAQPage
  - [ ] lagkrav-anpassningar-arbetsmiljo.html → Article + FAQPage
- **Method:**
  ```bash
  # Find pages missing schema
  grep -L "application/ld\+json" static/*.html
  ```

---

## 📊 CHECK PERFORMANCE FIRST

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# 2. Check SQLite Leads
python3 -c 'import sqlite3; conn=sqlite3.connect("data/neurovibe.db"); print(f"Total leads: {conn.execute(\"SELECT COUNT(*) FROM neurovibe_leads\").fetchone()[0]}")'

# 3. Recent lead sources
python3 -c 'import sqlite3; conn=sqlite3.connect("data/neurovibe.db"); [print(f"{r[0]} from {r[1]}") for r in conn.execute("SELECT email, source FROM neurovibe_leads ORDER BY id DESC LIMIT 5").fetchall()]'
```

---

## 🗓️ WEEK 2 PRIORITIES (Aug 12-18)

### 4. B2B Content: "Inkluderande Team Kickoffs" ⏰ 3h
- **File:** `static/inkluderande-kickoff-host.html`
- **Target:** Managers, HR doing Q3/fall team meetings
- **Sections:**
  - Varför traditionella kickoffs utesluter NPF
  - Mall för neuroinclusive möten (based on inkluderande-moten tool)
  - Checklista: Energi, sensorik, kommunikation
- **CTA:** Arbetsgivarpaketet link + partner inquiry form
- **Expected Impact:** B2B leads (HR searches "inkluderande teambuilding")

### 5. Internal Linking Sprint ⏰ 2h
- **Method:** Create hub-and-spoke structure
- **Hubs:**
  - data-rapport-2026.html (link to all tools mentioned in insights)
  - resurser.html (link to all guides + tools)
- **Spokes:**
  - post-semester-stress → burnout calculator, schema tool
  - forsakringskassan-stod → myndighetsnavigator, lagkrav
  - adhd-anpassningar → anpassningsgenerator, fokus timer
- **Script approach:**
  ```python
  # Create update script that adds contextual internal links
  # to top 10 pages based on keyword overlap
  ```

---

## 📋 CONTENT PIPELINE (Prep for Weeks 3-4)

### Draft Outlines (When Time Allows)
- [ ] "Studiestart med NPF" (students + working adults)
- [ ] "Arbetsgivarens höstchecklista 2026" (B2B seasonal)
- [ ] "NPF och mörka dagar" (October prep - energy management)

---

## 🚨 BLOCKERS

### Railway Token Invalid
- **Impact:** Cannot deploy to production
- **Status:** Noted in TOOLS.md (2026-06-03)
- **Action Required:** Ask Sim for new token
- **Workaround:** Prepare all content locally, batch deploy when token refreshed

### Low Traffic = Long Feedback Cycles
- **Current:** 4 clicks/month = hard to A/B test
- **Strategy:** Focus on quick wins (schema, internal links, title optimization)
- **Metric:** Track impressions (more leading indicator than clicks at this volume)

---

## 📈 SUCCESS METRICS (4-Week Target)

**From:** 2026-08-05  
**To:** 2026-09-02

- **Clicks:** 4 → 15-20 (+275%)
- **Impressions:** 51 → 150+ (+194%)
- **Leads:** 6 → 12-15 (+100%)
- **Top 10 Rankings:** 0 → 2-3 queries
- **Pages with Schema:** 10 → 20+

---

*Last updated: 2026-08-05 by Medium (Subagent)*  
*Full report: weekly_report_2026-08-05.md*
