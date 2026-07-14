# app/services/model_registry.py
from ctypes import pointer
import os
import json
import joblib

MODEL_DIR = "app/ml/saved_models"
_cached_model = None
_cached_version = None


def get_active_model():
    global _cached_model, _cached_version
    latest_path = os.path.join(MODEL_DIR, "latest.json")
    if not os.path.exists(latest_path):
        return None

    with open(latest_path) as f:
        pointer = json.load(f)

    if pointer["version"] != _cached_version:
      # This forces any Windows backslashes to become Linux forward slashes
        safe_path = pointer["model_path"].replace('\\', '/')
        _cached_model = joblib.load(safe_path)
        _cached_version = pointer["version"]

    return _cached_model


def get_active_version():
    return _cached_version