from typing import Dict
from .models.statistical import StatisticalModel
from .models.early_warning import EarlyWarningSystem
from .models.factor import FactorAnalysis
from .utils.calculations import calculate_final_estimate, calculate_parallel_time

class IntegrationPredictor:
    def __init__(self):
        self.statistical_model = StatisticalModel()
        self.early_warning = EarlyWarningSystem()
        self.factor_analysis = FactorAnalysis()
        
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

