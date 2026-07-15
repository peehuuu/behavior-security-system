import os
from flask import Flask
from flask_talisman import Talisman
from app.config import Config
from app.models.database import db
from app.extensions import limiter, migrate  # <--- Added migrate
from app.services.logging_config import setup_logging

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
        # 1. Import all blueprints here to avoid circular dependencies
        from app.routes.health import health_bp
        from app.routes.auth import auth_bp
        from app.routes.simulate import simulate_bp
        from app.routes.admin import admin_bp
        from app.routes.session import session_bp  # <--- ADDED: Import session blueprint
        
        # 2. Register all blueprints
        app.register_blueprint(health_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(simulate_bp)
        app.register_blueprint(admin_bp)        
        app.register_blueprint(session_bp)         # <--- ADDED: Register session blueprint
        from flask import render_template
        @app.route("/")
        def serve_dashboard():
            return render_template("index.html")
    return app