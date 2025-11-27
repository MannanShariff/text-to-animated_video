import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/generate",
        json={"prompt": "Show me a rotating square"},
        timeout=60
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
