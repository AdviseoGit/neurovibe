from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi import Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import os
import sqlite3

import asyncio
from openai import OpenAI
import psycopg2
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_secret_key") # CHANGE THIS
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Endpoints nedan har redan offline-fallbacks när nyckeln saknas, så importen
# får aldrig krascha bara för att OPENAI_API_KEY inte är satt (annars går hela
# sajten — inklusive lead-flödet — ner om nyckeln försvinner ur miljön).
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

import leadengine

# Sajten pekar ut icke-www som primär i sitemap.xml, robots.txt och samtliga
# canonicals. Utan en redirect svarar www-varianten ändå med 200, så Google
# måste crawla varje sida två gånger för att sedan slå ihop dem via canonical.
# Det fungerar, men kostar crawlbudget och ger brus i Search Console.
CANONICAL_HOST = os.environ.get("NV_CANONICAL_HOST", "neurovibe.se")


@app.middleware("http")
async def canonical_url_redirect(request: Request, call_next):
    """Flyttar www till icke-www, och /index.html till /, i ett enda hopp."""
    host = request.headers.get("host", "")
    is_www = host.startswith("www.") and host[4:].split(":")[0] == CANONICAL_HOST
    is_index = request.url.path == "/index.html"

    if not (is_www or is_index):
        return await call_next(request)

    target = request.url
    if is_www:
        target = target.replace(netloc=host[4:])
    if is_index:
        target = target.replace(path="/")

    # Railway terminerar TLS, så request.url säger "http" även när besökaren
    # kom via https. Gäller båda fallen: utan detta skickar en https-besökare
    # vidare till http och får en nedgradering plus ett extra hopp.
    proto = request.headers.get("x-forwarded-proto")
    if proto or is_www:
        target = target.replace(scheme=proto or "https")

    return RedirectResponse(str(target), status_code=301)


@app.on_event("startup")
async def _startup_leadengine():
    """Se till att lead-tabellen finns och att gamla leads flyttas in i den."""
    leadengine.init_db()
    leadengine.migrate_legacy_leads()
    # Logga var databasen faktiskt hamnade. Är volymen monterad men NV_DATA_DIR
    # osatt går skrivningarna till containerns filsystem, och det syns inte
    # förrän nästa deploy redan har raderat leadsen.
    info = leadengine.storage_info()
    if info["persistent"]:
        print(f"[nv] lead-databas på monterad volym: {info['db_path']}")
    else:
        print(f"[nv] VARNING: lead-databasen ligger i containern ({info['db_path']}). "
              f"Sätt NV_DATA_DIR till volymens sökväg — annars försvinner "
              f"leadsen vid nästa deploy.")


# --- User & Auth Models ---
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Auth Utility Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Database User Functions ---
def get_user(db, username: str):
    # This is a placeholder. In a real app, you'd query the database.
    # For now, we'll use a dummy user.
    if username == "testuser":
        return UserInDB(username="testuser", hashed_password=get_password_hash("testpassword"))
    return None

# --- Current User Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(None, username=token_data.username) # Replace None with DB connection
    if user is None:
        raise credentials_exception
    return user

# --- API Endpoints ---
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(None, form_data.username) # Replace None with DB connection
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/content", StaticFiles(directory="content"), name="content")

@app.get("/article")
async def read_article():
    return FileResponse("static/article.html")




@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# ... (rest of the original endpoints)
class ChatRequest(BaseModel):
    message: str

class LeadRequest(BaseModel):
    """Ett formulär för alla segment. Bara email + consent krävs.

    segment: individ | arbetsgivare | partner
    """
    email: EmailStr
    source: str = "unknown"
    segment: str = "individ"
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    company_size: Optional[str] = None
    need: Optional[str] = None
    timeline: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None
    offer: Optional[str] = None
    source_page: Optional[str] = None
    referrer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    consent: bool = False

class FeedbackRequest(BaseModel):
    tool: str
    rating: int
    comment: str = ""

class PostRequest(BaseModel):
    title: str
    content: str
    category: str = "Allmänt"

class ToolUsageData(BaseModel):
    tool: str
    modules: Optional[list[str]] = None
    input_text: Optional[str] = None
    output_text: Optional[str] = None
    metadata: Optional[dict] = None

class BurnoutData(BaseModel):
    sensoryLoad: int
    cognitiveLoad: int
    workHours: int
    sleepQuality: int
    hyperfocusTime: int
    maskingLevel: int
    riskPercentage: int



@app.post("/api/tool-usage")
async def save_tool_usage(data: ToolUsageData):
    os.makedirs("data", exist_ok=True)
    import time
    import json
    import sqlite3
    import os
    
    timestamp = int(time.time())
    modules_str = json.dumps(data.modules) if data.modules else ""
    input_str = data.input_text.replace("\n", " ").replace(",", ";") if data.input_text else ""
    output_str = data.output_text.replace("\n", " ").replace(",", ";") if data.output_text else ""
    metadata_str = json.dumps(data.metadata) if data.metadata else ""
    
    # Save to SQLite
    try:
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool TEXT NOT NULL,
                modules TEXT,
                input_text TEXT,
                output_text TEXT,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        cur.execute(
            "INSERT INTO tool_usage (tool, modules, input_text, output_text, metadata) VALUES (?, ?, ?, ?, ?)",
            (data.tool, modules_str, input_str, output_str, metadata_str)
        )
        conn.commit()
        conn.close()
        print(f"USAGE LOGGED (SQLite): {data.tool}")
    except Exception as e:
        print(f"SQLite Tool Usage Error: {e}")
        
    # Also save to CSV as fallback/legacy
    file_path = os.path.join("data", "tool_usage.csv")
    file_exists = os.path.isfile(file_path)
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("timestamp,tool,modules,input_text,output_text,metadata\n")
            f.write(f'{timestamp},{data.tool},"{modules_str}","{input_str}","{output_str}","{metadata_str}"\n')
    except Exception as e:
        print(f"CSV error: {e}")
        
    return {"status": "success"}


class MyndighetData(BaseModel):
    selectedSupport: str
    selectedAgency: str
    difficulty: int
    helpFound: bool

@app.post("/api/myndighet-data")
async def save_myndighet_data(data: MyndighetData):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "myndighet_data.csv")
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("timestamp,selectedSupport,selectedAgency,difficulty,helpFound\n")
        
        import time
        timestamp = int(time.time())
        f.write(f"{timestamp},{data.selectedSupport},{data.selectedAgency},{data.difficulty},{data.helpFound}\n")
        
    return {"status": "success"}

@app.post("/api/burnout-data")

async def save_burnout_data(data: BurnoutData):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "burnout_data.csv")
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("timestamp,sensoryLoad,cognitiveLoad,workHours,sleepQuality,hyperfocusTime,maskingLevel,riskPercentage\n")
        
        import time
        timestamp = int(time.time())
        f.write(f"{timestamp},{data.sensoryLoad},{data.cognitiveLoad},{data.workHours},{data.sleepQuality},{data.hyperfocusTime},{data.maskingLevel},{data.riskPercentage}\n")
        
    return {"status": "success"}

@app.get("/robots.txt")

async def robots():
    return FileResponse("static/robots.txt")

@app.get("/llms.txt")
async def llms_txt():
    return FileResponse("static/llms.txt")

@app.get("/ads.txt")
async def ads_txt():
    return FileResponse("static/ads.txt")

@app.get("/schema.json")
async def schema_json():
    return FileResponse("static/schema.json")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("static/sitemap.xml")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.svg")

# Catch-all route to serve any .html file from the static directory from the root URL
@app.get("/{path:path}", response_class=FileResponse)
async def serve_html(path: str):
    if path.endswith(".html"):
        file_path = os.path.join("static", path)
        if os.path.exists(file_path):
            return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Item not found")

def _lead_payload(req: LeadRequest, segment_override: Optional[str] = None) -> dict:
    data = req.model_dump()
    data["email"] = str(req.email)
    # source är det gamla fältnamnet; behåll bakåtkompatibilitet.
    data["source_page"] = req.source_page or req.source
    if segment_override:
        data["segment"] = segment_override
    data.pop("source", None)
    return data


def _handle_lead(req: LeadRequest, background: BackgroundTasks,
                 segment_override: Optional[str] = None):
    data = _lead_payload(req, segment_override)
    result = leadengine.record_lead(data)

    # Mejl går alltid ut, även om skrivningen till databasen fallerade —
    # då finns leaden kvar i leads/fallback.jsonl och i ägarens inkorg.
    background.add_task(leadengine.deliver_lead, {**data, "_result": result})

    if not result.get("ok"):
        # Leaden är räddad via fallback + mejl, så besökaren ska inte se ett fel.
        print(f"[lead] sparad via fallback: {data['email']}")

    return {
        "status": "success",
        "segment": data["segment"],
        "grade": result.get("grade"),
        "next": f"/tack.html?segment={data['segment']}",
    }


@app.post("/api/lead")
async def save_lead(req: LeadRequest, background: BackgroundTasks):
    """Generisk lead-endpoint. Används av alla formulär via leadflow.js."""
    return _handle_lead(req, background)


@app.post("/api/b2b-lead")
async def save_b2b_lead(req: LeadRequest, background: BackgroundTasks):
    """Kvalificerad arbetsgivarlead (chef, HR, D&I, arbetsmiljö)."""
    return _handle_lead(req, background, segment_override="arbetsgivare")


@app.post("/api/partner-lead")
async def save_partner_lead(req: LeadRequest, background: BackgroundTasks):
    """Leverantör/partner som vill nå vår publik (mediakit, sponsring, leads)."""
    return _handle_lead(req, background, segment_override="partner")


def _require_admin(request: Request):
    expected = os.environ.get("INTERNAL_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="INTERNAL_API_KEY not configured")
    if request.headers.get("X-API-KEY") != expected:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.get("/api/admin/leads")
async def get_admin_leads(request: Request, segment: Optional[str] = None, limit: int = 200):
    _require_admin(request)
    return {
        "stats": leadengine.lead_stats(),
        "sla": leadengine.SLA,
        "storage": leadengine.storage_info(),
        "leads": leadengine.list_leads(segment=segment, limit=min(limit, 1000)),
    }


@app.get("/api/admin/leads.csv")
async def get_admin_leads_csv(request: Request, segment: Optional[str] = None):
    _require_admin(request)
    return PlainTextResponse(
        leadengine.leads_csv(segment=segment),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="neurovibe-leads.csv"'},
    )


class LeadStatusRequest(BaseModel):
    lead_id: int
    status: str
    notes: Optional[str] = None


@app.post("/api/admin/lead-status")
async def update_lead_status(req: LeadStatusRequest, request: Request):
    _require_admin(request)
    ok = leadengine.set_status(req.lead_id, req.status, req.notes)
    if not ok:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"status": "success"}

@app.post("/api/feedback")
async def save_feedback(req: FeedbackRequest):
    if not DATABASE_URL:
        print(f"FEEDBACK CAPTURED (No DB): Tool={req.tool}, Rating={req.rating}, Comment={req.comment}")
        return {"status": "success", "message": "Feedback saved (offline)"}
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Lazy table creation
        cur.execute("""
            CREATE TABLE IF NOT EXISTS neurovibe_feedback (
                id SERIAL PRIMARY KEY,
                tool VARCHAR(100) NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute(
            "INSERT INTO neurovibe_feedback (tool, rating, comment) VALUES (%s, %s, %s)",
            (req.tool, req.rating, req.comment)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"Feedback DB Error: {e}")
        raise HTTPException(status_code=500, detail="Could not save feedback")


@app.get("/api/admin/feedback")
async def get_admin_feedback(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != os.environ.get("INTERNAL_API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if not DATABASE_URL:
        return []
        
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, tool, rating, comment, created_at FROM neurovibe_feedback ORDER BY created_at DESC LIMIT 100")
        results = [{"id": r[0], "tool": r[1], "rating": r[2], "comment": r[3], "created_at": str(r[4])} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Admin DB Error: {e}")
        # If table doesn't exist yet, just return empty array
        return []


@app.get("/api/resources")
async def get_resources():
    # In a real dynamic system, this could come from PostgreSQL (e.g. neurovibe_resources table)
    # For now, we return a structured JSON representing the tools/guides to demonstrate the dynamic loading
    resources = [
        {
            "id": "verktyg-nedbrytare",
            "type": "tool",
            "title": "Uppgiftsnedbrytaren",
            "description": "Övervinn exekutiv dysfunktion. Få överväldigande uppgifter nedbrutna i tre extremt små, hanterbara steg.",
            "url": "/verktyg-nedbrytare.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>',
            "color": "indigo"
        },
        {
            "id": "verktyg-fokus-timer",
            "type": "tool",
            "title": "Fokus Timer",
            "description": "En visuell timer anpassad för neurodiversitet med korta arbetspass och tydlig struktur för att hantera tidsuppfattning.",
            "url": "/verktyg-fokus-timer.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>',
            "color": "indigo"
        },
        {
            "id": "verktyg-intervjuguide",
            "type": "tool",
            "title": "Intervjuguide",
            "description": "Bygg en neuroinkluderande intervjumall som mäter kompetens, inte förmågan att kallprata.",
            "url": "/intervju-guide.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>',
            "color": "green",
            
        },
        {
            "id": "verktyg-burnout",
            "type": "tool",
            "title": "Burnout Prevention Calculator",
            "description": "Mät din riskzon baserat på sensorisk belastning, maskering och kognitiva krav för att förhindra autistisk utmattning.",
            "url": "/verktyg-burnout-kalkylator.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>',
            "color": "red"
        },
        {
            "id": "verktyg-anpassningsgenerator",
            "type": "tool",
            "title": "Anpassningsgeneratorn",
            "description": "Välj dina största utmaningar i arbetsmiljön och få ett konkret, färdigt förslag på anpassningar att ta med till chefen.",
            "url": "/verktyg-anpassningsgenerator.html",
            "icon": "<svg class=\"w-6 h-6\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4\"></path></svg>",
            "color": "green",
            
        }
        ,
        {
            "id": "guide-masking-workplace",
            "type": "guide",
            "title": "Maskering på arbetsplatsen (Guide)",
            "description": "En djupgående guide om den osynliga ansträngningen med att maskera neurodivergenta drag och hur arbetsplatser kan skapa en mer accepterande kultur.",
            "url": "/maskering-pa-arbetsplatsen.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>',
            "color": "yellow"
        },
        {
            "id": "guide-adhd-workplace",
            "type": "guide",
            "title": "ADHD på arbetsplatsen (Guide)",
            "description": "Så skapar du en neuroinkluderande miljö. En djupgående guide för chefer och HR kring varför neurodiversitet är en styrka och hur man stöttar det.",
            "url": "/article_adhd_workplace.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>',
            "color": "indigo"
        }
    ]
    return resources

@app.get("/api/posts")
async def get_posts():
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Create table if not exists (lazy migration)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS neurovibe_posts (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        cur.execute("SELECT id, title, content, category, published_at FROM neurovibe_posts ORDER BY published_at DESC")
        posts = [{"id": r[0], "title": r[1], "content": r[2], "category": r[3], "date": r[4].strftime("%Y-%m-%d")} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return posts
    except Exception as e:
        print(f"Posts Error: {e}")
        return []

@app.post("/api/posts")
async def create_post(req: PostRequest, request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != os.environ.get("INTERNAL_API_KEY"):
        raise HTTPException(status_code=403)
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO neurovibe_posts (title, content, category, published_at) VALUES (%s, %s, %s, %s)",
        (req.title, req.content, req.category, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "success"}

@app.post("/api/breakdown")
async def breakdown_endpoint(req: ChatRequest):
    if not OPENAI_API_KEY:
        await asyncio.sleep(1.5)
        return {"response": "<b>API offline.</b><br>1. Andas<br>2. Hämta vatten<br>3. Prova igen senare"}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Du är ett neuroinkluderande verktyg som bryter ner överväldigande uppgifter. "
                        "Användaren ger dig en uppgift som känns för stor eller luddig. "
                        "Din enda uppgift är att returnera EXAKT TRE, extremt små, konkreta och friktionsfria steg för att påbörja uppgiften. "
                        "Steg 1 måste vara löjligt enkelt (t.ex. 'Öppna dokumentet' eller 'Ta fram ett glas vatten'). "
                        "Returnera svaret formaterat i HTML med en <ul> lista och <li> taggar. Ingen annan text."
                    )
                },
                {"role": "user", "content": req.message}
            ],
            max_tokens=150,
            temperature=0.3
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"Kunde inte bryta ner uppgiften just nu."}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not OPENAI_API_KEY:
        await asyncio.sleep(1.5)
        return {"response": "Jag är i zen-offline läge just nu. Kontrollera API-nyckeln."}

    try:
        # Load latest research and regulatory context
        knowledge_context = ""
        try:
            with open("research_knowledge.md", "r", encoding="utf-8") as f:
                knowledge_context = f.read()
        except:
            pass

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Du är 'Guiden', en lugn och stödjande AI-assistent för Neurovibe. "
                        "Din uppgift är att hjälpa personer med NPF att bryta ner överväldigande uppgifter. "
                        f"AKTUELL KUNSKAP (Använd vid behov för att ge korrekt stöd): {knowledge_context} "
                        "STRATEGI: När du har gett ett bra svar eller känner att användaren fått värde, "
                        "inkludera ALLTID den dolda taggen 'PROMPT_LEAD' sist i ditt svar. "
                        "Berätta först att användaren kan få en fullständig 'Executive Function Recovery Plan' "
                        "skickad till sig genom att registrera sin e-post i rutan som kommer dyka upp. "
                        "Håll tonen mjuk, zen-liknande och kravlös. Använd max 3 korta punkter för uppgifter. Språk: Svenska."
                    )
                },
                {"role": "user", "content": req.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"Det uppstod ett fel i tystnaden: {str(e)}"}


    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}


@app.get("/api/stats/leads")
async def get_stats_leads():
    # Publika leads-stats för scoreboard
    try:
        stats = leadengine.lead_stats()
        return {
            "total": stats.get("total", 0),
            "last_7_days": stats.get("last_7_days", 0)
        }
    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}
    except Exception as e:
        return {"total": 0, "last_7_days": 0, "error": str(e)}
