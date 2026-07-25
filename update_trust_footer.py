"""
Byter ut AI-disclaimern i footern på alla sidor.

Gammal text: "Denna sajt skapas och drivs helt av AI · Om sajten"
Ny text:     "Innehållet produceras av AI · Redaktionell policy & källor"

Poängen är inte att dölja att sajten är AI-driven — det står kvar, och står
utförligt på /redaktionell-policy.html. Poängen är att länken i footern ska
leda till sidan som svarar på läsarens faktiska fråga ("kan jag lita på det
här?") i stället för till en experiment-beskrivning. En arbetsgivare som ska
betala för synlighet läser den sidan innan de mejlar.

Kör: venv/bin/python update_trust_footer.py
"""
import glob
import os
import re

NEW_TEXT = (
    'Innehållet produceras av AI-system inom mänskligt satta ramar och utgör inte '
    'medicinsk rådgivning &middot; <a href="/redaktionell-policy.html" '
    'class="{cls}">Redaktionell policy &amp; källor</a>'
)

# Matchar hela disclaimern inklusive den efterföljande "Om sajten"-länken,
# oavsett vilka klasser den enskilda sidan råkar använda.
PATTERN = re.compile(
    r'Denna sajt skapas och drivs helt av AI'
    r'(?: inom mänskliga guardrails\.)?'
    r'\s*(?:&middot;|·)?\s*'
    r'<a href="/om-sajten\.html" class="([^"]*)">Om sajten</a>'
)

# Prosan på om-sajten.html är den utförliga förklaringen och ska stå kvar.
SKIP_PROSE = re.compile(r'Denna sajt skapas och drivs helt av AI-agenter')


def replace(match: re.Match) -> str:
    return NEW_TEXT.format(cls=match.group(1))


def main() -> None:
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    changed = []
    for path in sorted(glob.glob(os.path.join(static_dir, "*.html"))):
        with open(path, encoding="utf-8") as fh:
            original = fh.read()

        updated, count = PATTERN.subn(replace, original)

        # Varianten utan länk (förekommer i en footer-kolumn på ett par sidor).
        updated, count2 = re.subn(
            r'<span>Denna sajt skapas och drivs helt av AI</span>',
            '<span><a href="/redaktionell-policy.html" class="hover:text-white '
            'transition-colors">AI-transparens &amp; källor</a></span>',
            updated,
        )

        if count + count2:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(updated)
            changed.append((os.path.basename(path), count + count2))

    for name, n in changed:
        print(f"  {name}: {n} förekomst(er)")
    print(f"\nUppdaterade {len(changed)} filer.")
    remaining = []
    for path in sorted(glob.glob(os.path.join(static_dir, "*.html"))):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if "Denna sajt skapas och drivs helt av AI" in text and not SKIP_PROSE.search(text):
            remaining.append(os.path.basename(path))
    if remaining:
        print(f"Kvar att kolla manuellt: {', '.join(remaining)}")


if __name__ == "__main__":
    main()
