import sqlite3
import statistics

DB_PATH = "behavior.db"

def get_baseline_profile():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT wpm, avg_dwell, avg_flight, std_dwell, std_flight FROM sessions WHERE label='baseline'").fetchall()
    conn.close()

    wpms = [r["wpm"] for r in rows]
    dwells = [r["avg_dwell"] for r in rows]
    flights = [r["avg_flight"] for r in rows]

    return {
        "avg_wpm": round(statistics.mean(wpms), 2),
        "avg_dwell": round(statistics.mean(dwells), 4),
        "std_dwell": round(statistics.pstdev(dwells), 4),
        "avg_flight": round(statistics.mean(flights), 4),
        "std_flight": round(statistics.pstdev(flights), 4),
    }



def check_rules(current, baseline, wpm_threshold=0.4, dwell_std_multiplier=2.0):
    """
    current: dict with wpm, avg_dwell, std_flight for the session being checked
    baseline: dict from get_baseline_profile()
    Returns: (is_anomaly: bool, reasons: list[str], risk_score: int 0-100)
    """
    reasons = []
    risk_score = 0

    # Rule 1: typing speed deviates too much from baseline average WPM
    wpm_diff_ratio = abs(current["wpm"] - baseline["avg_wpm"]) / baseline["avg_wpm"] if baseline["avg_wpm"] else 0
    if wpm_diff_ratio > wpm_threshold:
        reasons.append(f"Typing speed deviates {round(wpm_diff_ratio*100,1)}% from baseline")
        risk_score += 35

    # Rule 2: average dwell time is outside baseline mean +/- N*std
    dwell_low = baseline["avg_dwell"] - dwell_std_multiplier * baseline["std_dwell"]
    dwell_high = baseline["avg_dwell"] + dwell_std_multiplier * baseline["std_dwell"]
    if not (dwell_low <= current["avg_dwell"] <= dwell_high):
        reasons.append("Key hold (dwell) time outside normal range")
        risk_score += 30

    # Rule 3: flight time is abnormally uniform (near-zero variation => possible bot/script)
    if current["std_flight"] < baseline["std_flight"] * 0.2 and baseline["std_flight"] > 0:
        reasons.append("Typing rhythm is unusually uniform (possible automated input)")
        risk_score += 35

    is_anomaly = risk_score >= 40
    return is_anomaly, reasons, min(risk_score, 100)

if __name__ == "__main__":
    baseline = get_baseline_profile()
    print("Baseline profile:", baseline)

    normal_sample = {"wpm": baseline["avg_wpm"] + 1, "avg_dwell": baseline["avg_dwell"], "std_flight": baseline["std_flight"]}
    bot_sample = {"wpm": 95, "avg_dwell": 0.03, "std_flight": 0.002}

    print("\nNormal sample check:", check_rules(normal_sample, baseline))
    print("Bot-like sample check:", check_rules(bot_sample, baseline))