from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from teacher import generate_outline
from compiler import generate_manim_code
from runner import render_scene
from narrator import generate_narration_audio

app = FastAPI()

# Get the directory of the current script (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure the media directory exists
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Serve static frontend files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))

@app.post("/generate")
async def generate_video(request: PromptRequest):
    try:
        # 1. Teacher Brain: Generate Outline
        outline = await generate_outline(request.prompt)
        
        # 2. Narrator: Generate Audio FIRST
        narration_text = outline.get("narration")
        audio_path = None
        if narration_text:
            print(f"Generating audio for: {narration_text}")
            # Generate audio in BASE_DIR so it is accessible to the script
            audio_path = generate_narration_audio(narration_text)
            if audio_path:
                print(f"Audio generated at: {audio_path}")
        
        # 3. Compiler Brain: Generate Manim Code (with audio path)
        code = await generate_manim_code(outline, audio_path=audio_path)
        
        # 4. Runner: Execute Manim
        video_path = await render_scene(code)
        
        # Convert absolute path to relative URL for serving
        relative_to_media = os.path.relpath(video_path, start=MEDIA_DIR)
        video_url = f"/media/{relative_to_media}".replace("\\", "/")
        
        return {
            "status": "ok",
            "video_url": video_url,
            "outline": outline,
            "code": code,
            "narration": narration_text
        }
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating video: {error_msg}")
        with open("error.log", "w") as f:
            f.write(error_msg)
            import traceback
            traceback.print_exc(file=f)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
