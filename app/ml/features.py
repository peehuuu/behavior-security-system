# app/ml/features.py
import statistics


def compute_features_v2(events, total_time, word_count, backspaces):
    """
    events: list of {"dwell_time": float, "flight_time": float|None}
    """
    dwell_times = [e["dwell_time"] for e in events]
    flight_times = [e["flight_time"] for e in events if e["flight_time"] is not None]

    avg_dwell = statistics.mean(dwell_times) if dwell_times else 0
    avg_flight = statistics.mean(flight_times) if flight_times else 0
    std_dwell = statistics.pstdev(dwell_times) if len(dwell_times) > 1 else 0
    std_flight = statistics.pstdev(flight_times) if len(flight_times) > 1 else 0
    wpm = (word_count / total_time) * 60 if total_time > 0 else 0

    backspace_rate = backspaces / len(dwell_times) if dwell_times else 0
    longest_pause = max(flight_times) if flight_times else 0
    dwell_flight_ratio = (avg_dwell / avg_flight) if avg_flight > 0 else 0

    return {
        "wpm": round(wpm, 2), "avg_dwell": round(avg_dwell, 4), "avg_flight": round(avg_flight, 4),
        "std_dwell": round(std_dwell, 4), "std_flight": round(std_flight, 4),
        "backspace_rate": round(backspace_rate, 4), "longest_pause": round(longest_pause, 4),
        "dwell_flight_ratio": round(dwell_flight_ratio, 4),
    }


FEATURE_ORDER = ["avg_dwell", "avg_flight", "std_dwell", "std_flight", "wpm",
                  "backspace_rate", "longest_pause", "dwell_flight_ratio"]


def to_vector(feature_dict):
    """Fixed-order list the model expects -- ALWAYS build model inputs through this function."""
    return [feature_dict.get(k, 0) for k in FEATURE_ORDER]