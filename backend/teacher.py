import google.generativeai as genai
import os
import json

# Configure Gemini inside the function to ensure env vars are loaded

TEACHER_SYSTEM_PROMPT = """
You are the "Teacher Brain" of an educational video generator.
Your goal is to take a raw user prompt and convert it into a structured educational OUTLINE JSON.

Your output must be a valid JSON object with the following structure:
{
  "topic": "The topic of the video",
  "mode": "education",
  "steps": [
    {
      "action": "draw shape",
      "shape": "triangle|circle|square|line|arrow",
      "scale": 1.0,
      "label": "optional label",
      "position": "optional position (e.g., LEFT, RIGHT, UP, DOWN)"
    },
    // ... more steps
  ],
  "narration": "A short, simple paragraph (3-6 sentences) explaining the concept shown in the animation. Use simple English suitable for beginners."
}

Rules:
- Do NOT write any code.
- Do NOT write formulas in LaTeX (use simple text representation like a^2 + b^2 = c^2).
- Keep steps simple and sequential.
- Focus on visual explanation.
- The "action" field determines what happens. Supported actions: "draw shape", "show text", "wait", "clear".
"""

async def generate_outline(prompt: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    full_prompt = f"{TEACHER_SYSTEM_PROMPT}\n\nUSER PROMPT: {prompt}\n\nOUTPUT JSON:"
    
    response = model.generate_content(full_prompt)
    
    try:
        # cleanup response text to ensure it's valid JSON
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response: {response.text}")
        # Fallback or re-raise
        raise e
