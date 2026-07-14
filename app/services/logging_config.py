# app/services/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    os.makedirs("logs", exist_ok=True)
    
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    # General Application Log
    app_handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
    app_handler.setFormatter(formatter)
    app.logger.addHandler(app_handler)
    app.logger.setLevel(logging.INFO)
    
    # Isolated Security Log
    security_logger = logging.getLogger("security")
    security_handler = RotatingFileHandler("logs/security.log", maxBytes=1_000_000, backupCount=3)
    security_handler.setFormatter(formatter)
    
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.WARNING)
    security_logger.propagate = False  # Prevents security warnings from leaking into app.log
    
    return security_logger