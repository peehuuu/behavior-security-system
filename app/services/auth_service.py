# app/services/auth_service.py
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.database import db, User


def create_user(username, password, role="user"):
    if User.query.filter_by(username=username).first():
        return None, "username already exists"
    user = User(username=username, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    return user, None


def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def generate_token(user):
    payload = {
        "user_id": user.id, "username": user.username, "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]), None
    except jwt.ExpiredSignatureError:
        return None, "token expired"
    except jwt.InvalidTokenError:
        return None, "invalid token"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing or malformed Authorization header"}), 401
        token = auth_header.split(" ", 1)[1]
        payload, error = decode_token(token)
        if error:
            return jsonify({"error": error}), 401
        request.user = payload
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if getattr(request, "user", {}).get("role") != "admin":
            return jsonify({"error": "admin access required"}), 403
        return f(*args, **kwargs)
    return decorated