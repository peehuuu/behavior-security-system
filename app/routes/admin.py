# app/routes/admin.py
from flask import Blueprint, jsonify
from app.services.auth_service import token_required, admin_required
from app.models.database import Session, User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/api/admin/sessions", methods=["GET"])
@token_required
@admin_required
def all_sessions():
    sessions = Session.query.order_by(Session.timestamp.desc()).limit(200).all()
    return jsonify([s.to_dict() for s in sessions])

@admin_bp.route("/api/admin/alerts", methods=["GET"])
@token_required
@admin_required
def alerts():
    flagged = Session.query.filter_by(is_anomaly=True).order_by(Session.timestamp.desc()).limit(100).all()
    return jsonify([s.to_dict() for s in flagged])

@admin_bp.route("/api/admin/users", methods=["GET"])
@token_required
@admin_required
def all_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "role": u.role} for u in users])