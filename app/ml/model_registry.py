import os
import json
from app.ml import MODEL_DIR

def get_active_model(user_id):
    """
    Returns the path to the latest model for a specific user.
    If no user-specific model exists, returns None (or path to a default/global model).
    """
    user_dir = os.path.join(MODEL_DIR, f"user_{user_id}")
    latest_path = os.path.join(user_dir, "latest.json")
    
    # Check if the user directory and the latest.json file exist
    if not os.path.exists(latest_path):
        print(f"No model found for user_{user_id} at {latest_path}")
        return None
        
    try:
        with open(latest_path, "r") as f:
            meta = json.load(f)
        return meta.get("path")
    except Exception as e:
        print(f"Error reading model registry for user_{user_id}: {e}")
        return None