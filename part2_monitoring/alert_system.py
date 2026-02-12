"""
SISTEMA DE ALERTAS AUTOMÁTICOS
CloudWalk - Monitoring Intelligence Challenge
"""

import logging
from datetime import datetime
import json
import os

class AlertSystem:
    def __init__(self, log_file='alerts.log'):
        self.log_file = log_file
        self.alert_history = []
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, detection):
        alert_id = f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        alert_data = {
            'id': alert_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': detection['status'],
            'current_rate': detection['current_rate'],
            'baseline': detection['baseline_rate'],
            'variation': detection['variation_percent'],
            'level': detection['alert_level'],
            'score': detection['score'],
            'recommendation': detection['recommendation']
        }
        
        self.alert_history.append(alert_data)
        
        if detection['alert_level'] == 'CRITICAL':
            level_icon = "🔴"
            log_level = logging.CRITICAL
        elif detection['alert_level'] == 'WARNING':
            level_icon = "🟡"
            log_level = logging.WARNING
        else:
            level_icon = "🟢"
            log_level = logging.INFO
        
        message = f"""
{level_icon} ALERTA {detection['alert_level']}
ID: {alert_id}
Status: {detection['status'].upper()}
Taxa: {detection['current_rate']:.1f}% | Baseline: {detection['baseline_rate']:.1f}%
Variação: {detection['variation_percent']:+.1f}%
Recomendação: {detection['recommendation']}
"""
        
        self.logger.log(log_level, message)
        return alert_data
    
    def get_recent_alerts(self, limit=10):
        return self.alert_history[-limit:]