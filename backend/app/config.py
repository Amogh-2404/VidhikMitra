import os

class Config:
    """Configuration with environment variables"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'devsecret')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    MODEL_PATH = os.environ.get('MODEL_PATH', './model')
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB uploads
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100/minute')
    ANALYTICS_ENABLED = os.environ.get('ANALYTICS_ENABLED', 'false')
