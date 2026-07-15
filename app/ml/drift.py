# app/ml/drift.py
import statistics

def compute_drift(original_baseline, recent_sessions, feature="avg_dwell", z_threshold=1.5):
    """
    Compares the ORIGINAL registration baseline against a rolling window of
    recent *legitimate-passing* sessions, to see if the user's natural rhythm
    has gradually shifted, rather than being attacked all at once.
    """
    if len(recent_sessions) < 5:
        return {"drift_detected": False, "reason": "not enough recent sessions to assess drift"}

    recent_values = [s[feature] for s in recent_sessions]
    recent_mean = statistics.mean(recent_values)

    original_mean = original_baseline[feature]
    original_std = original_baseline.get(f"std_{feature.replace('avg_', '')}", 0.01) or 0.01

    z = abs(recent_mean - original_mean) / original_std
    drift_detected = z > z_threshold

    return {
        "drift_detected": drift_detected, "feature": feature,
        "original_mean": round(original_mean, 4), "recent_mean": round(recent_mean, 4),
        "z_score": round(z, 2),
        "recommendation": "Consider re-collecting baseline sessions" if drift_detected else "Baseline still representative",
    }