from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi import Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import os
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

client = OpenAI(api_key=OPENAI_API_KEY)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def _deliver_welcome_nv(email: str):
    import mailer
    import report_nv
    pdf = None
    try:
        pdf = report_nv.build_checklist_pdf()
    except Exception as e:
        print(f"[nv] checklist pdf failed: {e}")
    atts = [("Neurovibe-checklista.pdf", pdf, "application/pdf")] if pdf else None
    mailer.send_email(email, "Valkommen till Neurovibe - din checklista",
                      report_nv.user_email_html(), attachments=atts, from_name="Neurovibe")
    mailer.notify_owner("Ny lead - Neurovibe (vantelista)",
                        f"<p>Ny lead: <b>{email}</b></p>", reply_to=email, from_name="Neurovibe")


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


@app.post("/api/waitlist")
async def join_waitlist(email: str = Form(...)):
    # Create dir if not exists
    os.makedirs(os.path.join(DATA_DIR, "leads"), exist_ok=True)
    waitlist_file = os.path.join(DATA_DIR, "leads", "waitlist.txt")
    
    with open(waitlist_file, "a") as f:
        f.write(f"{email}\n")
        
    return RedirectResponse(url="/waitlist-success.html", status_code=303)

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# ... (rest of the original endpoints)
class ChatRequest(BaseModel):
    message: str

class LeadRequest(BaseModel):
    email: EmailStr

class FeedbackRequest(BaseModel):
    tool: str
    rating: int
    comment: str = ""

class PostRequest(BaseModel):
    title: str
    content: str
    category: str = "Allmänt"

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
@app.get("/{filename}", response_class=FileResponse)
async def serve_html(filename: str):
    if filename.endswith(".html"):
        file_path = os.path.join("static", filename)
        if os.path.exists(file_path):
            return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/api/lead")
async def save_lead(req: LeadRequest, background: BackgroundTasks):
    background.add_task(_deliver_welcome_nv, req.email)
    if not DATABASE_URL:
        # Fallback if DB not connected
        print(f"LEAD CAPTURED (No DB): {req.email}")
        return {"status": "success", "message": "Email saved (offline)"}
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS neurovibe_leads (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                source VARCHAR(64),
                created_at TIMESTAMP DEFAULT NOW()
            )
            """
        )
        cur.execute(
            "INSERT INTO neurovibe_leads (email, source) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
            (req.email, "beta_landing")
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Could not save email")


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
            "id": "verktyg-burnout",
            "type": "tool",
            "title": "Burnout Prevention Calculator",
            "description": "Mät din riskzon baserat på sensorisk belastning, maskering och kognitiva krav för att förhindra autistisk utmattning.",
            "url": "/verktyg-burnout-kalkylator.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>',
            "color": "red",
            "badge": "NYTT VERKTYG"
        },
        {
            "id": "mall-arbetsgivare",
            "type": "template",
            "title": "Mall för Arbetsplatsanpassning",
            "description": "Ett formellt men vänligt dokument du kan fylla i och ge till din chef för att begära anpassningar (t.ex. brusreducerande hörlurar eller hemarbete).",
            "url": "/template-employer.html",
            "icon": '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>',
            "color": "green"
        },
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
