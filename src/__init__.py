from flask import Flask
from flask import jsonify

# Import from constants http_status_codes.py
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

# Import apps
from src.app import __MRS

import os

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"))
    else:
        app.config.from_mapping(test_config)
        
        
    # Register all Blueprints
    app.register_blueprint(__MRS)
        
        
    # Error handling
    app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR
    
    return app