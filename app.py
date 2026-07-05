from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__, template_folder='../templates')

# Kredensial Supabase
SUPABASE_URL = "https://kmyipabrhukygbashtwh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtteWlwYWJyaHVreWdiYXNodHdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0ODMyMTIsImV4cCI6MjA5ODA1OTIxMn0.EQC95fFG2xeM0Wy5UiG55bo1ftx8sA7gS1etoTmOym0"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Template HTML yang sudah digabung
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GemstonesHub • Bot Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css">
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
        * {
            box-sizing: border-box;
        }
        
        html, body {
            overflow-x: hidden;
            width: 100%;
            position: relative;
            margin: 0;
            padding: 0;
        }
        
        body {
            max-width: 100vw;
            overflow-x: hidden;
        }
        
        .item-image {
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
            transition: transform 0.3s ease, filter 0.3s ease;
        }
        .item-image:hover {
            transform: scale(1.1);
            filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.5)) brightness(1.1);
        }
        
        [data-aos="fade-up-custom"] {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        [data-aos="fade-up-custom"].aos-animate {
            opacity: 1;
            transform: translateY(0);
        }
        
        [data-aos="fade-right-custom"] {
            opacity: 0;
            transform: translateX(-30px);
            transition: opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        [data-aos="fade-right-custom"].aos-animate {
            opacity: 1;
            transform: translateX(0);
        }
        
        [data-aos="zoom-in-custom"] {
            opacity: 0;
            transform: scale(0.9);
            transition: opacity 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        [data-aos="zoom-in-custom"].aos-animate {
            opacity: 1;
            transform: scale(1);
        }
        
        .stats-card {
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.1); }
            50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
        }
        
        .table-wrapper {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: thin;
            scrollbar-color: rgba(75, 85, 99, 0.3) transparent;
        }
        
        .table-wrapper::-webkit-scrollbar {
            height: 6px;
        }
        
        .table-wrapper::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .table-wrapper::-webkit-scrollbar-thumb {
            background: rgba(75, 85, 99, 0.3);
            border-radius: 3px;
        }
        
        .table-wrapper table {
            width: 100%;
            min-width: 600px;
        }
        
        .value-badge {
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.75rem;
            border-radius: 0.5rem;
            font-weight: 500;
            font-size: 0.875rem;
            min-width: fit-content;
        }
        
        .main-container {
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
        }
        
        @media (max-width: 640px) {
            .value-badge {
                padding: 0.25rem 0.5rem;
                font-size: 0.75rem;
                gap: 0.25rem;
            }
            
            .table-wrapper table {
                min-width: 500px;
            }
        }
        
        @media (max-width: 480px) {
            .table-wrapper table {
                min-width: 450px;
            }
        }
        
        .status-online {
            color: #34d399;
        }
        .status-offline {
            color: #f87171;
        }
    </style>
</head>
<body class="bg-[#0a0a0f] min-h-screen font-poppins overflow-x-hidden">
    <!-- Background Gradient Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse" style="animation-duration: 8s;"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" style="animation-duration: 10s;"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/5 rounded-full blur-3xl animate-pulse" style="animation-duration: 12s;"></div>
    </div>

    <!-- Respawn Modal -->
    <div id="respawnModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick="closeRespawnModal()"></div>
        <div class="relative bg-[#12121a] border border-gray-800/60 rounded-2xl p-4 sm:p-6 w-full max-w-md shadow-2xl">
            <div class="flex items-center justify-between mb-4 sm:mb-6">
                <h3 class="text-base sm:text-lg font-semibold text-white flex items-center gap-2">
                    <i class="fa-solid fa-skull text-red-400"></i>
                    Respawn Bot
                </h3>
                <button onclick="closeRespawnModal()" class="text-gray-500 hover:text-white transition-colors">
                    <i class="fa-solid fa-xmark text-xl"></i>
                </button>
            </div>
            
            <div class="mb-4">
                <p class="text-gray-300 text-sm sm:text-base">Anda yakin ingin me-respawn bot <span id="respawnUsername" class="text-blue-400 font-semibold"></span>?</p>
                <p class="text-gray-500 text-xs sm:text-sm mt-2">Bot akan melakukan teleportasi ke spawn point.</p>
            </div>
            
            <div class="flex gap-2 sm:gap-3">
                <button onclick="closeRespawnModal()" 
                        class="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl border border-gray-700 text-gray-400 text-sm sm:text-base font-medium hover:bg-gray-800 transition-colors">
                    Cancel
                </button>
                <button onclick="confirmRespawn()" 
                        class="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl bg-gradient-to-r from-red-500 to-red-600 text-white text-sm sm:text-base font-medium hover:from-red-600 hover:to-red-700 transition-all shadow-lg shadow-red-500/25">
                    <i class="fa-solid fa-check mr-1 sm:mr-2"></i> Respawn
                </button>
            </div>
        </div>
    </div>

    <div class="main-container relative max-w-6xl mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-10">
        <!-- Header Section -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-6 mb-6 sm:mb-10" 
             data-aos="fade-down" data-aos-duration="800" data-aos-easing="ease-out-cubic" data-aos-once="true">
            <div class="space-y-1">
                <div class="flex items-center gap-2 sm:gap-3">
                    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25 flex-shrink-0"
                         data-aos="zoom-in" data-aos-duration="600" data-aos-delay="200" data-aos-once="true">
                        <i class="fa-solid fa-robot text-white text-sm sm:text-lg"></i>
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-semibold text-white tracking-tight" 
                        data-aos="fade-right" data-aos-duration="600" data-aos-delay="400" data-aos-once="true">
                        Gemstones<span class="text-blue-400">Hub</span>
                    </h1>
                </div>
                <p class="text-gray-500 text-xs sm:text-sm ml-10 sm:ml-13" 
                   data-aos="fade-up" data-aos-duration="600" data-aos-delay="600" data-aos-once="true">
                    Bot Management Dashboard
                </p>
            </div>
            
            <div class="flex gap-2 sm:gap-3 w-full sm:w-auto">
                <button onclick="refreshData()" 
                        class="flex items-center gap-2 px-4 sm:px-5 py-2.5 sm:py-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400 font-medium text-xs sm:text-sm hover:bg-blue-500/20 hover:border-blue-500/40 transition-all duration-300 w-full sm:w-auto justify-center">
                    <i class="fa-solid fa-rotate"></i>
                    <span>Refresh</span>
                </button>
                <a href="/inventory" 
                   class="flex items-center gap-2 px-4 sm:px-5 py-2.5 sm:py-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-400 font-medium text-xs sm:text-sm hover:bg-purple-500/20 hover:border-purple-500/40 transition-all duration-300 w-full sm:w-auto justify-center">
                    <i class="fa-solid fa-gem"></i>
                    <span>Inventory</span>
                </a>
            </div>
        </div>

        <!-- Stats Overview Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-5 mb-6 sm:mb-10">
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-green-500/30 transition-all duration-300 group stats-card"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="100" data-aos-once="true">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-green-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <i class="fa-solid fa-circle text-green-400 text-2xl sm:text-3xl"></i>
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Online Bots</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="online-count">0</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-red-500/30 transition-all duration-300 group stats-card"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="300" data-aos-once="true">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-red-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <i class="fa-solid fa-circle text-red-400 text-2xl sm:text-3xl"></i>
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Offline Bots</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="offline-count">0</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-blue-500/30 transition-all duration-300 group stats-card"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="500" data-aos-once="true">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-blue-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <i class="fa-solid fa-users text-blue-400 text-2xl sm:text-3xl"></i>
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Total Bots</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="total-count">0</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Table Section -->
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl overflow-hidden"
             data-aos="fade-up" data-aos-duration="800" data-aos-delay="200" data-aos-once="true">
            <div class="px-4 sm:px-6 py-3 sm:py-5 border-b border-gray-800/60 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 sm:gap-0">
                <h2 class="text-base sm:text-lg font-medium text-white flex items-center gap-2">
                    <i class="fa-solid fa-robot text-gray-400"></i>
                    Bot Status
                </h2>
                <span class="text-xs text-gray-500" id="last-update">Last updated: Just now</span>
            </div>
            
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr class="border-b border-gray-800/60">
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-left">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Username</span>
                            </th>
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-left">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Status</span>
                            </th>
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-left">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Last Seen</span>
                            </th>
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Command</span>
                            </th>
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Action</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/40" id="bot-table-body">
                        <!-- Data akan diisi oleh JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <script>
        // Initialize AOS
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            mirror: false,
            offset: 50,
            delay: 100,
            anchorPlacement: 'top-bottom',
            disable: false
        });
        
        let currentRespawnUser = null;
        
        // Fetch data dari API
        async function fetchBots() {
            try {
                const response = await fetch('/api/users');
                const data = await response.json();
                updateTable(data.bots);
                updateStats(data.bots);
                document.getElementById('last-update').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
            } catch (error) {
                console.error('Error fetching bots:', error);
            }
        }
        
        function updateTable(bots) {
            const tbody = document.getElementById('bot-table-body');
            
            if (bots.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="py-12 sm:py-16 text-center">
                            <div class="flex flex-col items-center gap-2 sm:gap-3">
                                <div class="w-12 h-12 sm:w-16 sm:h-16 rounded-2xl bg-gray-800/50 flex items-center justify-center">
                                    <i class="fa-solid fa-inbox text-gray-600 text-xl sm:text-2xl"></i>
                                </div>
                                <p class="text-gray-500 text-sm sm:text-base font-medium">No bots online</p>
                                <p class="text-gray-600 text-xs sm:text-sm">Waiting for bots to connect</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            let html = '';
            const now = new Date();
            
            bots.forEach((bot, index) => {
                const lastSeen = new Date(bot.last_seen);
                const diffMinutes = Math.floor((now - lastSeen) / 1000 / 60);
                const isOnline = diffMinutes < 1;
                const statusText = isOnline ? 'Online' : 'Offline';
                const statusColor = isOnline ? 'status-online' : 'status-offline';
                const statusIcon = isOnline ? 'fa-circle' : 'fa-circle';
                
                const lastSeenText = diffMinutes < 1 ? 'Just now' : 
                                    diffMinutes < 60 ? `${diffMinutes}m ago` :
                                    `${Math.floor(diffMinutes / 60)}h ${diffMinutes % 60}m ago`;
                
                html += `
                    <tr class="hover:bg-white/[0.02] transition-colors duration-200" 
                        data-username="${bot.username}"
                        data-aos="fade-up-custom" data-aos-duration="500" data-aos-delay="${index * 100}" data-aos-once="true">
                        <td class="py-3 sm:py-4 px-3 sm:px-6">
                            <div class="flex items-center gap-2 sm:gap-3">
                                <div class="w-7 h-7 sm:w-8 md:w-9 sm:h-8 md:h-9 rounded-lg bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center text-xs sm:text-sm font-medium text-white flex-shrink-0">
                                    ${bot.username.substring(0, 1).toUpperCase()}
                                </div>
                                <span class="text-white text-sm sm:text-base font-medium truncate max-w-[80px] sm:max-w-[120px] md:max-w-none">${bot.username}</span>
                            </div>
                        </td>
                        <td class="py-3 sm:py-4 px-3 sm:px-6">
                            <div class="flex items-center gap-2">
                                <i class="fa-solid ${statusIcon} text-xs ${statusColor}"></i>
                                <span class="${statusColor} text-sm font-medium">${statusText}</span>
                            </div>
                        </td>
                        <td class="py-3 sm:py-4 px-3 sm:px-6 text-sm text-gray-400">${lastSeenText}</td>
                        <td class="py-3 sm:py-4 px-3 sm:px-6 text-center">
                            <span class="px-2 py-1 rounded-lg text-xs font-medium ${bot.command === 'respawn' ? 'bg-red-500/20 text-red-400' : 'bg-gray-700/30 text-gray-400'}">
                                ${bot.command || 'none'}
                            </span>
                        </td>
                        <td class="py-3 sm:py-4 px-3 sm:px-6 text-center">
                            <button onclick="openRespawnModal('${bot.username}')" 
                                    class="w-7 h-7 sm:w-8 md:w-9 sm:h-8 md:h-9 rounded-lg bg-gray-800 hover:bg-red-500/20 hover:text-red-400 text-gray-400 flex items-center justify-center transition-all duration-200 group" 
                                    title="Respawn Bot">
                                <i class="fa-solid fa-skull text-xs sm:text-sm group-hover:scale-110 transition-transform"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            
            tbody.innerHTML = html;
            
            // Re-initialize AOS for new elements
            AOS.refresh();
        }
        
        function updateStats(bots) {
            const now = new Date();
            let online = 0, offline = 0;
            
            bots.forEach(bot => {
                const lastSeen = new Date(bot.last_seen);
                const diffMinutes = Math.floor((now - lastSeen) / 1000 / 60);
                if (diffMinutes < 1) online++;
                else offline++;
            });
            
            document.getElementById('online-count').textContent = online;
            document.getElementById('offline-count').textContent = offline;
            document.getElementById('total-count').textContent = bots.length;
        }
        
        function openRespawnModal(username) {
            currentRespawnUser = username;
            document.getElementById('respawnUsername').textContent = username;
            document.getElementById('respawnModal').classList.remove('hidden');
            document.getElementById('respawnModal').classList.add('flex');
            document.body.style.overflow = 'hidden';
        }
        
        function closeRespawnModal() {
            document.getElementById('respawnModal').classList.add('hidden');
            document.getElementById('respawnModal').classList.remove('flex');
            document.body.style.overflow = '';
            currentRespawnUser = null;
        }
        
        function confirmRespawn() {
            if (!currentRespawnUser) return;
            
            fetch('/api/respawn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: currentRespawnUser })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeRespawnModal();
                    fetchBots(); // Refresh data
                } else {
                    alert('Gagal mengirim perintah respawn');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat mengirim perintah');
            });
        }
        
        function refreshData() {
            fetchBots();
        }
        
        // Auto refresh setiap 30 detik
        setInterval(fetchBots, 30000);
        
        // Load data pertama kali
        fetchBots();
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeRespawnModal();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/inventory')
def inventory_dashboard():
    url = f"{SUPABASE_URL}/rest/v1/inventory_tracking?select=*"
    res = requests.get(url, headers=HEADERS)
    
    data = res.json() if res.status_code == 200 else []
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/api/poll', methods=['POST'])
def bot_poll():
    data = request.json or {}
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    clean_username = username.strip().lower()
    current_time = datetime.now(timezone.utc).isoformat()

    # Cek apakah user sudah terdaftar di Supabase
    check_res = requests.get(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", headers=HEADERS)
    
    if check_res.status_code == 200 and len(check_res.json()) > 0:
        # Jika ada, update last_seen saja
        requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", json={"last_seen": current_time}, headers=HEADERS)
    else:
        # Jika belum ada, daftarkan baru
        requests.post(f"{SUPABASE_URL}/rest/v1/bots", json={"username": clean_username, "last_seen": current_time, "command": "none"}, headers=HEADERS)

    # Ambil status perintah (command) saat ini
    command = "none"
    get_cmd = requests.get(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}&select=command", headers=HEADERS)
    if get_cmd.status_code == 200 and len(get_cmd.json()) > 0:
        command = get_cmd.json()[0].get('command', 'none')

    # Jika perintahnya respawn, langsung reset ke 'none' agar tidak mati berulang kali
    if command == "respawn":
        requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", json={"command": "none"}, headers=HEADERS)

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
    res = requests.patch(f"{SUPABASE_URL}/rest/v1/bots?username=eq.{clean_username}", json={"command": "respawn"}, headers=HEADERS)
    
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
    """Informasi endpoint untuk bot Roblox"""
    return jsonify({
        "poll_url": "https://roblox-teleport-script.vercel.app/api/poll",
        "method": "POST",
        "body": {"username": "your_bot_username"},
        "response": {"command": "respawn or none"}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
