# app/main/routes.py
from flask import Blueprint, request, jsonify
import time
from app.core.download_audio import download_audio
from app.core.genai import genai_custom
from app.core.audio_processing import audio_processing
from app.utils.prompts import sys_prompt
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
    try:
        response = audio_processing(video_url, "transcribe")
        return jsonify(response)
    except Exception:
        return jsonify({'error': 'Failed to summarize audio'}), 500

@main_bp.route('/summarize-ai', methods=['POST'])
def summarize_ai():
    video_url = request.json.get('video_url')
    try:
        response = audio_processing(video_url, "summarize")
        return jsonify(response)
    except Exception:
        return jsonify({'error': 'Failed to summarize audio'}), 500

@main_bp.route('/generate-article-ai', methods=['POST'])
def generate_article_ai():
    video_url = request.json.get('video_url')
    output_directory = "./data/audio/"
    yt_title, audio_path = download_audio(video_url, output_directory)
    try:
        print("\nGenerating article from audio...")
        transcribe_response = genai_custom(f"Transcribe the audio of the video '{yt_title}'.", audio_path)
        summarize_response = genai_custom(f"Summarize the audio of the video '{yt_title}'.", audio_path)
        article_response = genai_custom(sys_prompt, audio_path)

        response_data = {
            'transcription': transcribe_response,  
            'summary': summarize_response,        
            'article': article_response          
        }

        return jsonify(response_data)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Failed to generate article'}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted downloaded audio: {audio_path}")
