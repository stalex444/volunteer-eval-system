import os
from datetime import timedelta

# Get the absolute path to the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database config - use absolute path
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "database", "volunteers.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Application settings
    EVALUATIONS_PER_PAGE = 50
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
