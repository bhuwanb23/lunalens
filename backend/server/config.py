import os
import secrets
from dotenv import load_dotenv

load_dotenv()


def _get_required_secret(env_var: str) -> str:
    """Get a required secret from environment. Generate a random one for development only."""
    value = os.environ.get(env_var)
    if value:
        return value
    if os.environ.get('FLASK_CONFIG') == 'production':
        raise RuntimeError(
            f"Environment variable {env_var} is required in production. "
            f"Set it before starting the server."
        )
    # Auto-generate for development — prints a warning so devs notice
    value = secrets.token_hex(32)
    print(f"⚠️  WARNING: {env_var} not set. Using auto-generated key for development only.")
    print(f"   Set {env_var} in your .env file or environment for production use.")
    return value


class Config:
    """Base configuration class"""
    SECRET_KEY = _get_required_secret('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Database configuration (SQLite for Windows compatibility)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///lunalens.db'  # SQLite database file
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

    # JWT configuration
    JWT_SECRET_KEY = _get_required_secret('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24 hours
    
    # Boulder detection configuration
    BOULDER_DETECTION_MODELS_PATH = os.environ.get('BOULDER_DETECTION_MODELS_PATH', '../boulder_detection/models')
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/lunalens.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///lunalens_dev.db'  # SQLite development database
    )

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///lunalens_prod.db')
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'sqlite:///lunalens_test.db'  # SQLite test database
    )

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 