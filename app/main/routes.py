# app/main/routes.py
from flask import Blueprint, request, jsonify
import time
from app.core.download_audio import download_audio
from app.core.gen_article_data import gen_article_data
from app.core.genai import genai_custom
from app.core.audio_processing import audio_processing
from app.utils.prompts import ref_prompt, ref_format

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
        return jsonify({'error': 'Failed to summarize audio', 'details': str(e)}), 500

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
        formatted_ref_prompt = ref_prompt.format(video_url=video_url, ref_format=ref_format)
        references_genai = audio_processing(video_url, "references", custom_prompt=formatted_ref_prompt)
        return jsonify(references_genai)
    except Exception as e:
        print(f"Error during reference extraction: {e}")
        return jsonify({'error': 'Failed to extract references', 'details': str(e)}), 500

@main_bp.route('/generate-article-json', methods=['POST'])
def generate_article_json():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400
    try:
        response_data = gen_article_data(video_url, config="article-json")
        return jsonify(response_data)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to generate article', 'details': str(e)}), 500

# Deprecated route as we can generate HTML from the article JSON directly in frontend
# @main_bp.route('/generate-article-html', methods=['POST'])
# def generate_article_html():
#     article_json = request.json.get('artticle_json')
#     video_url = request.json.get('video_url')
#     if not video_url:
#         return jsonify({'error': 'Invalid request'}), 400
#     try:
#         if article_json:
#             print("Generate Article HTML...")
#             formatted_html_prompt = article_html_prompt.format(video_url=video_url, article_json=article_json)
#             html_genai = genai_custom(formatted_html_prompt, config="article-html")
#             return html_genai
#         else:
#             get_article_data = gen_article_data(video_url, config="article-json")
#             article_json = get_article_data['article']
#             formatted_html_prompt = article_html_prompt.format(video_url=video_url, article_json=article_json)
#             html_genai = genai_custom(formatted_html_prompt, config="article-html")
#             return jsonify(html_genai)
#     except Exception as e:
#         print(f"Error during reference extraction: {e}")
#         return jsonify({'error': 'Failed to generate article', 'details': str(e)}), 500