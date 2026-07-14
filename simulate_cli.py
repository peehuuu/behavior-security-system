# simulate_cli.py  (project root)
import requests
import sys
import getpass

API_BASE = "http://127.0.0.1:5050"


def login(username, password):
    r = requests.post(f"{API_BASE}/api/auth/login", json={"username": username, "password": password})
    r.raise_for_status()
    return r.json()["token"]


def run_batch(token, n_per_type=5):
    headers = {"Authorization": f"Bearer {token}"}
    for attack_type in ["bot_typing", "high_speed_typing", "noisy_impersonator", "random_noise_injection"]:
        for i in range(n_per_type):
            r = requests.post(f"{API_BASE}/api/simulate", headers=headers, json={"attack_type": attack_type})
            result = r.json()
            status = "CAUGHT" if result["is_anomaly"] else "MISSED"
            print(f"[{attack_type:>22}] #{i+1}: {status}  risk={result['risk_score']}")


if __name__ == "__main__":
    username = "peehu_test"
    password = "securepassword123"
    token = login(username, password)
    run_batch(token, n_per_type=5)