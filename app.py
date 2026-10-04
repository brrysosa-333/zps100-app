<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZPS-100 Terminal de Precisión</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: #050711;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            background-image: radial-gradient(circle at 50% 50%, #0d1b3e 0%, #050711 80%);
        }

        .phone-container {
            width: 380px;
            background: #090e1f;
            border: 2px solid #00d2ff;
            border-radius: 40px;
            padding: 20px 15px;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.4), inset 0 0 15px rgba(0, 210, 255, 0.2);
            position: relative;
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #8a99ad;
            margin-bottom: 15px;
            padding: 0 5px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid #1e293b;
            border-radius: 15px;
            padding: 12px;
            margin-bottom: 15px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .avatar {
            width: 36px;
            height: 36px;
            background: #1e293b;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px solid #38bdf8;
        }

        .title-group h1 {
            font-size: 14px;
            letter-spacing: 0.5px;
            color: #ffffff;
        }

        .title-group p {
            font-size: 10px;
            color: #38bdf8;
            font-weight: bold;
        }

        .live-badge {
            font-size: 10px;
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            padding: 3px 8px;
            border-radius: 10px;
            border: 1px solid #22c55e;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .live-dot {
            width: 6px;
            height: 6px;
            background: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 6px #22c55e;
        }

        .search-box {
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid #1e3a8a;
            border-radius: 12px;
            padding: 10px 14px;
            color: #94a3b8;
            font-size: 12px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tabs {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 12px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 8px;
        }

        .tab {
            color: #64748b;
            cursor: pointer;
        }

        .tab.active {
            color: #38bdf8;
            font-weight: bold;
            border-bottom: 2px solid #38bdf8;
            padding-bottom: 6px;
        }

        .section-title {
            font-size: 11px;
            color: #38bdf8;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }

        .track-card {
            background: rgba(13, 20, 38, 0.9);
            border: 1px solid #3b82f6;
            border-radius: 16px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
        }

        .track-header {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .indicator.green { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
        .indicator.yellow { background: #eab308; box-shadow: 0 0 6px #eab308; }
        .indicator.purple { background: #a855f7; box-shadow: 0 0 6px #a855f7; }
        .indicator.red { background: #ef4444; box-shadow: 0 0 6px #ef4444; }

        .track-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            font-size: 10px;
            color: #94a3b8;
            margin-bottom: 6px;
            text-align: left;
        }

        .track-metrics span:nth-child(2), .track-metrics span:nth-child(5),
        .track-metrics span:nth-child(3), .track-metrics span:nth-child(6) {
            color: #ffffff;
        }

        .progress-bar-container {
            width: 100%;
            height: 16px;
            background: #020617;
            border-radius: 8px;
            border: 1px solid #1e3a8a;
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
            opacity: 0.35;
        }

        .progress-fill.green { background: #22c55e; width: 72%; }
        .progress-fill.yellow { background: #eab308; width: 66%; }
        .progress-fill.red { background: #ef4444; width: 75%; }
        .progress-fill.purple { background: #3b82f6; width: 75%; }

        .progress-text {
            position: relative;
            z-index: 2;
            font-size: 10px;
            font-weight: bold;
            color: #ffffff;
        }

        .footer-nav {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
            padding-top: 12px;
            border-top: 1px solid #1e293b;
            font-size: 10px;
            color: #94a3b8;
        }

        .footer-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            cursor: pointer;
        }

        .footer-item:hover {
            color: #38bdf8;
        }
    </style>
</head>
<body>

    <div class="phone-container">
        <!-- Barra superior móvil -->
        <div class="status-bar">
            <span>8:05</span>
            <span>📶 🛜 🔋 4G</span>
        </div>

        <!-- Cabecera de la App -->
        <div class="header">
            <div class="user-info">
                <div class="avatar">👤</div>
                <div class="title-group">
                    <h1>ZPS-100</h1>
                    <p>TERMINAL DE PRECISIÓN</p>
                </div>
            </div>
            <div class="live-badge">
                <div class="live-dot"></div> EN VIVO
            </div>
        </div>

        <!-- Buscador exacto -->
        <div class="search-box">
            🔍 Buscar pista exacta (ej. Yastremska, NFL)...
        </div>

        <!-- Pestañas -->
        <div class="tabs">
            <span class="tab active">📊 ACTIVAS</span>
            <span class="tab">⏳ PENDIENTES</span>
            <span class="tab">📂 HISTORIAL</span>
        </div>

        <div class="section-title">🎵 PISTAS ACTIVAS (SWEET SPOT: 68% - 75%)</div>

        <!-- Pista 1 -->
        <div class="track-card">
            <div class="track-header">
                <div class="indicator green"></div> 1. Dayana Yastremska (WTA)
            </div>
            <div class="track-metrics">
                <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                <span>$0.00</span><span>$2.00</span><span>$9.17</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-fill green"></div>
                <span class="progress-text">72%</span>
            </div>
        </div>

        <!-- Pista 2 -->
        <div class="track-card">
            <div class="track-header">
                <div class="indicator green"></div> 2. Naoya Honda (ATP)
            </div>
            <div class="track-metrics">
                <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                <span>$0.00</span><span>$6.00</span><span>$8.17</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-fill green"></div>
                <span class="progress-text">66%</span>
            </div>
        </div>

        <!-- Pista 3 -->
        <div class="track-card">
            <div class="track-header">
                <div class="indicator yellow"></div> 3. Julieta Pareja (ITF)
            </div>
            <div class="track-metrics">
                <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                <span>-Cato $.00</span><span>-$1.19</span><span>-$1.19</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-fill red"></div>
                <span class="progress-text">75%</span>
            </div>
        </div>

        <!-- Pista 4 -->
        <div class="track-card">
            <div class="track-header">
                <div class="indicator green"></div> 4. SEA Seahawks (NFL)
            </div>
            <div class="track-metrics">
                <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                <span>-Cato $.00</span><span>$4.00</span><span>$9.41</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-fill green"></div>
                <span class="progress-text">66%</span>
            </div>
        </div>

        <!-- Pista 5 -->
        <div class="track-card">
            <div class="track-header">
                <div class="indicator purple"></div> 5. Combo ATP Beijing
            </div>
            <div class="track-metrics">
                <span>Probabilidad</span><span>Costo</span><span>Paga</span>
                <span>-Cato $.00</span><span>$6.00</span><span>$7.12</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-fill purple"></div>
                <span class="progress-text">75%</span>
            </div>
        </div>

        <!-- Menú Inferior -->
        <div class="footer-nav">
            <div class="footer-item"><span>≡</span> Menú</div>
            <div class="footer-item"><span>🔄</span> Sincronizar</div>
            <div class="footer-item"><span>➕</span> Nueva Pista</div>
            <div class="footer-item"><span>⚙️</span> Ajustes</div>
        </div>
    </div>

</body>
</html>
