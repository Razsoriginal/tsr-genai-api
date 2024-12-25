from flask import jsonify
from app.utils.prompts import sys_prompt, ref_prompt, ref_format, article_format
from app.core.download_audio import download_audio
from app.core.genai import genai_custom
from app.core.audio_processing import audio_processing
import os

def gen_article_data(video_url, config=None):
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400

    output_directory = "./data/audio/"
    yt_title, audio_path = download_audio(video_url, output_directory)

    try:
        print("\nGenerating article from audio...")

        transcribe_response = audio_processing(video_url=video_url, operation="transcribe", yt_title=yt_title, audio_path=audio_path, delete_audio=False)

        summarize_response = audio_processing(video_url=video_url, operation="summarize", yt_title=yt_title, audio_path=audio_path, delete_audio=False)

        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_format=ref_format)
        references_genai = audio_processing(video_url, "references", custom_prompt=formatted_ref_prompt, yt_title=yt_title, audio_path=audio_path, delete_audio=False)

        formatted_sys_prompt = sys_prompt.format(
            yt_title=yt_title,
            video_url=video_url,
            transcription_genai=transcribe_response['candidates'][0],
            #references_genai=references_genai, // Add this in prompt:  - **References:** {references_genai} 
            #summary_genai=summarize_response, // Add this in prompt:  - **Summary:** {summary_genai}
            article_format=article_format
        )

        article_response = audio_processing(video_url, "article-html", custom_prompt=formatted_sys_prompt, yt_title=yt_title, audio_path=audio_path, delete_audio=True)
        print("Generatin Article")

        response_data = {
            'transcription': transcribe_response['candidates'][0], 
            'summary': summarize_response['candidates'][0], 
            'references': references_genai['candidates'][0],      
            'article': article_response['candidates'][0]          
        }

        return response_data

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Failed to generate article', 'details': str(e)}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted downloaded audio: {audio_path}")