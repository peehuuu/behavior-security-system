import tkinter as tk
import time

PHRASE = "the quick brown fox jumps over the lazy dog"

key_events = []          # every completed press/release pair we capture
press_times = {}         # currently-held keys -> press timestamp
session_start = None
last_release_time = None


def on_key_press(event):
    global session_start
    char = event.char
    if session_start is None:
        session_start = time.time()
    if char not in press_times:
        press_times[char] = time.time()


def on_key_release(event):
    global last_release_time
    char = event.char
    press_time = press_times.pop(char, None)
    if press_time is None:
        return
    release_time = time.time()
    dwell_time = release_time - press_time

    flight_time = None
    if last_release_time is not None:
        flight_time = press_time - last_release_time

    key_events.append({
        "key": char,
        "dwell_time": round(dwell_time, 4),
        "flight_time": round(flight_time, 4) if flight_time is not None else None
    })
    last_release_time = release_time

def finish_session():
    if not key_events:
        print("No keys captured yet.")
        return
    total_time = time.time() - session_start
    print("\n--- SESSION SUMMARY ---")
    print(f"Keys captured : {len(key_events)}")
    print(f"Total time    : {round(total_time, 2)} sec")
    for e in key_events[:5]:
        print(e)
    print("... (showing first 5 keys only)")

root = tk.Tk()
root.title("Typing Behavior Tracker - Phase 1")
root.geometry("500x200")

label = tk.Label(root, text=f'Type this phrase:\n\n"{PHRASE}"', wraplength=460, justify="left")
label.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=10)
entry.bind("<KeyPress>", on_key_press)
entry.bind("<KeyRelease>", on_key_release)
entry.focus()

finish_btn = tk.Button(root, text="Finish & Show Summary", command=finish_session)
finish_btn.pack(pady=10)

root.mainloop()