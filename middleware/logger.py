import logging
from logging.handlers import RotatingFileHandler
import os
from flask import request

def setup_logger(app):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = RotatingFileHandler('logs/access.log', maxBytes=100000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    
    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.path} - Args: {str(dict(request.args))}")

def log_request():
    """Standalone logging function for use in app.py"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Request logged")

