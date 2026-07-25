"""
Lappar de gamla, inline-kodade lead-formulären.

De byggdes en gång per sida och skickar bara { email } till /api/lead. Utan
källa och segment går det inte att se vilken sida som faktiskt konverterar,
vilket är hela poängen med lead-maskinen.

Detta skript gör tre saker utan att röra sidornas layout:
  1. Rättar felstavade endpoints (/api/leads -> /api/lead). Den varianten har
     aldrig fungerat — POST mot /api/leads finns inte och ger 404.
  2. Lägger till segment, offer och source_page i JSON-kroppen.
  3. Lägger till en synlig integritetsnotis under formuläret där den saknas.

Formulären bör på sikt ersättas med <form data-nv-lead> och en riktig
samtyckesruta (se LEADFLOW.md) — då sköter leadflow.js allt detta.

Kör: venv/bin/python fix_legacy_lead_forms.py
"""
import glob
import os
import re

NOTICE = (
    '<p class="nv-privacy-note" style="font-size:0.75rem;color:#808080;margin-top:0.75rem">'
    'Vi skickar det du bett om och enstaka mejl med nya verktyg. Avregistrering med ett svar. '
    '<a href="/integritetspolicy.html" style="color:#D83131">Integritetspolicy</a>.</p>'
)

# Matchar JSON-kroppen i ett fetch mot lead-endpointen.
BODY_RE = re.compile(
    r"body:\s*JSON\.stringify\(\{\s*\n?\s*email:\s*email\s*,?\s*"
    r"(?:\n\s*)?(?:source:\s*'([^']*)'\s*,?)?\s*\n?\s*\}\)"
)


def patch_body(match: re.Match) -> str:
    source = match.group(1) or "legacy"
    return (
        "body: JSON.stringify({\n"
        "                        email: email,\n"
        f"                        source: '{source}',\n"
        "                        segment: 'individ',\n"
        f"                        offer: '{source}',\n"
        "                        source_page: window.location.pathname\n"
        "                    })"
    )


def main() -> None:
    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    report = []

    for path in sorted(glob.glob(os.path.join(static, "*.html"))):
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html
        actions = []

        if "/api/leads'" in html or '/api/leads"' in html:
            html = html.replace("/api/leads'", "/api/lead'").replace('/api/leads"', '/api/lead"')
            actions.append("rättade endpoint")

        html, n = BODY_RE.subn(patch_body, html)
        if n:
            actions.append(f"berikade {n} payload(er)")

        # Notisen läggs bara på sidor som har ett gammalt formulär och saknar
        # både notis och en riktig samtyckesruta.
        has_legacy_form = "/api/lead" in html and "data-nv-lead" not in html
        has_notice = "nv-privacy-note" in html or "integritetspolicy.html" in html
        if has_legacy_form and not has_notice:
            match = re.search(r"</form>", html)
            if match:
                html = html[:match.end()] + "\n    " + NOTICE + html[match.end():]
                actions.append("la till integritetsnotis")

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            report.append((os.path.basename(path), actions))

    for name, actions in report:
        print(f"  {name}: {'; '.join(actions)}")
    print(f"\nUppdaterade {len(report)} filer.")


if __name__ == "__main__":
    main()
