from flask import jsonify

def error_response(message, status_code=400, details=None):
    response = {'error': message, 'status': 'failure'}
    if details:
        response['details'] = details
    return jsonify(response), status_code

def success_response(data):
    return jsonify({'response': data, 'status': 'success'})

def stream_generator(audio_service_method, video_url):
    try:
        for chunk in audio_service_method(video_url):
            yield chunk
    except Exception as e:
        yield error_response('An error occurred during processing', details=str(e))
