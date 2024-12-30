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

def calculate_parallel_time(current_progress: Dict) -> float:
    active_parallel = current_progress.get('active_parallel_steps', [])
    steps_time = current_progress.get('steps_time', {})
    
    if not active_parallel:
        return 0
        
    return max(steps_time.get(step, 0) for step in active_parallel)

def calculate_final_estimate(stats: Dict, complexity: float, current_progress: Dict) -> float:
    base_time = get_standard_time(current_progress['step'])
    steps_history = current_progress.get('steps_history', {})
    dependencies = current_progress.get('steps_dependencies', {})
    
    # Рассчитываем тренд задержек
    delay_factor = 1.0
    delay_penalty = 1.0
    
    if steps_history:
        delays = []
        
        # Получаем время параллельных шагов
        parallel_time = calculate_parallel_time(current_progress)
        
        for step, actual_time in steps_history.items():
            standard_time = get_standard_time(step)
            current_delay = actual_time / standard_time
            
            # Если шаг не в активных параллельных
            if step not in current_progress.get('active_parallel_steps', []):
                delays.append(current_delay)
                # Добавляем штраф за каждую задержку
                if current_delay > 1:
                    overtime_percent = (current_delay - 1) * 100
                    delay_penalty *= (1 + overtime_percent / 100)
        
        # Добавляем задержку от параллельных шагов
        if parallel_time > 0:
            parallel_delay = parallel_time / max(
                get_standard_time(step) 
                for step in current_progress.get('active_parallel_steps', [])
            )
            delays.append(parallel_delay)
            
        delay_factor = sum(delays) / len(delays)
    
    adjusted_time = base_time * complexity * delay_factor * delay_penalty
    statistical_factor = stats['mean'] / base_time
    
    # Используем время активного шага из steps_time
    current_step_time = current_progress.get('steps_time', {}).get(current_progress['step'], 0)
    progress_factor = current_step_time / base_time
    
    return adjusted_time * statistical_factor * progress_factor

