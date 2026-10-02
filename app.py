import streamlit as st

st.set_page_config(page_title="ZPS-100 Scanner", page_icon="🛡", layout="centered")

st.title("🛡️️ ZPS-100 Precision Scanner")
st.caption("Sistema Cuantitativo de Evaluación para Mercados Kalshi")

st.markdown("---")

st.header("📊 Datos de la Oportunidad")

prob = st.slider("Probabilidad Implícita / Precio (%)", min_value=1, max_value=100, value=70)
vol = st.number_input("Volumen de Contratos / Liquidez ($)", min_value=0, value=1500, step=100)
dias = st.number_input("Días hasta la resolución", min_value=0, value=3)

# Algoritmo ZPS-100
score = 0

# 1. Rango Óptimo de Probabilidad (68% - 75%)
if 68 <= prob <= 75:
    score += 40
elif 60 <= prob < 68 or 75 < prob <= 80:
    score += 20

# 2. Filtro de Liquidez
if vol >= 1000:
    score += 30
elif vol >= 500:
    score += 15

# 3. Horizonte Temporal (Corto plazo preferido)
if dias <= 3:
    score += 30
elif dias <= 7:
    score += 15

st.markdown("---")
st.subheader("🎯 Resultado de la Evaluación")

st.metric(label="Puntuación ZPS-100", value=f"{score} / 100 PTS")

if score >= 80:
    st.success("✅ **ENTRADA VÁLIDA (ZONA DE PRECISIÓN)**\n\n- Stake Fijo: **$6.00 USD**\n- Stop-Loss Operativo: Si la prob. en vivo cae de **68%**")
elif score >= 50:
    st.warning("⚠️ **EVALUAR CON PRECAUCIÓN**\n\nNo cumple con todos los filtros estrictos del sistema.")
else:
    st.error("❌ **DESCHARTAR / NO OPERAR**\n\nFuera de los parámetros de ventaja cuantitativa.")
  
