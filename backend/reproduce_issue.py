import requests
import json

prompt = "Demonstrate bubble sort with colored bars."

print(f"Sending prompt: {prompt}")

try:
    response = requests.post(
        "http://localhost:8000/generate",
        json={"prompt": prompt},
        timeout=120
    )
    
    if response.status_code == 200:
        data = response.json()
        with open("reproduction_output.txt", "w", encoding="utf-8") as f:
            f.write("--- GENERATED OUTLINE ---\n")
            f.write(json.dumps(data.get("outline"), indent=2))
            f.write("\n\n--- GENERATED CODE ---\n")
            f.write(data.get("code"))
            f.write("\n\n--- VIDEO URL ---\n")
            f.write(data.get("video_url"))
        print("Output written to reproduction_output.txt")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Request failed: {e}")
