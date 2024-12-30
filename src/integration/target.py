from typing import Dict

class IntegrationTarget:
    def __init__(self):
        self.target_days = 30
        
    def calculate_target(self, actual_days: float) -> Dict:
        deviation = actual_days - self.target_days
        completion_rate = min(1.0, self.target_days / actual_days) if actual_days > 0 else 0
        
        return {
            'on_time': actual_days <= self.target_days,
            'deviation_days': deviation,
            'completion_rate': completion_rate
        }
