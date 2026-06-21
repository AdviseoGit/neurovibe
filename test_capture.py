import requests

url = "http://localhost:8000/api/burnout-data"
data = {
    "sensoryLoad": 5,
    "cognitiveLoad": 5,
    "workHours": 40,
    "sleepQuality": 5,
    "hyperfocusTime": 5,
    "maskingLevel": 5,
    "riskPercentage": 40
}

try:
    response = requests.post(url, json=data)
    print("Response status:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
