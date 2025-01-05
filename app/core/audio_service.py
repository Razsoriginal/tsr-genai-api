from app.core.audio_processing import audio_processing
from app.core.download_audio import download_audio
from app.utils.prompts import sys_prompt, ref_prompt, ref_format, article_format
import os

class AudioService:
    @staticmethod
    def transcribe(video_url, yt_title=None, audio_path=None, delete_audio=True):
        return audio_processing(video_url=video_url, operation="transcribe", yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio)

    @staticmethod
    def summarize(video_url, yt_title=None, audio_path=None, delete_audio=True):
        return audio_processing(video_url=video_url, operation="summarize", yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio)

    @staticmethod
    def extract_references(video_url, yt_title=None, audio_path=None, delete_audio=True):
        formatted_prompt = ref_prompt.format(video_url=video_url, ref_format=ref_format)
        return audio_processing(video_url, "references", custom_prompt=formatted_prompt, yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio)

    @staticmethod
    def generate_article_json(video_url):
        output_directory = "./data/audio/"
        yt_title, audio_path = download_audio(video_url, output_directory)

        try:
            transcription = AudioService.transcribe(video_url, yt_title, audio_path, delete_audio=False)
            summary = AudioService.summarize(video_url, yt_title, audio_path, delete_audio=False)
            references = AudioService.extract_references(video_url, yt_title, audio_path, delete_audio=False)

            formatted_sys_prompt = sys_prompt.format(
                yt_title=yt_title,
                video_url=video_url,
                transcription_genai=transcription['candidates'][0],
                article_format=article_format
            )

            article = audio_processing(video_url, "article-html", custom_prompt=formatted_sys_prompt, yt_title=yt_title, audio_path=audio_path, delete_audio=True)

            return {
                'transcription': transcription['candidates'][0],
                'summary': summary['candidates'][0],
                'references': references['candidates'][0],
                'article': article['candidates'][0]
            }

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
