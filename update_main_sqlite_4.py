import urllib.request
import json

req = urllib.request.Request(
    'https://neurovibe.se/api/lead',
    data=json.dumps({"email": "test2@example.com", "source": "test_script_2"}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print(result)
except Exception as e:
    print(e)
