import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DEL SISTEMA ---
st.set_page_config(page_title="ZPS-100 Terminal de Precisión", page_icon="🎛️", layout="wide", initial_sidebar_state="collapsed")

# --- INGENIERÍA DE INTERFAZ Y BLINDAJE ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <!-- Meta tags para hacerla inmersiva en móvil y bloquear zoom/escalado -->
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
            /* --- INGENIERÍA UX: BLOQUEO TOTAL DE COPIAR/PEGAR Y RESALTADO --- */
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Permitir selección solo DENTRO del input de búsqueda */
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
            padding: 10px; /* Padding reducido para aprovechar pantalla */
            background-image: radial-gradient(circle at 50% 50%, #0d1b3e 0%, var(--bg-deep) 90%);
            overflow-x: hidden;
            padding-top: env(safe-area-inset-top);
            padding-bottom: env(safe-area-inset-bottom);
        }

        .app-container {
            width: 100%;
            max-width: 420px; /* Ancho ligeramente más compacto y profesional */
            background: var(--bg-card);
            border: 1px solid var(--neon-blue);
            border-radius: 32px; /* Esquinas ligeramente menos redondeadas para look más serio */
            padding: 20px;
            box-shadow: 0 0 30px rgba(0, 210, 255, 0.2), inset 0 0 15px rgba(0, 210, 255, 0.1);
            position: relative;
            display: flex;
            flex-direction: column;
            margin-top: 10px;
            margin-bottom: 10px;
            height: calc(100vh - 20px); /* Ocupa casi todo el alto disponible */
            max-height: 900px; /* Altura máxima para tablets/laptops */
        }

        /* Barra de estado simulada (más minimalista) */
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

        /* --- INGENIERÍA BUSCADOR: AHORA ES FORMULARIO FUNCIONAL --- */
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

        /* Feedback visual de búsqueda */
        #search-feedback {
            font-size: 10px;
            color: var(--neon-cyan);
            margin-bottom: 10px;
            text-align: center;
            display: none; /* Oculto por defecto */
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

        .tab:hover {
            color: var(--neon-cyan);
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

        /* Contenedor scrolleable de las tarjetas */
        .tracks-wrapper {
            flex: 1;
            overflow-y: auto;
            padding-right: 5px;
            margin-right: -5px;
            /* Scrollbar personalizado */
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) var(--bg-deep);
        }

        .tracks-wrapper::-webkit-scrollbar {
            width: 6px;
        }

        .tracks-wrapper::-webkit-scrollbar-track {
            background: var(--bg-deep);
        }

        .tracks-wrapper::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 3px;
        }

        .tracks-wrapper::-webkit-scrollbar-thumb:hover {
            background: var(--neon-blue);
        }

        .track-card {
            background: var(--bg-card);
            border: 1px solid var(--neon-blue); /* Borde base más fino */
            border-radius: 18px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: 0 0 8px rgba(59, 130, 246, 0.15);
            transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s;
            cursor: default; /* Cursor por defecto, no de puntero */
        }

        /* Estado de tarjeta encontrada por búsqueda */
        .track-card.found {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
            /* Pequeño efecto de escala al encontrar */
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

        .track-metrics span:nth-child(4), /* Valores de la 2da fila */
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
            opacity: 0.4; /* Un poco más translúcido para el neón */
            transition: width 0.5s ease-out;
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
        <!-- Barra de estado superior (imita la del móvil) -->
        <div class="top-status-bar">
            <span>9:26</span>
            <span>🛜 🔋 4G</span>
        </div>

        <!-- Cabecera de la App -->
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

        <!-- --- INGENIERÍA BUSCADOR: FORMULARIO FUNCIONAL --- -->
        <form class="search-form" id="search-form">
            <input type="text" class="search-input" id="search-input" placeholder="🔍 Buscar pista exacta (ej. Yastremska, NFL)..." autocomplete="off">
            <button type="submit" class="search-button" aria-label="Buscar">🔍</button>
        </form>
        
        <!-- Feedback de búsqueda -->
        <div id="search-feedback"></div>

        <div class="tabs">
            <span class="tab active" id="tab-activas">📊 ACTIVAS</span>
            <span class="tab" id="tab-pendientes">⏳ PENDIENTES</span>
            <span class="tab" id="tab-historial">📂 HISTORIAL</span>
        </div>

        <div class="section-title">🎵 PISTAS ACTIVAS (SWEET SPOT: 68% - 75%)</div>

        <!-- Contenedor scrolleable -->
        <div class="tracks-wrapper" id="tracks-container">
            
            <!-- Pista 1 -->
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

            <!-- Pista 2 -->
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

            <!-- Pista 3 -->
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

            <!-- Pista 4 -->
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

            <!-- Pista 5 -->
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
            
            <!-- Añadimos unas tarjetas más de ejemplo para probar el scroll -->
            <div class="track-card" data-track-name="Daniil Medvedev ATP">
                <div class="track-header"><div class="indicator green"></div> 6. Daniil Medvedev (ATP)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>$0.00</span><span>$5.00</span><span>$8.90</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill green" style="width: 78%;"></div>
                    <span class="progress-text">78%</span>
                </div>
            </div>
             <div class="track-card" data-track-name="Aryna Sabalenka WTA">
                <div class="track-header"><div class="indicator yellow"></div> 7. Aryna Sabalenka (WTA)</div>
                <div class="track-metrics">
                    <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                    <span>-Cato $.00</span><span>-$2.00</span><span>-$2.00</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fill red" style="width: 70%;"></div>
                    <span class="progress-text">70%</span>
                </div>
            </div>

        </div> <!-- Fin tracks-wrapper -->

        <!-- Menú Inferior de Estudio -->
        <footer class="footer-nav">
            <div class="footer-item"><span>≡</span> Menú</div>
            <div class="footer-item"><span>🔄</span> Sync</div>
            <div class="footer-item"><span>➕</span> Nueva</div>
            <div class="footer-item"><span>⚙</span> Ajustes</div>
        </footer>
    </div>

    <!-- --- INGENIERÍA JAVASCRIPT: BÚSQUEDA INTERNA Y BLOQUEO GLOBAL --- -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const searchForm = document.getElementById('search-form');
            const searchInput = document.getElementById('search-input');
            const tracksContainer = document.getElementById('tracks-container');
            const trackCards = tracksContainer.querySelectorAll('.track-card');
            const search
