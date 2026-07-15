import re

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide.md', 'r', encoding='utf-8') as f:
    content = f.read()

expansion = """
## Del 5: Rättigheter och Anpassningar efter Diagnos

När du väl har fått din diagnos öppnas dörrar till specifika rättigheter och stöd, både i arbetslivet och samhället i stort. Det är viktigt att känna till vilka lagar som skyddar dig och vilka resurser som finns tillgängliga.

### Diskrimineringslagen och Arbetslivet
Enligt svensk lag klassas ADHD som en funktionsnedsättning. Det innebär att du skyddas av diskrimineringslagen, vilket förbjuder arbetsgivare att missgynna dig på grund av din diagnos. Dessutom har arbetsgivaren en skyldighet att vidta "skäliga stöd- och anpassningsåtgärder" för att du ska kunna utföra ditt arbete på lika villkor.
Dessa anpassningar behöver inte vara kostsamma eller komplicerade. De kan inkludera:
- **Flexibla arbetstider:** Möjlighet att anpassa start- och sluttider för att optimera när du är mest fokuserad.
- **Tydlig kommunikation:** Skriftliga instruktioner istället för (eller som komplement till) muntliga.
- **Minskade distraktioner:** Tillgång till ett tyst rum, möjlighet att arbeta hemifrån vissa dagar, eller brusreducerande hörlurar.
- **Tekniska hjälpmedel:** Programvara för planering, text-till-tal, eller specifika kalenderverktyg.

### Försäkringskassan och Arbetsförmedlingen
Om du har nedsatt arbetsförmåga på grund av din ADHD finns det olika typer av stöd att få:
- **Lönebidrag:** Arbetsförmedlingen kan bevilja lönebidrag till en arbetsgivare. Detta är en ekonomisk kompensation som gör det lättare för arbetsgivaren att anställa eller behålla en person med nedsatt arbetsförmåga, och ge utrymme för att arbetstakten kanske inte alltid är 100%.
- **Arbetshjälpmedel:** Du kan ansöka om bidrag från Försäkringskassan (om du varit anställd över ett år) eller Arbetsförmedlingen för specifika hjälpmedel som du behöver för att klara ditt arbete.
- **Rehabilitering:** Försäkringskassan kan vara inblandad i att samordna rehabiliteringsinsatser om du varit sjukskriven på grund av utmattning, vilket är vanligt bland vuxna med odiagnostiserad ADHD.

## Del 6: Medicinering och Behandlingsalternativ

För många vuxna är medicinering en central del av behandlingen för ADHD, men det är sällan den enda lösningen. En kombinerad ansats brukar ge bäst resultat.

### Centralstimulerande Läkemedel
De vanligaste medicinerna för ADHD i Sverige är centralstimulerande medel, såsom metylfenidat (t.ex. Concerta, Ritalin) eller lisdexamfetamin (t.ex. Elvanse). Dessa fungerar genom att öka tillgången på signalsubstanserna dopamin och noradrenalin i hjärnan, vilket förbättrar fokus, minskar impulsivitet och ökar uthålligheten.
- **Individuell anpassning:** Det kan ta tid att hitta rätt medicin och rätt dos. Biverkningar som minskad aptit, sömnsvårigheter och ökad puls är vanliga inledningsvis, och det krävs noggrann uppföljning av läkare.

### Icke-stimulerande Läkemedel
För de som inte tolererar centralstimulerande medel, eller där dessa inte ger tillräcklig effekt, finns icke-stimulerande alternativ som atomoxetin (t.ex. Strattera) eller guanfacin (t.ex. Intuniv). Dessa tar ofta längre tid innan de ger full effekt.

### Psykologisk Behandling
- **KBT (Kognitiv Beteendeterapi):** Speciellt anpassad KBT för vuxna med ADHD fokuserar på praktiska strategier för planering, tidsorganisation och problemlösning. Det hjälper också till med att hantera ångest eller låg självkänsla som ofta följer med diagnosen.
- **Arbetsterapi:** En arbetsterapeut kan hjälpa till att strukturera vardagen, hitta rätt hjälpmedel och skapa rutiner som fungerar långsiktigt.
- **Coaching:** Vissa regioner, eller privata aktörer, erbjuder ADHD-coaching. Detta är mer praktiskt inriktat än terapi och syftar till att hjälpa individen att nå specifika mål i vardagen eller arbetslivet.

## Del 7: Att Leva med Diagnosen

Att få en ADHD-diagnos som vuxen beskrivs ofta som en berg-och-dalbana. Det är vanligt att känna en blandning av lättnad ("Det var inte mitt fel!"), sorg över den tid som varit ("Tänk om jag vetat detta tidigare"), och osäkerhet inför framtiden.

- **Acceptera din hjärna:** Det viktigaste steget är att sluta försöka tvinga in dig själv i en form som är gjord för neurotypiska personer. Lär dig hur din unika hjärna fungerar.
- **Kommunicera dina behov:** Var inte rädd för att berätta för arbetsgivare, partners och vänner vad du behöver. De flesta vill hjälpa till, men de kan inte läsa dina tankar.
- **Hitta ditt "hyperfokus":** ADHD är inte bara en samling utmaningar. Många med diagnosen har en fantastisk förmåga till "hyperfokus" på uppgifter de finner intressanta, är extremt kreativa och har hög energi. Lär dig att kanalisera dessa styrkor.
"""

content = content + expansion

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Expanded content saved to adhd-diagnos-guide-expanded.md")
