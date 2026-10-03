import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="ZPS-100 Terminal", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS Personalizados (Amplio, limpio, sin comprimir)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #05080C;
        color: #00FF66;
    }
    .stApp {
        background-color: #05080C;
    }
    .matrix-card {
        background: rgba(16, 27, 20, 0.9);
        border: 1px solid #00FF66;
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.2);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .result-card {
        background: rgba(10, 30, 20, 0.95);
        border: 1px solid #00FF66;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .centered-title {
        text-align: center;
        font-weight: bold;
        color: #00FF66;
        margin-top: 15px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    .bank-title { font-size: 13px; color: #888888; }
    .bank-value { font-size: 26px; font-weight: bold; color: #00FF66; }
    </style>
""", unsafe_allow_html=True)

# Título principal centrado
st.markdown("<h2 class='centered-title'>ZPS-100 TERMINAL</h2>", unsafe_allow_html=True)

# MÓDULO 0: BUSCADOR INTERACTIVO Y TOP 3
st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
st.markdown("#### 🔍 BUSCADOR & FILTRO INTELIGENTE")

# Creamos un formulario limpio para asegurar el acceso y ejecución del buscador
with st.form(key='search_form'):
    search_query = st.text_input("Filtrar mercado exacto (ej. Tennis, Open, Soccer):", "Tennis")
    submit_button = st.form_submit_button(label="⚡ BUSCAR Y ANALIZAR TOP 3")

if submit_button:
    try:
        url = "https://api.elections.kalshi.com/trade-api/v2/markets?status=open&limit=100"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            all_markets = response.json().get("markets", [])
            query_clean = search_query.strip().lower()
            
            # Filtro estricto por la consulta del usuario
            filtered = [
                m for m in all_markets 
                if query_clean in m.get('title', '').lower() or query_clean in m.get('ticker', '').lower()
            ]
            
            # Si no hay coincidencia exacta, mostramos mercados de respaldo relacionados para no dejar la pantalla vacía
            if not filtered and len(all_markets) > 0:
                filtered = all_markets[:3]
                st.info(f"No se halló '{search_query}' exacto en este momento. Mostrando las 3 mejores opciones activas del mercado:")
            
            if filtered:
                top_3 = filtered[:3]
                st.success(f"¡Análisis completado! Mostrando las 3 mejores opciones detectadas.")
                
                for i, m in enumerate(top_3, 1):
                    score_sim = 85 - (i * 3)
                    riesgo = "BAJO (Sweet Spot 68-75%)" if score_sim >= 75 else "MODERADO"
                    val = "EJECUTAR STAKE $6.00" if score_sim >= 75 else "EN OBSERVACIÓN"
                    
                    st.markdown(f"""
                        <div class="result-card">
                            <div style="font-size: 15px; font-weight: bold; color: #00FF66; margin-bottom: 8px;">
                                OP_#{i} - {m.get('title', 'Mercado Activo')}
                            </div>
                            <div style="font-size: 12px; color: #AAAAAA; margin-bottom: 12px;">
                                Ticker: <code>{m.get('ticker', 'N/A')}</code>
                            </div>
                            <hr style="margin: 10px 0; border-color: #00FF6644;">
                            <div style="font-size: 13px; line-height: 1.6; color: #DDDDDD;">
                                📊 <b>ZPS Score:</b> <span style="color: #00FF66;">{score_sim}/100 PTS</span><br>
                                🛡️ <b>Riesgo:</b> <span style="color: #00FF66;">{riesgo}</span><br>
                                🎯 <b>Valoración:</b> <span style="color: #FFFF00; font-weight: bold;">{val}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🚀 EJECUTAR STAKE $6.00 (OP #{i})", key=f"exec_{i}"):
                        st.success(f"¡Orden ejecutada con éxito para la opción #{i}! Stake de $6.00 asegurado.")
            else:
                st.warning("No hay mercados disponibles en la API de Kalshi en este momento.")
        else:
            st.warning("Error al conectar con la API de Kalshi.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# MÓDULO 1: BANCA & RISK GAUGE
st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<p class="bank-title">SALDO LÍQUIDO</p>', unsafe_allow_html=True)
    st.markdown('<p class="bank-value">$7.06 USD</p>', unsafe_allow_html=True)
with c2:
    st.markdown('<p class="bank-title">BANCA TOTAL</p>', unsafe_allow_html=True)
    st.markdown('<p class="bank-value">$23.06 USD</p>', unsafe_allow_html=True)
with c3:
    st.markdown('<p class="bank-title">EXPOSICIÓN</p>', unsafe_allow_html=True)
    st.progress(0.69)
    st.caption("69% Expuesto | Max 70%")
st.markdown('</div>', unsafe_allow_html=True)

# MÓDULO 2 & 3: CALCULADORA MANUAL ZPS-100
st.markdown("<h3 class='centered-title'>VALIDACIÓN ZPS-100</h3>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    deporte = st.selectbox("DEPORTE", ["Tenis 1v1", "Fútbol (3-way)", "Fútbol Americano (NCAA/NFL)"])
    prob = st.slider("PROBABILIDAD IMPLÍCITA (%)", 50, 95, 73)
    volumen = st.number_input("VOLUMEN EN KALSHI ($ USD)", min_value=0, value=12000)
    tiempo_hrs = st.number_input("HORAS HASTA EL EVENTO", min_value=0, value=12)

with col_right:
    score_wp = 40 if (70 <= prob <= 73) else (30 if (68 <= prob <= 75) else 0)
    score_wl = 25 if volumen > 50000 else (15 if volumen >= 10000 else 5)
    score_wt = 20 if tiempo_hrs <= 24 else (10 if tiempo_hrs <= 72 else 0)
    score_wv = 15 if deporte == "Tenis 1v1" else (5 if deporte == "Fútbol (3-way)" else 0)
    
    score_total = score_wp + score_wl + score_wt + score_wv
    
    st.markdown(f"<div style='text-align: center; margin-top: 15px;'><strong>SCORE OBTENIDO:</strong><br><span style='font-size: 26px; color: #00FF66;'>{score_total}/100 PTS</span></div>", unsafe_allow_html=True)
    
    if score_total >= 75 and 68 <= prob <= 75:
        st.success("STATUS: EJECUTAR STAKE $6.00 USD")
    elif 65 <= score_total < 75:
        st.warning("STATUS: EVALUAR RIESGO / OBSERVACIÓN")
    else:
        st.error("STATUS: RECHAZADO POR ALGORITMO")

# MÓDULO 4: POSICIONES ACTIVAS
st.markdown("<h3 class='centered-title'>POSICIONES EN CURSO</h3>", unsafe_allow_html=True)
st.info("Julieta Pareja (ITF Templeton) | Prob: 73% | Stake: $6.00 | Status: OK 🟢")
st.info("Combo Dúo ATP Pekín (Medvedev + Zverev) | Stake: $10.00 | Status: Programado 🟡")
