import os
from flask import Flask
from flask_talisman import Talisman
from app.config import Config
from app.models.database import db
from app.extensions import limiter, migrate  # <--- Added migrate
from app.services.logging_config import setup_logging
from app.routes.simulate import simulate_bp

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)
    
    limiter.init_app(app)
    db.init_app(app)             
    migrate.init_app(app, db)    # <--- Initialize migrate here
    
    app.config["RATELIMIT_DEFAULT"] = app.config["RATE_LIMIT_DEFAULT"]

    Talisman(
        app,
        force_https=False,
        content_security_policy={
            "default-src": "'self'",
            "script-src": ["'self'", "https://cdn.tailwindcss.com", "https://cdn.jsdelivr.net"],
            "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            "font-src": ["https://fonts.gstatic.com"],
        },
    )
    
    setup_logging(app)
    os.makedirs(app.config["MODEL_DIR"], exist_ok=True)
    
    with app.app_context():
        from app.routes.health import health_bp
        app.register_blueprint(health_bp)
        
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
        
        # db.create_all() has been REMOVED.
        
        app.register_blueprint(simulate_bp)
        
    return app