# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app.services.auth_service import create_user, verify_user, generate_token, token_required
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if len(username) < 3 or len(password) < 6:
        return jsonify({"error": "username must be 3+ chars, password 6+ chars"}), 400
    user, error = create_user(username, password)
    if error:
        return jsonify({"error": error}), 409
    return jsonify({"message": "user created", "username": user.username}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json() or {}
    user = verify_user(data.get("username", ""), data.get("password", ""))
    if not user:
        return jsonify({"error": "invalid username or password"}), 401
    token = generate_token(user)
    return jsonify({"token": token, "username": user.username, "role": user.role})


@auth_bp.route("/api/auth/me", methods=["GET"])
@token_required
def me():
    return jsonify(request.user)