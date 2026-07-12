from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.post("/api/lead", json={"email": "test3@example.com", "source": "test_script_3"})
print(response.status_code)
print(response.json())
