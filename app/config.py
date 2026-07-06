

# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-too")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///behavior.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_DIR = os.environ.get("MODEL_DIR", "app/ml/saved_models")
    RATE_LIMIT_DEFAULT = os.environ.get("RATE_LIMIT_DEFAULT", "100 per hour")
    DEBUG = os.environ.get("FLASK_ENV", "production") == "development"