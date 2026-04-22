from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
import os
import asyncio
from openai import OpenAI
import psycopg2
from datetime import datetime

app = FastAPI()

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL") # We'll set this in Railway
client = OpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    message: str

class LeadRequest(BaseModel):
    email: EmailStr

class PostRequest(BaseModel):
    title: str
    content: str
    category: str = "Allmänt"

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/content", StaticFiles(directory="content"), name="content")

@app.get("/article")
async def read_article():
    return FileResponse("static/article.html")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

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
async def save_lead(req: LeadRequest):
    if not DATABASE_URL:
        # Fallback if DB not connected
        print(f"LEAD CAPTURED (No DB): {req.email}")
        return {"status": "success", "message": "Email saved (offline)"}
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
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
