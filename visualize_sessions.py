# visualize_sessions.py  (project root)
import matplotlib
matplotlib.use("Agg")   # saves to file instead of trying to open a window
import matplotlib.pyplot as plt
from app import create_app
from app.models.database import Session

app = create_app()
with app.app_context():
    sessions = Session.query.filter(Session.true_label.isnot(None)).all()

legit = [s for s in sessions if s.true_label == "legitimate"]
attack = [s for s in sessions if s.true_label == "attack"]

plt.figure(figsize=(8, 6))
plt.scatter([s.wpm for s in legit], [s.avg_dwell for s in legit], c="#39ff8f", label="legitimate", alpha=0.7)
plt.scatter([s.wpm for s in attack], [s.avg_dwell for s in attack], c="#ff3b5c", label="attack", alpha=0.7)
plt.xlabel("Words per minute (WPM)")
plt.ylabel("Average dwell time (s)")
plt.title("Legitimate vs. Attack Sessions — Feature Space")
plt.legend()
plt.savefig("session_scatter.png", dpi=150)
print("Saved session_scatter.png")