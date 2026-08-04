"""
Tar bort de påhittade datapåståendena från sajten.

Siffrorna "68% i riskzon" och "82% hög maskeringsgrad" presenterades som
Neurovibes egen data. Underlaget var 1 rad i burnout_data.csv och 4 rader
simulerad tool_usage. De hade läckt ut från rapportsidan till startsidan, till
en guide och till mallen för kall B2B-outreach.

Ersätts med formuleringar som håller: det vi faktiskt vet är vad regelverket
kräver och vilket mönster verktygen är byggda kring — inte hur många procent
som något gäller för.

Kör: venv/bin/python fix_unsourced_claims.py
"""
import os

REPLACEMENTS = [
    # --- Startsidan: kortet som länkar till rapporten ---
    (
        "static/index.html",
        '<h3 class="text-xl font-bold mt-3 mb-4 group-hover:text-white transition-colors">State of Neurodiversity at Work 2026</h3>',
        '<h3 class="text-xl font-bold mt-3 mb-4 group-hover:text-white transition-colors">Neurodiversitet i svenskt arbetsliv 2026</h3>',
    ),
    (
        "static/index.html",
        'Vår första unika data-rapport: 68% av neurodivergenta på jobbet är i riskzon för utbrändhet. Läs hela analysen av våra insamlade data.',
        'Tre mönster vi ser om maskering, exekutiv funktion och stödsystem — och varför vi ännu inte publicerar procentsatser om dem.',
    ),

    # --- Guide som citerade siffran som fastställd data ---
    (
        "static/post-semester-stress-npf.html",
        'Att plötsligt tvingas in i "arbets-masken" igen dränerar all energi på några dagar. Enligt data från Neurovibe (Q2 2026) lägger 68% av neurodivergenta medarbetare enorm energi på maskering, vilket är en primär orsak till utbrändhet.',
        'Att plötsligt tvingas in i "arbets-masken" igen dränerar all energi på några dagar. Maskering är arbete som inte syns i något tidrapporteringssystem, men som tar av samma ändliga kapacitet som arbetsuppgifterna — och är en vanlig väg in i utmattning.',
    ),
    (
        "static/post-semester-stress-npf.html",
        'Ladda ner vår <a href="/data-rapport-2026.html" class="font-semibold underline">State of Neurodiversity 2026-rapport</a>.',
        'Läs våra <a href="/data-rapport-2026.html" class="font-semibold underline">observationer om neurodiversitet i svenskt arbetsliv</a>.',
    ),
    # Generatorn som producerar sidan ovan — annars återskapas påståendet.
    (
        "generate_back_to_work_guide.py",
        'Enligt data från Neurovibe (Q2 2026) lägger 68% av neurodivergenta medarbetare enorm energi på maskering, vilket är en primär orsak till utbrändhet.',
        'Maskering är arbete som inte syns i något tidrapporteringssystem, men som tar av samma ändliga kapacitet som arbetsuppgifterna — och är en vanlig väg in i utmattning.',
    ),
    (
        "generate_back_to_work_guide.py",
        'Ladda ner vår <a href="/data-rapport-2026.html" class="font-semibold underline">State of Neurodiversity 2026-rapport</a>.',
        'Läs våra <a href="/data-rapport-2026.html" class="font-semibold underline">observationer om neurodiversitet i svenskt arbetsliv</a>.',
    ),

    # --- Resurser och navigation: nytt namn på sidan ---
    (
        "static/resurser.html",
        '<h2 class="text-xl font-bold text-white mb-3">State of Neurodiversity 2026</h2>',
        '<h2 class="text-xl font-bold text-white mb-3">Neurodiversitet i svenskt arbetsliv 2026</h2>',
    ),
    (
        "static/for-arbetsgivare.html",
        'Läs State of Neurodiversity at Work 2026 &rarr;',
        'Läs våra observationer för 2026 &rarr;',
    ),
    (
        "static/partner.html",
        '<a href="/data-rapport-2026.html" class="text-[#D83131] hover:underline">State of Neurodiversity-rapport</a>',
        '<a href="/data-rapport-2026.html" class="text-[#D83131] hover:underline">årliga observationsdokument</a>',
    ),
    (
        "static/tack.html",
        "'State of Neurodiversity at Work 2026: vad medarbetare själva rapporterar om belastning och maskering.',",
        "'Tre mönster om maskering, exekutiv funktion och stödsystem — och en ärlig not om vad underlaget är.',",
    ),
]

# --- Sidan för arbetsgivare lovade mer än rapporten levererar ---
ARBETSGIVARE_OLD = """                    <p class="text-[#A0A0A0] leading-relaxed mb-6">
                        Våra verktyg används varje dag av medarbetare som beskriver sin faktiska
                        arbetssituation: vad som belastar, vad de maskerar och vilka anpassningar
                        de efterfrågar. Vi sammanställer det anonymiserat till en årlig rapport.
                    </p>
                    <p class="text-[#A0A0A0] leading-relaxed mb-8">
                        Det gör att vi kan svara på frågor som ingen enkätleverantör kan: inte vad
                        chefer <em>tror</em> att neurodivergenta medarbetare behöver, utan vad de
                        själva skriver in när ingen chef ser.
                    </p>"""

ARBETSGIVARE_NEW = """                    <p class="text-[#A0A0A0] leading-relaxed mb-6">
                        Våra verktyg används av medarbetare som beskriver sin faktiska
                        arbetssituation: vad som belastar, vad de maskerar och vilka anpassningar
                        de efterfrågar. Inmatningarna sker i stunden, inte i efterhand i en enkät.
                    </p>
                    <p class="text-[#A0A0A0] leading-relaxed mb-8">
                        Vi sammanställer mönstren anonymiserat en gång om året. Och vi säger rakt ut
                        var gränsen går: volymen är ännu för liten för att räkna procent på, så vi
                        publicerar inga siffror förrän underlaget bär dem. Ni ska kunna lita på det
                        vi skriver just för att vi inte skriver mer än vi vet.
                    </p>"""

# --- Mallen för kall outreach byggde hela hooken på siffran ---
OUTREACH = """# B2B Outreach Strategy - Neurovibe

**Target:** HR-chefer, fackförbund och D&I-ansvariga i Sverige.
**Lead magnet:** Arbetsgivarpaketet (rutinmall enligt AFS 2020:5, anpassningsbibliotek,
samtalsmall, lagkravsöversikt).
**Mål:** Bygga auktoritet, fånga B2B-leads och positionera Neurovibe som den
praktiska resursen för neuroinkluderande arbetsplatser.

## Hooken

Bygg aldrig hooken på en siffra vi inte kan belägga. Vi har ingen statistik som
håller ännu — se `/redaktionell-policy.html`. Det vi kan säga och stå för:

> *AFS 2020:5 kräver att arbetsgivaren har en skriftlig rutin för
> arbetsanpassning. De flesta organisationer har ingen — inte av ovilja, utan för
> att ingen vet vad den ska innehålla.*

Det är ett påstående om regelverket, inte om en population, och det går att
kontrollera mot föreskriften.

## Mejlsekvens

### Mejl 1: Lagkravet (kall kontakt)
**Ämne:** Har ni er rutin för arbetsanpassning på plats?

Hej [Namn],

AFS 2020:5 kräver att ni som arbetsgivare har en skriftlig rutin för
arbetsanpassning — hur behov uppmärksammas, vem som utreder, hur beslut
dokumenteras och när det följs upp. I praktiken saknas den hos de flesta, och
frågan blir akut först när någon redan är sjukskriven.

Vi har byggt en färdig mall som täcker de moment som efterfrågas vid inspektion,
tillsammans med ett anpassningsbibliotek sorterat efter problem — sensorisk
belastning, tidsuppfattning, avbrott, muntliga instruktioner — där det framgår
vilka åtgärder som kostar noll kronor.

Kostnadsfritt, ingen inloggning: https://neurovibe.se/for-arbetsgivare.html

Vänliga hälsningar,
Neurovibe

### Mejl 2: Verktygen (uppföljning)
**Ämne:** Konkreta verktyg för en neuroinkluderande arbetsplats

Hej [Namn],

En uppföljning på mitt förra mejl.

Ett av de vanligaste problemen vi ser är att ansvaret för att formulera en
anpassning hamnar hos den medarbetare vars exekutiva funktion redan är ansträngd.
Det är den sämsta möjliga fördelningen av arbetet.

Två verktyg som flyttar det ansvaret:

- **Anpassningsgeneratorn** — medarbetaren kryssar i vad som är svårt och får ett
  sakligt formulerat förslag att skicka till chefen, utan att nämna diagnos:
  https://neurovibe.se/verktyg-anpassningsgenerator.html
- **Intervjuguiden** — neuroinkluderande intervjumall som mäter kompetens i
  stället för förmågan att kallprata:
  https://neurovibe.se/intervju-guide.html

Säg till om ni vill att jag tittar på er situation specifikt.

Vänliga hälsningar,
Neurovibe

## Regler för outreach

1. Inga siffror utan belagd källa. Regelverk får citeras, egen data inte förrän
   den finns.
2. Länka till arbetsgivarsidan, inte till observationsdokumentet — det senare är
   medvetet försiktigt formulerat och säljer inte.
3. Följ upp en gång. Ingen tredje påminnelse.
"""


def apply_replacements() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    changed = 0
    missing = []
    for rel, old, new in REPLACEMENTS:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            missing.append(rel)
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if old not in text:
            if new not in text:
                missing.append(f"{rel}: hittade inte texten")
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new))
        changed += 1
        print(f"  {rel}: ersatt")

    # Arbetsgivarsidans dataavsnitt
    path = os.path.join(root, "static", "for-arbetsgivare.html")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if ARBETSGIVARE_OLD in text:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(ARBETSGIVARE_OLD, ARBETSGIVARE_NEW))
        changed += 1
        print("  static/for-arbetsgivare.html: dataavsnitt omskrivet")

    # Outreach-mallen skrivs om helt
    for rel in ("content/b2b_outreach_strategy.md",):
        with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
            fh.write(OUTREACH)
        changed += 1
        print(f"  {rel}: omskriven")

    for m in missing:
        print(f"  ! {m}")
    return changed


if __name__ == "__main__":
    print(f"\n{apply_replacements()} ändringar.")
