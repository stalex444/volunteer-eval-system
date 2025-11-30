import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Force use of local SQLite database to avoid external Postgres schema issues
    SQLALCHEMY_DATABASE_URI = 'sqlite:///volunteer_eval.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Application settings
    EVALUATIONS_PER_PAGE = 50
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
