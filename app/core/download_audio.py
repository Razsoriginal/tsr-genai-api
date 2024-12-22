import os
import yt_dlp

def download_audio(url, output_path="."):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(id)s.%(ext)s', 
        'extract-audio': True,
        'audio-format': "mp3",
        'audio-quality': 0
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(info)
 
            if output_file.endswith(".webm"):
              old_output_file = output_file
              output_file = output_file[:-5]+".mp3"
              os.rename(old_output_file, output_file)
              print(f"File converted to {output_file}")
            print(f"Downloaded audio to {output_file}")
            return info['title'], output_file
        
    except Exception as e:
        print(f"An error occurred: {e}")