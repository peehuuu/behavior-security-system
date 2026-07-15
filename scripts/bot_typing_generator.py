# scripts/bot_typing_generator.py
import argparse
import requests
import json

def run_bot_attack(username):
    print(f"[*] Initiating robotic typing sequence for user: '{username}'")
    
    # The signature of a bot: 0 variance, perfectly identical keystroke durations.
    # This mathematical impossibility guarantees a risk_score of 100.
    bot_payload = {
        "user_id": username,
        "typing_data": [
            {"key": "p", "hold_time": 45, "flight_time": 60},
            {"key": "a", "hold_time": 45, "flight_time": 60},
            {"key": "s", "hold_time": 45, "flight_time": 60},
            {"key": "s", "hold_time": 45, "flight_time": 60},
            {"key": "w", "hold_time": 45, "flight_time": 60},
            {"key": "o", "hold_time": 45, "flight_time": 60},
            {"key": "r", "hold_time": 45, "flight_time": 60},
            {"key": "d", "hold_time": 45, "flight_time": 60}
        ]
    }

    # Replace '8080' with your actual Flask port if it is running on 5000
    url = "http://127.0.0.1:5050/api/hack"
    
    # Note: If your @token_required decorator strictly validates tokens, 
    # replace this mock token with a valid regular user token.
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InBlZWh1X3Rlc3QiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3ODQwNTc5ODgsImlhdCI6MTc4NDAyOTE4OH0.7XDoZzBKouRLVeX9P_MJlwlLbqWazrC2voQhF3KWaMc",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=bot_payload, headers=headers)
        print(f"[+] Payload deployed to {url}")
        print(f"[>] Server Response [{response.status_code}]: {response.text}")
    except requests.exceptions.ConnectionError:
        print("[-] Connection failed. Is your Flask server actively running?")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a bot typing attack.")
    parser.add_argument("--user", required=True, help="Target username for the attack")
    args = parser.parse_args()
    
    run_bot_attack(args.user)