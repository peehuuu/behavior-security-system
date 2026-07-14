from flask import Flask, request, jsonify, render_template
import random

# 1. Initialize the app ONE time at the top
app = Flask(__name__)

# Simulating a basic in-memory counter for failed attempts
failed_attempts = 0

# 2. Register all routes BEFORE starting the server
@app.route("/")
def serve_dashboard():
    # This tells Flask to look inside the "templates" folder for "index.html"
    return render_template("index.html")

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/auth/login", methods=["POST"])
def login():
    global failed_attempts
    data = request.get_json()
    
    username = data.get("username")
    password = data.get("password")
    
    # Behavior Security Check: Block if too many attempts
    if failed_attempts >= 5:
        return jsonify({"error": "Account locked due to unusual behavior"}), 429
    
    # Standard Authentication Check
    if username == "peehu_test" and password == "securepassword123":
        failed_attempts = 0 # reset on success
        # Returning a token here so your Phase 9 frontend works perfectly!
        return jsonify({
            "message": "Login successful", 
            "token": "simulated_jwt_token_123"
        }), 200
    else:
        failed_attempts += 1
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/session", methods=["POST"])
def handle_session():
    # 1. Verify the Token (Phase 6 Security!)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized: Missing or invalid token"}), 401
    
    # 2. Process the Data
    data = request.get_json()
    archetype = data.get("archetype", "Unknown")
    
    # Print it to your Python terminal so you can see it arrived safely
    print(f"\n[ALERT] Received {archetype} attack simulation data!")
    print(f"Data payload: {data}\n")
    
    return jsonify({
        "status": "Analysis complete", 
        "risk_score": 85, 
        "action": "Flagged"
    }), 200

@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    # Enforce security token for viewing history
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    # Mock database of sessions (including Anomalies vs Normal)
    mock_sessions = [
        {"id": "TRK-901", "wpm": 85, "risk_score": 12, "true_label": "Valid User", "source": "Web", "is_anomaly": False},
        {"id": "TRK-902", "wpm": 15, "risk_score": 92, "true_label": "Botnet Swarm", "source": "live", "is_anomaly": True},
        {"id": "TRK-903", "wpm": 110, "risk_score": 88, "true_label": "Brute Force", "source": "API", "is_anomaly": True}
    ]
    return jsonify(mock_sessions)

@app.route("/api/simulate", methods=["POST"])
def simulate_attack():
    # Enforce token security
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    attack_type = data.get("attack_type", "unknown")
    
    # Mocking what Phase 7's attack_generator.py will eventually return
    mock_wpm = random.randint(150, 300) if attack_type == "high_speed_typing" else random.randint(10, 40)
    
    return jsonify({
        "is_anomaly": True,
        "risk_score": random.randint(85, 99),
        "profile": {
            "wpm": mock_wpm
        }
    })

# 3. Run the app at the VERY BOTTOM
if __name__ == "__main__":
    from waitress import serve
    print("Starting production server with Waitress on port 8080...")
    serve(app, host="0.0.0.0", port=8080)