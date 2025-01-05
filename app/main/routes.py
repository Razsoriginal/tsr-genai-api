from flask import Blueprint, request
from app.core.audio_service import AudioService
from app.utils.responses import error_response, success_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return success_response('Welcome to the AI Blog Article Generator API!')

@main_bp.route('/transcribe-ai', methods=['POST'])
def transcribe_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    try:
        response = AudioService.transcribe(video_url)
        return success_response(response)
    except Exception as e:
        return error_response('Failed to transcribe audio', details=str(e))

@main_bp.route('/summarize-ai', methods=['POST'])
def summarize_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    try:
        response = AudioService.summarize(video_url)
        return success_response(response)
    except Exception as e:
        return error_response('Failed to summarize audio', details=str(e))

@main_bp.route('/extract-references', methods=['POST'])
def extract_references():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    try:
        response = AudioService.extract_references(video_url)
        return success_response(response)
    except Exception as e:
        return error_response('Failed to extract references', details=str(e))

@main_bp.route('/generate-article-json', methods=['POST'])
def generate_article_json():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    try:
        response_data = AudioService.generate_article_json(video_url)
        return success_response(response_data)
    except Exception as e:
        return error_response('Failed to generate article', details=str(e))
