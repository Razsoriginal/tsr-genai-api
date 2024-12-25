from app.core.download_audio import download_audio
from app.core.genai import genai_custom
import os

def audio_processing(video_url, operation, custom_prompt=None, yt_title=None, audio_path=None, delete_audio=True):
    """Download audio, process it, and clean up."""
    output_directory = "/data/audio/"
    audio_path = audio_path  
    try:
        if yt_title is None or audio_path is None:
            yt_title, audio_path = download_audio(video_url, output_directory)
        print(f"\n{operation.capitalize()} audio for video: {yt_title}...")
        prompt = custom_prompt if custom_prompt else f"{operation.capitalize()} the audio of the video '{yt_title}'."
        response = genai_custom(prompt, audio_path=audio_path, config=operation)
        return response  
    except Exception as e:  
        print(f"An error occurred during audio processing: {e}")
        return None  
    finally:
        if audio_path and os.path.exists(audio_path) and delete_audio: 
            os.remove(audio_path)
            print(f"Deleted downloaded audio: {audio_path}")