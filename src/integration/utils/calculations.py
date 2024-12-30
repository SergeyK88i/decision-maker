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
    steps_history = current_progress.get('steps_history', {})
    dependencies = current_progress.get('steps_dependencies', {})
    parallel_steps = current_progress.get('parallel_steps', [])

    # Рассчитываем тренд задержек
    delay_factor = 1.0
    delay_penalty = 1.0
    if steps_history:
        delays = []
        max_parallel_time = 0

        for step, actual_time in steps_history.items():
            standard_time = get_standard_time(step)
            current_delay = actual_time / standard_time

            if step in parallel_steps:
                max_parallel_time = max(max_parallel_time, actual_time)
            else:
                delays.append(current_delay)
                # Добавляем штраф за каждую задержку
                if current_delay > 1:
                    overtime_percent = (current_delay - 1) * 100
                    delay_penalty *= (1 + overtime_percent / 100)
                    
        if max_parallel_time > 0:
            delays.append(max_parallel_time / max(get_standard_time(step) for step in parallel_steps))
        delay_factor = sum(delays) / len(delays)

    adjusted_time = base_time * complexity * delay_factor * delay_penalty
    statistical_factor = stats['mean'] / base_time
    progress_factor = current_progress['days_spent'] / base_time
    
    return adjusted_time * statistical_factor * progress_factor
