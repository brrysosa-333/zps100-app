import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, StatusBar, TouchableOpacity, ActivityIndicator } from 'react-native';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [marketData, setMarketData] = useState(null);
  const [copilotMessage, setCopilotMessage] = useState("Sistema en espera de escaneo...");

  // Función para conectar con tu Backend Co-Pilot (Cambia la IP por la de tu servidor local o en la nube)
  const fetchLiveMarkets = async () => {
    setLoading(true);
    setCopilotMessage("Conectando con la API de Kalshi y aplicando ZPS-100...");
    
    try {
      // Nota: Si usas emulador Android usa 'http://10.0.2.2:5000/api/scan-markets' 
      // o la IP local de tu computadora en la red Wi-Fi.
      let response = await fetch('http://10.0.2.2:5000/api/scan-markets');
      let json = await response.json();
      
      if (json.status === "SUCCESS" && json.opportunities.length > 0) {
        setMarketData(json.opportunities[0]);
        setCopilotMessage(json.copilot_message);
      }
    } catch (error) {
      // En caso de estar probando sin el servidor encendido, cargamos data simulada autónoma:
      setMarketData({
        ticker: "TENIS-LIVE-SIM",
        title: "ATP / WTA Sweet Spot Match (Live Feed)",
        probability: 73,
        volume: 12500,
        score: 80,
        status: "EJECUTAR STAKE $6.00",
        action: "EXECUTE"
      });
      setCopilotMessage("Modo autónomo local: Datos procesados sin capturas.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLiveMarkets();
  }, []);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#05080C" />
      <ScrollView contentContainerStyle={styles.scroll}>
        
        {/* HEADER TERMINAL */}
        <Text style={styles.headerTitle}>🟢 ZPS-100 MATRIX CO-PILOT</Text>
        <Text style={styles.subTitle}>SYSTEM STATUS: ONLINE | AI AUTOMATED</Text>

        {/* RESUMEN BANCA */}
        <View style={styles.card}>
          <Text style={styles.cardLabel}>BANCA TOTAL / DISPONIBLE</Text>
          <Text style={styles.bankValue}>$23.06 USD <Text style={styles.liquid}>($7.06 USD Liq)</Text></Text>
          <View style={styles.progressBarBg}>
            <View style={[styles.progressBarFill, { width: '69%' }]} />
          </View>
          <Text style={styles.cardSub}>Risk Gauge: 69% Expuesto (Max 70%)</Text>
        </View>

        {/* PANEL DE ASISTENTE IA EN VIVO */}
        <View style={styles.cardAi}>
          <Text style={styles.aiTitle}>🤖 MATRIX AI CO-PILOT DICTAMEN</Text>
          <Text style={styles.aiMessage}>{copilotMessage}</Text>

          {loading ? (
            <ActivityIndicator size="small" color="#00FF66" style={{ marginTop: 10 }} />
          ) : marketData ? (
            <View style={styles.scoreBox}>
              <Text style={styles.cardSub}>Evento: {marketData.title}</Text>
              <Text style={styles.cardSub}>Probabilidad: {marketData.probability}% | Vol: ${marketData.volume}</Text>
              <Text style={styles.scoreText}>ZPS Score: {marketData.score}/100 PTS</Text>
              
              {marketData.action === "EXECUTE" ? (
                <Text style={styles.statusSuccess}>🟢 {marketData.status}</Text>
              ) : (
                <Text style={styles.statusError}>🔴 {marketData.status}</Text>
              )}
            </View>
          ) : null}

          <TouchableOpacity style={styles.button} onPress={fetchLiveMarkets}>
            <Text style={styles.buttonText}>⚡ ESCANEAR MERCADO EN VIVO</Text>
          </TouchableOpacity>
        </View>

        {/* IN-PLAY GUARD (MONITORING) */}
        <View style={styles.cardAlert}>
          <Text style={styles.alertTitle}>🛡️ POSICIONES EN CURSO (IN-PLAY GUARD)</Text>
          <Text style={styles.positionText}>🎾 Julieta Pareja @ 73% | Status: OK 🟢</Text>
          <Text style={styles.positionText}>🎾 Combo ATP Pekín | Status: Programado 🟡</Text>
        </View>

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#05080C', paddingTop: 40 },
  scroll: { padding: 16 },
  headerTitle: { color: '#00FF66', fontSize: 18, fontWeight: 'bold', fontFamily: 'monospace' },
  subTitle: { color: '#888', fontSize: 10, marginBottom: 15, fontFamily: 'monospace' },
  card: { backgroundColor: 'rgba(16, 27, 20, 0.85)', borderColor: '#00FF66', borderWidth: 1, borderRadius: 8, padding: 15, marginBottom: 15 },
  cardAi: { backgroundColor: 'rgba(10, 30, 20, 0.85)', borderColor: '#00FF66', borderWidth: 1.5, borderRadius: 8, padding: 15, marginBottom: 15 },
  cardAlert: { backgroundColor: 'rgba(25, 10, 15, 0.85)', borderColor: '#FF0055', borderWidth: 1, borderRadius: 8, padding: 15 },
  cardLabel: { color: '#888', fontSize: 10, fontFamily: 'monospace' },
  aiTitle: { color: '#00FF66', fontSize: 13, fontWeight: 'bold', marginBottom: 6, fontFamily: 'monospace' },
  aiMessage: { color: '#FFF', fontSize: 12, marginBottom: 10, fontFamily: 'monospace', fontStyle: 'italic' },
  bankValue: { color: '#00FF66', fontSize: 22, fontWeight: 'bold', marginVertical: 5 },
  liquid: { color: '#FFF', fontSize: 14 },
  progressBarBg: { height: 6, backgroundColor: '#1A261E', borderRadius: 3, marginVertical: 8 },
  progressBarFill: { height: 6, backgroundColor: '#00FF66', borderRadius: 3 },
  cardSub: { color: '#CCC', fontSize: 11, marginVertical: 2, fontFamily: 'monospace' },
  scoreBox: { marginTop: 8, paddingTop: 8, borderTopWidth: 1, borderTopColor: '#1A261E' },
  scoreText: { color: '#FFF', fontSize: 15, fontWeight: 'bold', fontFamily: 'monospace', marginTop: 4 },
  statusSuccess: { color: '#00FF66', fontWeight: 'bold', marginTop: 6, fontFamily: 'monospace' },
  statusError: { color: '#FF0055', fontWeight: 'bold', marginTop: 6, fontFamily: 'monospace' },
  alertTitle: { color: '#FF0055', fontSize: 12, fontWeight: 'bold', marginBottom: 8, fontFamily: 'monospace' },
  positionText: { color: '#FFF', fontSize: 11, marginVertical: 2, fontFamily: 'monospace' },
  button: { backgroundColor: '#00FF66', padding: 10, borderRadius: 5, marginTop: 12, alignItems: 'center' },
  buttonText: { color: '#05080C', fontWeight: 'bold', fontSize: 12, fontFamily: 'monospace' }
});
