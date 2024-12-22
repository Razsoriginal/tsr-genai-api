# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    with app.app_context():
        # Import routes
        from .main import routes

        # Register Blueprints
        app.register_blueprint(routes.main_bp)

    return app