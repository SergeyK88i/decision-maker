from typing import Dict
from .base import IntegrationHandler
from ..models.statistical import StatisticalModel
from ..utils.calculations import get_standard_time

class StatisticalHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.statistical_model = StatisticalModel()
        
    def handle(self, data: Dict) -> Dict:
        print("\n!!! StatisticalHandler STARTED !!!")
        print("\n=== StatisticalHandler START ===")
        print("1. Получены данные:", data)
         # 1. Получаем ML-риски (результат предыдущего обработчика)
        ml_results = data.get('ml_analysis', [])
        risk_level = next((r['risk_level'] for r in ml_results if r.get('risk_type') == 'schedule_risk'), 0)

        
        # 2. Берем свои базовые данные
        active_steps = data['current_progress']['active_parallel_steps']
        steps_time = data['current_progress']['steps_time']
        print("2. Активные шаги:", active_steps)
        print("3. Времена шагов:", steps_time)
        stats = {}
        for step in active_steps:
            # Базовая статистика
            base_metrics = self.statistical_model.calculate_metrics(step)
            print(f"4. Метрики для {step}:", base_metrics)

            # Корректируем с учетом ML-рисков
            adjusted_mean = base_metrics['mean'] * (1 + risk_level/100)

            current_time = steps_time.get(step, 0)
            stats[step] = {
                'metrics': base_metrics,
                'current_time': current_time,
                'standard_time': get_standard_time(step)
            }
        print("5. Итоговая статистика:", stats)
        data['statistical_analysis'] = stats
        print("=== StatisticalHandler END ===\n")
        return super().handle(data)
