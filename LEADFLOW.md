# LEADFLOW.md — Neurovibes lead-maskin

Ett dokument, en sanning: vem vi riktar oss mot, vad vi levererar till var och en,
hur leads fångas, poängsätts och följs upp. Ändrar du erbjudandet på en sida ska
det ändras här också.

Senast uppdaterad: 2026-07-25

---

## 1. Positionering — vad sajten faktiskt levererar

Innan: "vi bygger broar mellan neurodivergent talang och inkluderande
arbetsgivare" och en knapp som heter "Få tillgång". Ingen kunde svara på vad de
faktiskt fick.

Nu, i en mening:

> **Neurovibe är en svensk verktygslåda för NPF i arbetslivet. Medarbetare får
> färdiga anpassningsförslag och verktyg för exekutiv funktion. Chefer och HR får
> rutinmallar, lagkravsunderlag och ett anpassningsbibliotek.**

Det som gör den försvarbar mot konkurrens:

1. **Interaktiva verktyg**, inte artiklar. Ger återkommande besök och egen data.
2. **Svenska regelverk konkretiserade** — AFS 2020:5, diskrimineringslagen, FK/AF.
   Amerikanska ADA-guider hjälper ingen svensk HR-chef.
3. **Egen data** från verktygen, som ingen annan i nischen har.

---

## 2. Målgrupper (ICP)

### Segment A — Arbetsgivare (huvudintäkt)

| | |
|---|---|
| **Vem** | HR-chef, HR-partner, D&I-ansvarig, chef med personalansvar, arbetsmiljöansvarig |
| **Organisation** | 50–5 000 anställda i Sverige. Offentlig sektor och kommun är minst lika intressant som privat. |
| **Utlösande händelse** | Ett pågående ärende med en medarbetare, en förestående inspektion, en rehabprocess, eller en ny D&I-plan |
| **Vad de söker på** | "arbetsanpassning adhd", "afs 2020:5 rutin", "anpassningar autism arbetsplats", "skäliga anpassningar diskrimineringslagen" |
| **Vad de faktiskt vill** | Något att klistra in i ett dokument i dag. Inte förståelse — underlag. |
| **Ingång** | `/for-arbetsgivare.html` |
| **Erbjudande** | Arbetsgivarpaketet (gratis) → genomlysning (offert) → leverantörsmatchning (gratis för dem, betald av leverantören) |

### Segment B — Individ (publik, inte köpare)

| | |
|---|---|
| **Vem** | Medarbetare eller arbetssökande med ADHD, autism eller annan NPF. Även anhöriga. |
| **Utlösande händelse** | Nära utmattning, ny diagnos, ska prata med chefen, återgång efter sjukskrivning |
| **Vad de söker på** | "adhd anpassningar jobb", "orkar inte jobba adhd", "adhd utredning vuxen", "maskering autism" |
| **Ingång** | `/for-medarbetare.html` |
| **Erbjudande** | Verktygen + Executive Function-checklistan (gratis) |
| **Roll i affären** | De är trafiken och datan som gör oss värda att annonsera hos — och ofta den som skickar arbetsgivarsidan vidare till sin chef. De ska aldrig hamna i ett säljflöde. |

### Segment C — Partner/leverantör (betalar)

| | |
|---|---|
| **Vem** | Företagshälsovård, arbetsterapeuter, föreläsare och utbildningsleverantörer inom NPF, akustik och tysta rum (t.ex. kapseltillverkare), kontorsmöbler, HR-system, appar för fokus/tid/planering, digital vård |
| **Vad de vill** | Nå HR-chefer med budget, eller privatpersoner i ett aktivt köpläge |
| **Ingång** | `/partner.html` |
| **Erbjudande** | Sponsrad placering · leadgenerering · verktygssponsring · datasamarbete |

---

## 3. Erbjudanden per segment

| ID (`offer`) | Segment | Vad leaden får | Var |
|---|---|---|---|
| `b2b-anpassningspaket` | arbetsgivare | Rutinmall (AFS 2020:5), anpassningsbibliotek, samtalsmall, lagkravsöversikt, stöd & bidrag | `/for-arbetsgivare.html#arbetsgivarpaket` |
| `b2b-genomlysning` | arbetsgivare | Prioriterad åtgärdslista efter genomgång av deras miljö och rutiner | Offert |
| `datarapport-2026` | individ/arbetsgivare | Observationsdokumentet 2026 (PDF, byggs av `report_nv.build_report_pdf`) | `/data-rapport-2026.html` |
| `partner-mediakit` | partner | Trafik, målgruppsfördelning, format, priser + förslag | `/partner.html#mediakit` |
| `individ-checklista` | individ | Executive Function-checklistan (PDF) | `/for-medarbetare.html#checklista` |

**Varje `offer` med en PDF måste ha en byggare i `report_nv.py`**, kopplad i
`leadengine._attachment_for()`. Saknas den får leaden fel fil — vilket är precis
vad som hände när rapportsidan lovade en rådatarapport och skickade checklistan.

**Att bestämma innan paketet skickas första gången:** arbetsgivarpaketets fem
dokument måste faktiskt finnas. Sidan säljer dem redan. Prioritera i denna
ordning: (1) rutinmall, (2) anpassningsbibliotek, (3) lagkravsöversikt,
(4) samtalsmall, (5) stöd & bidrag — de två första är det som efterfrågas mest.

---

## 4. Så fångas en lead

Ett formulär, ett script, tre endpoints.

```
Guide/verktyg (organisk ingång)
        │  segment-CTA i botten av varje sida
        ▼
Målgruppssida  ──►  <form data-nv-lead data-segment="…" data-offer="…">
                            │  leadflow.js
                            ▼
        POST /api/lead · /api/b2b-lead · /api/partner-lead
                            │
                  leadengine.record_lead()
                     │            │
              scoring A–D    SQLite `leads`
                     │            │
        ┌────────────┘            └──────────► /admin.html (dashboard, CSV)
        ▼
  bekräftelsemejl till leaden  +  notis till ägaren med prio i ämnesraden
```

### Frontend: `static/leadflow.js`

Ett script för alla formulär på sajten. Ersätter de kopierade
`submitLeadMagnet()`-varianterna.

```html
<form data-nv-lead data-segment="arbetsgivare" data-offer="b2b-anpassningspaket"
      data-redirect="auto" data-error="#form-error">
  <input name="email" type="email" required>
  <select name="role">…</select>
  <input type="checkbox" name="consent" required>
  <button type="submit">Skicka</button>
</form>
```

Fältnamn som plockas upp automatiskt: `email`, `name`, `role`, `company`,
`company_size`, `need`, `timeline`, `phone`, `message`, `consent`.

Attribut: `data-segment`, `data-offer`, `data-endpoint`, `data-success`,
`data-error`, `data-redirect` (`"auto"` = tacksidan; utan attributet visas
bekräftelsen inline så att en läsare mitt i en guide inte rycks bort).

**UTM-fångst sker per session, inte per sida.** Kampanjkällan sparas i
`sessionStorage` vid första besöket och följer med även om besökaren klickar
sig vidare två artiklar innan hen fyller i formuläret — vilket är vad de flesta gör.

GA4-events: `lead_form_start` (första fokus i formuläret),
`generate_lead` (lyckat inskick), `lead_thankyou_view`. Skillnaden mellan
`lead_form_start` och `generate_lead` är den enda siffra som visar om ett
formulär är för krångligt.

---

## 5. Lead scoring

Definierad i `leadengine.py` (`ROLE_SCORES`, `SIZE_SCORES`, `NEED_SCORES`,
`TIMELINE_SCORES`). Ändra vikterna där — ingen annanstans.

| Faktor | Max | Logik |
|---|---|---|
| Bas | 10 | Fyllde i ett formulär med flera fält |
| Roll | 30 | HR-chef/ledning högst, "annat" lägst |
| Organisationsstorlek | 25 | 1 000+ högst |
| Behov | 28 | Vill köpa leads > annonsera > utbildning > policy > orienterar sig |
| Tidsram | 20 | Omgående högst |
| Jobbmejl (ej gmail/hotmail m.fl.) | 10 | Signalerar organisation |
| Telefonnummer angivet | 5 | Vill bli kontaktad |
| Fritext > 60 tecken | 5 | Skrev ett eget ärende = högre intent |

**Individ-segmentet poängsätts inte kommersiellt** (fast 10–20p). De är publiken,
inte köparen, och ska aldrig hamna i säljflödet.

### Klasser och SLA

| Klass | Poäng | Åtgärd |
|---|---|---|
| **A** | 78–100 | Personligt mejl eller telefon inom 24h |
| **B** | 55–77 | Personligt mejl inom 3 arbetsdagar |
| **C** | 32–54 | Nurture-sekvens (rapport + case) |
| **D** | 0–31 | Nyhetsbrev |

Klassen står i ämnesraden på ägarnotisen: `[A] Ny arbetsgivare-lead: Volvo Group
– 100p – Ring/mejla personligen inom 24h`. Ingen inloggning behövs för att veta
vad som ska göras med en lead.

Vid återkommande inskick från samma e-post och segment behålls den **högsta**
poängen leaden någonsin fått — en HR-chef som först laddade ner en checklista och
senare fyller i mindre ska inte degraderas.

---

## 6. Databas och drift

Tabellen `leads` i SQLite (`data/neurovibe.db`), skapas idempotent vid varje
skrivning. Unikt index på `(email, segment)` — samma person får finnas i två
segment (man kan vara både medarbetare och chef) men inte dubbelt inom ett.

Om skrivningen fallerar skrivs leaden till `leads/fallback.jsonl` **och** mejlas
till ägaren. En lead ska aldrig kunna försvinna tyst.

### ⚠️ Persistens måste ordnas i produktion

Databasen ligger i containerns filsystem. På Railway innebär det att **alla leads
försvinner vid varje deploy** om inte en volym monteras.

1. Montera en volym i Railway och sätt `NV_DATA_DIR` till dess sökväg.
   `leadengine.py` läser den variabeln och lägger databasen där.
2. `*.db` är numera gitignorerad — annars skriver varje deploy över
   produktionens leads med repots gamla kopia.
3. Exportera CSV från `/admin.html` regelbundet tills volymen är på plats.

**Så verifierar du att volymen faktiskt används.** Det räcker inte att volymen
är monterad — är `NV_DATA_DIR` osatt hamnar skrivningarna i containern ändå, och
det märks inte förrän en deploy har raderat leadsen. Två ställen visar sanningen:

- **Deploy-loggen** vid uppstart: `[nv] lead-databas på monterad volym: …` är
  rätt. `[nv] VARNING: lead-databasen ligger i containern …` betyder att
  variabeln inte är satt.
- **`/admin.html`** visar en röd ruta högst upp så länge något är fel — antingen
  osatt `NV_DATA_DIR` eller saknad SMTP-konfiguration (då går varken
  bekräftelser eller ägarnotiser ut, tyst). Rutan försvinner när båda är rätt.

Sluttest när volymen är på plats: fyll i ett formulär, kontrollera att leaden
syns i dashboarden, gör en ny deploy och se att den fortfarande är kvar.

### Miljövariabler

| Variabel | Används till |
|---|---|
| `NV_DATA_DIR` | Sökväg till monterad volym för databasen |
| `INTERNAL_API_KEY` | Skyddar `/api/admin/*` och låser upp `/admin.html` |
| `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` | Brevo, för bekräftelser och notiser |
| `LEAD_NOTIFY_EMAIL` | Vart ägarnotiser går (default `simon@adviseo.se`) |
| `OPENAI_API_KEY` | Chatt och uppgiftsnedbrytning (sajten startar även utan) |

### Endpoints

| Metod | Väg | Syfte |
|---|---|---|
| POST | `/api/lead` | Generisk (segment i payloaden) |
| POST | `/api/b2b-lead` | Tvingar segment `arbetsgivare` |
| POST | `/api/partner-lead` | Tvingar segment `partner` |
| GET | `/api/admin/leads` | Leads + aggregat (kräver `X-API-KEY`) |
| GET | `/api/admin/leads.csv` | CSV-export |
| POST | `/api/admin/lead-status` | Sätt status på en lead |

Status: `new` → `contacted` → `qualified` → `won` / `lost` / `nurture`.

---

## 7. Förtroende (E-E-A-T) — varför det är en intäktsfråga

Google klassar det här som YMYL. En annonsör betalar dessutom mer för att synas
på en sida som ser trovärdig ut. Men lösningen är inte att tona ner att sajten är
AI-driven till otydlighet — det är att vara så tydlig att en läsare kan bedöma
underlaget själv.

Vad som gjorts:

- **`/redaktionell-policy.html`** — hur innehållet tas fram, vad vi aldrig
  uttalar oss om, hur egen data ska tolkas (självselekterat urval), spelregler
  för sponsring, rättelserutin, och en öppen inbjudan till legitimerade experter.
- **Footern på alla sidor** pekar nu till den sidan i stället för till en
  experimentbeskrivning. Formuleringen: "Innehållet produceras av AI-system inom
  mänskligt satta ramar och utgör inte medicinsk rådgivning."
- **Inga påhittade auktoritetsmarkörer.** Ingen "granskad av"-byline sätts på en
  sida där ingen faktiskt granskat, inga uppfunna kundlogotyper, inga citat.

Det som skulle lyfta auktoriteten mest härifrån, i ordning:

1. **En legitimerad granskare** på de tre tyngsta guiderna (lagkrav, maskering,
   diagnos). Inbjudan ligger redan på policysidan. En arbetsterapeut eller
   psykolog som får sitt namn på tre sidor mot en rimlig ersättning är billigare
   än man tror — och gör att B2B-priserna kan höjas direkt.
2. **Riktiga trafiksiffror i mediakitet.** Se varningen i avsnitt 8.
3. **Citat och länkar till rapporten** från fackförbund eller branschmedia.

---

## 8. ⚠️ Innan du gör outreach — tre saker som inte får hittas på

0. **Inga siffror utan belagd källa.** Rapportsidan presenterade tidigare
   "68% i riskzon" och "82% hög maskeringsgrad" som egen data. Underlaget var
   1 rad i `burnout_data.csv` och 4 rader simulerad `tool_usage` från
   `simulate_tool_usage.py`. Siffrorna är borttagna överallt, inklusive från
   startsidan, en guide och outreach-mallen. Låt dem inte komma tillbaka:
   regelverk får citeras, egen data först när den finns.

1. **Trafiksiffrorna på `/partner.html` är avsiktligt tomma.** Sidan säger att
   aktuella siffror skickas i mediakitet. Fyll i dem från GA4 (`G-YJG1D5GJPR`)
   innan du länkar hit i outreach. En annonsör som upptäcker uppblåsta siffror
   köper aldrig igen — och berättar det för nästa. Se HTML-kommentaren i
   avsnittet "Räckvidd och trafiksiffror".
2. **`/for-arbetsgivare.html` lovar svar inom en arbetsdag** och nämner
   leverantörsmatchning. Det är löften om ditt eget beteende. Antingen håller du
   dem, eller så mjukar du upp formuleringarna.
3. **Arbetsgivarpaketets fem dokument måste finnas** innan det första
   formuläret fylls i. Se avsnitt 3.

---

## 9. Prisförslag (att bekräfta, inte publicerat)

Sidorna säger "pris efter omfattning" med flit — inga siffror är publicerade.
Detta är utgångspunkter för ditt första samtal, baserade på vad svenska
B2B-nischsajter och HR-tjänster normalt tar:

| Vad | Förslag | Kommentar |
|---|---|---|
| Sponsrad placering i en guide | 6 000–15 000 kr/kvartal | Skalar med sidans trafik. Sätt priset först när GA4-siffrorna finns. |
| Verktygssponsring | 12 000–30 000 kr/kvartal | Högre — exponeringen upprepas vid varje användning och i mejlet. |
| Kvalificerad arbetsgivarlead | 800–2 500 kr/lead | Övre spannet för klass A med beskrivet behov och tidsram. Sätt volymtak. |
| Genomlysning (er egen leverans) | 25 000–60 000 kr | Efter omfattning och antal enheter. |
| Datasamarbete i rapporten | 25 000–75 000 kr | Inklusive medavsändarskap. |

Börja i underkanten på de två första försäljningarna för att få referenser att
peka på, och höj sedan.

---

## 10. Kvar att göra

**Innan lansering av leadflödet**
- [x] Montera volym i Railway + sätt `NV_DATA_DIR`, och bekräfta i deploy-loggen
      eller `/admin.html` att den används (avsnitt 6)
- [ ] Verifiera att `SMTP_USER`/`SMTP_PASS` är satta — utan dem skickas inga mejl
      (`mailer.configured()` loggar men kastar inte). Syns som varning i
      `/admin.html`.
- [ ] Skicka ett testinskick per segment och kontrollera att båda mejlen kommer fram
- [x] Producera arbetsgivarpaketets dokument (avsnitt 3)
- [x] Fyll i trafiksiffror i mediakitet (avsnitt 8)

**Nästa iteration av maskinen**
- [x] Migrera de återstående inline-formulären (`verktyg-*.html`,
      `adhd-diagnos-*.html`, `data-rapport-2026.html` m.fl.) till
      `<form data-nv-lead>` med en riktig samtyckesruta. De har nu fått
      attribution och en integritetsnotis, men samtycket registreras inte i
      databasen förrän de har en kryssruta.
- [ ] Nurture-sekvens för klass C (rapport dag 0, case dag 4, verktyg dag 10)
- [ ] `/tack.html` för arbetsgivare: lägg in en kalenderlänk för bokning
- [ ] Segmentera nyhetsbrevet — individ och arbetsgivare ska aldrig få samma mejl
- [ ] Exit-intent på `/for-arbetsgivare.html` — `leadflow.js` exponerar
      `window.nvLeadflow.bind()` och `.track()` så ett dynamiskt inlagt formulär
      kan kopplas in, men själva exit-intent-logiken är inte byggd
