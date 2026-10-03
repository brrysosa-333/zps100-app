import streamlit as st
import pandas as pd
import requests

# Configuración de página
st.set_page_config(
    page_title="ZPS-100 | Escáner Kalshi",
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

st.title("🛡️ Escáner ZPS-100 (Kalshi Live)")
st.caption("Filtrado cuantitativo de oportunidades según el rango de probabilidad de precisión (68% - 75%).")

STAKE_FIJO = 6.00

def calcular_zps(prob, volume, hours_left, category):
    # 1. Probabilidad Implícita (Max 40 pts)
    if 70 <= prob <= 73:
        p_score = 40
        p_status = "Aceptable Óptimo"
    elif (68 <= prob < 70) or (73 < prob <= 75):
        p_score = 30
        p_status = "Aceptable Limítrofe"
    else:
        return 0, "🔴 DESCARTAR", "Fuera de Rango (<68% o >75%)"
    
    # 2. Liquidez y Volumen (Max 25 pts)
    if category.lower() in ["climate", "weather", "clima"]:
        l_score = 25 if volume >= 8000 else (15 if volume >= 3000 else 0)
    else:
        l_score = 25 if volume >= 50000 else (15 if volume >= 10000 else 0)
            
    # 3. Horizonte Temporal (Max 20 pts)
    t_score = 20 if hours_left <= 24 else (15 if hours_left <= 72 else 0)
        
    # 4. Estructura y Varianza (Base 15 pts)
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

# --- GUÍA VISUAL DE PROBABILIDAD ---
st.markdown("### 📊 Clasificación por Probabilidad y Puntuación")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("**🟢 ACEPTABLE / EJECUTAR**\n\nProbabilidad: **70% - 73%** (Óptimo)\nPuntos: **≥ 80 PTS**\nStake: **$6.00 USD**")
with c2:
    st.warning("**🟡 MONITOREAR**\n\nProbabilidad: **68%-69%** o **74%-75%**\nPuntos: **65 - 79 PTS**\nStake: **$0.00 USD (Esperar)**")
with c3:
    st.error("**🔴 RECHAZAR / DESCARTAR**\n\nProbabilidad: **< 68%** o **> 75%**\nPuntos: **< 65 PTS**\nStake: **$0.00 USD (Abortar)**")

# --- BUSCADOR Y FILTROS POR BOTÓN ---
st.markdown("---")
st.subheader("🔍 Filtro de Mercados")

search_query = st.text_input("🔎 Equipo, jugador, deporte o liga:", placeholder="Ej: Tennis, Sakkari, Soccer, Fed...")

st.write("**Filtrar rápido por estado de probabilidad:**")

filter_state = st.radio(
    "Selecciona un filtro:",
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
        
        # Filtro de texto
        match_text = True if not query_clean else (query_clean in title.lower() or query_clean in ticker.lower())
        
        # Filtro por estado
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
        
