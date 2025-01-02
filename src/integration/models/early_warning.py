from typing import Dict, List
import yaml
from pathlib import Path

class EarlyWarningSystem:
    def __init__(self):
        self.thresholds = {
            'yellow': 1.2,  # 20% превышение
            'red': 1.5      # 50% превышение
        }
        self.settings = self.load_settings()

    def load_settings(self):
        config_path = Path(__file__).parent.parent.parent / 'config' / 'settings.yaml'
        with open(config_path) as f:
            return yaml.safe_load(f)
        
    def check_status(self, active_steps: List[str], steps_time: Dict) -> str:
        # Берем максимальное отношение времени выполнения к стандартному
        max_ratio = 0
        for step in active_steps:
            standard_time = self.get_standard_time(step)
            actual_time = steps_time.get(step, 0)
            ratio = actual_time / standard_time
            max_ratio = max(max_ratio, ratio)
    
        if max_ratio >= self.thresholds['red']:
            return 'red'
        elif max_ratio >= self.thresholds['yellow']:
            return 'yellow'
        return 'green'
        
    def get_standard_time(self, step: str) -> int:
        return self.settings['integration']['steps'][step]
