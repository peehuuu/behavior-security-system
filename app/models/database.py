# app/models/database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sessions = db.relationship("Session", backref="user", lazy=True)


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    wpm = db.Column(db.Float)
    avg_dwell = db.Column(db.Float)
    avg_flight = db.Column(db.Float)
    std_dwell = db.Column(db.Float)
    std_flight = db.Column(db.Float)
    backspace_rate = db.Column(db.Float)
    longest_pause = db.Column(db.Float)
    dwell_flight_ratio = db.Column(db.Float)

    is_anomaly = db.Column(db.Boolean, default=False, index=True)
    risk_score = db.Column(db.Integer, default=0)
    reasons = db.Column(db.Text)
    rule_anomaly = db.Column(db.Boolean, default=False)
    ml_anomaly = db.Column(db.Boolean, default=False)

    true_label = db.Column(db.String(20), nullable=True, index=True)
    source = db.Column(db.String(20), default="live")
    model_version = db.Column(db.String(40), nullable=True)

    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "wpm": self.wpm, "avg_dwell": self.avg_dwell, "avg_flight": self.avg_flight,
            "std_dwell": self.std_dwell, "std_flight": self.std_flight,
            "backspace_rate": self.backspace_rate, "longest_pause": self.longest_pause,
            "dwell_flight_ratio": self.dwell_flight_ratio,
            "is_anomaly": self.is_anomaly, "risk_score": self.risk_score,
            "reasons": self.reasons, "rule_anomaly": self.rule_anomaly, "ml_anomaly": self.ml_anomaly,
            "true_label": self.true_label, "source": self.source, "model_version": self.model_version,
        }