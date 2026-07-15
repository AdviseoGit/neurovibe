import re

with open('/data/workspace/projects/neurovibe/content/arbetsprovning-2026-forsakringskassan.md', 'r', encoding='utf-8') as f:
    content = f.read()

expansion = """
## Del 2: Samarbetet mellan Arbetsförmedlingen och Försäkringskassan 2026

Ett av de stora problemen historiskt har varit att individen bollats mellan Försäkringskassan och Arbetsförmedlingen. Som neurodivergent är detta ofta katastrofalt, då den administrativa bördan och oförutsägbarheten kan utlösa enorm stress och ytterligare nedsatt arbetsförmåga.

### Den Nya Samordningslagen (2026)
Under 2026 har en ny riktlinje implementerats som syftar till att minska glappet. Om din arbetsprövning inte fungerar som tänkt, ska du inte längre per automatik skrivas ut från sjukförsäkringen och hamna i ett vakuum.
- **Tidig gemensam kartläggning:** Innan arbetsprövningen ens påbörjas ska både en representant från Försäkringskassan (personlig handläggare) och en SIUS-konsulent (Särskild stödperson för introduktion och uppföljning) från Arbetsförmedlingen vara involverade om behovet finns.
- **Sömlös övergång:** Om arbetsprövningen visar att du har viss arbetsförmåga, men inte i ditt ordinarie yrke, aktiveras snabbspåret till Arbetsförmedlingens program för arbetshjälpmedel och lönebidrag.

### Lönebidrag - En trygghet för båda parter
När arbetsprövningen övergår i en anställning är **lönebidrag** ofta nyckeln till hållbarhet.
1. **Vad är det?** Ett ekonomiskt bidrag till arbetsgivaren som kompenserar för att du kanske arbetar långsammare, behöver fler pauser eller att arbetsgivaren behöver lägga tid på extra handledning.
2. **Hur bedöms det?** Det bedöms utifrån din *arbetsförmåga i relation till det specifika arbetet*. Det är inte kopplat till din diagnos i sig, utan till hur väl du kan utföra arbetsuppgifterna med dina utmaningar (t.ex. nedsatt arbetsminne eller stresskänslighet).
3. **Nivåer:** 2026 kan lönebidraget anpassas mer dynamiskt än tidigare, och taket för den bidragsgrundande lönen har justerats för att matcha dagens löneläge bättre.

## Del 3: Konkreta Tips för Möten med Myndigheter

Möten med Försäkringskassan är ofta ångestfyllda för personer med ADHD eller autism. Här är strategier för att hantera dem:

- **Ha alltid någon med dig:** En anhörig, vän eller ett personligt ombud. De behöver inte ens prata; deras uppgift är att föra anteckningar och vara ditt externa minne. Personer med ADHD riskerar att "frysa" eller säga ja till saker de inte kan hantera under press.
- **Skriv ner allt INNAN:** Gör en lista över dina svårigheter *på en riktigt dålig dag*. Myndigheter behöver veta hur det fungerar när det är som sämst, inte hur du presterar de timmar du lyckas hyperfokusera.
- **Be om skriftlig kommunikation:** Du har rätt att begära att viktiga beslut och överenskommelser tas skriftligt. Om din handläggare ringer dig, be dem vänligt men bestämt att skicka ett meddelande i portalen istället så att du i lugn och ro kan läsa och processa informationen.

## Del 4: Rättigheter till Arbetshjälpmedel (Vem betalar vad?)

En vanlig källa till förvirring är vem som faktiskt ska betala för anpassningar och hjälpmedel på arbetsplatsen.

1. **Arbetsgivarens ansvar:** Enligt diskrimineringslagen (bristande tillgänglighet) ska arbetsgivaren stå för "skäliga" anpassningar. Det kan vara brusreducerande hörlurar, en egen tyst arbetsplats, eller inköp av mjukvara som t.ex. rättstavningsprogram eller planeringsverktyg.
2. **Försäkringskassan:** Om du varit anställd *mer än 12 månader* hos samma arbetsgivare är det Försäkringskassan du (och arbetsgivaren) söker bidrag för arbetshjälpmedel hos. Detta gäller dyrare hjälpmedel, t.ex. specialanpassade kontorsstolar (vid komorbiditet) eller avancerade kognitiva hjälpmedelsprogram.
3. **Arbetsförmedlingen:** Om du är ny på jobbet (mindre än 12 månader) eller arbetssökande, är det Arbetsförmedlingen som ska stå för arbetshjälpmedlen.

Genom att ha koll på dessa nya regler och ansvarsfördelningar från 2026 kan du säkerställa att du får det stöd du har rätt till, utan att behöva bränna ut dig på byråkrati.
"""

content = content + expansion

with open('/data/workspace/projects/neurovibe/content/arbetsprovning-2026-forsakringskassan-expanded.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Expanded content saved to arbetsprovning-2026-forsakringskassan-expanded.md")
