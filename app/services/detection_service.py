# app/services/detection_service.py
import numpy as np
from app.ml.features import to_vector


def check_rules(current, baseline, wpm_threshold=0.4, dwell_std_multiplier=2.0):
    reasons = []
    risk_score = 0

    wpm_diff_ratio = abs(current["wpm"] - baseline["avg_wpm"]) / baseline["avg_wpm"] if baseline["avg_wpm"] else 0
    if wpm_diff_ratio > wpm_threshold:
        reasons.append(f"Typing speed deviates {round(wpm_diff_ratio*100,1)}% from baseline")
        risk_score += 35

    dwell_low = baseline["avg_dwell"] - dwell_std_multiplier * baseline["std_dwell"]
    dwell_high = baseline["avg_dwell"] + dwell_std_multiplier * baseline["std_dwell"]
    if not (dwell_low <= current["avg_dwell"] <= dwell_high):
        reasons.append("Key hold (dwell) time outside normal range")
        risk_score += 30

    if current["std_flight"] < baseline["std_flight"] * 0.2 and baseline["std_flight"] > 0:
        reasons.append("Typing rhythm is unusually uniform (possible automated input)")
        risk_score += 35

    return risk_score >= 40, reasons, min(risk_score, 100)


def run_detection(features, baseline, model):
    rule_anomaly, reasons, risk_score = check_rules(features, baseline)

    ml_anomaly = False
    if model is not None:
        vec = np.array([to_vector(features)])
        pred = model.predict(vec)[0]
        ml_anomaly = bool(pred == -1)

       
        if risk_score < 40:
            ml_anomaly = False

        if ml_anomaly:
            reasons.append("ML model (Isolation Forest) flagged this session as an outlier")

    final_anomaly = bool(rule_anomaly or ml_anomaly)

    return final_anomaly, rule_anomaly, ml_anomaly, risk_score, reasons