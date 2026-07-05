from flask import Flask, request, jsonify, render_template_string
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

# Template HTML untuk Dashboard Bot (disederhanakan)
BOT_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GemstonesHub • Bot Dashboard</title>
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
    <style>
        * { box-sizing: border-box; }
        body { background: #0a0a0f; font-family: 'Poppins', sans-serif; }
        .status-online { color: #34d399; }
        .status-offline { color: #f87171; }
        .table-wrapper { overflow-x: auto; }
        .table-wrapper table { min-width: 600px; width: 100%; }
        @media (max-width: 640px) { .table-wrapper table { min-width: 500px; } }
    </style>
</head>
<body class="bg-[#0a0a0f] min-h-screen">
    <div class="max-w-6xl mx-auto px-4 py-8">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <div>
                <h1 class="text-2xl sm:text-3xl font-semibold text-white">
                    Gemstones<span class="text-blue-400">Hub</span>
                </h1>
                <p class="text-gray-500 text-sm">Bot Management Dashboard</p>
            </div>
            <div class="flex gap-3 w-full sm:w-auto">
                <button onclick="refreshData()" class="px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400 text-sm hover:bg-blue-500/20">
                    <i class="fa-solid fa-rotate mr-2"></i>Refresh
                </button>
                <a href="/inventory" class="px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-400 text-sm hover:bg-purple-500/20">
                    <i class="fa-solid fa-gem mr-2"></i>Inventory
                </a>
            </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-4 mb-8">
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Online</p>
                <p class="text-2xl font-semibold text-white" id="online-count">0</p>
            </div>
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Offline</p>
                <p class="text-2xl font-semibold text-white" id="offline-count">0</p>
            </div>
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Total</p>
                <p class="text-2xl font-semibold text-white" id="total-count">0</p>
            </div>
        </div>

        <!-- Table -->
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-800/60 flex justify-between items-center">
                <h2 class="text-white font-medium"><i class="fa-solid fa-robot mr-2"></i>Bot Status</h2>
                <span class="text-xs text-gray-500" id="last-update">Just now</span>
            </div>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr class="border-b border-gray-800/60">
                            <th class="py-3 px-6 text-left text-gray-500 text-xs uppercase">Username</th>
                            <th class="py-3 px-6 text-left text-gray-500 text-xs uppercase">Status</th>
                            <th class="py-3 px-6 text-left text-gray-500 text-xs uppercase">Last Seen</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Command</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Action</th>
                        </tr>
                    </thead>
                    <tbody id="bot-table-body"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Respawn Modal -->
    <div id="respawnModal" class="fixed inset-0 hidden items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-6 max-w-md w-full">
            <h3 class="text-lg font-semibold text-white mb-4">
                <i class="fa-solid fa-skull text-red-400 mr-2"></i>Respawn Bot
            </h3>
            <p class="text-gray-300 mb-4">Respawn bot <span id="respawnUsername" class="text-blue-400 font-semibold"></span>?</p>
            <div class="flex gap-3">
                <button onclick="closeRespawnModal()" class="flex-1 px-4 py-2 rounded-xl border border-gray-700 text-gray-400 hover:bg-gray-800">Cancel</button>
                <button onclick="confirmRespawn()" class="flex-1 px-4 py-2 rounded-xl bg-red-500 text-white hover:bg-red-600">Respawn</button>
            </div>
        </div>
    </div>

    <script>
        let currentRespawnUser = null;

        async function fetchBots() {
            try {
                const response = await fetch('/api/users');
                const data = await response.json();
                updateTable(data.bots);
                updateStats(data.bots);
                document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function updateTable(bots) {
            const tbody = document.getElementById('bot-table-body');
            if (!bots || bots.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" class="py-8 text-center text-gray-500">No bots online</td></tr>`;
                return;
            }

            let html = '';
            const now = new Date();
            bots.forEach(bot => {
                const lastSeen = new Date(bot.last_seen);
                const diffMinutes = Math.floor((now - lastSeen) / 1000 / 60);
                const isOnline = diffMinutes < 1;
                const statusClass = isOnline ? 'status-online' : 'status-offline';
                const statusText = isOnline ? 'Online' : 'Offline';
                const lastSeenText = diffMinutes < 1 ? 'Just now' : 
                                    diffMinutes < 60 ? diffMinutes + 'm ago' :
                                    Math.floor(diffMinutes / 60) + 'h ' + (diffMinutes % 60) + 'm ago';

                html += `
                    <tr class="hover:bg-white/[0.02]">
                        <td class="py-3 px-6 text-white">${bot.username}</td>
                        <td class="py-3 px-6">
                            <span class="${statusClass}">● ${statusText}</span>
                        </td>
                        <td class="py-3 px-6 text-gray-400 text-sm">${lastSeenText}</td>
                        <td class="py-3 px-6 text-center">
                            <span class="px-2 py-1 rounded-lg text-xs ${bot.command === 'respawn' ? 'bg-red-500/20 text-red-400' : 'bg-gray-700/30 text-gray-400'}">
                                ${bot.command || 'none'}
                            </span>
                        </td>
                        <td class="py-3 px-6 text-center">
                            <button onclick="openRespawnModal('${bot.username}')" class="px-3 py-1 bg-gray-800 hover:bg-red-500/20 text-gray-400 hover:text-red-400 rounded-lg transition">
                                <i class="fa-solid fa-skull"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
        }

        function updateStats(bots) {
            const now = new Date();
            let online = 0, offline = 0;
            bots.forEach(bot => {
                const diffMinutes = Math.floor((now - new Date(bot.last_seen)) / 1000 / 60);
                diffMinutes < 1 ? online++ : offline++;
            });
            document.getElementById('online-count').textContent = online;
            document.getElementById('offline-count').textContent = offline;
            document.getElementById('total-count').textContent = bots.length;
        }

        function openRespawnModal(username) {
            currentRespawnUser = username;
            document.getElementById('respawnUsername').textContent = username;
            document.getElementById('respawnModal').style.display = 'flex';
        }

        function closeRespawnModal() {
            document.getElementById('respawnModal').style.display = 'none';
            currentRespawnUser = null;
        }

        function confirmRespawn() {
            if (!currentRespawnUser) return;
            fetch('/api/respawn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: currentRespawnUser })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeRespawnModal();
                    fetchBots();
                } else {
                    alert('Failed to respawn bot');
                }
            })
            .catch(error => alert('Error: ' + error));
        }

        function refreshData() { fetchBots(); }
        setInterval(fetchBots, 30000);
        fetchBots();
    </script>
</body>
</html>
"""

# Template HTML untuk Inventory (disederhanakan)
INVENTORY_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GemstonesHub • Inventory</title>
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
    <style>
        * { box-sizing: border-box; }
        body { background: #0a0a0f; font-family: 'Poppins', sans-serif; }
        .table-wrapper { overflow-x: auto; }
        .table-wrapper table { min-width: 600px; width: 100%; }
        .value-badge { 
            display: inline-flex; 
            align-items: center; 
            gap: 0.375rem; 
            padding: 0.25rem 0.75rem; 
            border-radius: 0.5rem; 
            font-weight: 500; 
            font-size: 0.875rem; 
        }
        @media (max-width: 640px) { .table-wrapper table { min-width: 500px; } }
    </style>
</head>
<body class="bg-[#0a0a0f] min-h-screen">
    <div class="max-w-6xl mx-auto px-4 py-8">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <div>
                <h1 class="text-2xl sm:text-3xl font-semibold text-white">
                    Gemstones<span class="text-blue-400">Hub</span>
                </h1>
                <p class="text-gray-500 text-sm">Inventory Tracking Dashboard</p>
            </div>
            <div class="flex gap-3 w-full sm:w-auto">
                <button onclick="resetData()" class="px-4 py-2 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm hover:bg-red-500/20">
                    <i class="fa-solid fa-rotate-left mr-2"></i>Reset
                </button>
                <a href="/" class="px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400 text-sm hover:bg-blue-500/20">
                    <i class="fa-solid fa-robot mr-2"></i>Bot Dashboard
                </a>
            </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-4 mb-8">
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Elshark</p>
                <p class="text-2xl font-semibold text-white" id="total-shark">0</p>
            </div>
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Gladiator</p>
                <p class="text-2xl font-semibold text-white" id="total-gladiator">0</p>
            </div>
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-4">
                <p class="text-gray-500 text-xs uppercase">Enchant Stone</p>
                <p class="text-2xl font-semibold text-white" id="total-stone">0</p>
            </div>
        </div>

        <!-- Table -->
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-800/60">
                <h2 class="text-white font-medium"><i class="fa-solid fa-users mr-2"></i>Player Inventory</h2>
            </div>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr class="border-b border-gray-800/60">
                            <th class="py-3 px-6 text-left text-gray-500 text-xs uppercase">Player</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Elshark</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Gladiator</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Stone</th>
                            <th class="py-3 px-6 text-center text-gray-500 text-xs uppercase">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                        <tr class="hover:bg-white/[0.02]" data-username="{{ row.username }}">
                            <td class="py-3 px-6 text-white">{{ row.username }}</td>
                            <td class="py-3 px-6 text-center">
                                <span class="value-badge bg-blue-500/10 text-blue-400">
                                    <span class="item-value" data-field="elshark_gran_maja">{{ row.elshark_gran_maja }}</span>
                                </span>
                            </td>
                            <td class="py-3 px-6 text-center">
                                <span class="value-badge bg-purple-500/10 text-purple-400">
                                    <span class="item-value" data-field="gladiator_shark">{{ row.gladiator_shark }}</span>
                                </span>
                            </td>
                            <td class="py-3 px-6 text-center">
                                <span class="value-badge bg-amber-500/10 text-amber-400">
                                    <span class="item-value" data-field="evolved_enchant_stone">{{ row.evolved_enchant_stone }}</span>
                                </span>
                            </td>
                            <td class="py-3 px-6 text-center">
                                <button onclick="openEditModal('{{ row.username }}', {{ row.elshark_gran_maja }}, {{ row.gladiator_shark }}, {{ row.evolved_enchant_stone }})" 
                                        class="px-3 py-1 bg-gray-800 hover:bg-blue-500/20 text-gray-400 hover:text-blue-400 rounded-lg transition">
                                    <i class="fa-solid fa-pen-to-square"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                        {% if not data %}
                        <tr><td colspan="5" class="py-8 text-center text-gray-500">No data yet</td></tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Edit Modal -->
    <div id="editModal" class="fixed inset-0 hidden items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-6 max-w-md w-full">
            <h3 class="text-lg font-semibold text-white mb-4">
                <i class="fa-solid fa-pen-to-square text-blue-400 mr-2"></i>Edit Inventory
            </h3>
            <div class="mb-4">
                <label class="block text-gray-400 text-sm mb-1">Username</label>
                <input type="text" id="editUsername" disabled class="w-full bg-[#0a0a0f] border border-gray-700 rounded-xl px-4 py-2 text-gray-400">
            </div>
            <div class="space-y-3 mb-4">
                <div>
                    <label class="block text-gray-400 text-sm mb-1">Elshark Gran Maja</label>
                    <div class="flex gap-2">
                        <button onclick="decrementValue('editElshark')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">-</button>
                        <input type="number" id="editElshark" min="0" class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-4 py-2 text-white text-center">
                        <button onclick="incrementValue('editElshark')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">+</button>
                    </div>
                </div>
                <div>
                    <label class="block text-gray-400 text-sm mb-1">Gladiator Shark</label>
                    <div class="flex gap-2">
                        <button onclick="decrementValue('editGladiator')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">-</button>
                        <input type="number" id="editGladiator" min="0" class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-4 py-2 text-white text-center">
                        <button onclick="incrementValue('editGladiator')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">+</button>
                    </div>
                </div>
                <div>
                    <label class="block text-gray-400 text-sm mb-1">Evolved Enchant Stone</label>
                    <div class="flex gap-2">
                        <button onclick="decrementValue('editStone')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">-</button>
                        <input type="number" id="editStone" min="0" class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-4 py-2 text-white text-center">
                        <button onclick="incrementValue('editStone')" class="px-3 py-1 bg-gray-800 rounded-lg text-white">+</button>
                    </div>
                </div>
            </div>
            <div class="flex gap-3">
                <button onclick="closeEditModal()" class="flex-1 px-4 py-2 rounded-xl border border-gray-700 text-gray-400 hover:bg-gray-800">Cancel</button>
                <button onclick="saveEdit()" class="flex-1 px-4 py-2 rounded-xl bg-blue-500 text-white hover:bg-blue-600">Save</button>
            </div>
        </div>
    </div>

    <script>
        let currentEditingUser = null;

        function openEditModal(username, elshark, gladiator, stone) {
            currentEditingUser = username;
            document.getElementById('editUsername').value = username;
            document.getElementById('editElshark').value = elshark;
            document.getElementById('editGladiator').value = gladiator;
            document.getElementById('editStone').value = stone;
            document.getElementById('editModal').style.display = 'flex';
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
            currentEditingUser = null;
        }

        function incrementValue(id) {
            const input = document.getElementById(id);
            input.value = parseInt(input.value) + 1;
        }

        function decrementValue(id) {
            const input = document.getElementById(id);
            const val = parseInt(input.value) - 1;
            input.value = val >= 0 ? val : 0;
        }

        function saveEdit() {
            if (!currentEditingUser) return;
            const data = {
                username: currentEditingUser,
                elshark_gran_maja: parseInt(document.getElementById('editElshark').value),
                gladiator_shark: parseInt(document.getElementById('editGladiator').value),
                evolved_enchant_stone: parseInt(document.getElementById('editStone').value)
            };

            fetch('/api/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    location.reload();
                } else {
                    alert('Failed to update');
                }
            })
            .catch(error => alert('Error: ' + error));
        }

        function resetData() {
            if (confirm('Reset all inventory to 0?')) {
                fetch('/api/reset', { method: 'POST' })
                .then(() => location.reload());
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(BOT_TEMPLATE)

@app.route('/inventory')
def inventory_dashboard():
    url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?select=*"
    res = requests.get(url, headers=HEADERS)
    data = res.json() if res.status_code == 200 else []
    return render_template_string(INVENTORY_TEMPLATE, data=data)

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

# Untuk Vercel
if __name__ == '__main__':
    app.run(debug=True, port=5000)
