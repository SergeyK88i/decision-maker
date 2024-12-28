from typing import Dict
from .models.statistical import StatisticalModel
from .models.early_warning import EarlyWarningSystem
from .models.factor import FactorAnalysis
from .utils.calculations import calculate_final_estimate

class IntegrationPredictor:
    def __init__(self):
        self.statistical_model = StatisticalModel()
        self.early_warning = EarlyWarningSystem()
        self.factor_analysis = FactorAnalysis()
        
    def predict_completion(self, source_data: Dict) -> Dict:
        current_step = source_data['current_progress']['step']
        days_spent = source_data['current_progress']['days_spent']
        
        # Получаем данные из всех моделей
        stats = self.statistical_model.calculate_metrics(current_step)
        warning_status = self.early_warning.check_status(current_step, days_spent)
        complexity = self.factor_analysis.calculate_multiplier(
            source_data['characteristics']
        )
        
        # Рассчитываем финальную оценку
        estimated_days = calculate_final_estimate(
            stats=stats,
            complexity=complexity,
            current_progress=source_data['current_progress']
        )
        
        return {
            'estimated_days': estimated_days,
            'warning_status': warning_status,
            'complexity_factor': complexity,
            'statistical_data': stats
        }
