# app/routes/session.py
from flask import Blueprint, jsonify, request

# Models & Services
from app.models.database import Session, User
from app.services.alerting import send_alert
from app.services.baseline_service import compute_user_baseline
from app.ml.drift import compute_drift

# Config & Auth
from app.config import DEMO_BASELINE 
from app.services.auth_service import token_required

# Define the blueprint
session_bp = Blueprint('session_bp', __name__)

# ==========================================
# ROUTE 1: Continuous Authentication Check
# ==========================================
@session_bp.route("/api/drift", methods=["GET"])
#@token_required
def drift_check():
    user_id = request.user["user_id"]
    
    baseline, error = compute_user_baseline(user_id)
    if error:
        baseline = DEMO_BASELINE
        
    recent = Session.query.filter_by(user_id=user_id, is_anomaly=False)\
                          .order_by(Session.timestamp.desc()).limit(10).all()
    
    if not recent:
        return jsonify({
            "status": "no_data", 
            "message": "Insufficient session history to compute drift."
        })
    
    result = compute_drift(baseline, [s.to_dict() for s in recent])
    return jsonify(result)

# ==========================================
# ROUTE 2: THE DATABASE-FREE BACKDOOR TEST
# ==========================================
@session_bp.route("/api/hack", methods=["POST"])
def backdoor_test():
    from app.services.alerting import send_alert
    
    # 1. Create a fake user object so we completely ignore the broken database
    class FakeUser:
        username = "peehu_test"
    
    mock_user = FakeUser()
    
    # 2. Simulate the exact output of a bot attack (Risk Score 100)
    fake_attack_data = {
        "risk_score": 100,
        "reasons": ["Typing speed deviates heavily from baseline", "Zero variance in keypress duration"]
    }
    
    # 3. Fire your alerting system directly
    send_alert(fake_attack_data, mock_user)
    
    return {"status": "alert_triggered_successfully", "risk": 100}

# (Note: We will restore your full /api/session/new route after this test!)