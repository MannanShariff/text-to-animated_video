import os
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import uuid

# Get the directory of the current script (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
AUDIO_DIR = os.path.join(MEDIA_DIR, "audio")

# Ensure audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_narration_audio(text: str, filename: str = None) -> str:
    """
    Generates an MP3 audio file from the given text using gTTS.
    Returns the absolute path to the generated audio file.
    """
    try:
        if not filename:
            run_id = str(uuid.uuid4())
            filename = f"narration_{run_id}.mp3"
            
        # Save in BASE_DIR (backend/) so it's accessible to the script
        filepath = os.path.join(BASE_DIR, filename)
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filepath)
        
        return filepath
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def merge_audio_video(video_path: str, audio_path: str) -> str:
    """
    Merges the given audio file into the video file.
    Returns the path to the new video file with audio.
    If merging fails, returns the original video path.
    """
    try:
        if not audio_path or not os.path.exists(audio_path):
            print("Audio file not found, skipping merge.")
            return video_path
            
        if not video_path or not os.path.exists(video_path):
            print("Video file not found, skipping merge.")
            return video_path

        # Generate output path
        video_dir = os.path.dirname(video_path)
        video_filename = os.path.basename(video_path)
        output_filename = f"narrated_{video_filename}"
        output_path = os.path.join(video_dir, output_filename)

        # Load clips
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Handle duration mismatch
        # If audio is longer, we might need to loop video or cut audio. 
        # For simplicity, we'll let the video dictate duration, but if audio is longer, 
        # we might lose the end. Ideally, we'd extend the last frame of video.
        # Here, we'll just set audio to video duration (cut off) or loop video?
        # Let's just set the audio to the video.
        
        # Better approach: If audio is longer, extend video? No, that's hard with compiled video.
        # Let's just set the audio. If it's too long, it gets cut.
        
        final_audio = audio_clip
        
        # Set audio to video
        final_video = video_clip.with_audio(final_audio)
        
        # Write output
        # codec='libx264' is standard. audio_codec='aac'
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', logger=None)
        
        # Cleanup
        video_clip.close()
        audio_clip.close()
        
        return output_path

    except Exception as e:
        print(f"Error merging audio and video: {e}")
        with open("merge_error.log", "w") as f:
            f.write(str(e))
            import traceback
            traceback.print_exc(file=f)
        # Return original video on failure
        return video_path
