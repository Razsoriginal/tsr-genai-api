from flask import Blueprint, request, stream_with_context
from app.core.audio_service import AudioService
from app.utils.responses import error_response, stream_generator, success_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return success_response('Welcome to the AI Blog Article Generator API!')

@main_bp.route('/transcribe-ai', methods=['POST'])
def transcribe_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    return stream_with_context(stream_generator(AudioService.transcribe, video_url))

@main_bp.route('/summarize-ai', methods=['POST'])
def summarize_ai():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    return stream_with_context(stream_generator(AudioService.summarize, video_url))

@main_bp.route('/extract-references', methods=['POST'])
def extract_references():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    return stream_with_context(stream_generator(AudioService.extract_references, video_url))

@main_bp.route('/generate-article-json', methods=['POST'])
def generate_article_json():
    video_url = request.json.get('video_url')
    if not video_url:
        return error_response('Video URL is required')

    return stream_with_context(stream_generator(AudioService.generate_article_json, video_url))