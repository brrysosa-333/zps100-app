import streamlit as st
import pandas as pd
import requests

# Configuración de página
st.set_page_config(page_title="ZPS-100 | Kalshi Scanner", layout="wide", initial_sidebar_state="expanded")

st.title("🛡️ Escáner ZPS-100 (Kalshi Live)")
st.caption("Búsqueda inteligente y filtrado automático de oportunidades según el algoritmo ZPS-100.")

STAKE_FIJO = 6.00

def calcular_zps(prob, volume, hours_left, category):
    # 1. Probabilidad Implícita (Max 40 pts)
    if 70 <= prob <= 73:
        p_score = 40
    elif (68 <= prob < 70) or (73 < prob <= 75):
        p_score = 30
    else:
        return 0, "🔴 DESCARTAR (<68% o >75%)"
    
    # 2. Liquidez y Volumen (Max 25 pts)
    if category.lower() in ["climate", "weather"]:
        l_score = 25 if volume >= 8000 else (15 if volume >= 3000 else 0)
    else:
        l_score = 25 if volume >= 50000 else (15 if volume >= 10000 else 0)
            
    # 3. Horizonte Temporal (Max 20 pts)
    t_score = 20 if hours_left <= 24 else (15 if hours_left <= 72 else 0)
        
    # 4. Estructura y Varianza (Base 15 pts)
    v_score = 15
    
    total = p_score + l_score + t_score + v_score
    
    if total >= 80:
        status = "🟢 EJECUTAR ($6.00)"
    elif total >= 65:
        status = "🟡 MONITOREAR"
    else:
        status = "🔴 DESCARTAR"
        
    return total, status

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

# --- BARRA DE BÚSQUEDA Y FILTROS ---
st.subheader("🔍 Buscador de Mercados")
col_search, col_min_score = st.columns([3, 1])

with col_search:
    search_query = st.text_input("🔎 Buscar por equipo, jugador, liga o categoría:", placeholder="Ej: Sakkari, Boca, Tenis, LaLiga...")

with col_min_score:
    min_score = st.number_input("Puntuación mínima (PTS):", min_value=0, max_value=100, value=65, step=5)

# Cargar datos
raw_markets = fetch_kalshi_markets()

if raw_markets:
    parsed_results = []
    for m in raw_markets:
        ticker = m.get("ticker", "")
        title = m.get("title", "")
        category = m.get("category", "General")
        
        yes_price = m.get("last_price") or m.get("yes_bid") or 0
        prob = float(yes_price)
        volume = float(m.get("volume", 0))
        hours_left = 24  # Ajuste base para eventos activos
        
        score, status = calcular_zps(prob, volume, hours_left, category)
        
        # Filtro de búsqueda textual en tiempo real
        match_text = (
            search_query.lower() in title.lower() or 
            search_query.lower() in ticker.lower() or 
            search_query.lower() in category.lower()
        )
        
        if match_text and score >= min_score:
            parsed_results.append({
                "Estatus": status,
                "Score ZPS": score,
                "Mercado / Evento": title,
                "Probabilidad": f"{prob:.0f}%",
                "Volumen ($)": f"${volume:,.0f}",
                "Stake Recomendado": f"${STAKE_FIJO:.2f} USD" if score >= 80 else "$0.00 USD",
                "Ticker": ticker
            })
            
    if parsed_results:
        df = pd.DataFrame(parsed_results)
        df = df.sort_values(by="Score ZPS", ascending=False)
        
        st.success(f"Se encontraron **{len(df)}** mercado(s) coincidente(s).")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No se encontraron mercados que coincidan con la búsqueda o el puntaje mínimo seleccionado.")
else:
    st.info("Obteniendo mercados activos de Kalshi...")
    
  
