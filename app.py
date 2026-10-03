import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="ZPS-100 | Escáner Kalshi & Journal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

STAKE_FIJO = 6.00
JOURNAL_FILE = "journal_zps100.csv"

# --- FUNCIONES DEL SISTEMA ---
def calcular_zps(prob, volume, hours_left, category):
    if 70 <= prob <= 73:
        p_score = 40
        p_status = "Aceptable Óptimo"
    elif (68 <= prob < 70) or (73 < prob <= 75):
        p_score = 30
        p_status = "Aceptable Limítrofe"
    else:
        return 0, "🔴 DESCARTAR", "Fuera de Rango (<68% o >75%)"
    
    if category.lower() in ["climate", "weather", "clima"]:
        l_score = 25 if volume >= 8000 else (15 if volume >= 3000 else 0)
    else:
        l_score = 25 if volume >= 50000 else (15 if volume >= 10000 else 0)
            
    t_score = 20 if hours_left <= 24 else (15 if hours_left <= 72 else 0)
    v_score = 15
    
    total = p_score + l_score + t_score + v_score
    
    if total >= 80:
        status = "🟢 EJECUTAR"
    elif total >= 65:
        status = "🟡 MONITOREAR"
    else:
        status = "🔴 DESCARTAR"
        
    return total, status, p_status

@st.cache_data(ttl=60)
def fetch_kalshi_markets():
    url = "https://api.elections.kalshi.com/trade-api/v2/markets?limit=200&status=open"
    try:
        response = requests.get(url, headers={"accept": "application/json"}, timeout=10)
        if response.status_code == 200:
            return response.json().get("markets", [])
        return []
    except Exception as e:
        st.error(f"Error de conexión con Kalshi: {e}")
        return []

def cargar_journal():
    if os.path.exists(JOURNAL_FILE):
        return pd.read_csv(JOURNAL_FILE)
    else:
        return pd.DataFrame(columns=[
            "Fecha", "Ticker", "Mercado", "Precio Entrada", "Score ZPS",
            "Stake ($)", "Resultado", "P&L ($)", "Notas"
        ])

def guardar_journal(df):
    df.to_csv(JOURNAL_FILE, index=False)

# --- NAVEGACIÓN PRINCIPAL ---
st.title("🛡️ Sistema ZPS-100 (Kalshi)")

tab_escanner, tab_journal = st.tabs(["🔍 Escáner Live", "📖 Bitácora / Journal"])

# ==========================================
# PESTAÑA 1: ESCÁNER LIVE
# ==========================================
with tab_escanner:
    st.caption("Filtrado cuantitativo de oportunidades según el rango de probabilidad de precisión (68% - 75%).")
    
    st.markdown("### 📊 Clasificación por Probabilidad y Puntuación")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**🟢 ACEPTABLE / EJECUTAR**\n\nProbabilidad: **70% - 73%** (Óptimo)\nPuntos: **≥ 80 PTS**\nStake: **$6.00 USD**")
    with c2:
        st.warning("**🟡 MONITOREAR**\n\nProbabilidad: **68%-69%** o **74%-75%**\nPuntos: **65 - 79 PTS**\nStake: **$0.00 USD (Esperar)**")
    with c3:
        st.error("**🔴 RECHAZAR / DESCARTAR**\n\nProbabilidad: **< 68%** o **> 75%**\nPuntos: **< 65 PTS**\nStake: **$0.00 USD (Abortar)**")

    st.markdown("---")
    st.subheader("🔍 Filtro de Mercados")

    search_query = st.text_input(
        "Escribe un equipo, jugador o liga y presiona Enter para buscar:",
        placeholder="🔍 Escribe aquí y presiona Enter...",
        type="search",
        key="search_live"
    )

    filter_state = st.radio(
        "Selecciona un filtro rápido:",
        ["🌐 Ver Todos", "🟢 Solo Ejecutar", "🟡 Solo Monitorear", "🔴 Solo Descartar"],
        horizontal=True
    )

    raw_markets = fetch_kalshi_markets()

    if raw_markets:
        parsed_results = []
        query_clean = search_query.strip().lower()
        
        for m in raw_markets:
            ticker = m.get("ticker", "")
            title = m.get("title", "")
            category = m.get("category", "General")
            
            yes_price = m.get("last_price") or m.get("yes_bid") or 0
            prob = float(yes_price)
            volume = float(m.get("volume", 0))
            hours_left = 24
            
            score, status, p_status = calcular_zps(prob, volume, hours_left, category)
            
            match_text = True if not query_clean else (query_clean in title.lower() or query_clean in ticker.lower())
            
            match_status = True
            if filter_state == "🟢 Solo Ejecutar":
                match_status = "🟢" in status
            elif filter_state == "🟡 Solo Monitorear":
                match_status = "🟡" in status
            elif filter_state == "🔴 Solo Descartar":
                match_status = "🔴" in status
                
            if match_text and match_status:
                parsed_results.append({
                    "Dictamen": status,
                    "Rango Probabilidad": p_status,
                    "Probabilidad Implícita": f"{prob:.0f}%",
                    "Score ZPS": score,
                    "Mercado": title,
                    "Volumen": f"${volume:,.0f}",
                    "Stake": f"${STAKE_FIJO:.2f} USD" if "🟢" in status else "$0.00 USD",
                    "Ticker": ticker
                })
                
        if parsed_results:
            df = pd.DataFrame(parsed_results)
            df = df.sort_values(by="Score ZPS", ascending=False)
            
            st.success(f"Se encontraron **{len(df)}** mercado(s).")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontraron mercados con el filtro o estado seleccionado.")

# ==========================================
# PESTAÑA 2: BITÁCORA / JOURNAL DE OPERACIONES
# ==========================================
with tab_journal:
    st.subheader("📖 Journal de Operaciones ZPS-100")
    st.caption("Lleva el control exacto de tus entradas, calcula tu Win Rate y mide tus ganancias netas.")
    
    df_journal = cargar_journal()
    
    # METRICAS PRINCIPALES
    if not df_journal.empty:
        total_ops = len(df_journal)
        cerradas = df_journal[df_journal["Resultado"].isin(["Ganada", "Perdida"])]
        ganadas = len(df_journal[df_journal["Resultado"] == "Ganada"])
        win_rate = (ganadas / len(cerradas) * 100) if len(cerradas) > 0 else 0.0
        pnl_total = df_journal["P&L ($)"].sum()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Operaciones Registradas", total_ops)
        m2.metric("Win Rate", f"{win_rate:.1f}%")
        m3.metric("P&L Total", f"${pnl_total:+.2f} USD")
        m4.metric("Stake Base", f"${STAKE_FIJO:.2f} USD")
    else:
        st.info("Aún no tienes operaciones registradas en tu bitácora.")

    st.markdown("---")
    
    # FORMULARIO DE REGISTRO
    with st.expander("➕ Registrar Nueva Operación"):
        with st.form("form_nuevo_trade"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                input_ticker = st.text_input("Ticker / Mercado ID:", placeholder="Ej: KXSOCCER-24OCT-BAL")
                input_mercado = st.text_input("Nombre del Mercado / Equipo:", placeholder="Ej: Real Madrid vs FC Barcelona")
                input_precio = st.number_input("Precio de Entrada (¢ / %):", min_value=1, max_value=99, value=71)
            with col_f2:
                input_score = st.number_input("Score ZPS (0 - 100):", min_value=0, max_value=100, value=85)
                input_resultado = st.selectbox("Estado / Resultado:", ["Pendiente", "Ganada", "Perdida"])
                input_pnl = st.number_input("Ganancia / Pérdida ($ USD):", value=0.0, step=0.5)
                
            input_notas = st.text_area("Notas / Observaciones:", placeholder="Ej: Excelente volumen y liquidez en tenis 1v1...")
            btn_guardar = st.form_submit_button("💾 Guardar en Bitácora")
            
            if btn_guardar:
                if input_mercado.strip():
                    nueva_fila = {
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Ticker": input_ticker.upper(),
                        "Mercado": input_mercado,
                        "Precio Entrada": f"{input_precio}%",
                        "Score ZPS": input_score,
                        "Stake ($)": STAKE_FIJO,
                        "Resultado": input_resultado,
                        "P&L ($)": input_pnl if input_resultado != "Pendiente" else 0.0,
                        "Notas": input_notas
                    }
                    df_journal = pd.concat([pd.DataFrame([nueva_fila]), df_journal], ignore_index=True)
                    guardar_journal(df_journal)
                    st.success("✅ ¡Operación registrada correctamente!")
                    st.rerun()
                else:
                    st.error("Por favor completa el nombre del mercado.")

    # TABLA DE HISTORIAL
    if not df_journal.empty:
        st.markdown("### 📜 Historial de Registros")
        st.dataframe(df_journal, use_container_width=True, hide_index=True)
    
