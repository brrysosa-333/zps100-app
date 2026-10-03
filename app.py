import React, { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, StatusBar } from 'react-native';

export default function App() {
  const [prob, setProb] = useState(73);
  const [volumen, setVolumen] = useState(12000);
  
  // Algoritmo ZPS-100 Integrado
  const wp = (prob >= 70 && prob <= 73) ? 40 : ((prob >= 68 && prob <= 75) ? 30 : 0);
  const wl = volumen >= 50000 ? 25 : (volumen >= 10000 ? 15 : 5);
  const wt = 20; // < 24h
  const wv = 15; // Tenis 1v1
  const score = wp + wl + wt + wv;

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#05080C" />
      <ScrollView contentContainerStyle={styles.scroll}>
        
        {/* HEADER TERMINAL */}
        <Text style={styles.headerTitle}>🟢 ZPS-100 MATRIX TERMINAL</Text>
        <Text style={styles.subTitle}>SYSTEM STATUS: ONLINE | MOBILE CORE</Text>

        {/* RESUMEN BANCA */}
        <View style={styles.card}>
          <Text style={styles.cardLabel}>BANCA TOTAL / DISPONIBLE</Text>
          <Text style={styles.bankValue}>$23.06 USD <Text style={styles.liquid}>($7.06 USD Liq)</Text></Text>
          <View style={styles.progressBarBg}>
            <View style={[styles.progressBarFill, { width: '69%' }]} />
          </View>
          <Text style={styles.cardSub}>Risk Gauge: 69% Expuesto (Max 70%)</Text>
        </View>

        {/* CALCULADORA ZPS-100 */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>🧮 VALIDACIÓN DE RIESGO</Text>
          <Text style={styles.cardSub}>Deporte: Tenis 1v1 (ATP/WTA)</Text>
          <Text style={styles.cardSub}>Probabilidad Implícita: {prob}%</Text>
          <Text style={styles.cardSub}>Volumen: ${volumen.toLocaleString()} USD</Text>
          
          <View style={styles.scoreBox}>
            <Text style={styles.scoreText}>ZPS Score: {score}/100 PTS</Text>
            {score >= 80 ? (
              <Text style={styles.statusSuccess}>🟢 EXECUTE STAKE $6.00</Text>
            ) : (
              <Text style={styles.statusError}>🔴 REJECT / HOLD</Text>
            )}
          </View>
        </View>

        {/* IN-PLAY GUARD (MONITORING) */}
        <View style={styles.cardAlert}>
          <Text style={styles.alertTitle}>🛡️ POSICIONES EN CURSO (IN-PLAY GUARD)</Text>
          <Text style={styles.positionText}>🎾 Julieta Pareja @ 73% | Status: OK</Text>
          <Text style={styles.positionText}>🎾 Combo ATP Pekín | Status: Programado</Text>
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
  cardAlert: { backgroundColor: 'rgba(25, 10, 15, 0.85)', borderColor: '#FF0055', borderWidth: 1, borderRadius: 8, padding: 15 },
  cardLabel: { color: '#888', fontSize: 10, fontFamily: 'monospace' },
  cardTitle: { color: '#00FF66', fontSize: 14, fontWeight: 'bold', marginBottom: 8, fontFamily: 'monospace' },
  bankValue: { color: '#00FF66', fontSize: 22, fontWeight: 'bold', marginVertical: 5 },
  liquid: { color: '#FFF', fontSize: 14 },
  progressBarBg: { height: 6, backgroundColor: '#1A261E', borderRadius: 3, marginVertical: 8 },
  progressBarFill: { height: 6, backgroundColor: '#00FF66', borderRadius: 3 },
  cardSub: { color: '#CCC', fontSize: 12, marginVertical: 2, fontFamily: 'monospace' },
  scoreBox: { marginTop: 10, paddingTop: 10, borderTopWidth: 1, borderTopColor: '#1A261E' },
  scoreText: { color: '#FFF', fontSize: 16, fontWeight: 'bold', fontFamily: 'monospace' },
  statusSuccess: { color: '#00FF66', fontWeight: 'bold', marginTop: 5 },
  statusError: { color: '#FF0055', fontWeight: 'bold', marginTop: 5 },
  alertTitle: { color: '#FF0055', fontSize: 12, fontWeight: 'bold', marginBottom: 8, fontFamily: 'monospace' },
  positionText: { color: '#FFF', fontSize: 11, marginVertical: 2, fontFamily: 'monospace' }
});
