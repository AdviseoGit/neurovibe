import re

with open('/data/workspace/projects/neurovibe/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Pydantic model for BurnoutData
model_code = """class PostRequest(BaseModel):
    title: str
    content: str
    category: str = "Allmänt"

class BurnoutData(BaseModel):
    sensoryLoad: int
    cognitiveLoad: int
    workHours: int
    sleepQuality: int
    hyperfocusTime: int
    maskingLevel: int
    riskPercentage: int
"""
content = content.replace("class PostRequest(BaseModel):\n    title: str\n    content: str\n    category: str = \"Allmänt\"", model_code)

# Add endpoint for /api/burnout-data
endpoint_code = """
@app.post("/api/burnout-data")
async def save_burnout_data(data: BurnoutData):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "burnout_data.csv")
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("timestamp,sensoryLoad,cognitiveLoad,workHours,sleepQuality,hyperfocusTime,maskingLevel,riskPercentage\\n")
        
        import time
        timestamp = int(time.time())
        f.write(f"{timestamp},{data.sensoryLoad},{data.cognitiveLoad},{data.workHours},{data.sleepQuality},{data.hyperfocusTime},{data.maskingLevel},{data.riskPercentage}\\n")
        
    return {"status": "success"}

@app.get("/robots.txt")
"""
content = content.replace("@app.get(\"/robots.txt\")", endpoint_code)

with open('/data/workspace/projects/neurovibe/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
