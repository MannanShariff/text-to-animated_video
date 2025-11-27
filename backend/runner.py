import os
import subprocess
import uuid

# Get the directory of the current script (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")

async def render_scene(code: str):
    # Create a unique ID for this run
    run_id = str(uuid.uuid4())
    filename = f"scene_{run_id}.py"
    
    # Save code to file in the backend directory
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(code)
        
    # Run Manim
    # manim -qm --media_dir MEDIA_DIR filename.py GenScene
    
    cmd = ["manim", "-qm", "--media_dir", MEDIA_DIR, filepath, "GenScene"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Manim Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Manim Error:", e.stderr)
        raise Exception(f"Manim failed: {e.stderr}")
        
    # Construct expected output path
    # Manim structure with --media_dir: {MEDIA_DIR}/videos/{filename_without_extension}/720p30/GenScene.mp4
    
    video_folder = filename.replace(".py", "")
    video_path = os.path.join(MEDIA_DIR, "videos", video_folder, "720p30", "GenScene.mp4")
    
    if not os.path.exists(video_path):
        raise Exception(f"Video file not found at {video_path}")
        
    return video_path
