"""
SIMULADOR DE TRANSAÇÕES EM TEMPO REAL
CloudWalk - Monitoring Intelligence Challenge
"""

import requests
import random
import time
from datetime import datetime, timedelta
import json

# Lista de status possíveis
STATUS_LIST = ['approved', 'approved', 'approved', 'approved', 'approved', 
               'approved', 'approved', 'failed', 'denied', 'reversed']

# Merchants simulados
MERCHANTS = [f'MER{str(i).zfill(3)}' for i in range(1, 21)]

# Métodos de pagamento
PAYMENT_METHODS = ['credit_card', 'debit', 'pix', 'boleto']

def generate_transaction():
    """Gera uma transação simulada"""
    
    status = random.choice(STATUS_LIST)
    
    # Pesos diferentes para cada status (para criar padrões)
    if random.random() < 0.05:  # 5% de chance de falha
        status = 'failed'
    elif random.random() < 0.03:  # 3% de chance de denied
        status = 'denied'
    elif random.random() < 0.02:  # 2% de chance de reversed
        status = 'reversed'
    
    transaction = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'transaction_id': f'TXN{random.randint(10000, 99999)}',
        'status': status,
        'amount': round(random.uniform(10.0, 1000.0), 2),
        'merchant_id': random.choice(MERCHANTS),
        'payment_method': random.choice(PAYMENT_METHODS)
    }
    
    return transaction

def simulate_traffic(rate_per_second=2, duration_seconds=60):
    """
    Simula tráfego de transações
    
    Args:
        rate_per_second: Transações por segundo
        duration_seconds: Duração da simulação em segundos
    """
    
    print("\n" + "="*60)
    print("📊 SIMULADOR DE TRANSAÇÕES EM TEMPO REAL")
    print("="*60)
    print(f"Taxa: {rate_per_second} transações/segundo")
    print(f"Duração: {duration_seconds} segundos")
    print(f"Total estimado: {rate_per_second * duration_seconds} transações")
    print("="*60 + "\n")
    
    url = "http://localhost:5000/check-transaction"
    transactions_sent = 0
    start_time = time.time()
    
    # Criar picos de falha para testar alertas
    failure_spike_time = start_time + 20  # Pico após 20 segundos
    
    try:
        while time.time() - start_time < duration_seconds:
            # Simular pico de falhas
            current_time = time.time()
            if failure_spike_time <= current_time < failure_spike_time + 5:
                # Aumentar taxa de falhas durante o pico
                batch_size = rate_per_second * 3
                status_override = 'failed'
            else:
                batch_size = rate_per_second
                status_override = None
            
            for _ in range(batch_size):
                transaction = generate_transaction()
                
                # Forçar status durante pico
                if status_override:
                    transaction['status'] = status_override
                
                try:
                    response = requests.post(url, json=transaction, timeout=0.1)
                    transactions_sent += 1
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('alert'):
                            print(f"⚠️ ALERTA: {result['status']} - {result['alert_level']} - {result['recommendation']}")
                    
                except:
                    pass  # Ignora erros de timeout
            
            time.sleep(1)  # Aguarda 1 segundo
            
            # Progresso
            elapsed = int(time.time() - start_time)
            print(f"⏱️  {elapsed}s | Transações: {transactions_sent}")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Simulação interrompida pelo usuário")
    
    finally:
        print("\n" + "="*60)
        print("✅ SIMULAÇÃO FINALIZADA")
        print(f"Total de transações enviadas: {transactions_sent}")
        print("="*60)

if __name__ == '__main__':
    # Parâmetros configuráveis
    TAXA_TRANSACOES = 2  # Transações por segundo
    DURACAO = 60         # Duração em segundos
    
    simulate_traffic(rate_per_second=TAXA_TRANSACOES, duration_seconds=DURACAO)