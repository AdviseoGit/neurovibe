with open("main.py", "r") as f:
    content = f.read()

content = content.replace("@app.post(\"/api/feedback\")\n: FeedbackRequest):", "@app.post(\"/api/feedback\")\nasync def save_feedback(req: FeedbackRequest):")

with open("main.py", "w") as f:
    f.write(content)
