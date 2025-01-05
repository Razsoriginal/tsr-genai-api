from app.core.audio_processing import audio_processing
from app.core.download_audio import download_audio
from app.utils.prompts import sys_prompt, ref_prompt, ref_format, article_format
import os

class AudioService:
    @staticmethod
    def transcribe(video_url, yt_title=None, audio_path=None, delete_audio=True):
        for chunk in audio_processing(video_url=video_url, operation="transcribe", yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio):
            yield chunk

    @staticmethod
    def summarize(video_url, yt_title=None, audio_path=None, delete_audio=True):
        for chunk in audio_processing(video_url=video_url, operation="summarize", yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio):
            yield chunk

    @staticmethod
    def extract_references(video_url, yt_title=None, audio_path=None, delete_audio=True):
        for chunk in audio_processing(video_url, "references", custom_prompt=ref_prompt.format(video_url=video_url, ref_format=ref_format), yt_title=yt_title, audio_path=audio_path, delete_audio=delete_audio):
            yield chunk

    @staticmethod
    def generate_article_json(video_url):
        output_directory = "./data/audio/"
        yt_title, audio_path = download_audio(video_url, output_directory)

        try:
            transcription_chunks = AudioService.transcribe(video_url, yt_title, audio_path, delete_audio=False)
            transcription = ''.join(chunk for chunk in transcription_chunks)

            summary_chunks = AudioService.summarize(video_url, yt_title, audio_path, delete_audio=False)
            summary = ''.join(chunk for chunk in summary_chunks)

            references_chunks = AudioService.extract_references(video_url, yt_title, audio_path, delete_audio=False)
            references = ''.join(chunk for chunk in references_chunks)

            formatted_sys_prompt = sys_prompt.format(
                yt_title=yt_title,
                video_url=video_url,
                transcription_genai=transcription,
                article_format=article_format
            )

            article_chunks = audio_processing(video_url, "article-html", custom_prompt=formatted_sys_prompt, yt_title=yt_title, audio_path=audio_path, delete_audio=True)
            article = ''.join(chunk for chunk in article_chunks)

            yield {
                'transcription': transcription,
                'summary': summary,
                'references': references,
                'article': article
            }

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)