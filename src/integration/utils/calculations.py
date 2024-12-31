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

def calculate_critical_path(dependencies: Dict, steps_time: Dict) -> float:
    def get_path_time(step: str, visited: set) -> float:
        # print(f"Processing step: {step}")  # Debug print
        if step in visited:
            return 0
        visited.add(step)
        
        # Получаем время шага из steps_time или стандартное время
        step_time = steps_time.get(step, get_standard_time(step))
        # print(f"Step {step} time: {step_time}")

        # Если нет зависимостей, возвращаем время шага
        if not dependencies[step]:
            return step_time

        #Иначе время шага + максимальное время зависимостей 
        max_dep_time = max(
            get_path_time(dep, visited.copy()) 
            for dep in dependencies[step]
        )
        total_time = step_time + max_dep_time
        # print(f"Total time for {step}: {total_time}")
        return total_time


    # Находим конечные шаги (не имеют зависящих от них)
    end_steps = {s for s in dependencies if not any(s in deps for deps in dependencies.values())}
    
    # Вычисляем максимальное время критического пути
    return max(get_path_time(step, set()) for step in end_steps)

def calculate_final_estimate(stats: Dict, complexity: float, current_progress: Dict) -> float:
    dependencies = current_progress['steps_dependencies']
    steps_time = current_progress.get('steps_time', {})
    steps_history = current_progress.get('steps_history', {})
    
    # Рассчитываем базовое время по критическому пути
    critical_path_time = calculate_critical_path(dependencies, steps_time)
    
    # Рассчитываем тренд задержек
    delay_factor = 1.0
    if steps_history:
        delays = []
        for step in steps_history:
            standard_time = get_standard_time(step)
            actual_time = steps_history[step]  # Use steps_history instead of steps_time
            if standard_time > 0:
                delays.append(actual_time / standard_time)
        if delays:
            delay_factor = sum(delays) / len(delays)
    
    # Статистический фактор из исторических данных
    statistical_factor = stats['mean'] / stats['median'] if stats['median'] > 0 else 1.0
    
    # Прогресс текущих шагов
    active_steps = current_progress['active_parallel_steps']
    progress_factor = min(1.5,max(
        steps_time.get(step, 0) / get_standard_time(step)
        for step in active_steps
        if get_standard_time(step) > 0
    )) if active_steps else 1.0
    
    # Итоговый расчет с учетом всех факторов
    adjusted_time = (
        critical_path_time 
        * complexity 
        * delay_factor 
        * statistical_factor 
        * progress_factor
    )
    print(f"Calculation: {critical_path_time} * {complexity} * {delay_factor} * {statistical_factor} * {progress_factor} = {adjusted_time}")
    return adjusted_time


