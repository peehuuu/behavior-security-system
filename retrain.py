# retrain.py  (project root)
import numpy as np
from app import create_app
from app.models.database import Session
from app.ml.features import to_vector
from app.ml.train import train_model, save_versioned_model, evaluate_model

app = create_app()

with app.app_context():
    legit_sessions = Session.query.filter(
        (Session.true_label == "legitimate") | (Session.source == "baseline")
    ).all()
    attack_sessions = Session.query.filter_by(true_label="attack").all()

    if len(legit_sessions) < 10:
        print(f"Only {len(legit_sessions)} legitimate sessions found. Collect more baseline data before retraining.")
        raise SystemExit

    feature_dicts = [s.to_dict() for s in legit_sessions]
    X_all = np.array([to_vector(f) for f in feature_dicts])

    split = int(len(X_all) * 0.8)
    X_train, X_test_legit = X_all[:split], X_all[split:]

    model = train_model(X_train)

    X_test_attack = np.array([to_vector(s.to_dict()) for s in attack_sessions]) if attack_sessions else np.empty((0, len(X_all[0])))
    if len(X_test_attack) > 0:
        X_test = np.vstack([X_test_legit, X_test_attack])
        y_true = [1] * len(X_test_legit) + [-1] * len(X_test_attack)
        metrics = evaluate_model(model, X_test, y_true)
    else:
        metrics = {"note": "no labeled attack sessions yet -- run Phase 7's simulator first for full metrics"}

    version, path, meta = save_versioned_model(model, metrics=metrics, n_samples=len(X_train))

    print(f"Trained on {len(X_train)} legitimate sessions, held out {len(X_test_legit)} + {len(attack_sessions)} attacks for evaluation.")
    print(f"Saved as version {version} -> {path}")
    print("Evaluation metrics:", metrics)