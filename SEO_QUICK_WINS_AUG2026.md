# SEO Quick Wins - August 2026
**Purpose:** Capture low-hanging fruit from GSC data to boost traffic quickly  
**Data Source:** GSC (sc-domain:neurovibe.se, last 28 days, pulled 2026-08-05)

---

## 🎯 IMMEDIATE OPPORTUNITIES (Week 1)

### 1. Optimize "Post-semester stress" Page (HIGHEST PRIORITY)
**Current Performance:**
- Position: 11.6 (page 2, close to page 1)
- Impressions: 9 (shows demand exists)
- Clicks: 0 (poor CTR, likely due to weak title/meta)

**Why This Matters:**
- **Position 11 = page 2 top** → small push gets us to page 1
- 9 impressions in 28 days = consistent demand
- Seasonal relevance (August = post-vacation return)

**Action Plan:**
```html
<!-- CURRENT (guessing based on naming) -->
<title>Hantera stress efter semestern - Neurovibe</title>
<meta name="description" content="Guide om post-semester stress...">

<!-- OPTIMIZED -->
<title>Hantera stress efter semestern med NPF - 7 strategier som fungerar</title>
<meta name="description" content="Återgång till jobbet efter semester? 7 beprövade strategier för att hantera stress och övergångar när du har ADHD, autism eller annan NPF. Gratis checklista.">
```

**Content Additions:**
- Add FAQ schema (5 Q&As):
  - "Varför är det svårt att återgå till jobbet efter semester med ADHD?"
  - "Hur lång tid tar det att bygga nya rutiner efter semester?"
  - "Vilka anpassningar kan hjälpa vid återgång till arbetet?"
  - "Hur hanterar jag energibrist efter semestern?"
  - "Bör jag berätta för chefen om svårigheter med övergångar?"

- Add comparison table:
  | Före semester | Efter semester |
  |---------------|----------------|
  | Planera delegering | Prioritera uppstart |
  | Skala ner vecka 1 | Bygg rutiner gradvis |
  | Dokumentera rutiner | Återta rutiner steg-för-steg |

- Internal links:
  - → Burnout-kalkylator ("Är du i riskzonen för utbrändhet?")
  - → Schema-guide ("Bygg hållbara rutiner")
  - → Fokus Timer ("Återta fokus efter ledighet")

**Expected Impact:**
- Position 11.6 → 7-9 (page 1)
- Impressions 9 → 20-30/month
- Clicks 0 → 2-5/month
- CTR 0% → 10-15%

---

### 2. FK/AF Guide - Expand for "lönebidrag adhd" Query
**Current Performance:**
- Position: 22.0 (page 3)
- Impressions: 8
- Clicks: 0
- Query showing interest: "lönebidrag vid adhd" (5 impressions, position 21.6)

**Why This Matters:**
- **Specific intent:** "lönebidrag adhd" = high-value query (person actively seeking support)
- Page exists but not optimized for this specific term
- Position 22 → easier to move than starting from scratch

**Action Plan:**
1. **Add dedicated H2 section:** "Lönebidrag vid ADHD och autism"
   - What it is (brief explanation)
   - Who qualifies (criteria)
   - How to apply (step-by-step)
   - Common pitfalls (why applications get denied)

2. **Add structured data:**
   ```json
   {
     "@type": "HowTo",
     "name": "Hur ansöker du om lönebidrag vid ADHD",
     "step": [...]
   }
   ```

3. **Internal link:**
   - From index.html (add "Lönebidrag för NPF" to main nav or hero)
   - From lagkrav page (cross-reference employer obligations)

4. **Lead magnet:**
   - "Lönebidrag-ansökan checklista" (PDF download)
   - Capture emails of people applying for support (B2C leads)

**Expected Impact:**
- Position 22 → 12-15 (page 2)
- Impressions 8 → 25+/month
- Clicks 0 → 2-3/month
- New lead source (people applying for lönebidrag)

---

### 3. Data Rapport - Maintain + Expand (Already Performing Well)
**Current Performance:**
- Position: 4.2 ⭐ (TOP 5!)
- Impressions: 4
- Clicks: 1
- CTR: 25% (EXCELLENT)

**Why This Matters:**
- **Already winning** - top 5 position is gold
- High CTR shows strong title/meta
- Low impressions = need more queries to trigger it

**Action Plan:**
1. **Expand content to rank for more queries:**
   - Add section: "NPF i Sverige - statistik 2026" (broader query)
   - Add section: "Hur vanligt är NPF på svenska arbetsplatser?" (FAQ-style)
   - Add comparison: "ADHD vs autism på arbetsplatsen - vad visar data?"

2. **Add more structured data:**
   - DataCatalog schema (mark it as a research report)
   - FAQPage schema (5+ data-related Q&As)

3. **Internal links TO this page:**
   - From all tool pages ("Se vår data-rapport för insikter från X användare")
   - From index.html (prominent "State of Neurodiversity 2026" CTA)
   - From all guides (cite specific stats from rapport)

4. **Promote externally:**
   - Share on LinkedIn (Sim's network, Adviseo page)
   - Submit to Swedish HR forums/groups
   - Pitch to media: "Första svenska rapporten om NPF på arbetsplatsen"

**Expected Impact:**
- Position 4.2 → maintain or improve to 2-3
- Impressions 4 → 20-30/month (more keywords trigger it)
- Clicks 1 → 5-8/month
- Backlinks from shares/citations

---

## 🔍 KEYWORD RESEARCH FROM GSC

### Queries We're Already Ranking For (But Not Clicking)
| Query | Impressions | Position | Opportunity |
|-------|-------------|----------|-------------|
| lönebidrag vid adhd | 5 | 21.6 | Expand FK/AF guide |
| netvibes | 7 | 59.4 | Irrelevant (brand confusion) - ignore |
| neuroguiden | 3 | 62.3 | Competitor - consider creating "vs Neuroguiden" comparison |
| arbetsgivarens ansvar vid funktionsnedsättning | 1 | 32.0 | Add to lagkrav page |

### New Content Gaps (Not Ranking Yet)
Based on related searches and seasonal context:
- "adhd höstplanering" (seasonal, August)
- "inkluderande kickoff" (B2B, fall team meetings)
- "npf studiestart" (students returning)
- "rutiner efter semester adhd" (post-vacation)
- "anpassningar jobb adhd" (evergreen, but we're not ranking)

**Priority:**
1. Höstplanering guide (capture August traffic)
2. Inkluderande kickoff (B2B lead gen)
3. Strengthen "anpassningar jobb adhd" (update existing adhd-anpassningar-jobb.html)

---

## 📊 SCHEMA.ORG AUDIT

### Pages Missing Schema (High Priority)
Run audit:
```bash
cd /data/workspace/projects/neurovibe
grep -L "application/ld\+json" static/*.html | grep -E "(forsakring|lagkrav|adhd-anpassningar|autism-arbetsplatsen|post-semester)"
```

**Expected Missing:**
- forsakringskassan-arbetsformedlingen-stod.html
- lagkrav-anpassningar-arbetsmiljo.html
- adhd-anpassningar-jobb.html
- post-semester-stress-npf.html
- autism-arbetsplatsen-tips-guide.html

**Add Schema Types:**
1. **Article** (all guides):
   ```json
   {
     "@type": "Article",
     "headline": "...",
     "datePublished": "...",
     "author": {"@type": "Organization", "name": "Neurovibe"}
   }
   ```

2. **FAQPage** (all guides with Q&A sections):
   ```json
   {
     "@type": "FAQPage",
     "mainEntity": [...]
   }
   ```

3. **HowTo** (process guides like FK/AF):
   ```json
   {
     "@type": "HowTo",
     "name": "Hur ansöker du om stöd från Försäkringskassan",
     "step": [...]
   }
   ```

---

## 🔗 INTERNAL LINKING STRATEGY

### Current Problem
- Tools exist in isolation (no cross-linking)
- Guides don't link to relevant tools
- Data rapport not linked FROM enough pages

### Hub-and-Spoke Structure

#### Hub 1: Data Rapport (authority page)
**Link TO:**
- All tools mentioned in insights (Burnout-kalkylator, Anpassningsgenerator, etc.)
- All guides that support data findings

**Link FROM:**
- Index.html (hero CTA: "Läs vår forskningsrapport")
- All tool pages (footer: "Se vad data säger om [X]")
- All guides (cite specific stats)

#### Hub 2: Resurser Page (navigation hub)
**Link TO:**
- All guides (categorized: Anställd, Arbetsgivare, Stöd & Rättigheter)
- All tools (categorized: Planering, Diagnos, Stöd)

**Link FROM:**
- Index.html (main nav + footer)
- All guides (footer: "Fler resurser")
- All tools (sidebar: "Relaterade guider")

#### Spoke: Topic Clusters
**Example: ADHD Cluster**
- adhd-anpassningar-jobb.html (pillar page)
  - Links to: adhd-diagnos-guide.html, fokus-timer, anpassningsgenerator
- adhd-diagnos-guide.html
  - Links to: adhd-anpassningar-jobb.html, FK/AF guide, interview guide
- Tools (fokus-timer, etc.)
  - Link to: adhd-anpassningar-jobb.html

**Example: Employer Cluster**
- for-arbetsgivare.html (pillar page)
  - Links to: arbetsgivarpaketet, lagkrav, inkluderande-rekrytering
- lagkrav-anpassningar-arbetsmiljo.html
  - Links to: for-arbetsgivare, FK/AF guide, partner page
- arbetsgivarpaketet.html
  - Links to: all B2B resources

---

## 🎯 QUICK WIN METRICS (2-Week Target)

### Success Criteria
**By 2026-08-19:**
- [ ] Post-semester page: Position 11 → 7-9
- [ ] FK/AF guide: Add lönebidrag section, position 22 → 15-18
- [ ] Data rapport: Impressions 4 → 15+
- [ ] Total clicks: 4 → 10+ (150% increase)
- [ ] Total impressions: 51 → 100+ (96% increase)

### How to Track
```bash
# Run weekly GSC check
python3 /data/workspace/skills/search-console/scripts/gsc_report.py --site sc-domain:neurovibe.se --days 7

# Compare to baseline (2026-08-05):
# - Clicks: 4
# - Impressions: 51
# - Top pages: data-rapport (pos 4.2), post-semester (pos 11.6)
```

---

## 🚀 EXECUTION PRIORITY

### Day 1-2 (This Week)
1. Optimize post-semester page (title, meta, FAQ schema, internal links)
2. Add lönebidrag section to FK/AF guide
3. Schema.org audit (identify all pages missing structured data)

### Day 3-5 (This Week)
4. Add schema to top 5 priority pages
5. Internal linking sprint (hub-and-spoke structure)
6. Create "Höstplanering för NPF" guide (seasonal opportunity)

### Week 2
7. Monitor GSC daily for changes
8. Adjust titles/metas based on CTR data
9. Create "Inkluderande kickoff" B2B guide
10. Promote data rapport externally (LinkedIn, outreach)

---

**Created:** 2026-08-05  
**Data Source:** GSC (28-day window, 4 total clicks, 51 impressions)  
**Next Check:** 2026-08-12 (verify impact of optimizations)
