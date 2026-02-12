"""
MÓDULO DE DETECÇÃO DE ANOMALIAS
CloudWalk - Monitoring Intelligence Challenge
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class AnomalyDetector:
    def __init__(self, historical_data_file='transactional_data.csv'):
        self.historical_data_file = historical_data_file
        self.baseline = {}
        self.thresholds = {
            'failed': {'warning': 1.15, 'critical': 1.30},
            'denied': {'warning': 1.15, 'critical': 1.30},
            'reversed': {'warning': 1.15, 'critical': 1.30},
            'approved': {'warning': 0.80, 'critical': 0.60}
        }
        self.load_baseline()
    
    def load_baseline(self):
        try:
            if os.path.exists(self.historical_data_file):
                df = pd.read_csv(self.historical_data_file)
                total = len(df)
                for status in ['failed', 'denied', 'reversed', 'approved']:
                    count = len(df[df['status'] == status])
                    percentual = (count / total * 100) if total > 0 else 0
                    self.baseline[status] = round(percentual, 2)
                print(f"✅ Baseline carregado: {total} transações")
            else:
                self.baseline = {'failed': 8.5, 'denied': 5.2, 'reversed': 2.1, 'approved': 84.2}
                print("⚠️ Baseline padrão carregado")
        except:
            self.baseline = {'failed': 8.5, 'denied': 5.2, 'reversed': 2.1, 'approved': 84.2}
    
    def detect_anomaly(self, status, current_rate):
        baseline_rate = self.baseline.get(status, 5.0)
        warning_threshold = baseline_rate * self.thresholds.get(status, {}).get('warning', 1.15)
        critical_threshold = baseline_rate * self.thresholds.get(status, {}).get('critical', 1.30)
        
        if baseline_rate > 0:
            variation = ((current_rate - baseline_rate) / baseline_rate) * 100
        else:
            variation = 0
        
        if current_rate > critical_threshold:
            alert_level = "CRITICAL"
            score = min(100, 50 + (variation / 2))
            should_alert = True
            recommendation = self._get_recommendation(status, 'critical')
        elif current_rate > warning_threshold:
            alert_level = "WARNING"
            score = min(70, 30 + (variation / 3))
            should_alert = True
            recommendation = self._get_recommendation(status, 'warning')
        else:
            alert_level = "NORMAL"
            score = 0
            should_alert = False
            recommendation = "Monitorar normalmente"
        
        return {
            'status': status,
            'current_rate': round(current_rate, 2),
            'baseline_rate': round(baseline_rate, 2),
            'variation_percent': round(variation, 2),
            'warning_threshold': round(warning_threshold, 2),
            'critical_threshold': round(critical_threshold, 2),
            'alert': should_alert,
            'alert_level': alert_level,
            'score': round(score, 2),
            'recommendation': recommendation
        }
    
    def _get_recommendation(self, status, level):
        recommendations = {
            'failed': {
                'warning': '⚠️ Investigar aumento de falhas - Verificar gateway',
                'critical': '🔴 AÇÃO IMEDIATA! Possível indisponibilidade - Acionar plantão'
            },
            'denied': {
                'warning': '⚠️ Aumento de transações negadas - Verificar antifraude',
                'critical': '🔴 AÇÃO IMEDIATA! Possível problema no antifraude'
            },
            'reversed': {
                'warning': '⚠️ Aumento de estornos - Monitorar merchants',
                'critical': '🔴 AÇÃO IMEDIATA! Possível fraude em lote'
            },
            'approved': {
                'warning': '⚠️ Queda nas aprovações - Investigar',
                'critical': '🔴 AÇÃO IMEDIATA! Queda crítica nas aprovações'
            }
        }
        return recommendations.get(status, {}).get(level, 'Investigar anomalia')