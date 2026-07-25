"""
Städar och bygger om sitemap.xml.

Den gamla filen hade dubbletter (samma URL upp till tre gånger, ett fall med två
lastmod i samma <url>) vilket gör att Google får motstridiga signaler. Här byggs
den om från en enda lista: en URL per rad, en lastmod per URL.

Kör: venv/bin/python update_sitemap_leadmachine.py
"""
import glob
import os
import re
from datetime import date

BASE = "https://neurovibe.se/"
TODAY = date.today().isoformat()

# Sidor som inte ska indexeras.
EXCLUDE = {
    "admin.html",          # intern
    "tack.html",           # noindex, bara efter formulär
    "waitlist-success.html",
    "lead-magnet-snippet.html",  # fragment, ingen egen sida
}

# Prioritet efter roll i lead-maskinen: målgruppssidorna är ingångar,
# verktyg och pelarinnehåll driver trafiken, policysidor är stöd.
PRIORITY = {
    "": "1.0",
    "for-arbetsgivare.html": "0.9",
    "for-medarbetare.html": "0.9",
    "data-rapport-2026.html": "0.9",
    "partner.html": "0.7",
    "redaktionell-policy.html": "0.5",
    "integritetspolicy.html": "0.3",
    "om-sajten.html": "0.5",
    "feedback.html": "0.4",
}
DEFAULT_PRIORITY = "0.8"


def previous_lastmods(path: str) -> dict:
    """Behåll befintliga lastmod-datum så vi inte påstår att allt ändrats i dag."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        xml = fh.read()
    found = {}
    for block in re.findall(r"<url>(.*?)</url>", xml, re.DOTALL):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", block)
        mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block)
        if loc:
            slug = loc.group(1).replace(BASE, "")
            if mod:
                # Vid dubbletter vinner det senaste datumet.
                found[slug] = max(found.get(slug, ""), mod.group(1))
    return found


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    static = os.path.join(root, "static")
    sitemap_path = os.path.join(static, "sitemap.xml")

    old = previous_lastmods(sitemap_path)

    slugs = [""]  # startsidan
    for path in sorted(glob.glob(os.path.join(static, "*.html"))):
        name = os.path.basename(path)
        if name in EXCLUDE or name == "index.html":
            continue
        with open(path, encoding="utf-8") as fh:
            head = fh.read(4000)
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', head):
            print(f"  hoppar över (noindex): {name}")
            continue
        slugs.append(name)

    lines = ['<?xml version="1.0" encoding="utf-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug in slugs:
        lastmod = old.get(slug, TODAY)
        # Nya och omskrivna sidor får dagens datum.
        if slug in ("", "for-arbetsgivare.html", "for-medarbetare.html",
                    "partner.html", "redaktionell-policy.html"):
            lastmod = TODAY
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE}{slug}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{PRIORITY.get(slug, DEFAULT_PRIORITY)}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"\nSkrev {len(slugs)} URL:er till sitemap.xml (inga dubbletter).")


if __name__ == "__main__":
    main()
