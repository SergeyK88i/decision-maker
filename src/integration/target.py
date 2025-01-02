from typing import Dict
import math
from .utils.calculations import get_standard_time
from .models.statistical import StatisticalModel

class IntegrationTarget:
    def __init__(self):
        self.target_days = 30
        self.statistical_model = StatisticalModel()
        
    def calculate_target(self, actual_days: float, steps_history: Dict, current_step: int) -> Dict:
        # История выполненных шагов
        historical_time = sum(steps_history.values())

        # Получаем статистику для текущего шага
        stats = self.statistical_model.calculate_metrics(f'step{current_step}')

        # Текущее время из actual_days
        current_time = actual_days - historical_time

        # Считаем оставшееся время на невыполненные шаги
        remaining_steps_time = sum(get_standard_time(f'step{i}') for i in range(current_step + 1, 8))

        # Анализируем историю выполнения
        delays = []
        for step, time in steps_history.items():
            standard = get_standard_time(step)
            delay = time / standard
            delays.append(delay)

        # Средний процент задержек
        avg_delay = sum(delays) / len(delays) if delays else 1.0
    
        # Прогноз с учетом истории
        # predicted_days = actual_days * avg_delay
        predicted_days = actual_days


        # Общий прогноз времени
        total_time = (
            historical_time * 1.0 +  # Фактическое время - точное
            current_time * (1 + stats['std']) +  # Текущее время + погрешность
            remaining_steps_time * 1.2  # Будущее время с запасом
        )


        # Если уже превысили целевое время - вероятность 0
        if total_time > self.target_days:
            completion_rate = 0
        else:
            # Вероятность уложиться в срок
            # Чем больше запас по времени, тем выше вероятность
                buffer = (self.target_days - total_time) / self.target_days
                completion_rate = min(0.9, buffer)  # Нормализуем до 100%        
            
        return {
            'on_time': predicted_days <= self.target_days,
            'deviation_days': predicted_days - self.target_days,
            'completion_rate': completion_rate,
            'historical_delay': avg_delay,
            'remaining_time': remaining_steps_time,
            'historical_time': historical_time,
            'total_time': total_time
        }
