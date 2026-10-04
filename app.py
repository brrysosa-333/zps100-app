import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DEL SISTEMA ---
st.set_page_config(page_title="ZPS-100 Terminal de Precisión", page_icon="🎛️", layout="wide", initial_sidebar_state="collapsed")

# --- INGENIERÍA DE INTERFAZ Y BLINDAJE ---
html_code = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>ZPS-100 Terminal</title>
    <style>
        :root {
            --bg-deep: #050711;
            --bg-card: #090e1f;
            --neon-blue: #00d2ff;
            --neon-cyan: #38bdf8;
            --neon-green: #22c55e;
            --neon-yellow: #eab308;
            --neon-red: #ef4444;
            --neon-purple: #a855f7;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --border-color: #1e3a8a;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        input.search-input, textarea {
            -webkit-user-select: text !important;
            -khtml-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }

        body {
            background-color: var(--bg-deep);
            color: var(--text-primary);
            display: flex;
            justify-content: center;
            min-height: 100vh;
            padding: 10px;
            background-image: radial-gradient(circle at 50% 50%, #0d1b3e 0%, var(--bg-deep) 90%);
            overflow-x: hidden;
        }

        .app-container {
            width: 100%;
            max-width: 420px;
            background: var(--bg-card);
            border: 1px solid var(--neon-blue);
            border-radius: 32px;
            padding: 20px;
            box-shadow: 0 0 30px rgba(0, 210, 255, 0.2), inset 0 0 15px rgba(0, 210, 255, 0.1);
            position: relative;
            display: flex;
            flex-direction: column;
            margin: 10px auto;
            height: calc(100vh - 20px);
            max-height: 900px;
        }

        .top-status-bar {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: var(--text-secondary);
            margin-bottom: 15px;
            padding: 0 5px;
            opacity: 0.7;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 10px 15px;
            margin-bottom: 15px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .avatar {
            width: 32px;
            height: 32px;
            background: #1e293b;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px solid var(--neon-cyan);
            font-size: 16px;
            color: var(--neon-cyan);
            box-shadow: 0 0 5px var(--neon-cyan);
        }

        .title-group h1 {
            font-size: 13px;
            letter-spacing: 0.5px;
            color: var(--text-primary);
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        }

        .title-group p {
            font-size: 9px;
            color: var(--neon-cyan);
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .live-badge {
            font-size: 9px;
            background: rgba(34, 197, 94, 0.15);
            color: var(--neon-green);
            padding: 4px 8px;
            border-radius: 10px;
            border: 1px solid var(--neon-green);
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: bold;
            box-shadow: 0 0 8px rgba(34, 197, 94, 0.3);
        }

        .live-dot {
            width: 6px;
            height: 6px;
            background: var(--neon-green);
            border-radius: 50%;
            box-shadow: 0 0 6px var(--neon-green);
        }

        .search-form {
            width: 100%;
            display: flex;
            align-items: center;
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            margin-bottom: 15px;
            padding-right: 8px;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        .search-form:focus-within {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }

        .search-input {
            flex: 1;
            background: transparent;
            border: none;
            padding: 12px 15px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
        }

        .search-input::placeholder {
            color: var(--text-secondary);
            opacity: 0.6;
        }

        .search-button {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 8px;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.7;
        }

        .search-button:hover {
            color: var(--neon-cyan);
            opacity: 1;
        }

        #search-feedback {
            font-size: 10px;
            color: var(--neon-cyan);
            margin-bottom: 10px;
            text-align: center;
            display: none;
            text-shadow: 0 0 5px var(--neon-cyan);
            font-weight: bold;
        }

        .tabs {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 11px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
        }

        .tab {
            color: var(--text-secondary);
            cursor: pointer;
            padding-bottom: 6px;
            position: relative;
            transition: color 0.3s;
        }

        .tab.active {
            color: var(--neon-cyan);
            font-weight: bold;
        }

        .tab.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--neon-cyan);
            box-shadow: 0 0 8px var(--neon-cyan);
        }

        .section-title {
            font-size: 10px;
            color: var(--neon-cyan);
            margin-bottom: 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
            text-shadow: 0 0 5px var(--neon-cyan);
        }

        .tracks-wrapper {
            flex: 1;
            overflow-y: auto;
            padding-right: 5px;
            margin-right: -5px;
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) var(--bg-deep);
        }

        .tracks-wrapper::-webkit-scrollbar {
            width: 6px;
        }

        .tracks-wrapper::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 3px;
        }

        .track-card {
            background: var(--bg-card);
            border: 1px solid var(--neon-blue);
            border-radius: 18px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: 0 0 8px rgba(59, 130, 246, 0.15);
            transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s;
        }

        .track-card.found {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
            transform: scale(1.02);
        }

        .track-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 6px;
        }

        .indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .indicator.green { background: var(--neon-green); box-shadow: 0 0 8px var(--neon-green); }
        .indicator.yellow { background: var(--neon-yellow); box-shadow: 0 0 8px var(--neon-yellow); }
        .indicator.purple { background: var(--neon-purple); box-shadow: 0 0 8px var(--neon-purple); }

        .track-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            font-size: 10px;
            color: var(--text-secondary);
            margin-bottom: 6px;
            text-align: left;
        }

        .track-metrics span:nth-child(4),
        .track-metrics span:nth-child(5),
        .track-metrics span:nth-child(6) {
            color: var(--text-primary);
            font-weight: bold;
        }

        .progress-bar-container {
            width: 100%;
            height: 14px;
            background: #020617;
            border-radius: 7px;
            border: 1px solid var(--border-color);
            overflow: hidden;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .progress-fill {
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            opacity: 0.4;
        }

        .progress-fill.green { background: var(--neon-green); }
        .progress-fill.yellow { background: var(--neon-yellow); }
        .progress-fill.red { background: var(--neon-red); }
        .progress-fill.purple { background: var(--neon-purple); }

        .progress-text {
            position: relative;
            z-index: 2;
            font-size: 9px;
            font-weight: bold;
            color: var(--text-primary);
            text-shadow: 0 0 3px rgba(0,0,0,0.5);
        }

        .footer-nav {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
            font-size: 10px;
            color: var(--text-secondary);
            opacity: 0.9;
        }

        .footer-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            transition: color 0.3s;
        }

        .footer-item:hover {
            color: var(--neon-cyan);
        }
    </style>
</head>
<body>

    <div class="app-container">
        <div class="top-status-bar">
            <span>9:28</span>
            <span>🛜 🔋 4G</span>
        </div>

        <div class="header">
            <div class="user-info">
                <div class="avatar">👤</div>
                <div class="title-group">
                    <h1>ZPS-100</h1>
                    <p>Terminal de Precisión</p>
                </div>
            </div>
            <div class="live-badge">
                <div class="live-dot"></div> EN VIVO
            </div>
        </div>

        <form class="search-form" id="search-form">
            <input type="text" class="search-input" id="search-input" placeholder="🔍 Buscar pista exacta (ej. Yastremska, NFL)..." autocomplete="off">
            <button type="submit" class="search-button" aria-label="Buscar">🔍</button>
        </form>
        
        <div id="search-feedback"></div>

        <div class="tabs">
            <span class="tab active" id="tab-activas">📊 ACTIVAS</span>
            <span class="tab" id="tab-pendientes">⏳ PENDIENTES</span>
            <span class="tab" id="tab-historial">📂 HISTORIAL</span>
        </div>

        <div class="section-title">🎵 PISTAS ACTIVAS (SWEET SPOT: 68% - 75%)</div>

        <div class="tracks-wrapper" id="tracks-container">
            <div class="track-card" data-track-name="Dayana Yastremska WTA">
                <div class="track-header"><div class="indicator green"></div> 1. Dayana Yastremska (WTA)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>$0.00</span><span>$2.00</span><span>$9.17</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill green" style="width: 72%;"></div>
                    <span class="progress-text">72%</span>
                </div>
            </div>

            <div class="track-card" data-track-name="Naoya Honda ATP">
                <div class="track-header"><div class="indicator green"></div> 2. Naoya Honda (ATP)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>$0.00</span><span>$6.00</span><span>$8.17</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill green" style="width: 66%;"></div>
                    <span class="progress-text">66%</span>
                </div>
            </div>

            <div class="track-card" data-track-name="Julieta Pareja ITF">
                <div class="track-header"><div class="indicator yellow"></div> 3. Julieta Pareja (ITF)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>-Cato $.00</span><span>-$1.19</span><span>-$1.19</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill red" style="width: 75%;"></div>
                    <span class="progress-text">75%</span>
                </div>
            </div>

            <div class="track-card" data-track-name="SEA Seahawks NFL">
                <div class="track-header"><div class="indicator green"></div> 4. SEA Seahawks (NFL)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>-Cato $.00</span><span>$4.00</span><span>$9.41</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill green" style="width: 66%;"></div>
                    <span class="progress-text">66%</span>
                </div>
            </div>

            <div class="track-card" data-track-name="Combo ATP Beijing Medvedev Zverev">
                <div class="track-header"><div class="indicator purple"></div> 5. Combo ATP Beijing</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>-Cato $.00</span><span>$6.00</span><span>$7.12</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill purple" style="width: 75%;"></div>
                    <span class="progress-text">75%</span>
                </div>
            </div>
        </div>

        <footer class="footer-nav">
            <div class="footer-item"><span>≡</span> Menú</div>
            <div class="footer-item"><span>🔄</span> Sync</div>
            <div class="footer-item"><span>➕</span> Nueva</div>
            <div class="footer-item"><span>⚙</span> Ajustes</div>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const searchForm = document.getElementById('search-form');
            const searchInput = document.getElementById('search-input');
            const tracksContainer = document.getElementById('tracks-container');
            const trackCards = tracksContainer.querySelectorAll('.track-card');
            const searchFeedback = document.getElementById('search-feedback');

            function performSearch() {
                const query = searchInput.value.toLowerCase().trim();
                let foundCount = 0;

                trackCards.forEach(card => {
                    const trackName = card.getAttribute('data-track-name').toLowerCase();
                    if (trackName.includes(query)) {
                        card.style.display = 'block';
                        card.classList.add('found');
                        foundCount++;
                    } else {
                        card.style.display = 'none';
                        card.classList.remove('found');
                    }
                });

                if (query === '') {
                    searchFeedback.style.display = 'none';
                    trackCards.forEach(card => card.style.display = 'block');
                } else {
                    searchFeedback.textContent = `🔍 ${foundCount} coincidencia${foundCount === 1 ? '' : 's'} para: "${query}"`;
                    searchFeedback.style.display = 'block';
                }
                tracksContainer.scrollTop = 0;
            }

            searchForm.addEventListener('submit', function(e) {
                e.preventDefault();
                performSearch();
                searchInput.blur();
            });

            const appContainer = document.querySelector('.app-container');
            ['copy', 'cut', 'paste'].forEach(event => {
                appContainer.addEventListener(event, (e) => e.preventDefault());
            });

            appContainer.addEventListener('contextmenu', (e) => {
                if (e.target !== searchInput) {
                    e.preventDefault();
                }
            }, false);
            
            appContainer.addEventListener('selectstart', (e) => {
                if (e.target !== searchInput) {
                    e.preventDefault();
                }
            }, false);
            
            searchInput.addEventListener('focus', function() {
                this.select();
            });
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
