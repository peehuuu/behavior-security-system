# app/services/baseline_service.py
import statistics
from app.models.database import Session


def compute_user_baseline(user_id):
    """Per-user baseline, computed ONLY from that user's own legitimate/baseline sessions."""
    sessions = Session.query.filter(
        Session.user_id == user_id,
        (Session.true_label == "legitimate") | (Session.source == "baseline")
    ).all()

    if len(sessions) < 5:
        return None, f"only {len(sessions)} baseline sessions for user {user_id} (need 5+)"

    wpms = [s.wpm for s in sessions]
    dwells = [s.avg_dwell for s in sessions]
    flights = [s.avg_flight for s in sessions]

    baseline = {
        "avg_wpm": round(statistics.mean(wpms), 2),
        "avg_dwell": round(statistics.mean(dwells), 4),
        "std_dwell": round(statistics.pstdev(dwells) or 0.01, 4),
        "avg_flight": round(statistics.mean(flights), 4),
        "std_flight": round(statistics.pstdev(flights) or 0.01, 4),
        "n_sessions": len(sessions),
    }
    return baseline, None