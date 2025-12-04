import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use Render Postgres (DATABASE_URL) if available, otherwise SQLite for local dev
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///volunteer_eval.db'
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Application settings
    EVALUATIONS_PER_PAGE = 50
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
