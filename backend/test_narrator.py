import sys
import os

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.narrator import generate_narration_audio, merge_audio_video

def test_narrator():
    print("Testing Audio Generation...")
    text = "This is a test narration. The audio should be generated and merged with the video."
    audio_path = generate_narration_audio(text)
    
    if audio_path and os.path.exists(audio_path):
        print(f"Audio generated successfully at: {audio_path}")
    else:
        print("Audio generation failed!")
        return

    print("\nTesting Video Merge...")
    # We need a dummy video to test merge. 
    # Let's check if we have any video in media/videos
    # If not, we can't test merge easily without generating one.
    # But we can try to find one.
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, "media")
    
    video_path = None
    for root, dirs, files in os.walk(media_dir):
        for file in files:
            if file.endswith(".mp4") and "narrated" not in file:
                video_path = os.path.join(root, file)
                break
        if video_path:
            break
            
    if video_path:
        print(f"Found video for testing: {video_path}")
        final_path = merge_audio_video(video_path, audio_path)
        
        if final_path and os.path.exists(final_path) and "narrated" in final_path:
            print(f"Merge successful! Output at: {final_path}")
        else:
            print(f"Merge failed. Result: {final_path}")
    else:
        print("No existing video found to test merge. Please generate a video first.")

if __name__ == "__main__":
    test_narrator()
