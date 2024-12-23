from flask import jsonify
from app.utils.prompts import sys_prompt, ref_prompt, ref_format, article_format
from app.core.download_audio import download_audio
from app.core.genai import genai_custom
import os

def gen_article_data(video_url, config=None):
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400

    output_directory = "./data/audio/"
    yt_title, audio_path = download_audio(video_url, output_directory)

    try:
        print("\nGenerating article from audio...")

        transcribe_response = genai_custom(f"Transcribe the audio of the video titled '{yt_title}'.", audio_path)

        summarize_response = genai_custom(f"Summarize the transcription of the video titled '{yt_title}'.", audio_path)

        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_format=ref_format)
        references_genai = genai_custom(formatted_ref_prompt, config=config)

        formatted_sys_prompt = sys_prompt.format(
            yt_title=yt_title,
            video_url=video_url,
            transcription_genai=transcribe_response,
            #references_genai=references_genai, // Add this in prompt:  - **References:** {references_genai} 
            #summary_genai=summarize_response, // Add this in prompt:  - **Summary:** {summary_genai}
            article_format=article_format
        )

        article_response = genai_custom(formatted_sys_prompt)

        response_data = {
            'transcription': transcribe_response, 
            'summary': summarize_response, 
            'references': references_genai,      
            'article': article_response          
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Failed to generate article', 'details': str(e)}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted downloaded audio: {audio_path}")