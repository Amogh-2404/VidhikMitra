"""Backend package initialization."""
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config
from .routes.auth import auth_bp
from .routes.chat import chat_bp
from .routes.upload import upload_bp
import logging


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config())

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    Limiter(
        get_remote_address,
        app=app,
        default_limits=[Config.RATE_LIMIT],
    )
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    return app
