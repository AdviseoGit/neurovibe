with open("main.py", "r") as f:
    content = f.read()

content = content.replace(
"""class LeadRequest(BaseModel):
    email: EmailStr

class FeedbackRequest(BaseModel):""",
"""class LeadRequest(BaseModel):
    email: EmailStr
    source: str = "unknown"

class FeedbackRequest(BaseModel):""")

with open("main.py", "w") as f:
    f.write(content)
