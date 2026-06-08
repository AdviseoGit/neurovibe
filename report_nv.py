"""
Neurovibe lead magnet — the "neuroinkluderande checklista" the waitlist modal
promises ("tillgang till vara neuroinkluderande verktyg och checklistor").
Static, high-value content PDF + the welcome email body.
fpdf2 core font = latin-1 (a/a/o ok; avoid em-dash/smart quotes -> _s()).
"""

RED = (216, 49, 49)
INK = (28, 28, 30)
MUTED = (110, 110, 116)

SECTIONS = [
    ("Fysisk arbetsmiljo", [
        "Erbjud tysta zoner och mojlighet till horselskydd/brus-reducering.",
        "Lat medarbetare justera ljus (dampbart, undvik flimrande lysror).",
        "Tillat egna verktyg: stressboll, fidget, stabord, horlurar.",
    ]),
    ("Kommunikation", [
        "Skriv ner det viktiga - komplettera muntligt med text/punktlistor.",
        "Var konkret och direkt; undvik underforstadda 'mellan raderna'.",
        "Ge en agenda i forvag sa hjarnan hinner forbereda sig.",
    ]),
    ("Moten", [
        "Boka kortare moten med tydligt syfte och sluttid.",
        "Tillat kamera av och att delta via chatt.",
        "Skicka anteckningar och beslut efterat - inte alla minns muntligt.",
    ]),
    ("Arbetssatt & fokus", [
        "Bryt ner stora uppgifter i sma, tydliga steg med delmal.",
        "Skydda fokustid: block i kalendern, fa avbrott, asynkront forst.",
        "Anvand timers/Pomodoro och visuella to-do-listor.",
    ]),
    ("Ledarskap & kultur", [
        "Fraga 'hur fungerar du bast?' - en storlek passar inte alla.",
        "Normalisera anpassningar sa ingen behover 'be om ursakt'.",
        "Fokusera pa resultat, inte pa narvaro eller arbetssatt.",
    ]),
]


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


def build_checklist_pdf() -> bytes:
    from fpdf import FPDF
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    pdf.set_fill_color(*RED)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_xy(14, 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Neurovibe", ln=1)
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _s("Neuroinkluderande arbetsplats - snabbstart-checklista"), ln=1)

    pdf.set_xy(14, 38)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(182, 5, _s(
        "Sma, konkreta forandringar som gor stor skillnad for medarbetare med ADHD, "
        "autism och andra neurotyper - och som oftast gor det battre for alla. "
        "Bocka av det ni redan gor och valj 2-3 nya att testa den har manaden."))
    pdf.ln(2)

    for title, items in SECTIONS:
        pdf.set_text_color(*RED)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, _s(title), ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*INK)
        for it in items:
            y = pdf.get_y()
            pdf.set_draw_color(*MUTED)
            pdf.rect(15, y + 1.2, 3.5, 3.5)
            pdf.set_x(22)
            pdf.multi_cell(173, 6, _s(it))
        pdf.ln(2)

    pdf.set_y(-18)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(182, 4, _s("Neurovibe | neurovibe.se | Kognitiv harmoni for arbetslivet. "
                              "Detta ar allman vagledning, inte medicinsk radgivning."))
    return bytes(pdf.output())


def user_email_html() -> str:
    return """\
<div style="font-family:Segoe UI,Arial,sans-serif;max-width:560px;margin:auto;color:#1c1c1e">
  <div style="background:#d83131;color:#fff;padding:22px 24px;border-radius:12px 12px 0 0">
    <h2 style="margin:0;font-size:20px">Välkommen till Neurovibe 🧠</h2>
  </div>
  <div style="border:1px solid #ececec;border-top:0;border-radius:0 0 12px 12px;padding:24px">
    <p>Hej, och tack för att du gick med!</p>
    <p>Du står nu på listan för early access — vi hör av oss så fort det finns en plats för dig.
       Under tiden får du redan nu vår <b>neuroinkluderande snabbstart-checklista</b> som
       <b>PDF i bilagan</b>.</p>
    <p>Den samlar konkreta, lågtröskel-anpassningar för ADHD, autism och andra neurotyper i
       arbetslivet — välj 2–3 att testa den här månaden.</p>
    <p style="margin-top:22px">Varma hälsningar,<br><b>Neurovibe</b><br>
       <a href="https://neurovibe.se" style="color:#d83131">neurovibe.se</a></p>
    <p style="font-size:11px;color:#9a9a9a;margin-top:22px">Du får detta för att du anmälde dig på
       neurovibe.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""
