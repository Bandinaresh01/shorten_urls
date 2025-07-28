from flask import Flask, render_template
from routes.shortener import shortener_bp
from middleware.logger import log_request
from database import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.getcwd(), 'instance', 'shortener.db')
    app.config['LOG_FOLDER'] = os.path.join(os.getcwd(), 'logs')

    # Ensure log folder exists
    os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
    
    # Ensure instance folder exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    # Initialize DB
    init_db()

    # Register routes
    app.register_blueprint(shortener_bp)

    # Logging middleware
    @app.before_request
    def before_request():
        log_request()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
