# app/ml/train.py
import os
import json
import joblib
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

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

    metadata = {
        "version": version, "trained_at": datetime.utcnow().isoformat(),
        "n_training_samples": n_samples, "feature_order": FEATURE_ORDER,
        "metrics": metrics or {}, "model_path": model_path,
    }
    meta_path = os.path.join(MODEL_DIR, f"typing_model_{version}.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    latest_path = os.path.join(MODEL_DIR, "latest.json")
    with open(latest_path, "w") as f:
        json.dump({"model_path": model_path, "meta_path": meta_path, "version": version}, f, indent=2)

    return version, model_path, metadata


def evaluate_model(model, X_test, y_true):
    """y_true: 1 for legitimate, -1 for attack (matches IsolationForest's own convention)."""
    y_pred = model.predict(X_test)
    scores = model.decision_function(X_test)

    metrics = {
        "precision": round(precision_score(y_true, y_pred, pos_label=-1, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, pos_label=-1, zero_division=0), 4),
        "f1_score": round(f1_score(y_true, y_pred, pos_label=-1, zero_division=0), 4),
        "roc_auc": round(roc_auc_score([1 if y == -1 else 0 for y in y_true], -scores), 4),
    }
    cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
    metrics["confusion_matrix"] = {
        "true_legitimate_pred_legitimate": int(cm[0][0]), "true_legitimate_pred_attack": int(cm[0][1]),
        "true_attack_pred_legitimate": int(cm[1][0]), "true_attack_pred_attack": int(cm[1][1]),
    }
    return metrics