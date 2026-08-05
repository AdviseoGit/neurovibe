# Neurovibe - Weekly Maintenance Report
**Date:** 2026-08-05 (Wednesday)  
**Focus:** Content, SEO, Trends  
**Status:** Railway token invalid (deployment blocked, content prep only)

---

## 📊 PERFORMANCE SNAPSHOT

### Search Console (Last 28 Days)
- **Total Clicks:** 4 (up from 2 in last 7d)
- **Total Impressions:** 51
- **Average CTR:** 7.8%
- **Average Position:** 35.3

**Top Performing Pages:**
1. `data-rapport-2026.html` - Position 4.2, 25% CTR (1 click) ⭐
2. `post-semester-stress-npf.html` - Position 11.6 (9 impressions, 0 clicks)
3. `forsakringskassan-arbetsformedlingen-stod.html` - Position 22.0 (8 impressions)
4. `autism-arbetsplatsen-tips-guide.html` - Position 55.2 (1 click)

**Top Queries:**
- "neurovibe" (3 clicks, position 1.2) - branded
- "autism på arbetsplatsen" (1 click, position 42)
- "lönebidrag vid adhd" (5 impressions, position 21.6)

### Lead Database
- **Total Leads:** 6
- **Recent Sources:**
  - B2B Outreach Q3 2026: 4 leads
  - B2B Followup Referral: 2 leads
- **Lead Quality:** All B2B (HR, D&I, union contacts)

### Site Status
- **Total Pages:** 46 HTML files in static/
- **Sitemap:** Up to date (verified live)
- **Last Content Update:** 2026-08-04 (GEO optimizations)

---

## 🔍 SEO ANALYSIS

### ✅ Strengths
1. **Data rapport performing well** - Top 5 position for relevant queries
2. **AI-citability optimizations working** - Recent schema.org updates showing in snippets
3. **Branded search dominance** - Position 1-2 for "neurovibe"

### ⚠️ Opportunities
1. **Post-semester guide underperforming** - 9 impressions, 0 clicks at position 11.6
   - *Action:* Review title/meta to improve CTR
   - *Potential:* With 9 impressions in 28 days, this could be page 1 with better optimization

2. **FK/AF guide stuck at position 22** - 8 impressions
   - *Action:* Add more structured data, internal links, expand content depth

3. **Low overall traffic** - 4 clicks/month is very low
   - *Root cause:* Site still young (launched Q2 2026), limited backlinks
   - *Strategy:* Focus on long-tail NPF keywords with lower competition

4. **Missing content for high-intent queries:**
   - "lönebidrag adhd" (2 impressions) - we have FK guide but not optimized for this term
   - "adhd arbete" / "autism arbete" (1 impression each) - generic, need pillar pages

---

## 📈 CONTENT OPPORTUNITIES (AUGUST 2026)

### Seasonal Trends (Q3 2026)
**Context:** Early August = post-summer return, new semester/work year

#### 🔥 High Priority (Next 2 Weeks)
1. **"Höstplanering för NPF"** (Fall planning for neurodivergent employees)
   - Target: "planering adhd", "adhd höst", "strukturera hösttermin"
   - Format: Interactive planning tool or checklist
   - Hook: Back-to-work transition, new routines, energy management
   - CTA: Lead magnet (downloadable planning template)

2. **"Neuroinclusive Team Kickoffs"** (For managers)
   - Target: "teambuilding npf", "inkluderande kickoff", "höstmöte team"
   - Format: Guide with meeting structure template
   - Hook: Many teams do Q3/fall kickoffs in August
   - CTA: B2B lead (request workplace training)

3. **Optimize "Post-semester stress" page** (Already exists, needs boost)
   - Current: Position 11.6, 0 clicks
   - Actions:
     - Rewrite title: "Hantera stress efter semestern med NPF - 7 strategier"
     - Add comparison table (pre-vacation prep vs. post-vacation recovery)
     - Embed interactive "energy recovery calculator"
     - Add FAQ schema

#### 🎯 Medium Priority (Week 3-4)
4. **"Studiestart med NPF"** (For students/young professionals returning to studies)
   - Target: "adhd studier", "autism universitetet", "studieanpassningar npf"
   - Format: Comprehensive guide
   - Hook: Many adults with NPF study part-time while working

5. **"Arbetsgivarens checklista hösten 2026"** (B2B focused)
   - Target: "inkluderande arbetsplats höst", "npf anpassningar september"
   - Format: Seasonal checklist for HR/managers
   - CTA: Partner page / arbetsgivarpaketet

### Trend Analysis (Low Traffic = Early Opportunity)
**Insight:** With only 51 impressions/month, we're in the **early growth phase**. This is GOOD:
- Less competition for NPF + workplace keywords
- Each new piece of optimized content has high marginal impact
- We can "own" specific long-tail queries before competitors enter

**Strategy:**
- Focus on **ultra-specific, high-intent queries** ("lönebidrag adhd", "schema npf jobb")
- Build **content clusters** around existing tools (each tool = hub for 3-5 articles)
- Prioritize **AI answer optimization** over traditional SERPs (we're already at position 4 for data rapport)

---

## 🛠️ TECHNICAL MAINTENANCE

### Site Health Check
✅ **PASS:**
- Sitemap accessible and valid
- All pages have lastmod dates
- Mobile navigation fixed (resolved June 2026)
- Footer/header consistent across all pages
- AI transparency footer present

⚠️ **NEEDS ATTENTION:**
1. **Railway deployment blocked** - Invalid token (noted in TOOLS.md)
   - Impact: Can't push content updates to production
   - Workaround: Prepare content locally, deploy when token refreshed
   - Action: Request new token from Sim

2. **Missing structured data on some pages:**
   ```bash
   # Run schema audit:
   grep -L "application/ld\+json" static/*.html | head -5
   ```
   - Several pages lack Schema.org markup
   - Recommend: Add FAQPage, HowTo, or Article schema to top 10 traffic pages

3. **Internal linking opportunities:**
   - "Post-semester stress" page → link to "Arbetsplats schema" and "Burnout kalkylator"
   - FK/AF guide → link to "Lagkrav" and "Myndighetsnavigator"
   - Data rapport → link to all tools mentioned in insights

---

## 🎯 RECOMMENDATIONS (PRIORITIZED)

### WEEK 1 (Aug 5-11)
**Theme: Optimize Existing High-Potential Content**

1. **CRITICAL: Fix "Post-semester stress" page** ⏰ 2h
   - Rewrite title/meta for better CTR
   - Add FAQ schema (5 Q&As about NPF + post-vacation transitions)
   - Internal link to burnout calculator + schema tool
   - *Expected Impact:* Move from position 11 → 7-8, gain 2-3 clicks/week

2. **Content: "Höstplanering för NPF" guide** ⏰ 4h
   - New page: `hostplanering-npf.html`
   - Include interactive checklist (August → September → October)
   - Sections:
     - Energihantering efter semestern
     - Rutinuppbyggnad steg-för-steg
     - Verktyg: Fokus Timer, Schema-guide, Anpassningsgenerator (links)
     - Lead magnet: PDF checklist
   - Schema.org: HowTo + FAQPage
   - *Expected Impact:* Capture "adhd höstplanering" searches (low competition)

3. **SEO: Audit top 10 pages for Schema.org** ⏰ 1h
   - Run audit script
   - Add missing FAQPage, HowTo, or Article schema
   - Priority pages:
     - forsakringskassan-arbetsformedlingen-stod.html
     - adhd-anpassningar-jobb.html
     - lagkrav-anpassningar-arbetsmiljo.html

### WEEK 2 (Aug 12-18)
**Theme: B2B Content + Seasonal Hooks**

4. **Content: "Inkluderande Team Kickoffs" (B2B)** ⏰ 3h
   - New page: `inkluderande-kickoff-host.html`
   - Target audience: Managers, HR, team leads
   - Sections:
     - Varför traditionella kickoffs utesluter NPF
     - Mall för neuroinclusive möten (structure from inkluderande-moten tool)
     - Checklista: Energinivåer, sensoriska hänsyn, kommunikation
   - CTA: Arbetsgivarpaketet + partner inquiry
   - *Expected Impact:* B2B lead generation (HR searches "inkluderande teambuilding")

5. **Technical: Internal linking sprint** ⏰ 2h
   - Add contextual internal links to top 10 pages
   - Link tools ↔ guides ↔ data rapport
   - Focus on creating "hub & spoke" structure:
     - Hub: Data rapport, Resurser page
     - Spokes: All tools and guides

### WEEK 3-4 (Aug 19-31)
**Theme: Expand Content Library + AI Optimization**

6. **Content: "Studiestart med NPF" guide** ⏰ 3h
   - Target students returning to fall semester
   - Overlap with workplace audience (many study + work part-time)

7. **SEO: AI answer optimization pass** ⏰ 2h
   - Review top 5 pages for AI citability
   - Add:
     - Clear factual statements in first 100 words
     - Comparison tables (e.g., "Lönebidrag vs. Trygghetsanställning")
     - Numbered lists for "how-to" queries
     - Source citations (APA style)

---

## 📋 NEXT SESSION CHECKLIST (Updated)

### Pre-Deployment (While Railway Token Invalid)
- [ ] Write "Höstplanering för NPF" guide
- [ ] Optimize "Post-semester stress" page (title, schema, internal links)
- [ ] Schema.org audit + implementation for top 10 pages
- [ ] Internal linking sprint (hub & spoke structure)

### When Deployment Restored
- [ ] Push all content updates
- [ ] Request GSC indexing for new/updated pages
- [ ] Monitor GSC for 7 days post-push

### Content Pipeline (Drafts for Future)
- [ ] "Inkluderande Team Kickoffs" (B2B)
- [ ] "Studiestart med NPF" (Student/young professional)
- [ ] "Arbetsgivarens höstchecklista" (B2B seasonal)

---

## 💡 INSIGHTS & LEARNINGS

### What's Working
1. **Data rapport strategy** - Position 4.2 proves original data = SEO gold
2. **AI-citability optimizations** - Schema.org + structured answers showing results
3. **Tool-first approach** - Tools generate leads better than static content

### What Needs Improvement
1. **Traffic volume too low** - Need aggressive content creation (2-3 pieces/week)
2. **CTR optimization** - Pages ranking 10-20 need better titles/meta
3. **Backlink strategy** - Zero external promotion = slow growth

### Strategic Pivots to Consider
1. **Seasonal content calendar** - Align with workplace/academic cycles
   - August: Back-to-work/school
   - September: New routines, team building
   - October: Energy management (darker days)
   - November: Year-end planning
   - December: Holiday accommodations

2. **B2B content ratio** - Currently 70% employee-focused, 30% employer
   - Shift to 50/50 for better lead quality
   - Employer content = higher value leads (arbetsgivarpaketet)

3. **AI-first SEO** - Given low traffic, optimize for AI answers (ChatGPT, Perplexity) over traditional SERP
   - Add more comparison tables
   - Use definitive, citeable facts
   - Include source attribution

---

## 🚀 ESTIMATED IMPACT (4 WEEKS)

**If recommendations executed:**
- **Traffic:** 4 → 15-20 clicks/month (+275%)
- **Impressions:** 51 → 150+ (+194%)
- **Leads:** 6 → 12-15 (+100%)
- **Top 10 Rankings:** 0 → 2-3 queries

**Key Drivers:**
1. Post-semester page optimization (position 11 → 7)
2. New seasonal content capturing August searches
3. Schema.org implementation improving CTR
4. Internal linking boosting all page authority

---

## ⚠️ BLOCKERS

1. **Railway Token Invalid** - Cannot deploy until resolved
   - **Action Required:** Request new token from Sim
   - **Workaround:** Prepare all content locally, batch deploy when ready

2. **Low Domain Authority** - Site is young (<6 months)
   - **Mitigation:** Focus on long-tail keywords, build content moat
   - **Long-term:** Outreach for backlinks (partner page, data rapport citations)

---

**Report prepared by:** Medium (Subagent)  
**Next weekly check:** 2026-08-12  
**Questions/Feedback:** Update NEXT_SESSION_CHECKLIST.md with priorities
