# SITE_VISION.md — Neurovibe

## Vision Statement
Neurovibe.se ska vara Sveriges ledande, mest trovärdiga och praktiskt användbara resurs för neurodivergens på arbetsplatsen. Vi är inte en blogg — vi är en operativ plattform som ger anställda, chefer och företag de verktyg, data och insikter de behöver för att bygga genuint neuroinkluderande och högpresterande team.

Vår "moat" är egeninsamlad, anonymiserad data från våra verktyg, som vi använder för att publicera unika, datadrivna rapporter som ingen annan i nischen kan matcha.

**Erbjudandet i en mening:** Neurovibe är en svensk verktygslåda för NPF i arbetslivet — medarbetare får färdiga anpassningsförslag och verktyg för exekutiv funktion, chefer och HR får rutinmallar, lagkravsunderlag och ett anpassningsbibliotek.

Målgrupper, erbjudanden, lead scoring, SLA och prissättning: se **[LEADFLOW.md](LEADFLOW.md)**.

## Målbild (När vi är #1)
- **Innehåll:** Vi har 3-5 djupa, ständigt uppdaterade innehållspelare (t.ex. "Anpassningar", "Chefsguiden", "Rättigheter & Stöd") som täcker sökintentionen för våra kärnämnen.
- **Verktyg:** Vi har en svit av 3-4 interaktiva verktyg (t.ex. "Burnout-kalkylator", "Anpassnings-checklista", "Mötes-prep") som besökare använder och delar.
- **Leadflow:** Vår primära lead-magnet är inte en PDF, utan tillgång till "Pro"-versioner av våra verktyg eller en djupare data-rapport. E-postlistan är segmenterad (Anställd, Chef, HR).
- **Data:** Vi publicerar en årlig "State of Neurodiversity at Work" rapport baserad på vår egen data, vilket cementerar vår position som thought leader.
- **Design/UX:** Sajten är 100% enhetlig, professionell, snabb och mobilanpassad. Varumärket är igenkännbart och inger förtroende.

## Milstolpar till Visionen
1.  **[ ] Grundläggande Professionalism (Q2 2026):**
    -   [ ] Enhetlig header och footer på ALLA sidor.
    -   [ ] Enhetlig stilmall (CSS/Tailwind) applicerad på ALLA sidor.
    -   [ ] Mobilanpassning verifierad på ALLA sidor.
    -   [ ] Alla sidor finns med i `sitemap.xml`.
    -   [ ] Grundläggande teknisk SEO är på plats (titles, metas, canonicals, robots.txt).

2.  **[ ] Datafångst & Första Verktyget (Q3 2026):**
    -   [ ] Ett första interaktivt verktyg (t.ex. "Uppgiftsnedbrytaren") är live.
    -   [ ] Verktyget har en fungerande backend-endpoint som SPARAR (anonymiserad) input/output.
    -   [x] Lead-formulär (waitlist) är live och kopplat till en fungerande e-posthantering.

3.  **[ ] Innehållspelare & SEO-fäste (Q4 2026):**
    -   [ ] Skapa och publicera den första innehållspelaren (t.ex. en komplett guide till "ADHD-anpassningar på jobbet" som samlar all relaterad information).
    -   [ ] Uppnå topp 10-ranking för minst 3 av våra primära sökord.
    -   [ ] Internlänkningen är strategiskt uppbyggd för att stödja innehållspelarna.

4.  **[x] Publicera Första Data-rapporten (Q1 2027):**
    -   [x] Analysera insamlad data från verktyg/leads.
    -   [x] Skapa en landningssida med den första "Neurovibe Insights" rapporten.
    -   [x] Använda rapporten som lead-magnet för att accelerera list-tillväxt.

5.  **[ ] Expansion & Auktoritet (Q2 2027):**
    -   [x] Bygga ut verktygssviten med ett andra verktyg (har nu 5 st).
    -   [ ] Börja outreach för att få rapporten citerad och länkad.
    -   [ ] Etablera en process för att löpande uppdatera innehållspelare och data.

6.  **[ ] Lead-maskin & tydlighet (Q3 2027):**
    -   [x] Tydlig målgruppsrouter på startsidan (medarbetare / arbetsgivare / partner).
    -   [x] Egen landningssida per segment med konkret erbjudande och eget formulär.
    -   [x] Segmenterad lead-fångst med scoring A–D, SLA och ägarnotis med prio.
    -   [x] Admin-dashboard med pipeline, status och CSV-export.
    -   [x] Redaktionell policy för E-E-A-T i stället för en ren experimentbeskrivning.
    -   [ ] Persistent volym för lead-databasen i produktion (`NV_DATA_DIR`).
    -   [ ] Producera arbetsgivarpaketets fem dokument.
    -   [ ] Knyta en legitimerad granskare till de tre tyngsta guiderna.
    -   [ ] Fylla mediakitet med verkliga GA4-siffror innan partner-outreach.


## DESIGN-SKULD (rapporterad av Sim 2026-06-11 — HÖGSTA PRIORITET)
- [x] Mobilmenyn passar INTE skärmen (Löst 2026-06-16 med gemensam JS-funktion och mobile-menu-btn). — fixa hamburgermenyn/navigationen så den ryms, öppnas/stängs korrekt och är tap-vänlig på 360px-bredd. Verifiera mot CSS:en, anta inget.
- [x] Navigeringsöversyn enligt design-nordstjärnan (max 2 klick, inga återvändsgränder). (Åtgärdat 2026-06-16: Enhetlig footer och JS-mobilmeny impl. på alla sidor)

- [x] Enhetlig stilmall för alla verktyg och artiklar (Löst 2026-06-17).