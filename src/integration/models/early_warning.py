from typing import Dict

class EarlyWarningSystem:
    def __init__(self):
        self.thresholds = {
            'yellow': 1.2,  # 20% превышение
            'red': 1.5      # 50% превышение
        }
        
    def check_status(self, step: str, days: float) -> str:
        standard_time = self.get_standard_time(step)
        ratio = days / standard_time
        
        if ratio >= self.thresholds['red']:
            return 'red'
        elif ratio >= self.thresholds['yellow']:
            return 'yellow'
        return 'green'
        
    def get_standard_time(self, step: str) -> int:
        standard_times = {
            'step1': 3, 'step2': 7, 'step3': 5,
            'step4': 5, 'step5': 1, 'step6': 8, 'step7': 1
        }
        return standard_times[step]
