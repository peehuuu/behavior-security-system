import sqlite3

DB_PATH = "behavior.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            wpm REAL,
            avg_dwell REAL,
            avg_flight REAL,
            std_dwell REAL,
            std_flight REAL,
            backspaces INTEGER,
            label TEXT,
            is_anomaly INTEGER,
            risk_score INTEGER,
            reasons TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

import statistics

def compute_features(events, total_time, word_count, backspaces):
    dwell_times = [e["dwell_time"] for e in events]
    flight_times = [e["flight_time"] for e in events if e["flight_time"] is not None]

    avg_dwell = statistics.mean(dwell_times) if dwell_times else 0
    avg_flight = statistics.mean(flight_times) if flight_times else 0
    std_dwell = statistics.pstdev(dwell_times) if len(dwell_times) > 1 else 0
    std_flight = statistics.pstdev(flight_times) if len(flight_times) > 1 else 0
    wpm = (word_count / total_time) * 60 if total_time > 0 else 0

    return {
        "wpm": round(wpm, 2),
        "avg_dwell": round(avg_dwell, 4),
        "avg_flight": round(avg_flight, 4),
        "std_dwell": round(std_dwell, 4),
        "std_flight": round(std_flight, 4),
        "backspaces": backspaces,
    }

def save_session(features, label="baseline"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO sessions (timestamp, wpm, avg_dwell, avg_flight, std_dwell, std_flight, backspaces, label)
        VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?)
    """, (features["wpm"], features["avg_dwell"], features["avg_flight"],
          features["std_dwell"], features["std_flight"], features["backspaces"], label))
    conn.commit()
    conn.close()

import tkinter as tk
import time
import sqlite3
import statistics

PHRASE = "the quick brown fox jumps over the lazy dog"
DB_PATH = "behavior.db"
TARGET_SESSIONS = 15   # how many baseline samples we want before Phase 4 (ML) is useful

key_events = []
press_times = {}
session_start = None
last_release_time = None
backspace_count = 0
session_count = 0


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, wpm REAL, avg_dwell REAL, avg_flight REAL,
            std_dwell REAL, std_flight REAL, backspaces INTEGER, label TEXT,
            is_anomaly INTEGER, risk_score INTEGER, reasons TEXT, source TEXT
        )
    """)
    conn.commit()
    conn.close()


def compute_features(events, total_time, word_count, backspaces):
    dwell_times = [e["dwell_time"] for e in events]
    flight_times = [e["flight_time"] for e in events if e["flight_time"] is not None]
    avg_dwell = statistics.mean(dwell_times) if dwell_times else 0
    avg_flight = statistics.mean(flight_times) if flight_times else 0
    std_dwell = statistics.pstdev(dwell_times) if len(dwell_times) > 1 else 0
    std_flight = statistics.pstdev(flight_times) if len(flight_times) > 1 else 0
    wpm = (word_count / total_time) * 60 if total_time > 0 else 0
    return {
        "wpm": round(wpm, 2), "avg_dwell": round(avg_dwell, 4), "avg_flight": round(avg_flight, 4),
        "std_dwell": round(std_dwell, 4), "std_flight": round(std_flight, 4), "backspaces": backspaces,
    }


def save_session(features, label="baseline"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO sessions (timestamp, wpm, avg_dwell, avg_flight, std_dwell, std_flight, backspaces, label)
        VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?)
    """, (features["wpm"], features["avg_dwell"], features["avg_flight"],
          features["std_dwell"], features["std_flight"], features["backspaces"], label))
    conn.commit()
    conn.close()


def on_key_press(event):
    global session_start
    char = event.keysym
    if session_start is None:
        session_start = time.time()
    if char not in press_times:
        press_times[char] = time.time()


def on_key_release(event):
    global last_release_time, backspace_count
    char = event.keysym
    if char == "BackSpace":
        backspace_count += 1
    press_time = press_times.pop(char, None)
    if press_time is None:
        return
    release_time = time.time()
    dwell_time = release_time - press_time
    flight_time = (press_time - last_release_time) if last_release_time is not None else None
    key_events.append({"dwell_time": dwell_time, "flight_time": flight_time})
    last_release_time = release_time


def next_session():
    global session_start, last_release_time, backspace_count, session_count
    if len(key_events) < 5:
        status_label.config(text="Type a bit more before finishing this session.")
        return

    total_time = time.time() - session_start
    word_count = len(PHRASE.split())
    features = compute_features(key_events, total_time, word_count, backspace_count)
    save_session(features, label="baseline")

    session_count += 1
    key_events.clear()
    press_times.clear()
    session_start = None
    last_release_time = None
    backspace_count = 0
    entry.delete(0, tk.END)

    if session_count >= TARGET_SESSIONS:
        status_label.config(text=f"Done! {session_count}/{TARGET_SESSIONS} baseline sessions saved.\nClose this window and move to Phase 4.")
        finish_btn.config(state="disabled")
    else:
        status_label.config(text=f"Saved session {session_count}/{TARGET_SESSIONS}. Type the phrase again.")


init_db()

root = tk.Tk()
root.title("Typing Behavior Tracker - Phase 2 (with storage)")
root.geometry("520x260")

label = tk.Label(root, text=f'Type this phrase:\n\n"{PHRASE}"', wraplength=480, justify="left")
label.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=8)
entry.bind("<KeyPress>", on_key_press)
entry.bind("<KeyRelease>", on_key_release)
entry.focus()

finish_btn = tk.Button(root, text="Save Session & Continue", command=next_session)
finish_btn.pack(pady=8)

status_label = tk.Label(root, text=f"Session 0/{TARGET_SESSIONS}. Type the phrase and click Save.", fg="blue")
status_label.pack(pady=8)

root.mainloop()