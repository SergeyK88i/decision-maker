from typing import Dict
import yaml
from pathlib import Path

def load_settings():
    config_path = Path(__file__).parent.parent.parent / 'config' / 'settings.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_standard_time(step: str) -> int:
    settings = load_settings()
    return settings['integration']['steps'][step]

def calculate_final_estimate(stats: Dict, complexity: float, 
                           current_progress: Dict) -> float:
    base_time = get_standard_time(current_progress['step'])
    adjusted_time = base_time * complexity
    
    statistical_factor = stats['mean'] / base_time
    progress_factor = current_progress['days_spent'] / base_time
    
    return adjusted_time * statistical_factor * progress_factor
