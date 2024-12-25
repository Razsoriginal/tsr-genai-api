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

        transcribe_response = audio_processing(video_url, "transcribe")
        print("Generating Transcription")

        summarize_response = audio_processing(video_url, "summarize")
        print("Generating Summary")

        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_format=ref_format)
        references_genai = genai_custom(formatted_ref_prompt, config="references")
        print("Generating References")

        formatted_sys_prompt = sys_prompt.format(
            yt_title=yt_title,
            video_url=video_url,
            transcription_genai=transcribe_response['candidates'][0]['content']['parts'][0]['text'],
            #references_genai=references_genai, // Add this in prompt:  - **References:** {references_genai} 
            #summary_genai=summarize_response, // Add this in prompt:  - **Summary:** {summary_genai}
            article_format=article_format
        )

        article_response = genai_custom(formatted_sys_prompt, config="article-json", audio_path=audio_path)
        print("Generatin Article")

        response_data = {
            'transcription': transcribe_response['candidates'][0]['content']['parts'][0]['text'], 
            'summary': summarize_response['candidates'][0]['content']['parts'][0]['text'], 
            'references': references_genai['candidates'][0]['content']['parts'][0]['text'],      
            'article': article_response['candidates'][0]['content']['parts'][0]['text']          
        }

        return response_data

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Failed to generate article', 'details': str(e)}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted downloaded audio: {audio_path}")