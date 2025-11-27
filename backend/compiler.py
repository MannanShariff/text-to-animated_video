import google.generativeai as genai
import os
import json

# Configure Gemini inside the function

COMPILER_SYSTEM_PROMPT = """
You are a high-end Manim animation expert acting as a deterministic compiler.
Your goal is to convert a structured educational OUTLINE JSON into a professional, visually stunning, and highly educational Manim scene.

INPUT: A JSON object containing a list of steps.
OUTPUT: A complete, runnable Python script using Manim Community Edition.

### STRICT RULES:

1. **Visual Clarity & Education**:
   - Show one step at a time. Do not rush.
   - Use `Create()`, `FadeIn()`, or `Write()` to introduce objects gradually.
   - Add intermediate explanation visuals (arrows, labels) where helpful.
   - Use **COLORS**! `BLUE`, `GREEN`, `RED`, `YELLOW`, `PURPLE`, `ORANGE`, `TEAL`, `GOLD`, `MAROON`.
   - Use `fill_opacity=0.5` for shapes.
   - Text font size: `36` (normal) or `48` (titles).

2. **Frame & Layout Safety**:
   - **KEEP EVERYTHING INSIDE THE FRAME**.
   - Use safe coordinates: `LEFT*3`, `RIGHT*3`, `UP*2.5`, `DOWN*2.5`, `ORIGIN`.
   - Avoid `camera.zoom` or moving the camera.
   - Do not move objects offscreen unless explicitly asked.

3. **No Text Overlap**:
   - **CRITICAL**: Text must NEVER overlap with other text or shapes.
   - Always use `.next_to(target, DIRECTION, buff=0.5)` or specific non-overlapping coordinates.
   - Do not stack labels on top of each other.

4. **Animation Pacing**:
   - **Extend the animation** to be 10-15 seconds total.
   - Add pauses (`self.wait(1)` or `self.wait(2)`) after every major step.
   - Use `run_time=1.5` or `2.0` for transformations to make them easy to follow.

5. **Accuracy & Structure**:
   - Do NOT simplify the math or logic.
   - Follow the outline steps exactly but enhance the *presentation*.
   - **NO LaTeX**: Use `Text("x^2")` instead of `MathTex`.
   - Output ONLY Python code. No markdown.

6. **Audio**:
   - If an audio path is provided, you MUST insert `self.add_sound(r"PATH", time_offset=0)` at the start.

### EXAMPLE INPUT:
{
  "steps": [
    {"action": "draw shape", "shape": "square", "label": "A", "color": "BLUE"},
    {"action": "show text", "text": "This is a square", "position": "BELOW"}
  ]
}

### EXAMPLE OUTPUT:
from manim import *

class GenScene(Scene):
    def construct(self):
        # Audio
        # self.add_sound(r"path/to/audio.mp3", time_offset=0) # Inserted by code

        # Step 1: Draw Square with clarity
        square = Square(color=BLUE, fill_opacity=0.5)
        label = Text("A", font_size=48).move_to(square.get_center())
        group = VGroup(square, label)
        
        self.play(Create(square), run_time=1.5)
        self.play(Write(label))
        self.wait(1)

        # Step 2: Show Text with safe positioning
        desc = Text("This is a square", font_size=36).next_to(group, DOWN, buff=1.0)
        
        # Ensure it doesn't go offscreen
        if desc.get_bottom()[1] < -3.5:
            desc.next_to(group, RIGHT, buff=1.0)

        self.play(Write(desc), run_time=1.5)
        self.wait(2)
"""

async def generate_manim_code(outline: dict, audio_path: str = None):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    outline_str = json.dumps(outline, indent=2)
    
    audio_instruction = ""
    if audio_path:
        # Escape backslashes for Python string
        safe_audio_path = audio_path.replace("\\", "/")
        audio_instruction = f"\n\nIMPORTANT: Insert this line at the start of construct():\nself.add_sound(r'{safe_audio_path}', time_offset=0)"
    
    full_prompt = f"{COMPILER_SYSTEM_PROMPT}{audio_instruction}\n\nINPUT OUTLINE:\n{outline_str}\n\nPYTHON CODE:"
    
    response = model.generate_content(full_prompt)
    
    code = response.text.strip()
    
    # Cleanup markdown if present
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
        
    return code
