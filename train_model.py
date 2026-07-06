import sqlite3
import statistics
import json
import os
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

DB_PATH = "behavior.db"
MODEL_PATH = "models/typing_model.pkl"
BASELINE_PATH = "baseline.json"


def load_baseline_rows():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT wpm, avg_dwell, avg_flight, std_dwell, std_flight FROM sessions WHERE label='baseline'"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def train_and_save(X):
    os.makedirs("models", exist_ok=True)
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained on {len(X)} sessions and saved to {MODEL_PATH}")
    return model


def save_baseline_json(rows):
    baseline = {
        "avg_wpm": round(statistics.mean([r["wpm"] for r in rows]), 2),
        "avg_dwell": round(statistics.mean([r["avg_dwell"] for r in rows]), 4),
        "std_dwell": round(statistics.pstdev([r["avg_dwell"] for r in rows]) or 0.01, 4),
        "avg_flight": round(statistics.mean([r["avg_flight"] for r in rows]), 4),
        "std_flight": round(statistics.pstdev([r["avg_flight"] for r in rows]) or 0.01, 4),
        "n_sessions": len(rows)
    }
    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, indent=2)
    print("Baseline profile:", baseline)
    return baseline


def main():
    rows = load_baseline_rows()
    if len(rows) < 5:
        print(f"Not enough baseline sessions ({len(rows)}). Run typing_tracker_db.py (Phase 2) a few more times.")
        return

    X = np.array([[r["avg_dwell"], r["avg_flight"], r["std_dwell"], r["std_flight"], r["wpm"]] for r in rows])
    train_and_save(X)
    save_baseline_json(rows)


if __name__ == "__main__":
    main()