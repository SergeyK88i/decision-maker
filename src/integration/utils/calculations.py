from typing import Dict

def calculate_final_estimate(stats: Dict, complexity: float, 
                           current_progress: Dict) -> float:
    base_time = get_standard_time(current_progress['step'])
    adjusted_time = base_time * complexity
    
    # Учитываем статистику и текущий прогресс
    statistical_factor = stats['mean'] / base_time
    progress_factor = current_progress['days_spent'] / base_time
    
    return adjusted_time * statistical_factor * progress_factor

def get_standard_time(step: str) -> int:
    standard_times = {
        'step1': 3, 'step2': 7, 'step3': 5,
        'step4': 5, 'step5': 1, 'step6': 8, 'step7': 1
    }
    return standard_times[step]
