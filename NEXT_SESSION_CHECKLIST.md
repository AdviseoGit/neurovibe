# Neurovibe - Next Session Quick Checklist
**For:** Wednesday, June 24, 2026 (Weekly Maintenance)

---

## 🔥 TOP 3 ACTIONS (In Order)

### 1. Publish Maskering Guide (Expanded) ✍️
- **File:** `/data/workspace/projects/neurovibe/content/maskering-en-guide.md` (718 words → expand to 2,500+)
- **Action:**
  1. Read draft: `content/maskering-en-guide.md`
  2. Expand with:
     - June 2026 #MaskingAtWork TikTok trend context (2.4M views)
     - 3 case studies (Tech worker, Healthcare professional, Educator)
     - FAQ section (10 Q&A) with Schema.org FAQPage markup
     - 5-step unmasking roadmap (actionable steps)
     - Internal links to: adhd-anpassningar-jobb.html, npf-arbetslivet.html, verktyg-burnout-kalkylator.html
  3. Convert to HTML (copy template from `static/maskering-pa-arbetsplatsen.html`)
  4. Deploy: `git add static/maskering-guide-expanded.html && git commit -m "feat(content): Publish expanded Maskering guide (2,500+ words, FAQ schema)" && git push origin main`
  5. Verify live: https://neurovibe.se/maskering-guide-expanded.html

### 2. Begin ADHD-Diagnos Guide (50% Draft) 📝
- **File:** Create new `/data/workspace/projects/neurovibe/content/adhd-diagnos-guide.md`
- **Action:**
  1. Research June 2026 wait times (Stockholm, Göteborg, Malmö)
  2. Research private clinic pricing (2026 rates)
  3. Outline structure (10 sections)
  4. Write first 1,500 words (50% target):
     - Introduction (late diagnosis stigma, masking)
     - Swedish healthcare navigation (vårdcentral → remiss process)
     - Step-by-step assessment (testing, interviews)
  5. Save draft (don't publish yet - aim for 3,000+ words total)

### 3. Add FAQ to 3 Articles (Schema.org) ⚡
- **Files:** `static/neurodiversitet-arbetsplatsen.html`, `static/npf-arbetslivet.html`, `static/adhd-anpassningar-jobb.html`
- **Action:**
  1. Add FAQ section at end of article (before CTA)
  2. 10 Q&A per article (relevant to topic)
  3. Add Schema.org FAQPage markup in `<script type="application/ld+json">`
  4. Deploy all 3 together: `git commit -m "feat(seo): Add FAQ sections with Schema.org FAQPage to 3 articles"`

---

## 📊 CHECK PERFORMANCE FIRST

Before starting work, run these commands to measure progress:

```bash
# 1. Google Search Console performance (7-day window)
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# Expected: Impressions >10 (baseline), hopefully 1-2 non-brand keywords

# 2. Verify Schema.org markup count
cd /data/workspace/projects/neurovibe/static && grep -c '"@type": "Article"' *.html

# Expected: 6 (all core articles have Article schema)

# 3. Check Railway deployment status
cd /data/workspace/projects/neurovibe && git status

# Expected: Clean (no uncommitted changes from last week)
```

---

## ✅ SUCCESS CRITERIA (End of Session)

- [ ] Maskering guide published (2,500+ words, live at neurovibe.se/maskering-guide-expanded.html)
- [ ] ADHD-diagnos guide draft exists (1,500+ words in `content/adhd-diagnos-guide.md`)
- [ ] FAQ sections added to 3 articles (with Schema.org FAQPage markup)
- [ ] GSC shows impressions >50 (up from 10 baseline)
- [ ] At least 1 non-brand keyword impression tracked in GSC

---

## 🔍 RESEARCH NOTES (For ADHD-Diagnos Guide)

### Key Data Points Needed
- **Wait times by region (June 2026):**
  - Stockholm: 12-18 months (Region Stockholm data)
  - Göteborg: 18-24 months (VGR data)
  - Malmö: 6-9 months (Region Skåne data)
- **Private clinic pricing (2026):**
  - Typical range: 8,000-15,000 SEK (full assessment)
  - Follow-up: 1,500-3,000 SEK
- **Public cost:**
  - Vårdavgift: 300 SEK (specialist visit)
- **Post-diagnosis rights:**
  - FK: Sjukskrivning support, aktivitetsersättning (if severe)
  - Workplace: Right to request accommodations (Diskrimineringslagen)
  - Medication: Subsidized via högkostnadsskyddet

### Sources to Check
- 1177.se (official healthcare info)
- Attention.se (Swedish ADHD association)
- Riksförbundet Attention
- Kunskapsguiden.se

---

## 📅 TIMELINE (June 24 Session - ~4 hours)

- **Hour 1:** Run performance checks + research ADHD-diagnos data
- **Hour 2:** Expand Maskering guide (draft 2,500+ words)
- **Hour 3:** Convert to HTML, add Schema, deploy + verify
- **Hour 4:** Begin ADHD-diagnos guide outline + first 500 words

**If time allows:** Add FAQ to first article (neurodiversitet-arbetsplatsen.html)

---

## 🎯 NEXT WEEK PREVIEW (July 1 Session)

1. Complete ADHD-diagnos guide (3,000+ words total)
2. Publish Försäkringskassan guide (expand draft with June 2026 FK reforms)
3. Publish AI note-taking guide (expand to 2,500+ words)

---

**Quick Reference:**
- **Current Traffic:** 1 click/month (brand only)
- **Current Content:** 6 articles (all with Schema ✅) + 3 tools
- **4-Week Target:** 50+ clicks/month, 10+ articles
- **Risk Level:** LOW ✅
- **Trend Alignment:** PERFECT ⭐⭐⭐⭐⭐

*Last updated: June 17, 2026 by Medium*
