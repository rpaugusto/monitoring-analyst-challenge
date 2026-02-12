"""
MÓDULO DE BANCO DE DADOS SQLITE
CloudWalk - Monitoring Intelligence Challenge
Autor: [Seu nome]
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

class MonitoringDatabase:
    """Gerenciador do banco de dados de monitoramento"""
    
    def __init__(self, db_path='monitoring.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                transaction_id VARCHAR(50) UNIQUE,
                status VARCHAR(20),
                amount DECIMAL(10,2),
                merchant_id VARCHAR(20),
                payment_method VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de métricas por minuto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS minute_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                minute DATETIME,
                status VARCHAR(20),
                count INTEGER,
                percentage DECIMAL(5,2),
                total_transactions INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id VARCHAR(30) UNIQUE,
                timestamp DATETIME,
                status VARCHAR(20),
                current_rate DECIMAL(5,2),
                baseline_rate DECIMAL(5,2),
                variation DECIMAL(5,2),
                alert_level VARCHAR(20),
                score INTEGER,
                recommendation TEXT,
                acknowledged BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Banco de dados inicializado")
    
    def insert_transaction(self, transaction):
        """Insere uma transação no banco"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO transactions 
                (timestamp, transaction_id, status, amount, merchant_id, payment_method)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                transaction.get('timestamp'),
                transaction.get('transaction_id'),
                transaction.get('status