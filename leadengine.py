"""
Neurovibe lead engine.

En plats för allt som rör leads: lagring, scoring, segmentering och notiser.
Ren stdlib + mailer.py. Kastar aldrig vidare till anropande request — returnerar
dict med resultat och loggar fel, så att ett trasigt SMTP eller en låst databas
aldrig gör att besökaren ser ett fel efter att ha lämnat sin e-post.

Segment:
  individ   — medarbetare/privatperson med NPF (B2C)
  arbetsgivare — chef, HR, D&I, arbetsmiljö (B2B, huvudintäkt)
  partner   — företagshälsovård, utbildare, hårdvara/akustik, mjukvara (annons/sponsring)
"""
import json
import os
import re
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Sätt NV_DATA_DIR till en monterad volym i produktion. Utan det ligger
# databasen i containerns filsystem och försvinner vid varje deploy.
DATA_DIR = os.environ.get("NV_DATA_DIR") or os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "neurovibe.db")

SEGMENTS = ("individ", "arbetsgivare", "partner")

# E-postdomäner som indikerar privatperson snarare än en organisation.
FREEMAIL_DOMAINS = {
    "gmail.com", "hotmail.com", "hotmail.se", "outlook.com", "outlook.se",
    "live.se", "live.com", "yahoo.com", "yahoo.se", "icloud.com", "me.com",
    "telia.com", "comhem.se", "bredband.net", "spray.se", "msn.com",
    "protonmail.com", "proton.me", "bahnhof.se",
}

# --- Scoring-vikter -------------------------------------------------------
# Håll dem här (inte utspridda i endpoints) så modellen kan justeras på ett ställe.
ROLE_SCORES = {
    "hr-chef": 30,
    "hr-specialist": 24,
    "di-ansvarig": 26,
    "chef": 20,
    "ledning": 28,
    "arbetsmiljo": 18,
    "skyddsombud": 12,
    "foretagshalsovard": 22,
    "fackligt": 12,
    "medarbetare": 6,
    "annat": 4,
}

SIZE_SCORES = {
    "1000+": 25,
    "250-999": 21,
    "50-249": 15,
    "10-49": 8,
    "1-9": 3,
    "vet-ej": 2,
}

NEED_SCORES = {
    "utbildning": 20,        # föreläsning/workshop för chefer
    "policy": 16,            # policy, process, AFS-efterlevnad
    "rekrytering": 15,
    "individuellt-arende": 12,
    "lokaler": 14,           # akustik, tysta rum, kontorsmiljö
    "verktyg": 10,
    "annonsera": 26,         # vill nå vår publik = direkt intäkt
    "annonsera-leads": 28,   # köper leads = högst betalningsvilja
    "annonsera-data": 20,
    "orienterar": 3,
}

TIMELINE_SCORES = {
    "omgaende": 20,
    "detta-kvartal": 13,
    "i-ar": 7,
    "vet-ej": 0,
}


# --- Databas -------------------------------------------------------------
def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Idempotent schema-setup. Anropas vid varje skrivning (billigt i SQLite)."""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                name TEXT,
                segment TEXT NOT NULL DEFAULT 'individ',
                role TEXT,
                company TEXT,
                company_size TEXT,
                need TEXT,
                timeline TEXT,
                phone TEXT,
                message TEXT,
                offer TEXT,
                source_page TEXT,
                referrer TEXT,
                utm_source TEXT,
                utm_medium TEXT,
                utm_campaign TEXT,
                consent INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                grade TEXT,
                status TEXT DEFAULT 'new',
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_segment ON leads(segment)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at DESC)")
        # En e-post får finnas i flera segment (samma person kan vara både
        # medarbetare och chef), men inte dubbletter inom samma segment.
        cur.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_leads_email_segment ON leads(email, segment)"
        )
        conn.commit()
    finally:
        conn.close()


# --- Scoring -------------------------------------------------------------
def is_business_email(email: str) -> bool:
    domain = email.split("@")[-1].strip().lower() if "@" in email else ""
    return bool(domain) and domain not in FREEMAIL_DOMAINS


def score_lead(data: dict) -> tuple[int, str]:
    """Returnerar (score 0-100, grade A-D).

    A = ring inom 24h, B = ring inom 3 arbetsdagar, C = nurture-sekvens,
    D = enbart nyhetsbrev.
    """
    segment = (data.get("segment") or "individ").lower()

    if segment == "individ":
        # B2C-leads poängsätts inte kommersiellt — de är publiken, inte köparen.
        # De får en låg baspoäng så att de aldrig hamnar i säljflödet.
        score = 10
        if data.get("need") in ("utbildning", "policy", "rekrytering"):
            score += 10  # signalerar att de kan bli en intern dörröppnare
        return min(score, 100), grade_for(score)

    score = 10  # bas: någon fyllde i ett formulär med flera fält

    score += ROLE_SCORES.get((data.get("role") or "annat").lower(), 4)
    score += SIZE_SCORES.get((data.get("company_size") or "vet-ej").lower(), 2)
    score += NEED_SCORES.get((data.get("need") or "orienterar").lower(), 3)
    score += TIMELINE_SCORES.get((data.get("timeline") or "vet-ej").lower(), 0)

    if is_business_email(data.get("email", "")):
        score += 10
    if (data.get("phone") or "").strip():
        score += 5
    if len((data.get("message") or "").strip()) > 60:
        score += 5  # skrev ett eget ärende = högre intent

    score = max(0, min(score, 100))
    return score, grade_for(score)


def grade_for(score: int) -> str:
    if score >= 78:
        return "A"
    if score >= 55:
        return "B"
    if score >= 32:
        return "C"
    return "D"


SLA = {
    "A": "Ring/mejla personligen inom 24h",
    "B": "Personligt mejl inom 3 arbetsdagar",
    "C": "Nurture-sekvens (rapport + case)",
    "D": "Nyhetsbrev",
}


# --- Skrivning -----------------------------------------------------------
_FIELDS = (
    "email", "name", "segment", "role", "company", "company_size", "need",
    "timeline", "phone", "message", "offer", "source_page", "referrer",
    "utm_source", "utm_medium", "utm_campaign", "consent",
)


def record_lead(data: dict) -> dict:
    """Sparar en lead och returnerar {ok, id, score, grade, duplicate}."""
    email = (data.get("email") or "").strip().lower()
    if not email or "@" not in email:
        return {"ok": False, "error": "invalid_email"}

    segment = (data.get("segment") or "individ").lower()
    if segment not in SEGMENTS:
        segment = "individ"
    data = {**data, "email": email, "segment": segment}

    score, grade = score_lead(data)

    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM leads WHERE email = ? AND segment = ?", (email, segment))
        duplicate = cur.fetchone() is not None

        values = [data.get(f) for f in _FIELDS]
        values[_FIELDS.index("consent")] = 1 if data.get("consent") else 0
        values[_FIELDS.index("segment")] = segment

        cur.execute(
            f"""
            INSERT INTO leads ({", ".join(_FIELDS)}, score, grade)
            VALUES ({", ".join("?" for _ in _FIELDS)}, ?, ?)
            ON CONFLICT(email, segment) DO UPDATE SET
                name = COALESCE(excluded.name, leads.name),
                role = COALESCE(excluded.role, leads.role),
                company = COALESCE(excluded.company, leads.company),
                company_size = COALESCE(excluded.company_size, leads.company_size),
                need = COALESCE(excluded.need, leads.need),
                timeline = COALESCE(excluded.timeline, leads.timeline),
                phone = COALESCE(excluded.phone, leads.phone),
                message = COALESCE(excluded.message, leads.message),
                offer = COALESCE(excluded.offer, leads.offer),
                score = MAX(excluded.score, leads.score),
                grade = CASE WHEN excluded.score > leads.score
                             THEN excluded.grade ELSE leads.grade END,
                updated_at = CURRENT_TIMESTAMP
            """,
            values + [score, grade],
        )
        # Läs tillbaka det lagrade värdet — vid en uppdatering behåller vi den
        # högsta poängen leaden någonsin fått, och det är den som ska styra SLA.
        cur.execute("SELECT id, score, grade FROM leads WHERE email = ? AND segment = ?",
                    (email, segment))
        row = cur.fetchone()
        conn.commit()
        conn.close()

        stored_score = row["score"] if row else score
        stored_grade = row["grade"] if row else grade
        print(f"[lead] {segment}/{stored_grade} {stored_score}p {email} "
              f"({'återkommande' if duplicate else 'ny'}) src={data.get('source_page')}")
        return {
            "ok": True,
            "id": row["id"] if row else None,
            "score": stored_score,
            "grade": stored_grade,
            "duplicate": duplicate,
        }
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] DB FEL: {exc}")
        # Fallback: skriv till fil så att en lead aldrig tappas helt.
        try:
            os.makedirs("leads", exist_ok=True)
            with open(os.path.join("leads", "fallback.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps({**data, "score": score, "grade": grade,
                                     "ts": datetime.now(timezone.utc).isoformat()},
                                    ensure_ascii=False) + "\n")
        except Exception as exc2:  # noqa: BLE001
            print(f"[lead] FALLBACK FEL: {exc2}")
        return {"ok": False, "error": "db_error", "score": score, "grade": grade}


def set_status(lead_id: int, status: str, notes: str | None = None) -> bool:
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()
        if notes is None:
            cur.execute("UPDATE leads SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (status, lead_id))
        else:
            cur.execute(
                "UPDATE leads SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, notes, lead_id))
        changed = cur.rowcount
        conn.commit()
        conn.close()
        return changed > 0
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] STATUS FEL: {exc}")
        return False


# --- Läsning -------------------------------------------------------------
def list_leads(segment: str | None = None, limit: int = 200) -> list[dict]:
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()
        if segment and segment in SEGMENTS:
            cur.execute(
                "SELECT * FROM leads WHERE segment = ? ORDER BY score DESC, created_at DESC LIMIT ?",
                (segment, limit))
        else:
            cur.execute(
                "SELECT * FROM leads ORDER BY score DESC, created_at DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] LIST FEL: {exc}")
        return []


def lead_stats() -> dict:
    """Aggregat för admin-dashboarden."""
    empty = {"total": 0, "by_segment": {}, "by_grade": {}, "by_status": {},
             "last_7_days": 0, "last_30_days": 0, "pipeline_a_b": 0, "top_sources": []}
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()

        def group(col):
            cur.execute(f"SELECT {col} AS k, COUNT(*) AS n FROM leads GROUP BY {col}")
            return {(r["k"] or "okänt"): r["n"] for r in cur.fetchall()}

        cur.execute("SELECT COUNT(*) AS n FROM leads")
        total = cur.fetchone()["n"]
        stats = {
            "total": total,
            "by_segment": group("segment"),
            "by_grade": group("grade"),
            "by_status": group("status"),
        }
        cur.execute("SELECT COUNT(*) AS n FROM leads WHERE created_at >= datetime('now','-7 days')")
        stats["last_7_days"] = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) AS n FROM leads WHERE created_at >= datetime('now','-30 days')")
        stats["last_30_days"] = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) AS n FROM leads WHERE grade IN ('A','B') AND segment != 'individ'")
        stats["pipeline_a_b"] = cur.fetchone()["n"]
        cur.execute(
            """SELECT COALESCE(source_page,'okänt') AS k, COUNT(*) AS n FROM leads
               GROUP BY k ORDER BY n DESC LIMIT 8""")
        stats["top_sources"] = [{"page": r["k"], "count": r["n"]} for r in cur.fetchall()]
        conn.close()
        return stats
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] STATS FEL: {exc}")
        return empty


def storage_info() -> dict:
    """Var ligger databasen, och överlever den en deploy?

    Visas i admin-dashboarden och loggas vid uppstart. Utan detta är enda sättet
    att upptäcka en felkonfigurerad volym att tappa leadsen först.
    """
    configured = bool(os.environ.get("NV_DATA_DIR"))
    exists = os.path.exists(DB_PATH)
    size = os.path.getsize(DB_PATH) if exists else 0
    return {
        "db_path": DB_PATH,
        "data_dir": DATA_DIR,
        "persistent": configured,
        "nv_data_dir_set": configured,
        "db_exists": exists,
        "db_size_bytes": size,
        "smtp_configured": _smtp_configured(),
    }


def _smtp_configured() -> bool:
    try:
        import mailer
        return mailer.configured()
    except Exception:  # noqa: BLE001
        return False


def leads_csv(segment: str | None = None) -> str:
    import csv
    import io
    rows = list_leads(segment=segment, limit=5000)
    buf = io.StringIO()
    cols = ["id", "created_at", "segment", "grade", "score", "status", "email", "name",
            "role", "company", "company_size", "need", "timeline", "phone",
            "offer", "source_page", "utm_source", "utm_campaign", "message"]
    writer = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue()


# --- Notiser -------------------------------------------------------------
def _esc(value) -> str:
    text = "" if value is None else str(value)
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _row_html(label: str, value) -> str:
    if not value:
        return ""
    return (f'<tr><td style="padding:6px 12px 6px 0;color:#666;white-space:nowrap">{_esc(label)}</td>'
            f'<td style="padding:6px 0;color:#111"><b>{_esc(value)}</b></td></tr>')


GRADE_COLORS = {"A": "#137333", "B": "#b06000", "C": "#5f6368", "D": "#9aa0a6"}

OFFER_LABELS = {
    "b2b-anpassningspaket": "Anpassningspaketet (HR-kit)",
    "b2b-genomlysning": "Neuroinklusions-genomlysning",
    "datarapport-2026": "Observationsdokumentet 2026",
    "data_report_2026": "Observationsdokumentet 2026 (gammalt formulär)",
    "b2b-samtal": "Bokat orienteringssamtal",
    "partner-mediakit": "Mediakit / annonsering",
    "individ-checklista": "Executive Function-checklistan",
    "individ-anpassningsmall": "Anpassningsmall till chefen",
}


def notify_owner_new_lead(data: dict, result: dict) -> None:
    """Skickar en notis till ägaren. Prio och nästa steg står i ämnesraden."""
    import mailer

    grade = result.get("grade", "D")
    segment = data.get("segment", "individ")
    company = data.get("company") or ""
    score = result.get("score", 0)

    if segment == "individ":
        subject = f"Ny prenumerant (Neurovibe) – {data.get('email')}"
    else:
        subject = (f"[{grade}] Ny {segment}-lead: {company or data.get('email')} "
                   f"– {score}p – {SLA.get(grade, '')}")

    rows = "".join([
        _row_html("Segment", segment),
        _row_html("Score", f"{score} / 100 (klass {grade})"),
        _row_html("Nästa steg", SLA.get(grade, "")),
        _row_html("Namn", data.get("name")),
        _row_html("E-post", data.get("email")),
        _row_html("Telefon", data.get("phone")),
        _row_html("Organisation", company),
        _row_html("Antal anställda", data.get("company_size")),
        _row_html("Roll", data.get("role")),
        _row_html("Behov", data.get("need")),
        _row_html("Tidsram", data.get("timeline")),
        _row_html("Erbjudande", OFFER_LABELS.get(data.get("offer"), data.get("offer"))),
        _row_html("Sida", data.get("source_page")),
        _row_html("Kampanj", " / ".join(
            [v for v in (data.get("utm_source"), data.get("utm_medium"),
                         data.get("utm_campaign")) if v])),
        _row_html("Återkommande", "Ja" if result.get("duplicate") else ""),
    ])

    message = data.get("message")
    message_html = ""
    if message:
        message_html = (
            '<p style="margin:20px 0 6px;color:#666;font-size:13px">Fritext:</p>'
            f'<blockquote style="margin:0;padding:12px 16px;background:#f6f6f6;'
            f'border-left:3px solid #D83131;color:#111;white-space:pre-wrap">'
            f'{_esc(message)}</blockquote>')

    html = f"""
    <div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:600px">
      <p style="display:inline-block;margin:0 0 16px;padding:4px 12px;border-radius:999px;
                background:{GRADE_COLORS.get(grade, '#5f6368')};color:#fff;
                font-size:12px;font-weight:700;letter-spacing:.08em">
        KLASS {grade} &middot; {score}P
      </p>
      <h2 style="margin:0 0 4px;font-size:20px;color:#111">
        {_esc(company or data.get('email'))}
      </h2>
      <p style="margin:0 0 20px;color:#666;font-size:14px">{_esc(SLA.get(grade, ''))}</p>
      <table style="border-collapse:collapse;font-size:14px">{rows}</table>
      {message_html}
      <p style="margin:28px 0 0;color:#999;font-size:12px">
        Neurovibe lead engine &middot; svara direkt på detta mejl för att nå leaden.
      </p>
    </div>
    """
    mailer.notify_owner(subject, html, reply_to=data.get("email"), from_name="Neurovibe Leads")


def _shell(title: str, body: str) -> str:
    return f"""
    <div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;
                max-width:560px;color:#111;line-height:1.6">
      <p style="margin:0 0 24px;font-size:13px;letter-spacing:.14em;
                text-transform:uppercase;color:#D83131;font-weight:700">Neurovibe</p>
      <h1 style="margin:0 0 16px;font-size:24px;line-height:1.3">{title}</h1>
      {body}
      <hr style="margin:32px 0;border:none;border-top:1px solid #e5e5e5">
      <p style="margin:0;color:#888;font-size:12px">
        Neurovibe &middot; Adviseo &middot; Stockholm<br>
        Du får detta mejl eftersom du fyllde i ett formulär på neurovibe.se.
        Svara på mejlet om du vill bli borttagen.<br>
        <a href="https://neurovibe.se/redaktionell-policy.html"
           style="color:#888">Redaktionell policy &amp; källor</a>
      </p>
    </div>
    """


def _btn(href: str, label: str) -> str:
    return (f'<p style="margin:24px 0"><a href="{href}" style="display:inline-block;'
            f'background:#D83131;color:#fff;text-decoration:none;padding:14px 26px;'
            f'border-radius:10px;font-weight:600">{label}</a></p>')


def confirmation_email(data: dict) -> tuple[str, str]:
    """Returnerar (subject, html) anpassat efter segment."""
    segment = data.get("segment", "individ")
    offer = data.get("offer") or ""
    name = (data.get("name") or "").split(" ")[0]
    hello = f"Hej {_esc(name)}," if name else "Hej,"

    if is_report_offer(offer):
        subject = "Neurodiversitet i svenskt arbetsliv 2026 – dina observationer"
        body = f"""
        <p>{hello}</p>
        <p>Dokumentet ligger som bilaga. Det innehåller de tre observationerna från
           sidan, diskussionsfrågorna för ledningsgruppen och en not om vad
           underlaget är och inte är.</p>
        <p>En sak vi hellre säger direkt än begraver i en fotnot: det här är
           <b>inte statistik</b>. Våra verktyg är nya och volymen är än så länge
           för liten för att räkna procent på, så vi publicerar inga siffror.
           Använd dokumentet som underlag för ett samtal — inte som mätdata.</p>
        <p>Vill du ha det som faktiskt är konkret i dag:</p>
        <ul style="padding-left:20px">
          <li><b>Lagkrav &amp; anpassningar</b> – vad AFS 2020:5 och
              diskrimineringslagen kräver av en arbetsgivare.
              <a href="https://neurovibe.se/lagkrav-anpassningar-arbetsmiljo.html">Läs guiden</a></li>
          <li><b>Anpassningsgeneratorn</b> – ett färdigt förslag att ta till chefen.
              <a href="https://neurovibe.se/verktyg-anpassningsgenerator.html">Öppna verktyget</a></li>
        </ul>
        {_btn("https://neurovibe.se/for-arbetsgivare.html", "Underlag för arbetsgivare")}
        """
    elif segment == "arbetsgivare":
        subject = "Ditt arbetsgivarpaket – Neurovibe"
        body = f"""
        <p>{hello}</p>
        <p>Tack för att du hörde av dig. <b>Arbetsgivarpaketet ligger här</b> —
           spara länken, den kräver ingen inloggning:</p>
        {_btn("https://neurovibe.se/arbetsgivarpaketet.html", "Öppna arbetsgivarpaketet")}
        <p>Det tyngsta i paketet är rutinmallen enligt AFS 2020:5, anpassnings&shy;processens
           fyra steg och samtalsmallen med de tio frågor en chef kan ställa utan att gå in
           på diagnos eller hälsa.</p>
        <p>Tre saker till som hör ihop med det:</p>
        <ul style="padding-left:20px">
          <li><b>Neurodiversitet i svenskt arbetsliv 2026</b> – tre mönster vi ser
              om maskering, exekutiv funktion och stödsystem, med en tydlig not om
              vad underlaget är och inte är.
              <a href="https://neurovibe.se/data-rapport-2026.html">Läs observationerna</a></li>
          <li><b>Lagkrav &amp; anpassningar</b> – vad arbetsmiljölagen, AFS 2020:5 och
              diskrimineringslagen faktiskt kräver av er som arbetsgivare.
              <a href="https://neurovibe.se/lagkrav-anpassningar-arbetsmiljo.html">Läs guiden</a></li>
          <li><b>Anpassningsgeneratorn</b> – låt medarbetaren själv formulera
              behoven inför chefssamtalet.
              <a href="https://neurovibe.se/verktyg-anpassningsgenerator.html">Öppna verktyget</a></li>
        </ul>
        <p>Jag återkommer personligen med förslag på nästa steg utifrån det du
           beskrev. Har du ett akut ärende går det snabbast att svara på detta mejl.</p>
        {_btn("https://neurovibe.se/for-arbetsgivare.html", "Se vad vi levererar")}
        """
    elif segment == "partner":
        subject = "Mediakit och samarbeten – Neurovibe"
        body = f"""
        <p>{hello}</p>
        <p>Tack för intresset. Vår publik består av två grupper som är svåra att
           nå någon annanstans i Sverige: medarbetare med NPF som aktivt söker
           lösningar, och chefer/HR som behöver uppfylla lagkrav kring skäliga
           anpassningar.</p>
        <p>Jag skickar aktuellt mediakit med trafik, målgruppsfördelning,
           placeringar och priser inom en arbetsdag. Berätta gärna i ett svar
           vilket format ni är mest intresserade av:</p>
        <ul style="padding-left:20px">
          <li>Sponsrad placering i en guide eller ett verktyg</li>
          <li>Leadgenerering (kvalificerade HR-kontakter)</li>
          <li>Samarbete kring innehåll eller data</li>
        </ul>
        {_btn("https://neurovibe.se/partner.html", "Se placeringar och format")}
        """
    else:
        subject = "Din checklista från Neurovibe"
        body = f"""
        <p>{hello}</p>
        <p>Checklistan ligger som bilaga i detta mejl. Den är byggd för de dagar
           då den exekutiva funktionen inte samarbetar — börja med ett steg, inte
           med hela listan.</p>
        <p>Tre saker som brukar hjälpa mest att börja med:</p>
        <ul style="padding-left:20px">
          <li><b>Uppgiftsnedbrytaren</b> – gör en luddig uppgift till tre små steg.
              <a href="https://neurovibe.se/verktyg-nedbrytare.html">Öppna</a></li>
          <li><b>Anpassningsgeneratorn</b> – få ett färdigt förslag att ta med till chefen.
              <a href="https://neurovibe.se/verktyg-anpassningsgenerator.html">Öppna</a></li>
          <li><b>Burnout-kalkylatorn</b> – se var din belastning ligger just nu.
              <a href="https://neurovibe.se/verktyg-burnout-kalkylator.html">Öppna</a></li>
        </ul>
        <p style="color:#666;font-size:13px">Neurovibe ger inte medicinska råd.
           Vi fokuserar på arbetsmiljö, anpassningar och praktiskt stöd.</p>
        {_btn("https://neurovibe.se/for-medarbetare.html", "Se alla verktyg")}
        """
    return subject, _shell(subject, body)


def is_report_offer(offer: str | None) -> bool:
    """Både nya `datarapport-2026` och gamla `data_report_2026` — det senare
    ligger kvar i cachade sidor hos besökare ett tag efter en deploy."""
    return bool(offer) and ("datarapport" in offer or "data_report" in offer)


def _attachment_for(offer: str | None, segment: str) -> tuple[str | None, str]:
    """(byggarfunktion i report_nv, filnamn) för ett erbjudande.

    Lovar en sida en PDF ska den PDF:en finnas här — annars får leaden fel fil,
    vilket är exakt vad som hände när rapportsidan skickade ut checklistan.
    """
    if is_report_offer(offer):
        return "build_report_pdf", "Neurovibe-observationer-2026.pdf"
    if segment == "individ":
        return "build_checklist_pdf", "Neurovibe-checklista.pdf"
    return None, ""


def deliver_lead(data: dict) -> None:
    """Körs som BackgroundTask: bekräftelse till leaden + notis till ägaren."""
    import mailer

    result = data.pop("_result", {}) or {}
    subject, html = confirmation_email(data)

    # Bilagan styrs av erbjudandet, inte av segmentet. Den som bad om
    # observationsdokumentet ska få det, inte checklistan.
    attachments = None
    builder, filename = _attachment_for(data.get("offer"), data.get("segment", "individ"))
    if builder:
        try:
            import report_nv
            pdf = getattr(report_nv, builder)()
            if pdf:
                attachments = [(filename, pdf, "application/pdf")]
        except Exception as exc:  # noqa: BLE001
            print(f"[lead] {builder} misslyckades: {exc}")

    try:
        mailer.send_email(data["email"], subject, html,
                          attachments=attachments, from_name="Neurovibe")
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] bekräftelsemejl misslyckades: {exc}")

    try:
        notify_owner_new_lead(data, result)
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] ägarnotis misslyckades: {exc}")


# --- Hjälp för migrering av gamla leads ----------------------------------
def migrate_legacy_leads() -> int:
    """Flyttar rader från den gamla neurovibe_leads-tabellen till leads."""
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='neurovibe_leads'")
        if not cur.fetchone():
            conn.close()
            return 0
        cur.execute("SELECT email, source, created_at FROM neurovibe_leads")
        legacy = cur.fetchall()
        moved = 0
        for row in legacy:
            cur.execute(
                """INSERT OR IGNORE INTO leads
                   (email, segment, offer, source_page, score, grade, status, created_at)
                   VALUES (?, 'individ', 'individ-checklista', ?, 10, 'D', 'legacy', ?)""",
                (row["email"], row["source"], row["created_at"]))
            moved += cur.rowcount
        conn.commit()
        conn.close()
        print(f"[lead] migrerade {moved} legacy-leads")
        return moved
    except Exception as exc:  # noqa: BLE001
        print(f"[lead] MIGRERING FEL: {exc}")
        return 0


VALID_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
