from typing import Dict
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
        
    def check_status(self, step: str, days: float) -> str:
        standard_time = self.get_standard_time(step)
        ratio = days / standard_time
        
        if ratio >= self.thresholds['red']:
            return 'red'
        elif ratio >= self.thresholds['yellow']:
            return 'yellow'
        return 'green'
        
    def get_standard_time(self, step: str) -> int:
        return self.settings['integration']['steps'][step]
