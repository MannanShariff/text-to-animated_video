import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("No API Key found")
    exit(1)

genai.configure(api_key=api_key)

print("Listing models...")
try:
    with open("models_clean.txt", "w", encoding="utf-8") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(m.name + "\n")
                print(m.name)
except Exception as e:
    print(f"Error: {e}")
