# verify_retrofit.py  (project root)
import numpy as np
from app import create_app
from app.models.database import Session
from app.ml.features import to_vector
from app.ml.train import train_model, save_versioned_model
from app.services.detection_service import run_detection

app = create_app()
with app.app_context():
    sessions = Session.query.filter_by(true_label="legitimate").all()
    X = np.array([to_vector(s.to_dict()) for s in sessions])
    model = train_model(X)
    save_versioned_model(model, n_samples=len(X))

    baseline = {"avg_wpm": 40, "avg_dwell": 0.09, "std_dwell": 0.015, "std_flight": 0.04}
    normal_sample = {"wpm": 41, "avg_dwell": 0.09, "avg_flight": 0.07, "std_dwell": 0.01,
                      "std_flight": 0.04, "backspace_rate": 0, "longest_pause": 0.1, "dwell_flight_ratio": 1.28}
    bot_sample = {"wpm": 95, "avg_dwell": 0.03, "avg_flight": 0.01, "std_dwell": 0.001,
                  "std_flight": 0.002, "backspace_rate": 0, "longest_pause": 0.02, "dwell_flight_ratio": 3.0}

    print("Normal ->", run_detection(normal_sample, baseline, model))
    print("Bot    ->", run_detection(bot_sample, baseline, model))