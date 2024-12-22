# app/main/routes.py
from flask import Blueprint, request, jsonify
import time
from app.core.download_audio import download_audio
from app.core.genai import genai_custom
from app.core.audio_processing import audio_processing
from app.utils.prompts import sys_prompt, ref_prompt, ref_out, article_format
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'response': 'Welcome to the AI Blog Article Generator API!',
        'status': 'success',
        'timestamp': time.time()
    })

@main_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong',
        'status': 'success',
        'timestamp': time.time()
    })

@main_bp.route('/transcribe-ai', methods=['POST'])
def transcribe_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400
    try:
        response = audio_processing(video_url, "transcribe")
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': 'Failed to summarize audio', 'details': e}), 500

@main_bp.route('/summarize-ai', methods=['POST'])
def summarize_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400
    try:
        response = audio_processing(video_url, "summarize")
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': 'Failed to summarize audio', 'details': str(e)}), 500
    
@main_bp.route('/extract-references', methods=['POST'])
def extract_references():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400
    try:
        print("\nExtracting References...")
        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_out=ref_out)
        references_genai = genai_custom(formatted_ref_prompt)
        return jsonify({'references': references_genai})
    except Exception as e:
        print(f"Error during reference extraction: {e}")
        return jsonify({'error': 'Failed to extract references', 'details': str(e)}), 500

@main_bp.route('/generate-article-ai', methods=['POST'])
def generate_article_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400

    output_directory = "./data/audio/"
    yt_title, audio_path = download_audio(video_url, output_directory)

    try:
        print("\nGenerating article from audio...")

        transcribe_response = genai_custom(f"Transcribe the audio of the video titled '{yt_title}'.", audio_path)

        summarize_response = genai_custom(f"Summarize the transcription of the video titled '{yt_title}'.", audio_path)

        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_out=ref_out)
        references_genai = genai_custom(formatted_ref_prompt)

        formatted_sys_prompt = sys_prompt.format(
            yt_title=yt_title,
            video_url=video_url,
            transcription_genai=transcribe_response,
            references_genai=references_genai,
            summary_genai=summarize_response,
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
