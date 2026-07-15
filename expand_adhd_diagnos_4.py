import re

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'r', encoding='utf-8') as f:
    content = f.read()

expansion = """
## Del 12: ADHD hos Kvinnor – Den Dolda Diagnosen

En av de viktigaste förändringarna i förståelsen av ADHD under de senaste decennierna, och framförallt fram till 2026, är insikten om att ADHD hos kvinnor ofta ser annorlunda ut än hos män. Historiskt sett var kriterierna utformade utifrån hur pojkar betedde sig, vilket ledde till att generationer av kvinnor missades.

### Varför missas kvinnor?
Flickor och kvinnor med ADHD tenderar att ha en mer "inåtvänd" (ouppmärksam) presentation av diagnosen, tidigare känt som ADD. Istället för att klättra på väggarna eller störa i klassrummet (hyperaktivitet), kanske de drömmer sig bort, har svårt att följa instruktioner eller känner en inre rastlöshet.
- **Maskering:** Kvinnor är ofta experter på att "maskera" sina symtom. De anstränger sig enormt för att passa in i samhällets förväntningar på ordning, empati och social kompetens. Denna konstanta ansträngning leder ofta till total utmattning och misstolkas regelbundet av vården som depression, ångest eller bipolär sjukdom.
- **Utmattningssyndrom som första symptom:** Många kvinnor diagnostiseras med ADHD först efter att de "gått in i väggen" en eller flera gånger. När kraven i vuxenlivet (karriär, barn, hushåll) överstiger deras förmåga att kompensera för sina exekutiva svårigheter, kraschar de.

### Konsekvenser av en Sen Diagnos
Att leva hela livet utan att förstå varför allting känns svårare än för andra leder ofta till en djupgående känsla av skam och låg självkänsla. Många kvinnor internaliserar sina svårigheter och tror att de är lata, dumma eller ostrukturerade. Att äntligen få en diagnos är därför ofta en enorm lättnad, men det kräver också att man bygger upp sin självkänsla på nytt.

## Vanliga Frågor (FAQ) om ADHD-utredning för Vuxna

**1. Hur lång tid tar en ADHD-utredning i offentlig vård?**
År 2026 varierar det kraftigt mellan olika regioner, men du kan tyvärr räkna med mellan 12 och 24 månaders väntetid i stora delar av Sverige.

**2. Täcks en privat utredning av frikortet?**
Nej, som regel bekostar du en privat utredning helt själv (ofta 25 000–40 000 kr). Däremot gäller frikortet och högkostnadsskyddet för *medicineringen* i efterhand, förutsatt att du får receptet från en läkare inom (eller med avtal med) den offentliga vården.

**3. Kan man bli av med sin diagnos?**
ADHD är en livslång funktionsnedsättning (hjärnans struktur är annorlunda), så du "växer inte ifrån" den. Däremot kan symtomen minska och hanteringen förbättras avsevärt med rätt strategier, mognad, medicin och anpassningar, så att den inte längre utgör ett lika stort funktionshinder.

**4. Måste jag berätta för min arbetsgivare?**
Nej, du har ingen laglig skyldighet att berätta om din diagnos. Det är helt upp till dig. Men om du inte berättar kan du heller inte kräva anpassningar enligt diskrimineringslagen (tex flexibla arbetstider eller hjälpmedel).

**5. Påverkar en ADHD-diagnos mitt körkort?**
Transportstyrelsen kräver att du anmäler diagnoser som kan påverka körförmågan. För de flesta med ADHD utgör diagnosen inget hinder för att ha körkort, men du behöver ofta lämna in ett läkarintyg som bekräftar att tillståndet är stabilt (särskilt om du medicinerar).

**6. Kan jag få sjukersättning på grund av ADHD?**
ADHD i sig ger sällan rätt till sjukersättning (förtidspension). Försäkringskassan bedömer din *arbetsförmåga*, inte din diagnos. Målet är i första hand rehabilitering och anpassningar på arbetsplatsen (exempelvis via lönebidrag) för att du ska kunna arbeta.
"""

content = content + expansion

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Expanded content 4 saved to adhd-diagnos-guide-expanded.md")
