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

    def paragraph(self, text, size=10.5, gap=3):
        pdf = self.pdf
        if pdf.get_y() > 255:
            pdf.add_page()
        pdf.set_x(self.MARGIN)
        pdf.set_font("Helvetica", "", size)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.WIDTH, 5.5, _s(text))
        pdf.ln(gap)

    def lead(self, text):
        """Ingress i avvikande ton — används för 'läs detta först'-rutan."""
        pdf = self.pdf
        pdf.set_x(self.MARGIN)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(self.WIDTH, 5.5, _s(text))
        pdf.set_text_color(*INK)
        pdf.ln(3)

    def bullets(self, items):
        pdf = self.pdf
        for it in items:
            if pdf.get_y() > 262:
                pdf.add_page()
            y = pdf.get_y()
            pdf.set_text_color(*self.brand)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_xy(self.MARGIN + 1, y)
            pdf.cell(5, 5.5, "-")
            pdf.set_text_color(*INK)
            pdf.set_xy(self.MARGIN + 7, y)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.multi_cell(self.WIDTH - 7, 5.5, _s(it))
            pdf.ln(1)

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


# --- Observationsdokumentet -------------------------------------------------
# Speglar /data-rapport-2026.html ordagrant i sak. Ändras sidan ska detta ändras
# med den — annars lovar sidan en sak och PDF:en levererar en annan, vilket är
# precis det som var fel innan.

REPORT_INTRO = (
    "Tre mönster vi ser om utmattning, exekutiv funktion och stödsystem i svenskt "
    "arbetsliv - och varför vi ännu inte publicerar några procentsatser om dem.")

REPORT_CAVEAT = (
    "Det här är INTE en statistisk undersökning. Neurovibes verktyg är nya och antalet "
    "inmatningar är än så länge för litet för att räkna procent på. Vi publicerar därför "
    "inga siffror - det vore lätt att göra och omöjligt att försvara.\n\n"
    "Det du läser nedan är kvalitativa observationer: mönster vi ser i hur verktygen "
    "används, satt i relation till svenska regelverk och till det som är väl beskrivet om "
    "exekutiv funktion sedan tidigare. Behandla det som underlag för samtal, inte som "
    "mätdata.\n\n"
    "När kommer siffrorna? Vi publicerar procentsatser först när underlaget bär dem, och "
    "redovisar då urvalsstorlek och den självselektion som ligger i att personer som söker "
    "upp en burnout-kalkylator sannolikt är mer belastade än genomsnittet.")

REPORT_OBSERVATIONS = [
    ("Observation 1: Maskering är arbete som ingen bokför",
     "Det som återkommer tydligast när människor beskriver sin arbetssituation är inte "
     "arbetsuppgifterna - det är ansträngningen att framstå som neurotypisk medan de utförs. "
     "Ögonkontakt, småprat, dämpat stimming, konstant självövervakning. Den ansträngningen "
     "syns inte i något tidrapporteringssystem, men den tar av samma ändliga kapacitet som "
     "arbetet gör.\n\n"
     "En medarbetare som verkar prestera normalt kan göra det till en kostnad som först blir "
     "synlig när den plötsligt inte går att betala längre. Det är därför utmattning i den här "
     "gruppen ofta kommer utan förvarning för arbetsgivaren."),
    ("Observation 2: Det som fastnar är starten, inte utförandet",
     "De uppgifter människor matar in i Uppgiftsnedbrytaren är sällan svåra i sig: 'svara på "
     "vd:s mejl', 'skriva reseräkning', 'boka tandläkartid'. Det är uppgifter personen fullt "
     "ut klarar av att utföra. Tröskeln ligger i igångsättningen - ett välbeskrivet drag hos "
     "nedsatt exekutiv funktion, och något helt annat än bristande kompetens eller "
     "motivation.\n\n"
     "Det har en direkt konsekvens för hur man leder: 'ta tag i det' är inte en instruktion "
     "som hjälper. Ett definierat första steg är det."),
    ("Observation 3: Stödet finns, men processen kräver just det man saknar",
     "Det finns stöd att söka - arbetshjälpmedel och bidrag till anpassning via "
     "Försäkringskassan och Arbetsförmedlingen. Men ansökningsvägarna kräver precis de "
     "förmågor som är nedsatta: överblick, uthållighet i en flerstegsprocess, förmåga att "
     "driva ett ärende genom flera instanser utan omedelbar återkoppling.\n\n"
     "Ett stödsystem som förutsätter intakt exekutiv funktion når per definition inte dem som "
     "behöver det mest. Det är ett starkt argument för att arbetsgivaren tar initiativet i "
     "stället för att vänta på att medarbetaren ska be om det."),
]

REPORT_QUESTIONS = [
    "Om en av våra medarbetare närmade sig utmattning - hur skulle vi märka det innan "
    "sjukskrivningen? Vilken signal skulle nå oss?",
    "Vilka av våra möten, rutiner och sociala förväntningar kräver maskering för att delta "
    "på lika villkor?",
    "När vi delegerar en uppgift - lämnar vi över ett mål eller ett definierat första steg?",
    "Vem hos oss äger ansvaret för att föreslå en anpassning: medarbetaren eller chefen? Vad "
    "står det i vår rutin?",
    "Har vi en skriftlig rutin för arbetsanpassning enligt AFS 2020:5, och vet cheferna var "
    "den finns?",
    "Vilka anpassningar skulle vi kunna göra tillgängliga för alla, så att ingen behöver "
    "berätta om en diagnos för att använda dem?",
]

REPORT_METHOD = (
    "Observationerna bygger på hur Neurovibes verktyg används - Burnout-kalkylatorn, "
    "Uppgiftsnedbrytaren och Myndighetsnavigatorn. Inmatningarna lagras anonymiserat och "
    "kopplas aldrig till e-postadresser eller identifierbara personer.\n\n"
    "Det som gör materialet intressant är att inmatningarna sker i stunden, ofta när "
    "belastningen redan är ett faktum - inte i efterhand i en enkät. Det som gör det "
    "begränsat är volymen, och att urvalet är självselekterat. Båda sakerna gäller tills vi "
    "skriver något annat.\n\n"
    "Innehållet produceras av AI-system inom mänsklig ram och utgör inte medicinsk "
    "rådgivning. Se neurovibe.se/redaktionell-policy.html")


def build_report_pdf() -> bytes:
    """Observationsdokumentet som /data-rapport-2026.html erbjuder."""
    r = DeluxeReport(BRAND, BRAND_DK)
    pdf = r.pdf

    def footer_fn():
        pdf.set_y(-15)
        pdf.set_draw_color(*LINE)
        pdf.line(r.MARGIN, pdf.get_y(), 210 - r.MARGIN, pdf.get_y())
        pdf.set_y(-13)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4, _s("Neurovibe | neurovibe.se | Kvalitativa observationer, inte "
                          "statistik. Utgör inte medicinsk rådgivning."), align="C")

    pdf.footer = footer_fn
    r.cover("Neurovibe",
            "Neurodiversitet i svenskt arbetsliv 2026",
            "Observationer från våra verktyg",
            REPORT_INTRO)

    r.section("Om underlaget - läs detta först")
    r.lead(REPORT_CAVEAT)

    for title, body in REPORT_OBSERVATIONS:
        r.section(title)
        r.paragraph(body)

    r.section("Diskussionsfrågor för ledningsgruppen")
    r.paragraph("Sex frågor att ta med till nästa genomgång. De har inga rätta svar - poängen "
                "är att det oftast blir tyst på minst två av dem.", gap=2)
    r.bullets(REPORT_QUESTIONS)

    r.section("Metod och begränsningar")
    r.paragraph(REPORT_METHOD)

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
       arbetslivet, indelat i fysisk miljö, kommunikation, möten, fokus och ledarskap — välj
       2–3 att testa den här månaden.</p>
    <p style="margin-top:22px">Varma hälsningar,<br><b>Neurovibe</b><br>
       <a href="https://neurovibe.se" style="color:#d83131">neurovibe.se</a></p>
    <p style="font-size:11px;color:#9a9a9a;margin-top:22px">Du får detta för att du anmälde dig på
       neurovibe.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""
