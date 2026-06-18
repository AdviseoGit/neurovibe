"""
Neurovibe lead magnet — the "neuroinkluderande checklista" the waitlist modal
promises ("tillgång till våra neuroinkluderande verktyg och checklistor").

Deluxe, multi-section PDF (shared design language with the other portfolio
sites). fpdf2 core font = latin-1, which covers å/ä/ö; _s() keeps those and
only strips characters latin-1 cannot represent (em-dash, smart quotes, ...).
"""

# Brand palette
BRAND = (216, 49, 49)     # neurovibe red
BRAND_DK = (150, 28, 28)
INK = (28, 28, 30)
MUTED = (110, 110, 116)
LINE = (228, 228, 231)
WASH = (254, 242, 242)
WASH2 = (250, 250, 250)

INTRO = ("Små, konkreta förändringar som gör stor skillnad för medarbetare med ADHD, autism och "
         "andra neurotyper - och som oftast gör arbetsplatsen bättre för alla. Bocka av det ni "
         "redan gör och välj 2-3 nya att testa den här månaden.")

SECTIONS = [
    ("Fysisk arbetsmiljö", [
        "Erbjud tysta zoner och möjlighet till hörselskydd/brusreducering.",
        "Låt medarbetare justera ljus (dämpbart, undvik flimrande lysrör).",
        "Tillåt egna verktyg: stressboll, fidget, ståbord, hörlurar.",
    ]),
    ("Kommunikation", [
        "Skriv ner det viktiga - komplettera muntligt med text/punktlistor.",
        "Var konkret och direkt; undvik underförstådda budskap 'mellan raderna'.",
        "Ge en agenda i förväg så hjärnan hinner förbereda sig.",
    ]),
    ("Möten", [
        "Boka kortare möten med tydligt syfte och sluttid.",
        "Tillåt kamera av och att delta via chatt.",
        "Skicka anteckningar och beslut efteråt - alla minns inte muntligt.",
    ]),
    ("Arbetssätt & fokus", [
        "Bryt ner stora uppgifter i små, tydliga steg med delmål.",
        "Skydda fokustid: block i kalendern, få avbrott, asynkront först.",
        "Använd timers/Pomodoro och visuella to-do-listor.",
    ]),
    ("Ledarskap & kultur", [
        "Fråga 'hur fungerar du bäst?' - en storlek passar inte alla.",
        "Normalisera anpassningar så ingen behöver 'be om ursäkt'.",
        "Fokusera på resultat, inte på närvaro eller arbetssätt.",
    ]),
]

CLOSING = ("Vill ni ta nästa steg? Neurovibe bygger verktyg som hjälper team att omsätta det här i "
           "praktiken - du står nu på listan för early access och hör av oss så snart det finns en "
           "plats för dig.")


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


class DeluxeReport:
    MARGIN = 14
    WIDTH = 210 - 2 * 14

    def __init__(self, brand, brand_dk):
        from fpdf import FPDF
        self.brand, self.brand_dk = brand, brand_dk
        self.pdf = FPDF(format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.set_margins(self.MARGIN, self.MARGIN, self.MARGIN)

    def cover(self, brandname, title, subtitle, intro):
        pdf = self.pdf
        pdf.add_page()
        pdf.set_fill_color(*self.brand)
        pdf.rect(0, 0, 210, 60, "F")
        pdf.set_fill_color(*self.brand_dk)
        pdf.rect(0, 56, 210, 4, "F")
        pdf.set_xy(14, 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 25)
        pdf.cell(0, 12, _s(brandname), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 8, _s(title), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, _s(subtitle), ln=1)
        pdf.set_y(70)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(self.WIDTH, 5, _s(intro))
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def section(self, title):
        pdf = self.pdf
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, 9, "F")
        pdf.set_xy(self.MARGIN + 3, y + 1)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(self.WIDTH - 6, 7, _s(title), ln=1)
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def checks(self, items, mark="box"):
        pdf = self.pdf
        for i, it in enumerate(items):
            if pdf.get_y() > 262:
                pdf.add_page()
            y = pdf.get_y()
            if mark == "box":
                pdf.set_draw_color(*self.brand)
                pdf.rect(self.MARGIN + 1, y + 1.2, 4, 4)
            else:  # cross
                pdf.set_text_color(190, 40, 40)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_xy(self.MARGIN, y)
                pdf.cell(6, 5.5, "X")
                pdf.set_text_color(*INK)
            pdf.set_xy(self.MARGIN + 8, y)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.multi_cell(self.WIDTH - 8, 5.5, _s(it))
            pdf.ln(1)

    def callout(self, text):
        pdf = self.pdf
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        # measure roughly: render text, then box. Simpler: fixed-ish box via multi_cell height.
        pdf.set_fill_color(*WASH)
        pdf.set_draw_color(*self.brand)
        x = self.MARGIN
        pdf.set_xy(x + 4, y + 3)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*INK)
        # draw box first with estimated height
        import math
        approx_lines = max(1, math.ceil(pdf.get_string_width(_s(text)) / (self.WIDTH - 10)))
        h = approx_lines * 5 + 8
        pdf.rect(x, y, self.WIDTH, h, "DF")
        pdf.set_xy(x + 4, y + 3)
        pdf.multi_cell(self.WIDTH - 8, 5, _s(text))
        pdf.set_y(y + h + 2)

    def footer_text(self, txt):
        self._footer = txt


def _build(brandname, title, subtitle, intro, sections, closing, brand, brand_dk, footer):
    r = DeluxeReport(brand, brand_dk)
    pdf = r.pdf

    def footer_fn():
        pdf.set_y(-15)
        pdf.set_draw_color(*LINE)
        pdf.line(r.MARGIN, pdf.get_y(), 210 - r.MARGIN, pdf.get_y())
        pdf.set_y(-13)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4, _s(footer), align="C")

    pdf.footer = footer_fn
    r.cover(brandname, title, subtitle, intro)
    for stitle, items in sections:
        r.section(stitle)
        r.checks(items)
    if closing:
        r.callout(closing)
    return bytes(pdf.output())


def build_checklist_pdf() -> bytes:
    return _build(
        "Neurovibe",
        "Neuroinkluderande arbetsplats",
        "Snabbstart-checklista för chefer och team",
        INTRO, SECTIONS, CLOSING, BRAND, BRAND_DK,
        "Neurovibe | neurovibe.se | Kognitiv harmoni för arbetslivet. "
        "Allmän vägledning, inte medicinsk rådgivning.")


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
       arbetslivet, indelat i fysisk miljö, kommunikation, möten, fokus och ledarskap — välj
       2–3 att testa den här månaden.</p>
    <p style="margin-top:22px">Varma hälsningar,<br><b>Neurovibe</b><br>
       <a href="https://neurovibe.se" style="color:#d83131">neurovibe.se</a></p>
    <p style="font-size:11px;color:#9a9a9a;margin-top:22px">Du får detta för att du anmälde dig på
       neurovibe.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""
