from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime, timezone

app = Flask(__name__)

# Kredensial Supabase
SUPABASE_URL = "https://kmyipabrhukygbashtwh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtteWlwYWJyaHVreWdiYXNodHdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0ODMyMTIsImV4cCI6MjA5ODA1OTIxMn0.EQC95fFG2xeM0Wy5UiG55bo1ftx8sA7gS1etoTmOym0"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def dashboard():
    return render_template('bot.html')

@app.route('/inventory')
def inventory_dashboard():
    url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?select=*"
    res = requests.get(url, headers=HEADERS)
    data = res.json() if res.status_code == 200 else []
    
    # Calculate totals
    total_shark = sum(row.get('elshark_gran_maja', 0) for row in data)
    total_gladiator = sum(row.get('gladiator_shark', 0) for row in data)
    total_stone = sum(row.get('evolved_enchant_stone', 0) for row in data)
    
    return render_template('inventory.html', 
                         data=data, 
                         total_shark=total_shark, 
                         total_gladiator=total_gladiator, 
                         total_stone=total_stone)

@app.route('/api/poll', methods=['POST'])
def bot_poll():
    data = request.json or {}
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    clean_username = username.strip().lower()
    current_time = datetime.now(timezone.utc).isoformat()

    check_res = requests.get(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", headers=HEADERS)
    
    if check_res.status_code == 200 and len(check_res.json()) > 0:
        requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", 
                      json={"last_seen": current_time}, headers=HEADERS)
    else:
        requests.post(f"{SUPABASE_URL}/rest/v1/bots", 
                     json={"username": clean_username, "last_seen": current_time, "command": "none"}, 
                     headers=HEADERS)

    command = "none"
    get_cmd = requests.get(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}&select=command", headers=HEADERS)
    if get_cmd.status_code == 200 and len(get_cmd.json()) > 0:
        command = get_cmd.json()[0].get('command', 'none')

    if command == "respawn":
        requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", 
                      json={"command": "none"}, headers=HEADERS)

    return jsonify({"command": command})

@app.route('/api/users', methods=['GET'])
def get_users():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/bots?select=*&order=last_seen.desc", headers=HEADERS)
    if res.status_code == 200:
        return jsonify({"bots": res.json()})
    return jsonify({"bots": []})

@app.route('/api/respawn', methods=['POST'])
def trigger_respawn():
    data = request.json or {}
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    clean_username = username.strip().lower()
    res = requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", 
                        json={"command": "respawn"}, headers=HEADERS)
    
    if res.status_code in [200, 201, 204]:
        return jsonify({"success": True})
    return jsonify({"error": "Gagal update database"}), 500

@app.route('/api/track', methods=['POST'])
def track_item():
    req_data = request.json
    username = req_data.get('username')
    items = req_data.get('items', [])

    if not username or not items:
        return jsonify({"error": "Data tidak lengkap"}), 400

    check_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=eq.{username}&select=*"
    check_res = requests.get(check_url, headers=HEADERS)
    
    user_rows = check_res.json() if check_res.status_code == 200 else []
    is_existing_user = len(user_rows) > 0

    current_data = {
        "elshark_gran_maja": 0,
        "gladiator_shark": 0,
        "evolved_enchant_stone": 0
    }

    if is_existing_user:
        current_data = user_rows[0]

    update_data = {}
    if "Elshark Gran Maja" in items:
        update_data["elshark_gran_maja"] = current_data.get("elshark_gran_maja", 0) + 1
    if "Gladiator Shark" in items:
        update_data["gladiator_shark"] = current_data.get("gladiator_shark", 0) + 1
    if "Evolved Enchant Stone" in items:
        update_data["evolved_enchant_stone"] = current_data.get("evolved_enchant_stone", 0) + 1

    if is_existing_user:
        patch_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=eq.{username}"
        requests.patch(patch_url, json=update_data, headers=HEADERS)
    else:
        update_data["username"] = username
        post_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking"
        requests.post(post_url, json=update_data, headers=HEADERS)

    return jsonify({"status": "success"}), 200

@app.route('/api/update', methods=['POST'])
def update_item():
    req_data = request.json
    username = req_data.get('username')
    
    if not username:
        return jsonify({"error": "Username diperlukan"}), 400
    
    update_data = {
        "elshark_gran_maja": req_data.get('elshark_gran_maja', 0),
        "gladiator_shark": req_data.get('gladiator_shark', 0),
        "evolved_enchant_stone": req_data.get('evolved_enchant_stone', 0)
    }
    
    patch_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=eq.{username}"
    res = requests.patch(patch_url, json=update_data, headers=HEADERS)
    
    if res.status_code in [200, 204]:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Gagal update data"}), 500

@app.route('/api/reset', methods=['POST'])
def reset_counts():
    reset_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=not.is.null"
    reset_data = {
        "elshark_gran_maja": 0,
        "gladiator_shark": 0,
        "evolved_enchant_stone": 0
    }
    
    requests.patch(reset_url, json=reset_data, headers=HEADERS)
    return jsonify({"message": "Semua data berhasil direset ke 0"}), 200

@app.route('/api/poll_endpoint')
def poll_endpoint_info():
    return jsonify({
        "poll_url": "https://roblox-teleport-script.vercel.app/api/poll",
        "method": "POST",
        "body": {"username": "your_bot_username"},
        "response": {"command": "respawn or none"}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
