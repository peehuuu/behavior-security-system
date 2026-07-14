# app/routes/simulate.py
from flask import Blueprint, request, jsonify
from app.services.auth_service import token_required
from app.services.detection_service import run_detection
from app.models.database import db, Session
from app.ml.attack_generator import ATTACK_GENERATORS
import random
import logging
from app.services.model_registry import get_active_model

simulate_bp = Blueprint("simulate", __name__)
security_logger = logging.getLogger("security")

DEMO_BASELINE = {"avg_wpm": 40, "avg_dwell": 0.09, "std_dwell": 0.015, "std_flight": 0.04}


@simulate_bp.route("/api/simulate", methods=["POST"])
@token_required
def simulate_attack():
    data = request.get_json() or {}
    attack_type = data.get("attack_type", random.choice(list(ATTACK_GENERATORS.keys())))
    if attack_type not in ATTACK_GENERATORS:
        return jsonify({"error": "unknown attack_type", "options": list(ATTACK_GENERATORS.keys())}), 400

    profile = ATTACK_GENERATORS[attack_type]()
    profile["dwell_flight_ratio"] = profile["avg_dwell"] / profile["avg_flight"] if profile["avg_flight"] else 0

    from app.services.model_registry import get_active_model   # see Phase 8
    model = get_active_model()
    is_anomaly, rule_anomaly, ml_anomaly, risk_score, reasons = run_detection(profile, DEMO_BASELINE, model)

    record = Session(
        user_id=request.user["user_id"], **{k: v for k, v in profile.items() if k != "dwell_flight_ratio"},
        dwell_flight_ratio=profile["dwell_flight_ratio"],
        is_anomaly=is_anomaly, risk_score=risk_score, reasons="; ".join(reasons),
        rule_anomaly=rule_anomaly, ml_anomaly=ml_anomaly,
        true_label="attack", source="simulated",
    )
    db.session.add(record)
    db.session.commit()

    security_logger.warning(f"SIMULATED ATTACK type={attack_type} caught={is_anomaly} risk={risk_score}")

    return jsonify({
        "attack_type": attack_type, "profile": profile,
        "is_anomaly": is_anomaly, "risk_score": risk_score, "reasons": reasons,
    })