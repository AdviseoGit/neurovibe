"""
Kopplar in befintliga guider i lead-maskinen.

Varje organisk ingång ska leda vidare till rätt målgruppssida i stället för att
sluta i en footer. Skriptet lägger in ett CTA-block strax före footern och ser
till att leadflow.js finns på sidan.

Blocket är märkt med <!-- nv-segment-cta --> så att skriptet kan köras om utan
att dubblera något. Inline-stilar används medvetet: sidorna har inte identiska
Tailwind-klasser, och blocket ska se likadant ut på alla.

Kör: venv/bin/python add_segment_ctas.py
"""
import os
import re

MARKER = "<!-- nv-segment-cta -->"
SCRIPT_TAG = '<script src="/static/leadflow.js" defer></script>'

# Sida -> segment. Avgör vilken väg vidare läsaren erbjuds.
PAGE_SEGMENTS = {
    # Arbetsgivarspåret: chefer, HR, arbetsmiljö
    "lagkrav-anpassningar-arbetsmiljo.html": "arbetsgivare",
    "inkluderande-kultur-npf.html": "arbetsgivare",
    "inkluderande-rekrytering-npf.html": "arbetsgivare",
    "fem-tips-for-chefer.html": "arbetsgivare",
    "kognitiv-ergonomi-npf.html": "arbetsgivare",
    "intervju-guide.html": "arbetsgivare",
    "fordelarna-med-neurodiversitet.html": "arbetsgivare",
    "neurodiversitet-arbetsplatsen.html": "arbetsgivare",
    "arbetsplats-schema-npf.html": "arbetsgivare",
    "maskering-pa-arbetsplatsen.html": "arbetsgivare",
    "data-rapport-2026.html": "arbetsgivare",
    # Individspåret: medarbetare, arbetssökande, anhöriga
    "adhd-anpassningar-jobb.html": "individ",
    "adhd-diagnos-guide.html": "individ",
    "adhd-diagnos-vuxen.html": "individ",
    "autism-arbetsplatsen-tips-guide.html": "individ",
    "npf-arbetslivet.html": "individ",
    "forsakringskassan-arbetsformedlingen-stod.html": "individ",
    "arbetsprovning-2026-forsakringskassan.html": "individ",
    "post-semester-stress-npf.html": "individ",
    "ai-verktyg-neurodiversitet.html": "individ",
    "ai-verktyg-jobb-kalkylator.html": "individ",
    "verktyg-nedbrytare.html": "individ",
    "verktyg-fokus-timer.html": "individ",
    "verktyg-burnout-kalkylator.html": "individ",
    "verktyg-anpassningsgenerator.html": "individ",
    "verktyg-myndighetsnavigator.html": "individ",
}

BLOCK = """
{marker}
<div style="max-width:52rem;margin:4rem auto;padding:2rem;border:1px solid rgba(255,255,255,0.08);
            border-left:3px solid #D83131;border-radius:16px;background:rgba(255,255,255,0.03)">
  <p style="font-family:ui-monospace,monospace;font-size:0.7rem;letter-spacing:0.2em;
            text-transform:uppercase;color:#D83131;margin:0 0 0.75rem">{eyebrow}</p>
  <h2 style="font-size:1.5rem;font-weight:700;color:#fff;margin:0 0 0.75rem;line-height:1.3">{title}</h2>
  <p style="color:#A0A0A0;line-height:1.7;margin:0 0 1.5rem">{body}</p>
  <div style="display:flex;flex-wrap:wrap;gap:0.75rem">
    <a href="{primary_href}" style="display:inline-block;background:#D83131;color:#fff;text-decoration:none;
       padding:0.85rem 1.5rem;border-radius:10px;font-weight:600">{primary_label}</a>
    <a href="{secondary_href}" style="display:inline-block;border:1px solid rgba(255,255,255,0.15);
       color:#fff;text-decoration:none;padding:0.85rem 1.5rem;border-radius:10px;font-weight:600">{secondary_label}</a>
  </div>
</div>
"""

COPY = {
    "arbetsgivare": {
        "eyebrow": "Nästa steg för er som arbetsgivare",
        "title": "Vi har samlat underlaget ni behöver",
        "body": ("Rutinmall enligt AFS 2020:5, anpassningsbibliotek sorterat efter problem, "
                 "samtalsmall för chefen och en översikt över vilka stöd ni kan söka. "
                 "Kostnadsfritt, utan inloggning."),
        "primary_href": "/for-arbetsgivare.html#arbetsgivarpaket",
        "primary_label": "Beställ arbetsgivarpaketet",
        "secondary_href": "/for-arbetsgivare.html",
        "secondary_label": "Se vad det innehåller",
    },
    "individ": {
        "eyebrow": "Nästa steg",
        "title": "Verktygen som gör det konkret",
        "body": ("Bryt ner det som känns för stort, mät din belastning eller få ett färdigt "
                 "anpassningsförslag att ta med till chefen — utan att behöva förklara någon "
                 "diagnos. Allt är gratis."),
        "primary_href": "/for-medarbetare.html",
        "primary_label": "Till verktygslådan",
        "secondary_href": "/for-medarbetare.html#checklista",
        "secondary_label": "Få checklistan i mejlen",
    },
}


def inject(path: str, segment: str) -> str:
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    changes = []

    if MARKER not in html:
        block = BLOCK.format(marker=MARKER, **COPY[segment])
        # Placera blocket precis före den sista footern på sidan.
        matches = list(re.finditer(r'(<!--\s*Footer\s*-->\s*)?<footer', html, re.IGNORECASE))
        if matches:
            pos = matches[-1].start()
            html = html[:pos] + block + "\n" + html[pos:]
            changes.append("cta")
        else:
            print(f"  ! {os.path.basename(path)}: hittade ingen <footer>, hoppar över CTA")

    if "leadflow.js" not in html:
        if "</body>" in html:
            html = html.replace("</body>", f"    {SCRIPT_TAG}\n</body>", 1)
            changes.append("script")

    if changes:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
    return ", ".join(changes)


def main() -> None:
    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    touched = 0
    for page, segment in sorted(PAGE_SEGMENTS.items()):
        path = os.path.join(static, page)
        if not os.path.exists(path):
            print(f"  ! saknas: {page}")
            continue
        result = inject(path, segment)
        if result:
            touched += 1
            print(f"  {page} [{segment}]: {result}")
    print(f"\nUppdaterade {touched} sidor.")


if __name__ == "__main__":
    main()
