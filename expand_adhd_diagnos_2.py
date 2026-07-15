import re

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'r', encoding='utf-8') as f:
    content = f.read()

expansion = """
## Del 8: Navigera Vården och Samhället - Praktiska Tips

När du står inför en ADHD-utredning eller nyligen har fått en diagnos kan vårdsystemet kännas överväldigande. Här är några praktiska råd för att hantera processen.

### Förbered dig inför läkarbesök
Läkare har ofta begränsat med tid. För att få ut det mesta av dina besök:
- **Dokumentera din vardag:** För en loggbok under några veckor. Skriv ner situationer där du upplever svårigheter (t.ex. glömde viktiga papper, tappade koncentrationen under ett möte, impulsivt avbröt någon).
- **Använd standardiserade skattningsskalor:** Förutom ASRS v1.1, kan du titta på Wender Utah Rating Scale (WURS) för att bedöma symtom i barndomen, och ta med resultaten.
- **Ta med en närstående:** En partner, förälder eller nära vän kan ofta ge ett viktigt utifrånperspektiv på dina symtom som läkaren behöver höra. De kan också hjälpa dig att minnas vad som sades under mötet.

### Hantera väntetider
Under väntan på utredning eller behandling, som kan vara lång, kan du börja implementera egna strategier:
- **Strukturera din miljö:** Minska onödiga distraktioner i ditt hem och på din arbetsplats. En ren och välorganiserad miljö kan avlasta din arbetsminne.
- **Externalisera minnet:** Lita inte på din hjärna för att komma ihåg möten eller uppgifter. Använd kalendrar, larm på telefonen, visuella checklistor och "post-it"-lappar.
- **Sök kunskap och gemenskap:** Det finns många bra böcker om vuxen-ADHD. Dessutom kan patientföreningar, som Riksförbundet Attention, erbjuda ovärderligt stöd, kunskap och en känsla av gemenskap med andra i liknande situationer.

## Del 9: Framtiden för Neurodiversitet och ADHD

Synen på ADHD och neurodiversitet förändras snabbt i Sverige och globalt. År 2026 ser vi flera positiva trender:
- **Från bristmodell till styrkebaserad modell:** Fler arbetsgivare börjar förstå att neurodivergenta individer, inklusive de med ADHD, för med sig unika styrkor som kreativitet, innovationsförmåga och snabbtänkthet.
- **Tekniska innovationer:** Framväxten av AI och avancerade digitala verktyg erbjuder nya sätt att kompensera för exekutiva svårigheter. Smarta assistenter, tidsplaneringsalgoritmer och adaptiva arbetsmiljöer blir allt vanligare.
- **Ökad medvetenhet och minskat stigma:** Med fler offentliga personer som pratar öppet om sin diagnos, och ökad kunskap i samhället, minskar skammen och stigmateiseringen kring att ha ADHD.

Att förstå sin ADHD är ett livslångt projekt. Diagnosen är en nyckel som hjälper dig att öppna dörren till en bättre förståelse av dig själv. Genom att kombinera rätt behandling, anpassningar i arbetslivet och egna strategier, kan du bygga ett liv där dina styrkor får blomma och dina utmaningar blir hanterbara. Du är inte din diagnos, men din diagnos är en viktig del av hur du upplever världen.
"""

content = content + expansion

with open('/data/workspace/projects/neurovibe/content/adhd-diagnos-guide-expanded.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Expanded content 2 saved to adhd-diagnos-guide-expanded.md")
