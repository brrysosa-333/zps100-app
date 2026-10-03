import streamlit as st
import time

# Configuración de página estilo Matrix
st.set_page_config(page_title="ZPS-100 Matrix Terminal", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS Personalizados (Matrix Theme)
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
        background: rgba(16, 27, 20, 0.85);
        border: 1px solid #00FF66;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .bank-title { font-size: 12px; color: #888888; }
    .bank-value { font-size: 24px; font-weight: bold; color: #00FF66; }
    .alert-card {
        background: rgba(40, 10, 15, 0.85);
        border: 1px solid #FF0055;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.3);
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Matrix Terminal
st.markdown("### ZPS-100 MATRIX TERMINAL v1.0")
st.caption("> SYSTEM STATUS: ONLINE | ALGORITHM: ACTIVE")

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

# MÓDULO 2 & 3: CALCULADORA Y ESCÁNER EN TIEMPO REAL
st.markdown("#### VALIDACIÓN DE OPORTUNIDAD (ZPS-100)")

col_left, col_right = st.columns([1, 1])

with col_left:
    deporte = st.selectbox("DEPORTE", ["Tenis 1v1", "Fútbol (3-way)", "Fútbol Americano (NCAA/NFL)"])
    prob = st.slider("PROBABILIDAD IMPLÍCITA (%)", 50, 95, 73)
    volumen = st.number_input("VOLUMEN EN KALSHI ($ USD)", min_value=0, value=12000)
    tiempo_hrs = st.number_input("HORAS HASTA EL EVENTO", min_value=0, value=12)

with col_right:
    # Lógica de cálculo cuantitativo ZPS-100
    score_wp = 40 if (70 <= prob <= 73) else (30 if (68 <= prob <= 75) else 0)
    score_wl = 25 if volumen > 50000 else (15 if volumen >= 10000 else 5)
    score_wt = 20 if tiempo_hrs <= 24 else (10 if tiempo_hrs <= 72 else 0)
    score_wv = 15 if deporte == "Tenis 1v1" else (5 if deporte == "Fútbol (3-way)" else 0)
    
    score_total = score_wp + score_wl + score_wt + score_wv
    
    st.markdown(f"**SCORE OBTENIDO:** `{score_total}/100 PTS`")
    
    if score_total >= 75 and 68 <= prob <= 75:
        st.success("STATUS: EJECUTAR STAKE $6.00 USD")
    elif 65 <= score_total < 75:
        st.warning("STATUS: EVALUAR RIESGO / ENTRADA EN OBSERVACIÓN")
    else:
        st.error("STATUS: RECHAZADO POR ALGORITMO")

# MÓDULO 4: POSICIONES ACTIVAS & IN-PLAY GUARD
st.markdown("#### POSICIONES EN CURSO")
st.info("Julieta Pareja (ITF Templeton) | Prob: 73% | Stake: $6.00 | Status: OK")
st.info("Combo Dúo ATP Pekín (Medvedev + Zverev) | Stake: $10.00 | Status: Programado")
