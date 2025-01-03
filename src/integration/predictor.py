from typing import Dict
from .models.statistical import StatisticalModel
from .models.early_warning import EarlyWarningSystem
from .models.factor import FactorAnalysis
from .utils.calculations import calculate_final_estimate, calculate_parallel_time, get_standard_time

class IntegrationPredictor:
    def __init__(self):
        self.statistical_model = StatisticalModel()
        self.early_warning = EarlyWarningSystem()
        self.factor_analysis = FactorAnalysis()
        
    def calculate_progress_estimate(self, source_data: Dict) -> Dict:
        # Получаем все шаги
        all_steps = source_data['current_progress']['steps_dependencies'].keys()
        
        # Baseline из статистики (34.8 дней)
        baseline_estimate = sum(
            self.statistical_model.calculate_metrics(step)['mean'] 
            for step in all_steps
        )
        
        steps_history = source_data['current_progress']['steps_history']
        
        # Фактически потраченное время
        days_spent = sum(steps_history.values())
        
        # Процент выполненных шагов
        completed_steps_percent = len(steps_history) / len(all_steps)
        
        # Расчет delay_factor
        delays = []
        for step, time in steps_history.items():
            standard = get_standard_time(step)
            delay = time / standard if standard > 0 else 1.0
            delays.append(delay)
        delay_factor = sum(delays) / len(delays) if delays else 1.0
        
        # Оценка оставшегося времени
        remaining_estimate = baseline_estimate * (1 - completed_steps_percent) * delay_factor
        
        return {
            'baseline_estimate': baseline_estimate,
            'days_spent': days_spent,
            'remaining_estimate': remaining_estimate,
            'total_estimate': days_spent + remaining_estimate,
            'completion_percent': completed_steps_percent * 100,
            'delay_factor': delay_factor
        }

    def predict_completion(self, source_data: Dict) -> Dict:
        active_steps = source_data['current_progress']['active_parallel_steps']
        steps_time = source_data['current_progress'].get('steps_time', {})
    
        # Получаем максимальное время из активных шагов
        current_step_time = max(steps_time.get(step, 0) for step in active_steps)
    
        # Получаем метрики для всех активных шагов
        stats = {
            step: self.statistical_model.calculate_metrics(step) 
            for step in active_steps
        }
        # Используем максимальные значения из статистики
        max_stats = {
            'mean': max(s['mean'] for s in stats.values()),
            'median': max(s['median'] for s in stats.values()),
            'std': max(s['std'] for s in stats.values())
        }
    
        warning_status = self.early_warning.check_status(active_steps, steps_time)
        complexity = self.factor_analysis.calculate_multiplier(
            source_data['characteristics']
        )
    
        parallel_time = calculate_parallel_time(source_data['current_progress'])
        
        estimated_days = calculate_final_estimate(
            stats=max_stats,
            complexity=complexity,
            current_progress=source_data['current_progress']
        )
        return {
            'estimated_days': estimated_days,
            'warning_status': warning_status,
            'complexity_factor': complexity,
            'statistical_data': max_stats
        }

    def initial_estimate(self, source_data: Dict) -> Dict:
        active_steps = source_data['current_progress']['active_parallel_steps']
        
        # Получаем статистику для активных шагов
        stats = {
            step: self.statistical_model.calculate_metrics(step) 
            for step in active_steps
        }
        
        # Максимальное среднее время из статистики
        max_stats = {
            'mean': max(s['mean'] for s in stats.values()),
            'median': max(s['median'] for s in stats.values()),
            'std': max(s['std'] for s in stats.values())
        }
        
        # Считаем сложность
        complexity = self.factor_analysis.calculate_multiplier(source_data['characteristics'])
        
        # Начальная оценка времени
        initial_time = max_stats['mean'] * complexity
        
        return {
            'initial_estimate': initial_time,
            'standard_time': max(get_standard_time(step) for step in active_steps),
            'complexity': complexity,
            'stats': max_stats
        }



