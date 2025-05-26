from flask import Flask
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints/routes
    from app.bot.message_handler import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app