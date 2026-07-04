import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Kredensial Supabase langsung ditaruh di dalam codingan (Private Project)
SUPABASE_URL = "https://kmyipabrhukygbashtwh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtteWlwYWJyaHVreWdiYXNodHdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0ODMyMTIsImV4cCI6MjA5ODA1OTIxMn0.EQC95fFG2xeM0Wy5UiG55bo1ftx8sA7gS1etoTmOym0"

# Header wajib untuk mengakses REST API Supabase
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Template HTML modern dengan Poppins & Font Awesome
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GemstonesHub • Farming Tracker</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'poppins': ['Poppins', 'sans-serif'],
                    },
                }
            }
        }
    </script>
</head>
<body class="bg-[#0a0a0f] min-h-screen font-poppins">
    <!-- Background Gradient Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/5 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-6xl mx-auto px-4 py-10">
        <!-- Header Section -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6 mb-10">
            <div class="space-y-1">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25">
                        <i class="fa-solid fa-gem text-white text-lg"></i>
                    </div>
                    <h1 class="text-3xl font-semibold text-white tracking-tight">
                        Gemstones<span class="text-blue-400">Hub</span>
                    </h1>
                </div>
                <p class="text-gray-500 text-sm ml-13">Inventory tracking dashboard</p>
            </div>
            
            <button onclick="resetData()" 
                    class="group flex items-center gap-2 px-5 py-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 font-medium text-sm hover:bg-red-500/20 hover:border-red-500/40 transition-all duration-300">
                <i class="fa-solid fa-rotate-left group-hover:-translate-x-1 transition-transform duration-300"></i>
                <span>Reset Data</span>
            </button>
        </div>

        <!-- Stats Overview Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-10">
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-5 hover:border-blue-500/30 transition-all duration-300">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center">
                        <i class="fa-solid fa-fish text-blue-400 text-xl"></i>
                    </div>
                    <div>
                        <p class="text-gray-500 text-xs uppercase tracking-wider">Elshark Gran Maja</p>
                        <p class="text-2xl font-semibold text-white mt-1" id="total-shark">-</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-5 hover:border-purple-500/30 transition-all duration-300">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center">
                        <i class="fa-solid fa-shield-halved text-purple-400 text-xl"></i>
                    </div>
                    <div>
                        <p class="text-gray-500 text-xs uppercase tracking-wider">Gladiator Shark</p>
                        <p class="text-2xl font-semibold text-white mt-1" id="total-gladiator">-</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-5 hover:border-amber-500/30 transition-all duration-300">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center">
                        <i class="fa-solid fa-wand-magic-sparkles text-amber-400 text-xl"></i>
                    </div>
                    <div>
                        <p class="text-gray-500 text-xs uppercase tracking-wider">Enchant Stone</p>
                        <p class="text-2xl font-semibold text-white mt-1" id="total-stone">-</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Table Section -->
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl overflow-hidden">
            <div class="px-6 py-5 border-b border-gray-800/60">
                <h2 class="text-lg font-medium text-white flex items-center gap-2">
                    <i class="fa-solid fa-users text-gray-400"></i>
                    Player Inventory
                </h2>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="border-b border-gray-800/60">
                            <th class="py-4 px-6 text-left">
                                <span class="text-gray-500 text-xs font-medium uppercase tracking-wider">Player</span>
                            </th>
                            <th class="py-4 px-6 text-center">
                                <span class="text-gray-500 text-xs font-medium uppercase tracking-wider">
                                    <i class="fa-solid fa-fish text-blue-400/70 mr-1"></i> Elshark
                                </span>
                            </th>
                            <th class="py-4 px-6 text-center">
                                <span class="text-gray-500 text-xs font-medium uppercase tracking-wider">
                                    <i class="fa-solid fa-shield-halved text-purple-400/70 mr-1"></i> Gladiator
                                </span>
                            </th>
                            <th class="py-4 px-6 text-center">
                                <span class="text-gray-500 text-xs font-medium uppercase tracking-wider">
                                    <i class="fa-solid fa-wand-magic-sparkles text-amber-400/70 mr-1"></i> Stone
                                </span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/40">
                        {% for row in data %}
                        <tr class="hover:bg-white/[0.02] transition-colors duration-200">
                            <td class="py-4 px-6">
                                <div class="flex items-center gap-3">
                                    <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center text-sm font-medium text-white">
                                        {{ row.username[:1].upper() }}
                                    </div>
                                    <span class="text-white font-medium">{{ row.username }}</span>
                                </div>
                            </td>
                            <td class="py-4 px-6 text-center">
                                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 font-medium text-sm">
                                    {{ row.elshark_gran_maja }}
                                </span>
                            </td>
                            <td class="py-4 px-6 text-center">
                                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-500/10 text-purple-400 font-medium text-sm">
                                    {{ row.gladiator_shark }}
                                </span>
                            </td>
                            <td class="py-4 px-6 text-center">
                                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-400 font-medium text-sm">
                                    {{ row.evolved_enchant_stone }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                        
                        {% if not data %}
                        <tr>
                            <td colspan="4" class="py-16 text-center">
                                <div class="flex flex-col items-center gap-3">
                                    <div class="w-16 h-16 rounded-2xl bg-gray-800/50 flex items-center justify-center">
                                        <i class="fa-solid fa-inbox text-gray-600 text-2xl"></i>
                                    </div>
                                    <p class="text-gray-500 font-medium">No data yet</p>
                                    <p class="text-gray-600 text-sm">Start tracking your inventory items</p>
                                </div>
                            </td>
                        </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Calculate and display totals
        function updateTotals() {
            const rows = document.querySelectorAll('tbody tr:not(:last-child)');
            let totalShark = 0, totalGladiator = 0, totalStone = 0;
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td span');
                if (cells.length >= 3) {
                    totalShark += parseInt(cells[1].textContent.trim()) || 0;
                    totalGladiator += parseInt(cells[2].textContent.trim()) || 0;
                    totalStone += parseInt(cells[3].textContent.trim()) || 0;
                }
            });
            
            document.getElementById('total-shark').textContent = totalShark || '0';
            document.getElementById('total-gladiator').textContent = totalGladiator || '0';
            document.getElementById('total-stone').textContent = totalStone || '0';
        }
        
        updateTotals();

        function resetData() {
            if(confirm("Are you sure you want to reset all item counts to 0?")) {
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

    # 1. Cek apakah user sudah ada di database
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

    # 2. Kalkulasi nilai baru
    update_data = {}
    if "Elshark Gran Maja" in items:
        update_data["elshark_gran_maja"] = current_data.get("elshark_gran_maja", 0) + 1
    if "Gladiator Shark" in items:
        update_data["gladiator_shark"] = current_data.get("gladiator_shark", 0) + 1
    if "Evolved Enchant Stone" in items:
        update_data["evolved_enchant_stone"] = current_data.get("evolved_enchant_stone", 0) + 1

    # 3. Update atau insert data
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
