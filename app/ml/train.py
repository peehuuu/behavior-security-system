# app/ml/train.py
import os, json, joblib
from datetime import datetime
from sklearn.ensemble import IsolationForest
from app.ml.features import FEATURE_ORDER

MODEL_DIR = "app/ml/saved_models"

def train_model(X_normal, contamination=0.1, n_estimators=150):
    model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)
    model.fit(X_normal)
    return model

def save_versioned_model(model, metrics=None, n_samples=0):
    os.makedirs(MODEL_DIR, exist_ok=True)
    version = datetime.utcnow().strftime("v%Y%m%d_%H%M%S")
    model_path = os.path.join(MODEL_DIR, f"typing_model_{version}.pkl")
    joblib.dump(model, model_path)
    metadata = {"version": version, "trained_at": datetime.utcnow().isoformat(),
                "n_training_samples": n_samples, "feature_order": FEATURE_ORDER,
                "metrics": metrics or {}, "model_path": model_path}
    meta_path = os.path.join(MODEL_DIR, f"typing_model_{version}.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    with open(os.path.join(MODEL_DIR, "latest.json"), "w") as f:
        json.dump({"model_path": model_path, "meta_path": meta_path, "version": version}, f, indent=2)
    return version, model_path, metadata