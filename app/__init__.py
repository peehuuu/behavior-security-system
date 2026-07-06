# app/__init__.py
import os
from flask import Flask
from app.config import Config
from app.models.database import db

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)
    os.makedirs(app.config["MODEL_DIR"], exist_ok=True)
    db.init_app(app)
    return app