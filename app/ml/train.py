import os
import joblib
import json
from app.ml import MODEL_DIR

def save_versioned_model(user_id, model, version):
    # Create the user-specific path: saved_models/user_<id>/
    user_dir = os.path.join(MODEL_DIR, f"user_{user_id}")
    os.makedirs(user_dir, exist_ok=True) # Ensure directory exists!
    
    # Save the model file
    model_path = os.path.join(user_dir, f"typing_model_{version}.pkl")
    joblib.dump(model, model_path)
    
    # Update the latest.json pointer for this user
    latest_path = os.path.join(user_dir, "latest.json")
    with open(latest_path, "w") as f:
        json.dump({"latest_version": version, "path": model_path}, f)
        
    return model_path