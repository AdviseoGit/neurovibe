"""
Lägger canonical-tagg på indexerade sidor som saknar den.

Utan canonical får Google själv gissa vilken URL som är originalet när samma
innehåll nås på flera adresser (www/icke-www, /index.html vs /, med och utan
query-parametrar). Gissar den fel hamnar rankingen på fel URL.

Sajten pekar redan ut icke-www som primär i sitemap.xml, robots.txt och de
canonicals som finns — så skriptet följer det.

Noindex-sidor hoppas över: de ska inte indexeras alls och behöver ingen canonical.

Kör: venv/bin/python add_canonicals.py
"""
import glob
import os
import re

BASE = "https://neurovibe.se/"


def main() -> None:
    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    added, skipped = [], []

    for path in sorted(glob.glob(os.path.join(static, "*.html"))):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()

        if 'rel="canonical"' in html:
            continue
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', html, re.I):
            skipped.append(f"{name} (noindex)")
            continue
        if "<head" not in html:
            skipped.append(f"{name} (ingen <head>)")
            continue

        url = BASE if name == "index.html" else BASE + name
        tag = f'    <link rel="canonical" href="{url}">\n'

        # Lägg den direkt efter <title> om den finns — annars först i <head>.
        m = re.search(r"</title>\s*\n", html)
        if m:
            html = html[:m.end()] + tag + html[m.end():]
        else:
            m = re.search(r"<head[^>]*>\s*\n", html)
            html = html[:m.end()] + tag + html[m.end():]

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        added.append(f"{name} -> {url}")

    for a in added:
        print(f"  + {a}")
    for s in skipped:
        print(f"  . hoppade över {s}")
    print(f"\n{len(added)} canonicals tillagda.")


if __name__ == "__main__":
    main()
