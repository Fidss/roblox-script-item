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

# Template HTML responsive dengan animasi sekali jalan
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
        .item-image {
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
            transition: transform 0.3s ease, filter 0.3s ease;
        }
        .item-image:hover {
            transform: scale(1.1);
            filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.5)) brightness(1.1);
        }
        
        /* Custom AOS animations */
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
        
        [data-aos="flip-left-custom"] {
            opacity: 0;
            transform: perspective(400px) rotateY(-20deg);
            transition: opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        [data-aos="flip-left-custom"].aos-animate {
            opacity: 1;
            transform: perspective(400px) rotateY(0);
        }
        
        /* Pulse animation for stats */
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.1); }
            50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
        }
        
        .stats-card {
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        /* Responsive table */
        .table-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
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
        
        /* Responsive adjustments */
        @media (max-width: 640px) {
            .value-badge {
                padding: 0.25rem 0.5rem;
                font-size: 0.75rem;
            }
            
            .item-image-small {
                width: 1rem !important;
                height: 1rem !important;
            }
        }
        
        @media (max-width: 480px) {
            .stats-card .item-image {
                width: 2.5rem !important;
                height: 2.5rem !important;
            }
        }
    </style>
</head>
<body class="bg-[#0a0a0f] min-h-screen font-poppins">
    <!-- Background Gradient Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse" style="animation-duration: 8s;"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" style="animation-duration: 10s;"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/5 rounded-full blur-3xl animate-pulse" style="animation-duration: 12s;"></div>
    </div>

    <!-- Edit Modal -->
    <div id="editModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick="closeEditModal()"></div>
        <div class="relative bg-[#12121a] border border-gray-800/60 rounded-2xl p-4 sm:p-6 w-full max-w-md shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-4 sm:mb-6">
                <h3 class="text-base sm:text-lg font-semibold text-white flex items-center gap-2">
                    <i class="fa-solid fa-pen-to-square text-blue-400"></i>
                    Edit Inventory
                </h3>
                <button onclick="closeEditModal()" class="text-gray-500 hover:text-white transition-colors">
                    <i class="fa-solid fa-xmark text-xl"></i>
                </button>
            </div>
            
            <div class="mb-3 sm:mb-4">
                <label class="block text-gray-400 text-xs sm:text-sm mb-1.5 sm:mb-2">Username</label>
                <input type="text" id="editUsername" disabled 
                       class="w-full bg-[#0a0a0f] border border-gray-700 rounded-xl px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-gray-400 font-medium">
            </div>
            
            <div class="space-y-3 sm:space-y-4 mb-4 sm:mb-6">
                <div>
                    <label class="block text-gray-400 text-xs sm:text-sm mb-1.5 sm:mb-2 flex items-center gap-2">
                        <img src="https://i.ibb.co.com/qMgYjNyS/no-Filter-1.png" alt="Elshark" class="w-6 h-6 sm:w-8 sm:h-8 object-contain item-image">
                        <span class="truncate">Elshark Gran Maja</span>
                    </label>
                    <div class="flex items-center gap-1.5 sm:gap-2">
                        <button onclick="decrementValue('editElshark')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-minus text-xs sm:text-sm"></i>
                        </button>
                        <input type="number" id="editElshark" min="0" 
                               class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-white text-center font-medium focus:border-blue-500 focus:outline-none min-w-0">
                        <button onclick="incrementValue('editElshark')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-plus text-xs sm:text-sm"></i>
                        </button>
                    </div>
                </div>
                
                <div>
                    <label class="block text-gray-400 text-xs sm:text-sm mb-1.5 sm:mb-2 flex items-center gap-2">
                        <img src="https://i.ibb.co.com/kVzGR565/no-Filter.png" alt="Gladiator" class="w-6 h-6 sm:w-8 sm:h-8 object-contain item-image">
                        <span class="truncate">Gladiator Shark</span>
                    </label>
                    <div class="flex items-center gap-1.5 sm:gap-2">
                        <button onclick="decrementValue('editGladiator')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-minus text-xs sm:text-sm"></i>
                        </button>
                        <input type="number" id="editGladiator" min="0" 
                               class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-white text-center font-medium focus:border-purple-500 focus:outline-none min-w-0">
                        <button onclick="incrementValue('editGladiator')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-plus text-xs sm:text-sm"></i>
                        </button>
                    </div>
                </div>
                
                <div>
                    <label class="block text-gray-400 text-xs sm:text-sm mb-1.5 sm:mb-2 flex items-center gap-2">
                        <img src="https://i.ibb.co.com/bMhfSHw4/no-Filter-2.png" alt="Enchant Stone" class="w-6 h-6 sm:w-8 sm:h-8 object-contain item-image">
                        <span class="truncate">Evolved Enchant Stone</span>
                    </label>
                    <div class="flex items-center gap-1.5 sm:gap-2">
                        <button onclick="decrementValue('editStone')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-minus text-xs sm:text-sm"></i>
                        </button>
                        <input type="number" id="editStone" min="0" 
                               class="flex-1 bg-[#0a0a0f] border border-gray-700 rounded-xl px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-white text-center font-medium focus:border-amber-500 focus:outline-none min-w-0">
                        <button onclick="incrementValue('editStone')" 
                                class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gray-800 hover:bg-gray-700 text-white flex items-center justify-center transition-colors flex-shrink-0">
                            <i class="fa-solid fa-plus text-xs sm:text-sm"></i>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="flex gap-2 sm:gap-3">
                <button onclick="closeEditModal()" 
                        class="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl border border-gray-700 text-gray-400 text-sm sm:text-base font-medium hover:bg-gray-800 transition-colors">
                    Cancel
                </button>
                <button onclick="saveEdit()" 
                        class="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm sm:text-base font-medium hover:from-blue-600 hover:to-blue-700 transition-all shadow-lg shadow-blue-500/25">
                    <i class="fa-solid fa-check mr-1 sm:mr-2"></i> Save
                </button>
            </div>
        </div>
    </div>

    <div class="relative max-w-6xl mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-10">
        <!-- Header Section -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-6 mb-6 sm:mb-10" 
             data-aos="fade-down" data-aos-duration="800" data-aos-easing="ease-out-cubic" data-aos-once="true">
            <div class="space-y-1">
                <div class="flex items-center gap-2 sm:gap-3">
                    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25 flex-shrink-0"
                         data-aos="zoom-in" data-aos-duration="600" data-aos-delay="200" data-aos-once="true">
                        <i class="fa-solid fa-gem text-white text-sm sm:text-lg"></i>
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-semibold text-white tracking-tight" 
                        data-aos="fade-right" data-aos-duration="600" data-aos-delay="400" data-aos-once="true">
                        Gemstones<span class="text-blue-400">Hub</span>
                    </h1>
                </div>
                <p class="text-gray-500 text-xs sm:text-sm ml-10 sm:ml-13" 
                   data-aos="fade-up" data-aos-duration="600" data-aos-delay="600" data-aos-once="true">
                    Inventory tracking dashboard
                </p>
            </div>
            
            <button onclick="resetData()" 
                    class="group flex items-center gap-2 px-4 sm:px-5 py-2.5 sm:py-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 font-medium text-xs sm:text-sm hover:bg-red-500/20 hover:border-red-500/40 transition-all duration-300 w-full sm:w-auto justify-center"
                    data-aos="fade-left" data-aos-duration="600" data-aos-delay="400" data-aos-once="true">
                <i class="fa-solid fa-rotate-left group-hover:-translate-x-1 transition-transform duration-300"></i>
                <span>Reset Data</span>
            </button>
        </div>

        <!-- Stats Overview Cards -->
        <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-5 mb-6 sm:mb-10">
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-blue-500/30 transition-all duration-300 group stats-card"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="100" data-aos-once="true">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-blue-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <img src="https://i.ibb.co.com/qMgYjNyS/no-Filter-1.png" alt="Elshark" class="w-full h-full object-contain item-image">
                    </div>
                    <div class="min-w-0">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Elshark Gran Maja</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="total-shark">-</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-purple-500/30 transition-all duration-300 group stats-card"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="300" data-aos-once="true"
                 style="animation-delay: 0.5s;">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-purple-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <img src="https://i.ibb.co.com/kVzGR565/no-Filter.png" alt="Gladiator" class="w-full h-full object-contain item-image">
                    </div>
                    <div class="min-w-0">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Gladiator Shark</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="total-gladiator">-</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl p-3 sm:p-5 hover:border-amber-500/30 transition-all duration-300 group stats-card xs:col-span-2 sm:col-span-1"
                 data-aos="flip-left" data-aos-duration="800" data-aos-delay="500" data-aos-once="true"
                 style="animation-delay: 1s;">
                <div class="flex items-center gap-3 sm:gap-4">
                    <div class="w-10 h-10 sm:w-12 md:w-14 sm:h-12 md:h-14 rounded-xl bg-amber-500/10 flex items-center justify-center p-1.5 sm:p-2 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                        <img src="https://i.ibb.co.com/bMhfSHw4/no-Filter-2.png" alt="Enchant Stone" class="w-full h-full object-contain item-image">
                    </div>
                    <div class="min-w-0">
                        <p class="text-gray-500 text-[10px] xs:text-xs uppercase tracking-wider truncate">Enchant Stone</p>
                        <p class="text-lg sm:text-xl md:text-2xl font-semibold text-white mt-0.5 sm:mt-1 tabular-nums" id="total-stone">-</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Table Section -->
        <div class="bg-[#12121a] border border-gray-800/60 rounded-2xl overflow-hidden"
             data-aos="fade-up" data-aos-duration="800" data-aos-delay="200" data-aos-once="true">
            <div class="px-4 sm:px-6 py-3 sm:py-5 border-b border-gray-800/60">
                <h2 class="text-base sm:text-lg font-medium text-white flex items-center gap-2">
                    <i class="fa-solid fa-users text-gray-400"></i>
                    Player Inventory
                </h2>
            </div>
            
            <div class="table-container">
                <table class="w-full min-w-[600px] md:min-w-full">
                    <thead>
                        <tr class="border-b border-gray-800/60">
                            <th class="py-3 sm:py-4 px-3 sm:px-6 text-left">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Player</span>
                            </th>
                            <th class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider flex items-center justify-center gap-1 sm:gap-1.5">
                                    <img src="https://i.ibb.co.com/qMgYjNyS/no-Filter-1.png" alt="Elshark" class="w-4 h-4 sm:w-5 md:w-6 sm:h-5 md:h-6 object-contain item-image flex-shrink-0">
                                    <span class="hidden xs:inline">Elshark</span>
                                </span>
                            </th>
                            <th class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider flex items-center justify-center gap-1 sm:gap-1.5">
                                    <img src="https://i.ibb.co.com/kVzGR565/no-Filter.png" alt="Gladiator" class="w-4 h-4 sm:w-5 md:w-6 sm:h-5 md:h-6 object-contain item-image flex-shrink-0">
                                    <span class="hidden xs:inline">Gladiator</span>
                                </span>
                            </th>
                            <th class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider flex items-center justify-center gap-1 sm:gap-1.5">
                                    <img src="https://i.ibb.co.com/bMhfSHw4/no-Filter-2.png" alt="Stone" class="w-4 h-4 sm:w-5 md:w-6 sm:h-5 md:h-6 object-contain item-image flex-shrink-0">
                                    <span class="hidden xs:inline">Stone</span>
                                </span>
                            </th>
                            <th class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <span class="text-gray-500 text-[10px] xs:text-xs font-medium uppercase tracking-wider">Action</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/40">
                        {% for row in data %}
                        <tr class="hover:bg-white/[0.02] transition-colors duration-200" 
                            data-username="{{ row.username }}"
                            data-aos="fade-up-custom" data-aos-duration="500" data-aos-delay="{{ loop.index * 100 }}" data-aos-once="true">
                            <td class="py-3 sm:py-4 px-3 sm:px-6">
                                <div class="flex items-center gap-2 sm:gap-3">
                                    <div class="w-7 h-7 sm:w-8 md:w-9 sm:h-8 md:h-9 rounded-lg bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center text-xs sm:text-sm font-medium text-white flex-shrink-0">
                                        {{ row.username[:1].upper() }}
                                    </div>
                                    <span class="text-white text-sm sm:text-base font-medium truncate max-w-[80px] sm:max-w-[120px] md:max-w-none">{{ row.username }}</span>
                                </div>
                            </td>
                            <td class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <div class="value-badge bg-blue-500/10 text-blue-400">
                                    <img src="https://i.ibb.co.com/qMgYjNyS/no-Filter-1.png" alt="Elshark" class="w-4 h-4 sm:w-5 sm:h-5 object-contain item-image flex-shrink-0">
                                    <span class="item-value tabular-nums" data-field="elshark_gran_maja">{{ row.elshark_gran_maja }}</span>
                                </div>
                            </td>
                            <td class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <div class="value-badge bg-purple-500/10 text-purple-400">
                                    <img src="https://i.ibb.co.com/kVzGR565/no-Filter.png" alt="Gladiator" class="w-4 h-4 sm:w-5 sm:h-5 object-contain item-image flex-shrink-0">
                                    <span class="item-value tabular-nums" data-field="gladiator_shark">{{ row.gladiator_shark }}</span>
                                </div>
                            </td>
                            <td class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <div class="value-badge bg-amber-500/10 text-amber-400">
                                    <img src="https://i.ibb.co.com/bMhfSHw4/no-Filter-2.png" alt="Stone" class="w-4 h-4 sm:w-5 sm:h-5 object-contain item-image flex-shrink-0">
                                    <span class="item-value tabular-nums" data-field="evolved_enchant_stone">{{ row.evolved_enchant_stone }}</span>
                                </div>
                            </td>
                            <td class="py-3 sm:py-4 px-2 sm:px-4 md:px-6 text-center">
                                <button onclick="openEditModal('{{ row.username }}', {{ row.elshark_gran_maja }}, {{ row.gladiator_shark }}, {{ row.evolved_enchant_stone }})" 
                                        class="w-7 h-7 sm:w-8 md:w-9 sm:h-8 md:h-9 rounded-lg bg-gray-800 hover:bg-blue-500/20 hover:text-blue-400 text-gray-400 flex items-center justify-center transition-all duration-200 group">
                                    <i class="fa-solid fa-pen-to-square text-xs sm:text-sm group-hover:scale-110 transition-transform"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                        
                        {% if not data %}
                        <tr>
                            <td colspan="5" class="py-12 sm:py-16 text-center">
                                <div class="flex flex-col items-center gap-2 sm:gap-3">
                                    <div class="w-12 h-12 sm:w-16 sm:h-16 rounded-2xl bg-gray-800/50 flex items-center justify-center">
                                        <i class="fa-solid fa-inbox text-gray-600 text-xl sm:text-2xl"></i>
                                    </div>
                                    <p class="text-gray-500 text-sm sm:text-base font-medium">No data yet</p>
                                    <p class="text-gray-600 text-xs sm:text-sm">Start tracking your inventory items</p>
                                </div>
                            </td>
                        </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <script>
        // Initialize AOS with once: true untuk animasi sekali jalan
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
        
        let currentEditingUser = null;

        function openEditModal(username, elshark, gladiator, stone) {
            currentEditingUser = username;
            document.getElementById('editUsername').value = username;
            document.getElementById('editElshark').value = elshark;
            document.getElementById('editGladiator').value = gladiator;
            document.getElementById('editStone').value = stone;
            document.getElementById('editModal').classList.remove('hidden');
            document.getElementById('editModal').classList.add('flex');
            document.body.style.overflow = 'hidden';
        }

        function closeEditModal() {
            document.getElementById('editModal').classList.add('hidden');
            document.getElementById('editModal').classList.remove('flex');
            document.body.style.overflow = '';
            currentEditingUser = null;
        }

        function incrementValue(elementId) {
            const input = document.getElementById(elementId);
            input.value = parseInt(input.value) + 1;
        }

        function decrementValue(elementId) {
            const input = document.getElementById(elementId);
            const newValue = parseInt(input.value) - 1;
            input.value = newValue >= 0 ? newValue : 0;
        }

        function saveEdit() {
            if (!currentEditingUser) return;

            const updatedData = {
                username: currentEditingUser,
                elshark_gran_maja: parseInt(document.getElementById('editElshark').value),
                gladiator_shark: parseInt(document.getElementById('editGladiator').value),
                evolved_enchant_stone: parseInt(document.getElementById('editStone').value)
            };

            fetch('/api/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const row = document.querySelector(`tr[data-username="${currentEditingUser}"]`);
                    if (row) {
                        const valueSpans = row.querySelectorAll('.item-value');
                        valueSpans[0].textContent = updatedData.elshark_gran_maja;
                        valueSpans[1].textContent = updatedData.gladiator_shark;
                        valueSpans[2].textContent = updatedData.evolved_enchant_stone;
                        
                        // Animate updated values
                        valueSpans.forEach(span => {
                            span.style.transform = 'scale(1.3)';
                            span.style.transition = 'transform 0.3s ease';
                            setTimeout(() => {
                                span.style.transform = 'scale(1)';
                            }, 300);
                        });
                    }
                    updateTotals();
                    closeEditModal();
                } else {
                    alert('Failed to update data');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while saving');
            });
        }

        function updateTotals() {
            const rows = document.querySelectorAll('tbody tr[data-username]');
            let totalShark = 0, totalGladiator = 0, totalStone = 0;
            
            rows.forEach(row => {
                const valueSpans = row.querySelectorAll('.item-value');
                if (valueSpans.length >= 3) {
                    totalShark += parseInt(valueSpans[0].textContent.trim()) || 0;
                    totalGladiator += parseInt(valueSpans[1].textContent.trim()) || 0;
                    totalStone += parseInt(valueSpans[2].textContent.trim()) || 0;
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

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeEditModal();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
