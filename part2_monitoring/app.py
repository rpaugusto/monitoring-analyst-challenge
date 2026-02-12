"""
ENDPOINT REST DE MONITORAMENTO
CloudWalk - Monitoring Intelligence Challenge
"""

from flask import Flask, request, jsonify
from detector import AnomalyDetector
from alert_system import AlertSystem
from datetime import datetime
import pandas as pd

app = Flask(__name__)
detector = AnomalyDetector()
alert_system = AlertSystem()

# Armazenar últimas transações para calcular taxas
recent_transactions = []

@app.route('/check-transaction', methods=['POST'])
def check_transaction():
    """Endpoint para verificar transação e gerar alertas"""
    
    try:
        data = request.json
        
        # Adicionar timestamp se não existir
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Adicionar à lista de transações recentes
        recent_transactions.append(data)
        
        # Manter apenas últimos 100 registros (10 minutos simulados)
        if len(recent_transactions) > 100:
            recent_transactions.pop(0)
        
        # Calcular taxa do status nos últimos registros
        df_recent = pd.DataFrame(recent_transactions)
        total = len(df_recent)
        
        if total > 0:
            count = len(df_recent[df_recent['status'] == data['status']])
            current_rate = (count / total * 100)
        else:
            current_rate = 0
        
        # Detectar anomalia
        detection = detector.detect_anomaly(data['status'], current_rate)
        
        # Gerar alerta se necessário
        if detection['alert']:
            alert = alert_system.send_alert(detection)
            detection['alert_id'] = alert['id']
        
        # Adicionar dados da transação
        response = {
            'transaction_id': data.get('transaction_id', 'N/A'),
            'status': data['status'],
            'timestamp': data['timestamp'],
            'alert': detection['alert'],
            'alert_level': detection['alert_level'],
            'current_rate': detection['current_rate'],
            'baseline_rate': detection['baseline_rate'],
            'variation': detection['variation_percent'],
            'recommendation': detection['recommendation'],
            'score': detection['score']
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'transactions_monitored': len(recent_transactions)
    })

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Retorna últimos alertas"""
    limit = int(request.args.get('limit', 10))
    return jsonify({
        'alerts': alert_system.get_recent_alerts(limit),
        'total': len(alert_system.alert_history)
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Retorna estatísticas do sistema"""
    return jsonify({
        'baseline': detector.baseline,
        'alerts_generated': len(alert_system.alert_history),
        'transactions_in_window': len(recent_transactions)
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CLOUDWALK - MONITORING INTELLIGENCE SYSTEM")
    print("="*60)
    print("\n📡 Endpoint disponível em: http://localhost:5000")
    print("   • POST /check-transaction - Enviar transação")
    print("   • GET  /health - Status do sistema")
    print("   • GET  /alerts - Últimos alertas")
    print("   • GET  /stats - Estatísticas")
    print("\n" + "="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)