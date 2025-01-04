from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config') 
    CORS(app) 

    with app.app_context():
        from .main import routes
        app.register_blueprint(routes.main_bp)

    return app