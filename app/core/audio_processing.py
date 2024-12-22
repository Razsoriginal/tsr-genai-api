from app.core.download_audio import download_audio
from app.core.genai import genai_custom
import os

def audio_processing(video_url, operation):
    """Download audio, process it, and clean up."""
    output_directory = "./app/data/audio/"
    yt_title, audio_path = download_audio(video_url, output_directory)
    print(f"\n{operation.capitalize()} audio for video: {yt_title}...")
    response = genai_custom(f"{operation.capitalize()} the audio of the video '{yt_title}'.", audio_path)

    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Deleted downloaded audio: {audio_path}")
    return response