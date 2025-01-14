from typing import Dict
from .base import IntegrationHandler
from ..models.statistical import StatisticalModel
from ..utils.calculations import get_standard_time
from ..predictor import IntegrationPredictor
class StatisticalHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.statistical_model = StatisticalModel()
        self.predictor = IntegrationPredictor()
        
    def handle(self, data: Dict) -> Dict:
        # print("\n=== StatisticalHandler START ===")
        # print("1. Получены данные:", data)
         # 1. Получаем ML-риски (результат предыдущего обработчика)
        ml_results = data.get('ml_analysis',{}).get('patterns',  [])
        risk_level = next((r['risk_level'] for r in ml_results if r.get('risk_type') == 'schedule_risk'), 0)

        
        # 2. Берем свои базовые данные
        active_steps = data['current_progress']['active_parallel_steps']
        steps_time = data['current_progress']['steps_time']
        # print("2. Активные шаги:", active_steps)
        # print("3. Времена шагов:", steps_time)
        stats = {}
        for step in active_steps:
            # Базовая статистика
            base_metrics = self.statistical_model.calculate_metrics(step)
            # print(f"4. Метрики для {step}:", base_metrics)

            # Корректируем с учетом ML-рисков
            adjusted_mean = base_metrics['mean'] * (1 + risk_level/100)

            current_time = steps_time.get(step, 0)
            stats[step] = {
                'metrics': base_metrics,
                'current_time': current_time,
                'standard_time': get_standard_time(step)
            }

        # Прогресс и baseline метрики    
        progress = self.calculate_progress_metrics(data)
        baseline = self.calculate_baseline_metrics(data)

        # print("5. Итоговая статистика:", stats)
        data['statistical_analysis'] = {
            'steps': stats,
            'progress': progress,
            'baseline': baseline
        }
        # print("=== StatisticalHandler END ===\n")
        return super().handle(data)

    def calculate_progress_metrics(self, data: Dict) -> Dict:
        progress = self.predictor.calculate_progress_estimate(data)
        return {
            'baseline_estimate': progress['baseline_estimate'],
            'days_spent': progress['days_spent'],
            'remaining_estimate': progress['remaining_estimate'],
            'completion_percent': progress['completion_percent'],
            'delay_factor': progress['delay_factor']
        }

    def calculate_baseline_metrics(self, data: Dict) -> Dict:
        initial = self.predictor.initial_estimate(data)
        return {
            'initial_estimate': initial['initial_estimate'],
            'standard_time': initial['standard_time'],
            'complexity': initial['complexity']
        }
