from app.core.download_audio import download_audio
from app.core.genai import genai_custom 
import os

def audio_processing(video_url, operation, custom_prompt=None, yt_title=None, audio_path=None, delete_audio=True):
    output_directory = "./data/audio/"

    try:
        if yt_title is None or audio_path is None:
            yt_title, audio_path = download_audio(video_url, output_directory)

        prompt = custom_prompt if custom_prompt else f"{operation.capitalize()} the audio of the video '{yt_title}'."
        print(f"\nProcessing audio for operation: {operation}...")

        for chunk in genai_custom(prompt, audio_path=audio_path, config=operation):
            if chunk:
                yield chunk

    except Exception as e:
        raise RuntimeError(f"Audio processing failed: {e}")

    finally:
        if delete_audio and audio_path and os.path.exists(audio_path):
            os.remove(audio_path)