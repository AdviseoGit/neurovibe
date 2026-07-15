import re

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'r', encoding='utf-8') as f:
    content = f.read()

expansion = """
## Del 10: ADHD och Relationer

Att leva med ADHD påverkar inte bara arbetslivet och studier, utan även hur vi fungerar i relationer. För många vuxna kan relationer vara både en källa till stor glädje och en arena för frekventa missförstånd.

### Utmaningar i Parrelationer
- **Glömska och distraktion:** Att glömma överenskommelser, årsdagar eller att inte verka lyssna under samtal kan av en partner misstolkas som bristande intresse eller kärlek. I själva verket handlar det ofta om bristande arbetsminne och en hjärna som lätt distraheras av inre eller yttre stimuli.
- **Impulsivitet:** Impulsiva kommentarer, plötsliga utbrott eller oövertänkta ekonomiska beslut kan skapa spänningar. Det är viktigt för båda parter att förstå att impulsiviteten är en del av diagnosen, även om det inte ursäktar sårande beteende. Man måste tillsammans hitta strategier, som att ta en "time-out" innan viktiga beslut fattas.
- **Ojämnt ansvar i hemmet (Mental Load):** Eftersom planering och organisation ("exekutiva funktioner") är kärnproblemet vid ADHD, hamnar ofta det administrativa ansvaret för hushållet ("the mental load") oproportionerligt mycket på den partner som inte har ADHD. Detta kan leda till förbittring.

### Strategier för Bättre Relationer
- **Öppen och ärlig kommunikation:** Prata om hur ADHD påverkar just er relation. Använd "jag"-budskap ("Jag känner mig osedd när du tittar på telefonen när vi pratar") istället för anklagelser ("Du lyssnar aldrig").
- **Tydlig ansvarsfördelning:** Skapa system för hushållssysslor som inte bygger på minnet. Använd gemensamma digitala kalendrar, scheman på kylskåpet och automatisera räkningar. Dela upp uppgifter efter styrkor – den med ADHD kanske är sämre på att komma ihåg att tvätta, men fantastisk på att ta initiativ till roliga utflykter.
- **Parterapi med ADHD-fokus:** Om relationen kämpar kan en parterapeut med kunskap om neuropsykiatriska funktionsnedsättningar vara till stor hjälp. De kan hjälpa er att bygga broar av förståelse och hitta konkreta verktyg.

## Del 11: Ekonomi och ADHD – Att Hantera Impulsiviteten

Ett ofta förbisett, men högst verkligt, problem för vuxna med ADHD är ekonomin. Impulsivitet och svårigheter med långsiktig planering kan leda till överkonsumtion, obetalda räkningar och i värsta fall skuldsättning.

### Varför är ekonomi svårt?
För en ADHD-hjärna som ständigt letar efter stimulans (dopamin), kan shopping ge en snabb och stark belöning. Känslan av att köpa något nytt ger en tillfällig kick, vilket kan leda till att man köper saker man varken behöver eller har råd med. Dessutom gör bristen på exekutiva funktioner att det är svårt att hålla koll på förfallodatum och budgetar. Det är helt enkelt för tråkigt och kräver för mycket ihållande koncentration.

### System för Ekonomisk Stabilitet
- **Automatisera allt:** Lägg in alla återkommande räkningar på autogiro eller e-faktura. Målet är att minska antalet aktiva beslut du behöver fatta kring din ekonomi varje månad.
- **Inför en "karens-tid":** För att undvika impulsiva köp, skapa en regel för dig själv: Om något kostar mer än ett visst belopp (t.ex. 500 kr), måste du vänta 24 eller 48 timmar innan du genomför köpet. Under den tiden hinner den initiala impulsen oftast lägga sig.
- **Enkla budgetar:** Undvik komplicerade Excel-ark om du vet med dig att du aldrig kommer att uppdatera dem. Använd istället appar som visuellt visar hur mycket pengar du har kvar att spendera varje vecka (så kallade "kuvert-system" i digital form).
- **Professionell hjälp:** Om ekonomin har kraschat, tveka inte att söka hjälp. Kommunens budget- och skuldrådgivare är gratis och har tystnadsplikt.

## Sammanfattning: Ett Liv i Balans

Att få en ADHD-diagnos som vuxen är ofta startskottet för en omorientering av hela livet. Det är en process som kräver tålamod, självmedkänsla och ibland en ganska stor portion humor. 

Genom att förstå hur din specifika hjärna fungerar, söka rätt medicinskt stöd, implementera anpassningar på din arbetsplats och bygga stabila system för din ekonomi och dina relationer, kan du minska stressen avsevärt. Kom ihåg att målet inte är att bli "neurotypisk" eller att bota din ADHD, utan att skapa en tillvaro där du kan blomstra på dina egna villkor. Dina styrkor är många – din kreativitet, din förmåga att tänka utanför boxen och din passion – och med rätt förutsättningar kan de bli din största tillgång.
"""

content = content + expansion

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Expanded content 3 saved to adhd-diagnos-guide-expanded.md")
