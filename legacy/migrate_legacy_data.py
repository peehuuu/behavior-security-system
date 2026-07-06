# migrate_legacy_data.py  (project root — one-time script, delete after running)
import sqlite3
from datetime import datetime
from app import create_app
from app.models.database import db, Session

OLD_DB_PATH = "behavior_old.db"   # rename your existing Phase 2 behavior.db to this first


def parse_legacy_timestamp(value):
    """Old rows were saved with SQLite's datetime('now'), which stores a
    plain string like '2026-07-06 07:12:11'. The new DateTime column needs
    an actual Python datetime object, not a string -- SQLAlchemy will
    reject the raw string with a TypeError if you skip this conversion."""
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return datetime.utcnow()


def fetch_legacy_rows():
    conn = sqlite3.connect(OLD_DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM sessions").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def migrate():
    legacy_rows = fetch_legacy_rows()
    print(f"Found {len(legacy_rows)} legacy sessions in {OLD_DB_PATH}")

    migrated, unrecoverable = 0, 0

    for row in legacy_rows:
        dwell_flight_ratio = (
            round(row["avg_dwell"] / row["avg_flight"], 4) if row["avg_flight"] else 0
        )
        if row.get("backspaces") is not None:
            unrecoverable += 1

        true_label = "legitimate" if row["label"] == "baseline" else row["label"]

        record = Session(
            user_id=None,
            timestamp=parse_legacy_timestamp(row["timestamp"]),
            wpm=row["wpm"], avg_dwell=row["avg_dwell"], avg_flight=row["avg_flight"],
            std_dwell=row["std_dwell"], std_flight=row["std_flight"],
            backspace_rate=None, longest_pause=None,
            dwell_flight_ratio=dwell_flight_ratio,
            is_anomaly=bool(row["is_anomaly"]) if row["is_anomaly"] is not None else False,
            risk_score=row["risk_score"] or 0,
            reasons=row["reasons"],
            true_label=true_label,
            source=row["label"] or "baseline",
        )
        db.session.add(record)
        migrated += 1

    db.session.commit()
    print(f"Migrated {migrated} sessions into the new database.")
    print(f"{unrecoverable} rows had an old 'backspaces' count that could not be "
          f"converted to backspace_rate -- left NULL, as explained above.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        migrate()