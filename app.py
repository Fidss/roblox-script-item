import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Kredensial Supabase langsung ditaruh di dalam codingan (Private Project)
SUPABASE_URL = "https://xyz-id-supabase-kamu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey..." # Masukkan anon/public key di sini

# Header wajib untuk mengakses REST API Supabase
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Template HTML menggunakan Tailwind CSS (Tetap Sama)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GemstonesHub - Farming Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white p-8">
    <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold text-blue-400">GemstonesHub Tracker</h1>
            <button onclick="resetData()" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Reset All Counts
            </button>
        </div>
        
        <div class="bg-gray-800 shadow-md rounded my-6 overflow-x-auto">
            <table class="min-w-full table-auto">
                <thead>
                    <tr class="bg-gray-700 text-gray-300 uppercase text-sm leading-normal">
                        <th class="py-3 px-6 text-left">Username</th>
                        <th class="py-3 px-6 text-center">Elshark Gran Maja</th>
                        <th class="py-3 px-6 text-center">Gladiator Shark</th>
                        <th class="py-3 px-6 text-center">Evolved Enchant Stone</th>
                    </tr>
                </thead>
                <tbody class="text-gray-200 text-sm font-light">
                    {% for row in data %}
                    <tr class="border-b border-gray-700 hover:bg-gray-700">
                        <td class="py-3 px-6 text-left font-bold">{{ row.username }}</td>
                        <td class="py-3 px-6 text-center">{{ row.elshark_gran_maja }}</td>
                        <td class="py-3 px-6 text-center">{{ row.gladiator_shark }}</td>
                        <td class="py-3 px-6 text-center">{{ row.evolved_enchant_stone }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function resetData() {
            if(confirm("Yakin ingin mereset semua item menjadi 0?")) {
                fetch('/api/reset', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    # Ambil semua data dari Supabase via GET request
    url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?select=*"
    res = requests.get(url, headers=HEADERS)
    
    data = res.json() if res.status_code == 200 else []
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/api/track', methods=['POST'])
def track_item():
    req_data = request.json
    username = req_data.get('username')
    items = req_data.get('items', [])

    if not username or not items:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # 1. Cek apakah user sudah ada di database (Cari berdasarkan username)
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

    # 2. Kalkulasi nilai baru (+1 untuk setiap item yang dikirim dari script)
    update_data = {}
    if "Elshark Gran Maja" in items:
        update_data["elshark_gran_maja"] = current_data.get("elshark_gran_maja", 0) + 1
    if "Gladiator Shark" in items:
        update_data["gladiator_shark"] = current_data.get("gladiator_shark", 0) + 1
    if "Evolved Enchant Stone" in items:
        update_data["evolved_enchant_stone"] = current_data.get("evolved_enchant_stone", 0) + 1

    # 3. Kirim data ke Supabase (UPDATE jika ada, INSERT jika belum ada)
    if is_existing_user:
        patch_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=eq.{username}"
        requests.patch(patch_url, json=update_data, headers=HEADERS)
    else:
        update_data["username"] = username
        post_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking"
        requests.post(post_url, json=update_data, headers=HEADERS)

    return jsonify({"status": "success"}), 200

@app.route('/api/reset', methods=['POST'])
def reset_counts():
    # Mengubah semua data item menjadi 0 tanpa menghapus username (menggunakan filter neq.null)
    reset_url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?username=not.is.null"
    reset_data = {
        "elshark_gran_maja": 0,
        "gladiator_shark": 0,
        "evolved_enchant_stone": 0
    }
    
    requests.patch(reset_url, json=reset_data, headers=HEADERS)
    return jsonify({"message": "Semua data berhasil direset ke 0"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
